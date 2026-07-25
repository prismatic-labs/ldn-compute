"""Generate the social-share card (public/og.png, 1200x630) from live data.

Runs automatically in the deploy workflow (.github/workflows/deploy.yml) before the
build, so the card in production always reflects current numbers. The committed
public/og.png is the local/dev fallback; regenerate it locally with any Pillow-enabled
Python if you want the checked-in copy fresh too."""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630
PAPER = (247, 246, 242)
INK = (26, 29, 31)
MUTED = (92, 99, 106)
UMBER = (138, 115, 85)
BLUE = (0, 114, 178)      # operating (Okabe-Ito)
STONE = (154, 139, 118)   # proposed

def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()

BOLD = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]  # last two: Linux/CI
REG = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
       "/System/Library/Fonts/Helvetica.ttc",
       "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
       "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]  # last two: Linux/CI

# --- live numbers ---
d = json.load(open(os.path.join(ROOT, "data/sites.geojson")))
PRIO = ["max_proposed_mw", "grid_connection_mw", "phase_1_mw", "it_load_mw"]
PIPE = {"pipeline", "consented", "under_construction"}
def best(p):
    pw = p.get("power") or {}
    for k in PRIO:
        q = pw.get(k)
        if isinstance(q, dict) and isinstance(q.get("value"), (int, float)):
            return q["value"]
    return 0
op = pipe = sites = 0
for f in d["features"]:
    p = f["properties"]
    if p.get("role") == "aggregate" or p.get("status") == "decommissioned":
        continue
    sites += 1
    r = p.get("operational_reality")
    if r == "operating": op += best(p)
    elif r in PIPE: pipe += best(p)
op, pipe = round(op), round(pipe)

img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img)
M = 76

# eyebrow
eb = font(BOLD, 27)
dr.text((M, 70), "T H E   L O N D O N   C O M P U T E   R I N G", font=eb, fill=UMBER)

# headline
hl = font(BOLD, 68)
dr.text((M, 120), "London's data-centre", font=hl, fill=INK)
dr.text((M, 196), "build-out, in the open", font=hl, fill=INK)

# sub
sub = font(REG, 31)
dr.text((M, 296), "A sourced map of AI & cloud infrastructure:", font=sub, fill=MUTED)
dr.text((M, 336), "power, land, and water — where communities can see them.", font=sub, fill=MUTED)

# stacked bar
bx, by, bw, bh = M, 430, W - 2 * M, 46
total = max(op + pipe, 1)
opw = int(bw * op / total)
dr.rounded_rectangle([bx, by, bx + opw - 2, by + bh], radius=6, fill=BLUE)
dr.rounded_rectangle([bx + opw + 2, by, bx + bw, by + bh], radius=6, fill=STONE)

lab = font(BOLD, 30)
small = font(REG, 25)
dr.text((bx, by + bh + 16), f"≈{op:,} MW operating", font=lab, fill=INK)
tw = dr.textlength(f"≈{pipe:,} MW proposed", font=lab)
dr.text((bx + bw - tw, by + bh + 16), f"≈{pipe:,} MW proposed", font=lab, fill=INK)

# footer
foot = font(REG, 25)
dr.text((M, H - 58), f"{sites} sourced sites · Greater London & the M25 fringe", font=foot, fill=MUTED)

out = os.path.join(ROOT, "public/og.png")
img.save(out, "PNG")
print(f"wrote {out}  ({op} MW operating / {pipe} MW proposed / {sites} sites)")
