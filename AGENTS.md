# AGENTS.md

Fresh `uv` scaffold: hello-world CLI, pydantic settings/models, and a schema-driven API layer (OpenAPI spec → generated models → connexion app → contract tests), with module boundaries enforced as architecture contracts. Verify claims against config below, not the README.

## Toolchain (verified)

- **uv-managed Python 3.14** — `.python-version` = `3.14`, `requires-python = ">=3.14"`. Don't target older versions.
- **src layout**: package at `src/driven_dev/`, console script `driven-dev = "driven_dev:main"`:
  - `settings.py` — pydantic-settings `Settings` + cached `get_settings()`; env prefix `DRIVEN_DEV_`, repo-root `.env` read if present (gitignored). Tests clear the cache via `get_settings.cache_clear()`.
  - `models.py` — hand-written domain models; the canonical layer.
  - `api_models.py` — **GENERATED** from `openapi/openapi.yaml`; never hand-edit.
  - `api.py` — connexion (spec-first) app: `create_app()` plus operation handlers wired by the spec (`operationId` + `x-openapi-router-controller`). Adding an operation = spec entry first, then the function.
- Build backend is `uv_build` — keep code inside `src/driven_dev/`.
- **BMad installed** (project scope, v6.13.0-next): `_bmad/` (config + shared scripts) and `.agents/skills/` (canonical skill copies), versions tracked in `skills-lock.json`. Ask the bmad agent to check updates; retired old copies are deliberately kept in `~/.agents/skills/`.
- Tests live in `tests/` (`test_contract.py` = schemathesis contract tests, `test_api.py` = endpoint integration, `test_specs.py` = Gherkin specs).

## Commands

```bash
uv sync                      # install deps + dev group (venv already synced)
uv run driven-dev            # run the CLI entrypoint
uv run python -m driven_dev.api  # serve the API on :8080 (cosmetic swagger-ui warning)
uv run ruff check .          # lint
uv run ruff format .         # format (--check to verify only)
uv run mypy                  # typecheck — no args needed; files configured in pyproject
uv run lint-imports          # architecture contracts (also a check-chain step)
uv run pytest                # tests; runs with coverage by default (addopts)
uv run ptw                    # watch mode: reruns suite on every save (TDD red-green loop)
uv run pre-commit run --files <paths>   # run hooks manually
uv run python render_diagrams.py  # regenerate docs/assets/*.png (needs graphviz `dot`)
.\check.ps1      # full verify chain (Windows); ./check.sh on unix
.\codegen.ps1    # regenerate api_models.py; add -Check for drift gate (./codegen.sh [--check])
.\clientgen.ps1  # typed client -> clients/ (gitignored artifact; ./clientgen.sh)
```

Verify order (both scripts and manual): `ruff check` → `ruff format --check` → `mypy` → **architecture** (`lint-imports`) → **spec contract** (`codegen -Check`) → **interrogate** → **docs build** → `pytest`. Fail-fast; **run `check.ps1` before considering work done** — it is the CI equivalent.

Single test: `uv run pytest path/to/test_file.py::test_name`.
Exit non-zero if zero tests are collected.

## TDD workflow

Red → green → refactor. For each behavior:

1. **Red** — write the failing test in `tests/` first; run only it (`uv run pytest tests/test_foo.py::test_bar`) and confirm it fails for the *right* reason (assertion/validation, not ImportError).
2. **Green** — implement in `src/driven_dev/` until that single test passes.
3. **Verify** — `.\check.ps1` (full chain incl. contract + coverage gate) before considering it done.

`uv run ptw` re-runs the whole suite on every save for a live red-green loop (pytest args go after `--`; there is no single-pass mode — use `uv run pytest <file>` for one-off runs). A freshly compiled venv may print one-time docopt `SyntaxWarning`s from ptw — harmless, not a failure.
Property-based tests belong in `tests/test_properties.py` (hypothesis pattern); contract-driven ones in `tests/test_contract.py` (schemathesis `@parametrize`).

## Specification-driven work

