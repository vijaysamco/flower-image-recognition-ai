"""
FlowerVision AI

API Routes
"""

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.health import HealthResponse
from app.schemas.prediction import PredictionResponse
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor
from app.utils.file_validator import FileValidator


logger = get_logger(__name__)

router = APIRouter()


# ------------------------------------------------------------------
# Services
# ------------------------------------------------------------------

image_processor = ImageProcessor()
predictor = Predictor()


# ------------------------------------------------------------------
# Root
# ------------------------------------------------------------------

@router.get("/")
async def root() -> dict:
    """
    API root endpoint.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "documentation": "/docs",
        "health": "/api/v1/health",
    }


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------

@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    """
    Return API health status.
    """

    return HealthResponse(
        status="healthy",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


# ------------------------------------------------------------------
# Flowers
# ------------------------------------------------------------------

@router.get(
    "/flowers",
)
async def flowers() -> dict:
    """
    Return supported flower classes.
    """

    classes = predictor.FLOWER_CLASSES

    return {
        "count": len(classes),
        "classes": classes,
    }


# ------------------------------------------------------------------
# Prediction
# ------------------------------------------------------------------

@router.post(
    "/predict",
    response_model=PredictionResponse,
)
async def predict(
    file: UploadFile = File(...),
) -> PredictionResponse:
    """
    Predict the flower class from an uploaded image.
    """

    logger.info(
        "Prediction request received | filename=%s | content_type=%s",
        file.filename,
        file.content_type,
    )

    # --------------------------------------------------------------
    # Validate uploaded file
    # --------------------------------------------------------------

    await FileValidator.validate(
        file
    )

    # --------------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:
        logger.warning(
            "Empty image file received | filename=%s",
            file.filename,
        )

        raise HTTPException(
            status_code=400,
            detail="Uploaded image file is empty.",
        )

    # --------------------------------------------------------------
    # Process image
    # --------------------------------------------------------------

    try:
        image_tensor = image_processor.process(
            image_bytes
        )

    except ValueError as exc:

        logger.warning(
            "Invalid image uploaded | filename=%s | error=%s",
            file.filename,
            str(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # --------------------------------------------------------------
    # Run prediction
    # --------------------------------------------------------------

    result = predictor.predict(
        image_tensor
    )

    logger.info(
        "Prediction completed | filename=%s | prediction=%s | confidence=%s",
        file.filename,
        result["prediction"],
        result["confidence"],
    )

    # --------------------------------------------------------------
    # Return response
    # --------------------------------------------------------------

    return PredictionResponse(
        success=True,
        filename=file.filename or "unknown",
        prediction=result["prediction"],
        confidence=result["confidence"],
    )