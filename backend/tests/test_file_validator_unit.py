"""
Unit tests for file validation behavior.
"""

import asyncio
import io

import pytest
from fastapi import UploadFile

from app.utils.file_validator import FileValidator


@pytest.mark.unit
def test_validate_accepts_supported_image():
    """Supported image uploads should pass validation."""

    async def run_validation() -> None:
        file = UploadFile(
            filename="flower.jpg",
            file=io.BytesIO(b"valid-image-bytes"),
            headers={"content-type": "image/jpeg"},
        )
        await FileValidator.validate(file)

    asyncio.run(run_validation())


@pytest.mark.unit
def test_validate_rejects_missing_filename():
    """Uploads without a filename should fail early."""

    async def run_validation() -> None:
        file = UploadFile(
            filename="",
            file=io.BytesIO(b"valid-image-bytes"),
            headers={"content-type": "image/jpeg"},
        )

        with pytest.raises(Exception):
            await FileValidator.validate(file)

    asyncio.run(run_validation())
