"""Vertical 1080x1920 reel from the animation frames (run scripts/anim.py first).
usage: python3 scripts/reel.py <python-with-imageio-ffmpeg>"""
import os, subprocess, sys, html
VENV_PY = sys.argv[1]
OUT = "anim/reel"; os.makedirs(OUT, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
YEARS = list(range(2002, 2042))
def caption(y):
    if y <= 2004: return "2002: one line.<br>Shahdara to Tis Hazari."
    if y <= 2011: return "Phase I &amp; II give the city<br>its backbone"
    if y <= 2019: return "The Pink and Magenta<br>ring lines arrive"
    if y <= 2025: return "Gurugram, Noida, Faridabad,<br>Ghaziabad all connected"
    if y == 2026: return "<b>Today</b><br>India's biggest metro"
    if y <= 2030: return "Phase IV + V(A) + V(B)<br>under way"
    if y <= 2035: return "Gurugram, Noida &amp; Meerut lines<br>+ Namo Bharat to Panipat"
    return "<b>Fully built:</b> ~1,130 km<br>bigger than any metro today"
TOP = "How Delhi Metro grows<br>2002 → 2041"
def page(img, cap, top=TOP, end=False):
    body = (f'<div class="top">{top}</div><img src="{img}"><div class="cap">{cap}</div>' if not end else
            f'<div class="endc"><div style="font-size:84px;font-weight:800;line-height:1.05">Explore every line,<br>year &amp; route</div>'
            f'<div style="font-size:46px;margin-top:40px;color:#444">amaydixit11.github.io/<br>delhi-metro-map</div>'
            f'<div style="font-size:34px;margin-top:60px;color:#888">Not an official map · plans from DMRC, NCRTC &amp; news reports</div></div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1080px;height:1920px;background:#f7f6f2;font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:#1d1d1f;overflow:hidden}}
.top{{position:absolute;top:150px;left:60px;right:60px;font-size:74px;font-weight:800;line-height:1.08;letter-spacing:-1.5px}}
img{{position:absolute;top:420px;left:0;width:1080px}}
.cap{{position:absolute;top:1560px;left:60px;right:60px;font-size:58px;line-height:1.18;font-weight:500}}
.cap b{{font-weight:800}}
.endc{{position:absolute;top:620px;left:80px;right:80px;text-align:center}}
</style></head><body>{body}</body></html>'''
jobs = []
for y in YEARS:
    p = os.path.abspath(f"{OUT}/r{y}.html")
    open(p, "w").write(page(os.path.abspath(f"anim/frames/f{y}.png"), caption(y)))
    jobs.append((p, f"{OUT}/r{y}.png"))
p = os.path.abspath(f"{OUT}/rend.html"); open(p, "w").write(page("", "", end=True)); jobs.append((p, f"{OUT}/rend.png"))
import concurrent.futures as cf
def shot(j): subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1920",
                             f"--screenshot={j[1]}", "file://" + j[0]], check=True, capture_output=True)
with cf.ThreadPoolExecutor(6) as ex: list(ex.map(shot, jobs))
lst = open(f"{OUT}/list.txt", "w")
for y in YEARS:
    d = 0.55
    if y in (2002, 2026): d = 1.6
    if y == 2041: d = 2.6
    lst.write(f"file 'r{y}.png'\nduration {d}\n")
lst.write("file 'rend.png'\nduration 3\nfile 'rend.png'\n"); lst.close()
subprocess.run([VENV_PY, "-c", f'''
import imageio_ffmpeg, subprocess
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "{OUT}/list.txt", "-vf", "fps=30,format=yuv420p",
                "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", "images/delhi-metro-reel.mp4"], check=True)
'''], check=True)
print("images/delhi-metro-reel.mp4")
