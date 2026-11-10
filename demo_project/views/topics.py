import streamlit as st

from core.api import MathAPIError, get_topics
from core.config import BRANCHES, DIFFICULTIES
from core.state import go_to
from core.ui import format_items, show_api_error


def topics_page() -> None:
    api_key = st.session_state.api_key

    try:
        topics = get_topics(api_key)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    st.title("Explore Topics")
    st.caption("Browse the full MathAPI catalog and open a topic workspace.")

    search = st.text_input(
        "Search topics",
        placeholder="Search by topic name or topic ID",
    )
    filters = st.columns(2)
    selected_branches = filters[0].multiselect("Branch", BRANCHES)
    selected_difficulty = filters[1].selectbox("Difficulty", ["All"] + DIFFICULTIES)

    filtered = []
    for topic in topics:
        topic_branches = topic.get("branch") or []
        haystack = f"{topic.get('topic_name', '')} {topic.get('topic_id', '')}".lower()

        if search and search.lower() not in haystack:
            continue
        if selected_branches and not set(selected_branches).intersection(topic_branches):
            continue
        if selected_difficulty != "All" and topic.get("difficulty") != selected_difficulty:
            continue
        filtered.append(topic)

    st.caption(f"{len(filtered)} of {len(topics)} topics shown")

    if not filtered:
        st.info("No topics match the selected filters.")
        return

    columns = st.columns(3)
    for index, topic in enumerate(filtered):
        topic_id = topic.get("topic_id", "")
        with columns[index % 3]:
            with st.container(border=True):
                st.subheader(topic.get("topic_name", topic_id))
                st.caption(topic_id)
                st.markdown(f"**Branch:** {format_items(topic.get('branch'))}")
                st.markdown(f"**Difficulty:** {topic.get('difficulty', 'Unknown')}")
                st.caption(
                    f"{topic.get('formulae_available', 0)} formulae | "
                    f"{topic.get('examples_available', 0)} examples | "
                    f"{topic.get('questions_available', 0)} questions | "
                    f"{topic.get('sources_available', 0)} sources"
                )
                prerequisites = topic.get("prerequisites") or []
                if prerequisites:
                    st.caption(f"Prerequisites: {format_items(prerequisites)}")
                if st.button("Open topic", key=f"open_topic_{topic_id}"):
                    st.session_state.selected_topic = topic_id
                    go_to("topic")
