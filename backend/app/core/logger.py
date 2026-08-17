"""
FlowerVision AI

Application Logging Configuration
"""

import logging
import sys

from app.core.config import settings


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging() -> None:
    """
    Configure application-wide logging.

    This function is safe to call multiple times and avoids
    creating duplicate handlers.
    """

    root_logger = logging.getLogger()

    # Avoid duplicate handlers when running with
    # Uvicorn reload or during repeated imports.
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    handler.setFormatter(formatter)

    root_logger.addHandler(handler)

    root_logger.setLevel(
        logging.DEBUG if settings.DEBUG else logging.INFO
    )

    # Keep noisy third-party logs under control.
    logging.getLogger("uvicorn.access").setLevel(
        logging.INFO
    )

    logging.getLogger("uvicorn.error").setLevel(
        logging.INFO
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Logger name, normally __name__.

    Returns:
        Configured logging.Logger instance.
    """

    configure_logging()

    return logging.getLogger(name)


__all__ = [
    "configure_logging",
    "get_logger",
]