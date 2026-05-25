import os
import random
import secrets
import time
import logging
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from database.db_manager import db
from llm.generator import generator
from local_catalog import get_local_catalog_payload, get_local_pattern, is_local_pattern_id


BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
WEB_SINGLE_USER_ID = None
WEB_ACCESS_KEY = (os.getenv("WEB_ACCESS_KEY") or "").strip()


def _parse_positive_int(value: Optional[str]):
    try:
        parsed = int(value or "")
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


WEB_SINGLE_USER_ID = _parse_positive_int(
    os.getenv("WEB_SINGLE_USER_ID")
    or os.getenv("WEB_USER_ID")
    or os.getenv("APP_USER_ID")
)

app = FastAPI(title="Aptitude Practice Mini App", version="0.1.0")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.middleware("http")
async def web_access_guard(request: Request, call_next):
    if WEB_ACCESS_KEY and request.url.path.startswith("/api/") and request.url.path != "/api/health":
        supplied = (
            request.headers.get("x-web-access-key")
            or request.query_params.get("access_key")
            or request.query_params.get("key")
            or ""
        )
        if not secrets.compare_digest(supplied, WEB_ACCESS_KEY):
            return JSONResponse(
                status_code=401,
                content={"detail": "Open the private app link to use this web app."},
            )
    return await call_next(request)


