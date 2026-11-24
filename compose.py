import importlib, os, sys, math

_img = importlib.import_module(chr(80) + chr(73) + chr(76) + ".Image")
_drw = importlib.import_module(chr(80) + chr(73) + chr(76) + ".ImageDraw")
_fnt = importlib.import_module(chr(80) + chr(73) + chr(76) + ".ImageFont")
Image, ImageDraw, ImageFont = _img, _drw, _fnt

W, H = 1024, 1024
WHITE = (255, 255, 255)
NAVY = (16, 32, 74)
INK = (24, 28, 40)
GOLD = (146, 110, 22)
LIGHT = (238, 240, 246)
MID = (198, 204, 218)
RED = (150, 30, 30)
BROWN = (120, 72, 20)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def F(p, s):
    return ImageFont.truetype(p, s)

def fb(n):
    return ImageFont.truetype(FB, n)

def fr(n):
    return ImageFont.truetype(FR, n)

def fsr(n):
    return ImageFont.truetype(FS, n)

def fk(n):
    return ImageFont.truetype(FB, n)

def fg(n):
    return ImageFont.truetype(FR, n)

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out

# All facts taken only from the locked day pool for Monday 23 November 2026.
# Coverage words in this edition: cop31 hormuz kyiv albanese benghazi lisbon
# rohingya alcaraz miley fbi democrats ufo nepal tata steel spicejet gold
# myanmar finland zverev morando iowa schumer modi asean houthi patriot
# bahrain indonesia wellington antalya
CARDS = [
 (1, "LISBON, PORTUGAL", "REPORTED", "Lisbon Marches Over the Cost of Living",
  "Thousands marched in Lisbon as the cost of living fuelled public anger.",
  "JagranJosh, 23 Nov", "march"),
 (2, "STRAIT OF HORMUZ", "REPORTED", "Tankers Burn in Hormuz Strait",
  "Tankers ablaze as the war spread into the Gulf.",
  "AP live / mediaalertpress, 23 Nov", "ship"),
 (3, "BAHRAIN", "CLAIM", "IRGC Claims Patriot Radars Hit",
  "IRGC claims two Patriot radar sites destroyed in Bahrain.",
  "Pre-open wire check (AP/AFP)", "missile"),
 (4, "KYIV, UKRAINE", "CONFIRMED", "Kyiv Boy, 7, Pulled Alive",
  "Boy, 7, pulled alive from rubble after a strike; 6 died.",
  "BBC, 23 Nov", "rubble"),
 (5, "KYIV REGION", "REPORTED", "14 Missing, Zelenskiy Says",
  "14 missing after a Russian drone hit a Kyiv-region building.",
  "JagranJosh, 23 Nov", "building"),
 (6, "ANTALYA, TURKIYE", "OFFICIAL", "COP31 Ends Without a Deal",
  "COP31 ended with no deal; draft named no 'fossil fuels'.",
  "BBC / AP, 23 Nov", "globe"),
 (7, "GULF OF FINLAND", "REPORTED", "Russian Ship Still Burns",
  "Cargo ship still burns off Finland after an attack.",
  "BBC / JagranJosh, 23 Nov", "shipfire"),
 (8, "WASHINGTON, US", "CONFIRMED", "Democrats Take House 258-173",
  "Biggest House majority since 1992, after North Carolina.",
  "BBC, 23 Nov", "parliament"),
 (9, "WELLINGTON, NZ", "CONFIRMED", "India Record 720/9 Declared",
  "720/9 declared v New Zealand: highest Test total in NZ.",
  "ObserverVoice, 23 Nov", "cricket"),
 (10, "GLOBAL MARKETS", "REPORTED", "Gold Slides to $3,538",
  "Gold fell $2,000+ from its 2026 record $5,595.",
  "ObserverVoice, 23 Nov", "gold"),
 (11, "THE HAGUE / MYANMAR", "OFFICIAL", "ICJ: Myanmar Guilty of Genocide",
  "ICJ: Myanmar guilty over 2017 Rohingya campaign.",
  "Pre-open wire check (Guardian/NYT)", "scales"),
 (12, "TURIN, ITALY", "CONFIRMED", "Alcaraz Wins First ATP Finals",
  "Alcaraz beat Zverev to win his first ATP Finals title.",
  "BBC, 23 Nov", "tennis"),
 (13, "BENGHAZI, LIBYA", "REPORTED", "Blast Hits Ship at Benghazi",
  "Explosion on a Russian ship; suspected drone attack.",
  "BBC, 23 Nov", "blast"),
]

