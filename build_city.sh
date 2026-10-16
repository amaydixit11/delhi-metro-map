#!/usr/bin/env bash
# usage: LOOM=<loom build dir> PYPOP=<python with rasterio> POPTIF=<worldpop tif> ./build_city.sh <code> "<City name>" <s,w,n,e> <fisheye lat,lon> <pop w,s,e,n>
set -euo pipefail; cd "$(dirname "$0")"
c=$1; name=$2; bbox=$3; fish=$4; popb=$5; export CITY=$c
[ -f cities/$c/routes.json ] || curl -s -m 190 -A delhi-metro-map/1.0 -o cities/$c/routes.json --data-urlencode \
  "data=[out:json][timeout:170];rel[\"route\"~\"subway|light_rail|monorail\"]($bbox)->.r;.r out body;node(r.r);out body;way(r.r);out geom;" https://overpass-api.de/api/interpreter
python3 -I scripts/research_to_city.py cities/$c/research.json "$name" "$bbox" | tail -1
python3 -I scripts/build_ops.py cities/$c/routes.json cities/$c/ops.json >/dev/null
python3 -I scripts/build_data.py cities/$c/ops.json cities/$c/metro-data.js | tail -2
[ -s cities/$c/pop.js ] || POP_BBOX=$popb "$PYPOP" -I scripts/population.py "$POPTIF" cities/$c/pop.js > /tmp/$c-pop.log 2>&1 &
best=""; bestn=999
for v in "8 70%" "10 70%" "8 60%" "6 70%"; do set -- $v
  FISH_C=$fish python3 -I scripts/build_graph.py cities/$c/metro-data.js /tmp/$c-g.json "" $1 0.7 >/dev/null
  "$LOOM/loom" < /tmp/$c-g.json 2>/dev/null | "$LOOM/octi" -g $2 2>/dev/null | "$LOOM/loom" 2>/dev/null > /tmp/$c-o.json || continue
  for G in 44 52; do n=$(python3 -I scripts/render_schematic.py /tmp/$c-o.json cities/$c/metro-data.js /tmp/$c-s.svg $G | head -1 | sed 's/overlaps=\([0-9]*\).*/\1/')
    if [ "$n" -lt "$bestn" ]; then bestn=$n; best="$1 $2 $G"; cp /tmp/$c-o.json cities/$c/layout.json; fi; done
  [ "$bestn" = 0 ] && break; done
echo "layout $best overlaps=$bestn"
python3 -I scripts/render_schematic.py cities/$c/layout.json cities/$c/metro-data.js cities/$c/schem.svg ${best##* } >/dev/null
wait; python3 -I scripts/assemble.py
