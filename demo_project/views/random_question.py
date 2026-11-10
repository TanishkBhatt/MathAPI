import streamlit as st

from core.api import MathAPIError, get_random_question
from core.ui import render_quiz, show_api_error


def random_page() -> None:
    api_key = st.session_state.api_key
    st.title("Random Question")
    st.caption("Practice a question from the full MathAPI question pool.")

    if "random_nonce" not in st.session_state:
        st.session_state.random_nonce = 0
    if "random_question" not in st.session_state:
        st.session_state.random_question = None

    if st.button("Load another random question", key="random_reload"):
        st.session_state.random_nonce += 1
        st.session_state.random_question = None
        st.rerun()

    if st.session_state.random_question is None:
        try:
            with st.spinner("Loading a random question..."):
                st.session_state.random_question = get_random_question(api_key)
        except MathAPIError as exc:
            show_api_error(exc)
            st.stop()

    question = st.session_state.random_question
    if not question:
        st.info("No random question is available right now.")
        return

    st.caption(f"Topic: {question.get('topic_id', 'Unknown')}")
    render_quiz([question], f"random_{st.session_state.random_nonce}")
