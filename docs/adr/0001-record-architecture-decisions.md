# 1. Record architecture decisions

Date: 2026-10-06

## Status

Accepted

## Context

The project makes consequential, hard-to-reverse choices (framework, toolchain layout, verification strategy) that are otherwise discoverable only by reading config and scripts.

## Decision

We record each significant decision as an ADR in `docs/adr/`, using `adr-tools-python` (`uv run adr-init docs/adr`, `uv run adr-new "Title"`). ADRs are immutable once accepted; superseding a decision creates a new ADR linking to the old one.

## Consequences

Decisions and their trade-offs ship with the docs site. Every new ADR must be added to `nav` in `mkdocs.yml`, or the strict docs build fails — docs stay indexed by construction.
