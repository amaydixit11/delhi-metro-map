import json, sys, time, urllib.parse, urllib.request, os
out = sys.argv[2]
qs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
res = json.load(open(out)) if os.path.exists(out) else {}
for q in qs:
    if q in res: continue
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 3, "countrycodes": "in"})
    req = urllib.request.Request(url, headers={"User-Agent": "delhi-metro-map/1.0"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
        res[q] = [[float(x["lat"]), float(x["lon"]), x.get("display_name","")[:90]] for x in r]
    except Exception as e:
        res[q] = "ERR " + str(e)
    print(q, "->", res[q][:1] if isinstance(res[q], list) else res[q], flush=True)
    json.dump(res, open(out, "w"), indent=0)
    time.sleep(1.2)
