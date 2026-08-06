# Tasks: Home display name normalization

**Input**: Design documents from `/specs/002-home-name-normalize/`

**Prerequisites**: plan.md, spec.md

**Tests**: Required for Gate 2 (`AC-HOME-15`)

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup

- [x] T001 Create feature artifacts under `specs/002-home-name-normalize/` — **Traces**: FR-HOME-04, AC-HOME-15

---

## Phase 2: Foundational

No shared infrastructure required.

---

## Phase 3: User Story 1 - Normalize home display names (Priority: P1) 🎯 MVP

**Goal**: Pure helper + AC proof

**Independent Test**: `test_AC_HOME_15_*` in HomesFlowTests

### Tests for User Story 1

- [x] T002 [P] [US1] Add `test_AC_HOME_15_*` covering trim + collapse in `ios/HomesFlowTests/HomeDisplayNameNormalizerTests.swift` — **Traces**: AC-HOME-15

### Implementation for User Story 1

- [x] T003 [P] [US1] Add `HomeDisplayNameNormalizer` with `@covers FR-HOME-04, AC-HOME-15` in `ios/HomesFlow/Core/Home/HomeDisplayNameNormalizer.swift` — **Traces**: FR-HOME-04, AC-HOME-15
- [x] T004 [US1] Regenerate Xcode project if needed (`cd ios && xcodegen generate`) — **Traces**: FR-HOME-04

**Checkpoint**: Helper unit-tested; Gate 2 green for new IDs

---

## Phase 4: Polish

- [x] T005 Run Clewseau Gate 2 (`bash .specify/extensions/clewseau-gate/scripts/check-traceability.sh`) — **Traces**: FR-HOME-04, AC-HOME-15
- [x] T006 [P] SwiftLint production Swift if touched — **Traces**: FR-HOME-04

## Clewseau — Traces (required)

Every task declares registry IDs via `**Traces**:`. No invented IDs.
