# TextQL Python SDK

[![PyPI version](https://img.shields.io/pypi/v/textql.svg)](https://pypi.org/project/textql/)
[![Python versions](https://img.shields.io/pypi/pyversions/textql.svg)](https://pypi.org/project/textql/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official Python SDK for the [TextQL Platform API](https://docs.textql.com/api-reference/v2/introduction).

## Installation

```bash
pip install textql
```

Requires Python 3.9+.

## Quickstart

```python
from textql import TextQL

client = TextQL(api_key="tql_...")  # or set TEXTQL_API_KEY in the environment

# Ask a question
response = client.chat.create("What was total revenue last quarter?", connector_ids=[1])
print(response["response"])

# Stream a response
for event in client.chat.stream("Summarize sales by region"):
    if event["type"] == "text":
        print(event["text"], end="", flush=True)

# Upload files with a question
response = client.chat.create("Analyze this data", files=["./sales.csv"])
```

## Resources

### Chat

```python
client.chat.list(limit=10)
client.chat.create("What connectors are available?", connector_ids=[1])
client.chat.create("Analyze this", files=["./data.csv"])   # multipart upload
client.chat.stream("Summarize revenue")                     # returns a Stream iterator
client.chat.get("chat-uuid")
client.chat.cancel("chat-uuid")
```

### Connectors

`config` is the connector configuration as documented by `types()` — `connector_type`
plus a per-type block (e.g. `postgres`, `kdb`, `snowflake`).

```python
client.connectors.list()
client.connectors.types()   # every connector type and its fields (self-describing)

cfg = {
    "connector_type": "POSTGRES",
    "name": "prod-db",
    "postgres": {"host": "db.example.com", "port": 5432, "user": "ro", "password": "...", "database": "app"},
}
client.connectors.test(cfg)                       # {"success": bool, "error": str} — a failed connection is success=False, not an error
created = client.connectors.create(cfg, allow_sql_write_operations=False)
client.connectors.update(created["connector_id"], cfg)
client.connectors.delete(created["connector_id"])
```

### Models

```python
client.models.list()   # models a key may pass as the chat `model` field
```

### Playbooks

```python
client.playbooks.list(limit=10)
pb = client.playbooks.create()
client.playbooks.get(pb["id"])
client.playbooks.update(pb["id"], name="Weekly Revenue", prompt="Summarize revenue by region")
client.playbooks.deploy(pb["id"])
client.playbooks.run(pb["id"])           # run(..., dry_run=True) to validate without sending
client.playbooks.delete(pb["id"])
```

### Sandbox

A sandbox is a stateful Python/SQL workspace. Start one, run code or load connector
data into DataFrames, manage its files, then stop it.

```python
sb = client.sandbox.start()              # start(sandbox_id="...") restarts a specific one
sid = sb["sandbox_id"]

client.sandbox.list(status="all")        # also: limit=, cursor=
client.sandbox.status(sid)
client.sandbox.executions(sid)           # recorded run history (limit=, cursor=)

# Run code / commands
client.sandbox.execute(sid, code="import pandas as pd; print(pd.__version__)")
client.sandbox.exec(sid, command="ls -la")               # bash by default
client.sandbox.exec(sid, command="print('hi')", kind="python")

# Load connector data into a DataFrame (exactly one of query / tql_path)
client.sandbox.query(sid, connector_id=1, query="SELECT * FROM sales LIMIT 10", dataframe_name="sales")
client.sandbox.query(sid, connector_id=2, tql_path="portfolio/current_positions.tql", params={"as_of": "2026-01-01"}, max_rows=500)

# Files
client.sandbox.upload_file(sid, "./data.csv")
client.sandbox.list_files(sid)                           # path="subdir" to scope
content: bytes = client.sandbox.download_file(sid, "out/report.csv")
client.sandbox.delete_file(sid, "out/report.csv")

# Library write-back
client.sandbox.library_diff(sid)
client.sandbox.create_library_patch(sid, title="Add metric", description="...", draft=True)

client.sandbox.stop(sid)
```

## Errors

Non-2xx responses raise typed exceptions, all subclasses of `textql.APIError`:

```python
from textql import TextQL, NotFoundError, RateLimitError, AuthenticationError

try:
    client.chat.get("does-not-exist")
except NotFoundError as e:
    print(e.status_code, e.request_id)
```

Also exported: `PermissionDeniedError`, `APITimeoutError`, `APIConnectionError`.

## Configuration

| Option | Env var | Default |
|---|---|---|
| `api_key` | `TEXTQL_API_KEY` | — (required) |
| `base_url` | `TEXTQL_BASE_URL` | `https://app.textql.com` |
| `timeout` | — | `60.0` seconds |

The `base_url` accepts a bare hostname (e.g. `app.textql.com`) or a full URL. The
client is a context manager:

```python
with TextQL(api_key="tql_...") as client:
    client.connectors.list()
```

## Links

- [API documentation](https://docs.textql.com/api-reference/v2/introduction)
- [Changelog](CHANGELOG.md)
- [Issues](https://github.com/TextQLLabs/textql-python/issues)

## License

[MIT](LICENSE)
