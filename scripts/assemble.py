import sys
t = open("src/template.html").read()
d = open("data/metro-data.js").read()
s = open("schematic/schem.svg").read()
import re
s = re.sub(r'^(<svg[^>]*?) width="[^"]*" height="[^"]*"', r'\1', s, count=1)
out = t.replace("/*DATA*/", d).replace("<!--SCHEM-->", s)
open("dist/index.html", "w").write(out)
print(len(out))
