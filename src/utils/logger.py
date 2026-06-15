"""Logging configuration.

Provides get_logger() so modules share a consistent format and level.
"""

from __future__ import annotations

import logging
import sys

from ..config import settings

_CONFIGURED = False


def _configure_root() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    root = logging.getLogger("bpo")
    root.setLevel(settings.log_level.upper())
    root.addHandler(handler)
    root.propagate = False
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger under the 'bpo' root."""
    _configure_root()
    short = name.replace("src.", "").replace("__main__", "main")
    return logging.getLogger(f"bpo.{short}")
