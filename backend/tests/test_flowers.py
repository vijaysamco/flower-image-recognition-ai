"""
Tests for supported flower classes endpoint.
"""


def test_supported_flowers(client):
    """
    Verify the supported flower classes.
    """

    response = client.get("/api/v1/flowers")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 5

    assert data["classes"] == [
        "daisy",
        "dandelion",
        "rose",
        "sunflower",
        "tulip",
    ]


def test_supported_flowers_count(client):
    """
    Verify that the reported count matches
    the number of classes returned.
    """

    response = client.get("/api/v1/flowers")

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == len(data["classes"])
