from __future__ import annotations

import os
from typing import Any, NoReturn

import httpx

from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from ._streaming import Stream
from ._version import __version__
from .resources.chat import Chat
from .resources.connectors import Connectors
from .resources.playbooks import Playbooks
from .resources.sandbox import Sandbox

DEFAULT_BASE_URL = "https://app.textql.com"
DEFAULT_TIMEOUT = 60.0


class TextQL:
    """Synchronous client for the TextQL v2 Platform API."""

    chat: Chat
    connectors: Connectors
    playbooks: Playbooks
    sandbox: Sandbox

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: httpx.Client | None = None,
    ) -> None:
        key = api_key or os.environ.get("TEXTQL_API_KEY")
        if not key:
            raise ValueError("No API key provided. Pass api_key=... or set TEXTQL_API_KEY.")
        self.api_key = key

        resolved = base_url or os.environ.get("TEXTQL_BASE_URL") or DEFAULT_BASE_URL
        resolved = resolved.rstrip("/")
        if not resolved.startswith(("http://", "https://")):
            resolved = f"https://{resolved}"
        self.base_url = resolved

        self._http = http_client or httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._default_headers(),
        )

        self.chat = Chat(self)
        self.connectors = Connectors(self)
        self.playbooks = Playbooks(self)
        self.sandbox = Sandbox(self)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": f"textql-python/{__version__}",
            "Accept": "application/json",
        }

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            resp = self._http.request(method, path, **kwargs)
        except httpx.TimeoutException as e:
            raise APITimeoutError(str(e)) from e
        except httpx.ConnectError as e:
            raise APIConnectionError(str(e)) from e

        if resp.status_code >= 400:
            self._raise_for_status(resp)

        if not resp.content:
            return None
        return resp.json()

    def stream_request(self, method: str, path: str, **kwargs: Any) -> Stream:
        try:
            req = self._http.build_request(method, path, **kwargs)
            resp = self._http.send(req, stream=True)
        except httpx.TimeoutException as e:
            raise APITimeoutError(str(e)) from e
        except httpx.ConnectError as e:
            raise APIConnectionError(str(e)) from e

        if resp.status_code >= 400:
            resp.read()
            resp.close()
            self._raise_for_status(resp)

        return Stream(resp)

    def _raise_for_status(self, response: httpx.Response) -> NoReturn:
        message = response.text
        request_id: str | None = None
        try:
            body: dict[str, Any] = response.json()
            error: dict[str, Any] = body.get("error", {})
            msg: Any = error.get("message")
            if isinstance(msg, str):
                message = msg
            rid: Any = error.get("request")
            if isinstance(rid, str):
                request_id = rid
        except Exception:
            pass

        status = response.status_code
        if status == 401:
            raise AuthenticationError(message, status_code=status, request_id=request_id)
        if status == 403:
            raise PermissionDeniedError(message, status_code=status, request_id=request_id)
        if status == 404:
            raise NotFoundError(message, status_code=status, request_id=request_id)
        if status == 429:
            raise RateLimitError(message, status_code=status, request_id=request_id)
        raise APIError(message, status_code=status, request_id=request_id)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> TextQL:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
