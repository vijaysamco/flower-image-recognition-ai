"""
FlowerVision AI

Prediction API Tests
"""

from io import BytesIO

from PIL import Image


SUPPORTED_FLOWERS = {
    "daisy",
    "dandelion",
    "rose",
    "sunflower",
    "tulip",
}


def create_test_image() -> bytes:
    """
    Create a valid JPEG image for API testing.
    """

    image = Image.new(
        "RGB",
        (224, 224),
        (255, 255, 255),
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
    )

    return buffer.getvalue()


def test_prediction(client):
    """
    Verify that the prediction endpoint successfully
    processes a valid image using the trained model.
    """

    image_bytes = create_test_image()

    response = client.post(
        "/api/v1/predict",
        files={
            "file": (
                "flower.jpg",
                image_bytes,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "flower.jpg"

    assert data["prediction"] in SUPPORTED_FLOWERS

    assert 0 <= data["confidence"] <= 100


def test_prediction_invalid_image(client):
    """
    Verify that invalid image content is rejected.
    """

    response = client.post(
        "/api/v1/predict",
        files={
            "file": (
                "invalid.jpg",
                b"not-a-real-image",
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 400