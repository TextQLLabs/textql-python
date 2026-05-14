from __future__ import annotations

import os
from typing import Any

import httpx

from ._version import __version__

DEFAULT_BASE_URL = "https://api.textql.com"
DEFAULT_TIMEOUT = 60.0


class TextQL:
    """Synchronous client for the TextQL Platform API.

    Resource clients (`chat`, `playbooks`, `sandbox`, `connectors`) are stubs
    in v0.1.0 — they will be filled in as the v2 SDK takes shape.
    """

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
            raise ValueError(
                "No API key provided. Pass api_key=... or set TEXTQL_API_KEY in the environment."
            )

        self.api_key = key
        resolved_base = base_url or os.environ.get("TEXTQL_BASE_URL") or DEFAULT_BASE_URL
        self.base_url = resolved_base.rstrip("/")
        self._http = http_client or httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._default_headers(),
        )

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": f"textql-python/{__version__}",
            "Accept": "application/json",
        }

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> TextQL:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
