"""Opening years for the timeline: operational sections (from the Wikipedia phase tables) and planned targets."""
import math, re

# (from, to, "YYYY-MM") along each operational stop sequence; edges not covered take the line default
OPEN = {
    "red": [("Shahdara", "Tis Hazari", "2002-12"), ("Tis Hazari", "Inderlok", "2003-10"), ("Inderlok", "Rithala", "2004-03"),
            ("Shahdara", "Dilshad Garden", "2008-06"), ("Dilshad Garden", "Shaheed Sthal (New Bus Adda)", "2019-03")],
    "yellow": [("Vishwavidyalaya", "Kashmere Gate", "2004-12"), ("Kashmere Gate", "Central Secretariat", "2005-07"),
               ("Vishwavidyalaya", "Jahangirpuri", "2009-02"), ("Millennium City Centre Gurugram", "Qutab Minar", "2010-06"),
               ("Qutab Minar", "Central Secretariat", "2010-09"), ("Jahangirpuri", "Samaypur Badli", "2015-11")],
    "blue": [("Dwarka–Kakrola", "Barakhamba Road", "2005-12"), ("Dwarka Sector 9", "Dwarka–Kakrola", "2006-04"),
             ("Barakhamba Road", "Indraprastha", "2006-11"), ("Indraprastha", "Yamuna Bank", "2009-05"),
             ("Yamuna Bank", "Noida City Centre", "2009-11"), ("Dwarka Sector 9", "Dwarka Sector 21", "2010-10"),
             ("Noida City Centre", "Noida Electronic City", "2019-03"),
             ("Yamuna Bank", "Anand Vihar", "2010-01"), ("Anand Vihar", "Vaishali", "2011-07")],
    "green": [("Inderlok", "Mundka", "2010-04"), ("Mundka", "Brigadier Hoshiyar Singh", "2018-06"),
              ("Ashok Park Main", "Kirti Nagar", "2011-08")],
    "violet": [("Central Secretariat", "Sarita Vihar", "2010-10"), ("Sarita Vihar", "Badarpur", "2011-01"),
               ("Mandi House", "Central Secretariat", "2014-06"), ("ITO", "Mandi House", "2015-06"),
               ("Badarpur", "Escorts Mujesar", "2015-09"), ("Kashmere Gate", "ITO", "2017-05"),
               ("Escorts Mujesar", "Raja Nahar Singh", "2018-11")],
    "airport": [("New Delhi", "Dwarka Sector 21", "2011-02"), ("Dwarka Sector 21", "Yashobhoomi Dwarka Sector 25", "2023-09")],
    "pink": [("Majlis Park", "Durgabai Deshmukh South Campus", "2018-03"), ("Durgabai Deshmukh South Campus", "Lajpat Nagar", "2018-08"),
             ("Shiv Vihar", "Trilokpuri–Sanjay Lake", "2018-10"), ("Lajpat Nagar", "Shri Ram Mandir Mayur Vihar", "2018-12"),
             ("Shri Ram Mandir Mayur Vihar", "Trilokpuri–Sanjay Lake", "2021-08"), ("Majlis Park", "Maujpur–Babarpur", "2026-03")],
    "magenta": [("Kalkaji Mandir", "Botanical Garden", "2017-12"), ("Janakpuri West", "Kalkaji Mandir", "2018-05"),
                ("Janakpuri West", "Krishna Park Extension", "2025-01"), ("Majlis Park", "Deepali Chowk", "2026-03")],
    "grey": [("Dwarka–Kakrola", "Najafgarh", "2019-10"), ("Najafgarh", "Dhansa Bus Stand", "2021-09")],
    "rapid": [("Sector 55–56", "Sikanderpur", "2017-03")],
    "rrts": [("Sahibabad", "Duhai", "2023-10"), ("Duhai", "Modinagar North", "2024-03"), ("Modinagar North", "Meerut South", "2024-08"),
             ("New Ashok Nagar", "Sahibabad", "2025-01"), ("Sarai Kale Khan", "New Ashok Nagar", "2026-02"),
             ("Meerut South", "Modipuram", "2026-02")],
}
DEFAULT = {"aqua": "2019-01", "rapid": "2013-11", "meerut": "2026-02"}
INFILL = {("green", "Punjabi Bagh West"): "2022-03"}  # station opened later than the track through it

