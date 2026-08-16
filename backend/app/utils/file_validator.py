"""
FlowerVision AI

File Validation Utilities
"""

from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class FileValidator:
    """
    Utility class for validating uploaded image files.
    """

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    @staticmethod
    async def validate(file: UploadFile) -> None:
        """
        Validate an uploaded image.

        Args:
            file: Uploaded file.

        Raises:
            HTTPException:
                If validation fails.
        """

        # --------------------------------------------
        # Validate filename
        # --------------------------------------------

        if not file.filename:
            logger.warning("Uploaded file has no filename.")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required.",
            )

        # --------------------------------------------
        # Validate extension
        # --------------------------------------------

        extension = Path(file.filename).suffix.lower()

        if extension not in FileValidator.ALLOWED_EXTENSIONS:
            logger.warning(
                "Unsupported file extension: %s",
                extension,
            )

            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=(
                    "Unsupported file extension. "
                    "Allowed: jpg, jpeg, png, webp."
                ),
            )

        # --------------------------------------------
        # Validate MIME type
        # --------------------------------------------

        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            logger.warning(
                "Unsupported MIME type: %s",
                file.content_type,
            )

            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported image format.",
            )

        # --------------------------------------------
        # Validate file size
        # --------------------------------------------

        contents = await file.read()

        file_size = len(contents)

        await file.seek(0)

        if file_size > settings.MAX_UPLOAD_SIZE:
            logger.warning(
                "File too large: %d bytes",
                file_size,
            )

            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    f"Maximum upload size is "
                    f"{settings.MAX_UPLOAD_SIZE // (1024 * 1024)} MB."
                ),
            )

        logger.info(
            "File validation successful: %s",
            file.filename,
        )
