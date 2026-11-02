"""
FlowerVision AI

In-memory telemetry store for request traces, metrics, and logs.
"""

from __future__ import annotations

from collections import defaultdict, deque
from contextvars import ContextVar
from datetime import datetime, timezone
from threading import Lock
from typing import Any

TRACE_ID_CONTEXT: ContextVar[str | None] = ContextVar(
    "trace_id",
    default=None,
)

SENSITIVE_KEYWORDS = (
    "authorization",
    "token",
    "secret",
    "password",
    "cookie",
    "session",
    "credential",
    "email",
    "phone",
    "api_key",
    "file_name",
)


def get_current_trace_id() -> str | None:
    """Return the active trace ID from context, if one exists."""

    return TRACE_ID_CONTEXT.get()


def utc_now_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


def sanitize_payload(payload: Any) -> Any:
    """Remove sensitive metadata before storing telemetry."""

    if isinstance(payload, dict):
        sanitized: dict[str, Any] = {}

        for key, value in payload.items():
            lowered = str(key).lower()

            if any(keyword in lowered for keyword in SENSITIVE_KEYWORDS):
                continue

            sanitized[str(key)] = sanitize_payload(value)

        return sanitized

    if isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]

    return payload


class TelemetryStore:
    """Store request metrics, traces, and structured logs in memory."""

    _instance: "TelemetryStore | None" = None
    _lock = Lock()

    def __new__(cls) -> "TelemetryStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()

        return cls._instance

    def _initialize(self) -> None:
        self._metrics: dict[tuple[str, tuple[tuple[str, str], ...]], dict[str, Any]] = {}
        self._traces: deque[dict[str, Any]] = deque(maxlen=200)
        self._logs: deque[dict[str, Any]] = deque(maxlen=500)

    def record_metric(
        self,
        name: str,
        value: float,
        *,
        tags: dict[str, Any] | None = None,
        trace_id: str | None = None,
    ) -> dict[str, Any]:
        """Add a metric sample for a request or workflow."""

        safe_tags = sanitize_payload(tags or {})
        key = (
            name,
            tuple(sorted((str(key), str(value)) for key, value in safe_tags.items())),
        )

        with self._lock:
            bucket = self._metrics.setdefault(
                key,
                {
                    "name": name,
                    "tags": safe_tags,
                    "count": 0,
                    "total": 0.0,
                    "average": 0.0,
                    "min": None,
                    "max": None,
                    "updated_at": utc_now_iso(),
                    "trace_id": trace_id,
                },
            )

            bucket["count"] += 1
            bucket["total"] += float(value)
            bucket["average"] = bucket["total"] / bucket["count"]
            bucket["min"] = value if bucket["min"] is None else min(bucket["min"], value)
            bucket["max"] = value if bucket["max"] is None else max(bucket["max"], value)
            bucket["updated_at"] = utc_now_iso()
            bucket["trace_id"] = trace_id or bucket.get("trace_id")

        return {
            "name": bucket["name"],
            "tags": bucket["tags"],
            "count": bucket["count"],
            "total": bucket["total"],
            "average": bucket["average"],
            "min": bucket["min"],
            "max": bucket["max"],
            "updated_at": bucket["updated_at"],
            "trace_id": bucket["trace_id"],
        }

    def record_trace(
        self,
        *,
        trace_id: str,
        route: str,
        method: str,
        status_code: int,
        duration_ms: float,
        journey: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Store a completed trace summary for the key user journey."""

        payload = {
            "trace_id": trace_id,
            "journey": journey,
            "route": route,
            "method": method,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 3),
            "timestamp": utc_now_iso(),
            "metadata": sanitize_payload(metadata or {}),
        }

        with self._lock:
            self._traces.append(payload)

        return payload

    def record_log(
        self,
        level: str,
        message: str,
        *,
        event: str,
        trace_id: str | None = None,
        **metadata: Any,
    ) -> dict[str, Any]:
        """Store a structured log event with a trace ID."""

        payload = {
            "timestamp": utc_now_iso(),
            "level": level,
            "message": message,
            "trace_id": trace_id or get_current_trace_id(),
            "event": event,
            "metadata": sanitize_payload(metadata),
        }

        with self._lock:
            self._logs.append(payload)

        return payload

    def snapshot(self) -> dict[str, list[dict[str, Any]] | dict[str, Any]]:
        """Return a serializable snapshot of metrics, traces, and logs."""

        with self._lock:
            metrics = [
                {
                    "name": bucket["name"],
                    "tags": bucket["tags"],
                    "count": bucket["count"],
                    "total": bucket["total"],
                    "average": bucket["average"],
                    "min": bucket["min"],
                    "max": bucket["max"],
                    "updated_at": bucket["updated_at"],
                    "trace_id": bucket["trace_id"],
                }
                for bucket in self._metrics.values()
            ]
            traces = list(self._traces)
            logs = list(self._logs)

        return {
            "metrics": metrics,
            "traces": traces,
            "logs": logs,
        }


telemetry_store = TelemetryStore()

def get_telemetry_store() -> TelemetryStore:
    """Return the singleton telemetry store instance."""

    return telemetry_store
