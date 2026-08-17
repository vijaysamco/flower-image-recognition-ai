"""
FlowerVision AI

Request Logging Middleware
"""

import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for request/response logging.

    Logs request metadata and processing time without
    logging request bodies or uploaded image contents.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """
        Process and log an HTTP request.
        """

        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Store request ID so other application components
        # can access it if needed.
        request.state.request_id = request_id

        logger.info(
            "Request started | id=%s | method=%s | path=%s",
            request_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(request)

        except Exception:
            process_time = time.perf_counter() - start_time

            logger.exception(
                "Request failed | id=%s | method=%s | "
                "path=%s | duration=%.4fs",
                request_id,
                request.method,
                request.url.path,
                process_time,
            )

            raise

        process_time = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = (
            f"{process_time:.4f}"
        )

        logger.info(
            "Request completed | id=%s | method=%s | "
            "path=%s | status=%s | duration=%.4fs",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response


def register_logging_middleware(app: FastAPI) -> None:
    """
    Register request logging middleware.
    """

    app.add_middleware(LoggingMiddleware)


__all__ = [
    "LoggingMiddleware",
    "register_logging_middleware",
]