PHASE_DEFAULT = {"VA": 2028, "VB": 2030}
YR_OVERRIDE = {"Aqua: Depot → Boraki": 2028}
# Estimated completion for corridors with no official target (our estimate, as of Oct 2026):
# year = (approval stage + typical sanction lag) + ~4–5 yr construction, nudged later for Delhi's history of slippage.
EST = {
  "Namo Bharat: Sarai Kale Khan → Panipat → Karnal": (2032, "PIB cleared Nov 2025; Cabinet sanction + ~5 yr build"),
  "Palam Vihar → Dwarka Sector 21": (2031, "Gurugram plan: construction from 2027 + ~4 yr"),
  "Yashobhoomi Dwarka Sec 25 → Rajiv Chowk (Gurugram)": (2032, "Gurugram plan: construction from 2027; 20 km underground ≈ 5 yr"),
  "Namo Bharat: IFFCO Chowk → Faridabad → Surajpur": (2032, "Gurugram plan: construction from 2027 + ~5 yr"),
  "Namo Bharat: Ghaziabad → Noida Airport (Jewar)": (2033, "DPR with UP govt since 2024; YEIDA funding set"),
  "Aqua: Noida Sector 51 → Knowledge Park V": (2033, "built together with the Ghaziabad–Jewar RRTS section I"),
  "Brigadier Hoshiyar Singh → Asaudha": (2032, "DPR May 2026, short 8 km elevated"),
  "Sector 56 → Pachgaon (Manesar)": (2034, "Gurugram plan: construction from 2029 + ~5 yr"),
  "Kherki Daula → Sector 111 (Dwarka Expressway)": (2034, "Gurugram plan: construction from 2029 + ~5 yr"),
  "Bhondsi → Gurugram Railway Station": (2034, "Gurugram plan: construction from 2029 + ~5 yr"),
  "Manesar → Samalkha–Kapashera Road (via Old Gurugram)": (2035, "Gurugram plan: construction from 2030 + ~5 yr"),
  "Golf Course Ext. Road → Sector 5": (2035, "Gurugram plan: construction from 2030 + ~5 yr"),
  "Faridabad–Gurugram: Bata Chowk → Vatika Chowk": (2034, "revised DPR pending; Aravalli section slows approvals"),
  "Raja Nahar Singh → Palwal": (2034, "HMRTC feasibility done; Haryana-funded"),
  "Shaheed Sthal → Ghaziabad Railway Station": (2035, "DMRC 18-corridor plan, after V(B)"),
  "Noida Electronic City → Sahibabad": (2035, "DMRC 18-corridor plan, after V(B)"),
  "Vaishali → Mohan Nagar": (2035, "DMRC 18-corridor plan, after V(B)"),
  "Dwarka Sector 21 → Udyog Vihar": (2035, "folded into the Airport-line DPR"),
  "Mayapuri → Kashmere Gate": (2036, "new underground line, DMRC 18-corridor plan"),
  "Tughlakabad → Noida Sector 142": (2036, "DMRC 18-corridor plan; Yamuna crossing"),
  "Gokulpuri → Arthala (via Hindon Airport)": (2035, "DMRC 18-corridor plan, after V(B)"),
  "Yamuna Bank → Loni": (2036, "DMRC 18-corridor plan, second stage"),
  "Shiv Vihar → Loni": (2035, "short Phase V proposal"),
  "Mayur Vihar Ph-III → Loni Border": (2036, "DMRC 18-corridor plan, second stage"),
  "CGO Complex → Surya Vihar (Faridabad)": (2037, "DMRC 18-corridor plan, second stage; route undecided"),
  "Grey Line: Dhansa Bus Stand → Jhajjar (via Badli)": (2036, "DPR consultant tendered Mar 2025"),
  "Red Line: Nathupur → Sonipat Sector 7": (2037, "studies done; follows Rithala–Nathupur (2029)"),
  "Green Line: Asaudha → Rohtak": (2037, "studies done; follows Asaudha (2032)"),
  "Meerut Line 2: Shradhapuri Ph-II → Jagriti Vihar": (2035, "awaiting new DPR tender"),
  "Meerut Line 3: CCS University → Begumpul (via Ganga Nagar)": (2038, "planning stage"),
  "Film City light rail: Noida Airport → YEIDA Sector 21": (2035, "tied to Film City and the Jewar RRTS"),
  "Namo Bharat: Delhi → Faridabad → Ballabgarh → Palwal": (2036, "NCRTC future phase; DPRs being prepared"),
  "Namo Bharat: Delhi → Bahadurgarh → Rohtak": (2037, "NCRTC future phase"),
  "Namo Bharat: Delhi → Shahdara → Baghpat → Baraut": (2037, "NCRTC future phase"),
  "Namo Bharat: Ghaziabad → Hapur": (2038, "NCRTC future phase"),
  "Namo Bharat: Ghaziabad → Bulandshahr → Khurja": (2038, "NCRTC future phase"),
  "Delhi Metrolite: Kirti Nagar → Dwarka Sector 28 (Bamnoli)": (2040, "stalled since 2019; may be cancelled"),
  "Palwal → Noida Airport (Jewar)": (2040, "no study yet"),
}
NEVER = 9999


