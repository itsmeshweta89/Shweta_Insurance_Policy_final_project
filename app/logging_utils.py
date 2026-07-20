import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    """Format log records as compact JSON payloads."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "context"):
            payload["context"] = record.context
        return json.dumps(payload, default=str)


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Return a configured logger for the given module name."""
    logger = logging.getLogger(name)
    logger.setLevel((level or os.getenv("LOG_LEVEL") or "INFO").upper())
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


def log_event(logger: logging.Logger, event: str, **fields: Any) -> dict[str, Any]:
    """Emit a structured event and return the payload for tests or callers."""
    payload = {"event": event, **fields}
    logger.info("%s", event, extra={"event": event, "context": fields})
    return payload
