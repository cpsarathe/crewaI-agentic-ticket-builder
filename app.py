"""Streamlit UI entrypoint.

Run:
  cd capstone-crewai
  streamlit run app.py
"""

import streamlit as st

from src.ui.config_sidebar import render_configuration_panel
from src.ui.dashboard import render_dashboard, render_analytics
from src.ui.processing import render_processing_and_override


def main() -> None:
    st.set_page_config(page_title="Feedback Analysis System", layout="wide")
    st.title("Intelligent User Feedback Analysis System")

    config = render_configuration_panel()

    tab_dash, tab_override, tab_analytics = st.tabs(
        ["Dashboard", "Manual Override", "Analytics"]
    )

    with tab_dash:
        render_dashboard(config)

    with tab_override:
        render_processing_and_override(config)

    with tab_analytics:
        render_analytics(config)


if __name__ == "__main__":
    main()