"""
FlowerVision AI

Image Processing Service
"""

from io import BytesIO

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

from app.core.logger import get_logger

logger = get_logger(__name__)


# ------------------------------------------------------------------
# Image Configuration
# ------------------------------------------------------------------

IMAGE_SIZE = 224

IMAGE_MEAN = [
    0.485,
    0.456,
    0.406,
]

IMAGE_STD = [
    0.229,
    0.224,
    0.225,
]


# ------------------------------------------------------------------
# Image Transform
# ------------------------------------------------------------------

IMAGE_TRANSFORM = transforms.Compose(
    [
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE)
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=IMAGE_MEAN,
            std=IMAGE_STD,
        ),
    ]
)


# ------------------------------------------------------------------
# Image Processor
# ------------------------------------------------------------------

class ImageProcessor:
    """
    Handles image validation, decoding, preprocessing,
    and conversion to a PyTorch tensor.
    """

    @staticmethod
    def validate_image(
        image_bytes: bytes,
    ) -> None:
        """
        Verify that the uploaded bytes represent a
        valid image.

        Args:
            image_bytes:
                Raw image bytes.

        Raises:
            ValueError:
                If the image cannot be decoded.
        """

        if not image_bytes:
            raise ValueError(
                "Image file is empty."
            )

        try:
            with Image.open(
                BytesIO(image_bytes)
            ) as image:

                image.verify()

        except (
            UnidentifiedImageError,
            OSError,
        ) as exc:

            logger.warning(
                "Invalid image received."
            )

            raise ValueError(
                "The uploaded file is not a valid image."
            ) from exc

    @staticmethod
    def process_image(
        image_bytes: bytes,
    ) -> torch.Tensor:
        """
        Convert raw image bytes into a model-ready
        PyTorch tensor.

        Processing pipeline:

            Raw bytes
                ↓
            PIL Image
                ↓
            RGB
                ↓
            Resize 224x224
                ↓
            Tensor
                ↓
            ImageNet normalization
                ↓
            Batch dimension
        """

        ImageProcessor.validate_image(
            image_bytes
        )

        try:
            with Image.open(
                BytesIO(image_bytes)
            ) as image:

                image = image.convert("RGB")

                tensor = IMAGE_TRANSFORM(
                    image
                )

        except (
            UnidentifiedImageError,
            OSError,
        ) as exc:

            logger.exception(
                "Failed to process uploaded image."
            )

            raise ValueError(
                "Unable to process the uploaded image."
            ) from exc

        # Add batch dimension:
        #
        # [3, 224, 224]
        #
        # becomes:
        #
        # [1, 3, 224, 224]

        tensor = tensor.unsqueeze(0)

        logger.debug(
            "Image processed successfully | "
            "shape=%s",
            tuple(tensor.shape),
        )

        return tensor


__all__ = [
    "ImageProcessor",
]