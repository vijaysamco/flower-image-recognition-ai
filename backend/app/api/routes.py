"""
FlowerVision AI

API Routes
"""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.core.logger import get_logger

from app.schemas import (
    FlowerClassesResponse,
    HealthResponse,
    PredictionResponse,
)
router = APIRouter(tags=["FlowerVision AI"])

logger = get_logger(__name__)

# ---------------------------------------------------------
# Supported Flower Classes
# ---------------------------------------------------------

FLOWER_CLASSES = [
    "daisy",
    "dandelion",
    "rose",
    "sunflower",
    "tulip",
]


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@router.get(
    "/health",
    summary="Health Check",
    response_description="Application health status",
    response_model=HealthResponse,
)
async def health_check():
    """
    Returns the application health status.
    """

    logger.info("Health check requested.")

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# ---------------------------------------------------------
# Supported Flower Species
# ---------------------------------------------------------

@router.get(
    "/flowers",
    summary="Supported Flower Species",
    response_model=FlowerClassesResponse,
)
async def get_supported_flowers():
    """
    Returns the list of supported flower species.
    """

    logger.info("Supported flower list requested.")

    return {
        "count": len(FLOWER_CLASSES),
        "classes": FLOWER_CLASSES,
    }


# ---------------------------------------------------------
# Flower Prediction
# ---------------------------------------------------------

@router.post(
    "/predict",
    summary="Predict Flower Species",
    response_model=PredictionResponse,
)
async def predict_flower(
    file: UploadFile = File(...),
):
    """
    Accepts a flower image and returns
    a prediction.

    NOTE:
    Actual AI inference will be implemented
    in the service layer.
    """

    logger.info("Prediction request received.")

    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        logger.warning(
            "Unsupported file type: %s",
            file.content_type,
        )

        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported image format.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    # -----------------------------------------------------
    # Placeholder Response
    # Replace with actual AI inference later.
    # -----------------------------------------------------

    prediction = "sunflower"
    confidence = 98.73

    logger.info(
        "Prediction completed successfully for %s",
        file.filename,
    )

    return {
        "filename": file.filename,
        "prediction": prediction,
        "confidence": confidence,
        "message": (
            "Placeholder prediction. "
            "AI inference will be connected "
            "in the next phase."
        ),
    }
