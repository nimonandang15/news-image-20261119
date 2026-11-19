#!/usr/bin/env python3
"""Render the 19 November 2026 world-news poster (1024x1024 PNG).

Draws a newspaper front page with PIL + DejaVu only. Deterministic:
same script, same bytes (PIL writes no timestamps into PNG data).
Stories verified against live reporting on 19 Nov 2026 (Reuters, AP/NPR,
NASA, Pew Research, IMD via The Hindu / live trackers).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (22, 19, 14)
RED = (200, 16, 46)
NAVY = (27, 42, 74)
TEAL = (14, 107, 107)
AMBER = (217, 142, 0)
PINK = (255, 93, 162)
CYAN = (25, 194, 216)
DARK = (16, 16, 24)
WHITE = (255, 255, 255)
GREY = (90, 84, 74)
CARD = (255, 255, 255)
GOLD = (232, 184, 32)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


FB = lambda s: font("DejaVuSans-Bold.ttf", s)      # noqa: E731
FR = lambda s: font("DejaVuSans.ttf", s)           # noqa: E731
FSB = lambda s: font("DejaVuSerif-Bold.ttf", s)    # noqa: E731


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color):
    f = FB(15)
    w = int(draw.textlength(label, font=f)) + 18
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=4, fill=color)
    draw.text((x + 9, y + 5), label, font=f, fill=WHITE)
    return w


def card(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=(214, 206, 190), width=2)


def dome(draw, cx, y, s, color):
    # simple capitol dome: semicircle + drum + columns
    draw.pieslice([cx - 34 * s, y, cx + 34 * s, y + 68 * s], 180, 360, fill=color)
    draw.rectangle([cx - 40 * s, y + 30 * s, cx + 40 * s, y + 44 * s], fill=color)
    for i in range(-3, 4):
        draw.rectangle([cx + i * 11 * s - 2 * s, y + 44 * s,
                        cx + i * 11 * s + 2 * s, y + 62 * s], fill=color)
    draw.rectangle([cx - 44 * s, y + 62 * s, cx + 44 * s, y + 68 * s], fill=color)


def spiral(draw, cx, cy, r0, color):
    for r in range(r0, 8, -8):
        a0 = r * 7 % 360
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 270,
                 fill=color, width=5)


def stars_circle(draw, cx, cy, r, n=12):
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=INK)
    d.text((36, 18), "THE WORLD IN ONE DAY", font=FSB(56), fill=WHITE)
    d.rectangle([36, 96, 36 + 470, 100], fill=RED)
    d.text((36, 108), "THURSDAY  19  NOVEMBER  2026",
           font=FB(26), fill=(255, 214, 64))
    d.text((660, 104), "SIX STORIES THAT", font=FB(20), fill=(200, 198, 190))
    d.text((660, 128), "DEFINED THE DAY", font=FB(20), fill=(200, 198, 190))
    d.rectangle([0, 148, W, 154], fill=RED)

    # ---- lead story: GTA VI ----
    d.rounded_rectangle([28, 172, 996, 452], radius=12, fill=DARK)
    # neon skyline
    for i, (bx, bw, bh, c) in enumerate([
            (52, 46, 120, PINK), (112, 34, 170, CYAN), (160, 52, 100, PINK),
            (226, 30, 150, (255, 214, 64)), (270, 44, 190, CYAN),
            (328, 36, 120, PINK), (378, 48, 160, (255, 214, 64))]):
        d.rectangle([bx, 430 - bh, bx + bw, 430], fill=c)
    d.text((470, 196), "CULTURE  •  LEAD STORY", font=FB(17), fill=PINK)
    d.text((470, 224), "VICE CITY OPENS", font=FSB(46), fill=WHITE)
    d.text((470, 292), "Grand Theft Auto VI launches\nworldwide today — the first\nnew GTA in 13 years.",
           font=FB(26), fill=(235, 235, 235))
    d.text((470, 392), "$79.99  •  PS5 & Xbox Series X|S  •  midnight local time",
           font=FR(18), fill=(180, 178, 170))
    d.text((52, 436), "", font=FR(12), fill=WHITE)

    # ---- row 1: Jeffries | EU loan ----
    y1, ch = 470, 188
    card(d, 28, y1, 474, ch)
    kicker(d, 48, y1 + 16, "UNITED STATES", NAVY)
    d.text((48, y1 + 52), "Jeffries nominated\nfor Speaker", font=FSB(30), fill=INK)
    text_block(d, 48, y1 + 126, "House Democrats pick Jeffries "
               "251–11. He would be the first Black Speaker; "
               "the full House votes 3 Jan.", FR(17), INK, 330, 22)
    dome(d, 420, y1 + 96, 1.0, NAVY)

    card(d, 522, y1, 474, ch)
    kicker(d, 542, y1 + 16, "EUROPE", (0, 51, 153))
    d.text((542, y1 + 52), "EU offers Ukraine\na €45bn loan", font=FSB(30), fill=INK)
    text_block(d, 542, y1 + 126, "Brussels offers a loan for "
               "two-thirds of Kyiv's €70bn 2027 gap — repaid "
               "only if Russia pays reparations.", FR(17), INK, 330, 22)
    d.ellipse([888, y1 + 84, 972, y1 + 168], fill=(0, 51, 153))
    stars_circle(d, 930, y1 + 126, 30)
    d.text((906, y1 + 112), "€", font=FB(26), fill=GOLD)

    # ---- row 2: Cyclone Akvan | Voyager 1 ----
    y2 = 676
    card(d, 28, y2, 474, ch)
    kicker(d, 48, y2 + 16, "INDIA  •  WEATHER", TEAL)
    d.text((48, y2 + 52), "Cyclone Akvan\nbears down", font=FSB(30), fill=INK)
    text_block(d, 48, y2 + 126, "Severe storm in the Bay of Bengal. "
               "Red alert in seven Andhra districts today; "
               "landfall due 20 Nov.", FR(17), INK, 330, 22)
    spiral(d, 420, y2 + 130, 44, TEAL)

    card(d, 522, y2, 474, ch)
    kicker(d, 542, y2 + 16, "SPACE", (60, 20, 80))
    d.text((542, y2 + 52), "Voyager 1, one\nlight-day away", font=FSB(30), fill=INK)
    text_block(d, 542, y2 + 126, "NASA confirms today: the 1977 probe "
               "is 16.1bn miles out — the first object a full "
               "light-day away.", FR(17), INK, 330, 22)
    d.ellipse([884, y2 + 82, 976, y2 + 174], fill=DARK)
    for i in range(6):
        x = 896 + i * 13
        d.ellipse([x, y2 + 122 + (i % 2) * 8, x + 4, y2 + 126 + (i % 2) * 8],
                  fill=(200, 198, 190))
    d.ellipse([962, y2 + 112, 972, y2 + 122], fill=GOLD)

    # ---- bottom strip: Pew ----
    y3 = 884
    d.rounded_rectangle([28, y3, 996, 986], radius=10, fill=(232, 222, 200))
    kicker(d, 48, y3 + 14, "WORLD  •  DEMOGRAPHICS", (120, 60, 10))
    d.text((48, y3 + 46), "Pew: Islam to be the world's", font=FSB(20), fill=INK)
    d.text((48, y3 + 72), "largest faith by 2035", font=FSB(20), fill=INK)
    # bars: Muslims 2.57bn vs Christians 2.52bn
    d.text((620, y3 + 16), "2.57bn Muslims", font=FB(16), fill=TEAL)
    d.rectangle([620, y3 + 38, 620 + 300, y3 + 52], fill=TEAL)
    d.text((620, y3 + 56), "2.52bn Christians", font=FB(16), fill=GREY)
    d.rectangle([620, y3 + 78, 620 + 294, y3 + 92], fill=GREY)

    # ---- footer ----
    d.text((36, 996), "Sources: Reuters  •  AP / NPR  •  NASA  •  Pew Research Center  •  India Meteorological Department",
           font=FR(13), fill=GREY)
    d.text((36, 1012), "", font=FR(12), fill=GREY)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
