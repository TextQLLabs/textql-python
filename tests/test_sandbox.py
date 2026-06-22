from __future__ import annotations

import json

import httpx
import pytest
import respx

from textql import TextQL

BASE = "https://app.textql.com"


def _client() -> TextQL:
    return TextQL(api_key="tql_test")


@respx.mock
def test_start_uses_sandcastles_path() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles").mock(
        return_value=httpx.Response(201, json={"sandbox_id": "org-1", "created_at": "t"})
    )
    _client().sandbox.start()
    assert route.called
    assert route.calls.last.request.url.path == "/v2/sandcastles"


@respx.mock
def test_start_with_sandbox_id_sends_body() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles").mock(return_value=httpx.Response(201, json={}))
    _client().sandbox.start(sandbox_id="org-abc")
    assert json.loads(route.calls.last.request.content) == {"sandbox_id": "org-abc"}


@respx.mock
def test_status_path() -> None:
    route = respx.get(f"{BASE}/v2/sandcastles/sb1").mock(
        return_value=httpx.Response(200, json={"status": "running"})
    )
    _client().sandbox.status("sb1")
    assert route.called


@respx.mock
def test_stop_path() -> None:
    route = respx.delete(f"{BASE}/v2/sandcastles/sb1").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    _client().sandbox.stop("sb1")
    assert route.called


@respx.mock
def test_execute_path_and_body() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles/sb1/execute").mock(
        return_value=httpx.Response(200, json={})
    )
    _client().sandbox.execute("sb1", code="print(1)")
    assert json.loads(route.calls.last.request.content) == {"code": "print(1)"}


@respx.mock
def test_list_path_and_params() -> None:
    route = respx.get(f"{BASE}/v2/sandcastles").mock(
        return_value=httpx.Response(200, json={"sandboxes": []})
    )
    _client().sandbox.list(status="all", limit=10, cursor="c1")
    assert dict(route.calls.last.request.url.params) == {
        "status": "all",
        "limit": "10",
        "cursor": "c1",
    }


@respx.mock
def test_executions_path_and_params() -> None:
    route = respx.get(f"{BASE}/v2/sandcastles/sb1/executions").mock(
        return_value=httpx.Response(200, json={"executions": []})
    )
    _client().sandbox.executions("sb1", limit=5)
    assert route.called
    assert dict(route.calls.last.request.url.params) == {"limit": "5"}


@respx.mock
def test_query_tql_path_branch() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles/sb1/query").mock(
        return_value=httpx.Response(200, json={"preview": "x"})
    )
    _client().sandbox.query(
        "sb1", connector_id=2, tql_path="portfolio/p.tql", params={"a": 1}, max_rows=50
    )
    assert json.loads(route.calls.last.request.content) == {
        "connector_id": 2,
        "tql_path": "portfolio/p.tql",
        "params": {"a": 1},
        "max_rows": 50,
    }


@respx.mock
def test_query_sql_branch() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles/sb1/query").mock(
        return_value=httpx.Response(200, json={"preview": "x"})
    )
    _client().sandbox.query("sb1", connector_id=2, query="select 1", dataframe_name="df")
    assert json.loads(route.calls.last.request.content) == {
        "connector_id": 2,
        "query": "select 1",
        "dataframe_name": "df",
    }


@respx.mock
def test_upload_file_path() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles/sb1/files").mock(
        return_value=httpx.Response(200, json={"filename": "a.txt", "size_bytes": 3})
    )
    _client().sandbox.upload_file("sb1", ("a.txt", b"abc"))
    assert route.called


def test_query_requires_exactly_one_of() -> None:
    c = _client()
    with pytest.raises(ValueError, match="exactly one of query or tql_path"):
        c.sandbox.query("sb1", connector_id=2)
    with pytest.raises(ValueError, match="exactly one of query or tql_path"):
        c.sandbox.query("sb1", connector_id=2, query="x", tql_path="y")


@respx.mock
def test_exec_path_and_body() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles/sb1/exec").mock(
        return_value=httpx.Response(200, json={"stdout": "hi\n", "exit_code": 0})
    )
    _client().sandbox.exec("sb1", command="echo hi", kind="bash", env={"X": "1"})
    assert json.loads(route.calls.last.request.content) == {
        "command": "echo hi",
        "kind": "bash",
        "env": {"X": "1"},
    }


@respx.mock
def test_list_files_path_and_params() -> None:
    route = respx.get(f"{BASE}/v2/sandcastles/sb1/files").mock(
        return_value=httpx.Response(200, json={"files": []})
    )
    _client().sandbox.list_files("sb1", path="sub")
    assert dict(route.calls.last.request.url.params) == {"path": "sub"}


@respx.mock
def test_download_file_returns_raw_bytes() -> None:
    respx.get(f"{BASE}/v2/sandcastles/sb1/files/out/data.csv").mock(
        return_value=httpx.Response(200, content=b"a,b\n1,2\n")
    )
    out = _client().sandbox.download_file("sb1", "out/data.csv")
    assert out == b"a,b\n1,2\n"


@respx.mock
def test_download_file_strips_leading_slash() -> None:
    route = respx.get(f"{BASE}/v2/sandcastles/sb1/files/x.txt").mock(
        return_value=httpx.Response(200, content=b"x")
    )
    _client().sandbox.download_file("sb1", "/x.txt")
    assert route.calls.last.request.url.path == "/v2/sandcastles/sb1/files/x.txt"


@respx.mock
def test_delete_file_path() -> None:
    route = respx.delete(f"{BASE}/v2/sandcastles/sb1/files/x.txt").mock(
        return_value=httpx.Response(200, json={"success": True})
    )
    _client().sandbox.delete_file("sb1", "x.txt")
    assert route.called


@respx.mock
def test_library_diff_path() -> None:
    route = respx.get(f"{BASE}/v2/sandcastles/sb1/library/diff").mock(
        return_value=httpx.Response(200, json={"has_changes": False})
    )
    _client().sandbox.library_diff("sb1")
    assert route.called


@respx.mock
def test_create_library_patch_body() -> None:
    route = respx.post(f"{BASE}/v2/sandcastles/sb1/library/patches").mock(
        return_value=httpx.Response(201, json={"patch_id": "p1"})
    )
    _client().sandbox.create_library_patch("sb1", title="t", description="d", draft=True)
    assert json.loads(route.calls.last.request.content) == {
        "title": "t",
        "description": "d",
        "draft": True,
    }
