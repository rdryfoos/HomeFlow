# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->



<!-- Clewseau (append) — constitution article -->

### Article: End-to-End Traceability (NON-NEGOTIABLE)

Every functional requirement, non-functional requirement, and acceptance criterion carries a durable unique ID of the form `<TYPE>-<DOMAIN>-<NN>` (e.g. `FR-LOG-01`, `AC-OFFL-03`). IDs are assigned once at the PRD level and are never reused or renumbered; retired IDs are tombstoned, not recycled.

1. Each acceptance criterion is **atomic** — one independently testable assertion — and maps to at least one automated test *or* an explicitly tracked debt entry. Silent-gap refusal is at **AC altitude**; US/FR/NFR IDs are planning labels (clew status `backlog`), not silent-gap candidates.
2. Every task in `tasks.md` MUST declare the ID(s) it implements via a `Traces:` field.
3. Every verifying test MUST encode the AC ID it protects. Every requirement-bearing source module MUST carry a coverage annotation naming the ID.
4. Coverage is **bidirectional** and machine-checked: no silent AC gaps, no untraced scope, and exact-set registry ≡ specs ≡ tasks. CI fails the build on any of these.
5. `/speckit.analyze` MUST report zero Clewseau traceability violations before `/speckit.implement` runs.

### Article: Clewseau vocabulary

Use these terms; do not invent synonyms (especially not “dossier”).

| Term | Meaning |
|------|---------|
| **clew** | The Gate-emitted traceability artifact (`format: "clew"`). Default filename `clew.json`. |
| **clew.json** | Usual on-disk path for a clew (configurable via Gate `clew_path`). |
| **Clewseau** | Spec Kit overlay: durable IDs, Gate 2, clew emission. Not Thorsten Schlathölter’s open-source `clew` tool. |
| **clewloupe** | Viewer that consumes a clew only — no target re-scan. |
| **verified** | Named carrier exists (AC proof and/or `@covers` / proof for US/FR/NFR). |
| **tracked-debt** | Incomplete, but declared on an open task with `Traces:`. |
| **GAP** | Silent AC gap — neither proof nor open debt; Gate refuses; thread frays. |
| **backlog** | US/FR/NFR with no own carrier — planning altitude, not a silent gap. |
| **Gate 2** | Deterministic Clewseau check + clew emit (`speckit.clewseau-gate.check`). |
