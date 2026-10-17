import sys, json, re, os

def og_tags(cfg, path):
    base = os.environ.get("BASE", "https://india-metro-map.vercel.app")
    title = cfg["h1"]; desc = cfg["sub"].replace('"', "'")
    return (f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{base}/og.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:url" content="{base}/{path}">\n<meta property="og:type" content="website">\n<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="description" content="{desc}">')
city = os.environ.get("CITY", "delhi")
base = "" if city == "delhi" else f"cities/{city}/"
t = open("src/template.html").read()
d = open(f"{base or 'data/'}{'metro-data.js'}").read()
s = open(f"{base or ''}schematic/schem.svg" if not base else f"{base}schem.svg").read()
s = re.sub(r'^(<svg[^>]*?) width="[^"]*" height="[^"]*"', r'\1', s, count=1)
cfg = json.load(open(f"cities/{city}/page.json")); cfg["code"] = city
popf = "data/pop.js" if city == "delhi" else f"{base}pop.js"
pop = open(popf).read() if os.path.exists(popf) else "window.POP=null;"
t = t.replace("<!--OG-->", og_tags(cfg, "" if city == "delhi" else city + "/"))
out = (t.replace("/*CITY*/", "window.CITY=" + json.dumps(cfg, ensure_ascii=False) + ";").replace("/*DATA*/", d)
        .replace("<!--SCHEM-->", s).replace("/*POP*/", pop))
dest = "dist/index.html" if city == "delhi" else f"dist/{city}/index.html"
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, "w").write(out)
print(dest, len(out))
