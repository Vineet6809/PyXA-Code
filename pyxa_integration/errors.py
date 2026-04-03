class PyXAIntegrationError(Exception):
    """Base error for integration runtime."""


class AdapterUnavailableError(PyXAIntegrationError):
    """Raised when a platform adapter dependency is unavailable."""


class PlannerOutputError(PyXAIntegrationError):
    """Raised when planner output is not valid structured JSON."""


class ToolExecutionError(PyXAIntegrationError):
    """Raised when a tool invocation fails."""
