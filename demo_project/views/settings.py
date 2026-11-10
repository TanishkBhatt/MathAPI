import streamlit as st

from core.api import MathAPIError, clear_api_cache, get_health
from core.config import API_BASE_URL, DEMO_EMAIL, DEMO_USERNAME
from core.state import mask_key


def settings_page() -> None:
    st.title("Settings")
    st.caption("Demo configuration and local API connection details.")

    st.subheader("Demo account")
    st.markdown(f"Username: `{st.session_state.get('api_username') or DEMO_USERNAME}`")
    st.markdown(f"Email: `{DEMO_EMAIL}`")
    st.markdown(f"API key: `{mask_key(st.session_state.get('api_key'))}`")
    st.markdown(f"Expiry: `{st.session_state.get('api_expiry') or 'Not available'}`")
    st.caption("MathLab signs in with this demo account at the start of every new session.")

    if st.button("Refresh demo session", key="settings_refresh_auth"):
        st.session_state.api_key = None
        st.session_state.auth_error = None
        st.rerun()

    st.divider()
    st.subheader("API connection")
    st.markdown(f"Base URL: `{API_BASE_URL}`")
    st.caption("MathLab connects only to the local MathAPI backend.")
    try:
        health = get_health()
        st.success("MathAPI is reachable.")
        st.caption(health.get("message", ""))
    except MathAPIError as exc:
        st.error(exc.message)
    st.caption("Start the local API before using the app.")

    st.divider()
    st.subheader("Data")
    if st.button("Clear cached API data", key="settings_clear_cache"):
        clear_api_cache()
        st.success("Cached API data cleared.")
    st.caption("Progress and bookmarks are session-only and reset when the session ends.")
