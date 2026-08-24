"""
FlowerVision AI

FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


# ------------------------------------------------------------------
# Application Lifespan
# ------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    """

    logger.info(
        "Starting %s v%s",
        settings.APP_NAME,
        settings.APP_VERSION,
    )

    try:
        # Importing Predictor here ensures the trained model
        # is loaded during application startup.
        from app.services.predictor import Predictor

        Predictor()

        logger.info(
            "Application services initialized successfully."
        )

        yield

    except Exception:
        logger.exception(
            "Application startup failed."
        )
        raise

    finally:
        logger.info(
            "Shutting down %s.",
            settings.APP_NAME,
        )


# ------------------------------------------------------------------
# FastAPI Application
# ------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI-powered flower image recognition API "
        "using MobileNetV3-Small."
    ),
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# API Routes
# ------------------------------------------------------------------

app.include_router(
    router,
    prefix="/api/v1",
)


# ------------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------------

@app.get("/")
async def root() -> dict:
    """
    Return basic application information.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "documentation": "/docs",
        "health": "/api/v1/health",
    }