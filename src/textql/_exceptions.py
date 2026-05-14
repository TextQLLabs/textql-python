from __future__ import annotations


class TextQLError(Exception):
    """Base class for all TextQL SDK errors."""


class APIError(TextQLError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id


class AuthenticationError(APIError):
    pass


class PermissionDeniedError(APIError):
    pass


class NotFoundError(APIError):
    pass


class RateLimitError(APIError):
    pass


class APIConnectionError(TextQLError):
    pass


class APITimeoutError(APIConnectionError):
    pass
