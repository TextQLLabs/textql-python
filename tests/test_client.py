from __future__ import annotations

import pytest

from textql import TextQL, __version__


def test_version_is_set() -> None:
    assert __version__


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TEXTQL_API_KEY", raising=False)
    with pytest.raises(ValueError, match="No API key"):
        TextQL()


def test_client_reads_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEXTQL_API_KEY", "tql_test_123")
    client = TextQL()
    assert client.api_key == "tql_test_123"


def test_client_explicit_api_key_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEXTQL_API_KEY", "from_env")
    client = TextQL(api_key="explicit")
    assert client.api_key == "explicit"


def test_client_strips_trailing_slash_from_base_url() -> None:
    client = TextQL(api_key="tql_x", base_url="https://example.com/")
    assert client.base_url == "https://example.com"


def test_client_normalizes_bare_hostname() -> None:
    client = TextQL(api_key="tql_x", base_url="staging.textql.com")
    assert client.base_url == "https://staging.textql.com"


def test_client_context_manager() -> None:
    with TextQL(api_key="tql_x") as client:
        assert client.api_key == "tql_x"


def test_client_has_resource_clients() -> None:
    client = TextQL(api_key="tql_x")
    assert hasattr(client, "chat")
    assert hasattr(client, "connectors")
    assert hasattr(client, "playbooks")
    assert hasattr(client, "sandbox")
