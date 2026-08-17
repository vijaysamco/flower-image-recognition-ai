"""
FlowerVision AI

API Routes
"""

from fastapi import APIRouter, File, Request, UploadFile

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.health import HealthResponse
from app.schemas.prediction import (
    FlowerClassesResponse,
    PredictionResponse,
)
from app.services.predictor import Predictor
from app.utils.file_validator import FileValidator

logger = get_logger(__name__)

router = APIRouter(
    tags=["FlowerVision AI"],
)

# Single source of truth for the currently supported classes.
FLOWER_CLASSES = Predictor.FLOWER_CLASSES


# ------------------------------------------------------------------
# Health Check
# ------------------------------------------------------------------

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check() -> HealthResponse:
    """
    Check whether the API is running.
    """

    return HealthResponse(
        status="healthy",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


# ------------------------------------------------------------------
# Supported Flowers
# ------------------------------------------------------------------

@router.get(
    "/flowers",
    response_model=FlowerClassesResponse,
    summary="Get Supported Flower Classes",
)
async def get_supported_flowers() -> FlowerClassesResponse:
    """
    Return all flower classes supported by the model.
    """

    return FlowerClassesResponse(
        count=len(FLOWER_CLASSES),
        classes=FLOWER_CLASSES,
    )


# ------------------------------------------------------------------
# Prediction
# ------------------------------------------------------------------

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Flower Species",
)
async def predict_flower(
    request: Request,
    file: UploadFile = File(...),
) -> PredictionResponse:
    """
    Predict the flower species from an uploaded image.
    """

    logger.info(
        "Prediction request received | file=%s",
        file.filename,
    )

    # --------------------------------------------------------------
    # 1. Validate uploaded file
    # --------------------------------------------------------------

    await FileValidator.validate(file)

    # --------------------------------------------------------------
    # 2. Get application services
    # --------------------------------------------------------------

    image_processor = request.app.state.image_processor
    predictor = request.app.state.predictor

    # --------------------------------------------------------------
    # 3. Preprocess image
    # --------------------------------------------------------------

    image_tensor = await image_processor.process(file)

    # --------------------------------------------------------------
    # 4. Run AI inference
    # --------------------------------------------------------------

    result = predictor.predict(image_tensor)

    logger.info(
        "Prediction successful | file=%s | prediction=%s | "
        "confidence=%.2f%%",
        file.filename,
        result["prediction"],
        result["confidence"],
    )

    # --------------------------------------------------------------
    # 5. Return API response
    # --------------------------------------------------------------

    return PredictionResponse(
        filename=file.filename or "unknown",
        prediction=result["prediction"],
        confidence=result["confidence"],
        message="Prediction completed successfully.",
    )


__all__ = [
    "router",
]