from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from .._client import TextQL
    from .._streaming import Stream

FileInput = Union[str, Path, "tuple[str, bytes]"]


class Chat:
    def __init__(self, client: TextQL) -> None:
        self._client = client

    # v2:covers GET /v2/chats
    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search_term: str | None = None,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search_term is not None:
            params["search_term"] = search_term
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_direction is not None:
            params["sort_direction"] = sort_direction
        return self._client.request("GET", "/v2/chats", params=params)

    # v2:covers POST /v2/chats
    def create(
        self,
        question: str,
        *,
        chat_id: str | None = None,
        connector_ids: list[int] | None = None,
        tools: dict[str, Any] | None = None,
        files: list[FileInput] | None = None,
    ) -> Any:
        if files:
            return self._create_multipart(
                question, chat_id=chat_id, connector_ids=connector_ids, files=files
            )
        body: dict[str, Any] = {"question": question}
        if chat_id is not None:
            body["chat_id"] = chat_id
        if connector_ids is not None:
            body["connector_ids"] = connector_ids
        if tools is not None:
            body["tools"] = tools
        return self._client.request("POST", "/v2/chats", json=body)

    def _create_multipart(
        self,
        question: str,
        *,
        chat_id: str | None = None,
        connector_ids: list[int] | None = None,
        files: list[FileInput],
    ) -> Any:
        fields: list[tuple[str, str]] = [("question", question)]
        if chat_id is not None:
            fields.append(("chat_id", chat_id))
        if connector_ids is not None:
            for cid in connector_ids:
                fields.append(("connector_ids", str(cid)))

        file_tuples: list[tuple[str, tuple[str, bytes]]] = []
        for f in files:
            if isinstance(f, tuple):
                file_tuples.append(("files", f))
            else:
                p = Path(f)
                file_tuples.append(("files", (p.name, p.read_bytes())))

        return self._client.request("POST", "/v2/chats", data=fields, files=file_tuples)

    # v2:covers GET /v2/chats/:id
    def get(self, chat_id: str) -> Any:
        return self._client.request("GET", f"/v2/chats/{chat_id}")

    # v2:covers POST /v2/chats/stream
    def stream(
        self,
        question: str,
        *,
        chat_id: str | None = None,
        connector_ids: list[int] | None = None,
        tools: dict[str, Any] | None = None,
    ) -> Stream:
        body: dict[str, Any] = {"question": question}
        if chat_id is not None:
            body["chat_id"] = chat_id
        if connector_ids is not None:
            body["connector_ids"] = connector_ids
        if tools is not None:
            body["tools"] = tools
        return self._client.stream_request("POST", "/v2/chats/stream", json=body)

    # v2:covers POST /v2/chats/:id/cancel
    def cancel(self, chat_id: str) -> Any:
        return self._client.request("POST", f"/v2/chats/{chat_id}/cancel")