def ym(s):
    y, m = s.split("-"); return round(int(y) + (int(m) - 1) / 12, 3)


def planned_year(sg):
    if sg["title"] in YR_OVERRIDE: return YR_OVERRIDE[sg["title"]]
    if sg["title"] in EST:
        sg["est"] = EST[sg["title"]][1]; return EST[sg["title"]][0]
    if sg["phase"] == "VB": sg["est"] = "V(B) has no official date; four corridors are due by 2029"
    yrs = [int(x) for x in re.findall(r"20\d\d", sg["status"])]
    if yrs and (sg["phase"] in ("IV",) or "target" in sg["status"]): return max(yrs)
    return PHASE_DEFAULT.get(sg["phase"], NEVER)


def seq_pairs(names, a, b):
    ia = [i for i, n in enumerate(names) if n == a]; ib = [i for i, n in enumerate(names) if n == b]
    if not ia or not ib: return None
    i, j = min(((i, j) for i in ia for j in ib), key=lambda p: abs(p[0] - p[1]))
    return (min(i, j), max(i, j))


def compute(stations, segs, tracks):
    S = stations
    line_year = {}  # (station id, line) -> earliest year
    edge_years = {}  # (cx_a, cx_b, line) -> year (for the schematic)
    missing = []
    for g in segs:
        line, ids = g["line"], g["ids"]
        if g["phase"] == "op":
            names = [S[i]["name"] for i in ids]
            ey = [None] * (len(ids) - 1)
            for a, b, d in OPEN.get(line, []):
                rng = seq_pairs(names, a, b)
                if rng is None: continue
                for k in range(rng[0], rng[1]):
                    if ey[k] is None or ym(d) < ey[k]: ey[k] = ym(d)
            dflt = ym(DEFAULT[line]) if line in DEFAULT else None
            for k in range(len(ey)):
                if ey[k] is None:
                    if dflt is None: missing.append((line, names[k], names[k + 1])); ey[k] = 2000
                    else: ey[k] = dflt
            g["ey"] = ey
        else:
            y = planned_year(g); g["yr"] = y
            ey = [y] * (len(ids) - 1)
        for k, (a, b) in enumerate(zip(ids, ids[1:])):
            for s in (a, b):
                key = (s, line)
                if key not in line_year or ey[k] < line_year[key]: line_year[key] = ey[k]
            ca, cb = S[a]["cx"], S[b]["cx"]
            kk = (min(ca, cb), max(ca, cb), line)
            if kk not in edge_years or ey[k] < edge_years[kk]: edge_years[kk] = ey[k]
    for (line, name), d in INFILL.items():
        for s in S:
            if s["name"] == name and (s["id"], line) in line_year: line_year[(s["id"], line)] = max(line_year[(s["id"], line)], ym(d))
    for s in S:
        ly = {ln: line_year[(s["id"], ln)] for ln in s["served"] if (s["id"], ln) in line_year}
        s["ly"] = ly
        s["y"] = min(ly.values()) if ly else NEVER

    # each OSM track way takes the year of the nearest station-to-station edge of its line
    def segd(p, a, b):
        ax, ay, bx, by = a[1], a[0], b[1], b[0]; px, py = p[1], p[0]
        dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy or 1e-12
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
        return math.hypot(px - (ax + t * dx), py - (ay + t * dy))
    track_years = {}
    for line, ways in tracks.items():
        edges = []
        for g in segs:
            if g["line"] == line and g["phase"] == "op":
                for k, (a, b) in enumerate(zip(g["ids"], g["ids"][1:])):
                    edges.append(((S[a]["lat"], S[a]["lon"]), (S[b]["lat"], S[b]["lon"]), g["ey"][k]))
        ys = []
        for w in ways:
            mid = w[len(w) // 2]
            best = min(edges, key=lambda e: segd(mid, e[0], e[1])) if edges else None
            ys.append(best[2] if best else 2000)
        track_years[line] = ys
    return edge_years, track_years, missing
