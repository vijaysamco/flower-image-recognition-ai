"""
FlowerVision AI

Image Processing Service
"""

from io import BytesIO

import torch
from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class ImageProcessor:
    """
    Handles image preprocessing before AI inference.
    """

    def __init__(self) -> None:
        self.transform = transforms.Compose(
            [
                transforms.Resize(
                    (
                        settings.IMAGE_SIZE,
                        settings.IMAGE_SIZE,
                    )
                ),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

    async def process(self, file: UploadFile) -> torch.Tensor:
        """
        Validate and preprocess an uploaded image.

        Args:
            file:
                Uploaded image.

        Returns:
            Preprocessed image tensor.

        Raises:
            HTTPException
                If the uploaded image is invalid.
        """

        try:
            image_bytes = await file.read()

            image = Image.open(
                BytesIO(image_bytes)
            ).convert("RGB")

        except UnidentifiedImageError:

            logger.error(
                "Invalid image uploaded."
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file.",
            )

        except Exception as exc:

            logger.exception(exc)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to process image.",
            )

        tensor = self.transform(image)

        tensor = tensor.unsqueeze(0)

        logger.info(
            "Image processed successfully."
        )

        return tensor
