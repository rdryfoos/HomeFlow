# Feature Specification: Home Display-Name Normalization

**Feature Branch**: `002-home-name-normalize`

**Created**: 2026-08-07

**Status**: Draft

**Input**: `HomesFlow.prd.md` — FR-HOME-04 (home display-name normalization).

> IDs inherited from PRD. Do not mint new IDs in this file. See PRD § ID Registry.

## Intended Use

Home display names are entered by people and often arrive with stray whitespace — leading/trailing spaces from copy-paste, double spaces between words, or embedded tabs and newlines. HomesFlow normalizes these names for display so the dashboard and home detail render clean, consistent titles. This is a pure, deterministic string helper: no UI wiring, no networking, and no sync behavior.

## Risk & failure modes

| Failure | User impact | Mitigation / trace |
|---------|-------------|-------------------|
| Ragged whitespace in a pasted name | Home title renders with double spaces or leading indentation | Normalize on display via pure helper; AC-HOME-15 |
| Tabs/newlines embedded in a name | Title wraps or shows control whitespace | Collapse all internal whitespace runs to a single space; AC-HOME-15 |
| Over-eager trimming of interior content | Words run together / meaning lost | Collapse runs to one space (never remove interior separators); AC-HOME-15 |

## User Scenarios & Testing

### User Story — Clean home display names (Priority: P3)

**ID**: FR-HOME-04

As a homeowner, I want home names to display without stray whitespace so my dashboard looks tidy regardless of how the name was typed or pasted.

**Why this priority**: Cosmetic polish on top of existing home CRUD (FR-HOME-01); depends on nothing and blocks nothing.

**Independent Test**: Feed representative raw names (leading/trailing whitespace, internal runs, tabs/newlines, already-clean, empty) to the normalizer and assert the collapsed, trimmed output.

**Acceptance Scenarios**:

1. **AC-HOME-15** — Given a raw home display name with leading/trailing whitespace and internal whitespace runs (spaces, tabs, or newlines), when it is normalized for display, then the result has no leading or trailing whitespace and every internal whitespace run is collapsed to a single space.

---

### Edge Cases

- Already-clean input returns unchanged.
- Empty string (or whitespace-only) normalizes to an empty string.
- Mixed whitespace kinds (space + tab + newline) in a single run collapse to one space.

## Requirements

### Functional Requirements

- **FR-HOME-04**: The system MUST normalize home display names for display by trimming leading/trailing whitespace and collapsing internal runs of whitespace to a single space. Pure helper; no UI, networking, or sync behavior (**AC-HOME-15**).

### Key Entities

- **Home** — Second-home property whose display `name` is normalized for presentation (FR-HOME-01 owns the entity; this feature only reads/normalizes the name string).

## Success Criteria

- **SC-01**: For any input string, `HomeDisplayName.normalized(_:)` returns a string with no leading/trailing whitespace and no internal whitespace run longer than a single space.

## Assumptions

- Whitespace is defined by Unicode/Swift `CharacterSet.whitespacesAndNewlines` (spaces, tabs, newlines, and related whitespace).
- Normalization is applied at display time only; the stored/entered value is not mutated.

## Out of Scope

- Any UI, view-model, networking, or sync changes.
- Case folding, Unicode NFC/NFD normalization, or profanity/length validation.
