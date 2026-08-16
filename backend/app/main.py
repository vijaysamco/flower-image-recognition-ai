"""
FlowerVision AI

Main FastAPI Application

Author: Vijay
License: MIT
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logger import get_logger
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info("========================================")
    logger.info("Starting FlowerVision AI API...")
    logger.info("========================================")

    # Initialize shared services
    app.state.image_processor = ImageProcessor()
    app.state.predictor = Predictor()

    logger.info("Application initialized successfully.")

    yield

    logger.info("========================================")
    logger.info("Shutting down FlowerVision AI API...")
    logger.info("========================================")


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
# CORS
# ------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/", tags=["General"])
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
