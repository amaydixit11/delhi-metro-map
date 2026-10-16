"""Readable Reddit images: central-NCR crop of the schematic, thick lines, few big labels."""
import re, json, sys, html
svg = open("schematic/schem.svg").read()
M = json.loads(open("data/metro-data.js").read()[len("window.METRO="):-1])
S, LINES = M["stations"], M["lines"]
X0, Y0, X1, Y1 = 640, 1980, 3920, 4930      # crop in schematic units
OUTW = 3000                                   # output px width
k = OUTW / (X1 - X0)
mode, year, title, sub, fname = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
MIN_LINES = int(sys.argv[6]) if len(sys.argv) > 6 else 3

# hubs from the schematic station groups
hubs = []
for m in re.finditer(r'<g class="([^"]*)" data-i="([^"]+)" data-s="([^"]*)"[^>]*><circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', svg):
    served = [x.split(":") for x in m.group(3).split()]
    alive = {l for l, p, y in served if (year == 0 or float(y) < year + 1) and (mode != "today" or p == "op")}
    x, y, r = float(m.group(4)), float(m.group(5)), float(m.group(6))
    if not (X0 < x < X1 and Y0 < y < Y1): continue
    ids = [int(i) for i in m.group(2).split(",")]
    names = [S[i][0] for i in ids]
    name = min(names, key=len) if len(set(names)) > 1 else names[0]
    hubs.append((len(alive), name, x, y, r))
hubs.sort(key=lambda h: -h[0])
FS = 30 / k                                   # 30 px on the output image
# obstacles: every drawn line segment (straight version) + every station circle
segs = []
for m in re.finditer(r'<path class="ln[^"]*ph-(\w+)" data-y="([\d.]+)" d="[^"]*" data-sharp="([^"]+)"', svg):
    ph, y = m.group(1), float(m.group(2))
    if year and (y >= year + 1 or (mode == "today" and ph != "op")): continue
    pts = [tuple(map(float, q.split(","))) for q in re.findall(r"[-\d.]+,[-\d.]+", m.group(3))]
    segs += list(zip(pts, pts[1:]))
circles = [(x, y, r) for _, _, x, y, r in hubs]
LW = 6 / k
def seg_hit(box, a, b):
    x0, y0, x1, y1 = box[0] - LW, box[1] - LW, box[2] + LW, box[3] + LW
    if max(a[0], b[0]) < x0 or min(a[0], b[0]) > x1 or max(a[1], b[1]) < y0 or min(a[1], b[1]) > y1: return False
    L = max(abs(b[0] - a[0]), abs(b[1] - a[1])); n = max(2, int(L / 2))
    return any(x0 <= a[0] + (b[0] - a[0]) * i / n <= x1 and y0 <= a[1] + (b[1] - a[1]) * i / n <= y1 for i in range(n + 1))
def hits(box, own):
    h = sum(1 for a, b in segs if seg_hit(box, a, b))
    h += sum(2 for (cx, cy, cr) in circles if (cx, cy) != own and box[0] - cr < cx < box[2] + cr and box[1] - cr < cy < box[3] + cr)
    return h
MUST = ["Rajiv Chowk", "Kashmere Gate", "New Delhi", "Central Secretariat", "Mandi House", "Hauz Khas", "Lajpat Nagar",
        "Sarai Kale Khan", "Anand Vihar", "Botanical Garden", "Noida Sector 142", "Dilli Haat–INA", "Kalkaji Mandir",
        "Janakpuri West", "Rajouri Garden", "Netaji Subhash Place", "Azadpur", "Inderlok", "Delhi Aerocity", "Terminal 1 IGI Airport",
        "Millennium City Centre Gurugram", "Rajiv Chowk (Gurugram)", "Hero Honda Chowk", "Cyber City", "IFFCO Chowk", "Sikanderpur",
        "Tughlakabad", "Ghaziabad", "Yashobhoomi Dwarka Sector 25", "Kirti Nagar", "Indraprastha", "Welcome", "Pari Chowk", "Kherki Daula"]
