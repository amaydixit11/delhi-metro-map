"""Render the 2002→2041 growth animation (MP4 + GIF) from the schematic."""
import json, math, os, subprocess, sys, concurrent.futures as cf
VENV_PY = sys.argv[1]                      # python with imageio-ffmpeg + pillow
OUT = "anim"; os.makedirs(f"{OUT}/frames", exist_ok=True)
M = json.loads(open("data/metro-data.js").read()[len("window.METRO="):-1])
S = M["stations"]
RR = {"rrts", "rrA", "rrP", "rrJ", "nbg", "rrF", "rrK", "rrR", "rrH", "rrB"}
SCALE = 0.907                              # calibrates straight-line km to DMRC's published ~416 km (2026)
def km(a, b):
    dl = math.radians(b[1] - a[1]); dn = math.radians(b[2] - a[2])
    x = math.sin(dl / 2) ** 2 + math.cos(math.radians(a[1])) * math.cos(math.radians(b[1])) * math.sin(dn / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(x)) * 1.12
def stats(Y):
    mk = 0; st = set()
    for g in M["segments"]:
        if g["line"] in RR: continue
        ys = g["ey"] if g["phase"] == "op" else [g["yr"]] * (len(g["ids"]) - 1)
        for k, (a, b) in enumerate(zip(g["ids"], g["ids"][1:])):
            if ys[k] < Y + 1 and (Y > 2026 or g["phase"] == "op"):
                mk += km(S[a], S[b]); st.add(S[a][5]); st.add(S[b][5])
    return round(mk * SCALE / 5) * 5, len(st)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
YEARS = list(range(2002, 2042))
def frame(Y):
    kmv, n = stats(Y)
    est = Y > 2026
    env = dict(os.environ, POSTER_FS="40", POSTER_BADGE=str(Y), POSTER_STATS=f"{kmv:,} km · {n} stations")
    sub = "Open lines" if not est else "Open + planned (official targets, otherwise estimates)"
    html = f"{OUT}/frames/f{Y}.html"
    subprocess.run([sys.executable, "-W", "ignore", "-I", "scripts/poster.py", "today" if not est else "hero", str(Y),
                    "Delhi NCR Metro", sub, html, "3"], env=env, check=True, capture_output=True)
    png = f"{OUT}/frames/f{Y}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=3140,3180",
                    f"--screenshot={png}", "file://" + os.path.abspath(html)], check=True, capture_output=True)
    return Y, kmv, n
with cf.ThreadPoolExecutor(4) as ex:
    for Y, kmv, n in ex.map(frame, YEARS): print(Y, kmv, n, flush=True)
# encode: 0.45 s per year, 2.5 s hold on the last frame
subprocess.run([VENV_PY, "-c", f'''
import imageio_ffmpeg, subprocess
from PIL import Image
ff = imageio_ffmpeg.get_ffmpeg_exe()
years = {YEARS}
lst = open("{OUT}/list.txt", "w")
for y in years:
    lst.write(f"file 'frames/f{{y}}.png'\\nduration {{2.5 if y == years[-1] else (1.2 if y == 2026 else 0.45)}}\\n")
lst.write(f"file 'frames/f{{years[-1]}}.png'\\n"); lst.close()
vf = "scale=1080:-2:flags=lanczos,format=yuv420p"
subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "{OUT}/list.txt", "-vf", vf, "-r", "30",
                "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", "{OUT}/delhi-metro-2002-2041.mp4"], check=True)
subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "{OUT}/list.txt",
                "-vf", "fps=10,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=sierra2_4a",
                "{OUT}/delhi-metro-2002-2041.gif"], check=True)
'''], check=True)
print("done")
