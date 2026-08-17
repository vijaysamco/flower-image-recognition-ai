"""
FlowerVision AI

Prediction API Schemas
"""

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """
    Response returned after flower image prediction.
    """

    filename: str = Field(
        ...,
        description="Name of the uploaded image.",
    )

    prediction: str = Field(
        ...,
        description="Predicted flower species.",
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Prediction confidence percentage.",
    )

    message: str = Field(
        default="Prediction completed successfully.",
        description="Human-readable prediction message.",
    )


class FlowerClassesResponse(BaseModel):
    """
    Response containing supported flower classes.
    """

    count: int = Field(
        ...,
        ge=0,
        description="Number of supported flower classes.",
    )

    classes: list[str] = Field(
        ...,
        description="Supported flower species.",
    )


__all__ = [
    "PredictionResponse",
    "FlowerClassesResponse",
]