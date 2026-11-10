import streamlit as st

from core.api import MathAPIError, get_formulae, get_topics
from core.ui import render_formula, show_api_error


def formula_page() -> None:
    api_key = st.session_state.api_key

    try:
        topics = get_topics(api_key)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    st.title("Formula Vault")
    st.caption("Browse formula sheets by topic and render every expression with LaTeX.")

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
        key=f"formula_topic_picker_{current_topic or 'default'}",
    )
    topic_id = labels[selected_label]
    st.session_state.selected_topic = topic_id

    try:
        formulae = get_formulae(api_key, topic_id)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    search = st.text_input("Filter formulae", placeholder="Search by title or LaTeX content")
    if search:
        needle = search.lower()
        formulae = [
            formula
            for formula in formulae
            if needle in str(formula.get("title", "")).lower()
            or needle in str(formula.get("code", "")).lower()
        ]

    st.caption(f"{len(formulae)} formulae in {selected_label}")
    if not formulae:
        st.info("No formulae match this selection.")
        return

    for formula in formulae:
        with st.container(border=True):
            st.markdown(f"**{formula.get('title', 'Formula')}**")
            render_formula(formula.get("code"))
