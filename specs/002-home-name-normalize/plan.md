# Implementation Plan: Home display name normalization

**Branch**: `cursor/home-display-name-normalize-7716` | **Date**: 2026-08-06 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-home-name-normalize/spec.md`

## Summary

Add a pure Swift policy helper that normalizes home display names (trim ends; collapse internal whitespace to one space). Prove with `test_AC_HOME_15_*` and `@covers FR-HOME-04, AC-HOME-15`. No UI, repository, or sync changes.

## Technical Context

**Language/Version**: Swift 5.9

**Primary Dependencies**: Foundation only

**Storage**: N/A

**Testing**: XCTest (`HomesFlowTests`)

**Target Platform**: iOS 17+

**Project Type**: iOS app (thin policy object)

**Performance Goals**: Negligible (string transform)

**Constraints**: Pure function; no UI; no sync (`FR-HOME-04`)

**Scale/Scope**: One helper + unit tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Product scope from PRD only — IDs `FR-HOME-04`, `AC-HOME-15` inherited, not minted in feature folder.
- Policy object for testable logic (craft conventions).
- Gate 2: `@covers` + `test_AC_*` (or open `Traces:` debt).

## Project Structure

### Documentation (this feature)

```text
specs/002-home-name-normalize/
├── plan.md
├── spec.md
├── tasks.md
└── checklists/requirements.md
```

### Source Code

```text
ios/HomesFlow/Core/Home/HomeDisplayNameNormalizer.swift
ios/HomesFlowTests/HomeDisplayNameNormalizerTests.swift
```

## Complexity Tracking

N/A — single pure helper.

## Phase 0 / Phase 1

No research, data-model, contracts, or quickstart needed (no entities, APIs, or integrations).
