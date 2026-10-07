# 3. Keep pytest config in pytest.ini

Date: 2026-10-06

## Status

Accepted

## Context

The convention was "all tool config lives in `pyproject.toml`". pytest-watch (`uv run ptw`, the TDD watch loop) probes pytest's inifile and parses it with `configparser` (plain INI) — it cannot parse TOML, so it crashes when pytest's configfile is `pyproject.toml`. Its `--config` workaround is worse: ptw forwards that flag to pytest as `-c`, hijacking pytest's own configuration.

## Decision

pytest's configuration lives in `pytest.ini` — pytest's highest-priority inifile, which ptw parses cleanly and, finding no `[pytest-watch]` section, falls back to defaults for. All other tool config stays in `pyproject.toml` `[tool.*]` sections.

## Consequences

`uv run ptw` works out of the box, but there are two config homes (documented in AGENTS.md). Never move pytest config back to `pyproject.toml`; never pass `--config` to ptw.
