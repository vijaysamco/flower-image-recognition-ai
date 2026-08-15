"""
FlowerVision AI

Main FastAPI Application

Author: VIJAY
License: MIT
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info("Starting FlowerVision AI API...")

    # TODO:
    # Load AI model
    # Initialize database
    # Create upload directories

    yield

    logger.info("Shutting down FlowerVision AI API...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Flower Image Recognition API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
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
        "docs": "/docs",
    }


# ------------------------------------------------------------------
# Health Check
# ------------------------------------------------------------------


@app.get("/health", tags=["General"])
async def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
