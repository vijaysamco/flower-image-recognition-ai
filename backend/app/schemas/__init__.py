"""
FlowerVision AI

Schemas Package

This package contains all Pydantic models used for
API request and response validation.
"""

from app.schemas.health import HealthResponse
from app.schemas.prediction import (
    FlowerClassesResponse,
    PredictionResponse,
)

__all__ = [
    "HealthResponse",
    "FlowerClassesResponse",
    "PredictionResponse",
]
