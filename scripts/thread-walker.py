#!/usr/bin/env python3
"""Thread walker — projection of Gate 2's golden thread as structured JSON.

Reads requirement truth only from where it already lives (PRD, @covers, test
names, tasks.md via Gate 2). Does not mint IDs or store a second registry.

Status for each AC comes from `scripts/check-traceability.sh --json` so the
visualizer and Gate 2 never disagree about covered vs gap vs tracked debt.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATE2 = REPO / "scripts" / "check-traceability.sh"
PRD = REPO / "HomesFlow.prd.md"
SRC_DIRS = [REPO / "ios" / "HomesFlow"]
TEST_DIRS = [REPO / "ios" / "HomesFlowTests", REPO / "ios" / "HomesFlowUITests"]

ID_RE = re.compile(r"(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?")
AC_TEXT_RE = re.compile(
    r"\*\*(AC-[A-Z][A-Z0-9]{1,5}-\d{2,}[a-z]?)\*\*\s*—\s*(.+)$"
)

# Visualizer-facing status vocabulary (mapped from Gate 2 status strings).
VIS_VERIFIED = "verified"
VIS_TRACKED = "tracked-debt"
VIS_GAP = "GAP"
VIS_OTHER = "other"


def run_gate2_json() -> list[dict]:
    result = subprocess.run(
        ["bash", str(GATE2), "--json"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def run_gate2_check() -> dict:
    """Run Gate 2 check; parse summary counts. Exit code 0/1 both yield stdout."""
    result = subprocess.run(
        ["bash", str(GATE2)],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    text = result.stdout + result.stderr
    counts = {
        "registryIds": None,
        "acs": None,
        "acsWithTests": None,
        "idsWithCovers": None,
        "gate2Passed": result.returncode == 0,
    }
    for line in text.splitlines():
        if "Registry IDs (PRD):" in line:
            counts["registryIds"] = int(line.rsplit(":", 1)[1].strip())
        elif "ACs in registry:" in line:
            counts["acs"] = int(line.rsplit(":", 1)[1].strip())
        elif "ACs with tests:" in line:
            counts["acsWithTests"] = int(line.rsplit(":", 1)[1].strip())
        elif "IDs with @covers in code:" in line:
            counts["idsWithCovers"] = int(line.rsplit(":", 1)[1].strip())
    return counts


def map_status(gate_status: str) -> str:
    if gate_status == "verified":
        return VIS_VERIFIED
    if gate_status == "gap":
        return VIS_GAP
    if gate_status in (
        "implemented-test-pending",
        "planned",
        "in-progress",
    ):
        return VIS_TRACKED
    return VIS_OTHER


def load_prd_ac_text() -> dict[str, str]:
    texts: dict[str, str] = {}
    for line in PRD.read_text(encoding="utf-8").splitlines():
        match = AC_TEXT_RE.search(line)
        if match:
            texts[match.group(1)] = match.group(2).strip()
    return texts


def expand_covers_token(token: str) -> list[str]:
    """Expand `AC-USER-04…06` / `AC-USER-04...06` into inclusive ID list."""
    token = token.strip().rstrip(",")
    ellipsis = re.match(
        r"^((?:FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-)(\d{2,}[a-z]?)(?:…|\.\.\.)(\d{2,}[a-z]?)$",
        token,
    )
    if not ellipsis:
        return [token] if ID_RE.fullmatch(token) else []
    prefix, start_s, end_s = ellipsis.group(1), ellipsis.group(2), ellipsis.group(3)
    start_n, end_n = int(re.match(r"\d+", start_s).group()), int(re.match(r"\d+", end_s).group())
    width = len(re.match(r"\d+", start_s).group())
    return [f"{prefix}{n:0{width}d}" for n in range(start_n, end_n + 1)]


def files_covering(ac_id: str) -> list[dict]:
    """Swift modules whose @covers line includes this ID (live grep, no cache)."""
    hits: list[dict] = []
    seen: set[str] = set()
    for root in SRC_DIRS:
        if not root.is_dir():
            continue
        for path in root.rglob("*.swift"):
            rel = str(path.relative_to(REPO))
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            for line in lines:
                if "@covers" not in line:
                    continue
                after = line.split("@covers", 1)[1]
                tokens = re.split(r"[\s,]+", after.strip())
                ids: set[str] = set()
                for token in tokens:
                    ids.update(expand_covers_token(token))
                if ac_id in ids and rel not in seen:
                    seen.add(rel)
                    hits.append({"path": rel, "kind": "implementation"})
    return hits


def files_for_tests(test_names: list[str]) -> list[dict]:
    if not test_names:
        return []
    wanted = set(test_names)
    found: dict[str, str] = {}
    for root in TEST_DIRS:
        if not root.is_dir():
            continue
        for path in root.rglob("*.swift"):
            rel = str(path.relative_to(REPO))
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            for name in list(wanted):
                if re.search(rf"func\s+{re.escape(name)}\s*\(", text):
                    found[name] = rel
                    wanted.discard(name)
            if not wanted:
                break
    return [
        {"name": name, "path": found.get(name)}
        for name in test_names
    ]


def build_threads(records: list[dict], ac_texts: dict[str, str]) -> list[dict]:
    threads = []
    for record in records:
        if record["type"] != "AC":
            continue
        ac_id = record["id"]
        tests = list(record.get("tests") or [])
        pending = list(record.get("pendingTasks") or [])
        done = list(record.get("doneTasks") or [])
        gate_status = record["status"]
        threads.append(
            {
                "id": ac_id,
                "requirement": {
                    "id": ac_id,
                    "text": ac_texts.get(ac_id, ""),
                    "source": "HomesFlow.prd.md",
                    "doneTasks": done,
                    "pendingTasks": pending,
                },
                "implementation": {
                    "covered": bool(record.get("covered")),
                    "modules": files_covering(ac_id),
                },
                "proof": {
                    "tests": files_for_tests(tests),
                },
                "gateStatus": gate_status,
                "status": map_status(gate_status),
            }
        )
    return threads


def apply_demo_break(payload: dict, break_id: str) -> dict:
    """Simulate deleting all proof for one AC using Gate 2's gap rules.

    Recomputes status the same way Gate 2 would after tests vanish:
    - still covered + pending task → tracked-debt (implemented-test-pending)
    - still covered + no pending → GAP
    - not covered + pending → tracked-debt (planned)
    - otherwise → GAP
    """
    out = json.loads(json.dumps(payload))  # deep copy
    out["demo"] = {
        "broken": True,
        "breakId": break_id,
        "note": (
            "Seeded demo break: proof tests for this AC were removed in the "
            "projection only. Regenerated from live Gate 2 data + surgical strip."
        ),
    }
    for thread in out["threads"]:
        if thread["id"] != break_id:
            continue
        thread["proof"]["tests"] = []
        covered = thread["implementation"]["covered"]
        pending = thread["requirement"]["pendingTasks"]
        if covered and pending:
            thread["gateStatus"] = "implemented-test-pending"
            thread["status"] = VIS_TRACKED
        elif covered and not pending:
            thread["gateStatus"] = "gap"
            thread["status"] = VIS_GAP
        elif pending:
            thread["gateStatus"] = "planned"
            thread["status"] = VIS_TRACKED
        else:
            thread["gateStatus"] = "gap"
            thread["status"] = VIS_GAP
        out["totals"]["acsWithTests"] = sum(
            1 for t in out["threads"] if t["proof"]["tests"]
        )
        out["totals"]["acsVerified"] = sum(
            1 for t in out["threads"] if t["status"] == VIS_VERIFIED
        )
        out["totals"]["acsGap"] = sum(
            1 for t in out["threads"] if t["status"] == VIS_GAP
        )
        break
    else:
        raise SystemExit(f"Demo break ID not found in threads: {break_id}")
    return out


def build_payload(break_id: str | None = None) -> dict:
    gate_counts = run_gate2_check()
    records = run_gate2_json()
    ac_texts = load_prd_ac_text()
    threads = build_threads(records, ac_texts)

    verified = sum(1 for t in threads if t["status"] == VIS_VERIFIED)
    gaps = sum(1 for t in threads if t["status"] == VIS_GAP)
    tracked = sum(1 for t in threads if t["status"] == VIS_TRACKED)
    with_tests = sum(1 for t in threads if t["proof"]["tests"])

    # Totals must match Gate 2's own numbers.
    if gate_counts["registryIds"] != len(records):
        raise SystemExit(
            f"Walker/Gate2 registry mismatch: walker={len(records)} "
            f"gate2={gate_counts['registryIds']}"
        )
    if gate_counts["acs"] != len(threads):
        raise SystemExit(
            f"Walker/Gate2 AC mismatch: walker={len(threads)} "
            f"gate2={gate_counts['acs']}"
        )
    if gate_counts["acsWithTests"] != with_tests:
        raise SystemExit(
            f"Walker/Gate2 ACs-with-tests mismatch: walker={with_tests} "
            f"gate2={gate_counts['acsWithTests']}"
        )

    sha = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip() or "unknown"

    payload = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": sha,
        "source": {
            "gate2": "scripts/check-traceability.sh",
            "prd": "HomesFlow.prd.md",
            "principle": "Projection only — not a second registry",
        },
        "totals": {
            "registryIds": gate_counts["registryIds"],
            "acs": gate_counts["acs"],
            "acsWithTests": gate_counts["acsWithTests"],
            "idsWithCovers": gate_counts["idsWithCovers"],
            "acsVerified": verified,
            "acsTrackedDebt": tracked,
            "acsGap": gaps,
            "gate2Passed": gate_counts["gate2Passed"],
        },
        "defaultDescentId": "AC-USER-04",
        "demoBreakId": "AC-USER-04",
        "threads": threads,
        "demo": {"broken": False, "breakId": None, "note": None},
    }

    if break_id:
        payload = apply_demo_break(payload, break_id)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit Gate 2 thread JSON for the visualizer")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write JSON to this path (default: stdout)",
    )
    parser.add_argument(
        "--demo-break",
        metavar="AC-ID",
        help="Seed a demo GAP by stripping proof for this AC in the projection",
    )
    args = parser.parse_args()
    payload = build_payload(break_id=args.demo_break)
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(
            f"Wrote {args.output} "
            f"({payload['totals']['acsWithTests']}/{payload['totals']['acs']} ACs with tests; "
            f"Gate 2 {'PASSED' if payload['totals']['gate2Passed'] else 'FAILED'})",
            file=sys.stderr,
        )
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
