# 5. Enforce module architecture with import-linter

Date: 2026-10-06

## Status

Accepted

## Context

The package grew distinct modules — composition root (`driven_dev`),
delivery (`api`), domain (`models`), generated DTOs (`api_models`), and
configuration (`settings`) — whose boundaries were documented only as prose
in AGENTS.md. Prose boundaries rot: nothing fails when a leaf module starts
importing the delivery layer, or when the composition root becomes a
dependency of everything else.

import-linter (already a declared dev dependency) turns those boundaries
into executable contracts.

## Decision

Keep three contracts in pyproject `[tool.importlinter]`, gated in the check
chain right after mypy:

1. **independence** — `models`, `settings`, and `api_models` never import
   each other;
2. **forbidden** — the leaves never import `driven_dev.api` (delivery);
3. **forbidden** — no module imports the composition root, with
   `as_packages = false`.

Two shape constraints drove the design:

- A **layers** contract was rejected: the root package is the parent of
  every other layer entry, and import-linter rejects layers with "shared
  descendants".
- `as_packages = false` on contract 3 is required because the default
  package-overlap rule **skips** any forbidden pair where the source lives
  inside the forbidden package — with sources living under `driven_dev`,
  a forbidden entry of `driven_dev` would be silently dead. Exact-module
  matching keeps `api -> driven_dev.settings` legal while catching
  `api -> driven_dev` itself.

Each contract was verified with a seeded violation: legitimate
`api -> settings` imports stay green; `api -> root`, `models -> api`,
`models -> settings`, and `models -> root` each break the expected contract.

## Consequences

Architecture violations fail locally and in the CI-equivalent chain before
tests even run. Changing the layering now requires editing the contracts —
and superseding this ADR if the structure itself changes. Tests are exempt
(`root_packages = driven_dev`), so fixtures may import anything.
