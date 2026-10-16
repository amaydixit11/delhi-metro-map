import json, math, sys
d = json.load(open(sys.argv[1])); fs = d["features"]
def merc(lon, lat): return lon, -math.degrees(math.log(math.tan(math.pi/4 + math.radians(lat)/2)))
pts = [merc(*c) for f in fs for c in ([f["geometry"]["coordinates"]] if f["geometry"]["type"]=="Point" else f["geometry"]["coordinates"])]
x0=min(p[0] for p in pts); x1=max(p[0] for p in pts); y0=min(p[1] for p in pts); y1=max(p[1] for p in pts)
W=1600; s=(W-80)/(x1-x0); H=int((y1-y0)*s)+80
P=lambda c:((merc(*c)[0]-x0)*s+40,(merc(*c)[1]-y0)*s+40)
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" style="background:#fff">']
for f in fs:
    if f["geometry"]["type"]!="LineString": continue
    ls=f["properties"]["lines"]; n=len(ls)
    pp=[P(c) for c in f["geometry"]["coordinates"]]
    for k,l in enumerate(ls):
        off=(k-(n-1)/2)*4
        (ax,ay),(bx,by)=pp[0],pp[-1]; dx,dy=bx-ax,by-ay; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L*off,dx/L*off
        out.append('<polyline fill="none" stroke="#%s" stroke-width="3.5" points="%s"/>'%(l["color"]," ".join(f"{x+nx:.1f},{y+ny:.1f}" for x,y in pp)))
for f in fs:
    if f["geometry"]["type"]!="Point": continue
    x,y=P(f["geometry"]["coordinates"])
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#fff" stroke="#222" stroke-width="1"/>')
    if len(sys.argv)>3: out.append(f'<text x="{x+4:.1f}" y="{y+3:.1f}" font-size="7" font-family="Arial">{f["properties"].get("station_label","")}</text>')
out.append("</svg>"); open(sys.argv[2],"w").write("\n".join(out)); print(W,H)
