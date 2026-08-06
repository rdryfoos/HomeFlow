**Loop 1 pipeline-test exception** — not real product scope. Granted by Rik, 2026-08-04.
See spudnik `OBJECTIVES.md` ENG-02 and `docs/field-notes-pipeline.md` FN-05.

# Implementation Plan: Cannon Pipeline Smoke Test — Build-Diagnostics Constant

**Feature Branch**: `000-cannon-smoketest`

**Spec**: `specs/000-cannon-smoketest/spec.md`

**Status**: Draft

## Summary

Add a single read-only accessor, `BuildInfo.summary`, that combines the app's `CFBundleShortVersionString` and `CFBundleVersion` (from `Info.plist`) into one `"<version> (<build>)"` string, with `"unknown"` substituted per-component when a value is missing. This satisfies `FR-SMOKE-01` / `AC-SMOKE-01a`. No UI wiring, no new dependencies, no persistence.

## Where the code goes

- **`ios/HomesFlow/Core/Observability/BuildInfo.swift`** (new file)
  Placed alongside `CrashReporting.swift`, the existing diagnostics-flavored accessor in `Core/Observability`, since both read values out of the app bundle for build/crash diagnostics purposes and neither belongs to a Feature module.
  - `enum BuildInfo` with a static computed property `summary: String`.
  - Reads `CFBundleShortVersionString` and `CFBundleVersion` via `Bundle.main.object(forInfoDictionaryKey:)`, mirroring the existing `Bundle.main.object(forInfoDictionaryKey:) as? String` pattern already used in `CrashReporting.swift`.
  - Each component independently falls back to the literal string `"unknown"` when absent, empty, or not castable to `String` (per Clarifications).
  - Format: `"\(version) (\(build))"`.

- **`ios/HomesFlowTests/BuildInfoTests.swift`** (new file)
  Follows the existing `HomesFlowTests` convention (`XCTest` + `@testable import HomesFlow`, one `test_AC_<ID>_...` method per acceptance scenario — see `HomeValidatorTests.swift`).

## Dependencies

None beyond `Foundation` (`Bundle`). No changes to `Info.plist` — it already declares `CFBundleShortVersionString` (`1.0`) and `CFBundleVersion` (`1`) at `ios/HomesFlow/Resources/Info.plist`. No changes to the Xcode project structure beyond adding the two new files to their existing targets (`HomesFlow` app target, `HomesFlowTests` test target).

## Testing approach for AC-SMOKE-01a

`AC-SMOKE-01a`: given Info.plist declares a bundle short version string and a bundle version, `BuildInfo.summary` returns them combined as `"<version> (<build>)"`.

- **Test**: `HomesFlowTests/BuildInfoTests.swift::test_AC_SMOKE_01a_summary_combines_version_and_build()`
- Reads `BuildInfo.summary` directly (no UI, no network, no auth — matches the spec's "Independent Test" note).
- Since the test target runs against the real app bundle (`Bundle.main` resolves to the `HomesFlow` app bundle under `HomesFlowTests`), the test asserts against the actual `Info.plist` values already present (`"1.0 (1)"`), rather than mocking `Bundle`. This keeps the test minimal and avoids introducing a `Bundle`-injection seam that nothing else in the codebase needs yet.
- The missing-value fallback (Edge Cases) is implemented in `BuildInfo.swift` but intentionally left untested per Clarifications ("one test, happy path only").

## Out of scope (per spec Assumptions)

- No Settings/About screen wiring.
- No changes to `HomesFlow.prd.md` or `specs/001-mvp/`.
- No design review.
