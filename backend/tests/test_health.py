"""
Tests for health and root endpoints.
"""


def test_root_endpoint(client):
    """
    Verify the root endpoint.
    """

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "FlowerVision AI"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"
    assert data["documentation"] == "/docs"
    assert data["health"] == "/api/v1/health"


def test_health_endpoint(client):
    """
    Verify the health endpoint.
    """

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "FlowerVision AI"
    assert data["version"] == "1.0.0"
