#!/usr/bin/env python3
"""THE WORLD DISPATCH — compose.py (NI23 G3, Final 7 / @lilywonder1).

Front page of a one-day world newspaper for Monday 23 November 2026.
Concept: a pine-green and cherry-red broadsheet built around the World
Chess Championship as the lead story, with a dotted world map whose
numbered pins match the numbered cards. All facts come only from the
locked NI23 pool. PIL is used here locally only; the submitted program
(main.py) is stdlib-only and copy-only.

Run: python3 compose.py [A|B|C] [out.png]
"""
import random
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MX = 28  # page margin


def fb(n):
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Bold.ttf", n)


def fblack(n):
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Black.ttf", n)


def fr(n):
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", n)


def fab(n):
    return ImageFont.truetype(FONT_DIR + "Archivo-Bold.ttf", n)


def fsr(n):
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", n)


# ---------------------------------------------------------------- data
REGIONS = {
    "MIDDLE EAST": (196, 110, 26),
    "EUROPE": (33, 92, 168),
    "SOUTH ASIA": (133, 62, 168),
    "SE ASIA": (0, 143, 131),
    "ASIA-PACIFIC": (96, 140, 38),
    "NORTH AMERICA": (178, 38, 58),
    "AFRICA": (186, 148, 24),
    "GLOBAL": (96, 96, 96),
}

# (num, region, topic, src, head, deck, kind)
grid = [
    (2, "MIDDLE EAST", "tanker", "AP live · 23 Nov",
     "Tankers Burn in Hormuz Strait",
     "Iran–US war reaches the Gulf; IRGC warns of unrest.",
     "tanker"),
    (3, "NORTH AMERICA", "capitol", "BBC · 23 Nov",
     "Democrats Take House 258–173",
     "Biggest since 1992; a seat flipped in North Carolina.",
     "capitol"),
    (4, "EUROPE", "rescue", "BBC · 23 Nov",
     "Kyiv Boy Freed From Rubble",
     "Out after hours in Kyiv rubble; six killed, says the BBC.",
     "rescue"),
    (5, "SOUTH ASIA", "cricket", "ObserverVoice",
     "India Post Record 720/9",
     "Highest Test total on New Zealand soil, at Wellington.",
     "cricket"),
    (6, "GLOBAL", "gold", "ObserverVoice",
     "Gold Slides to $3,538/oz",
     "Down over $2,000 from the 2026 record of $5,595.",
     "gold"),
    (7, "EUROPE", "climate", "BBC / AP · 23 Nov",
     "COP31 Ends With No Deal",
     "The final draft from Turkiye omits fossil fuels at COP31.",
     "globe"),
    (8, "NORTH AMERICA", "shield", "AP wire · 23 Nov",
     "FBI Probes Data Hack",
     "Criminal Justice Database breach probed in Washington.",
     "shield"),
    (9, "SOUTH ASIA", "pipe", "ObserverVoice",
     "Tata Steel: ₹28,000 Cr Sale",
     "Pipe unit sold to APL Apollo in a record Steel Deal.",
     "pipe"),
    (10, "SE ASIA", "factory", "JagranJosh · 23 Nov",
     "Indonesia: 50 Still Missing",
     "23 Nov update: 7 bodies found, 50 missing.",
     "factory"),
    (11, "EUROPE", "drone", "JagranJosh · 23 Nov",
     "14 Missing After Kyiv Strike",
     "Zelenskiy says 14 are missing after a drone hit Kyiv.",
     "drone"),
    (12, "SOUTH ASIA", "plane", "ObserverVoice",
     "IndiGo Holds 65.9% of Skies",
     "SpiceJet pilots seek urgent audit; IndiGo at 65.9%.",
     "plane"),
    (13, "EUROPE", "trophy", "BBC · 23 Nov",
     "Alcaraz Wins ATP Finals",
     "Alcaraz beats Zverev to lift his first ATP Finals Crown.",
     "trophy"),
]

NUMS = [
    ("258–173", "US HOUSE DEMOCRATS"),
    ("720/9d", "WELLINGTON TEST RECORD"),
    ("7 + 50", "INDONESIA FOUND MISSING"),
    ("14", "KYIV MISSING STRIKE"),
    ("$3,538", "GOLD PER OUNCE"),
    ("₹28,000 cr", "TATA STEEL PIPE SALE"),
]

