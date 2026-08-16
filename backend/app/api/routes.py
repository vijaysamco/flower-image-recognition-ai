"""
FlowerVision AI

API Routes
"""

from fastapi import APIRouter, File, UploadFile

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas import (
    FlowerClassesResponse,
    HealthResponse,
    PredictionResponse,
)
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor

router = APIRouter(tags=["FlowerVision AI"])

logger = get_logger(__name__)

# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

image_processor = ImageProcessor()
predictor = Predictor()

FLOWER_CLASSES = Predictor.FLOWER_CLASSES

# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check() -> HealthResponse:
    """
    Check API health.
    """

    logger.info("Health check requested.")

    return HealthResponse(
        status="healthy",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


# ---------------------------------------------------------
# Supported Flower Classes
# ---------------------------------------------------------


@router.get(
    "/flowers",
    response_model=FlowerClassesResponse,
    summary="Supported Flower Species",
)
async def get_supported_flowers() -> FlowerClassesResponse:
    """
    Return supported flower classes.
    """

    logger.info("Flower classes requested.")

    return FlowerClassesResponse(
        count=len(FLOWER_CLASSES),
        classes=FLOWER_CLASSES,
    )


# ---------------------------------------------------------
# Prediction Endpoint
# ---------------------------------------------------------


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Flower Species",
)
async def predict_flower(
    file: UploadFile = File(...),
) -> PredictionResponse:
    """
    Predict flower species from an uploaded image.
    """

    logger.info(
        "Prediction request received: %s",
        file.filename,
    )

    image_tensor = await image_processor.process(file)

    result = predictor.predict(image_tensor)

    logger.info(
        "Prediction completed: %s (%.2f%%)",
        result["prediction"],
        result["confidence"],
    )

    return PredictionResponse(
        filename=file.filename,
        prediction=result["prediction"],
        confidence=result["confidence"],
        message="Prediction completed successfully.",
    )
