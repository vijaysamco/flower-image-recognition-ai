"""
FlowerVision AI

Phase 3 - Flower Dataset Downloader

Downloads the TensorFlow Flowers dataset and prepares the
five flower classes required by the FlowerVision AI model.
"""

from pathlib import Path
import shutil
import zipfile
from urllib.request import urlretrieve


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "training" / "dataset"
DOWNLOAD_DIR = PROJECT_ROOT / "training" / "downloads"

DATASET_URL = (
    "https://storage.googleapis.com/"
    "download.tensorflow.org/example_images/"
    "flower_photos.tgz"
)

ARCHIVE_PATH = DOWNLOAD_DIR / "flower_photos.tgz"

# Classes expected by the backend predictor.
FLOWER_CLASSES = [
    "daisy",
    "dandelion",
    "roses",
    "sunflowers",
    "tulips",
]


def download_dataset() -> None:
    """
    Download the TensorFlow Flowers dataset.
    """

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if ARCHIVE_PATH.exists():
        print("Dataset archive already exists.")
        return

    print("Downloading flower dataset...")
    print(f"URL: {DATASET_URL}")

    urlretrieve(
        DATASET_URL,
        ARCHIVE_PATH,
    )

    print("Download completed.")


def extract_dataset() -> Path:
    """
    Extract the downloaded dataset.
    """

    extracted_dir = DOWNLOAD_DIR / "flower_photos"

    if extracted_dir.exists():
        print("Dataset is already extracted.")
        return extracted_dir

    print("Extracting dataset...")

    import tarfile

    with tarfile.open(
        ARCHIVE_PATH,
        "r:gz",
    ) as archive:
        archive.extractall(DOWNLOAD_DIR)

    print("Extraction completed.")

    return extracted_dir


def prepare_five_class_dataset(
    source_dir: Path,
) -> None:
    """
    Copy only the five required flower classes
    into the project's dataset directory.
    """

    if DATASET_DIR.exists():
        shutil.rmtree(DATASET_DIR)

    DATASET_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for class_name in FLOWER_CLASSES:

        source_class_dir = source_dir / class_name
        target_class_dir = DATASET_DIR / class_name

        if not source_class_dir.exists():
            raise FileNotFoundError(
                f"Missing class directory: {source_class_dir}"
            )

        print(
            f"Preparing class: {class_name}"
        )

        shutil.copytree(
            source_class_dir,
            target_class_dir,
        )

    print()
    print("Dataset preparation completed.")
    print(f"Dataset location: {DATASET_DIR}")


def print_dataset_summary() -> None:
    """
    Print the number of images in each class.
    """

    print()
    print("Dataset Summary")
    print("=" * 40)

    total_images = 0

    for class_name in FLOWER_CLASSES:

        class_dir = DATASET_DIR / class_name

        image_count = len(
            [
                file
                for file in class_dir.iterdir()
                if file.is_file()
            ]
        )

        total_images += image_count

        print(
            f"{class_name:12} : {image_count}"
        )

    print("-" * 40)
    print(
        f"{'Total':12} : {total_images}"
    )


def main() -> None:
    """
    Execute the complete dataset preparation process.
    """

    print("FlowerVision AI")
    print("Phase 3 - Dataset Preparation")
    print("=" * 40)

    download_dataset()

    source_dir = extract_dataset()

    prepare_five_class_dataset(
        source_dir
    )

    print_dataset_summary()


if __name__ == "__main__":
    main()