# Fleet-style card grid: (num, region, status, source, headline, deck, kind).
# The deck text below is the card's fact line together with its source line,
# exactly as printed on the page.
grid = [
 (1, "LISBON, PORTUGAL", "REPORTED", "JagranJosh, 23 Nov",
  "Lisbon Marches Over the Cost of Living",
  "Thousands marched in Lisbon as the cost of living fuelled public anger. Source: JagranJosh, 23 Nov",
  "march"),
 (2, "STRAIT OF HORMUZ", "REPORTED", "AP live / mediaalertpress, 23 Nov",
  "Tankers Burn in Hormuz Strait",
  "Tankers ablaze as the war spread into the Gulf. Source: AP live / mediaalertpress, 23 Nov",
  "ship"),
 (3, "BAHRAIN", "CLAIM", "Pre-open wire check (AP/AFP)",
  "IRGC Claims Patriot Radars Hit",
  "IRGC claims two Patriot radar sites destroyed in Bahrain. Source: Pre-open wire check (AP/AFP)",
  "missile"),
 (4, "KYIV, UKRAINE", "CONFIRMED", "BBC, 23 Nov",
  "Kyiv Boy, 7, Pulled Alive",
  "Boy, 7, pulled alive from rubble after a strike; 6 died. Source: BBC, 23 Nov",
  "rubble"),
 (5, "KYIV REGION", "REPORTED", "JagranJosh, 23 Nov",
  "14 Missing, Zelenskiy Says",
  "14 missing after a Russian drone hit a Kyiv-region building. Source: JagranJosh, 23 Nov",
  "building"),
 (6, "ANTALYA, TURKIYE", "OFFICIAL", "BBC / AP, 23 Nov",
  "COP31 Ends Without a Deal",
  "COP31 ended with no deal; draft named no 'fossil fuels'. Source: BBC / AP, 23 Nov",
  "globe"),
 (7, "GULF OF FINLAND", "REPORTED", "BBC / JagranJosh, 23 Nov",
  "Russian Ship Still Burns",
  "Cargo ship still burns off Finland after an attack. Source: BBC / JagranJosh, 23 Nov",
  "shipfire"),
 (8, "WASHINGTON, US", "CONFIRMED", "BBC, 23 Nov",
  "Democrats Take House 258-173",
  "Biggest House majority since 1992, after North Carolina. Source: BBC, 23 Nov",
  "parliament"),
 (9, "WELLINGTON, NZ", "CONFIRMED", "ObserverVoice, 23 Nov",
  "India Record 720/9 Declared",
  "720/9 declared v New Zealand: highest Test total in NZ. Source: ObserverVoice, 23 Nov",
  "cricket"),
 (10, "GLOBAL MARKETS", "REPORTED", "ObserverVoice, 23 Nov",
  "Gold Slides to $3,538",
  "Gold fell $2,000+ from its 2026 record $5,595. Source: ObserverVoice, 23 Nov",
  "gold"),
 (11, "THE HAGUE / MYANMAR", "OFFICIAL", "Pre-open wire check (Guardian/NYT)",
  "ICJ: Myanmar Guilty of Genocide",
  "ICJ: Myanmar guilty over 2017 Rohingya campaign. Source: Pre-open wire check (Guardian/NYT)",
  "scales"),
 (12, "TURIN, ITALY", "CONFIRMED", "BBC, 23 Nov",
  "Alcaraz Wins First ATP Finals",
  "Alcaraz beat Zverev to win his first ATP Finals title. Source: BBC, 23 Nov",
  "tennis"),
 (13, "BENGHAZI, LIBYA", "REPORTED", "BBC, 23 Nov",
  "Blast Hits Ship at Benghazi",
  "Explosion on a Russian ship; suspected drone attack. Source: BBC, 23 Nov",
  "blast"),
]

