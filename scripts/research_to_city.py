"""Turn a city research JSON (lines → segments → ordered stations) into cities/<code>/config.py inputs.

usage: CITY=blr python3 scripts/research_to_city.py research.json "Bengaluru" 12.7,77.3,13.3,77.9
Writes cities/<code>/plan.json (lines, segments with coordinates, sources, open dates) and pick list for OSM routes.
Station coordinates: OSM station nodes first (open / construction / proposed), then Nominatim, then interpolation.
"""
import json, os, re, sys, time, urllib.parse, urllib.request, difflib

city = os.environ["CITY"]
R = json.load(open(sys.argv[1]))
CITY_NAME = sys.argv[2]
S_, W_, N_, E_ = map(float, sys.argv[3].split(","))
D = f"cities/{city}"
os.makedirs(D, exist_ok=True)
UA = {"User-Agent": "delhi-metro-map/1.0"}

def norm(n):
    n = n.lower().replace("&", "and")
    n = re.sub(r"\b(metro|station|stn|road|rd|cross|junction|jn)\b\.?", " ", n)
    return re.sub(r"[^a-z0-9]+", "", n)

# ---- OSM stations (cached) ----
osm_f = f"{D}/osm_stations.json"
if not os.path.exists(osm_f):
    q = (f'[out:json][timeout:120];(node["railway"~"station|construction|proposed|stop"]["station"~"subway|light_rail|monorail"]({S_},{W_},{N_},{E_});'
         f'node["construction:railway"="station"]({S_},{W_},{N_},{E_});node["railway"="station"]["subway"="yes"]({S_},{W_},{N_},{E_});'
         f'node["public_transport"="station"]["subway"="yes"]({S_},{W_},{N_},{E_}););out body;')
    req = urllib.request.Request("https://overpass-api.de/api/interpreter", data=urllib.parse.urlencode({"data": q}).encode(), headers=UA)
    for attempt in range(5):
        try: json.dump(json.load(urllib.request.urlopen(req, timeout=150)), open(osm_f, "w")); break
        except Exception as ex: print("overpass retry", attempt, ex); time.sleep(20 * (attempt + 1))
osm = {}
for e in json.load(open(osm_f))["elements"]:
    t = e.get("tags", {})
    for k in ("name", "name:en", "alt_name", "old_name"):
        if t.get(k): osm.setdefault(norm(t[k]), (e["lat"], e["lon"], t.get("name")))
ALIAS = json.load(open(f"{D}/alias.json")) if os.path.exists(f"{D}/alias.json") else {}
geo_f = f"{D}/geocode_cache.json"
geo = json.load(open(geo_f)) if os.path.exists(geo_f) else {}

def nominatim(q):
    if q in geo: return geo[q]
    u = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q, "format": "json", "limit": 1, "viewbox": f"{W_},{N_},{E_},{S_}", "bounded": 1})
    try: r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
    except Exception: r = []
    time.sleep(1.1)
    geo[q] = [float(r[0]["lat"]), float(r[0]["lon"])] if r else None
    json.dump(geo, open(geo_f, "w"))
    return geo[q]

def locate(name):
    name = ALIAS.get(re.sub(r"\s*[\(\[].*?[\)\]]", "", name).strip(), name)
    name = re.sub(r"\s*[\(\[].*?[\)\]]", "", name).split(" / ")[0].strip()
    k = norm(name)
    if k in osm: return osm[k][:2], "osm"
    m = difflib.get_close_matches(k, list(osm), n=1, cutoff=0.88)
    if m: return osm[m[0]][:2], "osm~"
    for q in (f"{name} metro station, {CITY_NAME}", f"{name}, {CITY_NAME}"):
        g = nominatim(q)
        if g: return g, "nom"
    return None, None

# ---- lines and segments ----
PAL = ["#E21F26", "#1F63B6", "#1E9E48", "#6A2C91", "#F28C28", "#EE82B4", "#B5267B", "#C49A3A", "#0E9AA7", "#8B5A2B",
       "#7CB518", "#22408F", "#8E1B3C", "#5B5BD6", "#00ACC1", "#A1887F", "#D84315", "#9575CD"]
