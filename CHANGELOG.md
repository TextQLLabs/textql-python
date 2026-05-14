# Changelog

All notable changes to the `textql` Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-05-14

### Added
- Chat resource: `list`, `create`, `get`, `stream` (SSE), `cancel`.
- Connectors resource: `list`.
- Playbooks resource: `list`, `create`, `get`, `update`, `deploy`, `delete`, `run`.
- Sandbox resource: `start`, `status`, `stop`, `execute`, `query`, `upload_file`.
- SSE streaming via `Stream` iterator with context manager support.
- Multipart file upload support for chat and sandbox.
- Automatic error mapping to typed exceptions (`NotFoundError`, `RateLimitError`, etc.).
- Bare hostname support for `base_url` (e.g. `app.textql.com`).
- Integration test suite against staging.

### Changed
- Default `base_url` from `https://api.textql.com` to `https://app.textql.com`.
- All endpoints target the v2 REST API (`/v2/*`).

## [0.1.0] — 2026-05-13

### Added
- Initial repository scaffolding: `pyproject.toml`, `src/textql/` package layout, exception hierarchy, sync client stub.
- CI workflow: ruff lint + format check, pyright strict, pytest on Python 3.9–3.13.
