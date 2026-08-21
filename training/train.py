"""
FlowerVision AI

Phase 3 - Lightweight Transfer Learning

Model:
    MobileNetV3-Small

Classes:
    daisy
    dandelion
    rose
    sunflower
    tulip

Designed for CPU/laptop development.
"""

from pathlib import Path
import json
import random

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "training" / "dataset"

MODEL_DIR = PROJECT_ROOT / "backend" / "models"

MODEL_PATH = MODEL_DIR / "flower_classifier.pth"

CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

IMAGE_SIZE = 224

BATCH_SIZE = 16

EPOCHS = 5

LEARNING_RATE = 0.001

VALIDATION_SPLIT = 0.20

RANDOM_SEED = 42

NUM_WORKERS = 0

DEVICE = torch.device("cpu")


# ------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------

DATASET_CLASSES = [
    "daisy",
    "dandelion",
    "roses",
    "sunflowers",
    "tulips",
]

MODEL_CLASSES = [
    "daisy",
    "dandelion",
    "rose",
    "sunflower",
    "tulip",
]


# ------------------------------------------------------------------
# Reproducibility
# ------------------------------------------------------------------

random.seed(RANDOM_SEED)

torch.manual_seed(RANDOM_SEED)


# ------------------------------------------------------------------
# Dataset validation
# ------------------------------------------------------------------

def validate_dataset() -> None:
    """
    Verify that the expected dataset exists.
    """

    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset directory not found: {DATASET_DIR}"
        )

    for class_name in DATASET_CLASSES:

        class_dir = DATASET_DIR / class_name

        if not class_dir.exists():
            raise FileNotFoundError(
                f"Missing class directory: {class_dir}"
            )


# ------------------------------------------------------------------
# Image transforms
# ------------------------------------------------------------------

train_transform = transforms.Compose(
    [
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE)
        ),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.2,
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


validation_transform = transforms.Compose(
    [
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE)
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


# ------------------------------------------------------------------
# Dataset
# ------------------------------------------------------------------

def create_datasets():
    """
    Create training and validation datasets.
    """

    full_dataset = datasets.ImageFolder(
        DATASET_DIR,
        transform=train_transform,
    )

    total_size = len(full_dataset)

    validation_size = int(
        total_size * VALIDATION_SPLIT
    )

    training_size = (
        total_size - validation_size
    )

    generator = torch.Generator().manual_seed(
        RANDOM_SEED
    )

    train_dataset, validation_dataset = (
        torch.utils.data.random_split(
            full_dataset,
            [
                training_size,
                validation_size,
            ],
            generator=generator,
        )
    )

    # ImageFolder uses one shared dataset object.
    # Create a separate validation dataset to ensure
    # validation images do not receive augmentation.

    validation_base = datasets.ImageFolder(
        DATASET_DIR,
        transform=validation_transform,
    )

    validation_dataset = torch.utils.data.Subset(
        validation_base,
        validation_dataset.indices,
    )

    return (
        train_dataset,
        validation_dataset,
    )


# ------------------------------------------------------------------
# Model
# ------------------------------------------------------------------

def create_model() -> nn.Module:
    """
    Create MobileNetV3-Small using ImageNet-pretrained weights.
    """

    print(
        "Loading ImageNet-pretrained MobileNetV3-Small..."
    )

    weights = (
        models.MobileNet_V3_Small_Weights.DEFAULT
    )

    model = models.mobilenet_v3_small(
        weights=weights,
    )

    # Freeze feature extractor.
    for parameter in model.features.parameters():
        parameter.requires_grad = False

    # Replace final classifier.
    model.classifier[3] = nn.Linear(
        model.classifier[3].in_features,
        len(MODEL_CLASSES),
    )

    return model


# ------------------------------------------------------------------
# Training
# ------------------------------------------------------------------

def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
) -> tuple[float, float]:

    model.train()

    total_loss = 0.0

    correct = 0

    total = 0

    for images, labels in dataloader:

        images = images.to(DEVICE)

        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels,
        )

        loss.backward()

        optimizer.step()

        total_loss += (
            loss.item()
            * images.size(0)
        )

        predictions = outputs.argmax(
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    return (
        total_loss / total,
        correct / total,
    )


# ------------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------------

def evaluate(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
) -> tuple[float, float]:

    model.eval()

    total_loss = 0.0

    correct = 0

    total = 0

    with torch.no_grad():

        for images, labels in dataloader:

            images = images.to(DEVICE)

            labels = labels.to(DEVICE)

            outputs = model(images)

            loss = criterion(
                outputs,
                labels,
            )

            total_loss += (
                loss.item()
                * images.size(0)
            )

            predictions = outputs.argmax(
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    return (
        total_loss / total,
        correct / total,
    )


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> None:

    print()
    print("FlowerVision AI")
    print("Phase 3 - Transfer Learning")
    print("=" * 55)

    print(
        f"Training device: {DEVICE}"
    )

    print(
        f"Dataset: {DATASET_DIR}"
    )

    print(
        f"Model output: {MODEL_PATH}"
    )

    print()

    validate_dataset()

    # --------------------------------------------------------------
    # Dataset
    # --------------------------------------------------------------

    train_dataset, validation_dataset = (
        create_datasets()
    )

    print(
        f"Training images: {len(train_dataset)}"
    )

    print(
        f"Validation images: {len(validation_dataset)}"
    )

    print()

    # --------------------------------------------------------------
    # Data loaders
    # --------------------------------------------------------------

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
    )

    # --------------------------------------------------------------
    # Model
    # --------------------------------------------------------------

    model = create_model()

    model.to(DEVICE)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        filter(
            lambda parameter: parameter.requires_grad,
            model.parameters(),
        ),
        lr=LEARNING_RATE,
    )

    # --------------------------------------------------------------
    # Training
    # --------------------------------------------------------------

    best_validation_accuracy = 0.0

    for epoch in range(
        1,
        EPOCHS + 1,
    ):

        train_loss, train_accuracy = (
            train_one_epoch(
                model,
                train_loader,
                criterion,
                optimizer,
            )
        )

        validation_loss, validation_accuracy = (
            evaluate(
                model,
                validation_loader,
                criterion,
            )
        )

        print(
            f"Epoch {epoch}/{EPOCHS}"
        )

        print(
            f"  Train Loss: "
            f"{train_loss:.4f}"
        )

        print(
            f"  Train Accuracy: "
            f"{train_accuracy * 100:.2f}%"
        )

        print(
            f"  Validation Loss: "
            f"{validation_loss:.4f}"
        )

        print(
            f"  Validation Accuracy: "
            f"{validation_accuracy * 100:.2f}%"
        )

        print()

        if validation_accuracy > best_validation_accuracy:

            best_validation_accuracy = (
                validation_accuracy
            )

            MODEL_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            torch.save(
                model.state_dict(),
                MODEL_PATH,
            )

            print(
                "Best model saved."
            )

    # --------------------------------------------------------------
    # Class mapping
    # --------------------------------------------------------------

    class_mapping = {
        str(index): class_name
        for index, class_name
        in enumerate(MODEL_CLASSES)
    }

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        CLASS_NAMES_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            class_mapping,
            file,
            indent=4,
        )

    print()
    print("=" * 55)

    print(
        "Training completed."
    )

    print(
        f"Best validation accuracy: "
        f"{best_validation_accuracy * 100:.2f}%"
    )

    print(
        f"Model: {MODEL_PATH}"
    )

    print(
        f"Class mapping: {CLASS_NAMES_PATH}"
    )


if __name__ == "__main__":
    main()