class TelegramUser(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class StartSessionRequest(BaseModel):
    pattern_ids: list[int] = Field(default_factory=list)
    mode: str = "quick"
    target_count: Optional[int] = None
    telegram_user: Optional[TelegramUser] = None


class AnswerRequest(BaseModel):
    answer_index: int


class ReminderRequest(BaseModel):
    enabled: bool = False
    reminder_time: str = "20:00"
    timezone: str = "Asia/Kolkata"


SESSIONS: dict[str, dict[str, Any]] = {}
ENGAGEMENT_SCHEMA_READY = False
MODE_TARGETS = {
    "quick": 5,
    "focused": 15,
    "full": None,
}


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/web-config")
def web_config():
    return {
        "single_user_id": WEB_SINGLE_USER_ID,
        "access_required": bool(WEB_ACCESS_KEY),
    }


def _ensure_engagement_schema():
    global ENGAGEMENT_SCHEMA_READY
    if ENGAGEMENT_SCHEMA_READY:
        return
    db.ensure_engagement_schema()
    ENGAGEMENT_SCHEMA_READY = True


@app.get("/api/catalog")
def catalog():
    try:
        categories = db.get_categories() or []
        payload = []

        for category in categories:
            topics = db.get_topics(category["id"]) or []
            topic_payload = []

            for topic in topics:
                patterns = db.get_patterns(topic["id"]) or []
                pattern_payload = []
                topic_variant_count = 0

                for pattern in patterns:
                    variants = generator.get_hybrid_variants(pattern["name"])
                    variant_count = len(variants) if variants else 1
                    topic_variant_count += variant_count
                    pattern_payload.append(
                        {
                            "id": pattern["id"],
                            "name": pattern["name"],
                            "description": pattern.get("description") or "",
                            "difficulty": pattern.get("difficulty_level") or 1,
                            "variant_count": variant_count,
                        }
                    )

                topic_payload.append(
                    {
                        "id": topic["id"],
                        "name": topic["name"],
                        "description": topic.get("description") or "",
                        "pattern_count": len(pattern_payload),
                        "variant_count": topic_variant_count,
                        "patterns": pattern_payload,
                    }
                )

            payload.append(
                {
                    "id": category["id"],
                    "name": category["name"],
                    "topics": topic_payload,
                }
            )

        return {"categories": payload, "source": "database"}
    except Exception as exc:
        logging.warning("Using local catalog fallback because database catalog is unavailable: %s", exc)
        return {
            "categories": get_local_catalog_payload(),
            "source": "local",
            "warning": "Using the local practice catalog because the database is unavailable.",
        }


@app.get("/api/profile/{user_id}")
def profile(user_id: int):
    try:
        _ensure_engagement_schema()
        stats = db.execute_query(
            """
            SELECT
                COALESCE(SUM(total_attempts), 0) as total_attempts,
                COALESCE(SUM(correct_attempts), 0) as total_correct,
                COALESCE(AVG(mastery_score), 0) as avg_mastery,
                COALESCE(AVG(avg_time_seconds), 0) as avg_time
            FROM user_progress
            WHERE user_id = %s
            """,
            (user_id,),
        )
        weak_rows = db.execute_query(
            """
            SELECT p.id, p.name, t.name as topic_name, up.mastery_score
            FROM user_progress up
            JOIN patterns p ON up.pattern_id = p.id
            JOIN topics t ON p.topic_id = t.id
            WHERE up.user_id = %s AND p.is_unlocked = TRUE
            ORDER BY up.mastery_score ASC, up.total_attempts DESC
            LIMIT 5
            """,
            (user_id,),
        )

        row = stats[0] if stats else {}
        total_attempts = int(row.get("total_attempts") or 0)
        total_correct = int(row.get("total_correct") or 0)
        accuracy = round((total_correct / total_attempts) * 100, 1) if total_attempts else 0
        mistakes = db.get_mistake_book(user_id, limit=6)
        unlock_progress = db.get_unlock_progress(user_id)

        return {
            "total_attempts": total_attempts,
            "total_correct": total_correct,
            "accuracy": accuracy,
            "mastery": round(float(row.get("avg_mastery") or 0) * 100, 1),
            "avg_time": round(float(row.get("avg_time") or 0), 1),
            "today_solved": db.get_today_solved_count(user_id),
            "weak_patterns": weak_rows or [],
            "mistake_count": len(mistakes),
            "unlock_progress": unlock_progress,
        }
    except Exception as exc:
        logging.warning("Returning offline profile because database profile is unavailable: %s", exc)
        return _empty_profile(offline=True)


@app.post("/api/session/start")
def start_session(request: StartSessionRequest):
    if not request.pattern_ids:
        raise HTTPException(status_code=400, detail="Select at least one pattern.")

    user_id = request.telegram_user.id if request.telegram_user else None
    if request.telegram_user:
        try:
            db.register_user(
                request.telegram_user.id,
                request.telegram_user.username,
                request.telegram_user.first_name,
                request.telegram_user.last_name,
            )
        except Exception as exc:
            logging.warning("Continuing without user persistence because registration failed: %s", exc)
            user_id = None

    session_items, pattern_names = _build_session_items(request.pattern_ids)
    if not session_items:
        raise HTTPException(status_code=404, detail="No unlocked patterns found.")

    mode_target = MODE_TARGETS.get(request.mode, MODE_TARGETS["quick"])
    if request.target_count:
        target_count = request.target_count
    elif mode_target is None:
        target_count = len(session_items)
    else:
        target_count = mode_target

    if request.mode == "full":
        target_count = max(target_count, len(session_items))

    queue = session_items.copy()
    random.shuffle(queue)

    session_id = uuid4().hex
    SESSIONS[session_id] = {
        "id": session_id,
        "user_id": user_id,
        "mode": request.mode,
        "pattern_ids": request.pattern_ids,
        "pattern_names": pattern_names,
        "items": session_items,
        "queue": queue,
        "pool": [],
        "current_question": None,
        "current_started_at": None,
        "current_index": 0,
        "total_questions": target_count,
        "score": 0,
        "wrong_patterns": [],
        "history": [],
        "used_question_keys": set(),
        "used_question_texts": [],
        "started_at": time.time(),
    }

    return _session_public(SESSIONS[session_id])


@app.post("/api/session/{session_id}/next")
def next_question(session_id: str):
    session = _get_session(session_id)
    if session["current_index"] >= session["total_questions"]:
        return {"complete": True, "summary": _session_summary(session)}

    if session.get("current_question"):
        return {"complete": False, "question": _question_public(session)}

    if not session["pool"]:
        _fill_question_pool(session)

    if not session["pool"]:
        raise HTTPException(status_code=500, detail="Could not generate a question.")

    question = session["pool"].pop(0)
    question["question_number"] = session["current_index"] + 1
    question["saved"] = False
    session["current_question"] = question
    session["current_started_at"] = time.monotonic()

    _save_question_once(question)
    return {"complete": False, "question": _question_public(session)}


@app.post("/api/session/{session_id}/answer")
def answer_question(session_id: str, request: AnswerRequest):
    session = _get_session(session_id)
    question = session.get("current_question")
    if not question:
        raise HTTPException(status_code=409, detail="No active question to answer.")

    if request.answer_index < 0 or request.answer_index >= len(question["options"]):
        raise HTTPException(status_code=400, detail="Invalid answer option.")

    is_correct = request.answer_index == question["correct_option_index"]
    time_taken = round(time.monotonic() - (session.get("current_started_at") or time.monotonic()), 2)
    pattern_id = question.get("pattern_id")

    if is_correct:
        session["score"] += 1
    elif pattern_id:
        session["wrong_patterns"].append(pattern_id)

    session["history"].append(
        {
            "question_number": question.get("question_number"),
            "question_text": question.get("question_text"),
            "options": question.get("options", []),
            "selected_option_index": request.answer_index,
            "selected_option": question["options"][request.answer_index],
            "correct_option_index": question["correct_option_index"],
            "correct_option": question["options"][question["correct_option_index"]],
            "is_correct": is_correct,
            "explanation": question.get("explanation") or "",
            "difficulty": question.get("difficulty", 3),
            "time_taken": time_taken,
            "pattern_id": pattern_id,
        }
    )

    if session.get("user_id") and pattern_id:
        try:
            _ensure_engagement_schema()
            db.update_user_progress(
                session["user_id"],
                pattern_id,
                is_correct,
                5 if is_correct else 2,
                time_taken=time_taken,
            )
            db.record_question_attempt(session["user_id"], pattern_id, is_correct, time_taken)
            if not is_correct and not is_local_pattern_id(pattern_id):
                db.record_mistake(
                    session["user_id"],
                    pattern_id,
                    question["question_text"],
                    question.get("options", []),
                    question["correct_option_index"],
                    request.answer_index,
                    question.get("explanation") or "",
                    question.get("difficulty", 3),
                )
        except Exception as exc:
            logging.warning("Skipping progress persistence because database is unavailable: %s", exc)

    session["current_index"] += 1
    session["current_question"] = None
    session["current_started_at"] = None

    return {
        "is_correct": is_correct,
        "correct_option_index": question["correct_option_index"],
        "correct_option": question["options"][question["correct_option_index"]],
        "explanation": question.get("explanation") or "",
        "score": session["score"],
        "answered": session["current_index"],
        "total_questions": session["total_questions"],
        "time_taken": time_taken,
        "complete": session["current_index"] >= session["total_questions"],
        "summary": _session_summary(session) if session["current_index"] >= session["total_questions"] else None,
    }


@app.get("/api/session/{session_id}/review")
def review_session(session_id: str):
    session = _get_session(session_id)
    return {
        "summary": _session_summary(session),
        "questions": session.get("history", []),
    }


@app.get("/api/mistakes/{user_id}")
def mistakes(user_id: int):
    try:
        _ensure_engagement_schema()
        rows = db.get_mistake_book(user_id, limit=20)
        return {
            "mistakes": [_mistake_public(row) for row in rows],
            "pattern_ids": db.get_mistake_pattern_ids(user_id, limit=10),
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Mistake book unavailable: {exc}") from exc


@app.post("/api/mistakes/{user_id}/{mistake_id}/reviewed")
def mark_mistake_reviewed(user_id: int, mistake_id: int):
    try:
        _ensure_engagement_schema()
        db.mark_mistake_reviewed(user_id, mistake_id)
        return {"ok": True}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not update mistake: {exc}") from exc


@app.get("/api/reminders/{user_id}")
def reminder_settings(user_id: int):
    try:
        _ensure_engagement_schema()
        return _reminder_public(db.get_reminder_settings(user_id))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Reminder settings unavailable: {exc}") from exc


@app.post("/api/reminders/{user_id}")
def update_reminder_settings(user_id: int, request: ReminderRequest):
    if not _valid_time(request.reminder_time):
        raise HTTPException(status_code=400, detail="Reminder time must be in HH:MM format.")
    try:
        _ensure_engagement_schema()
        return _reminder_public(
            db.upsert_reminder_settings(
                user_id,
                request.enabled,
                request.reminder_time,
                request.timezone or "Asia/Kolkata",
            )
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not save reminders: {exc}") from exc


def _get_session(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session


def _session_public(session: dict[str, Any]):
    return {
        "session_id": session["id"],
        "mode": session["mode"],
        "total_questions": session["total_questions"],
        "variant_count": len(session["items"]),
        "pattern_names": session["pattern_names"],
        "score": session["score"],
        "answered": session["current_index"],
    }


def _session_summary(session: dict[str, Any]):
    total = session["total_questions"]
    score = session["score"]
    return {
        "score": score,
        "total_questions": total,
        "accuracy": round((score / total) * 100, 1) if total else 0,
        "wrong_count": len(session["wrong_patterns"]),
        "pattern_names": session["pattern_names"],
        "review_count": len(session.get("history", [])),
    }


def _empty_profile(offline: bool = False):
    return {
        "total_attempts": 0,
        "total_correct": 0,
        "accuracy": 0,
        "mastery": 0,
        "avg_time": 0,
        "today_solved": 0,
        "weak_patterns": [],
        "mistake_count": 0,
        "unlock_progress": {"topics": [], "patterns": []},
        "offline": offline,
    }


def _valid_time(value: str):
    if not isinstance(value, str) or len(value) != 5 or value[2] != ":":
        return False
    hours, minutes = value.split(":")
    if not hours.isdigit() or not minutes.isdigit():
        return False
    return 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59


def _reminder_public(row):
    row = row or {}
    return {
        "enabled": bool(row.get("enabled")),
        "reminder_time": row.get("reminder_time") or "20:00",
        "timezone": row.get("timezone") or "Asia/Kolkata",
        "last_reminded_at": str(row.get("last_reminded_at") or "") or None,
    }


def _mistake_public(row):
    options = row.get("options") or []
    if isinstance(options, str):
        try:
            import json

            options = json.loads(options)
        except Exception:
            options = []
    return {
        "id": row.get("id"),
        "pattern_id": row.get("pattern_id"),
        "pattern_name": row.get("pattern_name") or "Practice pattern",
        "topic_name": row.get("topic_name") or "",
        "question_text": row.get("question_text") or "",
        "options": options,
        "correct_option_index": row.get("correct_option_index"),
        "selected_option_index": row.get("selected_option_index"),
        "explanation": row.get("explanation") or "",
        "difficulty": row.get("difficulty") or 3,
        "missed_count": row.get("missed_count") or 1,
    }


def _question_public(session: dict[str, Any]):
    question = session["current_question"]
    return {
        "question_number": question["question_number"],
        "total_questions": session["total_questions"],
        "question_text": question["question_text"],
        "options": question["options"],
        "difficulty": question.get("difficulty", 3),
        "score": session["score"],
    }


def _build_session_items(pattern_ids: list[int]):
    session_items = []
    pattern_names = []

    for pattern_id in pattern_ids:
        if is_local_pattern_id(pattern_id):
            pattern = get_local_pattern(pattern_id)
        else:
            try:
                rows = db.execute_query(
                    """
                    SELECT p.id, p.name, p.description, p.difficulty_level, t.name as topic_name
                    FROM patterns p
                    JOIN topics t ON p.topic_id = t.id
                    WHERE p.id = %s AND p.is_unlocked = TRUE
                    """,
                    (pattern_id,),
                )
            except Exception as exc:
                logging.warning("Skipping pattern %s because database lookup failed: %s", pattern_id, exc)
                rows = []

            if not rows:
                continue
            pattern = rows[0]

        pattern_names.append(pattern["name"])
        variants = generator.get_hybrid_variants(pattern["name"])
        base_item = {
            "pattern_id": pattern["id"],
            "name": pattern["name"],
            "topic_name": pattern.get("topic_name") or "",
            "description": pattern.get("description") or "",
            "difficulty": pattern.get("difficulty") or pattern.get("difficulty_level") or 2,
            "source": pattern.get("source") or "database",
        }
        if variants:
            session_items.extend({**base_item, "hybrid_type": variant} for variant in variants)
        else:
            session_items.append(base_item)

    return session_items, pattern_names


def _fill_question_pool(session: dict[str, Any], batch_size: int = 3):
    remaining = session["total_questions"] - session["current_index"]
    batch_size = min(batch_size, remaining)
    attempts = 0
    last_error = None

    while len(session["pool"]) < batch_size and attempts < 5:
        attempts += 1
        selected_items = []
        while len(selected_items) < batch_size:
            if not session["queue"]:
                session["queue"] = session["items"].copy()
                random.shuffle(session["queue"])
            selected_items.append(session["queue"].pop(0))

        patterns_info = []
        recent_by_pattern = {}
        for item in selected_items:
            if item.get("source") == "local":
                pattern = item
                difficulty = item.get("difficulty", 2)
                avoid_questions = session.get("used_question_texts", [])
            else:
                try:
                    rows = db.execute_query(
                        """
                        SELECT p.id, p.name, p.description, p.difficulty_level, t.name as topic_name
                        FROM patterns p
                        JOIN topics t ON p.topic_id = t.id
                        WHERE p.id = %s AND p.is_unlocked = TRUE
                        """,
                        (item["pattern_id"],),
                    )
                except Exception as exc:
                    logging.warning("Skipping pattern %s because database lookup failed: %s", item["pattern_id"], exc)
                    rows = []
                if not rows:
                    continue

                pattern = rows[0]
                difficulty = (
                    db.get_current_difficulty(session["user_id"], pattern["id"])
                    if session.get("user_id")
                    else pattern["difficulty_level"]
                )
                try:
                    avoid_questions = db.get_recent_questions(pattern["id"], limit=200)
                except Exception as exc:
                    logging.warning("Continuing without recent-question history because database is unavailable: %s", exc)
                    avoid_questions = []

            pattern_id = pattern.get("id") or pattern["pattern_id"]
            recent_by_pattern[pattern_id] = {_question_key(text) for text in avoid_questions}
            pattern_info = {
                "id": pattern_id,
                "name": pattern["name"],
                "topic_name": pattern["topic_name"],
                "description": pattern.get("description") or "",
                "difficulty": difficulty,
                "avoid_questions": list(avoid_questions) + session.get("used_question_texts", []),
            }
            if item.get("hybrid_type"):
                pattern_info["hybrid_type"] = item["hybrid_type"]
            patterns_info.append(pattern_info)

        questions, error = generator.generate_batch(patterns_info, count=len(patterns_info), rephrase_hybrids=False)
        last_error = error
        for question in questions or []:
            q_key = _question_key(question.get("question_text"))
            pattern_id = question.get("pattern_id")
            if q_key in session["used_question_keys"]:
                continue
            if pattern_id and q_key in recent_by_pattern.get(pattern_id, set()) and attempts < 5:
                continue
            session["used_question_keys"].add(q_key)
            session["used_question_texts"].append(question.get("question_text", ""))
            session["pool"].append(question)
            if len(session["pool"]) >= batch_size:
                break

    if last_error and not session["pool"]:
        raise HTTPException(status_code=500, detail=last_error)


def _question_key(question_text: Any):
    return " ".join(str(question_text or "").lower().split())


def _save_question_once(question: dict[str, Any]):
    if question.get("saved") or not question.get("pattern_id"):
        return
    if is_local_pattern_id(question["pattern_id"]):
        question["saved"] = True
        return
    try:
        db.save_question(
            question["pattern_id"],
            question["question_text"],
            question["options"],
            question["correct_option_index"],
            question.get("explanation") or "",
            question.get("difficulty", 3),
        )
    except Exception as exc:
        logging.warning("Skipping question persistence because database is unavailable: %s", exc)
    question["saved"] = True
