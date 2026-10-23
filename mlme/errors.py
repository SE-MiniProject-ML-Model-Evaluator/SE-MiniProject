"""Standard API error format (Architecture & Design Spec, Section 5.2)."""
import logging
import uuid

from rest_framework import status
from rest_framework.exceptions import (
    APIException, AuthenticationFailed, NotAuthenticated, NotFound, PermissionDenied, ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def error_response(code, message, http_status, details=None):
    """Build the standard error body: {"error": {code, message, details, request_id}}."""
    body = {"error": {"code": code, "message": message, "details": details or {},
                      "request_id": uuid.uuid4().hex[:8]}}
    return Response(body, status=http_status)


class ApiError(APIException):
    """Raise from views/services to return a specific error code."""

    def __init__(self, code, message, http_status=status.HTTP_400_BAD_REQUEST, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = http_status
        self.details = details or {}


def api_exception_handler(exc, context):
    if isinstance(exc, ApiError):
        return error_response(exc.code, exc.message, exc.status_code, exc.details)
    if isinstance(exc, ValidationError):
        return error_response("VALIDATION_ERROR", "Some fields are invalid.", 400, exc.detail)
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return error_response("AUTH_REQUIRED", "Please log in.", 401)
    if isinstance(exc, PermissionDenied):
        return error_response("FORBIDDEN", "You do not have access.", 403)
    if isinstance(exc, NotFound):
        return error_response("NOT_FOUND", "Not found.", 404)
    response = exception_handler(exc, context)
    if response is not None:
        return error_response("ERROR", str(getattr(exc, "detail", "Request failed.")), response.status_code)
    logger.exception("Unhandled API error")
    return error_response("INTERNAL_ERROR", "Something went wrong.", 500)
