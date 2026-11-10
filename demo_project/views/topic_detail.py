import streamlit as st

from core.api import (
    MathAPIError,
    get_examples,
    get_explanation,
    get_formulae,
    get_questions,
    get_sources,
    get_topics,
)
from core.config import DIFFICULTIES, QUESTION_TYPES
from core.state import go_to, is_bookmarked, toggle_bookmark
from core.ui import (
    format_items,
    render_example,
    render_formula,
    render_quiz,
    render_source,
    render_text,
    show_api_error,
)


def topic_page() -> None:
    api_key = st.session_state.api_key

    try:
        topics = get_topics(api_key)
    except MathAPIError as exc:
        show_api_error(exc)
        st.stop()

    if not topics:
        st.title("Topic Studio")
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
        "Choose a topic",
        list(labels),
        index=current_index,
        key=f"topic_detail_picker_{current_topic or 'default'}",
    )
    topic_id = labels[selected_label]
    st.session_state.selected_topic = topic_id
    topic = next(item for item in topics if item.get("topic_id") == topic_id)

    st.title(topic.get("topic_name", topic_id))
    st.caption(
        f"{topic_id} | {topic.get('difficulty', 'Unknown')} | "
        f"{format_items(topic.get('branch'))}"
    )

    actions = st.columns(2)
    with actions[0]:
        bookmark_label = "Remove bookmark" if is_bookmarked(topic_id) else "Save topic"
        if st.button(bookmark_label, key=f"bookmark_topic_{topic_id}"):
            toggle_bookmark(topic_id)
            st.rerun()
    with actions[1]:
        if st.button("Practice this topic", key=f"practice_topic_{topic_id}"):
            go_to("practice")

    metrics = st.columns(4)
    metrics[0].metric("Formulae", topic.get("formulae_available", 0))
    metrics[1].metric("Examples", topic.get("examples_available", 0))
    metrics[2].metric("Questions", topic.get("questions_available", 0))
    metrics[3].metric("Sources", topic.get("sources_available", 0))

    prerequisites = topic.get("prerequisites") or []
    related = topic.get("related_topics") or []
    sub_topics = topic.get("sub_topics") or []
    if prerequisites:
        st.caption(f"Prerequisites: {format_items(prerequisites)}")
    if related:
        st.caption(f"Related topics: {format_items(related)}")
    if sub_topics:
        st.caption(f"Sub-topics: {format_items(sub_topics)}")

    section = st.segmented_control(
        "Section",
        ["Overview", "Examples", "Practice", "Formulae", "Sources"],
        default="Overview",
        key=f"topic_section_{topic_id}",
        label_visibility="collapsed",
    )
    section = section or "Overview"

    if section == "Overview":
        try:
            explanation = get_explanation(api_key, topic_id)
        except MathAPIError as exc:
            show_api_error(exc)
            st.stop()

        st.subheader("Definition")
        render_text(explanation.get("definition"))
        st.subheader("Origin")
        render_text(explanation.get("origin"))

        applications = explanation.get("applications") or []
        if applications:
            st.subheader("Applications")
            for application in applications:
                st.markdown(f"- {application}")

        for item in explanation.get("explanation") or []:
            st.subheader(item.get("title", "Explanation"))
            render_text(item.get("content"))

    elif section == "Examples":
        try:
            examples = get_examples(api_key, topic_id, limit=20)
        except MathAPIError as exc:
            show_api_error(exc)
            st.stop()
        if not examples:
            st.info("No worked examples are available for this topic.")
        else:
            for index, example in enumerate(examples, start=1):
                render_example(example, index)

    elif section == "Practice":
        filters = st.columns(3)
        difficulty = filters[0].selectbox(
            "Difficulty",
            ["Any"] + DIFFICULTIES,
            key=f"topic_difficulty_{topic_id}",
        )
        question_type = filters[1].selectbox(
            "Question type",
            ["Any"] + QUESTION_TYPES,
            key=f"topic_type_{topic_id}",
        )
        limit = filters[2].slider(
            "Questions",
            1,
            10,
            5,
            key=f"topic_limit_{topic_id}",
        )
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

        st.caption(f"{len(questions)} questions loaded")
        render_quiz(
            questions,
            f"topic_practice_{topic_id}_{difficulty}_{question_type}_{limit}",
        )

    elif section == "Formulae":
        try:
            formulae = get_formulae(api_key, topic_id)
        except MathAPIError as exc:
            show_api_error(exc)
            st.stop()
        if not formulae:
            st.info("No formulae are available for this topic.")
        else:
            for formula in formulae:
                with st.container(border=True):
                    st.markdown(f"**{formula.get('title', 'Formula')}**")
                    render_formula(formula.get("code"))

    elif section == "Sources":
        try:
            sources = get_sources(api_key, topic_id)
        except MathAPIError as exc:
            show_api_error(exc)
            st.stop()
        if not sources:
            st.info("No learning sources are available for this topic.")
        else:
            for source in sources:
                render_source(source)
