class SkillBridgeError(Exception):
    """Base exception for all SkillBridge AI errors."""


class DatabaseConnectionError(SkillBridgeError):
    """Raised when the database connection cannot be established."""


class LLMServiceError(SkillBridgeError):
    """Raised when an LLM call fails after retries."""


class VectorStoreError(SkillBridgeError):
    """Raised when a pgvector query or upsert operation fails."""


class GraphExecutionError(SkillBridgeError):
    """Raised when LangGraph graph execution encounters an unrecoverable state."""
