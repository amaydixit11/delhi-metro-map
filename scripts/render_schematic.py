"""Render LOOM/octi octilinear output into a styled SVG (schematic view).

usage: render_schematic.py octi.json metro-data.js out.svg
"""
import json, math, sys, html
from collections import defaultdict

octi = json.load(open(sys.argv[1]))["features"]
M = json.loads(open(sys.argv[2]).read()[len("window.METRO="):-1])
S, LINES = M["stations"], M["lines"]
import os
EY = json.load(open(os.path.join(os.path.dirname(sys.argv[2]), "edge_years.json")))

cx_members = defaultdict(list)
for i, s in enumerate(S):
    cx_members[s[5]].append(i)

def merc(lon, lat):
    return lon, -math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))

pts = [f for f in octi if f["geometry"]["type"] == "Point" and "station_id" in f["properties"]]
edges = [f for f in octi if f["geometry"]["type"] == "LineString"]

# scale: median nearest-neighbour distance between stations -> GRID px
P = [merc(*f["geometry"]["coordinates"]) for f in pts]
nn = []
for i, a in enumerate(P):
    best = min((math.hypot(a[0] - b[0], a[1] - b[1]) for j, b in enumerate(P) if j != i), default=1)
    nn.append(best)
nn.sort(); GRID = float(sys.argv[4]) if len(sys.argv) > 4 else 40.0
k = GRID / nn[len(nn) // 2]
allc = [merc(*c) for e in edges for c in e["geometry"]["coordinates"]] + P
x0 = min(p[0] for p in allc); y0 = min(p[1] for p in allc)
x1 = max(p[0] for p in allc); y1 = max(p[1] for p in allc)
PAD = 140
def T(c):
    x, y = merc(*c); return ((x - x0) * k + PAD, (y - y0) * k + PAD)
W = (x1 - x0) * k + 2 * PAD; H = (y1 - y0) * k + 2 * PAD

LW, GAP = 7.0, 1.8
STEP = LW + GAP

def offset_poly(pp, off):
    if abs(off) < 1e-9: return pp
    out = []
    n = len(pp)
    for i in range(n):
        if i == 0: dx, dy = pp[1][0] - pp[0][0], pp[1][1] - pp[0][1]; nx, ny = -dy, dx
        elif i == n - 1: dx, dy = pp[-1][0] - pp[-2][0], pp[-1][1] - pp[-2][1]; nx, ny = -dy, dx
        else:
            ax, ay = pp[i][0] - pp[i - 1][0], pp[i][1] - pp[i - 1][1]
            bx, by = pp[i + 1][0] - pp[i][0], pp[i + 1][1] - pp[i][1]
            la, lb = math.hypot(ax, ay) or 1, math.hypot(bx, by) or 1
            n1 = (-ay / la, ax / la); n2 = (-by / lb, bx / lb)
            mx, my = n1[0] + n2[0], n1[1] + n2[1]; ml = math.hypot(mx, my) or 1
            mx, my = mx / ml, my / ml
            cosv = mx * n1[0] + my * n1[1]
            sc = off / max(cosv, 0.35)
            out.append((pp[i][0] + mx * sc, pp[i][1] + my * sc)); continue
        l = math.hypot(nx, ny) or 1
        out.append((pp[i][0] + nx / l * off, pp[i][1] + ny / l * off))
    return out

# station positions by complex
st_pos = {}
for f in pts:
    c = int(f["properties"]["station_id"][1:])
    st_pos[c] = T(f["geometry"]["coordinates"])

line_svgs = []
segments_for_collision = []
spread_at = defaultdict(float)  # station complex -> max half-width of line bundle
CURVE_R = GRID * 1.6
ST_PTS = list(st_pos.values())

def station_caps(pp):
    """for each segment i (pp[i]->pp[i+1]): distance from each end to the nearest station on it"""
    caps = []
    for a, b in zip(pp, pp[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        da, db = L, L
        for s in ST_PTS:
            tproj = (s[0] - a[0]) * ux + (s[1] - a[1]) * uy
            if -0.5 <= tproj <= L + 0.5 and abs((s[0] - a[0]) * uy - (s[1] - a[1]) * ux) < 1.5:
                da = min(da, max(0.0, tproj)); db = min(db, max(0.0, L - tproj))
        caps.append((L, da, db))
    return caps

def curved_d(q, pp, caps, off):
    """round interior vertices of offset polyline q (centerline pp) with concentric arcs"""
    out = [f"M{q[0][0]:.1f},{q[0][1]:.1f}"]
    for i in range(1, len(q) - 1):
        a, v, b = pp[i - 1], pp[i], pp[i + 1]
        d1 = (v[0] - a[0], v[1] - a[1]); d2 = (b[0] - v[0], b[1] - v[1])
        l1, l2 = math.hypot(*d1) or 1e-9, math.hypot(*d2) or 1e-9
        cosang = max(-1, min(1, (d1[0] * d2[0] + d1[1] * d2[1]) / (l1 * l2)))
        theta = math.acos(cosang)
        cross = d1[0] * d2[1] - d1[1] * d2[0]
        if theta < 1e-3:
            out.append(f"L{q[i][0]:.1f},{q[i][1]:.1f}"); continue
        tan2 = math.tan(theta / 2)
        # usable straight length on each side: half the segment, and never past a station
        tmax = min(caps[i - 1][0] / 2, caps[i][0] / 2, caps[i - 1][2] - 2, caps[i][1] - 2)
        R = min(CURVE_R, max(0.0, tmax) / tan2)
        r = R - off * (1 if cross > 0 else -1)
        if R < 2 or r < 1:
            out.append(f"L{q[i][0]:.1f},{q[i][1]:.1f}"); continue
        tt = r * tan2
        qa, qv, qb = q[i - 1], q[i], q[i + 1]
        e1 = (qa[0] - qv[0], qa[1] - qv[1]); e2 = (qb[0] - qv[0], qb[1] - qv[1])
        m1, m2 = math.hypot(*e1) or 1e-9, math.hypot(*e2) or 1e-9
        p1 = (qv[0] + e1[0] / m1 * tt, qv[1] + e1[1] / m1 * tt)
        p2 = (qv[0] + e2[0] / m2 * tt, qv[1] + e2[1] / m2 * tt)
        sweep = 1 if cross > 0 else 0
        out.append(f"L{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 0 {sweep} {p2[0]:.1f},{p2[1]:.1f}")
    out.append(f"L{q[-1][0]:.1f},{q[-1][1]:.1f}")
    return " ".join(out)

segrec = defaultdict(list)
def nkey(p): return (round(p[0], 1), round(p[1], 1))
for e in edges:
    pp = [T(c) for c in e["geometry"]["coordinates"]]
    pp = [p for i, p in enumerate(pp) if i == 0 or math.hypot(p[0] - pp[i - 1][0], p[1] - pp[i - 1][1]) > 0.01]
    if len(pp) < 2: continue
    ls = e["properties"]["lines"]; n = len(ls)
    caps = station_caps(pp)
    for a, b in zip(pp, pp[1:]): segments_for_collision.append((a, b, n * STEP / 2))
    for j, l in enumerate(ls):
        line, phase = l["id"].rsplit("_", 1)
        off = (j - (n - 1) / 2) * STEP
        q = offset_poly(pp, off)
        segrec[l["id"]].append(dict(a=nkey(pp[0]), b=nkey(pp[-1]), q=q, pp=pp, off=off))
    for c, (sx, sy) in st_pos.items():
        for p in (pp[0], pp[-1]):
            if math.hypot(p[0] - sx, p[1] - sy) < 0.5: spread_at[c] = max(spread_at[c], n * STEP / 2)

# ---------- join each line's edges into continuous chains, then round the bends ----------
st_key = {nkey(v): c for c, v in st_pos.items()}
shift = {}
def seg_year(s, line):
    ca, cb = st_key.get(s["a"]), st_key.get(s["b"])
    if ca is None or cb is None: return None
    return EY.get(f"{min(ca, cb)}|{max(ca, cb)}|{line}")

def chains_for(segs):
    adj = defaultdict(list)
    for i, s in enumerate(segs): adj[s["a"]].append(i); adj[s["b"]].append(i)
    used, out = set(), []
    def walk(node, i):
        ch = []
        while i is not None and i not in used:
            used.add(i); s = segs[i]; rev = s["b"] == node and s["a"] != node
            ch.append((s, rev)); node = s["a"] if rev else s["b"]
            nxt = [j for j in adj[node] if j not in used and (segs[j]["y"] is None or s["y"] is None or segs[j]["y"] == s["y"])]
            i = nxt[0] if len(adj[node]) == 2 and nxt else None
        return ch
    for node, lst in adj.items():
        if len(lst) != 2:
            for i in lst:
                if i not in used: out.append(walk(node, i))
    for i in range(len(segs)):
        if i not in used: out.append(walk(segs[i]["a"], i))
    return out

def dp_keep(pts, tol, keep_pts):
    """Douglas-Peucker on pts; returns kept indices; never drops points in keep_pts (stations)"""
    keep = {0, len(pts) - 1} | {i for i, p in enumerate(pts) if nkey(p) in keep_pts}
    stack = [(0, len(pts) - 1)]
    anchors = sorted(keep)
    stack = list(zip(anchors, anchors[1:]))
    while stack:
        a, b = stack.pop()
        if b - a < 2: continue
        ax, ay = pts[a]; bx, by = pts[b]; L = math.hypot(bx - ax, by - ay) or 1e-9
        best, bi = -1, None
        for i in range(a + 1, b):
            d = abs((pts[i][0] - ax) * (by - ay) - (pts[i][1] - ay) * (bx - ax)) / L
            if d > best: best, bi = d, i
        if best > tol:
            keep.add(bi); stack += [(a, bi), (bi, b)]
    return sorted(keep)

def mpath(pts): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

for lid, segs in segrec.items():
    line, phase = lid.rsplit("_", 1)
    for s in segs: s["y"] = seg_year(s, line)
    for ch in chains_for(segs):
        ys = [s["y"] for s, _ in ch if s["y"] is not None]
        chy = min(ys) if ys else 9999
        P, O, C = [], [], []
        for s, rev in ch:
            q, pp, o = (s["q"][::-1], s["pp"][::-1], -s["off"]) if rev else (s["q"], s["pp"], s["off"])
            if P:
                P[-1] = ((P[-1][0] + q[0][0]) / 2, (P[-1][1] + q[0][1]) / 2); O[-1] = (O[-1] + o) / 2
                P += q[1:]; O += [o] * (len(q) - 1); C += pp[1:]
            else:
                P, O, C = list(q), [o] * len(q), list(pp)
        idx = dp_keep(C, 2.0, st_key.keys())
        P = [P[i] for i in idx]; O = [O[i] for i in idx]; C = [C[i] for i in idx]
        sharp = mpath(P)
        out = [f"M{P[0][0]:.1f},{P[0][1]:.1f}"]
        for i in range(1, len(P) - 1):
            a, v, b = C[i - 1], C[i], C[i + 1]
            d1 = (v[0] - a[0], v[1] - a[1]); d2 = (b[0] - v[0], b[1] - v[1])
            l1, l2 = math.hypot(*d1), math.hypot(*d2)
            if l1 < 0.5 or l2 < 0.5: out.append(f"L{P[i][0]:.1f},{P[i][1]:.1f}"); continue
            theta = math.acos(max(-1, min(1, (d1[0] * d2[0] + d1[1] * d2[1]) / (l1 * l2))))
            if theta < math.radians(12): out.append(f"L{P[i][0]:.1f},{P[i][1]:.1f}"); continue
            cross = d1[0] * d2[1] - d1[1] * d2[0]; sg = 1 if cross > 0 else -1
            tan2 = math.tan(theta / 2)
            R = min(CURVE_R, min(l1, l2) * 0.5 / tan2)
            r = R - O[i] * sg
            qa, qv, qb = P[i - 1], P[i], P[i + 1]
            e1 = (qa[0] - qv[0], qa[1] - qv[1]); e2 = (qb[0] - qv[0], qb[1] - qv[1])
            m1, m2 = math.hypot(*e1), math.hypot(*e2)
            if r < 1.5 or m1 < 1 or m2 < 1: out.append(f"L{P[i][0]:.1f},{P[i][1]:.1f}"); continue
            tt = min(r * tan2, m1 * 0.5, m2 * 0.5); r = tt / tan2
            p1 = (qv[0] + e1[0] / m1 * tt, qv[1] + e1[1] / m1 * tt)
            p2 = (qv[0] + e2[0] / m2 * tt, qv[1] + e2[1] / m2 * tt)
            out.append(f"L{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 0 {1 if cross > 0 else 0} {p2[0]:.1f},{p2[1]:.1f}")
            c = st_key.get(nkey(v))
            if c is not None and abs(O[i]) < 0.1:
                bx, by = e1[0] / m1 + e2[0] / m2, e1[1] / m1 + e2[1] / m2; bl = math.hypot(bx, by) or 1
                dd = r / math.cos(theta / 2) - r  # vertex -> arc midpoint, along the inner bisector
                shift[c] = (bx / bl * dd, by / bl * dd)
        out.append(f"L{P[-1][0]:.1f},{P[-1][1]:.1f}")
        line_svgs.append(f'<path class="ln ln-{line} ph-{phase}" data-y="{chy}" d="{" ".join(out)}" data-sharp="{sharp}" stroke="{LINES[line]["color"]}"/>')

# ---------- stations + labels ----------
FS = 10.5
def text_w(s, bold=False): return len(s) * FS * (0.58 if bold else 0.54)

placed_boxes = []
grid = defaultdict(list)
CELL = 80
def cells(b):
    for gx in range(int(b[0] // CELL), int(b[2] // CELL) + 1):
        for gy in range(int(b[1] // CELL), int(b[3] // CELL) + 1):
            yield (gx, gy)
seg_grid = defaultdict(list)
for idx, (a, b, hw) in enumerate(segments_for_collision):
    bb = (min(a[0], b[0]) - hw, min(a[1], b[1]) - hw, max(a[0], b[0]) + hw, max(a[1], b[1]) + hw)
    for c in cells(bb): seg_grid[c].append(idx)

def seg_box_hit(a, b, hw, box):
    # inflate box by half-width, sample segment
    bx0, by0, bx1, by1 = box[0] - hw, box[1] - hw, box[2] + hw, box[3] + hw
    L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(2, int(L / 3))
    for i in range(n + 1):
        t = i / n; x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
        if bx0 <= x <= bx1 and by0 <= y <= by1: return True
    return False

def overlap(b1, b2):
    return not (b1[2] <= b2[0] or b2[2] <= b1[0] or b1[3] <= b2[1] or b2[3] <= b1[1])

SKIP_IDX = set()
def score_box(box):
    s = 0
    if box[0] < 4 or box[1] < 4 or box[2] > W - 4 or box[3] > H - 4: s += 500
    seen = set()
    for c in cells(box):
        for i in grid[c]:
            if i in seen or i in SKIP_IDX: continue
            seen.add(i)
            if overlap(box, placed_boxes[i]): s += 1000
    seen = set()
    for c in cells(box):
        for i in seg_grid[c]:
            if i in seen: continue
            seen.add(i)
            a, b, hw = segments_for_collision[i]
            if seg_box_hit(a, b, hw, box): s += 120
    return s

def add_box(box):
    placed_boxes.append(box)
    for c in cells(box): grid[c].append(len(placed_boxes) - 1)

def wrap(name):
    if len(name) < 16: return [name]
    for sep in ["–", " - ", " "]:
        pass
    words = name.replace("–", "– ").split(" ")
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]).replace("– ", "–"), " ".join(words[i:]).replace("– ", "–")
        m = max(len(a), len(b))
        if best is None or m < best[0]: best = (m, [a, b])
    return best[1] if best else [name]

stations_out = []
order = []
for c, (x, y) in st_pos.items():
    mem = cx_members[c]
    lines = sorted({ln for i in mem for ln in S[i][4]})
    order.append((-(len(lines) > 1), c))
order.sort()

# reserve marker boxes first
marker_r = {}
marker_idx = {}
for _, c in order:
    x, y = st_pos[c]
    mem = cx_members[c]
    lines = {ln for i in mem for ln in S[i][4]}
    ix = len(lines) > 1
    r = max(6.5, spread_at[c] + 3) if ix else max(3.4, spread_at[c] + 1.5)
    marker_r[c] = (r, ix)
    marker_idx[c] = len(placed_boxes)
    add_box((x - r, y - r, x + r, y + r))

DIRS = [  # (dx, dy, anchor, pref)
    (1, 0, "start", 0), (-1, 0, "end", 0.3), (0, -1, "middle", 0.6), (0, 1, "middle", 0.6),
    (0.75, -0.75, "start", 0.8), (0.75, 0.75, "start", 0.8), (-0.75, -0.75, "end", 1.0), (-0.75, 0.75, "end", 1.0),
]
# dense horizontal chains: nearest station closer than the label width on a horizontal line
def horiz_dense(c, w):
    x, y = st_pos[c]
    horiz = False
    for a, b, hw in segments_for_collision:
        for p, q in ((a, b), (b, a)):
            if math.hypot(p[0] - x, p[1] - y) < 0.6 and abs(q[1] - p[1]) < 0.5 and abs(q[0] - p[0]) > 1: horiz = True
    if not horiz: return False
    d = min((math.hypot(x - v[0], y - v[1]) for k2, v in st_pos.items() if k2 != c), default=1e9)
    return d < w + 10
BAD = []
labels = []
def shape_boxes(ax, ay, w, h, ang, anc):
    """approximate a (possibly rotated) label by small boxes"""
    if ang == 0: return None
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    sgn = 1 if anc == "start" else -1
    n = max(1, int(math.ceil(w / (h * 0.9))))
    out = []
    for j in range(n):
        d = (j + 0.5) * w / n * sgn
        cx_, cy_ = ax + ux * d, ay + uy * d
        out.append((cx_ - h * .5, cy_ - h * .5, cx_ + h * .5, cy_ + h * .5))
    return out

for _, c in order:
    x, y = st_pos[c]
    r, ix = marker_r[c]
    mem = cx_members[c]
    names = [S[i][0] for i in mem]
    name = min(names, key=len) if len(set(names)) > 1 else names[0]
    proj = all(S[i][3] == "p" for i in mem)
    variants = [[name]] + ([wrap(name)] if len(name) >= 16 else [])
    best = None
    SKIP_IDX.clear()
    dense = horiz_dense(c, text_w(name, ix))
    for fsk, lines_txt in [(1.0, v) for v in variants] + [(0.8, v) for v in variants]:
        if fsk < 1 and best[0] < 1000: break
        w = max(text_w(t, ix) for t in lines_txt) * fsk; h = FS * 1.15 * len(lines_txt) * fsk
        for dx, dy, anc, pref in DIRS:
            for dist in (r + 3, r + 9):
                ax, ay = x + dx * dist, y + dy * dist
                bx0 = ax if anc == "start" else ax - w if anc == "end" else ax - w / 2
                if dy < -0.1 and dx == 0: by0 = ay - h
                elif dy > 0.1 and dx == 0: by0 = ay
                elif dy < -0.1: by0 = ay - h
                elif dy > 0.1: by0 = ay
                else: by0 = ay - h / 2
                box = (bx0, by0, bx0 + w, by0 + h)
                sc = score_box(box) + pref * 10 + (dist > r + 3) * 15 + (len(lines_txt) > 1) * 8 + dense * 400
                if best is None or sc < best[0]: best = (sc, [box], lines_txt, anc, ax, by0, 0, ay, fsk)
        if len(lines_txt) == 1:
            # 45-degree labels
            for ang, dx, dy, anc in ((-45, .7, -.7, "start"), (45, .7, .7, "start"), (45, -.7, -.7, "end"), (-45, -.7, .7, "end")):
                dist = r + 2.5
                ax, ay = x + dx * dist, y + dy * dist
                bxs = shape_boxes(ax, ay, w, FS * 1.05 * fsk, ang, anc)
                SKIP_IDX.add(marker_idx[c])
                sc = sum(score_box(b) for b in bxs) / max(1, len(bxs)) * 1.0 + 14
                sc = sc if all(score_box(b) < 1000 for b in bxs) else sc + 2000
                SKIP_IDX.clear()
                if best is None or sc < best[0]: best = (sc, bxs, lines_txt, anc, ax, ay, ang, ay, fsk)
    sc, bxs, lines_txt, anc, ax, by0, ang, ay, fsk = best
    if sc >= 1000: BAD.append(name)
    for b in bxs: add_box(b)
    labels.append((c, bxs, lines_txt, anc, ax, by0, ix, proj, ang, ay, fsk))

# ---------- emit ----------
out = [f'<svg xmlns="http://www.w3.org/2000/svg" id="schem-svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">',
       '<g id="s-lines" fill="none" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">']
out += line_svgs
out.append('</g><g id="s-stations">')
lab_by_c = {l[0]: l for l in labels}
for _, c in order:
    x, y = st_pos[c]
    r, ix = marker_r[c]
    mem = cx_members[c]
    served = {}
    for i in mem:
        for ln, ph in S[i][4].items(): served[f"{ln}:{ph}:{S[i][7].get(ln, 9999)}"] = 1
    proj = all(S[i][3] == "p" for i in mem)
    first = mem[0]
    col = "var(--stroke)" if ix else LINES[next(iter(S[first][4]))]["color"]
    cls = "st" + (" ix" if ix else "") + (" proj" if proj else "")
    lab = lab_by_c[c]; _, bxs, lines_txt, anc, ax, by0, _, _, ang, ay, fsk = lab
    F = FS * fsk
    if ang:
        tx = f'<tspan x="{ax:.1f}" y="{ay + F * 0.35:.1f}">{html.escape(lines_txt[0])}</tspan>'
    else:
        tx = "".join(f'<tspan x="{ax:.1f}" y="{by0 + F * (0.92 + 1.15 * j):.1f}">{html.escape(t)}</tspan>' for j, t in enumerate(lines_txt))
    sh = shift.get(c) if not ix else None
    shattr = f' data-sh="{sh[0]:.1f},{sh[1]:.1f}" transform="translate({sh[0]:.1f},{sh[1]:.1f})"' if sh else ""
    out.append(f'<g class="{cls}" data-i="{",".join(map(str, mem))}" data-s="{" ".join(served)}"{shattr}>'
               f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" style="stroke:{col}"/>'
               f'<text text-anchor="{anc}"' + (f' style="font-size:{F:.1f}px"' if fsk < 1 else "") + (f' transform="rotate({ang} {ax:.1f} {ay:.1f})"' if ang else "") + f'>{tx}</text></g>')
out.append("</g></svg>")
open(sys.argv[3], "w").write("\n".join(out))
print(f"overlaps={len(BAD)} {BAD[:12]}"); print(f"W={W:.0f} H={H:.0f} stations={len(st_pos)} lines={len(line_svgs)}")
