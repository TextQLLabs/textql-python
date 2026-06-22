from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import TextQL


class Models:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    # v2:covers GET /v2/models
    def list(self) -> Any:
        return self._client.request("GET", "/v2/models")
