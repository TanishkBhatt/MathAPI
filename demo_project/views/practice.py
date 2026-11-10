import streamlit as st

from core.api import MathAPIError, get_questions, get_topics
from core.config import DIFFICULTIES, QUESTION_TYPES
from core.ui import render_quiz, show_api_error


def practice_page() -> None:
    api_key = st.session_state.api_key

    try:
        topics = get_topics(api_key)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    st.title("Practice Arena")
    st.caption("Answer topic questions one at a time and track this session's score.")

    if not topics:
        st.info("No topics are available from MathAPI.")
        return

    labels = {
        f"{topic.get('topic_name', topic.get('topic_id'))} ({topic.get('topic_id')})": topic.get(
            "topic_id"
        )
        for topic in topics
    }
    values = list(labels.values())
    current_topic = st.session_state.get("selected_topic")
    current_index = values.index(current_topic) if current_topic in values else 0

    selected_label = st.selectbox(
        "Topic",
        list(labels),
        index=current_index,
        key=f"practice_topic_picker_{current_topic or 'default'}",
    )
    topic_id = labels[selected_label]
    st.session_state.selected_topic = topic_id

    filters = st.columns(3)
    difficulty = filters[0].selectbox("Difficulty", ["Any"] + DIFFICULTIES)
    question_type = filters[1].selectbox("Question type", ["Any"] + QUESTION_TYPES)
    limit = filters[2].slider("Number of questions", 1, 20, 10)

    try:
        questions = get_questions(
            api_key,
            topic_id,
            limit=limit,
            difficulty=None if difficulty == "Any" else difficulty,
            question_type=None if question_type == "Any" else question_type,
        )
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    st.caption(f"{len(questions)} questions loaded from {selected_label}")
    render_quiz(
        questions,
        f"practice_{topic_id}_{difficulty}_{question_type}_{limit}",
    )