DROPPED = []
lines, segs, srcs, stats = {}, [], {}, {"osm": 0, "osm~": 0, "nom": 0, "interp": 0}
STATUS = {"operational": "OP", "under_construction": "UC", "approved": "AP", "proposed": "PR"}
for li, L in enumerate(R["lines"]):
    key = re.sub(r"[^a-z0-9]", "", L["line"].lower())[:12] or f"l{li}"
    if key in lines: key = f"{key[:9]}{li}"
    col = L.get("color") or PAL[li % len(PAL)]
    if not re.match(r"^#[0-9a-fA-F]{6}$", str(col)): col = PAL[li % len(PAL)]
    lines[key] = (L["line"], col)
    for sg in L["segments"]:
        st = [s for s in sg.get("stations", []) if s]
        if len(st) < 3: DROPPED.append((L["line"], sg["from"], sg["to"], "no station list")); continue
        if len(st) < 2: continue
        pts = []
        for nm in st:
            c, how = locate(nm)
            if how: stats[how] += 1
            pts.append([nm, c])
        # drop outliers: a station whose detour from its neighbours is far longer than the direct hop
        import math
        def dk(p, q): return math.hypot((p[0] - q[0]) * 111, (p[1] - q[1]) * 111 * math.cos(math.radians(p[0])))
        for _ in range(4):
            loc = [i for i, (_, c) in enumerate(pts) if c]
            worst, wi = 0, None
            for k in range(len(loc)):
                i = loc[k]; a = loc[k - 1] if k > 0 else None; b = loc[k + 1] if k + 1 < len(loc) else None
                if a is not None and b is not None:
                    det = dk(pts[a][1], pts[i][1]) + dk(pts[i][1], pts[b][1]) - dk(pts[a][1], pts[b][1])
                    gap = (b - a) * 2.5
                    if det > max(4, gap) and det > worst: worst, wi = det, i
                elif len(loc) > 3:   # endpoint: compare with the next hop's typical spacing
                    nb = loc[k + 1] if a is None else loc[k - 1]; nb2 = loc[k + 2] if a is None else loc[k - 2]
                    hop = dk(pts[i][1], pts[nb][1]); ref = dk(pts[nb][1], pts[nb2][1]) / max(1, abs(nb2 - nb))
                    if hop > max(6, ref * abs(nb - i) * 4) and hop > worst: worst, wi = hop, i
            if wi is None: break
            pts[wi][1] = None; stats["dropped"] = stats.get("dropped", 0) + 1
        if sum(1 for _, c in pts if c) < max(3, 0.6 * len(pts)):
            DROPPED.append((L["line"], sg["from"], sg["to"], "too few stations locatable")); continue
        # interpolate gaps between located neighbours
        idx = [i for i, (_, c) in enumerate(pts) if c]
        if len(idx) < 2: print("SKIP (unlocatable)", L["line"], sg["from"], sg["to"]); continue
        for i, (nm, c) in enumerate(pts):
            if c: continue
            a = max([j for j in idx if j < i], default=None); b = min([j for j in idx if j > i], default=None)
            if a is None: a, b = idx[0], idx[1]
            if b is None: a, b = idx[-2], idx[-1]
            f = (i - a) / (b - a)
            pts[i][1] = [pts[a][1][0] + (pts[b][1][0] - pts[a][1][0]) * f, pts[a][1][1] + (pts[b][1][1] - pts[a][1][1]) * f]
            stats["interp"] += 1
        hops = sorted(dk(a[1], b[1]) for a, b in zip(pts, pts[1:]))
        med = hops[len(hops) // 2]
        if hops[-1] > max(6, 4 * med):
            DROPPED.append((L["line"], sg["from"], sg["to"], f"implausible {hops[-1]:.0f} km gap")); continue
        sid = f"s{len(srcs)}"; srcs[sid] = (f"{L['line']}: {sg['from']} – {sg['to']}", (sg.get("sources") or [""])[0])
        segs.append(dict(line=key, status=sg["status"], phase=STATUS.get(sg["status"], "PR"), year=sg.get("year"),
                         stage=sg.get("stage") or "", km=sg.get("km"), n=sg.get("n_stations"), title=f"{sg['from']} → {sg['to']}",
                         src=sid, st=[[re.sub(r"\s*\[.*?\]", "", nm).strip(), round(c[0], 5), round(c[1], 5)] for nm, c in pts]))
json.dump(dict(lines=lines, segs=segs, sources=srcs, notes=R.get("notes", [])), open(f"{D}/plan.json", "w"), indent=0, ensure_ascii=False)
for d in DROPPED: print("DROP", *d)
print("lines", len(lines), "segments", len(segs), "located:", stats)
