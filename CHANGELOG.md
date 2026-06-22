# Changelog

All notable changes to the `textql` Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] — 2026-06-22

### Fixed
- Sandbox resource now targets `/v2/sandcastles`; the backend renamed the path from `/v2/sandboxes` with no alias, so every sandbox call was 404ing.

### Added
- Sandbox: `list` and `executions` (both cursor-paginated), and an optional `sandbox_id` on `start` to restart a specific sandbox.
- Sandbox `query`: `tql_path` (run a saved library `.tql`), `params`, and `max_rows`; enforces exactly one of `query`/`tql_path` client-side.
- Sandbox: `exec` (bash/python command → stdout/stderr/exit_code), `list_files`, `download_file` (raw bytes), `delete_file`, `library_diff`, and `create_library_patch`.
- Models resource: `list` (`GET /v2/models`) — the models a key may pass as the chat `model` field.
- Connectors: `types`, `create`, `test`, `update`, `delete` — `config` is passed through as proto-JSON; call `connectors.types()` for per-type fields.
- Route-drift guard: `tests/test_route_coverage.py` + vendored `tests/routes.manifest.json` (33 routes), and a scheduled `route-sync` workflow that opens a PR when the backend route set changes.

## [2.0.0] — 2026-05-14

### Changed
- Version realigned to 2.x to track the v2 Platform API surface.
- Releases publish to PyPI via Trusted Publishing.

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
