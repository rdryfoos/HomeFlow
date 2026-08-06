# Clewseau consumer Break/Fix — peer review

**Date:** 2026-08-06  
**Tree:** `/Users/spudnik/HomesFlow-stock-clewseau` (Copy B)  
**Gift:** `/Users/spudnik/clewseau` (local dirty tree, `--dev` install)  
**Claim under test:** On a **stock Spec Kit** host, Clewseau Gate 2 refuses silent AC gaps and emits an honest **clew** — without HomesFlow’s embellished Spec Kit / craft-gate as the product under test.

**Not claimed:** Agent code identity across sessions; Copy A parity; Spec Kit community readiness; cold-agent discoverability (this session was already Spec-Kit/HomesFlow-aware).

---

## 1. Host stack (precondition)

| Layer | State |
|-------|--------|
| Product content | Kept (`HomesFlow.prd.md`, `specs/`, `ios/`, `glossary.md`, …) |
| HomesFlow Spec Kit overlay | Moved aside → `.specify.bak-homesflow` |
| Stock Spec Kit | `specify init --here --force --integration claude` (`specify 0.15.3.dev0`) |
| Constitution memory | Stock placeholder (`# [PROJECT_NAME] Constitution`) — **not** HomesFlow Constitution |
| Clewseau preset | `specify preset add --dev …/presets/clewseau` (v0.1.0) — appends onto stock templates |
| Clewseau Gate | `specify extension add --dev …/extensions/clewseau-gate` (v0.2.0) |
| Gate config | `registry: HomesFlow.prd.md`, `clew_path: clew.json` |
| **Witness** | `.specify/extensions/clewseau-gate/scripts/check-traceability.sh` only |
| Non-witness | `scripts/check-traceability.sh` (HomesFlow craft) left on disk; **ignored for pass/fail** |

Template composition (stock base + Clewseau append) confirmed via `specify preset resolve` for `constitution-template`, `spec-template`, `tasks-template`.

---

## 2. Method

**B-only deliberate Break/Fix** (no Copy A co-edit; no new PRD ID minted).

1. **Baseline** — Gate PASS; `AC-GUEST-05` = `verified` with named proof.  
2. **Break** — Rename the sole proof so it no longer matches Gate’s `test_ac_regex` (strip `AC_GUEST_05` from the test identifier). Leave no open `[ ]` task with `Traces: AC-GUEST-05` (so debt cannot excuse the gap).  
3. **Observe** — Clewseau Gate exit ≠ 0; clew written with `gate.ok=false` and row `status: GAP`.  
4. **Fix** — Restore the original test identifier.  
5. **Observe** — Gate PASS; row returns to `verified`; `GAP` count → 0.

Subject AC chosen because it was **verified**, had a **single** named proof, and had **no open tracked-debt** task (avoids conflating silent gap with declared debt).

| ID | Probe file | Baseline proof |
|----|------------|----------------|
| `AC-GUEST-05` | `ios/HomesFlowTests/PermissionServiceTests.swift` | `test_AC_GUEST_05_guest_cannot_update_step` |

---

## 3. Evidence

### 3.1 Baseline (before break)

```text
gate.ok = true
statusCounts = { verified: 61, tracked-debt: 13, GAP: 0, backlog: 5 }
AC-GUEST-05.status = verified
AC-GUEST-05.proofs = [test_AC_GUEST_05_guest_cannot_update_step @ PermissionServiceTests.swift]
```

### 3.2 Break

**Mutation (temporary):**

```swift
// was: func test_AC_GUEST_05_guest_cannot_update_step()
func test_guest_cannot_update_step_BREAK_PROBE() {
```

**Witness command:**

```bash
bash .specify/extensions/clewseau-gate/scripts/check-traceability.sh
```

**Result:**

```text
exit = 1
stdout/stderr:
  FAIL: silent gap: AC-GUEST-05 has no test and no open tracked-debt task
  Wrote clew.json (79 rows) gate.ok=False
  Clewseau Gate 2: FAILED
```

**clew.json (excerpt):**

```json
{
  "format": "clew",
  "schemaVersion": 3,
  "emitter": "clewseau-gate",
  "gate": {
    "ok": false,
    "failures": [
      {
        "kind": "silent-gap",
        "detail": "silent gap: AC-GUEST-05 has no test and no open tracked-debt task",
        "id": "AC-GUEST-05"
      }
    ]
  },
  "statusCounts": {
    "verified": 60,
    "tracked-debt": 13,
    "GAP": 1,
    "backlog": 5
  }
}
```

`AC-GUEST-05` row: `status: "GAP"`, `proofs: []`.

### 3.3 Fix

**Mutation reversed** — restored `test_AC_GUEST_05_guest_cannot_update_step` (working tree clean of probe rename).

**Result:**

```text
exit = 0
Wrote clew.json (79 rows) gate.ok=True
Clewseau Gate 2: OK (79 registry IDs)

gate.ok = true
statusCounts = { verified: 61, tracked-debt: 13, GAP: 0, backlog: 5 }
AC-GUEST-05.status = verified
AC-GUEST-05.proofs = [test_AC_GUEST_05_guest_cannot_update_step @ line 7]
```

---

## 4. Interpretation

| Expectation (promotion contract) | Observed |
|----------------------------------|----------|
| Silent AC gap → Gate refuses | Yes (`exit 1`, `kind: silent-gap`) |
| Clew written even on failure | Yes (`gate.ok=false`, row visible) |
| Status vocabulary `GAP` (AC only) | Yes (`AC-GUEST-05` → `GAP`) |
| Fix named proof → verified + gate.ok | Yes |
| Stock Spec Kit host (not HomesFlow `.specify`) | Yes (bak aside; stock constitution placeholder) |
| HomesFlow `scripts/check-traceability.sh` not the witness | Yes (unused for this cycle) |

**What this does *not* prove:** that a cold agent, without HomesFlow cursor rules / prior craft memory, would invent `@covers` / `Traces:` / `test_AC_*` from Clewseau templates alone. That needs a separate untainted session.

---

## 5. Reproduce

```bash
cd /Users/spudnik/HomesFlow-stock-clewseau

# Witness only
bash .specify/extensions/clewseau-gate/scripts/check-traceability.sh

# Break: rename test_AC_GUEST_05_* → a name without AC_GUEST_05 encoding
# Re-run witness → expect FAIL + GAP
# Fix: restore name → expect OK + verified
```

---

## 6. Peer review asks

1. Is stock Spec Kit + Clewseau `--dev` overlay accepted as the consumer host for this claim?  
2. Is a single-AC proof rename sufficient Break/Fix, or do you also want `missing-traces` / exact-set drift probes?  
3. Should `.specify.bak-homesflow` be deleted after review, or retained as forensic evidence?  
4. Cold-agent session next, or enough to treat Gate parity as green?
