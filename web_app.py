import os
import json
import random
import re
import secrets
import time
import logging
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
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
) or 1

INTERNAL_USER_ID = WEB_SINGLE_USER_ID

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
            return JSONResponse(status_code=401, content={"detail": "Open the private app link to use this web app."})
    return await call_next(request)


class StartSessionRequest(BaseModel):
    pattern_ids: list[int] = Field(default_factory=list)
    mode: str = "quick"
    target_count: Optional[int] = None
    adaptive: bool = True
    retry_mistakes: bool = False
    mistake_ids: list[int] = Field(default_factory=list)
    mistake_pattern_id: Optional[int] = None
    variant_selection: dict[str, list[str]] = Field(default_factory=dict)


class AnswerRequest(BaseModel):
    answer_index: int


class ReminderRequest(BaseModel):
    enabled: bool = False
    reminder_time: str = "20:00"
    timezone: str = "Asia/Kolkata"


SESSIONS: dict[str, dict[str, Any]] = {}
ENGAGEMENT_SCHEMA_READY = False
RESPONSE_CACHE: dict[tuple[str, Any], tuple[float, Any]] = {}
CACHE_TTL_SECONDS = {
    "catalog": 600,
    "pattern_details": 20,
    "profile_summary": 10,
    "recommendations": 15,
    "progress": 20,
}
MODE_TARGETS = {"quick": 10, "focused": 20, "full": None}


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/db-status")
def db_status():
    try:
        rows = db.execute_query(
            """
            SELECT
                current_database() as database,
                current_schema() as schema,
                (SELECT COUNT(*) FROM users) as users,
                (SELECT COUNT(*) FROM categories) as categories,
                (SELECT COUNT(*) FROM topics) as topics,
                (SELECT COUNT(*) FROM patterns) as patterns
            """
        )
        row = rows[0] if rows else {}
        return {
            "ok": True,
            "database": row.get("database"),
            "schema": row.get("schema"),
            "users": int(row.get("users") or 0),
            "categories": int(row.get("categories") or 0),
            "topics": int(row.get("topics") or 0),
            "patterns": int(row.get("patterns") or 0),
        }
    except Exception as exc:
        return JSONResponse(status_code=503, content={"ok": False, "error": _public_exception_message(exc), "database_url_set": bool(os.getenv("DATABASE_URL"))})


@app.get("/api/web-config")
def web_config():
    return {"single_user_id": WEB_SINGLE_USER_ID, "access_required": bool(WEB_ACCESS_KEY)}


def _ensure_engagement_schema():
    global ENGAGEMENT_SCHEMA_READY
    if ENGAGEMENT_SCHEMA_READY:
        return
    db.ensure_engagement_schema()
    ENGAGEMENT_SCHEMA_READY = True


@app.get("/api/catalog")
def catalog():
    cached = _cache_get("catalog", "database")
    if cached:
        return {**cached, "cached": True}
    try:
        payload = _build_database_catalog_payload()
        _cache_set("catalog", "database", payload)
        return payload
    except Exception as exc:
        logging.warning("Using local catalog fallback because database catalog is unavailable: %s", exc)
        return {"categories": get_local_catalog_payload(), "source": "local", "warning": f"Using the local practice catalog because the database is unavailable. {_public_exception_message(exc)}"}


@app.get("/api/catalog/fast")
def catalog_fast():
    cached = _cache_get("catalog", "database")
    if cached:
        return {**cached, "cached": True, "fast": True}
    return {"categories": get_local_catalog_payload(), "source": "local", "fast": True, "warning": "Showing instant local catalog while database catalog sync continues in the background."}


@app.get("/api/profile/{user_id}")
def profile(user_id: int):
    try:
        return {**_profile_summary(user_id), **_profile_progress(user_id)}
    except Exception as exc:
        logging.warning("Returning offline profile because database profile is unavailable: %s", exc)
        return _empty_profile(offline=True)


@app.get("/api/profile/{user_id}/summary")
def profile_summary(user_id: int):
    try:
        return _profile_summary(user_id)
    except Exception as exc:
        logging.warning("Returning offline profile summary because database is unavailable: %s", exc)
        return _empty_profile(offline=True)


@app.get("/api/profile/{user_id}/recommendations")
def profile_recommendations(user_id: int):
    try:
        return _profile_recommendations(user_id)
    except Exception as exc:
        logging.warning("Returning empty recommendations because database is unavailable: %s", exc)
        return {"weak_patterns": [], "recommended_pattern_ids": [], "mistake_count": 0, "offline": True}


@app.get("/api/profile/{user_id}/progress")
def profile_progress(user_id: int):
    try:
        return _profile_progress(user_id)
    except Exception as exc:
        logging.warning("Returning empty progress because database is unavailable: %s", exc)
        return {"unlock_progress": {"topics": [], "patterns": []}, "offline": True}


