from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .._client import TextQL


class Connectors:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    # v2:covers GET /v2/connectors
    def list(self) -> Any:
        return self._client.request("GET", "/v2/connectors")

    # v2:covers GET /v2/connectors/types
    def types(self) -> Any:
        return self._client.request("GET", "/v2/connectors/types")

    # v2:covers POST /v2/connectors
    def create(
        self,
        config: dict[str, Any],
        *,
        allow_sql_write_operations: bool | None = None,
        include_db_session_metadata: bool | None = None,
    ) -> Any:
        body: dict[str, Any] = {"config": config}
        if allow_sql_write_operations is not None:
            body["allow_sql_write_operations"] = allow_sql_write_operations
        if include_db_session_metadata is not None:
            body["include_db_session_metadata"] = include_db_session_metadata
        return self._client.request("POST", "/v2/connectors", json=body)

    # v2:covers POST /v2/connectors/test
    def test(self, config: dict[str, Any], *, connector_id: str | None = None) -> Any:
        body: dict[str, Any] = {"config": config}
        if connector_id is not None:
            body["connector_id"] = connector_id
        return self._client.request("POST", "/v2/connectors/test", json=body)

    # v2:covers PATCH /v2/connectors/:id
    def update(
        self,
        connector_id: int,
        config: dict[str, Any],
        *,
        allow_sql_write_operations: bool | None = None,
        include_db_session_metadata: bool | None = None,
    ) -> Any:
        body: dict[str, Any] = {"config": config}
        if allow_sql_write_operations is not None:
            body["allow_sql_write_operations"] = allow_sql_write_operations
        if include_db_session_metadata is not None:
            body["include_db_session_metadata"] = include_db_session_metadata
        return self._client.request("PATCH", f"/v2/connectors/{connector_id}", json=body)

    # v2:covers DELETE /v2/connectors/:id
    def delete(self, connector_id: int) -> Any:
        return self._client.request("DELETE", f"/v2/connectors/{connector_id}")
