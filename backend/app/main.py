"""
FlowerVision AI

Main FastAPI Application

Author: VIJAY
License: MIT
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings
from app.core.logger import get_logger
from app.exceptions import register_exception_handlers
from app.middleware import register_logging_middleware
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    """

    logger.info("=" * 60)
    logger.info("Starting %s...", settings.APP_NAME)
    logger.info("=" * 60)

    try:
        # ---------------------------------------------------------
        # Initialize shared services
        # ---------------------------------------------------------

        app.state.image_processor = ImageProcessor()
        app.state.predictor = Predictor()

        logger.info("Application services initialized successfully.")

        yield

    finally:
        logger.info("=" * 60)
        logger.info("Shutting down %s...", settings.APP_NAME)
        logger.info("=" * 60)


# ------------------------------------------------------------------
# FastAPI Application
# ------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Flower Image Recognition API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------

register_logging_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Exception Handlers
# ------------------------------------------------------------------

register_exception_handlers(app)

# ------------------------------------------------------------------
# API Routes
# ------------------------------------------------------------------

app.include_router(
    router,
    prefix=settings.API_PREFIX,
)

# ------------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------------


@app.get(
    "/",
    tags=["General"],
    summary="Application Information",
)
async def root():
    """
    Root endpoint.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "documentation": "/docs",
        "openapi": "/openapi.json",
    }
