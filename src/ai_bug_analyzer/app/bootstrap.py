from __future__ import annotations

from app.config import AppConfig
from app.state import BugAnalyzerState
from infrastructure.logging.setup import configure_logging


def bootstrap_application() -> BugAnalyzerState:
    config = AppConfig()

    configure_logging()

    return BugAnalyzerState(
        project_path=config.project_path,
        entry_command=config.entry_command,
        test_command=config.test_command,
        max_iterations=config.max_iterations,
    )
