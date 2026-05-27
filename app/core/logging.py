"""Logging configuration for the Cursor Memory Project backend."""

import logging
import sys

from app.core.config import Settings


_LOG_FORMATS = {
    "plain": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
    "compact": "%(levelname)s [%(name)s] %(message)s",
}


def configure_logging(settings: Settings) -> None:
    """Configure safe backend logging.

    Logging intentionally avoids request bodies, authorization headers,
    tokens, secrets, and memory-bank content.
    """
    log_level = getattr(logging, settings.log_level, logging.INFO)
    log_format = _LOG_FORMATS.get(settings.log_format, _LOG_FORMATS["plain"])

    logging.basicConfig(
        level=log_level,
        format=log_format,
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)