@app.post("/api/session/start")
def start_session(request: StartSessionRequest):
    if not request.pattern_ids and not request.retry_mistakes:
        raise HTTPException(status_code=400, detail="Select at least one pattern.")

    user_id = INTERNAL_USER_ID
    try:
        _ensure_user_row(user_id)
    except Exception as exc:
        logging.warning("Continuing without user persistence because registration failed: %s", exc)
        user_id = None

    mode_target = MODE_TARGETS.get(request.mode, MODE_TARGETS["quick"])
    if request.target_count:
        target_count = request.target_count
    elif mode_target is None:
        target_count = 0
    else:
        target_count = mode_target

    prefilled_questions = []
    if request.retry_mistakes:
        if not user_id:
            raise HTTPException(status_code=400, detail="Mistake retry needs a synced user profile.")
        prefilled_questions, session_items, pattern_names = _build_mistake_session_items(
            user_id,
            request.mistake_ids,
            request.mistake_pattern_id,
            target_count or 20,
        )
        if not prefilled_questions:
            raise HTTPException(status_code=404, detail="No open mistakes found for retry.")
        target_count = len(prefilled_questions)
    else:
        variant_selection = _normalize_variant_selection(request.variant_selection)
        session_items, pattern_names = _build_session_items(
            request.pattern_ids,
            user_id=user_id,
            adaptive=request.adaptive,
            variant_selection=variant_selection,
        )
        if not session_items:
            raise HTTPException(status_code=404, detail="No unlocked patterns found.")
        if target_count == 0:
            target_count = len(session_items)

    if request.mode == "full":
        target_count = max(target_count, len(session_items))

    queue = _build_adaptive_queue(session_items, user_id=user_id, adaptive=request.adaptive and not request.retry_mistakes)

    session_id = uuid4().hex
    session_pattern_ids = request.pattern_ids or list(dict.fromkeys(item["pattern_id"] for item in session_items if item.get("pattern_id")))
    session = {
        "id": session_id,
        "user_id": user_id,
        "mode": request.mode,
        "session_type": "mistake_retry" if request.retry_mistakes else request.mode,
        "pattern_ids": session_pattern_ids,
        "pattern_names": pattern_names,
        "adaptive": request.adaptive and not request.retry_mistakes,
        "items": session_items,
        "queue": queue,
        "pool": prefilled_questions.copy(),
        "current_question": None,
        "current_started_at": None,
        "current_index": 0,
        "total_questions": target_count,
        "score": 0,
        "wrong_patterns": [],
        "history": [],
        "skipped_count": 0,
        "stopped": False,
        "persistent_session_created": False,
        "persistent_completed": False,
        "prefilled": False,
        "used_question_keys": set(),
        "used_question_texts": [],
        "started_at": time.time(),
    }

    if not prefilled_questions:
        _fill_question_pool(session, batch_size=target_count)
    generated_count = len(session["pool"])
    if generated_count <= 0:
        raise HTTPException(status_code=500, detail="Could not generate questions for this practice set.")
    if generated_count < target_count:
        raise HTTPException(
            status_code=503,
            detail=(
                f"Could only generate {generated_count} of {target_count} requested questions. "
                "Please retry this selection."
            ),
        )
    session["prefilled"] = True
    _start_persistent_session(session)

    SESSIONS[session_id] = session
    return _session_public(session)


@app.post("/api/session/{session_id}/next")
def next_question(session_id: str, background_tasks: BackgroundTasks):
    session = _get_session(session_id)
    if session.get("stopped"):
        return {"complete": True, "summary": _session_summary(session)}

    if session["current_index"] >= session["total_questions"]:
        return {"complete": True, "summary": _session_summary(session)}

    if session.get("current_question"):
        return {"complete": False, "question": _question_public(session)}

    if not session["pool"]:
        raise HTTPException(status_code=500, detail="No pre-generated question is available. Please start a new session.")

    question = session["pool"].pop(0)
    question["question_number"] = session["current_index"] + 1
    question["saved"] = False
    session["current_question"] = question
    session["current_started_at"] = time.monotonic()

    if not question.get("saved"):
        question["saved"] = True
        background_tasks.add_task(_save_question_once, {**question, "saved": False})
    return {"complete": False, "question": _question_public(session)}


@app.post("/api/session/{session_id}/answer")
def answer_question(session_id: str, request: AnswerRequest, background_tasks: BackgroundTasks):
    session = _get_session(session_id)
    if session.get("stopped"):
        raise HTTPException(status_code=409, detail="This practice session was stopped.")

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

    session["history"].append(_question_history_entry(question, request.answer_index, time_taken))
    background_tasks.add_task(_persist_question_result, session, dict(question), request.answer_index, is_correct, time_taken)

    session["current_index"] += 1
    session["current_question"] = None
    session["current_started_at"] = None
    complete = session["current_index"] >= session["total_questions"]
    if complete:
        background_tasks.add_task(_complete_persistent_session, session, "completed")

    return {
        "is_correct": is_correct,
        "correct_option_index": question["correct_option_index"],
        "correct_option": question["options"][question["correct_option_index"]],
        "explanation": question.get("explanation") or "",
        "score": session["score"],
        "answered": session["current_index"],
        "total_questions": session["total_questions"],
        "time_taken": time_taken,
        "complete": complete,
        "summary": _session_summary(session) if complete else None,
    }


