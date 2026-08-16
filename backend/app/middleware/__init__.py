"""
FlowerVision AI

Middleware Package
"""

from app.middleware.logging import register_logging_middleware

__all__ = [
    "register_logging_middleware",
]
