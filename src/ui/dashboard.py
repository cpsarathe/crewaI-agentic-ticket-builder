from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


TICKETS_CSV = Path("generated_tickets.csv")
LOG_CSV = Path("processing_log.csv")
METRICS_CSV = Path("metrics.csv")


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def render_dashboard(config: dict) -> None:
    """Dashboard: overview of processed feedback and generated tickets."""

    st.header("Dashboard")

    tickets = _load_csv(TICKETS_CSV)
    logs = _load_csv(LOG_CSV)

    total = int(len(tickets))
    new = int((tickets.get("status") == "New").sum()) if total else 0
    approved = int((tickets.get("status") == "Approved").sum()) if total else 0
    rejected = int((tickets.get("status") == "Rejected").sum()) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tickets", total)
    c2.metric("New", new)
    c3.metric("Approved", approved)
    c4.metric("Rejected", rejected)

    st.subheader("Latest tickets")
    if total:
        st.dataframe(tickets.tail(25), use_container_width=True, hide_index=True)
    else:
        st.info("No tickets yet. Use Manual Override → Start Processing.")

    st.subheader("Recent processing log")
    if len(logs):
        st.dataframe(logs.tail(25), use_container_width=True, hide_index=True)
    else:
        st.info("No log entries yet.")


def render_analytics(config: dict) -> None:
    """Analytics: statistics and performance metrics."""

    st.header("Analytics")

    metrics = _load_csv(METRICS_CSV)
    if metrics.empty:
        st.info("No metrics captured yet. Save/approve tickets to create snapshots.")
        return

    st.subheader("Metrics snapshots")
    st.dataframe(metrics.tail(50), use_container_width=True, hide_index=True)

    if "timestamp" in metrics.columns:
        metrics = metrics.set_index("timestamp")

    for col in ["tickets_total", "tickets_new", "tickets_approved", "tickets_rejected"]:
        if col in metrics.columns:
            st.subheader(col)
            st.line_chart(metrics[[col]])