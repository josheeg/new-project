# driven-dev

A **schema-driven development** scaffold: the OpenAPI spec is the source of
truth for generated models, the running API, contract tests, and clients —
with strict lint/type/test/docs gates around all of it.

## Quickstart

```bash
uv sync                       # install everything (incl. dev group)
uv run python -m driven_dev.api   # serve the API on :8080
.\check.ps1                   # full verification chain (./check.sh on unix)
uv run mkdocs serve           # live docs at http://127.0.0.1:8000
```

## The pipeline

Everything flows from `openapi/openapi.yaml`:

- **Generated models** — `codegen` renders `driven_dev.api_models`; the check
  chain fails if it drifts from the spec.
- **Running API** — connexion serves routes from the spec with strict
  request/response validation (see [Architecture](architecture.md)).
- **Contract tests** — schemathesis generates property-based requests from
  the spec and validates responses in-process.
- **Typed client** — `clientgen` renders a client package into `clients/`
  (build artifact, not committed).

## Working on the code

- Agent/contributor instructions live in `AGENTS.md` (commands, TDD
  workflow, gotchas).
- Tooling: uv + Python 3.14, ruff, mypy (strict), pytest (+ hypothesis),
  pre-commit with local hooks.
- Decision history lives in [Decision Records](adr/0001-record-architecture-decisions.md).