TL = [
    ("00:02 UTC", "UN keeps lethal-AI talks alive"),
    ("02:00 UTC", "Albanese reacts to COP31 failure"),
    ("Morning UTC", "Kyiv boy, 7, pulled out alive"),
    ("Midday UTC", "House win 258–173 confirmed"),
    ("Afternoon UTC", "India pile up 720/9, Wellington"),
    ("Evening UTC", "Alcaraz lifts ATP Finals title"),
]

BRIEFS_L = [
    "IRGC claims two Patriot radars hit in Bahrain",
    "Houthi missile intercepted over western Saudi",
    "Swimmer crosses Hormuz for Iran's wildlife",
    "UN to keep negotiating lethal AI weapons",
    "US releases more UFO footage from Middle East",
    "Albanese: COP31 failure signals hard times",
    "Russian cargo ship still burning off Finland",
    "Russia-bound ship towed in Gulf of Finland",
    "Blast hits Russian ship in Benghazi port",
    "UK–EU reset deal called a Landmark",
    "Thousands march in Lisbon on living costs",
    "Myanmar junta calls ASEAN ruling unfair",
    "Cameroon ex-rebels trapped by broken promises",
    "Escaped lion spreads fear in Turkiye",
    "Nepal PM Shah in bilateral talks with Modi",
]

BRIEFS_R = [
    "India, Bulgaria discuss IMEC, Black Sea",
    "Guru Nanak Jayanti marked across India",
    "UP air-raid, blackout drills in 75 districts",
    "ICJ rules Myanmar guilty of Rohingya genocide",
    "India chase famous win; NZ reach 119/2",
    "India win ODI series 3–2 in New Zealand",
    "Anupama defends IBSF world snooker title",
    "Rajya Sabha MP Wadkute dies in Delhi",
    "Pilgrim bus tragedy in Kota: 9 killed",
    "IFFI hosts BRICS roundtable in Goa",
    "Modi opens AI centre at IIT Patna",
    "Shah launches ₹4,000 cr Arunachal push",
    "Chief Justice: AI rules a must in law schools",
    "JEE Main 2027 Session 1 entry closes today",
]

dc = ("Xi–Trump–Putin summit — 19 Nov 2026 · "
      "SpiceJet ₹5,500 cr fundraise — 18 Nov 2026 · "
      "Hyderabad bomb-threat emails — 21 Nov 2026 · "
      "Paolo Bulgari death reported — 22 Nov 2026 · "
      "24 civilians killed, South Sudan — 22 Nov 2026 · "
      "Kerch Bridge strike reported — 22 Nov 2026 · "
      "Bolsonaro 'stable' in ICU — 22 Nov 2026 · "
      "S. Korea minister resigns (AI scandal) — 22 Nov 2026")

# (card num, x fraction, y fraction) over the dotted_map box
PINS = [
    (1, 0.52, 0.30), (2, 0.60, 0.44), (3, 0.15, 0.33), (4, 0.555, 0.28),
    (5, 0.965, 0.86), (6, 0.44, 0.46), (7, 0.565, 0.37), (8, 0.17, 0.36),
    (9, 0.685, 0.47), (10, 0.815, 0.63), (11, 0.545, 0.315),
    (12, 0.665, 0.50), (13, 0.505, 0.345),
]

MAP_ROWS = [
    "..........####................................................",
    "......##########......######....#####.........................",
    ".....############....#######################......#####.......",
    "......#########.....#########################...########.....",
    ".......#######.......#######################.....######.......",
    "........#####.........##################..........###.........",
    ".........###...........################.......................",
    "..........##............##############..........##............",
    "...........#.............############..........####...........",
    "..........................##########..........######..........",
    "...........................########............####...........",
    "............................######..............##............",
    ".............................####.............................",
    "..............................##..............................",
    "..............................................................",
    "..............................................................",
]

LEGEND = "Numbered dots mark where each story happened — dot size is not to scale."

