# TextQL Python SDK

[![PyPI version](https://img.shields.io/pypi/v/textql.svg)](https://pypi.org/project/textql/)
[![Python versions](https://img.shields.io/pypi/pyversions/textql.svg)](https://pypi.org/project/textql/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official Python SDK for the [TextQL Platform API](https://docs.textql.com).

> **Status:** v0.1.0 is a scaffolding release. Resource clients (`chat`, `playbooks`, `sandbox`, `connectors`) are stubs and not yet functional.

## Installation

```bash
pip install textql
```

Requires Python 3.9+.

## Quickstart

```python
from textql import TextQL

client = TextQL(api_key="tql_...")  # or set TEXTQL_API_KEY in the environment
```

Once resource clients land, the surface will look like:

```python
# Simple chat
response = client.chat.create(question="What was total revenue last quarter?")

# Streaming
for event in client.chat.stream(question="..."):
    print(event.text, end="", flush=True)

# File upload
response = client.chat.create(
    question="Analyze this",
    files=[{"path": "./sales.csv"}],
)
```

## Configuration

| Option | Env var | Default |
|---|---|---|
| `api_key` | `TEXTQL_API_KEY` | — (required) |
| `base_url` | `TEXTQL_BASE_URL` | `https://api.textql.com` |
| `timeout` | — | `60.0` seconds |

## Development

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check .
pyright
pytest
```

## Links

- [API documentation](https://docs.textql.com)
- [Changelog](CHANGELOG.md)
- [Issues](https://github.com/TextQLLabs/textql-python/issues)

## License

[MIT](LICENSE)
