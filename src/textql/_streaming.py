from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any


class Stream:
    """Iterator over Server-Sent Events from a streaming response."""

    def __init__(self, response: Any) -> None:
        self._response = response
        self._iterator = self._parse_sse()

    def _parse_sse(self) -> Iterator[dict[str, Any]]:
        for line in self._response.iter_lines():
            if line.startswith("data: "):
                yield json.loads(line[6:])

    def __iter__(self) -> Stream:
        return self

    def __next__(self) -> dict[str, Any]:
        return next(self._iterator)

    def close(self) -> None:
        self._response.close()

    def __enter__(self) -> Stream:
        return self

    def __exit__(self, *_args: Any) -> None:
        self.close()