Specs live in `docs/specs/` (template: `docs/specs/TEMPLATE.md`) — write one **before** implementing:

1. Draft the spec: purpose + acceptance criteria, each criterion mapping to **exactly one** test. Status starts `Proposed`.
2. Implement test-first (TDD workflow above) until every criterion is green, then flip Status to `Implemented`.
3. Behavior-level criteria are executable Gherkin: features in `tests/features/*.feature`, steps in `tests/test_specs.py`. Features are tagged `@spec` (registered in `pytest.ini`) — run the suite with `uv run pytest -m spec`; plain tests may carry `@pytest.mark.spec` too.
4. New spec files must be added to `nav` in `mkdocs.yml` or the strict docs build fails (same index-enforcement as ADRs).
5. Architecture choices go to ADRs, API shape to `openapi/openapi.yaml` — specs reference those, they don't restate them.

## Documentation

- **Docs site**: `uv run mkdocs serve` (live reload) / `uv run mkdocs build` (strict — runs in the check chain). Config is `mkdocs.yml`; `docs/` holds pages + ADRs, mermaid diagrams render client-side (kroki deliberately not enabled: it needs network at build time).
- **Docstrings are gated at 100%** on `src/` (`uv run interrogate src`) — every new module/class/function needs one; `api_models.py` is excluded (generated).
- **ADRs**: `uv run adr-new "Title"` → numbered record in `docs/adr/`. **Add new ADRs to `nav` in `mkdocs.yml`** or the strict docs build fails — that is the index-enforcement working, not a bug.
- **Diagrams**: `uv run python render_diagrams.py` → committed PNGs in `docs/assets/` (diagrams-as-code). Needs graphviz `dot` on PATH; deliberately **not** in the check chain (outputs are committed).
- **Changelog**: towncrier fragments in `newsfragments/<name>.<type>.md` (naming in `newsfragments/README.md`); preview with `uv run towncrier build --draft`, consume with `uv run towncrier build`.

## Config (verified working)

- **ruff**: line length 88, `target-version = "py314"`; strict-ish rule set — `B, C4, E, F, I, PIE, PTH, RUF, SIM, UP, W`, with `B008` ignored (FastAPI `Depends()` idiom). Skill/tool trees (`.agents`, `_bmad`, adapter dirs) are excluded via `extend-exclude` **plus `force-exclude = true`** — without force-exclude, ruff would lint paths pre-commit passes explicitly even when excluded.
- **mypy**: `strict = true` on `src` and `tests`, with `plugins = ["pydantic.mypy"]` and `[tool.pydantic-mypy]` (`init_typed`, `init_forbid_extra`) — new code must be fully typed; model constructors are type-checked at the call site. `connexion` has a `ignore_missing_imports` override (no py.typed).
- **pytest**: config lives in **`pytest.ini`**, not `pyproject.toml` — `testpaths = tests`, `--strict-config`, `--strict-markers`, `--cov=driven_dev` in `addopts`, `asyncio_mode = auto`. Coverage gate `--cov-fail-under=90` is applied by `check.ps1`/`check.sh`, **not** addopts — so single-test runs stay usable during the TDD loop.
- **interrogate**: `fail-under = 100` on `src/`, generated `api_models.py` excluded (pyproject `[tool.interrogate]`).
- **import-linter**: three contracts in pyproject `[tool.importlinter]` — leaves (models/settings/api_models) independent, leaves never import delivery (`driven_dev.api`), nobody imports the composition root. Root imports are pinned with `as_packages = false` (exact module — see Gotchas). Each contract was verified with a seeded violation.
- **towncrier**: fragments in `newsfragments/`, changelog → `CHANGELOG.md`, version read from installed package metadata (pyproject `[tool.towncrier]`).
- Adding tools? Put config in `pyproject.toml` `[tool.*]` sections — except pytest (**must** stay in `pytest.ini`, see below) and mkdocs (`mkdocs.yml` is the only format the tool accepts).

## Gotchas

