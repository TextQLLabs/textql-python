# Tests

## Unit tests

```bash
pip install -e ".[dev]"
pytest tests/test_client.py
```

## Integration tests

Run against a live TextQL environment. Requires two env vars:

```bash
export TEXTQL_STAGING_API_KEY="..."
export TEXTQL_STAGING_BASE_URL="staging.textql.com"
pytest tests/test_integration.py -v
```

Tests are skipped automatically when the env vars are missing.

## Lint / type check

```bash
ruff check . && ruff format --check .
pyright
```
