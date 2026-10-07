# Newsfragments

Each user-facing change gets a fragment named `<name>.<type>.md`, where
`<type>` is one of towncrier's defaults (`feature`, `fix`, `doc`, `removal`,
`change`) and `<name>` is an issue number or `+<unique-string>` when there
is no issue — e.g. `+schema-gate.feature.md`.

- Preview the changelog: `uv run towncrier build --draft`
- Build it (consumes fragments): `uv run towncrier build`
