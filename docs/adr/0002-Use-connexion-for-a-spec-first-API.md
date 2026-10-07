# 2. Use connexion for a spec-first API

Date: 2026-10-06

## Status

Accepted

## Context

Both `fastapi` and `connexion[flask]` were declared dependencies — competing API layers. The goal is schema-driven development: the OpenAPI spec must be the source of truth for routes, validation, generated models, contract tests, and clients.

## Decision

Use connexion (spec-first): routes and validation derive from `openapi/openapi.yaml`, handlers are wired via `operationId` + `x-openapi-router-controller`, and responses are validated against the spec. Keep the spec at OpenAPI 3.0.x — connexion 3.3 rejects 3.1 outright, and no 3.1-only features are used. fastapi stays declared but unused until deliberately adopted or removed.

## Consequences

Spec changes drive code: regenerating models (`codegen`) and contract tests follows automatically, and the check chain gates drift. FastAPI conveniences (DI, `Depends`) are unavailable. OpenAPI 3.1 features cannot be used until connexion supports them. Connexion 3.3's Flask app is ASGI internally — tests use `from_asgi` and starlette's `TestClient`.
