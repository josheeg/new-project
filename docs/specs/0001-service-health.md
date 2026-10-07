# SPEC-0001: Service health endpoint

Date: 2026-10-06
Status: Implemented

## Purpose

Liveness probing: one unauthenticated `GET` that reports the service is up
and which version is deployed. Defined by the `Health` operation in
`openapi/openapi.yaml` and served by connexion.

## Acceptance criteria

Each criterion maps to exactly one test:

- [x] `GET /health` returns 200 with `status: "ok"` and the app `version` —
  `tests/test_api.py::test_health_returns_ok_and_version` and
  `tests/features/health.feature` → "Health check reports ok and the app version"
- [x] Unknown query parameters are rejected with 400 (strict validation) —
  `tests/test_api.py::test_health_rejects_unknown_query_params` and
  `tests/features/health.feature` → "Unknown query parameters are rejected"
- [x] Unknown paths fall through to 404 —
  `tests/test_api.py::test_unknown_path_is_404` and
  `tests/features/health.feature` → "Unknown paths fall through to 404"

## Out of scope

Authentication, metrics, and dependency checks (database, queue) — this
scaffold has none. Version string comes from package metadata, not the spec.

## Links

- Contract: `openapi/openapi.yaml` (`/health`)
- [ADR-0002: Use connexion for a spec-first API](../adr/0002-Use-connexion-for-a-spec-first-API.md)
