from __future__ import annotations

import json

import httpx
import respx

from textql import TextQL

BASE = "https://app.textql.com"


def _client() -> TextQL:
    return TextQL(api_key="tql_test")


@respx.mock
def test_list_path() -> None:
    route = respx.get(f"{BASE}/v2/connectors").mock(return_value=httpx.Response(200, json=[]))
    _client().connectors.list()
    assert route.called


@respx.mock
def test_types_path() -> None:
    route = respx.get(f"{BASE}/v2/connectors/types").mock(
        return_value=httpx.Response(200, json={"types": []})
    )
    _client().connectors.types()
    assert route.called


@respx.mock
def test_create_body() -> None:
    route = respx.post(f"{BASE}/v2/connectors").mock(
        return_value=httpx.Response(201, json={"connector_id": 7})
    )
    cfg = {"connector_type": "POSTGRES", "name": "db", "postgres": {"host": "h"}}
    _client().connectors.create(cfg, allow_sql_write_operations=True)
    assert json.loads(route.calls.last.request.content) == {
        "config": cfg,
        "allow_sql_write_operations": True,
    }


@respx.mock
def test_test_returns_success_false_without_raising() -> None:
    respx.post(f"{BASE}/v2/connectors/test").mock(
        return_value=httpx.Response(200, json={"success": False, "error": "nope"})
    )
    out = _client().connectors.test({"connector_type": "KDB", "name": "k", "kdb": {}})
    assert out == {"success": False, "error": "nope"}


@respx.mock
def test_update_path_and_body() -> None:
    route = respx.patch(f"{BASE}/v2/connectors/9").mock(
        return_value=httpx.Response(200, json={"id": 9})
    )
    _client().connectors.update(9, {"connector_type": "POSTGRES", "name": "db"})
    assert route.called
    assert json.loads(route.calls.last.request.content) == {
        "config": {"connector_type": "POSTGRES", "name": "db"}
    }


@respx.mock
def test_delete_path() -> None:
    route = respx.delete(f"{BASE}/v2/connectors/9").mock(
        return_value=httpx.Response(200, json={"id": 9, "success": True})
    )
    _client().connectors.delete(9)
    assert route.called