- **OpenAPI must stay 3.0.x** — connexion 3.3 rejects `openapi: 3.1.x` outright. The spec uses no 3.1-only features; don't bump the field.
- **Spec/model drift is gated**: `check.ps1` runs `codegen -Check` (regenerates to a temp file with `--disable-timestamp`, compares via `git diff --no-index`). Changed `openapi/openapi.yaml`? Run `.\codegen.ps1` and commit `api_models.py`.
- **schemathesis loads the spec THROUGH the app**: `from_asgi("/openapi.yaml", app)` — connexion serves the spec itself, and `FlaskApp` is **ASGI** in connexion 3.3 (`from_wsgi` fails). Its `test_client()` returns starlette's `TestClient` (`response.json()` is a method).
- **pytest config must stay in `pytest.ini`** — pytest-watch probes pytest's inifile and parses it with configparser (plain INI); it cannot parse TOML, so `uv run ptw` crashes if pytest's configfile is `pyproject.toml`. Follow-up trap: never pass `--config` to ptw — it forwards that flag to pytest as `-c`, hijacking pytest's own config.
- **Keep `.ps1` strings ASCII** — Windows PowerShell 5.1 reads scripts as ANSI (no BOM); a UTF-8 em-dash inside a string decodes to a curly quote, which PowerShell treats as a delimiter → "string missing terminator" parse errors.
- **import-linter's `forbidden` contracts skip overlapping pairs** — under the default `as_packages = true`, a source living *inside* the forbidden package is exempt, so `forbidden_modules = ["driven_dev"]` would silently match nothing (every module lives under `driven_dev`). The composition-root contract therefore pins the root with `as_packages = false` (exact module — legit `api -> driven_dev.settings` stays green, `api -> driven_dev` breaks). Related: the root package can't join a `layers` contract at all — it is the parent of the other entries and import-linter rejects "shared descendants".
- **graphviz is only needed to re-render `docs/assets/*.png`** (`uv run python render_diagrams.py`) — installed via `winget install Graphviz.Graphviz` at `C:\Program Files\Graphviz\bin`, added to **User PATH** (shells opened before that may still need a new session). Not part of the check chain; PNGs are committed.
- **pre-commit uses local `system` hooks** (`uv run ...`) — no remote repos/rev pins. Committing requires `uv` on PATH; hooks live at `.git/hooks/pre-commit` (installed).
- **No hosted CI** (`.github/` absent, no git remote) — `check.ps1` / `check.sh` are the CI equivalent; wire them into a workflow when a remote exists.
- **Cosmetic third-party noise**: app creation prints a swagger-ui warning (`connexion[swagger-ui]` not installed); pytest shows connexion/jsonschema `DeprecationWarning`s; mkdocs prints a Material-for-MkDocs banner about MkDocs 2.0. Not failures.
- **starlette's `TestClient` returns `httpx2.Response`** — starlette does `import httpx2 as httpx` (plain `httpx` is the deprecated fallback, also installed). Type fixture/step returns as `from httpx2 import Response`; importing `httpx` type-checks but mismatches at runtime boundaries.
- **fastapi is still a declared dep but unused** — connexion is the chosen API framework; drop fastapi or use it deliberately.
- Dev deps not wired up yet: `mkdocs-gen-files`, `mkdocs-kroki-plugin` (mermaid used instead), `pyinstaller`. (The rest — datamodel-code-generator, openapi-spec-validator, schemathesis, openapi-python-client, interrogate, adr-tools, towncrier, mkdocs/material/mkdocstrings, import-linter, diagrams — are wired via the scripts and config above.)
- **Skill/tool installers can touch `pyproject.toml`** — after any installer run, check `git diff pyproject.toml` (one added `pyinstaller` to main dependencies; it belongs in dev-only). Adapter dirs `.claude`, `.continue`, `.goose`, `.openhands`, `.roo` are **junctions** to `.agents/skills` and are gitignored — committing them would duplicate every skill file; `.kilo` and `.specify` hold real files (spec-kit) and are committed.
- Git repo has commits on `master` but **no remote**. Never commit without explicit user request.
