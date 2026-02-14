from __future__ import annotations

import datetime as dt
from pathlib import Path
import uuid

import pandas as pd
import streamlit as st

from src.main import main as kickoff_agents


TICKETS_CSV = Path("expected_classifications.csv")
LOG_CSV = Path("processing_log.csv")
METRICS_CSV = Path("metrics.csv")

TICKETS_COLUMNS = [
    "source_id",
    "source_type",
    "category",
    "priority",
    "technical_details",
    "suggested_title",
]

LOG_COLUMNS = ["timestamp", "event", "details"]

METRICS_COLUMNS = [
    "timestamp",
    "tickets_total",
    "tickets_new",
    "tickets_approved",
    "tickets_rejected",
]


def _now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _ensure_csvs_exist() -> None:
    if not TICKETS_CSV.exists():
        pd.DataFrame(columns=TICKETS_COLUMNS).to_csv(TICKETS_CSV, index=False)
    if not LOG_CSV.exists():
        pd.DataFrame(columns=LOG_COLUMNS).to_csv(LOG_CSV, index=False)
    if not METRICS_CSV.exists():
        pd.DataFrame(columns=METRICS_COLUMNS).to_csv(METRICS_CSV, index=False)


def _append_log(event: str, details: str) -> None:
    _ensure_csvs_exist()
    df = pd.read_csv(LOG_CSV)
    df = pd.concat(
        [df, pd.DataFrame([{"timestamp": _now_iso(), "event": event, "details": details}])],
        ignore_index=True,
    )
    df.to_csv(LOG_CSV, index=False)


def _write_metrics_snapshot(tickets_df: pd.DataFrame) -> None:
    _ensure_csvs_exist()
    def _count(status: str) -> int:
        return int((tickets_df.get("status") == status).sum())

    snapshot = {
        "timestamp": _now_iso(),
        "tickets_total": int(len(tickets_df)),
        "tickets_new": _count("New"),
        "tickets_approved": _count("Approved"),
        "tickets_rejected": _count("Rejected"),
    }
    df = pd.read_csv(METRICS_CSV)
    df = pd.concat([df, pd.DataFrame([snapshot])], ignore_index=True)
    df.to_csv(METRICS_CSV, index=False)


def _load_tickets() -> pd.DataFrame:
    _ensure_csvs_exist()
    df = pd.read_csv(TICKETS_CSV)
    for col in TICKETS_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[TICKETS_COLUMNS]


def _save_tickets(df: pd.DataFrame) -> None:
    df = df.copy()
    for col in TICKETS_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df[TICKETS_COLUMNS].to_csv(TICKETS_CSV, index=False)
    _write_metrics_snapshot(df[TICKETS_COLUMNS])


def _seed_demo_ticket_if_empty(config: dict) -> None:
    df = _load_tickets()
    if len(df) > 0:
        return
    ticket = {
        "ticket_id": str(uuid.uuid4())[:8],
        "source_id": "demo-1",
        "source_type": "demo",
        "category": "Bug",
        "priority": "High",
        "technical_details": "Steps: login -> crash (demo)",
        "suggested_title": "Demo: crash on login",
    }
    _save_tickets(pd.concat([df, pd.DataFrame([ticket])], ignore_index=True))
    _append_log("seed", "Seeded demo ticket because generated_tickets.csv was empty")


def render_processing_and_override(config: dict) -> None:
    """Manual Override screen.

    Requirements:
    - Manual override: edit or approve generated tickets
    - Ensure output files exist with proper structure
    """

    _ensure_csvs_exist()
    _seed_demo_ticket_if_empty(config)

    st.header("Manual Override")

    st.subheader("Run processing")
    st.caption(
        "This calls your agent runner (`src.main.main`). "
        "If your crew writes its own CSVs, keep that logic there; UI will still manage the three required output files."
    )
    if st.button("Start Processing", type="primary"):
        import os
        run_id = str(uuid.uuid4())[:8]
        os.environ["RUN_ID"] = run_id
        _append_log("run_id", run_id)
        _append_log("processing_start", "User started processing")
        with st.spinner("Running agents..."):
            try:
                kickoff_agents()
                _append_log("processing_done", "Agents finished")
                st.success("Processing complete")
            except Exception as e:
               import traceback
               _append_log("processing_error", traceback.format_exc())
               st.error(f"Processing failed: {e}")

    st.markdown("---")

    st.subheader("Review / edit / approve tickets")
    tickets = _load_tickets()

    edited = st.data_editor(
        tickets,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "source_type": st.column_config.SelectboxColumn(
                "source_type",
                options=["User Review", "Support Email", "Feature Request", "demo"],
                required=True,
            ),
            "priority": st.column_config.SelectboxColumn(
                "priority",
                options=["Critical", "High", "Medium", "Low"],
                required=True,
            ),
            "category": st.column_config.SelectboxColumn(
                "category",
                options=["Bug", "Feature Request", "Complaint", "Praise", "Spam", "Other"],
                required=True,
            ),
            "status": st.column_config.SelectboxColumn(
                "status",
                options=["New", "Approved", "Rejected"],
                required=True,
            ),
        },
        hide_index=True,
        key="tickets_editor",
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save changes"):
            edited = edited.copy()
            edited["updated_at"] = _now_iso()
            _save_tickets(edited)
            _append_log("manual_save", f"Saved {len(edited)} tickets")
            st.success("Saved to generated_tickets.csv")

    with c2:
            st.success("Approved all New tickets")