@app.post("/api/session/{session_id}/stop")
def stop_session(session_id: str):
    session = _get_session(session_id)

    if session.get("stopped"):
        return {
            "summary": _session_summary(session),
            "questions": session.get("history", []),
        }

    question = session.get("current_question")
    if question:
        time_taken = round(time.monotonic() - (session.get("current_started_at") or time.monotonic()), 2)
        session["history"].append(_question_history_entry(question, None, time_taken, is_skipped=True))
        _persist_question_result(session, question, None, False, time_taken, is_skipped=True)
        session["skipped_count"] = session.get("skipped_count", 0) + 1
        session["current_index"] += 1

    session["stopped"] = True
    session["stopped_at"] = time.time()
    session["current_question"] = None
    session["current_started_at"] = None
    session["queue"] = []
    session["pool"] = []
    _complete_persistent_session(session, "stopped")

    return {
        "summary": _session_summary(session),
        "questions": session.get("history", []),
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
        _invalidate_profile_cache(user_id)
        return {"ok": True}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Could not update mistake: {exc}") from exc


@app.get("/api/reminders/{user_id}")
def reminder_settings(user_id: int):
    try:
        _ensure_engagement_schema()
        _ensure_user_row(user_id)
        return _reminder_public(db.get_reminder_settings(user_id))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Reminder settings unavailable: {exc}") from exc


@app.post("/api/reminders/{user_id}")
def update_reminder_settings(user_id: int, request: ReminderRequest):
    if not _valid_time(request.reminder_time):
        raise HTTPException(status_code=400, detail="Reminder time must be in HH:MM format.")
    try:
        _ensure_engagement_schema()
        _ensure_user_row(user_id)
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


def _cache_get(namespace: str, key: Any):
    cache_key = (namespace, key)
    item = RESPONSE_CACHE.get(cache_key)
    if not item:
        return None
    expires_at, payload = item
    if expires_at < time.time():
        RESPONSE_CACHE.pop(cache_key, None)
        return None
    return payload


def _cache_set(namespace: str, key: Any, payload: Any, ttl: Optional[int] = None):
    RESPONSE_CACHE[(namespace, key)] = (
        time.time() + (ttl or CACHE_TTL_SECONDS.get(namespace, 30)),
        payload,
    )


def _invalidate_profile_cache(user_id: Optional[int]):
    if not user_id:
        return
    for namespace in ("profile_summary", "recommendations", "progress", "pattern_details"):
        RESPONSE_CACHE.pop((namespace, int(user_id)), None)


def _normalize_variant_selection(raw_selection: Optional[dict[str, list[str] | str]]) -> dict[int, list[str]]:
    if not raw_selection:
        return {}

    normalized: dict[int, list[str]] = {}
    for pattern_key, values in raw_selection.items():
        if values is None:
            continue
        if isinstance(values, str):
            value_list = [values]
        else:
            value_list = values

        cleaned = []
        for value in value_list:
            item = str(value).strip()
            if item:
                cleaned.append(item)
        if cleaned:
            normalized[int(pattern_key)] = list(dict.fromkeys(cleaned))
    return normalized


def _build_database_catalog_payload():
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
                        "variant_names": variants,
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


def _profile_summary(user_id: int):
    cached = _cache_get("profile_summary", int(user_id))
    if cached:
        return {**cached, "cached": True}

    _ensure_engagement_schema()
    _ensure_user_row(user_id)
    rows = db.execute_query(
        """
        WITH progress AS (
            SELECT
                COALESCE(SUM(total_attempts), 0) as total_attempts,
                COALESCE(SUM(correct_attempts), 0) as total_correct,
                COALESCE(AVG(mastery_score), 0) as avg_mastery,
                COALESCE(AVG(avg_time_seconds), 0) as avg_time
            FROM user_progress
            WHERE user_id = %s
        ),
        today AS (
            SELECT COUNT(*) as today_solved
            FROM question_attempts
            WHERE user_id = %s
              AND created_at >= CURRENT_DATE
              AND COALESCE(is_skipped, FALSE) = FALSE
        ),
        mistakes AS (
            SELECT COUNT(*) as mistake_count
            FROM mistake_book
            WHERE user_id = %s AND status = 'open'
        )
        SELECT
            progress.total_attempts,
            progress.total_correct,
            progress.avg_mastery,
            progress.avg_time,
            today.today_solved,
            mistakes.mistake_count
        FROM progress, today, mistakes
        """,
        (user_id, user_id, user_id),
    )
    row = rows[0] if rows else {}
    total_attempts = int(row.get("total_attempts") or 0)
    total_correct = int(row.get("total_correct") or 0)
    payload = {
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "accuracy": round((total_correct / total_attempts) * 100, 1) if total_attempts else 0,
        "mastery": round(float(row.get("avg_mastery") or 0) * 100, 1),
        "avg_time": round(float(row.get("avg_time") or 0), 1),
        "today_solved": int(row.get("today_solved") or 0),
        "mistake_count": int(row.get("mistake_count") or 0),
        "profile_sync": "summary",
    }
    _cache_set("profile_summary", int(user_id), payload)
    return payload


def _profile_recommendations(user_id: int):
    cached = _cache_get("recommendations", int(user_id))
    if cached:
        return {**cached, "cached": True}

    _ensure_engagement_schema()
    _ensure_user_row(user_id)
    all_ranked_patterns = sorted(
        _cached_pattern_progress_details(user_id),
        key=lambda item: (-float(item.get("weakness_score") or 0), int(item.get("total_attempts") or 0), int(item.get("id") or 0)),
    )
    weak_rows = all_ranked_patterns[:5]
    mistakes = db.get_mistake_book(user_id, limit=6)
    revision_ids = [int(row["id"]) for row in all_ranked_patterns[:8] if row.get("id")]
    payload = {
        "weak_patterns": weak_rows or [],
        "recommended_pattern_ids": [row["id"] for row in weak_rows or []],
        "mistake_count": len(mistakes),
        "profile_sync": "recommendations",
    }
    _cache_set("recommendations", int(user_id), payload)
    return payload


def _profile_progress(user_id: int):
    cached = _cache_get("progress", int(user_id))
    if cached:
        return {**cached, "cached": True}

    _ensure_engagement_schema()
    _ensure_user_row(user_id)
    pattern_details = _cached_pattern_progress_details(user_id)
    payload = {
        "unlock_progress": _unlock_progress_from_pattern_details(pattern_details),
        "profile_sync": "progress",
    }
    _cache_set("progress", int(user_id), payload)
    return payload


def _cached_pattern_progress_details(user_id: int):
    cached = _cache_get("pattern_details", int(user_id))
    if cached:
        return cached
    rows = db.get_pattern_progress_details(user_id)
    _cache_set("pattern_details", int(user_id), rows)
    return rows


def _unlock_progress_from_pattern_details(pattern_details: list[dict[str, Any]]):
    topic_map: dict[int, dict[str, Any]] = {}
    for row in pattern_details or []:
        topic_id = int(row.get("topic_id") or 0)
        if not topic_id:
            continue
        topic = topic_map.setdefault(
            topic_id,
            {
                "topic_id": topic_id,
                "topic_name": row.get("topic_name") or "Topic",
                "category_name": row.get("category_name") or "Category",
                "total_patterns": 0,
                "practiced_patterns": 0,
                "mastered_patterns": 0,
                "_mastery_sum": 0.0,
            },
        )
        mastery = float(row.get("mastery_score") or 0)
        topic["total_patterns"] += 1
        topic["_mastery_sum"] += mastery
        if int(row.get("total_attempts") or 0) > 0:
            topic["practiced_patterns"] += 1
        if mastery >= 0.8:
            topic["mastered_patterns"] += 1

    topics = []
    for topic in topic_map.values():
        total = int(topic["total_patterns"] or 0)
        topic["avg_mastery"] = (topic.pop("_mastery_sum", 0.0) / total) if total else 0
        topics.append(topic)
    topics.sort(key=lambda item: (item.get("category_name") or "", item.get("topic_name") or ""))
    return {
        "topics": topics,
        "patterns": pattern_details or [],
    }


def _get_session(session_id: str):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session


def _ensure_user_row(user_id: int):
    db.register_user(user_id, None, "Web", "Learner")


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
    planned_total = session["total_questions"]
    review_count = len(session.get("history", []))
    stopped = bool(session.get("stopped"))
    total = review_count if stopped else planned_total
    score = session["score"]
    return {
        "score": score,
        "total_questions": total,
        "planned_total_questions": planned_total,
        "answered": review_count,
        "accuracy": round((score / total) * 100, 1) if total else 0,
        "wrong_count": len(session["wrong_patterns"]),
        "skipped_count": session.get("skipped_count", 0),
        "stopped": stopped,
        "pattern_names": session["pattern_names"],
        "review_count": review_count,
    }


def _start_persistent_session(session: dict[str, Any]):
    if not session.get("user_id"):
        return
    try:
        _ensure_engagement_schema()
        db.create_practice_session(
            session["user_id"],
            session["id"],
            session.get("session_type") or session["mode"],
            session.get("pattern_ids", []),
            session.get("pattern_names", []),
            session["total_questions"],
        )
        session["persistent_session_created"] = True
    except Exception as exc:
        logging.warning("Skipping practice session persistence because database is unavailable: %s", exc)


def _complete_persistent_session(session: dict[str, Any], status: str):
    if not session.get("user_id") or session.get("persistent_completed"):
        return
    try:
        _ensure_engagement_schema()
        summary = _session_summary(session)
        db.complete_practice_session(
            session["id"],
            summary["score"],
            summary["total_questions"],
            status=status,
            stopped=status == "stopped",
        )
        session["persistent_completed"] = True
    except Exception as exc:
        logging.warning("Skipping practice session completion persistence because database is unavailable: %s", exc)


def _persist_question_result(
    session: dict[str, Any],
    question: dict[str, Any],
    selected_option_index: Optional[int],
    is_correct: bool,
    time_taken: float,
    is_skipped: bool = False,
):
    user_id = session.get("user_id")
    pattern_id = question.get("pattern_id")
    if not user_id or not pattern_id:
        return

    try:
        _ensure_engagement_schema()
        if not is_skipped:
            db.update_user_progress(
                user_id,
                pattern_id,
                is_correct,
                5 if is_correct else 2,
                time_taken=time_taken,
            )

        db.record_question_attempt(
            user_id,
            pattern_id,
            is_correct,
            time_taken,
            session_uuid=session["id"],
            question_number=question.get("question_number"),
            question_text=question.get("question_text"),
            options=question.get("options", []),
            correct_option_index=question.get("correct_option_index"),
            selected_option_index=selected_option_index,
            explanation=question.get("explanation") or "",
            difficulty=question.get("difficulty", 3),
            is_skipped=is_skipped,
        )

        if not is_correct and not is_skipped and not is_local_pattern_id(pattern_id):
            db.record_mistake(
                user_id,
                pattern_id,
                question["question_text"],
                question.get("options", []),
                question["correct_option_index"],
                selected_option_index,
                question.get("explanation") or "",
                question.get("difficulty", 3),
            )
        elif is_correct and question.get("mistake_id"):
            db.mark_mistake_reviewed(user_id, question["mistake_id"])
        _invalidate_profile_cache(user_id)
    except Exception as exc:
        logging.warning("Skipping question result persistence because database is unavailable: %s", exc)


def _build_smart_daily_plan(
    weak_patterns: list[dict[str, Any]],
    mistakes: list[dict[str, Any]],
    today_summary: dict[str, Any],
    today_pattern_attempts: list[dict[str, Any]],
    mistake_retry_count: int,
):
    revision_queue = [_revision_item_public(row) for row in (weak_patterns or [])[:4]]
    revision_ids = [int(item["id"]) for item in revision_queue if item.get("id")]
    today_solved = int(today_summary.get("total_attempts") or 0)
    best_weak = _best_weak_pattern_today(today_pattern_attempts, revision_ids)
    mistake_target = 5
    mistake_progress = min(int(mistake_retry_count or 0), mistake_target)

    missions = [
        {
            "key": "solve_20",
            "title": "Solve 20 questions",
            "description": "Build daily volume without waiting for random topic selection.",
            "progress": min(today_solved, 20),
            "target": 20,
            "unit": "questions",
            "completed": today_solved >= 20,
            "reward": {"xp": 120, "coins": 40, "streak_shields": 0},
            "action": {
                "type": "practice",
                "label": "Start 20Q",
                "pattern_ids": revision_ids,
                "mode": "focused",
                "target_count": 20,
            },
        },
        {
            "key": "improve_weak",
            "title": "Improve one weak pattern",
            "description": "Win 3 answers from one weak pattern to prove movement.",
            "progress": min(best_weak["correct"], 3),
            "target": 3,
            "unit": "wins",
            "completed": best_weak["correct"] >= 3,
            "reward": {"xp": 180, "coins": 55, "streak_shields": 0},
            "focus_pattern_id": best_weak.get("pattern_id") or (revision_ids[0] if revision_ids else None),
            "focus_pattern_name": best_weak.get("pattern_name") or (revision_queue[0]["name"] if revision_queue else "weak pattern"),
            "action": {
                "type": "practice",
                "label": "Drill weak",
                "pattern_ids": [best_weak.get("pattern_id") or revision_ids[0]] if revision_ids else [],
                "mode": "quick",
                "target_count": 10,
            },
        },
        {
            "key": "retry_5_mistakes",
            "title": "Retry 5 mistakes",
            "description": "Clear open mistakes before they become permanent weak spots.",
            "progress": mistake_progress,
            "target": mistake_target,
            "unit": "mistakes",
            "completed": mistake_progress >= mistake_target,
            "reward": {"xp": 150, "coins": 45, "streak_shields": 1},
            "open_mistakes": len(mistakes or []),
            "action": {
                "type": "mistakes",
                "label": "Open mistakes" if mistakes else "No mistakes",
                "pattern_ids": [],
                "mode": "quick",
                "target_count": 5,
            },
        },
    ]

    for mission in missions:
        target = int(mission.get("target") or 0)
        progress = int(mission.get("progress") or 0)
        mission["percent"] = round((progress / target) * 100) if target else 0

    if revision_queue:
        names = ", ".join(item["name"] for item in revision_queue[:4])
        coach_line = f"Today revise these {len(revision_queue)} weak patterns: {names}."
    else:
        coach_line = "Start with a 5-question baseline so the coach can detect weak patterns."

    return {
        "coach_line": coach_line,
        "revision_queue": revision_queue,
        "missions": missions,
        "wallet": {"xp": 0, "coins": 0, "streak_shields": 0, "level": 1, "next_level_xp": 500},
    }


def _attach_daily_rewards(plan: dict[str, Any], earned_keys: set[str], wallet: dict[str, Any]):
    earned_keys = earned_keys or set()
    today_xp = 0
    today_coins = 0
    for mission in plan.get("missions", []):
        reward = mission.get("reward") or {}
        mission["reward_claimed"] = mission.get("key") in earned_keys
        if mission["reward_claimed"]:
            today_xp += int(reward.get("xp") or 0)
            today_coins += int(reward.get("coins") or 0)
    plan["wallet"] = {
        **(wallet or {}),
        "today_xp": today_xp,
        "today_coins": today_coins,
    }
    return plan


def _best_weak_pattern_today(today_pattern_attempts: list[dict[str, Any]], revision_ids: list[int]):
    rows = today_pattern_attempts or []
    by_id = {int(row.get("pattern_id") or 0): row for row in rows}
    ordered = [by_id[pattern_id] for pattern_id in revision_ids if pattern_id in by_id]
    if not ordered:
        return {"pattern_id": revision_ids[0] if revision_ids else None, "correct": 0, "attempts": 0}
    best = max(
        ordered,
        key=lambda row: (
            int(row.get("correct") or 0),
            int(row.get("attempts") or 0),
            -revision_ids.index(int(row.get("pattern_id") or 0)) if int(row.get("pattern_id") or 0) in revision_ids else 0,
        ),
    )
    return {
        "pattern_id": int(best.get("pattern_id") or 0),
        "pattern_name": best.get("pattern_name") or "",
        "correct": int(best.get("correct") or 0),
        "attempts": int(best.get("attempts") or 0),
    }


def _revision_item_public(row: dict[str, Any]):
    mastery = round(float(row.get("mastery_score") or 0) * 100)
    attempts = int(row.get("total_attempts") or 0)
    accuracy = float(row.get("accuracy") or 0)
    avg_time = float(row.get("avg_time_seconds") or 0)
    open_mistakes = int(row.get("open_mistakes") or 0)
    reason = "Build first signal"
    if open_mistakes:
        reason = f"{open_mistakes} open mistake{'s' if open_mistakes != 1 else ''}"
    elif attempts == 0:
        reason = "New pattern baseline"
    elif accuracy and accuracy < 65:
        reason = f"{round(accuracy)}% accuracy"
    elif avg_time >= 75:
        reason = f"{round(avg_time)}s average"
    elif mastery < 70:
        reason = f"{mastery}% mastery"

    return {
        "id": row.get("id"),
        "name": row.get("name") or "Practice pattern",
        "topic_name": row.get("topic_name") or "",
        "mastery": mastery,
        "weakness_score": round(float(row.get("weakness_score") or 0)),
        "open_mistakes": open_mistakes,
        "reason": reason,
    }


def _empty_smart_daily_plan():
    return {
        "coach_line": "Connect your profile and solve a few questions to unlock smart revision.",
        "revision_queue": [],
        "missions": [
            {
                "key": "solve_20",
                "title": "Solve 20 questions",
                "description": "Daily volume mission.",
                "progress": 0,
                "target": 20,
                "unit": "questions",
                "percent": 0,
                "completed": False,
                "reward": {"xp": 120, "coins": 40, "streak_shields": 0},
                "reward_claimed": False,
                "action": {"type": "practice", "label": "Start", "pattern_ids": [], "mode": "focused", "target_count": 20},
            },
            {
                "key": "improve_weak",
                "title": "Improve one weak pattern",
                "description": "Win 3 answers from one weak pattern.",
                "progress": 0,
                "target": 3,
                "unit": "wins",
                "percent": 0,
                "completed": False,
                "reward": {"xp": 180, "coins": 55, "streak_shields": 0},
                "reward_claimed": False,
                "action": {"type": "practice", "label": "Drill", "pattern_ids": [], "mode": "quick", "target_count": 10},
            },
            {
                "key": "retry_5_mistakes",
                "title": "Retry 5 mistakes",
                "description": "Clear saved mistakes.",
                "progress": 0,
                "target": 5,
                "unit": "mistakes",
                "percent": 0,
                "completed": False,
                "reward": {"xp": 150, "coins": 45, "streak_shields": 1},
                "reward_claimed": False,
                "action": {"type": "mistakes", "label": "Open mistakes", "pattern_ids": [], "mode": "quick", "target_count": 5},
            },
        ],
        "wallet": {"xp": 0, "coins": 0, "streak_shields": 0, "level": 1, "next_level_xp": 500, "today_xp": 0, "today_coins": 0},
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
        "recommended_pattern_ids": [],
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


def _public_exception_message(exc: Exception):
    message = str(exc).strip() or exc.__class__.__name__
    lowered = message.lower()
    if (
        "connection to server" in lowered
        and (
            "permission denied" in lowered
            or "timed out" in lowered
            or "is the server running on that host" in lowered
            or "failed" in lowered
        )
    ) or "could not translate host name" in lowered or "network is unreachable" in lowered:
        return (
            "Database cannot be reached from this environment. "
            "Using the local practice catalog. For live progress sync, run the app on Render "
            "or allow outbound Postgres TCP to Supabase."
        )
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        message = message.replace(database_url, "[DATABASE_URL]")
    message = re.sub(r"(postgres(?:ql)?://[^:\s]+:)[^@\s]+(@)", r"\1***\2", message)
    message = re.sub(r"(password=)[^\s]+", r"\1***", message, flags=re.IGNORECASE)
    return message[:600]


def _reminder_public(row):
    row = row or {}
    return {
        "enabled": bool(row.get("enabled")),
        "reminder_time": row.get("reminder_time") or "20:00",
        "timezone": row.get("timezone") or "Asia/Kolkata",
        "last_reminded_at": str(row.get("last_reminded_at") or "") or None,
    }


def _decode_json_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
            return decoded if isinstance(decoded, list) else []
        except Exception:
            return []
    return []


def _mistake_public(row):
    options = row.get("options") or []
    options = _decode_json_list(options)
    correct_index = row.get("correct_option_index")
    selected_index = row.get("selected_option_index")
    correct_option = options[correct_index] if isinstance(correct_index, int) and 0 <= correct_index < len(options) else None
    selected_option = options[selected_index] if isinstance(selected_index, int) and 0 <= selected_index < len(options) else None
    return {
        "id": row.get("id"),
        "pattern_id": row.get("pattern_id"),
        "pattern_name": row.get("pattern_name") or "Practice pattern",
        "topic_name": row.get("topic_name") or "",
        "question_text": row.get("question_text") or "",
        "options": options,
        "correct_option_index": correct_index,
        "selected_option_index": selected_index,
        "correct_option": correct_option,
        "selected_option": selected_option,
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
        "pattern_id": question.get("pattern_id"),
        "score": session["score"],
    }


def _question_history_entry(
    question: dict[str, Any],
    selected_option_index: Optional[int],
    time_taken: float,
    is_skipped: bool = False,
):
    options = question.get("options", [])
    correct_option_index = question.get("correct_option_index", 0)
    selected_option = None if selected_option_index is None else options[selected_option_index]
    correct_option = options[correct_option_index] if 0 <= correct_option_index < len(options) else ""
    is_correct = (selected_option_index == correct_option_index) if selected_option_index is not None else False

    return {
        "question_number": question.get("question_number"),
        "question_text": question.get("question_text"),
        "options": options,
        "selected_option_index": selected_option_index,
        "selected_option": selected_option,
        "correct_option_index": correct_option_index,
        "correct_option": correct_option,
        "is_correct": is_correct,
        "is_skipped": is_skipped,
        "explanation": question.get("explanation") or "",
        "difficulty": question.get("difficulty", 3),
        "time_taken": time_taken,
        "pattern_id": question.get("pattern_id"),
    }


def _build_session_items(
    pattern_ids: list[int],
    user_id: Optional[int] = None,
    adaptive: bool = True,
    variant_selection: Optional[dict[int, list[str]]] = None,
):
    session_items = []
    pattern_names = []
    ordered_pattern_ids = _order_pattern_ids_for_adaptive_practice(pattern_ids, user_id, adaptive)
    selected_variants_by_pattern = variant_selection or {}

    for pattern_id in ordered_pattern_ids:
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
            allowed_variants = selected_variants_by_pattern.get(int(pattern["id"]))
            if allowed_variants:
                filtered = [variant for variant in variants if variant in allowed_variants]
                invalid_variants = [variant for variant in allowed_variants if variant not in variants]
                if invalid_variants:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Variant selection is out of date for '{pattern['name']}'. "
                            "Reload the catalog and select the variants again."
                        ),
                    )
                variants = filtered
            session_items.extend({**base_item, "hybrid_type": variant} for variant in variants)
        else:
            session_items.append(base_item)

    return session_items, pattern_names


