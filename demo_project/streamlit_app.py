import streamlit as st

from core.api import clear_api_cache
from core.config import API_BASE_URL, APP_NAME
from core.state import ensure_demo_auth, init_state, mask_key

from views.daily_challenge import daily_page
from views.dashboard import dashboard_page
from views.formula_vault import formula_page
from views.practice import practice_page
from views.random_question import random_page
from views.saved import saved_page
from views.settings import settings_page
from views.topic_detail import topic_page
from views.topics import topics_page

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

init_state()

if not ensure_demo_auth():
    st.title(APP_NAME)
    st.error("MathLab could not start a demo session.")
    st.code(st.session_state.get("auth_error") or "Unknown authentication error.")
    st.info(f"Start the MathAPI backend at {API_BASE_URL} and reload this page.")
    st.caption("Backend command: uv run uvs dev")
    st.stop()

pages = [
    st.Page(dashboard_page, title="Dashboard", default=True),
    st.Page(topics_page, title="Explore Topics"),
    st.Page(topic_page, title="Topic Studio"),
    st.Page(practice_page, title="Practice Arena"),
    st.Page(daily_page, title="Daily Challenge"),
    st.Page(random_page, title="Random Question"),
    st.Page(formula_page, title="Formula Vault"),
    st.Page(saved_page, title="Saved and Progress"),
    st.Page(settings_page, title="Settings"),
]

st.session_state["_pages"] = {
    "dashboard": pages[0],
    "topics": pages[1],
    "topic": pages[2],
    "practice": pages[3],
    "daily": pages[4],
    "random": pages[5],
    "formulas": pages[6],
    "saved": pages[7],
    "settings": pages[8],
}

navigation = st.navigation(pages)

with st.sidebar:
    st.caption("Demo session")
    st.caption(f"User: {st.session_state.get('api_username') or 'demo_project'}")
    st.caption(f"API key: {mask_key(st.session_state.get('api_key'))}")
    st.caption(f"Expires: {st.session_state.get('api_expiry') or 'Not available'}")
    st.caption(f"API: {API_BASE_URL}")

    if st.button("Refresh demo session", key="sidebar_refresh_auth"):
        st.session_state.api_key = None
        st.session_state.auth_error = None
        st.rerun()

    if st.button("Clear cached data", key="sidebar_clear_cache"):
        clear_api_cache()
        st.success("Cached data cleared.")

navigation.run()
