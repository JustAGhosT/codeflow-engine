"""Error handling utilities."""

from typing import Any


class CodeFlowUtilsError(Exception):
    """Base exception for codeflow-utils-python."""
    pass


def format_error_message(
    operation: str,
    error: Exception,
    context: dict[str, Any] | None = None,
) -> str:
    """
    Format error message with context.

    Args:
        operation: Name of the operation that failed
        error: The exception that was raised
        context: Optional context dictionary

    Returns:
        Formatted error message
    """
    message = f"{operation} failed: {str(error)}"

    if context:
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        message += f" (context: {context_str})"

    return message


def create_error_response(
    error: Exception,
    operation: str | None = None,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create standardized error response dictionary.

    Args:
        error: The exception that was raised
        operation: Optional operation name
        context: Optional context dictionary

    Returns:
        Error response dictionary
    """
    response = {
        "error": type(error).__name__,
        "message": str(error),
    }

    if operation:
        response["operation"] = operation

    if context:
        response["context"] = context

    return response
