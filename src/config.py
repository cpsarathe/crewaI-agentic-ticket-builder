"""Shared configuration for UI + agent pipeline.

The Streamlit UI writes `ui_config.json` at the project root. This module provides a
single place for the agent pipeline to load that config and apply sensible defaults.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


DEFAULT_CONFIG = {
    "classification_threshold": 0.75,
    "default_priority": "Medium",
    "priority_map": {
        "Bug": "High",
        "Feature Request": "Medium",
        "Complaint": "High",
        "Praise": "Low",
        "Spam": "Low",
        "Other": "Low",
    },
}


def config_path() -> Path:
    # Stored next to `app.py` when running `streamlit run app.py`
    return Path("ui_config.json")


def load_config() -> dict:
    path = config_path()
    if path.exists():
        try:
            return {**DEFAULT_CONFIG, **json.loads(path.read_text())}
        except Exception:
            logging.getLogger(__name__).exception(
                "Failed to load ui_config.json; using DEFAULT_CONFIG"
            )
            return dict(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


@dataclass(frozen=True)
class AgentConfig:
    classification_threshold: float
    default_priority: str
    priority_map: Dict[str, str]

    @staticmethod
    def from_dict(d: dict) -> "AgentConfig":
        cfg = {**DEFAULT_CONFIG, **(d or {})}
        return AgentConfig(
            classification_threshold=float(cfg.get("classification_threshold", 0.75)),
            default_priority=str(cfg.get("default_priority", "Medium")),
            priority_map=dict(cfg.get("priority_map", {})),
        )
