import json
import os
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    PlaywrightError = Exception
    expect = None
    sync_playwright = None


ROOT = Path(__file__).resolve().parents[1]
USER_ID = 123456789


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_server(base_url, timeout=20):
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with urlopen(f"{base_url}/api/health", timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as exc:
            last_error = exc
            time.sleep(0.2)
    raise RuntimeError(f"Server did not start: {last_error}")


class MockApi:
    def __init__(self, page, fallback=False):
        self.page = page
        self.fallback = fallback
        self.session_id = "ui-session-1"
        self.next_calls = 0
        self.last_answer_index = None
        self.last_start_body = None
        self.review_question = None
        page.route("**/api/**", self.handle)

    def handle(self, route):
        request = route.request
        path = urlparse(request.url).path
        method = request.method.upper()

        if path == "/api/web-config":
            return self.fulfill(route, {"single_user_id": USER_ID, "access_required": False})
        if path == "/api/health":
            return self.fulfill(route, {"ok": True})
        if path in ("/api/catalog", "/api/catalog/fast"):
            return self.fulfill(route, self.catalog_payload())
        if path == f"/api/profile/{USER_ID}":
            return self.fulfill(route, self.profile_payload())
        if path == f"/api/profile/{USER_ID}/summary":
            profile = self.profile_payload()
            return self.fulfill(
                route,
                {
                    "total_attempts": profile["total_attempts"],
                    "total_correct": profile["total_correct"],
                    "accuracy": profile["accuracy"],
                    "mastery": profile["mastery"],
                    "avg_time": profile["avg_time"],
                    "today_solved": profile["today_solved"],
                    "mistake_count": profile["mistake_count"],
                    "profile_sync": "summary",
                },
            )
        if path == f"/api/profile/{USER_ID}/recommendations":
            profile = self.profile_payload()
            return self.fulfill(
                route,
                {
                    "recommended_pattern_ids": profile["recommended_pattern_ids"],
                    "weak_patterns": profile["weak_patterns"],
                    "mistake_count": profile["mistake_count"],
                    "profile_sync": "recommendations",
                },
            )
        if path == f"/api/profile/{USER_ID}/progress":
            profile = self.profile_payload()
            return self.fulfill(
                route,
                {
                    "unlock_progress": profile["unlock_progress"],
                    "profile_sync": "progress",
                },
            )
        if path == f"/api/mistakes/{USER_ID}":
            return self.fulfill(route, self.mistakes_payload())
        if path == f"/api/reminders/{USER_ID}":
            return self.fulfill(route, {"enabled": True, "reminder_time": "20:00", "timezone": "Asia/Kolkata"})

        if path == "/api/session/start" and method == "POST":
            body = json.loads(request.post_data or "{}")
            self.last_start_body = body
            total = 1 if body.get("retry_mistakes") else min(int(body.get("target_count") or 1), 2)
            self.next_calls = 0
            return self.fulfill(
                route,
                {
                    "session_id": self.session_id,
                    "mode": body.get("mode", "quick"),
                    "total_questions": total,
                    "variant_count": len(body.get("pattern_ids") or []),
                    "pattern_names": ["Percentage Basics"],
                    "score": 0,
                    "answered": 0,
                },
            )

        if path == f"/api/session/{self.session_id}/next" and method == "POST":
            self.next_calls += 1
            question = self.question_payload(question_number=self.next_calls)
            self.review_question = question
            return self.fulfill(route, {"complete": False, "question": question})

        if path == f"/api/session/{self.session_id}/answer" and method == "POST":
            body = json.loads(request.post_data or "{}")
            self.last_answer_index = int(body.get("answer_index", -1))
            is_correct = self.last_answer_index == 2
            return self.fulfill(
                route,
                {
                    "is_correct": is_correct,
                    "correct_option_index": 2,
                    "correct_option": "40",
                    "explanation": "25% of 160 is 40.",
                    "score": 1 if is_correct else 0,
                    "answered": 1,
                    "total_questions": 1,
                    "time_taken": 4.2,
                    "complete": True,
                    "summary": {
                        "score": 1 if is_correct else 0,
                        "total_questions": 1,
                        "planned_total_questions": 1,
                        "answered": 1,
                        "accuracy": 100 if is_correct else 0,
                        "wrong_count": 0 if is_correct else 1,
                        "skipped_count": 0,
                        "stopped": False,
                        "pattern_names": ["Percentage Basics"],
                        "review_count": 1,
                    },
                },
            )

        if path == f"/api/session/{self.session_id}/review":
            selected = self.last_answer_index if self.last_answer_index is not None else 2
            return self.fulfill(
                route,
                {
                    "summary": {"score": 1, "total_questions": 1, "accuracy": 100, "review_count": 1},
                    "questions": [
                        {
                            "question_number": 1,
                            "question_text": "What is 25% of 160?",
                            "options": ["20", "30", "40", "50"],
                            "selected_option_index": selected,
                            "selected_option": ["20", "30", "40", "50"][selected],
                            "correct_option_index": 2,
                            "correct_option": "40",
                            "is_correct": selected == 2,
                            "is_skipped": False,
                            "explanation": "25% of 160 is 40.",
                            "difficulty": 2,
                            "time_taken": 4.2,
                            "pattern_id": 101,
                        }
                    ],
                },
            )

        return self.fulfill(route, {"detail": f"Unhandled mock route: {method} {path}"}, status=404)

    @staticmethod
    def fulfill(route, payload, status=200):
        route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps(payload),
        )

    def catalog_payload(self):
        source = "local" if self.fallback else "database"
        payload = {
            "categories": [
                {
                    "id": 1,
                    "name": "Quant",
                    "topics": [
                        {
                            "id": 11,
                            "name": "Percentage",
                            "description": "Percent concepts",
                            "pattern_count": 2,
                            "variant_count": 4,
                            "patterns": [
                                {
                                    "id": 101,
                                    "name": "Percentage Basics",
                                    "description": "Find percent values and conversions.",
                                    "difficulty": 1,
                                    "variant_count": 2,
                                },
                                {
                                    "id": 102,
                                    "name": "Successive Discounts",
                                    "description": "Multiple discount and change problems.",
                                    "difficulty": 2,
                                    "variant_count": 2,
                                },
                            ],
                        }
                    ],
                },
                {
                    "id": 2,
                    "name": "Reasoning",
                    "topics": [
                        {
                            "id": 21,
                            "name": "Direction",
                            "description": "Movement and turns.",
                            "pattern_count": 1,
                            "variant_count": 1,
                            "patterns": [
                                {
                                    "id": 201,
                                    "name": "Direction Turns",
                                    "description": "North, south, left, right turns.",
                                    "difficulty": 1,
                                    "variant_count": 1,
                                }
                            ],
                        }
                    ],
                },
                {"id": 3, "name": "Data Insights", "topics": []},
            ],
            "source": source,
        }
        if self.fallback:
            payload["warning"] = "Using the local practice catalog because the database is unavailable."
        return payload

    @staticmethod
    def profile_payload():
        return {
            "total_attempts": 12,
            "total_correct": 9,
            "accuracy": 75,
            "mastery": 58,
            "avg_time": 13.5,
            "today_solved": 8,
            "recommended_pattern_ids": [101],
            "weak_patterns": [
                {
                    "id": 101,
                    "name": "Percentage Basics",
                    "topic_name": "Percentage",
                    "mastery_score": 0.35,
                    "wrong_attempts": 3,
                }
            ],
            "mistake_count": 1,
            "smart_plan": {
                "coach_line": "Today revise these 2 weak patterns: Percentage Basics, Successive Discounts.",
                "revision_queue": [
                    {
                        "id": 101,
                        "name": "Percentage Basics",
                        "topic_name": "Percentage",
                        "mastery": 35,
                        "weakness_score": 72,
                        "open_mistakes": 1,
                        "reason": "1 open mistake",
                    },
                    {
                        "id": 102,
                        "name": "Successive Discounts",
                        "topic_name": "Percentage",
                        "mastery": 0,
                        "weakness_score": 64,
                        "open_mistakes": 0,
                        "reason": "New pattern baseline",
                    },
                ],
                "missions": [
                    {
                        "key": "solve_20",
                        "title": "Solve 20 questions",
                        "description": "Build daily volume without waiting for random topic selection.",
                        "progress": 8,
                        "target": 20,
                        "unit": "questions",
                        "percent": 40,
                        "completed": False,
                        "reward": {"xp": 120, "coins": 40, "streak_shields": 0},
                        "reward_claimed": False,
                        "action": {"type": "practice", "label": "Start 20Q", "pattern_ids": [101, 102], "mode": "focused", "target_count": 20},
                    },
                    {
                        "key": "improve_weak",
                        "title": "Improve one weak pattern",
                        "description": "Win 3 answers from one weak pattern to prove movement.",
                        "progress": 2,
                        "target": 3,
                        "unit": "wins",
                        "percent": 67,
                        "completed": False,
                        "reward": {"xp": 180, "coins": 55, "streak_shields": 0},
                        "reward_claimed": False,
                        "action": {"type": "practice", "label": "Drill weak", "pattern_ids": [101], "mode": "quick", "target_count": 5},
                    },
                    {
                        "key": "retry_5_mistakes",
                        "title": "Retry 5 mistakes",
                        "description": "Clear open mistakes before they become permanent weak spots.",
                        "progress": 1,
                        "target": 5,
                        "unit": "mistakes",
                        "percent": 20,
                        "completed": False,
                        "reward": {"xp": 150, "coins": 45, "streak_shields": 1},
                        "reward_claimed": False,
                        "action": {"type": "mistakes", "label": "Open mistakes", "pattern_ids": [], "mode": "quick", "target_count": 5},
                    },
                ],
                "wallet": {"xp": 420, "coins": 140, "streak_shields": 1, "level": 1, "next_level_xp": 500, "today_xp": 120, "today_coins": 40},
            },
            "unlock_progress": {
                "topics": [
                    {
                        "topic_id": 11,
                        "topic_name": "Percentage",
                        "category_name": "Quant",
                        "total_patterns": 2,
                        "practiced_patterns": 1,
                        "mastered_patterns": 0,
                        "avg_mastery": 0.35,
                    }
                ],
                "patterns": [
                    {
                        "id": 101,
                        "name": "Percentage Basics",
                        "description": "Find percent values and conversions.",
                        "topic_id": 11,
                        "topic_name": "Percentage",
                        "category_id": 1,
                        "category_name": "Quant",
                        "mastery_score": 0.35,
                        "total_attempts": 6,
                        "correct_attempts": 3,
                        "wrong_attempts": 3,
                        "avg_time_seconds": 12.4,
                        "last_practiced_at": "2026-06-03T10:00:00Z",
                        "weakness_score": 72,
                        "status": "learning",
                        "open_mistakes": 1,
                    },
                    {
                        "id": 102,
                        "name": "Successive Discounts",
                        "description": "Multiple discount and change problems.",
                        "topic_id": 11,
                        "topic_name": "Percentage",
                        "category_id": 1,
                        "category_name": "Quant",
                        "mastery_score": 0,
                        "total_attempts": 0,
                        "correct_attempts": 0,
                        "wrong_attempts": 0,
                        "avg_time_seconds": 0,
                        "last_practiced_at": None,
                        "weakness_score": 64,
                        "status": "locked",
                        "open_mistakes": 0,
                    },
                ],
            },
        }

    @staticmethod
    def mistakes_payload():
        return {
            "pattern_ids": [101],
            "mistakes": [
                {
                    "id": 501,
                    "pattern_id": 101,
                    "pattern_name": "Percentage Basics",
                    "topic_name": "Percentage",
                    "question_text": "What is 25% of 160?",
                    "options": ["20", "30", "40", "50"],
                    "correct_option_index": 2,
                    "selected_option_index": 1,
                    "correct_option": "40",
                    "selected_option": "30",
                    "explanation": "25% means one fourth, and one fourth of 160 is 40.",
                    "difficulty": 2,
                    "missed_count": 2,
                }
            ],
        }

    @staticmethod
    def question_payload(question_number=1):
        return {
            "question_number": question_number,
            "total_questions": 1,
            "question_text": "What is 25% of 160?",
            "options": ["20", "30", "40", "50"],
            "difficulty": 2,
            "pattern_id": 101,
            "score": 0,
        }


