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
from app.core.telemetry import TRACE_ID_CONTEXT, get_telemetry_store

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
        trace_id = (
            request.headers.get("X-Trace-ID")
            or request.headers.get("x-trace-id")
            or request_id
        )
        start_time = time.perf_counter()
        telemetry = get_telemetry_store()
        token = TRACE_ID_CONTEXT.set(trace_id)

        request.state.request_id = request_id
        request.state.trace_id = trace_id

        telemetry.record_metric(
            "http_requests_total",
            1,
            tags={
                "method": request.method,
                "path": request.url.path,
            },
            trace_id=trace_id,
        )

        logger.info(
            "Request started | trace_id=%s | id=%s | method=%s | path=%s",
            trace_id,
            request_id,
            request.method,
            request.url.path,
        )

        try:
            try:
                response = await call_next(request)

            except Exception:
                process_time = time.perf_counter() - start_time

                telemetry.record_metric(
                    "http_request_errors_total",
                    1,
                    tags={
                        "method": request.method,
                        "path": request.url.path,
                    },
                    trace_id=trace_id,
                )

                telemetry.record_trace(
                    trace_id=trace_id,
                    route=request.url.path,
                    method=request.method,
                    status_code=500,
                    duration_ms=process_time * 1000,
                    journey="http_request",
                    metadata={
                        "request_id": request_id,
                        "error": "uncaught_exception",
                    },
                )

                telemetry.record_log(
                    "ERROR",
                    "Request failed",
                    event="http_request",
                    trace_id=trace_id,
                    request_id=request_id,
                    method=request.method,
                    path=request.url.path,
                    duration_ms=round(process_time * 1000, 3),
                )

                logger.exception(
                    "Request failed | trace_id=%s | id=%s | method=%s | "
                    "path=%s | duration=%.4fs",
                    trace_id,
                    request_id,
                    request.method,
                    request.url.path,
                    process_time,
                )

                raise

            process_time = time.perf_counter() - start_time
            telemetry.record_metric(
                "http_request_duration_ms",
                process_time * 1000,
                tags={
                    "method": request.method,
                    "path": request.url.path,
                    "status": str(response.status_code),
                },
                trace_id=trace_id,
            )

            telemetry.record_trace(
                trace_id=trace_id,
                route=request.url.path,
                method=request.method,
                status_code=response.status_code,
                duration_ms=process_time * 1000,
                journey="http_request",
                metadata={
                    "request_id": request_id,
                    "status_code": response.status_code,
                },
            )

            telemetry.record_log(
                "INFO",
                "Request completed",
                event="http_request",
                trace_id=trace_id,
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(process_time * 1000, 3),
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Trace-ID"] = trace_id
            response.headers["X-Process-Time"] = (
                f"{process_time:.4f}"
            )

            logger.info(
                "Request completed | trace_id=%s | id=%s | method=%s | "
                "path=%s | status=%s | duration=%.4fs",
                trace_id,
                request_id,
                request.method,
                request.url.path,
                response.status_code,
                process_time,
            )

            return response

        finally:
            TRACE_ID_CONTEXT.reset(token)


def register_logging_middleware(app: FastAPI) -> None:
    """
    Register request logging middleware.
    """

    app.add_middleware(LoggingMiddleware)


__all__ = [
    "LoggingMiddleware",
    "register_logging_middleware",
]