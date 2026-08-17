"""
FlowerVision AI

Application Configuration
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    APP_NAME: str = Field(
        default="FlowerVision AI",
        description="Application name.",
    )

    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version.",
    )

    API_PREFIX: str = Field(
        default="/api/v1",
        description="API prefix.",
    )

    DEBUG: bool = Field(
        default=True,
        description="Enable debug mode.",
    )

    # ------------------------------------------------------------------
    # AI Model
    # ------------------------------------------------------------------

    DEVICE: str = Field(
        default="cpu",
        description="PyTorch device.",
    )

    MODEL_PATH: Path = Field(
        default=BASE_DIR / "models" / "flower_classifier.pth",
        description="Path to the trained model.",
    )

    IMAGE_SIZE: int = Field(
        default=224,
        description="Input image size.",
    )

    # ------------------------------------------------------------------
    # Upload Configuration
    # ------------------------------------------------------------------

    MAX_UPLOAD_SIZE: int = Field(
        default=5 * 1024 * 1024,
        description="Maximum upload size in bytes.",
    )

    ALLOWED_IMAGE_TYPES: list[str] = Field(
        default=[
            "image/jpeg",
            "image/png",
            "image/webp",
        ],
        description="Allowed image MIME types.",
    )

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    ALLOWED_ORIGINS: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
        ],
        description="Allowed CORS origins.",
    )


settings = Settings()