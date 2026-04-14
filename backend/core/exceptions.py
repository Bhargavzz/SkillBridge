from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class SkillBridgeAPIException(Exception):
    """Base exception for all structured SkillBridge API errors.

    Subclasses hard-code status_code and code so call-sites only supply a message.
    The global FastAPI handler in main.py intercepts any instance of this class
    and serializes it via to_response_dict() into the standard error envelope.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.description = description
        self.metadata: dict[str, Any] = metadata or {}

    def to_response_dict(self, endpoint: str = "") -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "description": self.description,
                "metadata": {
                    "endpoint": endpoint,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    **self.metadata,
                },
            }
        }


class DatabaseConnectionError(SkillBridgeAPIException):
    def __init__(
        self,
        message: str = "Database unavailable",
        description: str | None = None,
    ) -> None:
        super().__init__(503, "DATABASE_CONNECTION_ERROR", message, description)


class LLMServiceError(SkillBridgeAPIException):
    def __init__(
        self,
        message: str = "LLM service error",
        description: str | None = None,
    ) -> None:
        super().__init__(502, "LLM_SERVICE_ERROR", message, description)


class VectorStoreError(SkillBridgeAPIException):
    def __init__(
        self,
        message: str = "Vector store error",
        description: str | None = None,
    ) -> None:
        super().__init__(502, "VECTOR_STORE_ERROR", message, description)


class GraphExecutionError(SkillBridgeAPIException):
    def __init__(
        self,
        message: str = "Graph execution failed",
        description: str | None = None,
    ) -> None:
        super().__init__(500, "GRAPH_EXECUTION_ERROR", message, description)