def _order_pattern_ids_for_adaptive_practice(pattern_ids: list[int], user_id: Optional[int], adaptive: bool):
    ordered_ids = [int(pattern_id) for pattern_id in pattern_ids if pattern_id]
    if not user_id or not adaptive:
        return ordered_ids
    remote_ids = [pattern_id for pattern_id in ordered_ids if not is_local_pattern_id(pattern_id)]
    local_ids = [pattern_id for pattern_id in ordered_ids if is_local_pattern_id(pattern_id)]
    if not remote_ids:
        return ordered_ids
    try:
        ranked = db.get_pattern_progress_details(user_id, remote_ids)
    except Exception as exc:
        logging.warning("Continuing without adaptive pattern ranking because database is unavailable: %s", exc)
        return ordered_ids

    ranked_ids = [
        int(row["id"])
        for row in sorted(
            ranked,
            key=lambda item: (
                -float(item.get("weakness_score") or 0),
                int(item.get("total_attempts") or 0),
                int(item.get("id") or 0),
            ),
        )
    ]
    missing_ids = [pattern_id for pattern_id in remote_ids if pattern_id not in ranked_ids]
    return ranked_ids + missing_ids + local_ids


def _build_adaptive_queue(session_items: list[dict[str, Any]], user_id: Optional[int], adaptive: bool):
    queue = session_items.copy()
    if not user_id or not adaptive:
        random.shuffle(queue)
        return queue

    score_by_pattern = {}
    pattern_ids = sorted({int(item["pattern_id"]) for item in queue if item.get("pattern_id") and not is_local_pattern_id(item["pattern_id"])})
    if pattern_ids:
        try:
            score_by_pattern = {
                int(row["id"]): float(row.get("weakness_score") or 0)
                for row in db.get_pattern_progress_details(user_id, pattern_ids)
            }
        except Exception as exc:
            logging.warning("Using shuffled queue because adaptive scores are unavailable: %s", exc)
            random.shuffle(queue)
            return queue

    random.shuffle(queue)
    queue.sort(key=lambda item: (-score_by_pattern.get(int(item.get("pattern_id") or 0), 0), int(item.get("difficulty") or 0)))
    return queue


