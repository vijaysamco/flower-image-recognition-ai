"""
FlowerVision AI

Health Check API Schemas
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Response returned by the health check endpoint.
    """

    status: str = Field(
        ...,
        description="Current application health status.",
    )

    application: str = Field(
        ...,
        description="Application name.",
    )

    version: str = Field(
        ...,
        description="Application version.",
    )


__all__ = [
    "HealthResponse",
]