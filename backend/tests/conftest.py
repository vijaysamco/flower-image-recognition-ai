"""
FlowerVision AI

Pytest Configuration
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Provide a FastAPI test client.

    The context manager ensures the application lifespan
    startup and shutdown events are executed correctly.
    """

    with TestClient(app) as test_client:
        yield test_client