@unittest.skipUnless(HAS_PLAYWRIGHT, "Playwright is not installed. Run `pip install -r requirements-dev.txt`.")
class PlaywrightUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        env = os.environ.copy()
        env.setdefault("GROQ_API_KEY", "test-key")
        env.setdefault("WEB_SINGLE_USER_ID", str(USER_ID))
        cls.server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "web_app:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(cls.port),
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            wait_for_server(cls.base_url)
            cls.playwright = sync_playwright().start()
            cls.browser = cls.playwright.chromium.launch(headless=True)
        except PlaywrightError as exc:
            cls.tearDownClass()
            raise unittest.SkipTest(
                "Playwright browser runtime is not installed. Run `python -m playwright install chromium`."
            ) from exc
        except Exception:
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        browser = getattr(cls, "browser", None)
        if browser:
            browser.close()
        playwright = getattr(cls, "playwright", None)
        if playwright:
            playwright.stop()
        server = getattr(cls, "server", None)
        if server and server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 390, "height": 844})
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def open_app(self, fallback=False):
        self.api = MockApi(self.page, fallback=fallback)
        self.page.goto(f"{self.base_url}/?user_id={USER_ID}&v=ui-test")
        expect(self.page.locator("#practiceScreen")).to_be_visible()
        expect(self.page.locator("#catalogStatus")).to_contain_text("Ready" if not fallback else "Local")

    def select_percentage_pattern(self):
        self.page.locator('[data-category-id="1"]').click()
        self.page.locator('[data-topic-id="11"]').click()
        self.page.locator('[data-pattern-id="101"]').click()
        expect(self.page.locator("#selectedPatternCount")).to_have_text("1")
        expect(self.page.locator("#startButton")).to_be_enabled()

    def test_navigation_setup_and_mode_controls(self):
        self.open_app()

        expect(self.page.locator('[data-screen-target="practice"]')).to_be_visible()
        expect(self.page.locator('[data-screen-target="progress"]')).to_be_visible()
        expect(self.page.locator("#smartCoachCard")).to_have_count(0)
        self.assertIn("is-active", self.page.locator('[data-mode="quick"]').get_attribute("class") or "")

        self.page.locator('[data-mode="focused"]').click()
        expect(self.page.locator("#selectedModeLabel")).to_have_text("Focused 20")
        self.page.locator('[data-mode="full"]').click()
        expect(self.page.locator("#selectedModeLabel")).to_have_text("All Variants")

        self.select_percentage_pattern()
        expect(self.page.locator("#selectionList")).to_contain_text("Percentage Basics")
        expect(self.page.locator("#variantCount")).to_contain_text("variants")

    def test_practice_flow_answer_submit_result_and_review(self):
        self.open_app()
        self.select_percentage_pattern()

        self.page.locator("#startButton").click()
        expect(self.page.locator("#questionScreen")).to_be_visible()
        expect(self.page.locator("#questionScore")).to_have_text("0")
        expect(self.page.locator("#questionStreak")).to_have_text("0x")
        expect(self.page.locator("#questionCombo")).to_contain_text("Ready")
        expect(self.page.locator("#questionText")).to_have_text("What is 25% of 160?")
        expect(self.page.locator("#optionsGrid [data-answer-index]")).to_have_count(4)
        expect(self.page.locator("#stopPracticeButton")).to_be_visible()

        self.page.locator('[data-answer-index="2"]').click()
        expect(self.page.locator("#feedbackTitle")).to_have_text("Correct")
        expect(self.page.locator("#questionScore")).to_have_text("1")
        expect(self.page.locator("#questionStreak")).to_have_text("1x")
        expect(self.page.locator("#feedbackText")).to_contain_text("25% of 160 is 40")
        expect(self.page.locator("#nextButton")).to_have_text("View result")

        self.page.locator("#nextButton").click()
        expect(self.page.locator("#resultScreen")).to_be_visible()
        expect(self.page.locator("#resultScore")).to_have_text("1 / 1")
        expect(self.page.locator("#resultAccuracy")).to_contain_text("Accuracy 100")

        self.page.locator("#reviewAnswersButton").click()
        expect(self.page.locator("#reviewScreen")).to_be_visible()
        expect(self.page.locator("#reviewList")).to_contain_text("What is 25% of 160?")
        expect(self.page.locator("#reviewList")).to_contain_text("Correct answer")

    def test_progress_loading_skill_tree_mistake_book_and_retry(self):
        self.open_app()
        self.page.locator('[data-screen-target="progress"]').click()

        expect(self.page.locator("#progressScreen")).to_be_visible()
        expect(self.page.locator("#todaySolved")).to_have_text("8")
        expect(self.page.locator("#accuracyStat")).to_have_text("75%")
        expect(self.page.locator("#progressSnapshot")).to_contain_text("Mastery")
        expect(self.page.locator("#weeklyHeatmap")).to_be_visible()
        expect(self.page.locator("#weakRadar")).to_be_visible()
        expect(self.page.locator("#recoveryStats")).to_be_visible()
        expect(self.page.locator("#progressCategoryTabs")).to_contain_text("Quant")
        expect(self.page.locator("#progressTopicList")).to_contain_text("Percentage")
        expect(self.page.locator("#progressPatternList")).to_contain_text("Percentage Basics")
        expect(self.page.locator("#progressPatternDetail")).to_contain_text("Wrong")
        expect(self.page.locator("#weakList")).to_contain_text("Percentage Basics")

        expect(self.page.locator("#reminderEnabled")).to_be_checked()
        expect(self.page.locator("#mistakeList")).to_contain_text("Why this went wrong")
        expect(self.page.locator('[data-mistake-retry="501"]')).to_be_visible()
        expect(self.page.locator('[data-mistake-similar="101"]')).to_be_visible()
        expect(self.page.locator('[data-mistake-pattern="101"]')).to_be_visible()

        self.page.locator('[data-mistake-retry="501"]').click()
        expect(self.page.locator("#questionScreen")).to_be_visible()
        expect(self.page.locator("#questionText")).to_have_text("What is 25% of 160?")
        self.assertTrue(self.api.last_start_body["retry_mistakes"])
        self.assertEqual(self.api.last_start_body["mistake_ids"], [501])

    def test_database_fallback_local_catalog_banner(self):
        self.open_app(fallback=True)

        expect(self.page.locator("#statusBanner")).to_be_visible()
        expect(self.page.locator("#statusBanner")).to_contain_text("Using the local practice catalog")
        expect(self.page.locator("#catalogStatus")).to_have_text("Local")
        expect(self.page.locator("#categoryTabs")).to_contain_text("Quant")
        expect(self.page.locator("#topicList")).to_contain_text("Percentage")
        self.select_percentage_pattern()


if __name__ == "__main__":
    unittest.main()
