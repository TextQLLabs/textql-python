from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from .._client import TextQL

FileInput = Union[str, Path, "tuple[str, bytes]"]


class Sandbox:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    def start(self) -> Any:
        return self._client._request("POST", "/v2/sandboxes")

    def status(self, sandbox_id: str) -> Any:
        return self._client._request("GET", f"/v2/sandboxes/{sandbox_id}")

    def stop(self, sandbox_id: str) -> Any:
        return self._client._request("DELETE", f"/v2/sandboxes/{sandbox_id}")

    def execute(self, sandbox_id: str, *, code: str) -> Any:
        return self._client._request(
            "POST", f"/v2/sandboxes/{sandbox_id}/execute", json={"code": code}
        )

    def query(
        self,
        sandbox_id: str,
        *,
        connector_id: int,
        query: str,
        dataframe_name: str | None = None,
    ) -> Any:
        body: dict[str, Any] = {"connector_id": connector_id, "query": query}
        if dataframe_name is not None:
            body["dataframe_name"] = dataframe_name
        return self._client._request("POST", f"/v2/sandboxes/{sandbox_id}/query", json=body)

    def upload_file(self, sandbox_id: str, file: FileInput) -> Any:
        if isinstance(file, tuple):
            name, content = file
        else:
            p = Path(file)
            name = p.name
            content = p.read_bytes()
        return self._client._request(
            "POST",
            f"/v2/sandboxes/{sandbox_id}/files",
            files=[("file", (name, content))],
        )
