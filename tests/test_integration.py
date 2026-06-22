"""Integration tests against TextQL staging API.

Requires TEXTQL_STAGING_API_KEY and TEXTQL_STAGING_BASE_URL env vars.
"""

from __future__ import annotations

import os

import pytest

from textql import NotFoundError, Stream, TextQL

BASE_URL = os.environ.get("TEXTQL_STAGING_BASE_URL", "")
API_KEY = os.environ.get("TEXTQL_STAGING_API_KEY", "")

pytestmark = pytest.mark.skipif(
    not BASE_URL or not API_KEY,
    reason="TEXTQL_STAGING_BASE_URL and TEXTQL_STAGING_API_KEY required",
)


@pytest.fixture
def client():
    with TextQL(api_key=API_KEY, base_url=BASE_URL) as c:
        yield c


class TestConnectors:
    def test_list(self, client):
        result = client.connectors.list()
        assert isinstance(result, list)
        assert len(result) > 0
        first = result[0]
        assert "id" in first
        assert "name" in first
        assert "type" in first

    def test_types(self, client):
        result = client.connectors.types()
        assert "types" in result
        assert isinstance(result["types"], list)


class TestModels:
    def test_list(self, client):
        result = client.models.list()
        assert "models" in result
        assert isinstance(result["models"], list)


class TestChat:
    def test_list(self, client):
        result = client.chat.list(limit=2)
        assert "chats" in result
        assert "total_count" in result
        assert isinstance(result["chats"], list)
        assert len(result["chats"]) <= 2

    def test_create_and_get(self, client):
        created = client.chat.create("What connectors are available?")
        assert "response" in created
        assert "chat_id" in created
        assert "id" in created

        fetched = client.chat.get(created["chat_id"])
        assert "messages" in fetched
        assert "chat" in fetched
        assert len(fetched["messages"]) >= 2  # user + assistant

    def test_stream(self, client):
        events = []
        with client.chat.stream("Say hello in one word.") as stream:
            assert isinstance(stream, Stream)
            for event in stream:
                events.append(event)

        types = [e["type"] for e in events]
        assert types[0] == "metadata"
        assert types[-1] == "done"
        assert "text" in types
        assert events[-1]["status"] == "completed"

    def test_cancel(self, client):
        chats = client.chat.list(limit=1)
        chat_id = chats["chats"][0]["id"]
        result = client.chat.cancel(chat_id)
        assert "cancelled" in result

    def test_get_nonexistent_raises_not_found(self, client):
        with pytest.raises(NotFoundError):
            client.chat.get("00000000-0000-0000-0000-000000000000")


class TestPlaybooks:
    def test_crud_lifecycle(self, client):
        # list
        pbs = client.playbooks.list(limit=1)
        assert "playbooks" in pbs
        assert "total_count" in pbs

        # create
        created = client.playbooks.create()
        pb_id = created["id"]
        assert created["status"] == "draft"

        try:
            # get
            fetched = client.playbooks.get(pb_id)
            assert "playbook" in fetched
            assert fetched["playbook"]["id"] == pb_id

            # update
            updated = client.playbooks.update(pb_id, name="SDK Integration Test", prompt="test")
            assert updated["name"] == "SDK Integration Test"

            # deploy
            deployed = client.playbooks.deploy(pb_id)
            assert "deployed_at" in deployed
            assert deployed["playbook_id"] == pb_id
        finally:
            # delete (cleanup)
            deleted = client.playbooks.delete(pb_id)
            assert "deleted_at" in deleted
            assert deleted["playbook_id"] == pb_id


class TestSandbox:
    def test_lifecycle(self, client):
        # start
        started = client.sandbox.start()
        sb_id = started["sandbox_id"]
        assert "created_at" in started

        try:
            # status
            st = client.sandbox.status(sb_id)
            assert st["status"] in ("running", "stopped")

            # list (the running sandbox should appear)
            listed = client.sandbox.list()
            assert "sandboxes" in listed
            assert any(s["sandbox_id"] == sb_id for s in listed["sandboxes"])

            # exec (bash)
            ex = client.sandbox.exec(sb_id, command="echo hi")
            assert ex["stdout"].strip() == "hi"
            assert ex["exit_code"] == 0

            # execute
            result = client.sandbox.execute(sb_id, code="print(2 + 2)")
            assert result["output"] == ["4"]
            assert result["execution_time_ms"] >= 0

            # execute with error
            result = client.sandbox.execute(sb_id, code="raise ValueError('boom')")
            assert result["error"] is not None
            assert result["output"] is None

            # query (use first available connector)
            connectors = client.connectors.list()
            if connectors:
                cid = connectors[0]["id"]
                qr = client.sandbox.query(
                    sb_id,
                    connector_id=cid,
                    query="SELECT 1 AS test",
                    dataframe_name="test_df",
                )
                assert qr["dataframe_name"] == "test_df"
                assert qr["num_rows"] >= 1

            # executions (the runs above should be recorded)
            execs = client.sandbox.executions(sb_id)
            assert "executions" in execs
            assert isinstance(execs["executions"], list)

            # files + library diff (read-only)
            files = client.sandbox.list_files(sb_id)
            assert "files" in files
            diff = client.sandbox.library_diff(sb_id)
            assert "has_changes" in diff
        finally:
            # stop (cleanup)
            stopped = client.sandbox.stop(sb_id)
            assert stopped["success"] is True
