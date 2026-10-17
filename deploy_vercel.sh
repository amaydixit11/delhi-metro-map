#!/usr/bin/env bash
# Deploy dist/ to Vercel (india-metro-map.vercel.app) with Vercel Web Analytics; no name in the URL.
set -euo pipefail; cd "$(dirname "$0")"
D=$(mktemp -d)/india-metro-map; mkdir -p "$D"; cp -R dist/. "$D/"; rm -f "$D/planned-stations.csv"
mkdir -p "$D/.vercel"; cp .vercel-project.json "$D/.vercel/project.json"
for f in "$D"/index.html "$D"/*/index.html; do sed -i '' 's|</head>|<script defer src="/_vercel/insights/script.js"></script>\n</head>|' "$f"; done
(cd "$D" && vercel deploy --prod --yes)
