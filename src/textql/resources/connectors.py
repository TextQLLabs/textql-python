from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import TextQL


class Connectors:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    def list(self) -> Any:
        return self._client.request("GET", "/v2/connectors")
