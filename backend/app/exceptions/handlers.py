"""
FlowerVision AI

Global Exception Handlers
"""

import traceback

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application-wide exception handlers.

    Args:
        app: FastAPI application instance.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """
        Handle FastAPI HTTP exceptions.
        """

        logger.warning(
            "HTTP %s | %s | %s",
            exc.status_code,
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                },
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        """
        Handle Pydantic validation errors.
        """

        logger.warning(
            "Validation Error | %s | %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": 422,
                    "message": "Validation failed.",
                    "details": exc.errors(),
                },
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected exceptions.
        """

        logger.exception(
            "Unhandled exception on %s %s",
            request.method,
            request.url.path,
        )

        response = {
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal Server Error",
            },
        }

        # Show traceback only in development
        if settings.DEBUG:
            response["error"]["traceback"] = traceback.format_exc()

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response,
        )
