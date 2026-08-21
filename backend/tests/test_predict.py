"""
FlowerVision AI

Prediction API Tests
"""

from io import BytesIO

from PIL import Image


def create_test_image() -> bytes:
    """
    Create a small valid JPEG image for testing.
    """

    image = Image.new(
        "RGB",
        (100, 100),
        (255, 255, 255),
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
    )

    return buffer.getvalue()


def test_prediction_without_model(client):
    """
    Verify that prediction returns 503 when the trained
    model is not available.
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

    assert response.status_code == 503

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == 503

    assert (
        "model"
        in data["error"]["message"].lower()
    )