"""WorldPop 2020 1 km grid -> 500 m cells for the NCR core + named hotspot blocks (data/pop.js).
usage: python population.py ind_ppp_2020_1km_Aggregated_UNadj.tif data/pop.js   (needs rasterio, numpy)"""
import json, sys, time, urllib.parse, urllib.request
import numpy as np, rasterio
from rasterio.windows import from_bounds
import os
W, S, E, N = map(float, os.environ.get("POP_BBOX", "76.85,28.30,77.60,28.92").split(","))   # default: Delhi NCR core
r = rasterio.open(sys.argv[1])
win = from_bounds(W, S, E, N, r.transform).round_offsets().round_lengths()
a = r.read(1, window=win).astype(float); a[a < 0] = 0
t = r.window_transform(win); lon0, lat0, d1 = t.c, t.f, t.a          # top-left corner, 1 km step (deg)
# 2x upsample: bilinear-smoothed density, then rescale so each 1 km cell keeps its total
ny, nx = a.shape
pad = np.pad(a, 1, mode="edge")
up = np.zeros((ny * 2, nx * 2))
for dy in (0, 1):
    for dx in (0, 1):
        oy, ox = (dy * 2 - 1) * 0.25, (dx * 2 - 1) * 0.25
        y0, x0 = 1 + oy, 1 + ox
        iy, ix = int(np.floor(y0)), int(np.floor(x0)); fy, fx = y0 - iy, x0 - ix
        b = (pad[iy:iy + ny, ix:ix + nx] * (1 - fy) * (1 - fx) + pad[iy + 1:iy + 1 + ny, ix:ix + nx] * fy * (1 - fx)
             + pad[iy:iy + ny, ix + 1:ix + 1 + nx] * (1 - fy) * fx + pad[iy + 1:iy + 1 + ny, ix + 1:ix + 1 + nx] * fy * fx)
        up[dy::2, dx::2] = b
blk = up.reshape(ny, 2, nx, 2).sum(axis=(1, 3)); blk[blk == 0] = 1
up *= np.repeat(np.repeat(a / blk, 2, 0), 2, 1)
cells = np.rint(up).astype(int)
d = d1 / 2
print("grid", cells.shape, "people", int(cells.sum()))
# hotspots: 2 km blocks (4x4 cells), top 70 by population, named by reverse geocoding
B = 4
H, Wd = cells.shape[0] // B, cells.shape[1] // B
bs = cells[:H * B, :Wd * B].reshape(H, B, Wd, B).sum(axis=(1, 3))
top = np.dstack(np.unravel_index(np.argsort(-bs, axis=None)[:70], bs.shape))[0]
def name(lat, lon):
    u = "https://nominatim.openstreetmap.org/reverse?" + urllib.parse.urlencode({"lat": lat, "lon": lon, "format": "json", "zoom": 15})
    j = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "delhi-metro-map/1.0"}), timeout=30))
    ad = j.get("address", {})
    return ad.get("suburb") or ad.get("neighbourhood") or ad.get("quarter") or ad.get("village") or ad.get("town") or ad.get("city_district") or "?"
hot = []
for by, bx in top:
    lat = lat0 - (by * B + B / 2) * d; lon = lon0 + (bx * B + B / 2) * d
    hot.append([round(lat, 4), round(lon, 4), name(lat, lon), int(by * B), int(bx * B)]); time.sleep(1.1)
    print(hot[-1][2], int(bs[by, bx]), flush=True)
out = dict(lat0=lat0, lon0=lon0, d=d, nx=int(cells.shape[1]), ny=int(cells.shape[0]), B=B,
           cells=cells.ravel().tolist(), hot=hot, src="WorldPop 2020, UN-adjusted, 1 km (CC BY 4.0)")
open(sys.argv[2], "w").write("window.POP=" + json.dumps(out, separators=(",", ":")) + ";")
