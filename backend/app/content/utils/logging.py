"""Configuración de logging."""

from __future__ import annotations

import logging
import os


def get_logger(name: str = "content") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(os.environ.get("CONTENT_LOG_LEVEL", "INFO"))
    return logger
