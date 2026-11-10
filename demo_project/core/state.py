from typing import Any

import streamlit as st

from core.api import MathAPIError, authenticate
from core.config import DEMO_EMAIL, DEMO_USERNAME


def init_state() -> None:
    defaults: dict[str, Any] = {
        "api_key": None,
        "api_username": None,
        "api_expiry": None,
        "auth_error": None,
        "selected_topic": None,
        "bookmarks": set(),
        "progress": {
            "attempted": 0,
            "correct": 0,
            "streak": 0,
            "best_streak": 0,
            "topics": {},
        },
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def ensure_demo_auth(force: bool = False) -> bool:
    if force:
        clear_auth()

    if st.session_state.get("api_key"):
        return True

    try:
        payload = authenticate(DEMO_USERNAME, DEMO_EMAIL)
    except MathAPIError as exc:
        st.session_state.auth_error = exc.message
        return False

    data = payload.get("api_key_data") or {}
    api_key = data.get("api_key")
    if not api_key:
        st.session_state.auth_error = "MathAPI did not return an API key for the demo account."
        return False

    st.session_state.api_key = api_key
    st.session_state.api_username = data.get("username", DEMO_USERNAME)
    st.session_state.api_expiry = data.get("expiry")
    st.session_state.auth_error = None
    return True


def clear_auth() -> None:
    st.session_state.api_key = None
    st.session_state.api_username = None
    st.session_state.api_expiry = None


def mask_key(api_key: str | None) -> str:
    if not api_key:
        return "Not available"
    if len(api_key) <= 12:
        return "*" * len(api_key)
    return f"{api_key[:8]}...{api_key[-4:]}"


def go_to(page_key: str) -> None:
    pages = st.session_state.get("_pages") or {}
    page = pages.get(page_key)
    if page is not None:
        st.switch_page(page)


def is_bookmarked(topic_id: str) -> bool:
    return topic_id in st.session_state.bookmarks


def toggle_bookmark(topic_id: str) -> None:
    bookmarks = st.session_state.bookmarks
    if topic_id in bookmarks:
        bookmarks.remove(topic_id)
    else:
        bookmarks.add(topic_id)
    st.session_state.bookmarks = bookmarks


def record_answer(topic_id: str | None, correct: bool) -> None:
    progress = st.session_state.progress
    progress["attempted"] += 1
    topic_key = topic_id or "unknown"
    topic_stats = progress["topics"].setdefault(
        topic_key,
        {"attempted": 0, "correct": 0},
    )
    topic_stats["attempted"] += 1

    if correct:
        progress["correct"] += 1
        progress["streak"] += 1
        topic_stats["correct"] += 1
        progress["best_streak"] = max(progress["best_streak"], progress["streak"])
    else:
        progress["streak"] = 0

    st.session_state.progress = progress


def reset_progress() -> None:
    st.session_state.progress = {
        "attempted": 0,
        "correct": 0,
        "streak": 0,
        "best_streak": 0,
        "topics": {},
    }


def clear_bookmarks() -> None:
    st.session_state.bookmarks = set()
