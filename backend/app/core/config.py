"""
FlowerVision AI

Application Configuration
"""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------

    APP_NAME: str = "FlowerVision AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # ---------------------------------------------------------
    # Server
    # ---------------------------------------------------------

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    API_PREFIX: str = "/api/v1"

    # ---------------------------------------------------------
    # Frontend
    # ---------------------------------------------------------

    FRONTEND_URL: str = "http://localhost:5173"

    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:5173"]
    )

    # ---------------------------------------------------------
    # AI Model
    # ---------------------------------------------------------

    MODEL_NAME: str = "MobileNetV3"

    MODEL_PATH: str = "models/mobilenet_v3_flowers.pth"

    DEVICE: str = "cpu"

    IMAGE_SIZE: int = 224

    # ---------------------------------------------------------
    # Upload Settings
    # ---------------------------------------------------------

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024

    ALLOWED_IMAGE_TYPES: List[str] = Field(
        default=[
            "image/jpeg",
            "image/png",
            "image/webp",
        ]
    )

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------

    DATABASE_URL: str = "sqlite:///./flowervision.db"

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    LOG_LEVEL: str = "INFO"

    # ---------------------------------------------------------
    # Security
    # ---------------------------------------------------------

    SECRET_KEY: str = "change-this-secret-key"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ---------------------------------------------------------
    # Pydantic Settings Configuration
    # ---------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
