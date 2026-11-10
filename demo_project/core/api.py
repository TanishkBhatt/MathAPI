from typing import Any

import requests
import streamlit as st

from core.config import (
    API_BASE_URL,
    CONTENT_TTL,
    DAILY_TTL,
    REQUEST_TIMEOUT,
    TOPICS_TTL,
)


class MathAPIError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _error_message(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        payload = None

    detail = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict):
                parts.append(str(item.get("msg", item)))
            else:
                parts.append(str(item))
        detail = " ".join(parts)

    if detail:
        return str(detail)

    text = response.text.strip()
    return text or f"MathAPI returned HTTP {response.status_code}."


def _request_json(
    method: str,
    path: str,
    api_key: str | None = None,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> Any:
    headers = {"Accept": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key

    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            headers=headers,
            params=params,
            json=body,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise MathAPIError(
            f"Could not reach MathAPI at {API_BASE_URL}. Start the local API and try again."
        ) from exc

    if response.status_code >= 400:
        raise MathAPIError(_error_message(response), response.status_code)

    try:
        return response.json()
    except ValueError as exc:
        raise MathAPIError("MathAPI returned a response that was not valid JSON.") from exc


def authenticate(username: str, email: str) -> dict[str, Any]:
    return _request_json(
        "POST",
        "/auth",
        body={"username": username, "email": email},
    )


def get_health() -> dict[str, Any]:
    return _request_json("GET", "/")


@st.cache_data(ttl=TOPICS_TTL, show_spinner=False)
def get_topics(_api_key: str) -> list[dict[str, Any]]:
    payload = _request_json("GET", "/api/v1/topics", api_key=_api_key)
    return payload.get("topics", [])


@st.cache_data(ttl=CONTENT_TTL, show_spinner=False)
def get_explanation(_api_key: str, topic_id: str) -> dict[str, Any]:
    payload = _request_json(
        "GET",
        "/api/v1/explanation",
        api_key=_api_key,
        params={"topic_id": topic_id},
    )
    return payload.get("explanation", {})


@st.cache_data(ttl=CONTENT_TTL, show_spinner=False)
def get_examples(_api_key: str, topic_id: str, limit: int = 10) -> list[dict[str, Any]]:
    payload = _request_json(
        "GET",
        "/api/v1/examples",
        api_key=_api_key,
        params={"topic_id": topic_id, "limit": limit},
    )
    return payload.get("examples", [])


@st.cache_data(ttl=CONTENT_TTL, show_spinner=False)
def get_questions(
    _api_key: str,
    topic_id: str,
    limit: int = 10,
    difficulty: str | None = None,
    question_type: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {"topic_id": topic_id, "limit": limit}
    if difficulty:
        params["difficulty"] = difficulty
    if question_type:
        params["question_type"] = question_type
    payload = _request_json(
        "GET",
        "/api/v1/questions",
        api_key=_api_key,
        params=params,
    )
    return payload.get("questions", [])


@st.cache_data(ttl=CONTENT_TTL, show_spinner=False)
def get_formulae(_api_key: str, topic_id: str) -> list[dict[str, Any]]:
    payload = _request_json(
        "GET",
        "/api/v1/formulae",
        api_key=_api_key,
        params={"topic_id": topic_id},
    )
    return payload.get("formulae", [])


@st.cache_data(ttl=CONTENT_TTL, show_spinner=False)
def get_sources(_api_key: str, topic_id: str) -> list[dict[str, Any]]:
    payload = _request_json(
        "GET",
        "/api/v1/sources",
        api_key=_api_key,
        params={"topic_id": topic_id},
    )
    return payload.get("sources", [])


@st.cache_data(ttl=DAILY_TTL, show_spinner=False)
def get_daily_challenge(_api_key: str) -> dict[str, Any]:
    return _request_json("GET", "/api/v1/daily-challenge", api_key=_api_key)


def get_random_question(_api_key: str) -> dict[str, Any]:
    payload = _request_json("GET", "/api/v1/random-question", api_key=_api_key)
    return payload.get("question", {})


def clear_api_cache() -> None:
    get_topics.clear()
    get_explanation.clear()
    get_examples.clear()
    get_questions.clear()
    get_formulae.clear()
    get_sources.clear()
    get_daily_challenge.clear()