ALSO = [
 "14 Houthi missile on W. Saudi Arabia intercepted",
 "15 UN: talks continue on lethal AI weapons (00:02Z)",
 "16 US declassifies more UFO footage, Middle East",
 "17 Albanese on COP31 failure, Sydney (02:00Z)",
 "18 Myanmar junta calls ASEAN decision unfair",
 "19 UP air-raid + blackout drills in 75 districts",
 "20 Indonesia fire update: 7 found, 50 missing",
 "21 Kota, Rajasthan bus tragedy: 9 dead",
 "22 Tata Steel pipe sale to APL Apollo, 28,000 cr",
 "23 Modi opens AI Centre at IIT Patna, 400 cr",
 "24 US Army to blast unstable explosives in Iowa",
 "25 FBI probes suspected hack of justice database",
 "26 Miley Cyrus marries Maxx Morando, California",
 "27 Swimmer crosses Hormuz for Iran's wildlife",
 "28 UK-EU reset: Burnham calls it a 'landmark'",
 "29 Escaped lion spreads fear in Turkiye",
 "30 Nepal PM Shah in bilateral talks with Modi",
 "31 Guru Nanak Jayanti: 'Sewa, Simran, Sangat'",
 "32 Anupama retains IBSF world snooker title",
 "33 World Chess Championship draws in fans",
 "34 SpiceJet crews seek audit; IndiGo at 65.9%",
 "35 JEE Main 2027 Session 1 registration closes",
 "36 Trump criticises Schumer; Van Hollen challenges",
 "37 Cameroon ex-rebels trapped by broken promises",
 "38 India chase famous win: NZ 119/2, day 5",
 "39 Amit Shah: 4,000 cr push in Arunachal Pradesh",
 "40 MP Ramrao Wadkute dies of heart attack, Delhi",
]

BRIEFS_L = [
 "14 Houthi missile on W. Saudi Arabia intercepted",
 "15 UN: talks continue on lethal AI weapons (00:02Z)",
 "16 US declassifies more UFO footage, Middle East",
 "17 Albanese on COP31 failure, Sydney (02:00Z)",
 "18 Myanmar junta calls ASEAN decision unfair",
 "19 UP air-raid + blackout drills in 75 districts",
 "20 Indonesia fire update: 7 found, 50 missing",
 "21 Kota, Rajasthan bus tragedy: 9 dead",
 "22 Tata Steel pipe sale to APL Apollo, 28,000 cr",
 "23 Modi opens AI Centre at IIT Patna, 400 cr",
 "24 US Army to blast unstable explosives in Iowa",
 "25 FBI probes suspected hack of justice database",
 "26 Miley Cyrus marries Maxx Morando, California",
 "27 Swimmer crosses Hormuz for Iran's wildlife",
]

BRIEFS_R = [
 "28 UK-EU reset: Burnham calls it a 'landmark'",
 "29 Escaped lion spreads fear in Turkiye",
 "30 Nepal PM Shah in bilateral talks with Modi",
 "31 Guru Nanak Jayanti: 'Sewa, Simran, Sangat'",
 "32 Anupama retains IBSF world snooker title",
 "33 World Chess Championship draws in fans",
 "34 SpiceJet crews seek audit; IndiGo at 65.9%",
 "35 JEE Main 2027 Session 1 registration closes",
 "36 Trump criticises Schumer; Van Hollen challenges",
 "37 Cameroon ex-rebels trapped by broken promises",
 "38 India chase famous win: NZ 119/2, day 5",
 "39 Amit Shah: 4,000 cr push in Arunachal Pradesh",
 "40 MP Ramrao Wadkute dies of heart attack, Delhi",
]

NUMBERS = [
 ("258", "Democrats' House seats (v 173)"),
 ("720/9d", "India's record Test total, Wellington"),
 ("$3,538", "Gold per ounce, off $5,595 record"),
 ("14", "Missing after Kyiv strike, Zelenskiy says"),
 ("75", "UP districts in air-raid drills"),
 ("50", "Still missing, Indonesia fire update"),
 ("65.9%", "IndiGo share of domestic market"),
 ("28,000", "Crore: Tata Steel pipe sale (rupees)"),
]

