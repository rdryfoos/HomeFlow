# Newbie trial — micro-AC candidates (Rik amends PRD)

**Principle:** You add exactly one atomic AC to `HomesFlow.prd.md` (and the ID registry table). The newbie fans it into Spec Kit and proves it. Prefer ACs that are **already true in code** so the exam is process + thread, not a multi-day feature.

Next free IDs (as of main): `AC-USER-08`, `AC-LOG-07`, `AC-GUEST-06`, `AC-PROC-09`, `AC-SYNC-08`, `AC-HOME-15`, `AC-A11Y-04`.

---

## Candidate A — **Recommended:** `AC-USER-08` (invite is Owner-only)

**Why:** Atomic; unit-testable via `PermissionService`; already implemented (`invite` actions true only for `.owner`); clearly implied by FR-USER-01 / US-ADMIN-02 but not an explicit AC today. Forces Spec Kit + `@covers` + `test_AC_USER_08_*` without UI work.

**PRD placement:** under `### US-ADMIN-02 / FR-USER-01 — Owner invites users` (near AC-USER-01…03, AC-USER-07).

**Suggested text:**
> **AC-USER-08** — Given a Manager or Guest user for a home, when they attempt to create, resend, or revoke an invite for that home, then the app denies the action.

**Registry:** add `AC-USER-08` to the ID table; keep `AC-USER-01 … AC-USER-07` row accurate (either extend range or add a line).

**Likely touch points:** `PermissionService.swift` (`@covers`), new/extended test in `PermissionServiceTests` / `MemberInviteTests`, `specs/001-mvp/{spec,plan,tasks}.md`.

**Effort:** small. Best default for the first trial.

---

## Candidate B — `AC-LOG-07` (Log Book entries are not deletable)

**Why:** Append-only / grace-window edit is in FR-LOG-02; “no delete” is enforced in permissions/tests today but not named as its own AC. Slightly more product-judgment (is delete forever forbidden?).

**PRD placement:** under Log Book ACs (AC-LOG-01…06).

**Suggested text:**
> **AC-LOG-07** — Given an Owner or Manager views a Log Book entry, when they attempt to delete it, then the app rejects the deletion (entries may be edited only within the grace window; they are never deleted).

**Likely touch points:** `PermissionService` logBook delete cases, `LogBookTests` named `test_AC_LOG_07_*`.

**Effort:** small. Use if you want the trial in the Log Book domain.

---

## Candidate C — `AC-GUEST-06` (Guest cannot change membership / People admin)

**Why:** Owner-only People add is partly visible via AC-HOME-12 tests; an explicit Guest/Manager denial for membership mutate is a clean USER/GUEST rule. Slight overlap with AC-HOME-12 / invite rules — word carefully so it stays atomic and non-duplicate.

**PRD placement:** under Guest ACs or US-ADMIN-03.

**Suggested text:**
> **AC-GUEST-06** — Given a Guest user views People for a home, when they attempt to invite, change roles, or remove members, then the app denies the action and shows no membership-admin controls.

**Note:** Prefer Candidate A if you want zero overlap debates with AC-HOME-12. This one is better as a **second** trial AC.

**Effort:** small–medium (permission + possibly UI assertion policy).

---

## Not recommended for this trial
| ID / area | Why skip |
|-----------|----------|
| AC-HOME-09…11 | Needs snapshot/XCUITest infra; tracked debt already |
| AC-SYNC-02 | Explicitly deferred post-MVP |
| AC-USER-03 | Real product work (offline invite conflict); heavier than a procedure exam |
| Thread visualizer replay | Craft tooling; weak Spec Kit product signal |

---

## Your move
1. Pick A (default), B, or C.  
2. Land the PRD-only amendment on `main` yourself (or ask an agent: **PRD text only**, no tasks/tests).  
3. Hand the newbie `newbie-homesflow.con.txt` + the AC ID.  
4. Score with `newbie-trial-scorecard.PRIVATE.txt`.
