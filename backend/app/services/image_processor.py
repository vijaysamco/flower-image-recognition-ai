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
    Validates and preprocesses images for model inference.
    """

    def __init__(self) -> None:
        """
        Initialize the image transformation pipeline.
        """

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

    async def process(
        self,
        file: UploadFile,
    ) -> torch.Tensor:
        """
        Read and preprocess an uploaded image.

        Args:
            file: Uploaded image file.

        Returns:
            Tensor with shape [1, 3, IMAGE_SIZE, IMAGE_SIZE].

        Raises:
            HTTPException: If the image cannot be decoded.
        """

        try:
            image_bytes = await file.read()

            if not image_bytes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uploaded image is empty.",
                )

            image = Image.open(
                BytesIO(image_bytes)
            )

            # Force image decoding while the file is available.
            image.verify()

            # Re-open after verify() because PIL invalidates
            # the image object after verification.
            image = Image.open(
                BytesIO(image_bytes)
            ).convert("RGB")

        except UnidentifiedImageError as exc:
            logger.warning(
                "Unable to decode uploaded image: %s",
                file.filename,
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted image file.",
            ) from exc

        except HTTPException:
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error while processing image: %s",
                file.filename,
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to process the uploaded image.",
            ) from exc

        try:
            tensor = self.transform(image)

            # Add batch dimension:
            # [3, H, W] -> [1, 3, H, W]
            tensor = tensor.unsqueeze(0)

        except Exception as exc:
            logger.exception(
                "Image transformation failed: %s",
                file.filename,
            )

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to transform the image for prediction.",
            ) from exc

        logger.info(
            "Image processed successfully | file=%s | shape=%s",
            file.filename,
            tuple(tensor.shape),
        )

        return tensor


__all__ = [
    "ImageProcessor",
]