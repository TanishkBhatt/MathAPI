import streamlit as st

from core.api import MathAPIError, get_daily_challenge, get_health, get_topics
from core.state import go_to
from core.ui import show_api_error


def dashboard_page() -> None:
    api_key = st.session_state.api_key

    try:
        topics = get_topics(api_key)
        daily = get_daily_challenge(api_key)
        health = get_health()
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    st.title("MathLab")
    st.caption("A mathematics learning workspace powered by MathAPI.")

    branches = sorted({branch for topic in topics for branch in (topic.get("branch") or [])})
    total_questions = sum(int(topic.get("questions_available", 0)) for topic in topics)
    total_examples = sum(int(topic.get("examples_available", 0)) for topic in topics)

    first, second, third, fourth = st.columns(4)
    first.metric("Topics", len(topics))
    second.metric("Branches", len(branches))
    third.metric("Questions", total_questions)
    fourth.metric("Examples", total_examples)

    st.caption(health.get("message", "Connected to MathAPI."))
    if branches:
        st.caption(f"Available branches: {', '.join(branches)}")

    st.divider()
    st.subheader("Today's challenge")
    with st.container(border=True):
        question_count = daily.get("total_questions", 0)
        st.markdown(f"**{question_count} questions for {daily.get('challenge_date', 'today')}**")
        st.caption("One Beginner, one Intermediate, and one Advanced question.")
        if st.button("Open daily challenge", key="dashboard_open_daily"):
            go_to("daily")

    st.divider()
    st.subheader("Start learning")
    action_columns = st.columns(4)
    with action_columns[0]:
        if st.button("Explore topics", key="dashboard_explore"):
            go_to("topics")
    with action_columns[1]:
        if st.button("Practice arena", key="dashboard_practice"):
            go_to("practice")
    with action_columns[2]:
        if st.button("Random question", key="dashboard_random"):
            go_to("random")
    with action_columns[3]:
        if st.button("Formula vault", key="dashboard_formulae"):
            go_to("formulas")

    selected_topic = st.session_state.get("selected_topic")
    if selected_topic:
        current = next((topic for topic in topics if topic.get("topic_id") == selected_topic), None)
        if current:
            st.divider()
            st.subheader("Continue learning")
            with st.container(border=True):
                st.markdown(f"**{current.get('topic_name', selected_topic)}**")
                st.caption(
                    f"{current.get('difficulty', 'Unknown')} | "
                    f"{', '.join(current.get('branch') or [])}"
                )
                if st.button("Open topic studio", key="dashboard_continue"):
                    go_to("topic")

    if st.session_state.bookmarks:
        st.divider()
        st.caption(f"Saved topics in this session: {len(st.session_state.bookmarks)}")
        if st.button("View saved topics", key="dashboard_saved"):
            go_to("saved")
