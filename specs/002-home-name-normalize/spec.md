# Feature Specification: Home display name normalization

**Feature Branch**: `cursor/home-display-name-normalize-7716`

**Created**: 2026-08-06

**Status**: Draft

**Input**: PRD `FR-HOME-04` / `AC-HOME-15` — normalize home display names (trim ends; collapse internal whitespace). Pure helper; no UI; no sync.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Normalize home display names (Priority: P1)

Callers that need a canonical home display name receive a string with ends trimmed and runs of internal whitespace collapsed to a single space.

**Why this priority**: Sole scope of this thin slice; unit-testable without UI or sync.

**Independent Test**: Invoke the pure normalizer with strings that have leading, trailing, and repeated internal whitespace; assert the collapsed result.

**Acceptance Scenarios**:

1. **Given** a home display name with leading, trailing, or repeated internal whitespace, **When** it is normalized (`AC-HOME-15`), **Then** ends are trimmed and internal whitespace collapses to a single space.

---

### Edge Cases

- Empty string and whitespace-only input → empty string after normalize.
- Tabs/newlines treated as whitespace (collapsed like spaces).
- Already-normalized names are unchanged.
- Out of scope: UI wiring, persistence, sync, validation of empty names as save errors (existing home validation unchanged).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-HOME-04**: System MUST provide a pure helper that normalizes home display names by trimming ends and collapsing internal whitespace to a single space. No UI; no sync.

### Key Entities

- None (string transform only).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `AC-HOME-15` is proven by a named unit test (`test_AC_HOME_15_*`) covering trim + collapse.
- **SC-002**: Helper has no UI or network/sync side effects.

## Clewseau — durable IDs (required)

Inherited from PRD registry only:

| ID | Role |
|----|------|
| FR-HOME-04 | Functional requirement |
| AC-HOME-15 | Acceptance criterion |

## Risk & failure modes (required)

| Failure | User impact | Mitigation / trace |
|---------|-------------|-------------------|
| Helper not applied at call sites | Inconsistent display names in product (future) | Scope is pure helper only this slice; call-site wiring is out of scope |
| Silent AC gap | Gate 2 fail | `test_AC_HOME_15_*` + `@covers` |