PALETTES = {
    "A": dict(bg=(255, 255, 255), card=(252, 252, 250), ink=(23, 25, 23),
              mast=(27, 77, 50), accent=(163, 32, 47), soft=(235, 240, 236),
              line=(198, 200, 196), gray=(105, 105, 100)),
    "B": dict(bg=(247, 240, 221), card=(253, 249, 238), ink=(28, 26, 18),
              mast=(27, 77, 50), accent=(163, 32, 47), soft=(240, 233, 208),
              line=(205, 196, 168), gray=(110, 104, 88)),
    "C": dict(bg=(255, 255, 255), card=(252, 252, 250), ink=(23, 25, 23),
              mast=(163, 32, 47), accent=(27, 77, 50), soft=(243, 238, 240),
              line=(198, 200, 196), gray=(105, 105, 100)),
}


# ---------------------------------------------------------------- helpers
def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(dr, cx, y, text, font, fill):
    dr.text((cx - font.getlength(text) / 2, y), text, font=font, fill=fill)


def icon(dr, kind, x, y, s, col, ink):
    """Tiny own-drawn glyph in an s x s box at (x, y)."""
    cx, cy = x + s / 2, y + s / 2
    if kind == "tanker":
        dr.polygon([(x + 2, y + s - 6), (x + s - 2, y + s - 6),
                    (x + s - 6, y + s - 1), (x + 4, y + s - 1)], outline=col, width=2)
        dr.line([(x + 6, y + s - 6), (x + 6, y + 8), (x + s - 8, y + 8),
                 (x + s - 8, y + s - 6)], fill=col, width=2)
        dr.polygon([(cx, y + 1), (cx + 4, y + 7), (cx, y + 5), (cx - 4, y + 7)],
                   fill=(230, 120, 30))
    elif kind == "capitol":
        dr.arc([x + 5, y + 3, x + s - 5, y + s - 4], 180, 360, fill=col, width=2)
        dr.line([(x + 3, y + s - 8), (x + s - 3, y + s - 8)], fill=col, width=2)
        for i in range(4):
            xx = x + 6 + i * (s - 12) / 3
            dr.line([(xx, y + s - 8), (xx, y + 12)], fill=col, width=2)
        dr.line([(cx, y + 1), (cx, y + 5)], fill=col, width=2)
    elif kind == "rescue":
        dr.polygon([(x + 3, y + 11), (cx, y + 3), (x + s - 3, y + 11)], outline=col, width=2)
        dr.rectangle([x + 7, y + 11, x + s - 7, y + s - 3], outline=col, width=2)
        dr.line([(cx, y + 14), (cx, y + s - 6)], fill=(200, 40, 40), width=2)
        dr.line([(cx - 4, y + 17), (cx + 4, y + 17)], fill=(200, 40, 40), width=2)
    elif kind == "cricket":
        dr.line([(x + 7, y + s - 4), (x + s - 8, y + 5)], fill=col, width=4)
        dr.ellipse([x + s - 11, y + s - 11, x + s - 3, y + s - 3], outline=(200, 40, 40), width=2)
    elif kind == "gold":
        for i, yy in enumerate((y + s - 8, y + s - 15)):
            dr.polygon([(x + 5 + i * 4, yy), (x + 13 + i * 4, yy - 5),
                        (x + 21 + i * 4, yy), (x + 17 + i * 4, yy + 4),
                        (x + 9 + i * 4, yy + 4)], outline=col, width=2)
    elif kind == "globe":
        dr.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=col, width=2)
        dr.line([(x + 4, cy), (x + s - 4, cy)], fill=col, width=1)
        dr.arc([cx - 5, y + 4, cx + 5, y + s - 4], 90, 270, fill=col, width=1)
        dr.arc([cx - 5, y + 4, cx + 5, y + s - 4], 270, 90, fill=col, width=1)
    elif kind == "shield":
        dr.polygon([(cx, y + 3), (x + s - 5, y + 6), (x + s - 5, y + s - 9),
                    (cx, y + s - 2), (x + 5, y + s - 9), (x + 5, y + 6)],
                   outline=col, width=2)
        dr.line([(cx - 4, cy), (cx - 1, cy + 3), (cx + 5, cy - 4)], fill=col, width=2)
    elif kind == "pipe":
        dr.rectangle([x + 3, cy - 5, x + s - 3, cy + 5], outline=col, width=2)
        dr.line([(x + 9, cy - 5), (x + 9, cy + 5)], fill=col, width=2)
        dr.line([(x + s - 9, cy - 5), (x + s - 9, cy + 5)], fill=col, width=2)
    elif kind == "factory":
        dr.rectangle([x + 3, y + s - 10, x + s - 3, y + s - 3], outline=col, width=2)
        dr.rectangle([x + 6, y + 6, x + 11, y + s - 10], outline=col, width=2)
        dr.ellipse([x + 4, y + 1, x + 12, y + 7], outline=col, width=1)
    elif kind == "drone":
        for dx, dy in ((6, 6), (s - 6, 6), (6, s - 6), (s - 6, s - 6)):
            dr.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], outline=col, width=2)
        dr.line([(x + 8, y + 8), (x + s - 8, y + s - 8)], fill=col, width=1)
        dr.line([(x + s - 8, y + 8), (x + 8, y + s - 8)], fill=col, width=1)
        dr.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)
    elif kind == "plane":
        dr.polygon([(x + 3, cy + 4), (x + s - 4, cy - 5), (x + s - 8, cy + 3),
                    (cx + 2, cy + 2), (cx + 2, cy + 7), (cx - 3, cy + 7),
                    (cx - 3, cy + 3)], outline=col, width=2)
    elif kind == "trophy":
        dr.arc([x + 6, y + 3, x + s - 6, y + 17], 0, 180, fill=col, width=2)
        dr.line([(x + 6, y + 10), (x + 6, y + 12)], fill=col, width=2)
        dr.line([(x + s - 6, y + 10), (x + s - 6, y + 12)], fill=col, width=2)
        dr.line([(cx, y + 16), (cx, y + s - 6)], fill=col, width=2)
        dr.line([(x + 8, y + s - 4), (x + s - 8, y + s - 4)], fill=col, width=2)
    else:  # chess knight-ish: a stepped horse head profile
        dr.polygon([(x + 8, y + s - 3), (x + 8, y + 12), (x + 13, y + 5),
                    (x + s - 6, y + 3), (x + s - 9, y + 10), (x + 14, y + 13),
                    (x + 15, y + s - 3)], outline=col, width=2)
        dr.ellipse([x + 15, y + 7, x + 18, y + 10], fill=col)


