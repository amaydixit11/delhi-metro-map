import sys, json, re, os
city = os.environ.get("CITY", "delhi")
base = "" if city == "delhi" else f"cities/{city}/"
t = open("src/template.html").read()
d = open(f"{base or 'data/'}{'metro-data.js'}").read()
s = open(f"{base or ''}schematic/schem.svg" if not base else f"{base}schem.svg").read()
s = re.sub(r'^(<svg[^>]*?) width="[^"]*" height="[^"]*"', r'\1', s, count=1)
cfg = json.load(open(f"cities/{city}/page.json")); cfg["code"] = city
popf = "data/pop.js" if city == "delhi" else f"{base}pop.js"
pop = open(popf).read() if os.path.exists(popf) else "window.POP=null;"
out = (t.replace("/*CITY*/", "window.CITY=" + json.dumps(cfg, ensure_ascii=False) + ";").replace("/*DATA*/", d)
        .replace("<!--SCHEM-->", s).replace("/*POP*/", pop))
dest = "dist/index.html" if city == "delhi" else f"dist/{city}/index.html"
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, "w").write(out)
print(dest, len(out))
