from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

_DEFAULT_LOG_PATH = Path("run.log")


def setup_logging(log_path: Optional[str | Path] = None) -> None:
    """Configure application-wide logging.

    - Logs to console + a file (default: capstone-crewai/run.log)
    - Idempotent: safe to call multiple times
    """
    path = Path(log_path) if log_path else _DEFAULT_LOG_PATH

    root = logging.getLogger()
    if getattr(root, "_configured_by_app", False):
        return

    root.setLevel(logging.INFO)

    fmt = (
        "%(asctime)s %(levelname)s %(name)s "
        "run_id=%(run_id)s "
        "msg=%(message)s"
    )

    class RunIdFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record.run_id = os.getenv("RUN_ID", "-")
            return True

    formatter = logging.Formatter(fmt)

    # Console
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.addFilter(RunIdFilter())

    # File
    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(formatter)
    fh.addFilter(RunIdFilter())

    root.addHandler(sh)
    root.addHandler(fh)
    root._configured_by_app = True  # type: ignore[attr-defined]


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