def _build_mistake_session_items(user_id: int, mistake_ids: list[int], pattern_id: Optional[int], limit: int):
    rows = db.get_mistake_questions(
        user_id,
        mistake_ids=[int(item) for item in mistake_ids if item],
        pattern_id=pattern_id,
        limit=limit,
    )
    questions = []
    items_by_pattern = {}
    pattern_names = []

    for index, row in enumerate(rows, start=1):
        options = _decode_json_list(row.get("options"))
        if not row.get("pattern_id") or not options:
            continue
        pattern_name = row.get("pattern_name") or "Mistake pattern"
        if row["pattern_id"] not in items_by_pattern:
            items_by_pattern[row["pattern_id"]] = {
                "pattern_id": row["pattern_id"],
                "name": pattern_name,
                "topic_name": row.get("topic_name") or "",
                "description": "Mistake book retry",
                "difficulty": row.get("difficulty") or 3,
                "source": "mistake_book",
            }
            pattern_names.append(pattern_name)
        questions.append(
            {
                "pattern_id": row["pattern_id"],
                "question_text": row.get("question_text") or "",
                "options": options,
                "correct_option_index": row.get("correct_option_index") or 0,
                "explanation": row.get("explanation") or "",
                "difficulty": row.get("difficulty") or 3,
                "mistake_id": row.get("id"),
                "saved": True,
            }
        )

    random.shuffle(questions)
    return questions, list(items_by_pattern.values()), pattern_names


def _fill_question_pool(session: dict[str, Any], batch_size: int = 3):
    remaining = session["total_questions"] - session["current_index"]
    target_pool_size = min(len(session["pool"]) + batch_size, remaining)
    attempts = 0
    max_attempts = max(5, batch_size * 2)
    last_error = None

    while len(session["pool"]) < target_pool_size and attempts < max_attempts:
        attempts += 1
        needed_count = target_pool_size - len(session["pool"])
        selected_items = []
        while len(selected_items) < needed_count:
            if not session["queue"]:
                session["queue"] = _build_adaptive_queue(
                    session["items"],
                    user_id=session.get("user_id"),
                    adaptive=bool(session.get("adaptive")),
                )
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
            if pattern_id and q_key in recent_by_pattern.get(pattern_id, set()) and attempts < max_attempts:
                continue
            session["used_question_keys"].add(q_key)
            session["used_question_texts"].append(question.get("question_text", ""))
            session["pool"].append(question)
            if len(session["pool"]) >= target_pool_size:
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
