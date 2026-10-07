# SPEC-NNNN: Title

Date: YYYY-MM-DD
Status: Proposed | Accepted | Implemented | Superseded

## Purpose

What behavior this specifies, and why it exists. One spec per coherent
behavior, not per code change.

## Acceptance criteria

Each criterion maps to **exactly one** test — a unit test, a property test,
or a Gherkin scenario in `tests/features/`. A criterion without a test
reference does not merge.

- [ ] Criterion — `tests/test_foo.py::test_bar`
- [ ] Criterion — `tests/features/x.feature` → "Scenario name"

## Out of scope

Explicit non-goals, so the spec stays checkable.

## Links

- Contract: `openapi/openapi.yaml` (if the spec is API-facing)
- ADRs: `docs/adr/...` (if the spec settles an architectural choice)
- Related specs