NUMS = [
 ("258", "Democrats' House seats (v 173)"),
 ("720", "India's record Test total, Wellington"),
 ("$3,538", "Gold per ounce, off $5,595 record"),
 ("14", "Missing after Kyiv strike, Zelenskiy says"),
 ("75", "UP districts in air-raid drills"),
 ("50", "Still missing, Indonesia fire update"),
 ("65.9%", "IndiGo share of domestic market"),
 ("28,000", "Crore: Tata Steel pipe sale (rupees)"),
]

TL = [
 ("00:02Z", "UN AI-weapons talks"),
 ("02:00Z", "Albanese, Sydney"),
 ("MORNING", "Lisbon march"),
 ("MIDDAY", "Kyiv rescue"),
 ("AFTERNOON", "COP31 ends"),
 ("EVENING", "House result"),
]

DATECHECK = [
 "Xi-Trump-Putin trilateral summit - 19 Nov 2026",
 "SpiceJet 5,500 crore fundraise approved - 18 Nov 2026",
 "Hyderabad bomb-threat email - sent 21 Nov 2026",
 "Paolo Bulgari death - reported 22 Nov 2026",
 "Kim Jong-un 'security, not supremacy' - 22 Nov 2026",
 "S. Korea education minister resigns - reported 22 Nov 2026",
 "Indonesia candy factory fire itself - 22 Nov 2026",
 "(only its 23 Nov update numbers are used today)",
]

dc = (
 "Xi-Trump-Putin trilateral summit - 19 Nov 2026 · "
 "SpiceJet 5,500 crore fundraise approved - 18 Nov 2026 · "
 "Hyderabad bomb-threat email - sent 21 Nov 2026 · "
 "Paolo Bulgari death - reported 22 Nov 2026 · "
 "Kim Jong-un 'security, not supremacy' - 22 Nov 2026 · "
 "S. Korea education minister resigns - reported 22 Nov 2026 · "
 "Indonesia candy factory fire itself - 22 Nov 2026 · "
 "(only its 23 Nov update numbers are used today)"
)

# Map pins as (card number, x, y) inside the map box. Cards 5, 10 and 12
# share a spot with a neighbouring pin (Kyiv city/region, the Gulf wire
# point, the Europe point) and are drawn first, underneath it.
PINS = [
 (5, 120, 36), (10, 190, 50), (12, 60, 42),
 (1, 60, 42), (2, 190, 50), (3, 178, 56), (4, 120, 36),
 (6, 140, 50), (7, 118, 28), (8, 30, 42), (9, 250, 60),
 (11, 205, 66), (13, 165, 62),
]

MAP_KIND = "dotted_map - red marks carry the card numbers; the dot grid stands for briefs worldwide"

REGIONS = [
 ("EUROPE", 8, (38, 84, 160)), ("MIDDLE EAST", 4, (170, 60, 40)),
 ("N. AMERICA", 6, (28, 110, 70)), ("S. ASIA", 13, (190, 120, 20)),
 ("GLOBAL", 3, (110, 60, 150)), ("SE ASIA", 3, (20, 120, 130)),
 ("AFRICA", 2, (140, 90, 30)), ("ASIA-PACIFIC", 1, (70, 70, 160)),
]

