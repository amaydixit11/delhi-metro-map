#!/usr/bin/env bash
# Rebuild the map. Steps 1-2 are enough after editing scripts/planned.py or scripts/years.py
# unless the network shape changed; then also re-run the schematic layout (step 3, needs LOOM).
set -euo pipefail
cd "$(dirname "$0")"
python3 -I scripts/build_ops.py data/routes3.json data/ops.json            # OSM routes -> operational lines
python3 -I scripts/build_data.py data/ops.json data/metro-data.js          # + planned lines, years, interchanges
if [[ "${LAYOUT:-0}" == "1" ]]; then                                      # 3. schematic layout (LOOM octi)
  : "${LOOM:?set LOOM to the LOOM build dir, e.g. ~/src/loom/build}"
  python3 -I scripts/build_graph.py data/metro-data.js /tmp/dm-graph.json "" 10 0.7
  "$LOOM/loom" < /tmp/dm-graph.json | "$LOOM/octi" -g 60% | "$LOOM/loom" > schematic/layout.json
fi
python3 -I scripts/render_schematic.py schematic/layout.json data/metro-data.js schematic/schem.svg 60
# population grid (only when updating it): python scripts/population.py <worldpop.tif> data/pop.js
python3 -I scripts/assemble.py                                             # -> dist/index.html
echo "built dist/index.html"

python3 -I scripts/merge_cities.py   # all cities on one map -> dist/india/
