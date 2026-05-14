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
response = client.chat.create(
    "Analyze this data",
    files=["./sales.csv"],
)
```

## Resources

### Chat

```python
client.chat.list(limit=10)
client.chat.create("What connectors are available?")
client.chat.get("chat-uuid")
client.chat.stream("Summarize revenue")
client.chat.cancel("chat-uuid")
```

### Connectors

```python
client.connectors.list()
```

### Playbooks

```python
client.playbooks.list(limit=10)
pb = client.playbooks.create()
client.playbooks.update(pb["id"], name="Weekly Revenue", prompt="Summarize revenue by region")
client.playbooks.deploy(pb["id"])
client.playbooks.run(pb["id"])
client.playbooks.get(pb["id"])
client.playbooks.delete(pb["id"])
```

### Sandbox

```python
sb = client.sandbox.start()
sid = sb["sandbox_id"]

client.sandbox.execute(sid, code="import pandas as pd; print(pd.__version__)")
client.sandbox.query(sid, connector_id=1, query="SELECT * FROM sales LIMIT 10", dataframe_name="sales")
client.sandbox.upload_file(sid, "./data.csv")
client.sandbox.status(sid)
client.sandbox.stop(sid)
```

## Configuration

| Option | Env var | Default |
|---|---|---|
| `api_key` | `TEXTQL_API_KEY` | — (required) |
| `base_url` | `TEXTQL_BASE_URL` | `https://app.textql.com` |
| `timeout` | — | `60.0` seconds |

The `base_url` accepts a bare hostname (e.g. `app.textql.com`) or a full URL.

## Links

- [API documentation](https://docs.textql.com/api-reference/v2/introduction)
- [Changelog](CHANGELOG.md)
- [Issues](https://github.com/TextQLLabs/textql-python/issues)

## License

[MIT](LICENSE)
