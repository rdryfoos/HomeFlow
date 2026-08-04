# Thread Visualizer — Build Spec for HomesFlow

**For:** Claude in Cursor, building inside the HomesFlow repo.
**Purpose:** A read-only visualizer that renders HomesFlow's existing Gate 2 traceability chain as a showable artifact — the "golden thread" made visible for demo conversations (clients, and a collaborator named David).
**Status:** Build spec. The visual is a projection of real data; it must never become a second source of truth.

---

## The one non-negotiable principle

This tool **reads** the thread that already exists. It does not create, store, or duplicate any requirement truth. Every ID it displays must be extracted live from where that ID durably lives:

- Registry IDs from `HomesFlow.prd.md`
- Acceptance criteria from the PRD
- `@covers` annotations in the Swift source
- `test_AC_*` test names in the test suite

If the visualizer ever holds its own copy of an ID or a trace link, it has become a second registry and defeats its own purpose. It is a formatter over Gate 2's data, nothing more. When the code changes and regenerates, the visual changes. There is no hand-maintained diagram anywhere in this feature.

## Why this exists

HomesFlow's Gate 2 already enforces the chain: every acceptance criterion must be verified by a named test or explicitly tracked as debt, and silent gaps fail the build. That enforcement is currently legible only as a passing/failing script and a set of numbers. This tool makes the same chain *visible* — so someone across a table can see the trace from intent to proof, and see it break in real time.

## What to build, in order

### Part 1: The walker (the real artifact)

A script (language your call — Swift, or a small Node/Python tool in the repo tooling, whatever fits HomesFlow's existing Gate 2 tooling best; reuse the Gate 2 parser if one exists rather than writing a second parser).

It walks the repo and emits **structured data** (JSON) representing the thread. For each registry ID / acceptance criterion, it resolves the chain:

```
objective/requirement (PRD registry ID + AC text)
   -> implementation (Swift files/symbols carrying @covers for that ID)
      -> proof (test_AC_* tests naming that ID)
         -> status: verified | tracked-debt | blocked | GAP
```

The walker's output is the deliverable everything else formats. Design its JSON so a single requirement's full descent is one addressable object. Critically, it must mark the **gaps** — an AC with no test and no tracked-debt entry is the most important thing on the screen, not the least. Reuse Gate 2's own definition of a gap so the visualizer and the build agree exactly; they must never disagree about what counts as covered.

Verification for this part: the walker's totals must match Gate 2's own numbers (registry ID count, AC count, covered count). If the walker says 45 covered and Gate 2 says 45 covered, the walker is reading the thread correctly. If they disagree, the walker is wrong, not Gate 2.

### Part 2: The descent view (the demo)

A single-thread vertical rendering: pick one requirement, show its full descent top to bottom — requirement at top, implementation beneath, proof at the bottom, the ID as the through-line connecting all tiers. This is the money shot for the first conversation: "here is one intent, and here is the unbroken line to the proof it was delivered."

Design intent (do not skip): this must look deliberate, not like a raw dependency graph. Clean vertical, the ID quiet but present at each tier, generous spacing, one confident accent color for the intact thread. If HomesFlow or dryfoos.com has an existing visual language (there is a golden-thread motif on the site), echo it. A hairball node-graph of all 79 IDs is the wrong lead artifact; one clean descent is the right one. The full graph can be a secondary "and it scales" view, shown only after the single descent lands, and only to a technical audience.

### Part 3: The break state (the emotional beat)

The reason this beats a static slide: it must show a **broken thread going red, live**. Demonstrate that deleting a test (or renaming an AC so its `test_AC_*` no longer matches) causes that requirement's descent to visibly fray — the proof tier goes red, the status flips to GAP, and this mirrors exactly what Gate 2 would fail the build on. Seed a deliberate broken example for the demo rather than exposing real current gaps.

The pitch this enables: "watch — when the proof disappears, the thread shows it, and the build fails. You cannot quietly break this." That is the entire value proposition made visible. Prioritize this beat; an intact-only visualizer is worth far less than one that shows the break.

## What NOT to do

- Do not hand-draw or hand-place any nodes/edges. Everything renders from walker output.
- Do not create a new ID scheme or store IDs anywhere. Read from PRD / @covers / test names only.
- Do not let the visualizer's notion of "covered" drift from Gate 2's. One definition, reused.
- Do not lead with the full-graph hairball. Single descent first.
- Do not fake the break. It must reflect a real regeneration over real (or deliberately-seeded) repo state.

## Definition of done

1. Walker emits JSON whose totals match Gate 2's numbers exactly.
2. Descent view renders one real requirement's full chain, styled to show well.
3. Deleting/breaking a test causes that requirement to render red as a GAP on regeneration.
4. Nothing in the feature stores requirement truth; it is entirely a projection.

## Note for Rik (not for Cursor)

This is scoped to HomesFlow because HomesFlow's thread is real and populated (79 registry IDs, 50 ACs, 45 covered) — a compelling descent needs real data underneath it, and Spudnik's thread is still mostly empty scaffolding. The same walker pattern later ports to Spudnik's thread (objective -> policy -> skill -> test) once that repo's thread is populated, but the demo artifact should be built where the data already lives. Trace this work to STR-02 (convert experience into showable evidence) in your objectives, and note the durable-ID discipline it embodies is the same one at the center of the SpecDriven/David conversation — which makes this visualizer itself a demo asset for STR-03.
