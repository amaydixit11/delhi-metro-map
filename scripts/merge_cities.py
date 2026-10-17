"""Merge every city's metro-data into one India map: dist/india/index.html (geographic view only)."""
import json, os, re
CITIES = [("delhi", "Delhi NCR", "data/metro-data.js"), ("blr", "Bengaluru", "cities/blr/metro-data.js"),
          ("mum", "Mumbai", "cities/mum/metro-data.js"), ("pune", "Pune", "cities/pune/metro-data.js"),
          ("hyd", "Hyderabad", "cities/hyd/metro-data.js")]
out = dict(lines={}, stations=[], segments=[], tracks={}, trackYears={}, sources={})
pages = {c: json.load(open(f"cities/{c}/page.json")) for c, _, _ in CITIES}
phases, order, short, label, thin, rail, speeds, jumps = {}, [], {}, {}, [], [], {}, []
for c, name, f in CITIES:
    d = json.loads(open(f).read()[len("window.METRO="):-1])
    pre = lambda k: f"{c}_{k}"
    off, cxo = len(out["stations"]), len(out["stations"])
    for k, v in d["lines"].items(): out["lines"][pre(k)] = {**v, "name": v["name"] if c == "delhi" else f'{name}: {v["name"]}'}
    for s in d["stations"]:
        s = list(s); s[4] = {pre(k): v for k, v in s[4].items()}; s[5] += cxo; s[7] = {pre(k): v for k, v in s[7].items()}
        out["stations"].append(s)
    for g in d["segments"]:
        g = dict(g); g["line"] = pre(g["line"]); g["ids"] = [i + off for i in g["ids"]]
        if "src" in g: g["src"] = pre(g["src"])
        out["segments"].append(g)
    for k, v in d["tracks"].items(): out["tracks"][pre(k)] = v
    for k, v in d.get("trackYears", {}).items(): out["trackYears"][pre(k)] = v
    for k, v in d["sources"].items(): out["sources"][pre(k)] = v
    p = pages[c]
    for ph in p["order"]:
        if ph not in order: order.append(ph); phases[ph] = p["phases"][ph]; label[ph] = p["label"][ph]
        if ph in p["short"]: short.setdefault(ph, p["short"][ph])
    thin += [pre(x) for x in p["thin"]]; rail += [pre(x) for x in p["rail"]]
    speeds.update({pre(k): v for k, v in p["speeds"].items()})
    jumps.append([name, p["fit"]])
phases["OP"]["n"] = "Open (recent, other cities)"; phases["AP"]["n"] = "Approved (other cities)"; phases["UC"]["n"] = "Under construction (other cities)"; phases["PR"]["n"] = "Proposed (other cities)"
cfg = dict(code="india", title="India metro maps", h1="India's metros · open, building and planned",
           sub="Delhi NCR, Bengaluru, Mumbai, Pune and Hyderabad on one map. Pick a city below or zoom around. Data as of Oct 2026.",
           agency="the metro authority", region="these cities", fit=pages["delhi"]["fit"], allFit=[[17.0, 72.6], [29.2, 78.8]], lat=22.0,
           phases=phases, order=order, short=short, label=label, thin=thin, rail=rail, speeds=speeds, jumps=jumps,
           noSchematic=True, newLabel="planned stations",
           notes="".join(f'<div class="note"><b>{n}:</b> see the single-city page for its notes and sources.</div>' for _, n, _ in CITIES))
t = open("src/template.html").read()
html = (t.replace("/*CITY*/", "window.CITY=" + json.dumps(cfg, ensure_ascii=False) + ";")
        .replace("/*DATA*/", "window.METRO=" + json.dumps(out, separators=(",", ":"), ensure_ascii=False) + ";")
        .replace("<!--SCHEM-->", '<svg xmlns="http://www.w3.org/2000/svg" id="schem-svg" viewBox="0 0 10 10"></svg>')
        .replace("/*POP*/", "window.POP=null;"))
os.makedirs("dist/india", exist_ok=True); open("dist/india/index.html", "w").write(html)
print("dist/india/index.html", len(html), "stations", len(out["stations"]))
