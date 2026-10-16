"""Write cities/<c>/config.py + page.json. usage: make_page.py <c> "<City>" "<agency>" lat w,s,e,n '<json osm_lines>' '<json rename>'"""
import json, sys, os
c, city, agency, lat, fit, osm, ren = sys.argv[1:8]
w, s, e, n = map(float, fit.split(","))
open(f"cities/{c}/config.py", "w").write(f'''import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from city_config import make
globals().update(make(os.path.dirname(os.path.abspath(__file__)), {osm}, {ren}))
''')
r = json.load(open(f"cities/{c}/research.json"))
notes = "".join(f'<div class="note">{x}</div>' for x in r.get("notes", [])[:8])
cfg = dict(title=f"{city} Metro future map", h1=f"{city} Metro · open, building and planned",
  sub=f"Every open, under-construction, approved and proposed metro line in {city}. Data as of Oct 2026.",
  agency=agency, region=city, fit=[[s, w], [n, e]], lat=float(lat),
  phases={"op": {"n": "Operational", "d": None, "w": 4.5}, "OP": {"n": "Open (recent)", "d": None, "w": 4.5},
          "UC": {"n": "Under construction", "d": "11 7", "w": 4}, "AP": {"n": "Approved", "d": "1 8", "w": 4.5},
          "PR": {"n": "Proposed", "d": "10 6 1 6", "w": 3.5}},
  order=["op", "OP", "UC", "AP", "PR"], short={"OP": "open", "UC": "building", "AP": "approved", "PR": "proposed"},
  label={"op": "Open", "OP": "Open", "UC": "Under construction", "AP": "Approved", "PR": "Proposed"},
  thin=[], rail=[], speeds={},
  notes=f'<div class="note"><b>Sources:</b> Wikipedia station tables checked against 2025–26 news; open lines traced from OpenStreetMap. Corridors without published stations are drawn between their named endpoints. Years without an official target are estimates by stage.</div>' + notes)
json.dump(cfg, open(f"cities/{c}/page.json", "w"), ensure_ascii=False, indent=1)
