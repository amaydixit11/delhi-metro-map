"""Shared config for non-Delhi cities: reads cities/<code>/plan.json + routes.json and exposes the names
build_ops / build_data / years expect (PICK, RENAME, LINES, SEGMENTS, SOURCES, OPEN, DEFAULT, EST, PHASE_DEFAULT)."""
import json, os, re, difflib

EST_BY_STATUS = {"under_construction": (2028, "under construction; no official date"),
                 "approved": (2031, "approved; no official date, ~5 yr build"),
                 "proposed": (2035, "proposed; no approval yet")}

def norm(n):
    n = n.lower().replace("&", "and")
    n = re.sub(r"\b(metro|station|stn|road|rd)\b\.?", " ", n)
    return re.sub(r"[^a-z0-9]+", "", n)

def make(city_dir, osm_lines, extra_rename=None):
    """osm_lines: {line_key_in_plan: [osm relation ids to draw]} for lines that are open in OSM."""
    plan = json.load(open(os.path.join(city_dir, "plan.json")))
    routes = json.load(open(os.path.join(city_dir, "routes.json")))
    nodes = {e["id"]: e for e in routes["elements"] if e["type"] == "node"}
    rels = {e["id"]: e for e in routes["elements"] if e["type"] == "relation"}
    PICK, osm_names = [], {}
    for key, ids in osm_lines.items():
        for rid in ids:
            PICK.append((rid, key))
            for m in rels[rid]["members"]:
                if m["type"] == "node" and m["role"].startswith("stop") and m["ref"] in nodes:
                    nm = nodes[m["ref"]].get("tags", {}).get("name")
                    if nm: osm_names.setdefault(key, set()).add((extra_rename or {}).get(nm, nm))
    RENAME = dict(extra_rename or {})
    LINES = {k: tuple(v) for k, v in plan["lines"].items()}
    SEGMENTS, OPEN, EST, SOURCES, YRO = [], {}, {}, {}, {}
    for sid, (t, u) in plan["sources"].items(): SOURCES[sid] = (t, u)
    for s in plan["segs"]:
        key = s["line"]; title = f"{LINES[key][0]}: {s['title']}"
        yr = str(s.get("year") or "")
        if s["status"] == "operational" and key in osm_lines:
            # opening date for this stretch, matched to OSM stop names
            if re.match(r"^\d{4}", yr):
                names = sorted(osm_names.get(key, []))
                def m(n):
                    hit = difflib.get_close_matches(norm(n), [norm(x) for x in names], n=1, cutoff=0.75)
                    return next((x for x in names if norm(x) == hit[0]), None) if hit else None
                a, b = m(s["st"][0][0]), m(s["st"][-1][0])
                if a and b:
                    OPEN.setdefault(key, []).append((a, b, yr[:7] if len(yr) >= 7 else yr[:4] + "-06"))
            continue
        phase = {"operational": "OP", "under_construction": "UC", "approved": "AP"}.get(s["status"], "PR")
        y4 = int(yr[:4]) if re.match(r"^\d{4}", yr) else None
        if s["status"] == "operational":
            YRO[title] = y4 or 2025
        elif y4:
            YRO[title] = y4
        else:
            EST[title] = EST_BY_STATUS.get(s["status"], (2036, "proposed"))
        status = s["status"].replace("_", " ").capitalize() + (f" · {s['stage']}" if s.get("stage") else "") + (f" · {yr}" if yr and s["status"] != "operational" else "")
        SEGMENTS.append(dict(line=key, phase=phase, title=title, status=status[:160], km=s.get("km"), n=s.get("n"), src=s["src"],
                             st=[(nm, la, lo, "o") for nm, la, lo in s["st"]]))
    used = {s["line"] for s in SEGMENTS} | set(osm_lines)
    LINES = {k: v for k, v in LINES.items() if k in used}
    DEFAULT = {}
    for k, lst in OPEN.items(): DEFAULT[k] = min(d for _, _, d in lst)
    first = {}
    for s in plan["segs"]:
        y = str(s.get("year") or "")
        if s["status"] == "operational" and re.match(r"^\d{4}", y):
            first[s["line"]] = min(first.get(s["line"], "9999"), y[:7] if len(y) >= 7 else y[:4] + "-06")
    for k in osm_lines: DEFAULT.setdefault(k, first.get(k, "2015-01"))
    return dict(PICK=PICK, RENAME=RENAME, LINES=LINES, SEGMENTS=SEGMENTS, SOURCES=SOURCES, OPEN=OPEN, DEFAULT=DEFAULT,
                EST=EST, YR_OVERRIDE=YRO, PHASE_DEFAULT={}, INFILL={}, NOTES=plan.get("notes", []))
