"""Error handling utilities for ERPNext MCP Server."""

import logging
from functools import wraps
from typing import Any, Callable, Dict
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class ERPNextError(Exception):
    """Base exception for ERPNext operations."""
    
    def __init__(self, message: str, error_code: str = "ERPNEXT_ERROR", details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class AuthenticationError(ERPNextError):
    """Authentication related errors."""
    
    def __init__(self, message: str = "Authentication failed", details: Dict[str, Any] = None):
        super().__init__(message, "AUTHENTICATION_ERROR", details)


class ValidationError(ERPNextError):
    """Validation related errors."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class NotFoundError(ERPNextError):
    """Resource not found errors."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "NOT_FOUND_ERROR", details)


class PermissionError(ERPNextError):
    """Permission related errors."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "PERMISSION_ERROR", details)


class ErrorResponse(BaseModel):
    """Standardized error response format."""
    
    success: bool = False
    error_code: str
    message: str
    details: Dict[str, Any] = {}


def handle_frappe_errors(func: Callable) -> Callable:
    """Decorator to handle and convert Frappe client errors."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e).lower()
            
            # Map common Frappe errors to our custom errors
            if "authentication" in error_message or "login" in error_message:
                raise AuthenticationError(f"Authentication failed: {str(e)}")
            elif "validation" in error_message or "invalid" in error_message:
                raise ValidationError(f"Validation error: {str(e)}")
            elif "not found" in error_message or "does not exist" in error_message:
                raise NotFoundError(f"Resource not found: {str(e)}")
            elif "permission" in error_message or "not allowed" in error_message:
                raise PermissionError(f"Permission denied: {str(e)}")
            else:
                # Generic ERPNext error
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                raise ERPNextError(f"ERPNext operation failed: {str(e)}")
    
    return wrapper


def format_error_response(error: ERPNextError) -> Dict[str, Any]:
    """Format error as standardized response."""
    
    return {
        "success": False,
        "error_code": error.error_code,
        "message": error.message,
        "details": error.details
    }


def format_success_response(data: Any, message: str = "Operation successful") -> Dict[str, Any]:
    """Format success response."""
    
    return {
        "success": True,
        "message": message,
        "data": data
    }