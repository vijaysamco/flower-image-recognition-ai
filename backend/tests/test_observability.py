"""
Integration tests for observability telemetry.
"""

from io import BytesIO

import pytest
from PIL import Image

pytestmark = pytest.mark.integration


def create_test_image() -> bytes:
    """Create a valid JPEG image for API testing."""

    image = Image.new(
        "RGB",
        (224, 224),
        (255, 255, 255),
    )

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_observability_trace_id_is_shared_across_signals(client):
    """A prediction request should emit trace-linked metrics, logs, and traces."""

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
        headers={"Authorization": "Bearer super-secret-token"},
    )

    assert response.status_code == 200

    trace_id = response.headers.get("X-Trace-ID")
    assert trace_id

    telemetry = client.get("/api/v1/observability/telemetry").json()
    assert any(item.get("trace_id") == trace_id for item in telemetry["traces"])
    assert any(item.get("trace_id") == trace_id for item in telemetry["logs"])
    assert any(
        item.get("trace_id") == trace_id
        and item.get("name") == "flower_prediction_requests_total"
        for item in telemetry["metrics"]
    )
    assert "super-secret-token" not in str(telemetry)

    ui_response = client.get("/api/v1/observability/ui")
    assert ui_response.status_code == 200
    assert "FlowerVision Observability" in ui_response.text