hubs.sort(key=lambda h: (h[1] not in MUST, MUST.index(h[1]) if h[1] in MUST else 0, -h[0]))
placed, labels = [], []
def ov(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
for n, name, x, y, r in hubs:
    if n < MIN_LINES: continue
    w = len(name) * FS * 0.56; h = FS * 1.1
    best = None
    for dist in (r + FS * 0.35, r + FS * 0.9):
        for dx, dy, anc in ((1, 0, "start"), (-1, 0, "end"), (0, -1, "middle"), (0, 1, "middle"),
                            (.72, -.72, "start"), (.72, .72, "start"), (-.72, -.72, "end"), (-.72, .72, "end")):
            ax, ay0 = x + dx * dist, y + dy * dist
            if dy < -.1: base = ay0 - h * .15
            elif dy > .1: base = ay0 + h * .8
            else: base = ay0 + h * .35
            bx = ax if anc == "start" else ax - w if anc == "end" else ax - w / 2
            box = (bx, base - h * .82, bx + w, base + h * .18)
            if any(ov(box, p) for p in placed) or not (X0 < box[0] and box[2] < X1 and Y0 < box[1] and box[3] < Y1): continue
            sc = hits(box, (x, y)) * 10 + (dist > r + FS * .5) * 8 + (dx != 0 and dy != 0) * 1
            if best is None or sc < best[0]: best = (sc, box, ax, base, anc)
    if best is None: continue
    limit = 4 if name in MUST else 1 if n >= 3 else 0   # hits allowed: must-label hubs may cross a few lines
    if best[0] // 10 > limit: continue
    placed.append(best[1]); labels.append((best[2], best[3], best[4], name))
lab = "".join(f'<text x="{ax:.1f}" y="{ay:.1f}" text-anchor="{anc}">{html.escape(nm)}</text>' for ax, ay, anc, nm in labels)
body = svg.replace('<svg xmlns="http://www.w3.org/2000/svg" id="schem-svg" viewBox="0 0 ', '<svg xmlns="http://www.w3.org/2000/svg" id="schem-svg" data-full="', 1)
body = re.sub(r'data-full="[^"]*" width="[^"]*" height="[^"]*"', f'viewBox="{X0} {Y0} {X1-X0} {Y1-Y0}" width="{OUTW}" height="{(Y1-Y0)*k:.0f}"', body, 1)
body = body.replace("</svg>", f'<g id="hub-labels" style="font:700 {FS:.1f}px Inter,Arial,sans-serif">{lab}</g></svg>')
sw = 11 / k * (1.0 if mode == "detail" else 1.0)
legend = [] if True else [("Open", ""), ("Under construction / approved", "12 7"), ("Phase V(B) · state approved", ".1 10"), ("Proposed", "3 6 10 6")]
leg = "".join(f'<div class="ph"><svg width="90" height="20"><line x1="5" y1="10" x2="85" y2="10" stroke="#1d1d1f" stroke-width="7" stroke-linecap="round" stroke-dasharray="{d}"/></svg>{t}</div>' for t, d in legend)
leg += '<div class="ph"><svg width="40" height="30"><circle cx="20" cy="15" r="11" fill="#fff" stroke="#1d1d1f" stroke-width="4"/></svg>Interchange</div><div class="ph"><svg width="40" height="30"><circle cx="20" cy="15" r="6" fill="#fff" stroke="#1d1d1f" stroke-width="3"/></svg>Station</div>'
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#f7f6f2;font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:#1d1d1f}}
.wrap{{width:{OUTW}px;padding:70px 70px 50px;box-sizing:content-box}}
h1{{font-size:104px;margin:0;letter-spacing:-3px;line-height:1.05}} .sub{{font-size:44px;color:#555;margin:18px 0 26px}}
.legend{{display:flex;flex-wrap:wrap;gap:16px 46px;font-size:34px;margin-bottom:24px}} .ph{{display:flex;align-items:center;gap:12px}}
#s-lines path{{stroke-width:{sw:.2f}px}}
.ph-IV,.ph-G1{{stroke-dasharray:{14/k:.1f} {8/k:.1f}}} .ph-VA{{stroke-dasharray:{10/k:.1f} {7/k:.1f}}}
.ph-VB{{stroke-dasharray:.1 {16/k:.1f}}} .ph-VC,.ph-G2{{stroke-dasharray:{4/k:.1f} {8/k:.1f} {14/k:.1f} {8/k:.1f}}} .ph-RR{{stroke-dasharray:{22/k:.1f} {7/k:.1f}}}
.st circle{{fill:#fff;stroke-width:{3/k:.2f}px}} .st.ix circle{{stroke:#1d1d1f!important;stroke-width:{4/k:.2f}px}}
.st text{{display:{'inline' if mode=='detail' else 'none'};font:600 11px Inter,Arial,sans-serif;fill:#1d1d1f;paint-order:stroke;stroke:#f7f6f2;stroke-width:3px}}
.st.proj text{{font-style:italic;fill:#666}} .st.proj circle{{stroke-dasharray:2 2}}
#hub-labels{{display:{'none' if mode=='detail' else 'inline'};fill:#1d1d1f;paint-order:stroke;stroke:#f7f6f2;stroke-width:{13/k:.1f}px;stroke-linejoin:round}}
{'' if mode=='detail' else '.st:not(.ix) circle{r:' + f'{5/k:.1f}' + 'px}'}
{'path.ln:not(.ph-op){display:none} ' if mode=='today' else ''}#s-lines path{{stroke-dasharray:none!important}} .st.proj circle{{stroke-dasharray:none!important}} .foot{{font-size:26px;color:#777;margin-top:22px;line-height:1.45}}
</style></head><body><div class="wrap"><h1>{title}</h1><div class="sub">{sub}</div><div class="legend">{leg}</div>
{body}
<div class="foot">Not an official map. Open lines from OpenStreetMap; plans from DMRC, NCRTC, GMRL, NMRC, Union Cabinet & news reports (Oct 2026).<br>Most V(B)/V(C) and NCR station names are not yet published; those stops are placed by locality{" and shown in italics" if mode=="detail" else ""}. Outer lines to Karnal, Alwar, Meerut, Rohtak, Jewar etc. cropped.</div>
</div><script>
const Y={year};
if(Y){{document.querySelectorAll('path.ln').forEach(p=>{{if(+p.dataset.y>=Y+1)p.style.display='none'}});
document.querySelectorAll('g.st').forEach(g=>{{const ok=g.dataset.s.split(' ').some(x=>+x.split(':')[2]<Y+1&&({'true' if mode=='today' else 'false'}?x.split(':')[1]==='op':true));if(!ok)g.style.display='none'}});}}
</script></body></html>'''
open(fname, "w").write(page)
print(len(labels), "hub labels")
