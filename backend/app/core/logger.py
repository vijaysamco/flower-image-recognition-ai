"""
FlowerVision AI

Application Logging Configuration
"""

import logging
import sys

from app.core.config import settings


def setup_logger() -> None:
    """
    Configure the root logger for the application.
    """

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Usually __name__ from the calling module.

    Returns:
        Configured logger instance.
    """

    return logging.getLogger(name)


# Configure logging when this module is imported
setup_logger()
