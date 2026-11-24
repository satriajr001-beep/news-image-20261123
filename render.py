#!/usr/bin/env python3
"""Render the 23 Nov 2026 world-news summary poster (1024x1024 PNG).

All text is drawn with PIL from DejaVu fonts — no image model renders words.
Stories verified against CNN, Reuters and WSJ (23 November 2026).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (232, 163, 61)
INK = (26, 26, 26)
GRAY = (90, 90, 86)
CARD = (255, 255, 255)
BORDER = (214, 208, 194)
GREEN = (74, 122, 0)        # Nvidia green, darkened for contrast
STEEL = (46, 90, 136)
TEAL = (30, 122, 90)
RUST = (179, 64, 42)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(text, fnt, x, y, max_w, fill, leading):
    ys = y
    for line in wrap(text, fnt, max_w):
        d.text((x, ys), line, font=fnt, fill=fill)
        ys += leading
    return ys


# ---------------- masthead ----------------
d.rectangle([0, 0, W, 148], fill=NAVY)
mast = font(SERIF_B, 62)
t = "THE WORLD TODAY"
d.text(((W - d.textlength(t, font=mast)) / 2, 26), t, font=mast, fill=(255, 255, 255))
date_f = font(SANS_B, 26)
t = "MONDAY, 23 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=date_f)) / 2, 100), t, font=date_f, fill=GOLD)
d.line([36, 148, W - 36, 148], fill=GOLD, width=3)

# ---------------- lead story: Nvidia ----------------
LX, LY, LW, LH = 36, 168, 952, 300
d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=10, fill=CARD, outline=BORDER, width=2)
# chip icon, top right
cx, cy, s = LX + LW - 96, LY + 26, 62
d.rounded_rectangle([cx, cy, cx + s, cy + s], radius=8, fill=(118, 185, 0))
for i in range(3):
    yy = cy + 12 + i * 19
    d.line([cx - 8, yy, cx, yy], fill=(118, 185, 0), width=4)
    d.line([cx + s, yy, cx + s + 8, yy], fill=(118, 185, 0), width=4)
ai_f = font(SANS_B, 26)
t = "AI"
d.text((cx + (s - d.textlength(t, font=ai_f)) / 2, cy + 16), t, font=ai_f, fill=(255, 255, 255))

kick = font(SANS_B, 22)
d.text((LX + 28, LY + 24), "TECH  ·  BUSINESS", font=kick, fill=GREEN)
head = font(SERIF_B, 54)
d.text((LX + 28, LY + 58), "Huang is back at Nvidia", font=head, fill=INK)
body = font(SANS, 24)
lead = ("Nvidia's board unanimously reinstated Jensen Huang as chief executive on Monday, "
        "11 days after he resigned. President Trump pressed the board to bring him back, "
        "and shares soared 31% — their best day since 2003.")
draw_wrapped(lead, body, LX + 28, LY + 138, LW - 56, INK, 34)

# ---------------- "also today" label ----------------
lab = font(SANS_B, 20)
d.text((36, 492), "ALSO TODAY", font=lab, fill=GRAY)
d.line([170, 502, 988, 502], fill=BORDER, width=2)

# ---------------- three panels ----------------
panels = [
    dict(x=36, band=STEEL, kicker="UKRAINE WAR",
         headline="Ukraine sinks Russian warship off Libya",
         body=("Seven naval drones sank the corvette Merkury at Benghazi, Kyiv says, "
               "spreading the war to the Mediterranean."),
         icon="bars"),
    dict(x=360, band=TEAL, kicker="CLIMATE",
         headline="COP31 ends without a deal",
         body=("Climate talks in Antalya collapse after running two days over, split over "
               "fossil fuels and money for poor nations."),
         icon="sun"),
    dict(x=684, band=RUST, kicker="MIDDLE EAST",
         headline="Iran says tankers hit mines in Hormuz",
         body=("Three oil tankers caught fire after hitting mines, the Revolutionary Guards "
               "say, despite a US escort. The claims are unverified."),
         icon="flame"),
]
PY, PH, PW = 520, 408, 304
for p in panels:
    x = p["x"]
    d.rounded_rectangle([x, PY, x + PW, PY + PH], radius=10, fill=CARD, outline=BORDER, width=2)
    d.rectangle([x + 10, PY, x + PW - 10, PY + 8], fill=p["band"])
    # icon (60x60) at top
    ix, iy = x + 20, PY + 28
    if p["icon"] == "bars":
        for i, bh in enumerate([22, 38, 54]):
            bx = ix + i * 20
            d.rectangle([bx, iy + 54 - bh, bx + 14, iy + 54], fill=STEEL)
    elif p["icon"] == "sun":
        d.ellipse([ix + 8, iy + 8, ix + 46, iy + 46], fill=(232, 163, 61))
        for ang in range(0, 360, 45):
            import math
            r1, r2 = 30, 38
            cx0, cy0 = ix + 27, iy + 27
            x1 = cx0 + r1 * math.cos(math.radians(ang))
            y1 = cy0 + r1 * math.sin(math.radians(ang))
            x2 = cx0 + r2 * math.cos(math.radians(ang))
            y2 = cy0 + r2 * math.sin(math.radians(ang))
            d.line([x1, y1, x2, y2], fill=(232, 163, 61), width=4)
    elif p["icon"] == "flame":
        d.polygon([(ix + 27, iy + 2), (ix + 52, iy + 54), (ix + 2, iy + 54)], fill=(214, 90, 40))
        d.polygon([(ix + 27, iy + 24), (ix + 42, iy + 54), (ix + 12, iy + 54)], fill=(240, 180, 40))
    kf = font(SANS_B, 20)
    d.text((x + 20, PY + 98), p["kicker"], font=kf, fill=p["band"])
    hf = font(SERIF_B, 30)
    y = draw_wrapped(p["headline"], hf, x + 20, PY + 126, PW - 40, INK, 36)
    bf = font(SANS, 20)
    draw_wrapped(p["body"], bf, x + 20, y + 10, PW - 40, (60, 60, 60), 26)

# ---------------- footer ----------------
d.line([36, 940, 988, 940], fill=BORDER, width=2)
ff = font(SANS, 18)
t = "Sources: CNN · Reuters · WSJ — 23 November 2026"
d.text(((W - d.textlength(t, font=ff)) / 2, 954), t, font=ff, fill=GRAY)

img.save("/home/hatch/workspace/news-image-20261123/entry.png", optimize=True)
print("saved entry.png")
