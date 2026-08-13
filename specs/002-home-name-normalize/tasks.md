# Tasks: Home Display-Name Normalization

**Input**: [spec.md](./spec.md)

**Feature**: `002-home-name-normalize` | **Created**: 2026-08-07

## Format

- **Carries**: AC/FR/NFR ID(s) implemented
- **[P]**: Parallelizable

---

## Phase 1: Implementation

- [x] T001 Implement `HomeDisplayName.normalized(_:)` pure helper in `ios/HomesFlow/Core/Home/HomeDisplayName.swift` — trims leading/trailing whitespace and collapses internal whitespace runs to a single space; no UI, networking, or sync — **Carries**: FR-HOME-04, AC-HOME-15

## Phase 2: Tests

- [x] T002 [P] Unit test `test_AC_HOME_15_normalizes_whitespace` in `ios/HomesFlowTests/HomeDisplayNameTests.swift` — covers leading/trailing whitespace, internal runs, tabs/newlines, already-clean input, and empty string — **Carries**: AC-HOME-15