def dotted_map(dr, x, y, w, h, pal):
    """Own dotted world map from a coarse land grid, with numbered pins."""
    rows = MAP_ROWS
    gh = len(rows)
    gw = max(len(r) for r in rows)
    sx, sy = w / gw, (h - 14) / gh
    dot = max(2, int(min(sx, sy) * 0.42))
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "#":
                cxp, cyp = x + i * sx + sx / 2, y + j * sy + sy / 2
                dr.ellipse([cxp - dot / 2, cyp - dot / 2, cxp + dot / 2, cyp + dot / 2],
                           fill=pal["mast"])
    for num, fx, fy in PINS:
        px, py = x + fx * w, y + fy * (h - 14)
        dr.ellipse([px - 8, py - 8, px + 8, py + 8], fill=pal["accent"])
        t = str(num)
        f = fab(10)
        dr.text((px - f.getlength(t) / 2, py - 6), t, font=f, fill=(255, 255, 255))


def chess_drawing(dr, x, y, w, h, pal):
    """Chessboard with a knight — the lead story's own drawing."""
    sq = min(w // 8, h // 8)
    ox, oy = x + (w - sq * 8) // 2, y + (h - sq * 8) // 2
    for r in range(8):
        for c in range(8):
            fill = pal["soft"] if (r + c) % 2 == 0 else pal["mast"]
            dr.rectangle([ox + c * sq, oy + r * sq, ox + (c + 1) * sq, oy + (r + 1) * sq],
                         fill=fill)
    dr.rectangle([ox, oy, ox + sq * 8, oy + sq * 8], outline=pal["ink"], width=2)
    kx, ky = ox + sq * 4, oy + sq * 3
    icon(dr, "chess", kx + 2, ky + 2, sq * 2 - 4, pal["accent"], pal["ink"])
    dr.ellipse([ox + sq * 6 + 4, oy + sq * 5 + 4, ox + sq * 7 - 4, oy + sq * 6 - 4],
               outline=pal["accent"], width=3)


# ---------------------------------------------------------------- cards
def lead(dr, box, pal, num, region, color, ic, src, head, deck, kind):
    x, y, w, h = box
    dr.rectangle([x, y, x + w, y + h], fill=pal["card"], outline=pal["line"], width=1)
    dr.rectangle([x, y, x + 10, y + h], fill=color)
    chess_drawing(dr, x + 20, y + 10, 140, h - 20, pal)
    tx = x + 176
    dr.text((tx, y + 8), num, font=fab(16), fill=pal["accent"])
    chip = region
    cw = fab(11).getlength(chip) + 12
    dr.rectangle([tx + 30, y + 7, tx + 30 + cw, y + 25], fill=color)
    dr.text((tx + 36, y + 9), chip, font=fab(11), fill=(255, 255, 255))
    dr.text((x + w - 8 - fsr(11).getlength(src), y + 8), src, font=fsr(11), fill=pal["gray"])
    yy = y + 30
    for ln in wrap(head, fb(30), w - 192)[:2]:
        dr.text((tx, yy), ln, font=fb(30), fill=pal["ink"])
        yy += 31
    for ln in wrap(deck, fr(15), w - 192)[:2]:
        dr.text((tx, yy + 1), ln, font=fr(15), fill=pal["ink"])
        yy += 17


def mini(dr, card, box, pal):
    num, region, topic, src, head, deck, kind = card
    x, y, w, h = box
    color = REGIONS[region]
    dr.rectangle([x, y, x + w, y + h], fill=pal["card"], outline=pal["line"], width=1)
    dr.rectangle([x, y, x + 26, y + h], fill=pal["soft"])
    icon(dr, kind, x + 1, y + h / 2 - 12, 24, color, pal["ink"])
    tx = x + 34
    dr.text((tx, y + 6), str(num), font=fab(14), fill=pal["accent"])
    chip = region
    cw = fab(10).getlength(chip) + 10
    dr.rectangle([tx + 24, y + 6, tx + 24 + cw, y + 22], fill=color)
    dr.text((tx + 29, y + 8), chip, font=fab(10), fill=(255, 255, 255))
    sw = fsr(10).getlength(src)
    if tx + 24 + cw + 6 + sw <= x + w - 4:
        dr.text((x + w - 4 - sw, y + 7), src, font=fsr(10), fill=pal["gray"])
    yy = y + 24
    for ln in wrap(head, fb(24), w - 40)[:2]:
        dr.text((tx, yy), ln, font=fb(24), fill=pal["ink"])
        yy += 25
    yy = max(yy, y + 74)
    for ln in wrap(deck, fr(14), w - 40)[:2]:
        dr.text((tx, yy), ln, font=fr(14), fill=pal["ink"])
        yy += 16


# ---------------------------------------------------------------- page
def render(variant):
    pal = PALETTES[variant]
    img = Image.new("RGB", (W, H), pal["bg"])
    dr = ImageDraw.Draw(img)
    total = 13 + len(BRIEFS_L) + len(BRIEFS_R)

    # kicker + masthead + date
    kick = "%d STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026" % total
    center(dr, W / 2, 10, kick, fab(15), pal["accent"])
    dr.line([(MX, 34), (W - MX, 34)], fill=pal["ink"], width=2)
    center(dr, W / 2, 38, "THE WORLD DISPATCH", fblack(68), pal["mast"])
    dr.line([(MX, 116), (330, 116)], fill=pal["accent"], width=2)
    dr.line([(W - 330, 116), (W - MX, 116)], fill=pal["accent"], width=2)
    center(dr, W / 2, 108, "Monday 23 November 2026", fb(27), pal["ink"])

    # numbers strip
    y0 = 144
    bw = (W - 2 * MX - 5 * 8) / 6
    for i, (val, lab) in enumerate(NUMS):
        x = MX + i * (bw + 8)
        dr.rectangle([x, y0, x + bw, y0 + 44], fill=pal["soft"], outline=pal["line"])
        center(dr, x + bw / 2, y0 + 3, val, fab(22), pal["accent"])
        center(dr, x + bw / 2, y0 + 29, lab, fsr(10), pal["ink"])

    # lead + map row
    y1 = 194
    lead(dr, (MX, y1, 620, 124), pal, "1", "GLOBAL", REGIONS["GLOBAL"], "chess",
         "ObserverVoice · 23 Nov",
         "World Chess Title Draws the Crowds",
         "Fans pack the hall as the World Chess Championship grips followers across the Globe.",
         "chess")
    mx0 = MX + 632
    dr.rectangle([mx0, y1, W - MX, y1 + 124], fill=pal["card"], outline=pal["line"])
    dr.text((mx0 + 8, y1 + 4), "THE DAY ON THE MAP", font=fab(11), fill=pal["mast"])
    dotted_map(dr, mx0 + 6, y1 + 20, W - MX - mx0 - 12, 124 - 24, pal)
    dr.text((mx0 + 8, y1 + 124 - 15), LEGEND, font=fsr(10), fill=pal["gray"])

    # grid cards: 3 rows x 4
    gy = 326
    cw4 = (W - 2 * MX - 3 * 8) / 4
    for r in range(3):
        for c in range(4):
            card = grid[r * 4 + c]
            mini(dr, card, (MX + c * (cw4 + 8), gy + r * 124, cw4, 116), pal)

    # timeline
    ty = 692
    dr.line([(MX, ty), (W - MX, ty)], fill=pal["ink"], width=1)
    dr.text((MX, ty + 4), "THE DAY IN UTC", font=fab(12), fill=pal["accent"])
    tw = (W - 2 * MX) / 3
    for i, (tt, tx_) in enumerate(TL):
        cxp = MX + (i % 3) * tw
        cyp = ty + 22 + (i // 3) * 16
        dr.text((cxp, cyp), tt + " — ", font=fab(12), fill=pal["mast"])
        dr.text((cxp + fab(12).getlength(tt + " — "), cyp), tx_, font=fsr(12), fill=pal["ink"])
    dr.line([(MX, ty + 56), (W - MX, ty + 56)], fill=pal["ink"], width=1)

    # ALSO ON + DATE CHECK
    by = ty + 64
    dr.text((MX, by), "ALSO ON MONDAY", font=fab(16), fill=pal["mast"])
    dr.text((MX + fab(16).getlength("ALSO ON MONDAY") + 10, by + 3),
            "— stories 14 to 42, in brief", font=fsr(11), fill=pal["gray"])
    colw = 340
    for j, brief in enumerate(BRIEFS_L):
        yy = by + 24 + j * 13.5
        dr.text((MX, yy), "%d." % (14 + j), font=fab(13), fill=pal["accent"])
        for ln in wrap(brief, fsr(13), colw - 30)[:1]:
            dr.text((MX + 30, yy), ln, font=fsr(13), fill=pal["ink"])
    for j, brief in enumerate(BRIEFS_R):
        yy = by + 24 + j * 13.5
        x = MX + colw + 8
        dr.text((x, yy), "%d." % (29 + j), font=fab(13), fill=pal["accent"])
        for ln in wrap(brief, fsr(13), colw - 30)[:1]:
            dr.text((x + 30, yy), ln, font=fsr(13), fill=pal["ink"])

    dx = MX + 2 * colw + 16
    dr.rectangle([dx, by, W - MX, by + 224], outline=pal["accent"], width=2)
    dr.rectangle([dx, by, W - MX, by + 24], fill=pal["accent"])
    dr.text((dx + 8, by + 5), "DATE CHECK — NOT TODAY, KEPT OUT", font=fab(13),
            fill=(255, 255, 255))
    yy = by + 30
    for item in dc.split("·"):
        for ln in wrap(item.strip(), fsr(12), W - MX - dx - 16):
            dr.text((dx + 8, yy), ln, font=fsr(12), fill=pal["ink"])
            yy += 13.5
        yy += 2.5

    # footer
    center(dr, W / 2, 988,
           "Every story happened, or was first reported, on Monday 23 November 2026. "
           "Contested claims are attributed.", fsr(11), pal["ink"])
    center(dr, W / 2, 1004, "Original drawings.", fsr(11), pal["gray"])

    # light paper grain (deterministic) for print texture
    rng = random.Random(2307)
    for _ in range(2600):
        gx, gy = rng.randrange(W), rng.randrange(H)
        g = rng.randrange(228, 244)
        img.putpixel((gx, gy), (g, g, g - 4))
    return img


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g3-final7/variant%s.png" % variant
    render(variant).save(out, optimize=True)
    print("wrote", out)