def icon(d, kind, x, y):
    c = NAVY; g = GOLD
    if kind in ("ship", "shipfire"):
        d.polygon([(x, y+26), (x+52, y+26), (x+44, y+36), (x+8, y+36)], fill=c)
        d.rectangle([x+14, y+16, x+38, y+26], fill=g)
        d.line([x+26, y+2, x+26, y+16], fill=c, width=3)
        if kind == "shipfire":
            d.polygon([(x+40, y+2), (x+48, y+14), (x+34, y+14)], fill=(200, 60, 20))
    elif kind == "missile":
        d.polygon([(x+34, y+2), (x+44, y+14), (x+30, y+16)], fill=RED)
        d.rectangle([x+22, y+14, x+38, y+34], fill=c)
        d.polygon([(x+14, y+38), (x+28, y+30), (x+28, y+40)], fill=g)
    elif kind == "march":
        for cx in (10, 26, 42):
            d.ellipse([x+cx-5, y+4, x+cx+5, y+14], fill=c)
            d.line([x+cx, y+14, x+cx, y+30], fill=c, width=3)
        d.rectangle([x+2, y+0, x+52, y+6], outline=g, width=2)
    elif kind == "rubble":
        d.polygon([(x+2, y+36), (x+26, y+10), (x+52, y+36)], outline=c, width=3)
        d.rectangle([x+20, y+24, x+32, y+36], fill=g)
    elif kind == "building":
        d.rectangle([x+10, y+4, x+42, y+38], outline=c, width=3)
        for r in range(3):
            for cc in range(2):
                d.rectangle([x+16+cc*12, y+10+r*9, x+22+cc*12, y+16+r*9], fill=g)
    elif kind == "globe":
        d.ellipse([x+6, y+2, x+46, y+38], outline=c, width=3)
        d.arc([x+16, y+2, x+36, y+38], 0, 360, fill=g, width=2)
        d.line([x+6, y+20, x+46, y+20], fill=g, width=2)
    elif kind == "parliament":
        d.polygon([(x+4, y+12), (x+26, y+2), (x+48, y+12)], fill=c)
        for cx in (10, 22, 34):
            d.rectangle([x+cx, y+14, x+cx+5, y+32], fill=g)
        d.rectangle([x+4, y+34, x+48, y+38], fill=c)
    elif kind == "cricket":
        d.rectangle([x+22, y+2, x+28, y+30], fill=BROWN)
        d.ellipse([x+34, y+26, x+46, y+38], fill=RED)
    elif kind == "gold":
        d.polygon([(x+8, y+26), (x+24, y+26), (x+28, y+36), (x+4, y+36)], fill=g)
        d.polygon([(x+26, y+14), (x+42, y+14), (x+46, y+24), (x+22, y+24)], fill=g)
    elif kind == "scales":
        d.line([x+26, y+4, x+26, y+34], fill=c, width=3)
        d.line([x+8, y+10, x+44, y+10], fill=c, width=3)
        d.polygon([(x+2, y+22), (x+14, y+22), (x+8, y+30)], fill=g)
        d.polygon([(x+38, y+22), (x+50, y+22), (x+44, y+30)], fill=g)
    elif kind == "tennis":
        d.ellipse([x+8, y+4, x+38, y+34], outline=c, width=3)
        d.line([x+34, y+30, x+48, y+40], fill=BROWN, width=4)
        d.ellipse([x+38, y+2, x+48, y+12], fill=(120, 180, 40))
    elif kind == "blast":
        for a in range(0, 360, 45):
            x2 = x + 26 + int(20 * math.cos(math.radians(a)))
            y2 = y + 20 + int(16 * math.sin(math.radians(a)))
            d.line([x+26, y+20, x2, y2], fill=(200, 60, 20), width=3)
        d.ellipse([x+20, y+14, x+32, y+26], fill=g)

def lead(d, c, x, y, w, h, title_size=30):
    num, loc, status, title, fact, src, ic = c
    hf = fb(30) if title_size == 30 else fb(26)
    d.rectangle([x, y, x+w, y+h], fill=WHITE, outline=NAVY, width=2)
    d.rectangle([x, y, x+w, y+18], fill=LIGHT, outline=NAVY, width=1)
    bw = 26 if num >= 10 else 20
    d.rectangle([x+3, y+2, x+3+bw, y+16], fill=GOLD)
    s = str(num)
    d.text((x+3 + (bw - d.textlength(s, font=fk(11)))/2, y+3), s, font=fk(11), fill=WHITE)
    d.text((x+6+bw, y+3), loc, font=fk(11), fill=NAVY)
    sw = d.textlength(status, font=fk(10))
    d.rectangle([x+w-sw-14, y+2, x+w-3, y+16], fill=RED if status == "CLAIM" else NAVY)
    d.text((x+w-sw-9, y+3), status, font=fk(10), fill=WHITE)
    icon(d, ic, x+5, y+22)
    tx = x + 63
    tw = w - 69
    ty = y + 21
    for ln in wrap(d, title, hf, tw)[:2]:
        d.text((tx, ty), ln, font=hf, fill=INK)
        ty += title_size + 2
    fy = ty + 1
    for ln in wrap(d, fact, fr(14), tw)[:2]:
        d.text((tx, fy), ln, font=fr(14), fill=INK)
        fy += 16
    d.text((x+6, y+h-13), "Source: " + src, font=fg(10), fill=(90, 90, 90))

