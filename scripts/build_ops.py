import json, re, sys
d = json.load(open(sys.argv[1]))
els = d["elements"]
nodes = {e["id"]: e for e in els if e["type"] == "node"}
ways = {e["id"]: e for e in els if e["type"] == "way"}
rels = {e["id"]: e for e in els if e["type"] == "relation"}

# one relation per drawn branch: (relation id, line key)
PICK = [
    (447214, "red"), (447210, "yellow"), (447209, "blue"), (2535795, "blue"),
    (8037666, "green"), (2535796, "green"), (2535797, "violet"),
    (8037715, "airport"), (8241298, "pink"), (8385429, "magenta"),
    (20300114, "magenta"), (3537978, "grey"), (9268568, "aqua"),
    (4481323, "rapid"), (17337287, "rrts"), (16661918, "meerut"),
]
RENAME = {
    "Rohini West": "Dr. Baba Saheb Ambedkar Hospital", "Rohini East": "Rohini",
    "Rajendra Nagar": "Major Mohit Sharma Rajendra Nagar", "Punjabi Bagh": "Punjabi Bagh East",
    "Surajmal Stadium": "Maharaja Surajmal Stadium", "North Pitampura - Prashant Vihar": "Uttari Pitampura–Prashant Vihar",
    "Pul Bangash": "Pulbangash", "Barakhambha Road": "Barakhamba Road", "Chawri Bazaar": "Chawri Bazar",
    "Vishwa Vidyalaya": "Vishwavidyalaya", "GTB Nagar": "Guru Tegh Bahadur Nagar", "A.I.I.M.S.": "AIIMS",
    "M G Road": "MG Road", "IIT Delhi": "IIT", "Dashrath Puri": "Dashrathpuri",
    "New Delhi Airport Express Terminal": "New Delhi", "IGI Airport": "IGI Airport T3",
    "Satguru Ramsingh Marg": "Satguru Ram Singh Marg", "Shaheed Sthal": "Shaheed Sthal (New Bus Adda)",
    "Maujpur-Babarpur": "Maujpur–Babarpur", "Jagatpur - Wazirabad": "Jagatpur–Wazirabad",
    "Nanaksar - Sonia Vihar": "Nanaksar–Sonia Vihar", "Noida Golf Course": "Golf Course",
    "Dwarka - Kakrola": "Dwarka–Kakrola", "Trilokpuri Sanjay Lake": "Trilokpuri–Sanjay Lake",
    "Shree Ram Mandir Mayur Vihar": "Shri Ram Mandir Mayur Vihar", "Mayur Vihar - I": "Mayur Vihar-I",
    "East Vinod Nagar - Mayur Vihar - II": "East Vinod Nagar–Mayur Vihar-II",
    "Mandawali - West Vinod Nagar": "Mandawali–West Vinod Nagar", "ESI - Basaidarapur": "ESI–Basaidarapur",
    "Sarai Kale Khan - Nizamuddin": "Sarai Kale Khan–Nizamuddin", "Dilli Haat - INA": "Dilli Haat–INA",
    "Dabri Mor - Janakpuri South": "Dabri Mor–Janakpuri South", "Sir M. Vishweshwaraiah Moti Bagh": "Sir M. Vishweshwaraiah Moti Bagh",
    "Phase 3 Station": "Phase 3", "Bhainsali": "Bhaisali", "Moulsari Avenue Station": "Moulsari Avenue", "Depot Station": "Depot",
}
import os
CITY = os.environ.get("CITY", "delhi")
if CITY != "delhi":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cities", CITY))
    from config import PICK, RENAME
def clean(n):
    n = re.sub(r"\s*\((Blue|Yellow|Red|Pink|Grey|Magenta|Violet|Green) Line\)", "", n).strip()
    return RENAME.get(n, n)

tracks, stops = {}, {}
for rid, key in PICK:
    r = rels[rid]
    for m in r["members"]:
        if m["type"] == "way" and m["role"] in ("", "route") and m["ref"] in ways and "geometry" in ways[m["ref"]]:
            g = [[round(p["lat"], 5), round(p["lon"], 5)] for p in ways[m["ref"]]["geometry"]]
            tracks.setdefault(key, []).append(g)
    seq = []
    for m in r["members"]:
        if m["type"] == "node" and m["role"].startswith("stop") and m["ref"] in nodes:
            n = nodes[m["ref"]]
            nm = clean(n.get("tags", {}).get("name", "?"))
            if seq and seq[-1][0] == nm: continue
            seq.append([nm, round(n["lat"], 5), round(n["lon"], 5)])
    stops.setdefault(key, []).append(seq)

# Rapid Metro loop: drop duplicate DLF Phase 2/Sikanderpur repeats
json.dump({"tracks": tracks, "stops": stops}, open(sys.argv[2], "w"), separators=(",", ":"))
for k, v in stops.items():
    print(k, [len(s) for s in v], sum(len(t) for t in tracks[k]), "ways")
