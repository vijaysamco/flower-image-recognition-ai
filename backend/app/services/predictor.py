"""
FlowerVision AI

AI Prediction Service
"""

from pathlib import Path

import torch
import torch.nn.functional as F
from fastapi import HTTPException, status
from torchvision import models

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class Predictor:
    """
    Handles flower classification model loading and inference.
    """

    FLOWER_CLASSES = [
        "daisy",
        "dandelion",
        "rose",
        "sunflower",
        "tulip",
    ]

    def __init__(self) -> None:
        """
        Initialize the predictor and load the model.
        """

        self.device = self._get_device()
        self.model = self._load_model()

        logger.info(
            "Predictor initialized | device=%s",
            self.device,
        )

    # ------------------------------------------------------------------
    # Device
    # ------------------------------------------------------------------

    @staticmethod
    def _get_device() -> torch.device:
        """
        Determine the PyTorch execution device.

        CPU is used automatically if CUDA is requested but
        unavailable.
        """

        requested_device = settings.DEVICE.lower()

        if requested_device == "cuda":

            if torch.cuda.is_available():
                logger.info("CUDA device available.")
                return torch.device("cuda")

            logger.warning(
                "CUDA requested but unavailable. "
                "Falling back to CPU."
            )

            return torch.device("cpu")

        return torch.device("cpu")

    # ------------------------------------------------------------------
    # Model Creation
    # ------------------------------------------------------------------

    def _create_model(self) -> torch.nn.Module:
        """
        Create the MobileNetV3-Small architecture.

        The architecture must match the architecture used when
        training the saved model.
        """

        model = models.mobilenet_v3_small(
            weights=None,
        )

        model.classifier[3] = torch.nn.Linear(
            in_features=model.classifier[3].in_features,
            out_features=len(self.FLOWER_CLASSES),
        )

        return model

    # ------------------------------------------------------------------
    # Model Loading
    # ------------------------------------------------------------------

    def _load_model(self) -> torch.nn.Module:
        """
        Load the trained flower classification model.

        Returns:
            Loaded PyTorch model.

        Raises:
            HTTPException:
                If the model file is missing or cannot be loaded.
        """

        model_path = Path(settings.MODEL_PATH)

        logger.info(
            "Loading model from: %s",
            model_path,
        )

        if not model_path.exists():
            logger.error(
                "Model file not found: %s",
                model_path,
            )

            raise RuntimeError(
                f"Model file not found: {model_path}"
            )

        try:
            model = self._create_model()

            checkpoint = torch.load(
                model_path,
                map_location=self.device,
                weights_only=True,
            )

            # ----------------------------------------------------------
            # Support either a raw state_dict or a checkpoint dict.
            # ----------------------------------------------------------

            if isinstance(checkpoint, dict):

                if "state_dict" in checkpoint:
                    state_dict = checkpoint["state_dict"]

                elif "model_state_dict" in checkpoint:
                    state_dict = checkpoint["model_state_dict"]

                else:
                    state_dict = checkpoint

            else:
                raise RuntimeError(
                    "Unsupported model checkpoint format."
                )

            # Handle checkpoints saved from DataParallel.
            state_dict = {
                key.removeprefix("module."): value
                for key, value in state_dict.items()
            }

            model.load_state_dict(state_dict)

            model.to(self.device)
            model.eval()

            logger.info(
                "Flower classification model loaded successfully."
            )

            return model

        except RuntimeError:
            logger.exception(
                "Unable to load model checkpoint: %s",
                model_path,
            )
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error while loading model: %s",
                model_path,
            )

            raise RuntimeError(
                "Unable to load the flower classification model."
            ) from exc

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    @torch.inference_mode()
    def predict(
        self,
        image_tensor: torch.Tensor,
    ) -> dict[str, str | float]:
        """
        Run flower classification inference.

        Args:
            image_tensor:
                Preprocessed tensor with shape
                [1, 3, IMAGE_SIZE, IMAGE_SIZE].

        Returns:
            Dictionary containing prediction and confidence.
        """

        if image_tensor.ndim != 4:
            raise ValueError(
                "Expected image tensor with 4 dimensions: "
                "[batch, channels, height, width]."
            )

        try:
            image_tensor = image_tensor.to(
                self.device,
                non_blocking=True,
            )

            outputs = self.model(image_tensor)

            probabilities = F.softmax(
                outputs,
                dim=1,
            )

            confidence, predicted_index = torch.max(
                probabilities,
                dim=1,
            )

            class_index = predicted_index.item()

            if not 0 <= class_index < len(
                self.FLOWER_CLASSES
            ):
                raise RuntimeError(
                    "Model returned an invalid class index."
                )

            prediction = self.FLOWER_CLASSES[
                class_index
            ]

            confidence_percentage = round(
                confidence.item() * 100,
                2,
            )

            logger.info(
                "Prediction completed | class=%s | confidence=%.2f%%",
                prediction,
                confidence_percentage,
            )

            return {
                "prediction": prediction,
                "confidence": confidence_percentage,
            }

        except Exception as exc:

            logger.exception(
                "Model inference failed."
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to perform image prediction.",
            ) from exc


__all__ = [
    "Predictor",
]