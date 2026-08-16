"""
FlowerVision AI

Prediction Service
"""

from pathlib import Path

import torch
import torch.nn.functional as F
from torchvision import models

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class Predictor:
    """
    Handles AI model loading and inference.
    """

    FLOWER_CLASSES = [
        "daisy",
        "dandelion",
        "rose",
        "sunflower",
        "tulip",
    ]

    def __init__(self) -> None:
        self.device = torch.device(settings.DEVICE)
        self.model = self._load_model()

    def _load_model(self) -> torch.nn.Module:
        """
        Load the trained model.

        Returns:
            Loaded PyTorch model.
        """

        logger.info("Loading AI model...")

        model = models.mobilenet_v3_small(weights=None)

        model.classifier[3] = torch.nn.Linear(
            in_features=model.classifier[3].in_features,
            out_features=len(self.FLOWER_CLASSES),
        )

        model_path = Path(settings.MODEL_PATH)

        if model_path.exists():
            state_dict = torch.load(
                model_path,
                map_location=self.device,
            )

            model.load_state_dict(state_dict)

            logger.info("Model loaded successfully.")

        else:
            logger.warning(
                "Model file not found: %s",
                model_path,
            )
            logger.warning(
                "Using randomly initialized model."
            )

        model.to(self.device)
        model.eval()

        return model

    @torch.no_grad()
    def predict(
        self,
        image_tensor: torch.Tensor,
    ) -> dict:
        """
        Predict flower species.

        Args:
            image_tensor:
                Preprocessed image tensor.

        Returns:
            Prediction result.
        """

        image_tensor = image_tensor.to(self.device)

        outputs = self.model(image_tensor)

        probabilities = F.softmax(
            outputs,
            dim=1,
        )

        confidence, predicted = torch.max(
            probabilities,
            dim=1,
        )

        predicted_class = self.FLOWER_CLASSES[
            predicted.item()
        ]

        return {
            "prediction": predicted_class,
            "confidence": round(
                confidence.item() * 100,
                2,
            ),
        }
