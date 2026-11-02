"""
FlowerVision AI

API Routes
"""

import time

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.core.logger import get_logger
from app.core.telemetry import get_current_trace_id, get_telemetry_store
from app.schemas.health import HealthResponse
from app.schemas.prediction import PredictionResponse
from app.services.image_processor import ImageProcessor
from app.services.predictor import Predictor
from app.utils.file_validator import FileValidator


logger = get_logger(__name__)

router = APIRouter()


# ------------------------------------------------------------------
# Services
# ------------------------------------------------------------------

image_processor = ImageProcessor()
predictor = Predictor()


# ------------------------------------------------------------------
# Root
# ------------------------------------------------------------------

@router.get("/")
async def root() -> dict:
    """
    API root endpoint.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "documentation": "/docs",
        "health": "/api/v1/health",
    }


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------

@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    """
    Return API health status.
    """

    return HealthResponse(
        status="healthy",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


# ------------------------------------------------------------------
# Flowers
# ------------------------------------------------------------------

@router.get(
    "/flowers",
)
async def flowers() -> dict:
    """
    Return supported flower classes.
    """

    classes = predictor.FLOWER_CLASSES

    return {
        "count": len(classes),
        "classes": classes,
    }


# ------------------------------------------------------------------
# Observability
# ------------------------------------------------------------------

@router.get(
    "/observability/telemetry",
)
async def observability_telemetry() -> dict:
    """Return the latest in-memory metrics, traces, and logs."""

    return get_telemetry_store().snapshot()


@router.get(
    "/observability/ui",
    response_class=HTMLResponse,
)
async def observability_ui() -> HTMLResponse:
    """Serve a simple UI for viewing recent telemetry data."""

    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>FlowerVision Observability</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2rem; background: #f6f7fb; color: #1f2937; }
                h1 { margin-bottom: 1rem; }
                .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
                .card { background: white; border-radius: 12px; padding: 1rem; box-shadow: 0 2px 12px rgba(15, 23, 42, 0.08); }
                table { width: 100%; border-collapse: collapse; }
                th, td { text-align: left; padding: 0.5rem; border-bottom: 1px solid #e5e7eb; vertical-align: top; }
                code { background: #f3f4f6; padding: 0.2rem 0.35rem; border-radius: 6px; }
            </style>
        </head>
        <body>
            <h1>FlowerVision Observability</h1>
            <div class="grid">
                <div class="card">
                    <h2>Metrics</h2>
                    <div id="metrics"></div>
                </div>
                <div class="card">
                    <h2>Traces</h2>
                    <div id="traces"></div>
                </div>
            </div>
            <div class="card" style="margin-top: 1rem;">
                <h2>Structured Logs</h2>
                <div id="logs"></div>
            </div>
            <script>
                async function loadTelemetry() {
                    const response = await fetch('/api/v1/observability/telemetry');
                    const data = await response.json();

                    const metrics = data.metrics || [];
                    const traces = data.traces || [];
                    const logs = data.logs || [];

                    document.getElementById('metrics').innerHTML = metrics.length
                        ? '<table><thead><tr><th>Name</th><th>Value</th><th>Tags</th></tr></thead><tbody>' + metrics.map((metric) => `
                            <tr>
                                <td><code>${metric.name}</code></td>
                                <td>${metric.average !== null ? metric.average.toFixed(2) : metric.count}</td>
                                <td>${JSON.stringify(metric.tags || {})}</td>
                            </tr>
                        `).join('') + '</tbody></table>'
                        : '<p>No metrics collected yet.</p>';

                    document.getElementById('traces').innerHTML = traces.length
                        ? '<table><thead><tr><th>Trace</th><th>Route</th><th>Status</th><th>Latency</th></tr></thead><tbody>' + traces.map((trace) => `
                            <tr>
                                <td><code>${trace.trace_id}</code></td>
                                <td>${trace.route}</td>
                                <td>${trace.status_code}</td>
                                <td>${trace.duration_ms} ms</td>
                            </tr>
                        `).join('') + '</tbody></table>'
                        : '<p>No traces collected yet.</p>';

                    document.getElementById('logs').innerHTML = logs.length
                        ? '<table><thead><tr><th>Time</th><th>Trace</th><th>Level</th><th>Message</th></tr></thead><tbody>' + logs.map((entry) => `
                            <tr>
                                <td>${entry.timestamp}</td>
                                <td><code>${entry.trace_id || 'n/a'}</code></td>
                                <td>${entry.level}</td>
                                <td>${entry.message}</td>
                            </tr>
                        `).join('') + '</tbody></table>'
                        : '<p>No logs collected yet.</p>';
                }

                loadTelemetry();
                setInterval(loadTelemetry, 5000);
            </script>
        </body>
        </html>
        """
    )


