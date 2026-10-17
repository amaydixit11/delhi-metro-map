#!/usr/bin/env bash
# Deploy dist/ to Vercel (india-metro-map.vercel.app) with GoatCounter analytics; no name in the URL.
# GC = GoatCounter site code. Rename the code in GoatCounter settings to keep your username out of page source.
set -euo pipefail; cd "$(dirname "$0")"
GC=${GC:-indiametro}
D=$(mktemp -d)/india-metro-map; mkdir -p "$D"; cp -R dist/. "$D/"; rm -f "$D/planned-stations.csv"
mkdir -p "$D/.vercel"; cp .vercel-project.json "$D/.vercel/project.json"
for f in "$D"/index.html "$D"/*/index.html; do
  sed -i '' "s|</head>|<script data-goatcounter=\"https://$GC.goatcounter.com/count\" async src=\"//gc.zgo.at/count.js\"></script>\n</head>|" "$f"; done
(cd "$D" && vercel deploy --prod --yes) | grep -E '"url"' | head -1
