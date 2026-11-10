import uuid

import streamlit as st

from core.api import MathAPIError
from core.config import API_BASE_URL
from core.state import record_answer


def show_api_error(exc: MathAPIError) -> None:
    if exc.status_code in (401, 403):
        st.session_state.api_key = None
        st.error("The demo API key is no longer valid. Refresh the page to create a new demo session.")
    elif exc.status_code == 404:
        st.info("No matching content was found in MathAPI.")
    elif exc.status_code == 429:
        st.warning("The hourly API limit has been reached. Try again later or use cached pages.")
    elif exc.status_code == 503:
        st.error("MathAPI is unavailable. Start the local API and try again.")
        st.caption(f"Expected API URL: {API_BASE_URL}")
    else:
        st.error(exc.message)


def render_text(text: str | None) -> None:
    value = str(text or "").strip()
    if value:
        st.markdown(rf"{value}")


def render_formula(code: str | None) -> None:
    value = str(code or "").strip()
    if not value:
        return
    if value.startswith("$$") and value.endswith("$$"):
        value = value[2:-2]
    elif value.startswith("\\[") and value.endswith("\\]"):
        value = value[2:-2]
    elif value.startswith("$") and value.endswith("$"):
        value = value[1:-1]
    st.latex(value)


def format_items(values: list[str] | None) -> str:
    items = [str(value) for value in (values or []) if value]
    return ", ".join(items) if items else "None"


def render_example(example: dict, index: int) -> None:
    with st.container(border=True):
        st.markdown(rf"**Example {index}**")
        st.caption(f"{example.get('difficulty', 'Unknown')} | {format_items(example.get('question_type'))}")
        render_text(example.get("question"))

        st.markdown(r"**Key observation**")
        render_text(example.get("key_observation"))
        st.caption(f"Concepts: {format_items(example.get('concept_used'))}")

        formulae = example.get("formulae_used") or []
        if formulae:
            st.markdown(r"**Formulae used**")
            for formula in formulae:
                st.markdown(rf"*{formula.get('title', 'Formula')}*")
                render_formula(formula.get("code"))

        steps = example.get("steps") or []
        if steps:
            with st.expander("View solution steps", expanded=False):
                for step_index, step in enumerate(steps, start=1):
                    st.markdown(rf"**Step {step_index}**")
                    render_text(step)

        st.markdown(r"**Answer**")
        render_text(example.get("answer"))
        st.markdown(r"**Interpretation**")
        render_text(example.get("interpretation"))


def render_source(source: dict) -> None:
    with st.container(border=True):
        st.markdown(rf"**{source.get('title', 'Learning resource')}**")
        st.caption(source.get("type", "Resource"))
        link = source.get("link")
        if link:
            st.markdown(rf"[Open resource]({link})")


def render_quiz(questions: list[dict], quiz_key: str) -> None:
    if not questions:
        st.info("No questions are available for this selection.")
        return

    total = len(questions)
    signature = "||".join(str(question.get("question", "")) for question in questions)
    state_key = f"_quiz_{quiz_key}"
    state = st.session_state.get(state_key)

    if (
        not isinstance(state, dict)
        or state.get("signature") != signature
        or "token" not in state
    ):
        state = {
            "signature": signature,
            "token": uuid.uuid4().hex,
            "index": 0,
            "submitted": False,
            "selected": None,
            "results": [],
            "correct_answer": None,
            "is_correct": None,
        }
        st.session_state[state_key] = state

    index = state["index"]
    if index >= total:
        score = sum(1 for result in state["results"] if result)
        accuracy = round((score / total) * 100) if total else 0
        st.subheader("Session complete")
        first, second = st.columns(2)
        first.metric("Score", f"{score}/{total}")
        second.metric("Accuracy", f"{accuracy}%")
        st.progress(score / total)
        if score == total:
            st.success("All answers are correct.")
        else:
            st.info("Review the solution sources for the questions you missed.")
        if st.button("Start over", key=f"{state_key}_restart"):
            st.session_state.pop(state_key, None)
            st.rerun()
        return

    question = questions[index]
    st.progress(index / total, text=f"Question {index + 1} of {total}")
    metadata = [
        str(question.get("difficulty", "")),
        format_items(question.get("question_type")),
        str(question.get("expected_time_limit", "")),
    ]
    st.caption(" | ".join(item for item in metadata if item))
    render_text(question.get("question"))

    options = question.get("options") or {}
    for letter, option in options.items():
        with st.container(border=True):
            st.markdown(rf"**{letter}.** {option}")

    hint = question.get("hint")
    if hint:
        with st.expander("Hint"):
            render_text(hint)

    available = list(options.keys())
    if not available:
        st.warning("This question has no answer options.")
        return

    selected = st.radio(
        "Your answer",
        available,
        index=None,
        horizontal=True,
        key=f"{state_key}_choice_{state['token']}_{index}",
        disabled=bool(state.get("submitted")),
    )

    if not state.get("submitted"):
        if st.button(
            "Check answer",
            key=f"{state_key}_check_{index}",
            disabled=selected is None,
        ):
            correct_answer = str(question.get("answer", "")).strip().upper()
            is_correct = selected == correct_answer
            state["submitted"] = True
            state["selected"] = selected
            state["correct_answer"] = correct_answer
            state["is_correct"] = is_correct
            state["results"].append(is_correct)
            record_answer(question.get("topic_id"), is_correct)
            st.rerun()

    if state.get("submitted"):
        if state.get("is_correct"):
            st.success("Correct answer.")
        else:
            st.error(f"Incorrect. The correct answer is {state.get('correct_answer')}.")
        sources = question.get("solution_sources") or []
        if sources:
            st.markdown(r"**Solution sources**")
            for source in sources:
                title = source.get("source") or "Learning resource"
                link = source.get("link")
                if link:
                    st.markdown(rf"- [{title}]({link})")
                else:
                    st.markdown(rf"- {title}")

        next_label = "Next question" if index + 1 < total else "See results"
        if st.button(next_label, key=f"{state_key}_next_{index}"):
            state["index"] += 1
            state["submitted"] = False
            state["selected"] = None
            st.rerun()
