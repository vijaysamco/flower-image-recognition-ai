"""
FlowerVision AI

Global Exception Handlers
"""

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register application-wide exception handlers.
    """

    # ---------------------------------------------------------
    # HTTP Exceptions
    # ---------------------------------------------------------

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """
        Handle HTTPException instances.
        """

        logger.warning(
            "HTTP error | %s %s | status=%s | detail=%s",
            request.method,
            request.url.path,
            exc.status_code,
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": str(exc.detail),
                },
            },
            headers=exc.headers,
        )

    # ---------------------------------------------------------
    # Request Validation Errors
    # ---------------------------------------------------------

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle FastAPI request validation errors.
        """

        logger.warning(
            "Request validation error | %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "Request validation failed.",
                    "details": _sanitize_errors(exc.errors()),
                },
            },
        )

    # ---------------------------------------------------------
    # Unexpected Exceptions
    # ---------------------------------------------------------

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected application errors.
        """

        logger.exception(
            "Unhandled exception | %s %s",
            request.method,
            request.url.path,
        )

        error: dict[str, Any] = {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error.",
        }

        # Never expose traceback information in production.
        if settings.DEBUG:
            error["details"] = str(exc)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": error,
            },
        )


def _sanitize_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Convert validation errors into JSON-safe objects.

    Pydantic validation errors can contain values that are not
    directly JSON serializable, so only expose the useful fields.
    """

    sanitized: list[dict[str, Any]] = []

    for error in errors:
        sanitized.append(
            {
                "type": error.get("type"),
                "location": [
                    str(item)
                    for item in error.get("loc", [])
                ],
                "message": error.get("msg"),
            }
        )

    return sanitized