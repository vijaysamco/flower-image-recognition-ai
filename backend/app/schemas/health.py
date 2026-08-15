"""
FlowerVision AI

Health Response Schema
"""

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """
    Response model for the health check endpoint.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "application": "FlowerVision AI",
                "version": "1.0.0",
            }
        }
    )

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
        description="Current application version.",
    )
