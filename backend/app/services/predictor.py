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
        Initialize the predictor.

        The application can start without a trained model during
        development. Prediction requests will remain unavailable
        until the trained model is provided.
        """

        self.device = self._get_device()
        self.model: torch.nn.Module | None = None
        self.model_loaded = False

        model_path = Path(settings.MODEL_PATH)

        if model_path.exists():
            self.model = self._load_model()
            self.model_loaded = True

            logger.info(
                "Predictor initialized successfully | device=%s",
                self.device,
            )
        else:
            logger.warning(
                "Model file not found: %s",
                model_path,
            )

            logger.warning(
                "Application will start in development mode. "
                "Prediction endpoint will be unavailable until "
                "a trained model is provided."
            )

    # ------------------------------------------------------------------
    # Device
    # ------------------------------------------------------------------

    @staticmethod
    def _get_device() -> torch.device:
        """
        Determine the PyTorch execution device.
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

    # ------------------------------------------------------------------
    # Model Architecture
    # ------------------------------------------------------------------

    def _create_model(self) -> torch.nn.Module:
        """
        Create the MobileNetV3-Small architecture.

        This architecture must match the architecture used
        during model training.
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
        Load the trained model checkpoint.
        """

        model_path = Path(settings.MODEL_PATH)

        logger.info(
            "Loading flower classification model from: %s",
            model_path,
        )

        try:
            model = self._create_model()

            checkpoint = torch.load(
                model_path,
                map_location=self.device,
                weights_only=True,
            )

            # ----------------------------------------------------------
            # Extract state dictionary
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

            # ----------------------------------------------------------
            # Handle DataParallel checkpoints
            # ----------------------------------------------------------

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

        except Exception as exc:
            logger.exception(
                "Failed to load flower classification model."
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
                Preprocessed image tensor.

        Returns:
            Prediction and confidence.

        Raises:
            HTTPException:
                If the trained model is unavailable.
        """

        # --------------------------------------------------------------
        # Model availability check
        # --------------------------------------------------------------

        if not self.model_loaded or self.model is None:
            logger.warning(
                "Prediction requested but trained model is unavailable."
            )

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "Flower recognition model is not available. "
                    "Please provide the trained model."
                ),
            )

        # --------------------------------------------------------------
        # Validate tensor
        # --------------------------------------------------------------

        if image_tensor.ndim != 4:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "Invalid image tensor format."
                ),
            )

        # --------------------------------------------------------------
        # Inference
        # --------------------------------------------------------------

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
                "Prediction completed | "
                "class=%s | confidence=%.2f%%",
                prediction,
                confidence_percentage,
            )

            return {
                "prediction": prediction,
                "confidence": confidence_percentage,
            }

        except HTTPException:
            raise

        except Exception as exc:
            logger.exception(
                "Model inference failed."
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to perform image prediction.",
            ) from exc

    # ------------------------------------------------------------------
    # Model Status
    # ------------------------------------------------------------------

    def is_ready(self) -> bool:
        """
        Return whether the trained model is available.
        """

        return self.model_loaded


__all__ = [
    "Predictor",
]