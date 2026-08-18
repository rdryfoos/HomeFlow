# Spec: Backlog

**Status**: Living document — not a feature spec, the spec home for
retirement-carried and anointed-but-unbuilt intent.

**Input**: `HomesFlow.prd.md` — IDs inherited from PRD. Do not mint new IDs in
this file. See PRD § ID Registry.

> This is not `specs/001-mvp/spec.md`'s scope. The active feature spec carries
> living intent only — statements the product is actually building. IDs land
> here instead when they've been anointed into backlog (`specs/backlog/tasks.md`)
> without a feature spec of their own yet, or when they've been retired: the
> tooling is gone, the intent is deliberately withdrawn, and the registry
> statement itself carries a `[TOMBSTONED ...]` note naming the resolution.
> Either way, the ID stays real and gate-legible; it just doesn't belong in a
> living feature's spec.

## Clewseau cold-agent trial (retired)

* **US-CLEW-01** — As a developer validating Clewseau, I want a tiny pure display-name normalizer with durable IDs, so a stock Spec Kit + Clewseau agent can take one AC from registry through proof without UI or sync scope. [TOMBSTONED 2026-08-18: cold-agent probe concluded; tooling archived at tag clew-era-final; retirement carried by T900, pending the retired state.]
* **FR-CLEW-01** — **Clewseau trial.** Pure helper `HomeDisplayName.normalized(_:)` collapses whitespace in home display names (no UI, no sync). Temporary probe ID — tombstone after the cold-agent trial. [TOMBSTONED 2026-08-18: cold-agent probe concluded; tooling archived at tag clew-era-final; retirement carried by T900, pending the retired state.]
* **AC-CLEW-01** — Given a home display name string, when `HomeDisplayName.normalized(_:)` runs, then leading and trailing whitespace are stripped and any internal run of whitespace collapses to a single space. [TOMBSTONED 2026-08-18: cold-agent probe concluded; tooling archived at tag clew-era-final; retirement carried by T900, pending the retired state.]