# ------------------------------------------------------------------
# Prediction
# ------------------------------------------------------------------

@router.post(
    "/predict",
    response_model=PredictionResponse,
)
async def predict(
    request: Request,
    file: UploadFile = File(...),
) -> PredictionResponse:
    """
    Predict the flower class from an uploaded image.
    """

    trace_id = getattr(request.state, "trace_id", get_current_trace_id())
    telemetry = get_telemetry_store()
    start_time = time.perf_counter()

    telemetry.record_metric(
        "flower_prediction_requests_total",
        1,
        tags={
            "journey": "flower_prediction",
            "path": "/api/v1/predict",
        },
        trace_id=trace_id,
    )
    telemetry.record_log(
        "INFO",
        "Prediction request accepted",
        event="flower_prediction.request",
        trace_id=trace_id,
        content_type=file.content_type,
        size_bytes=0,
    )

    logger.info(
        "Prediction request received | trace_id=%s | content_type=%s",
        trace_id,
        file.content_type,
    )

    # --------------------------------------------------------------
    # Validate uploaded file
    # --------------------------------------------------------------

    await FileValidator.validate(
        file
    )

    # --------------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:
        logger.warning(
            "Empty image file received | trace_id=%s | content_type=%s",
            trace_id,
            file.content_type,
        )
        telemetry.record_log(
            "WARNING",
            "Empty image file received",
            event="flower_prediction.validation",
            trace_id=trace_id,
            content_type=file.content_type,
        )

        raise HTTPException(
            status_code=400,
            detail="Uploaded image file is empty.",
        )

    telemetry.record_log(
        "INFO",
        "Image bytes validated",
        event="flower_prediction.processing",
        trace_id=trace_id,
        content_type=file.content_type,
        size_bytes=len(image_bytes),
    )

    # --------------------------------------------------------------
    # Process image
    # --------------------------------------------------------------

    try:
        image_tensor = image_processor.process(
            image_bytes
        )

    except ValueError as exc:

        logger.warning(
            "Invalid image uploaded | trace_id=%s | error=%s",
            trace_id,
            str(exc),
        )
        telemetry.record_log(
            "WARNING",
            "Invalid image uploaded",
            event="flower_prediction.validation",
            trace_id=trace_id,
            content_type=file.content_type,
            error=str(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # --------------------------------------------------------------
    # Run prediction
    # --------------------------------------------------------------

    result = predictor.predict(
        image_tensor
    )

    duration_ms = (time.perf_counter() - start_time) * 1000
    telemetry.record_metric(
        "flower_prediction_duration_ms",
        duration_ms,
        tags={
            "journey": "flower_prediction",
            "status": "success",
        },
        trace_id=trace_id,
    )
    telemetry.record_trace(
        trace_id=trace_id,
        route="/api/v1/predict",
        method=request.method,
        status_code=200,
        duration_ms=duration_ms,
        journey="flower_prediction",
        metadata={
            "prediction": result["prediction"],
            "confidence": result["confidence"],
        },
    )
    telemetry.record_log(
        "INFO",
        "Prediction completed",
        event="flower_prediction.result",
        trace_id=trace_id,
        prediction=result["prediction"],
        confidence=result["confidence"],
    )

    logger.info(
        "Prediction completed | trace_id=%s | prediction=%s | confidence=%s",
        trace_id,
        result["prediction"],
        result["confidence"],
    )

    # --------------------------------------------------------------
    # Return response
    # --------------------------------------------------------------

    return PredictionResponse(
        success=True,
        filename=file.filename or "unknown",
        prediction=result["prediction"],
        confidence=result["confidence"],
    )