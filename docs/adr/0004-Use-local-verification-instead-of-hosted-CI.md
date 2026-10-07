# 4. Use local verification instead of hosted CI

Date: 2026-10-06

## Status

Accepted

## Context

The repository has no git remote and no `.github/` workflows, but pre-commit and many dev tools are declared dependencies. Verification needs a single authoritative path that does not silently diverge from what a hosted CI would run.

## Decision

Treat `check.ps1` / `check.sh` as the CI equivalent: ruff → format check → mypy → spec contract (validate + drift gate) → docstring coverage → strict docs build → pytest with coverage gate, fail-fast. pre-commit uses local `system` hooks (`uv run ...`) so there are no remote repos or rev pins to maintain.

## Consequences

Verification depends on `uv` being on PATH and runs only on this machine. When a remote exists, wire the check scripts into a hosted workflow as-is (they are already portable bash + PowerShell).
