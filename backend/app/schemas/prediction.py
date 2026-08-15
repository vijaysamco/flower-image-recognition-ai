"""
FlowerVision AI

Prediction Schemas
"""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class PredictionResponse(BaseModel):
    """
    Response model for a flower prediction.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "sunflower.jpg",
                "prediction": "sunflower",
                "confidence": 98.73,
                "message": "Prediction completed successfully.",
            }
        }
    )

    filename: str = Field(
        ...,
        description="Uploaded image filename.",
    )

    prediction: str = Field(
        ...,
        description="Predicted flower species.",
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=100,
        description="Prediction confidence percentage.",
    )

    message: str = Field(
        ...,
        description="Prediction status message.",
    )


class FlowerClassesResponse(BaseModel):
    """
    Response model for supported flower classes.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 5,
                "classes": [
                    "daisy",
                    "dandelion",
                    "rose",
                    "sunflower",
                    "tulip",
                ],
            }
        }
    )

    count: int = Field(
        ...,
        description="Number of supported flower classes.",
    )

    classes: List[str] = Field(
        ...,
        description="Supported flower species.",
    )
