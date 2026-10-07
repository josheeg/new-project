# driven-dev

Schema-driven development scaffold: the OpenAPI spec (`openapi/openapi.yaml`)
is the source of truth for generated models, the running API, contract tests,
and a typed client — wrapped in strict lint/type/test/docs gates.

## Quickstart

```bash
uv sync                          # install deps + dev group
uv run python -m driven_dev.api  # serve the API on :8080
.\check.ps1                      # full verify chain (./check.sh on unix)
uv run mkdocs serve              # docs at http://127.0.0.1:8000
.\clientgen.ps1                  # typed client -> clients/ (gitignored)
```

Requires [uv](https://docs.astral.sh/uv/) and Python 3.14 (managed by uv).

## Layout

- `src/driven_dev/` — package: `api` (connexion app), `models` (domain),
  `api_models` (generated), `settings`, CLI entrypoint
- `openapi/openapi.yaml` — the contract; change this first
- `tests/` — unit, integration, property (hypothesis), and contract
  (schemathesis) tests
- `docs/` — MkDocs site including [ADR decision records](docs/adr/)

## Docs & instructions

- `uv run mkdocs serve` — full documentation with API reference
- `AGENTS.md` — commands, TDD workflow, and repository gotchas
