import streamlit as st

from core.api import MathAPIError, get_topics
from core.state import (
    clear_bookmarks,
    go_to,
    reset_progress,
    toggle_bookmark,
)
from core.ui import show_api_error


def saved_page() -> None:
    api_key = st.session_state.api_key

    try:
        topics = get_topics(api_key)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    topic_map = {topic.get("topic_id"): topic for topic in topics}
    saved_ids = sorted(st.session_state.bookmarks)

    st.title("Saved and Progress")
    st.caption("Bookmarks and quiz progress are kept only for the current session.")

    st.subheader("Saved topics")
    if not saved_ids:
        st.info("No topics have been saved in this session.")
    else:
        for topic_id in saved_ids:
            topic = topic_map.get(topic_id, {})
            with st.container(border=True):
                st.markdown(f"**{topic.get('topic_name', topic_id)}**")
                st.caption(topic_id)
                actions = st.columns(2)
                with actions[0]:
                    if st.button("Open topic", key=f"saved_open_{topic_id}"):
                        st.session_state.selected_topic = topic_id
                        go_to("topic")
                with actions[1]:
                    if st.button("Remove bookmark", key=f"saved_remove_{topic_id}"):
                        toggle_bookmark(topic_id)
                        st.rerun()

    st.divider()
    st.subheader("Session progress")
    progress = st.session_state.progress
    attempted = progress.get("attempted", 0)
    correct = progress.get("correct", 0)
    accuracy = round((correct / attempted) * 100) if attempted else 0

    first, second, third, fourth = st.columns(4)
    first.metric("Attempted", attempted)
    second.metric("Correct", correct)
    third.metric("Accuracy", f"{accuracy}%")
    fourth.metric("Best streak", progress.get("best_streak", 0))
    st.progress(correct / attempted if attempted else 0)

    topic_stats = progress.get("topics") or {}
    if topic_stats:
        st.markdown("**By topic**")
        for topic_id, stats in topic_stats.items():
            topic_name = topic_map.get(topic_id, {}).get("topic_name", topic_id)
            st.write(
                f"{topic_name}: {stats.get('correct', 0)}/{stats.get('attempted', 0)} correct"
            )

    st.divider()
    actions = st.columns(2)
    with actions[0]:
        if st.button("Reset progress", key="saved_reset_progress"):
            reset_progress()
            st.rerun()
    with actions[1]:
        if st.button("Clear bookmarks", key="saved_clear_bookmarks"):
            clear_bookmarks()
            st.rerun()
