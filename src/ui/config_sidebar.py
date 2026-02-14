import json
from pathlib import Path

import streamlit as st


_DEFAULT_CONFIG = {
    "classification_threshold": 0.75,
    "default_priority": "Medium",
    "priority_map": {
        "Bug": "High",
        "Feature Request": "Medium",
        "Complaint": "High",
        "Praise": "Low",
        "Other": "Low",
    },
}


def _config_path() -> Path:
    # Stored next to app.py when running `streamlit run app.py`
    return Path("ui_config.json")


def load_config() -> dict:
    path = _config_path()
    if path.exists():
        try:
            return {**_DEFAULT_CONFIG, **json.loads(path.read_text())}
        except Exception:
            return dict(_DEFAULT_CONFIG)
    return dict(_DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    _config_path().write_text(json.dumps(config, indent=2))


def render_configuration_panel() -> dict:
    """Configuration Panel.

    Requirements:
    - Adjust classification thresholds and priorities
    """

    with st.sidebar:
        st.header("Configuration Panel")

        cfg = load_config()

        threshold = st.slider(
            "Classification confidence threshold",
            0.0,
            1.0,
            float(cfg.get("classification_threshold", 0.75)),
            0.01,
        )

        default_priority = st.selectbox(
            "Default priority",
            options=["Critical", "High", "Medium", "Low"],
            index=["Critical", "High", "Medium", "Low"].index(
                cfg.get("default_priority", "Medium")
            ),
        )

        st.subheader("Category → Priority")
        priority_map = dict(cfg.get("priority_map", {}))
        for cat in ["Bug", "Feature Request", "Complaint", "Praise", "Other"]:
            priority_map[cat] = st.selectbox(
                cat,
                options=["Critical", "High", "Medium", "Low"],
                index=["Critical", "High", "Medium", "Low"].index(
                    priority_map.get(cat, default_priority)
                ),
                key=f"prio_{cat}",
            )

        if st.button("Save configuration"):
            save_config(
                {
                    "classification_threshold": float(threshold),
                    "default_priority": default_priority,
                    "priority_map": priority_map,
                }
            )
            st.success("Saved")

        return {
            "classification_threshold": float(threshold),
            "default_priority": default_priority,
            "priority_map": priority_map,
        }