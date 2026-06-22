from __future__ import annotations

import httpx
import respx

from textql import TextQL

BASE = "https://app.textql.com"


def _client() -> TextQL:
    return TextQL(api_key="tql_test")


@respx.mock
def test_models_list_path() -> None:
    route = respx.get(f"{BASE}/v2/models").mock(
        return_value=httpx.Response(200, json={"models": [{"id": "claude-opus-4-8"}]})
    )
    out = _client().models.list()
    assert route.called
    assert out["models"][0]["id"] == "claude-opus-4-8"
