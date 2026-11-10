import streamlit as st

from core.api import MathAPIError, get_daily_challenge
from core.ui import render_quiz, show_api_error


def daily_page() -> None:
    api_key = st.session_state.api_key

    try:
        challenge = get_daily_challenge(api_key)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    st.title("Daily Challenge")
    st.caption(
        f"Challenge for {challenge.get('challenge_date', 'today')} | "
        f"{challenge.get('total_questions', 0)} questions"
    )

    questions = challenge.get("questions") or []
    if not questions:
        st.info("No daily challenge is available right now.")
        return

    render_quiz(questions, f"daily_{challenge.get('challenge_date', 'today')}")
