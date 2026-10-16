# Delhi NCR Metro map: up to Phase V(C)

Interactive map of the Delhi Metro and the wider NCR rail network: every open, under-construction, approved and proposed line through Phase V(C), plus the Gurugram, Noida and Meerut metros and the Namo Bharat (RRTS) corridors.

**Live map: https://amaydixit11.github.io/delhi-metro-map/** (or open `dist/index.html` locally).

- **Geographic view:** open lines traced from OpenStreetMap, planned lines from their station lists
- **Schematic view:** octilinear layout made with [LOOM](https://github.com/ad-freiburg/loom), with curved or sharp corners
- **Timeline:** drag 2002 → 2041 to watch the network grow (official targets where published, estimates otherwise)
- **Route planner:** fastest route on whatever network is visible for the chosen year
- Station cards show sources, phase and year; stations whose names aren't published yet are marked *projected*

`images/` has the Reddit images and `dist/planned-stations.csv` lists every planned station with its source status and year.

## Data notes
- Most Phase V(B), V(C) and NCR corridors have no published station list. Their stops are placed by locality and match the official station counts. They are marked projected.
- Years after 2026 are official targets where published; the rest are estimates by project stage (reason given in each station card).
- Not an official map.

## Rebuilding
```
./build.sh                       # after editing scripts/planned.py or scripts/years.py
LAYOUT=1 LOOM=~/src/loom/build ./build.sh   # also redo the schematic layout
```
`scripts/planned.py` holds every planned line, `scripts/years.py` the opening years and estimates.
