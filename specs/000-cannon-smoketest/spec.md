**Loop 1 pipeline-test exception** — not real product scope. Granted by Rik, 2026-08-04.
See spudnik `OBJECTIVES.md` ENG-02 and `docs/field-notes-pipeline.md` FN-05.

# Feature Specification: Cannon Pipeline Smoke Test — Build-Diagnostics Constant

**Feature Branch**: `000-cannon-smoketest`

**Created**: 2026-08-04

**Status**: Draft

**Input**: Ticket HOM-1 — "smoke-test the homesflow-sdd Cannon workflow end to end (Specify -> Clarify -> Plan -> Tasks/Gate1 -> Implement -> Gate2), not to ship a real feature." Suggested minimal scope taken as-is: expose a small build-diagnostics value in the iOS app (a `BuildInfo.summary` string combining bundle version + build number), covered by one atomic acceptance criterion and one test.

> This spec mints `FR-SMOKE-01` / `AC-SMOKE-01a` locally under the `SMOKE` domain, per exception granted above — the normal rule ("IDs are assigned at the PRD level; feature specs inherit them, never mint") does not apply here because there is no PRD entry to inherit from. This is the one place in the pipeline where minting is allowed.

## Intended Use

Engineers and CI running the Cannon pipeline use this feature to verify that the full Specify → Clarify → Plan → Tasks/Gate1 → Implement → Gate2 chain produces working, traceable, tested code — not to deliver end-user value. The only "user" of the shipped artifact is a developer or support engineer who wants to read the app's build version and build number as a single string (e.g. for a settings/about screen or a crash report) without duplicating the two individually.

## Risk & failure modes

| Failure | User impact | Mitigation / trace |
|---------|-------------|-------------------|
| `summary` reads a missing/malformed Info.plist key | Crash or garbled string in diagnostics output | Provide a safe fallback string when version or build values are absent; covered by AC-SMOKE-01a |
| Pipeline treats this smoke-test scope as real product scope and edits `HomesFlow.prd.md` / `specs/001-mvp/` | Corrupts the golden thread for the real MVP feature | Explicit exception banner at top of this spec; all work confined to `specs/000-cannon-smoketest/` |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read a combined build-diagnostics string (Priority: P1)

As a developer or support engineer, I want a single string that combines the app's bundle version and build number, so I can identify exactly which build produced a given diagnostic or crash report without cross-referencing two separate values.

**Why this priority**: It is the only story in this smoke-test feature — the pipeline needs one small, self-contained slice to exercise end-to-end.

**Independent Test**: Can be fully tested by reading `BuildInfo.summary` in isolation (no UI, no network, no auth) and asserting it renders the expected `"<version> (<build>)"` format from known Info.plist values.

**Acceptance Scenarios**:

1. **Given** the app's Info.plist declares a bundle short version string and a bundle version (build number), **When** `BuildInfo.summary` is read, **Then** it returns those two values combined into one human-readable string in the form `"<version> (<build>)"`.

---

### Edge Cases

- What happens when the bundle version or build number is missing from Info.plist (e.g. in a malformed test bundle)? `BuildInfo.summary` MUST NOT crash — it substitutes a placeholder (e.g. `"unknown"`) for the missing component.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-SMOKE-01**: The iOS app MUST expose a `BuildInfo.summary` string that combines the app's bundle short version string and bundle version (build number) into one human-readable value, with a safe fallback when either source value is unavailable.

### Key Entities *(include if feature involves data)*

- **BuildInfo**: A read-only diagnostics accessor. Not a persisted entity — it derives `summary` from the app bundle's `Info.plist` (`CFBundleShortVersionString`, `CFBundleVersion`) at read time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `BuildInfo.summary` returns a non-empty string in the `"<version> (<build>)"` format for a normally-configured build, verified by one automated unit test traced to `AC-SMOKE-01a`.
- **SC-002**: The full Cannon pipeline (Specify → Clarify → Plan → Tasks/Gate1 → Implement → Gate2) completes for this ticket without touching `HomesFlow.prd.md` or `specs/001-mvp/`.

## Assumptions

- This is a pipeline smoke test, not a real feature; no design review, UI surface, or PRD entry is expected or required.
- `BuildInfo.summary` need not be surfaced in any screen for this smoke test — the acceptance criterion is satisfied by the accessor and its unit test alone. Wiring it into a Settings/About screen is out of scope unless a later ticket asks for it.
- The iOS app's `Info.plist` already carries standard `CFBundleShortVersionString` / `CFBundleVersion` keys (confirmed present at `ios/HomesFlow/Resources/Info.plist`), so no new build-configuration work is needed to source these values.

## Clarifications

### Session 2026-08-04

- **Q**: Edge case wording: when a component (bundle version or build number) is missing from Info.plist, BuildInfo.summary "substitutes a placeholder (e.g. 'unknown') for the missing component." Should the exact placeholder be the literal string "unknown" (e.g. "unknown (42)" or "1.2.3 (unknown)"), or do you want a different fallback value/format?
  **A**: Use literal "unknown" per missing component, as drafted

- **Q**: The ticket scopes this to "one atomic acceptance criterion and one test." The spec's only formal Acceptance Scenario (AC-SMOKE-01a) covers the happy path (both values present). The missing-value fallback is described in Edge Cases as a MUST-NOT-crash requirement, but not as its own AC. Should the single required automated test cover ONLY the happy-path AC-SMOKE-01a (with the fallback behavior left as documented-but-untested), or do you want that one test to also exercise the missing-value fallback case?
  **A**: One test, happy path only (AC-SMOKE-01a) — fallback stays documented but untested
