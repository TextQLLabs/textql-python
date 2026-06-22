from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from .._client import TextQL

FileInput = Union[str, Path, "tuple[str, bytes]"]


class Sandbox:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    # v2:covers POST /v2/sandcastles
    def start(self, *, sandbox_id: str | None = None) -> Any:
        body: dict[str, Any] = {}
        if sandbox_id is not None:
            body["sandbox_id"] = sandbox_id
        return self._client.request("POST", "/v2/sandcastles", json=body or None)

    # v2:covers GET /v2/sandcastles
    def list(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        return self._client.request("GET", "/v2/sandcastles", params=params)

    # v2:covers GET /v2/sandcastles/:id
    def status(self, sandbox_id: str) -> Any:
        return self._client.request("GET", f"/v2/sandcastles/{sandbox_id}")

    # v2:covers GET /v2/sandcastles/:id/executions
    def executions(
        self,
        sandbox_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        return self._client.request(
            "GET", f"/v2/sandcastles/{sandbox_id}/executions", params=params
        )

    # v2:covers DELETE /v2/sandcastles/:id
    def stop(self, sandbox_id: str) -> Any:
        return self._client.request("DELETE", f"/v2/sandcastles/{sandbox_id}")

    # v2:covers POST /v2/sandcastles/:id/execute
    def execute(self, sandbox_id: str, *, code: str) -> Any:
        return self._client.request(
            "POST", f"/v2/sandcastles/{sandbox_id}/execute", json={"code": code}
        )

    # v2:covers POST /v2/sandcastles/:id/query
    def query(
        self,
        sandbox_id: str,
        *,
        connector_id: int,
        query: str | None = None,
        tql_path: str | None = None,
        params: dict[str, Any] | None = None,
        max_rows: int | None = None,
        dataframe_name: str | None = None,
    ) -> Any:
        if (query is None) == (tql_path is None):
            raise ValueError("exactly one of query or tql_path is required")
        body: dict[str, Any] = {"connector_id": connector_id}
        if query is not None:
            body["query"] = query
        if tql_path is not None:
            body["tql_path"] = tql_path
        if params is not None:
            body["params"] = params
        if max_rows is not None:
            body["max_rows"] = max_rows
        if dataframe_name is not None:
            body["dataframe_name"] = dataframe_name
        return self._client.request("POST", f"/v2/sandcastles/{sandbox_id}/query", json=body)

    # v2:covers POST /v2/sandcastles/:id/files
    def upload_file(self, sandbox_id: str, file: FileInput) -> Any:
        if isinstance(file, tuple):
            name, content = file
        else:
            p = Path(file)
            name = p.name
            content = p.read_bytes()
        return self._client.request(
            "POST",
            f"/v2/sandcastles/{sandbox_id}/files",
            files=[("file", (name, content))],
        )