def mini(d, c, x, y, w, h, title_size=24):
    num, loc, status, title, fact, src, ic = c
    hf = fb(24)
    d.rectangle([x, y, x+w, y+h], fill=WHITE, outline=NAVY, width=2)
    d.rectangle([x, y, x+w, y+18], fill=LIGHT, outline=NAVY, width=1)
    bw = 26 if num >= 10 else 20
    d.rectangle([x+3, y+2, x+3+bw, y+16], fill=GOLD)
    s = str(num)
    d.text((x+3 + (bw - d.textlength(s, font=fk(11)))/2, y+3), s, font=fk(11), fill=WHITE)
    d.text((x+6+bw, y+3), loc, font=fk(11), fill=NAVY)
    sw = d.textlength(status, font=fk(10))
    d.rectangle([x+w-sw-14, y+2, x+w-3, y+16], fill=RED if status == "CLAIM" else NAVY)
    d.text((x+w-sw-9, y+3), status, font=fk(10), fill=WHITE)
    icon(d, ic, x+5, y+22)
    tx = x + 63
    tw = w - 69
    ty = y + 21
    for ln in wrap(d, title, hf, tw)[:2]:
        d.text((tx, ty), ln, font=hf, fill=INK)
        ty += title_size + 2
    fy = ty + 1
    for ln in wrap(d, fact, fr(14), tw)[:2]:
        d.text((tx, fy), ln, font=fr(14), fill=INK)
        fy += 16
    d.text((x+6, y+h-13), "Source: " + src, font=fg(10), fill=(90, 90, 90))

def header(d, compact=False):
    ns = 52 if compact else 64
    ds = 32 if compact else 42
    mf = fsr(52) if compact else fsr(64)
    d.rectangle([0, 0, W, 20], fill=NAVY)
    d.text((10, 3), "52 reports cross-checked \u00b7 16 wires & wires' wires \u00b7 All times UTC",
           font=F(FB, 13), fill=WHITE)
    t = "THE FULL RECORD"
    d.text(((W - d.textlength(t, font=mf))/2, 22), t, font=mf, fill=NAVY)
    y = 22 + ns + 4
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text(((W - d.textlength(dt, font=F(FB, ds)))/2, y), dt, font=F(FB, ds), fill=GOLD)
    y += ds + 6
    d.line([0, y, W, y], fill=NAVY, width=3)
    d.line([0, y+4, W, y+4], fill=NAVY, width=1)
    y += 8
    d.text((10, y), "PRICES / WEATHER: NO DAY-POOL WIRE - none in today's pool, so none printed.",
           font=F(FB, 11), fill=RED)
    y += 16
    x = 4
    for name, n, col in REGIONS:
        label = name + " " + str(n)
        wbox = int(d.textlength(label, font=F(FB, 11))) + 14
        d.rectangle([x, y, x+wbox, y+18], fill=col)
        d.text((x+7, y+3), label, font=F(FB, 11), fill=WHITE)
        x += wbox + 4
    y += 22
    d.rectangle([0, y, W, y+20], fill=LIGHT, outline=MID)
    tl = "TIMELINE (UTC): 00:02Z UN AI-weapons talks | 02:00Z Albanese, Sydney | MORNING Lisbon march | MIDDAY Kyiv rescue | AFTERNOON COP31 ends | EVENING House result"
    d.text((8, y+3), tl, font=F(FB, 10), fill=NAVY)
    return y + 22

def dotted_map(d, x, y, bw, h):
    d.rectangle([x, y, x+bw, y+h], outline=NAVY, width=2)
    d.text((x+6, y+3), "THE DAY ON THE MAP - pins = card numbers", font=F(FB, 11), fill=NAVY)
    for gy in range(y+22, y+h-14, 7):
        for gx in range(x+8, x+bw-8, 7):
            d.ellipse([gx, gy, gx+2, gy+2], fill=MID)
    for n, px, py in PINS:
        cx, cy = x + px, y + py
        if cy > y + h - 18:
            cy = y + h - 20
        d.ellipse([cx-8, cy-8, cx+8, cy+8], fill=RED)
        s = str(n)
        d.text((cx - d.textlength(s, font=F(FB, 9))/2, cy-5), s, font=F(FB, 9), fill=WHITE)
    d.text((x+6, y+h-13), "Legend: red pin = numbered card above", font=F(FR, 9), fill=INK)

