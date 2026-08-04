#!/usr/bin/env bash
# Regenerate Thread Visualizer JSON from live Gate 2 data (projection only).
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=docs/thread-visualizer/data
mkdir -p "$OUT"

python3 scripts/thread-walker.py -o "$OUT/thread.json"
python3 scripts/thread-walker.py --demo-break AC-USER-04 -o "$OUT/thread-broken.json"

echo "Thread visualizer data refreshed under $OUT/"
echo "Open docs/thread-visualizer/index.html in a browser."
