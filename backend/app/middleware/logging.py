"""
FlowerVision AI

Request Logging Middleware
"""

import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs incoming requests and outgoing responses.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process an incoming request and log its execution.
        """

        start_time = time.perf_counter()

        logger.info(
            "Incoming Request | %s %s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        logger.info(
            "Completed Request | %s %s | %d | %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response


def register_logging_middleware(app: FastAPI) -> None:
    """
    Register the logging middleware with the FastAPI application.
    """

    app.add_middleware(LoggingMiddleware)
