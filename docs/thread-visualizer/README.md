# Thread Visualizer

Read-only projection of HomesFlow’s Gate 2 golden thread — for demo conversations.

**Principle:** this tool formats data that already lives in the repo. It does not create, store, or duplicate requirement truth.

## Open it

```bash
bash scripts/thread-visualizer-refresh.sh
open docs/thread-visualizer/index.html   # or any static file server
```

Because the page loads JSON via `fetch`, some browsers block `file://` requests. If that happens:

```bash
cd docs/thread-visualizer && python3 -m http.server 8765
# then visit http://127.0.0.1:8765/
```

## What you should see

1. **Descent** — one AC (default `AC-USER-04`) from PRD text → `@covers` modules → `test_AC_*` proof.
2. **Break the proof** — loads a seeded projection where that AC’s tests are stripped; status becomes `GAP` and the thread frays red. Same definition Gate 2 uses for a silent gap.
3. **Totals** — must match `bash scripts/check-traceability.sh` (registry IDs, AC count, ACs with tests).

## Regenerate after code changes

```bash
bash scripts/thread-visualizer-refresh.sh
```

Writes:

- `data/thread.json` — live Gate 2 projection
- `data/thread-broken.json` — same data with demo break on `AC-USER-04`
