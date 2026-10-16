import json, math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
CITY = os.environ.get("CITY", "delhi")
if CITY == "delhi":
    from planned import LINES, SEGMENTS, SOURCES, PENDING_EXISTING
else:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cities", CITY))
    from config import LINES, SEGMENTS, SOURCES
    import config as _cfg
    PENDING_EXISTING = getattr(_cfg, "PENDING_EXISTING", {})

ops = json.load(open(sys.argv[1]))
OPS_PHASE = "op"

def dist(a, b):
    dy = (a[0] - b[0]) * 111.2
    dx = (a[1] - b[1]) * 111.2 * math.cos(math.radians(28.6))
    return math.hypot(dx, dy)

# station registry: id -> {name, lat, lon, conf, served: {line: phase}}
stations, by_name = [], {}

def add_station(name, lat, lon, conf, line, phase):
    # merge with an existing point of the same name nearby, or any station within 120 m
    for s in by_name.get(name, []):
        if dist((s["lat"], s["lon"]), (lat, lon)) < 0.6:
            s["served"].setdefault(line, phase); return s
    s = dict(id=len(stations), name=name, lat=lat, lon=lon, conf=conf, served={line: phase})
    stations.append(s); by_name.setdefault(name, []).append(s); return s

def find(name):
    c = by_name.get(name)
    if not c: raise SystemExit("unresolved ref: " + name)
    return c[0]

# operational lines
segs = []
for line, seqs in ops["stops"].items():
    for seq in seqs:
        ids = []
        for nm, la, lo in seq:
            ph = PENDING_EXISTING.get(nm, OPS_PHASE)
            s = add_station(nm, la, lo, "o", line, ph)
            if ph != OPS_PHASE: s["served"][line] = ph
            if not ids or ids[-1] != s["id"]: ids.append(s["id"])
        segs.append(dict(line=line, phase=OPS_PHASE, ids=ids, track=True))

# planned
for sg in SEGMENTS:
    ids = []
    for e in sg["st"]:
        if e[0].startswith("@"):
            s = find(e[0][1:])
            if len(e) > 1 and e[1] == "o": s["conf"] = "o"
            if sg.get("infill"):
                pass
            else:
                s["served"].setdefault(sg["line"], sg["phase"])
        else:
            nm, la, lo, cf = e
            s = add_station(nm, la, lo, cf, sg["line"], sg["phase"])
        ids.append(s["id"])
    if sg.get("infill"): continue
    segs.append(dict(line=sg["line"], phase=sg["phase"], ids=ids, title=sg["title"], status=sg["status"],
                     km=sg.get("km"), n=sg.get("n"), src=sg["src"]))

# interchange clustering: distinct stations of different lines within 250 m become one complex
comp = list(range(len(stations)))
def root(i):
    while comp[i] != i: comp[i] = comp[comp[i]]; i = comp[i]
    return i
for i, a in enumerate(stations):
    for j in range(i + 1, len(stations)):
        b = stations[j]
        if set(a["served"]) != set(b["served"]) and dist((a["lat"], a["lon"]), (b["lat"], b["lon"])) < 0.25:
            comp[root(j)] = root(i)
for s in stations: s["cx"] = root(s["id"])

from years import compute as compute_years
edge_years, track_years, missing = compute_years(stations, segs, ops["tracks"])
if missing: print("WARN edges without opening date:", missing[:10])
json.dump({f"{a}|{b}|{ln}": y for (a, b, ln), y in edge_years.items()}, open(os.path.join(os.path.dirname(sys.argv[2]), "edge_years.json"), "w"))
out = dict(lines={k: dict(name=v[0], color=v[1]) for k, v in LINES.items()},
           stations=[[s["name"], round(s["lat"], 5), round(s["lon"], 5), s["conf"], s["served"], s["cx"], s["y"], s["ly"]] for s in stations],
           trackYears=track_years,
           segments=segs, tracks=ops["tracks"], sources={k: dict(t=v[0], u=v[1]) for k, v in SOURCES.items()})
open(sys.argv[2], "w").write("window.METRO=" + json.dumps(out, separators=(",", ":"), ensure_ascii=False) + ";")

# report
from collections import Counter
for ph in ["IV", "VA", "VB", "VC"]:
    new = [s for s in stations if all(v == ph for v in s["served"].values()) or (list(s["served"].values()).count(ph) and min(s["served"].values()) == ph and "op" not in s["served"].values())]
    print(ph, "segments:", sum(1 for g in segs if g["phase"] == ph))
for g in segs:
    if g["phase"] in ("VB", "VC") and g.get("n"):
        newc = sum(1 for i in g["ids"][1:] if stations[i]["served"].get(g["line"]) == g["phase"]) if g["line"] not in ("cs","jm","sm","kr","mk","tn") else len(g["ids"])
        print(f'{g["phase"]} {g["title"]}: listed {len(g["ids"])} new~{newc} official n={g["n"]}')
print("stations", len(stations), "projected", sum(1 for s in stations if s["conf"] == "p"))
print("size", os.path.getsize(sys.argv[2]))
