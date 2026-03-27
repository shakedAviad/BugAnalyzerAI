from __future__ import annotations

import logging

DEFAULT_LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DEFAULT_LOG_LEVEL: int = logging.INFO


def configure_logging(log_level: int = DEFAULT_LOG_LEVEL) -> None:
    logging.basicConfig(
        level=log_level,
        format=DEFAULT_LOG_FORMAT,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
