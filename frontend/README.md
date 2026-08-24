# FlowerVision AI — Frontend

Lightweight web interface for FlowerVision AI.

## Features

- Upload flower images
- Drag and drop support
- Image preview
- AI flower prediction
- Confidence score
- Responsive design
- FastAPI backend integration

## Supported Flowers

- Daisy
- Dandelion
- Rose
- Sunflower
- Tulip

## Backend

The frontend connects to:

http://127.0.0.1:8000

Prediction endpoint:

POST /api/v1/predict

## Running

Start the backend first:

```bash
python -m uvicorn app.main:app --reload