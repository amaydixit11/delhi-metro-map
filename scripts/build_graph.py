import json, sys
d = json.loads(open(sys.argv[1]).read()[len("window.METRO="):-1])
S, L = d["stations"], d["lines"]
SKIP = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] else set()
# one node per interchange complex
cx = {}
for i, s in enumerate(S):
    cx.setdefault(s[5], []).append(i)
node_of = {i: s[5] for i, s in enumerate(S)}
import math
C0 = (28.6328, 77.2197)  # Rajiv Chowk
FC = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0  # fisheye km constant
TAIL = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5  # scale of the regional tails beyond RC
def fish(lat, lon):
    y = (lat - C0[0]) * 111.2; x = (lon - C0[1]) * 111.2 * math.cos(math.radians(C0[0]))
    r = math.hypot(x, y)
    if r < 1e-9: return [C0[1], C0[0]]
    RC = 35.0  # beyond RC km the scale stays linear so long regional corridors keep even spacing
    if r <= RC: r2 = FC * math.log(1 + r / FC)
    else: r2 = FC * math.log(1 + RC / FC) + (r - RC) * FC / (FC + RC) * TAIL
    k = r2 / r
    return [C0[1] + x * k / (111.2 * math.cos(math.radians(C0[0]))), C0[0] + y * k / 111.2]
def pos(c):
    m = cx[c]; lat = sum(S[i][1] for i in m) / len(m); lon = sum(S[i][2] for i in m) / len(m)
    return fish(lat, lon)
def label(c):
    names = [S[i][0] for i in cx[c]]
    return min(names, key=len) if len(set(names)) > 1 else names[0]
edges = {}
used = set()
for g in d["segments"]:
    if g["line"] in SKIP: continue
    lid = f'{g["line"]}_{g["phase"]}'
    ids = [node_of[i] for i in g["ids"]]
    for a, b in zip(ids, ids[1:]):
        if a == b: continue
        k = (min(a, b), max(a, b))
        e = edges.setdefault(k, {})
        e[lid] = {"id": lid, "color": L[g["line"]]["color"].lstrip("#"), "label": L[g["line"]]["name"]}
        used.update(k)
feats = []
for c in used:
    feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": pos(c)},
                  "properties": {"id": f"n{c}", "station_id": f"s{c}", "station_label": label(c)}})
for (a, b), ls in edges.items():
    feats.append({"type": "Feature", "geometry": {"type": "LineString", "coordinates": [pos(a), pos(b)]},
                  "properties": {"from": f"n{a}", "to": f"n{b}", "id": f"e{a}_{b}", "lines": list(ls.values())}})
json.dump({"type": "FeatureCollection", "features": feats}, open(sys.argv[2], "w"))
print(len(used), "nodes", len(edges), "edges")