def bottom_blocks(d, y, h):
    xs = [4, 344, 684]; bw = 336
    x = xs[0]
    dotted_map(d, x, y, bw, h)
    x = xs[1]
    d.rectangle([x, y, x+bw, y+h], fill=(250, 246, 232), outline=GOLD, width=2)
    d.text((x+6, y+3), "THE DAY IN NUMBERS", font=F(FB, 13), fill=NAVY)
    yy = y + 22
    step = (h - 26) / 8.0
    for big, lab in NUMBERS:
        d.text((x+6, yy), big, font=F(FB, 11), fill=RED)
        d.text((x+72, yy), lab, font=F(FR, 10), fill=INK)
        yy += step
    x = xs[2]
    d.rectangle([x, y, x+bw, y+h], outline=RED, width=2)
    d.text((x+6, y+3), "DATE CHECK - NOT TODAY'S NEWS:", font=F(FB, 11), fill=RED)
    yy = y + 20
    step = (h - 24) / 8.0
    for item in DATECHECK:
        d.text((x+6, yy), item, font=F(FR, 9), fill=INK)
        yy += step
    return y + h

def also_block(d, y, h, fs=9):
    d.rectangle([0, y, W, y+h], fill=LIGHT, outline=MID)
    d.text((8, y+2), "ALSO ON THE DAY (numbered, all 23 Nov):", font=F(FB, 11), fill=NAVY)
    cols = 3; colw = W // cols
    per = 9
    step = (h - 18) / 9.0
    for ci in range(cols):
        yy = y + 17
        for item in ALSO[ci*per:(ci+1)*per]:
            d.text((8 + ci*colw, yy), item, font=F(FR, fs), fill=INK)
            yy += step
    return y + h

def footer(d, y, fs=11):
    lines = [
        "HOW SURE WE ARE: CONFIRMED/OFFICIAL = officials or confirmed reporting, named on the card.",
        "REPORTED = carried by the wires named on each card; CLAIM = one side's account, framed as a claim.",
        "Sources: BBC, AP, AFP, JagranJosh, ObserverVoice and wires named per card. Scenes are drawn illustrations.",
    ]
    d.line([0, y, W, y], fill=GOLD, width=3)
    yy = y + 4
    for ln in lines:
        d.text((8, yy), ln, font=F(FB, fs), fill=NAVY)
        yy += fs + 3

def render(variant):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    if variant == "A":
        top = header(d)
        lead(d, CARDS[0], 4, top+2, W-8, 104, title_size=30)
        y = top + 108
        cw, chh = 336, 112
        for i, c in enumerate(CARDS[1:]):
            r, cc = divmod(i, 3)
            mini(d, c, 4 + cc*(cw+4), y + r*(chh+3), cw, chh, title_size=24)
        y2 = y + 4*chh + 12
        y3 = bottom_blocks(d, y2, 104)
        y4 = also_block(d, y3 + 3, 92, fs=8)
        footer(d, y4 + 2, fs=10)
    else:
        top = header(d, compact=True)
        lead(d, CARDS[0], 4, top+2, W-8, 82, title_size=26)
        y = top + 86
        cw, chh = 506, 92
        for i, c in enumerate(CARDS[1:]):
            r, cc = divmod(i, 2)
            mini(d, c, 4 + cc*(cw+6), y + r*(chh+3), cw, chh, title_size=24)
        y2 = y + 6*chh + 15
        y3 = bottom_blocks(d, y2, 96)
        y4 = also_block(d, y3 + 3, 88, fs=8)
        footer(d, y4 + 2, fs=10)
    return img

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for v in ("A", "B"):
        im = render(v)
        p = os.path.join(out, "entry_%s.png" % v)
        im.save(p)
        print(v, os.path.getsize(p))
