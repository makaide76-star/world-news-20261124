#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Tuesday 24 November 2026.

Build-time only: uses Pillow (locally installed) and DejaVu fonts to draw
a 1024x1024 newspaper front page and writes assets/entry.png. The entry
program (main.py) is stdlib-only and merely copies that image.

Text fitting is enforced: every headline must wrap to one line and every
story body to at most two lines at the sizes used; the script raises
instead of painting over text.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (248, 244, 233)
INK = (28, 36, 51)
NAVY = (27, 42, 74)
GOLD = (201, 162, 39)
RED = (180, 35, 24)
TEAL = (46, 110, 142)
SKY = (169, 198, 222)
OCEAN = (47, 111, 168)
LAND = (91, 168, 91)
GRAY = (90, 90, 85)
LIGHT = (232, 226, 210)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
ORANGE = (214, 120, 40)
DARKGREEN = (0, 106, 78)
BROWN = (120, 72, 20)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real text measurement."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if draw.textlength(trial, font=fnt) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw, x, y, text, fnt, max_width, fill, leading):
    """Draw a wrapped paragraph; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------- pictograms
# Each draws a small flat pictogram inside a 56x56 box at (x, y).

def pic_satellite(d, x, y):
    # satellite: body, gold panels, orbit ring
    d.ellipse([x + 4, y + 4, x + 52, y + 52], outline=GRAY, width=2)
    d.rectangle([x + 8, y + 22, x + 20, y + 34], fill=NAVY)
    d.rectangle([x + 36, y + 22, x + 48, y + 34], fill=NAVY)
    d.rectangle([x + 22, y + 20, x + 34, y + 36], fill=INK)
    d.rectangle([x + 25, y + 24, x + 31, y + 30], fill=GOLD)
    d.line([x + 22, y + 28, x + 8, y + 28], fill=INK, width=2)
    d.line([x + 34, y + 28, x + 48, y + 28], fill=INK, width=2)
    d.ellipse([x + 24, y + 8, x + 32, y + 16], fill=RED)


def pic_memorial(d, x, y):
    # candle with flame beside a small cross
    d.rectangle([x + 8, y + 18, x + 16, y + 48], fill=WHITE, outline=GRAY)
    d.ellipse([x + 9, y + 6, x + 15, y + 16], fill=ORANGE)
    d.rectangle([x + 6, y + 48, x + 18, y + 52], fill=GOLD)
    d.rectangle([x + 34, y + 10, x + 40, y + 48], fill=INK)
    d.rectangle([x + 26, y + 18, x + 48, y + 24], fill=INK)
    d.rectangle([x + 32, y + 48, x + 42, y + 52], fill=INK)


def pic_estonia(d, x, y):
    # Estonian flag: blue, black, white horizontal stripes
    d.rectangle([x + 4, y + 12, x + 6, y + 50], fill=INK)
    d.rectangle([x + 7, y + 12, x + 50, y + 24], fill=(0, 114, 206))
    d.rectangle([x + 7, y + 24, x + 50, y + 36], fill=(0, 0, 0))
    d.rectangle([x + 7, y + 36, x + 50, y + 48], fill=WHITE, outline=GRAY)


def pic_siren(d, x, y):
    # warning triangle with exclamation and sound arcs
    d.polygon([(x + 28, y + 6), (x + 52, y + 48), (x + 4, y + 48)], fill=(255, 200, 0),
              outline=RED)
    d.rectangle([x + 26, y + 20, x + 30, y + 36], fill=RED)
    d.rectangle([x + 26, y + 40, x + 30, y + 44], fill=RED)
    d.arc([x + 44, y + 14, x + 54, y + 42], start=300, end=60, fill=RED, width=2)


def pic_bangladesh(d, x, y):
    # Bangladeshi flag: green field, red disc
    d.rectangle([x + 4, y + 12, x + 6, y + 50], fill=INK)
    d.rectangle([x + 7, y + 12, x + 50, y + 48], fill=DARKGREEN)
    d.ellipse([x + 20, y + 20, x + 38, y + 40], fill=RED)


def pic_gavel(d, x, y):
    # judge's gavel and sound block
    d.rectangle([x + 10, y + 10, x + 34, y + 22], fill=BROWN)
    d.rectangle([x + 30, y + 20, x + 50, y + 46], fill=(150, 100, 40))
    d.rectangle([x + 6, y + 46, x + 34, y + 52], fill=INK)


def pic_ball(d, x, y):
    # soccer ball
    d.ellipse([x + 6, y + 6, x + 50, y + 50], fill=WHITE, outline=INK, width=2)
    d.polygon([(x + 28, y + 20), (x + 36, y + 26), (x + 33, y + 36),
               (x + 23, y + 36), (x + 20, y + 26)], fill=INK)
    for px, py in ((28, 8), (12, 20), (44, 20), (16, 44), (40, 44)):
        d.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3], fill=INK)


def draw_hero_scene(d, x, y, w, h):
    """Chip and rising shares: sky, sun, big chip, green arrow, +33%."""
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=NAVY, width=3)
    d.ellipse([x + w - 62, y + 14, x + w - 22, y + 54], fill=GOLD)
    d.ellipse([x + 24, y + 26, x + 52, y + 54], fill=WHITE)
    d.ellipse([x + 40, y + 18, x + 74, y + 52], fill=WHITE)
    # big chip, centre-left
    cx, cy = x + 110, y + 130
    d.rectangle([cx - 52, cy - 52, cx + 52, cy + 52], fill=INK)
    d.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], fill=TEAL)
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=WHITE)
    for px in (-40, -14, 12, 38):
        d.rectangle([cx + px, cy - 64, cx + px + 8, cy - 52], fill=INK)
        d.rectangle([cx + px, cy + 52, cx + px + 8, cy + 64], fill=INK)
        d.rectangle([cx - 64, cy + px, cx - 52, cy + px + 8], fill=INK)
        d.rectangle([cx + 52, cy + px, cx + 64, cy + px + 8], fill=INK)
    # rising arrow, right side
    ax = x + w - 110
    d.line([ax, y + h - 60, ax + 46, y + 90], fill=GREEN, width=10)
    d.polygon([(ax + 46, y + 62), (ax + 78, y + 96), (ax + 46, y + 108)],
              fill=GREEN)
    d.text((x + w - 118, y + h - 52), "+33%", font=font(SANS_BOLD, 34),
           fill=GREEN)
    # small rising bars at the bottom
    bx = x + 24
    for i, bh in enumerate((18, 30, 44, 58)):
        d.rectangle([bx + i * 26, y + h - 22 - bh, bx + i * 26 + 16, y + h - 22],
                    fill=NAVY)


def draw_front_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.text((W // 2, 14), "THE WORLD TODAY", font=font(SERIF_BOLD, 62),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 82), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_BOLD, 26),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 116, W, 121], fill=GOLD)
    d.text((W // 2, 130), "THE DAY IN WORLD NEWS", font=font(SANS, 18),
           fill=GRAY, anchor="ma")

    # ---- hero: Huang reinstated at Nvidia
    hx, hy = 32, 158
    d.text((hx, hy), "NVIDIA CEO REINSTATED \u2014 SAN FRANCISCO",
           font=font(SANS_BOLD, 19), fill=RED)
    hero_head = "Huang Back at Nvidia After Trump Push"
    head_lines = wrap(d, hero_head, font(SERIF_BOLD, 44), 560)
    assert len(head_lines) <= 2, head_lines
    y = hy + 28
    for line in head_lines:
        d.text((hx, y), line, font=font(SERIF_BOLD, 44), fill=INK)
        y += 52
    hero_body = (
        "Nvidia's board voted unanimously on Monday to reinstate Jensen Huang "
        "as CEO, 11 days after he resigned. Trump said he lobbied the board "
        "directly. Shares jumped about 33%.")
    body_lines = wrap(d, hero_body, font(SANS, 20), 560)
    assert len(body_lines) <= 5, body_lines
    y = hy + 138
    for line in body_lines:
        d.text((hx, y), line, font=font(SANS, 20), fill=INK)
        y += 24
    # REINSTATED stamp
    sx, sy = hx, hy + 248
    d.rectangle([sx, sy, sx + 208, sy + 44], outline=RED, width=3)
    d.text((sx + 104, sy + 22), "REINSTATED", font=font(SANS_BOLD, 26),
           fill=RED, anchor="mm")
    d.text((sx + 222, sy + 12), "Monday, board vote", font=font(SANS, 18),
           fill=GRAY)

    # hero scene on the right
    draw_hero_scene(d, 620, 158, 372, 280)
    d.text((806, 446), "Nvidia shares jumped about 33% on Monday",
           font=font(SANS, 16), fill=GRAY, anchor="ma")

    d.rectangle([32, 472, 992, 475], fill=NAVY)

    # ---- stories 2-8 as full-width rows
    stories = [
        ("Russia May Launch Nuclear Satellite",
         "Monday: Western intelligence assessments say Russia could launch a "
         "satellite carrying a nuclear explosive as early as December. "
         "Russia denies it.",
         pic_satellite),
        ("Leaked Data Put Russian War Dead Near 500,000",
         "Monday: leaked death records analysed by Mediazona and Meduza show "
         "at least about 490,000 Russian soldiers dead; the true toll may be "
         "about 700,000.",
         pic_memorial),
        ("Moscow Warns Estonia It Risks 'Open War'",
         "Monday: Russia summoned Estonia's envoy, accusing Tallinn of "
         "hostile acts 'on the verge of triggering open war' after Estonia "
         "said it will shut its border.",
         pic_estonia),
        ("Korean Airspace Scare Proves False Alarm",
         "Tuesday: sirens sounded on Ulleung Island after an alert wrongly "
         "said an aircraft had violated airspace. It was lifted within about "
         "five minutes.",
         pic_siren),
        ("Hasina Plans Return to Bangladesh Dec. 16",
         "Tuesday: ousted PM Sheikh Hasina plans to fly home from exile in "
         "India on 16 December, Victory Day, her spokesperson told Reuters. "
         "She faces arrest on arrival.",
         pic_bangladesh),
        ("Two U.S. States Sue Musk Over Grok Deepfakes",
         "Monday: Virginia and Oregon sued SpaceX, alleging Grok's 'spicy "
         "mode' let users make non-consensual sexualised images. The claims "
         "are allegations, not findings.",
         pic_gavel),
        ("U.S. to Lead 2031 Women's World Cup",
         "Monday: FIFA confirmed the United States, Mexico, Costa Rica and "
         "Jamaica will co-host the 2031 Women's World Cup, the first 48-team "
         "edition.",
         pic_ball),
    ]

    row_y, row_h = 486, 66
    for i, (head, body, pic) in enumerate(stories):
        y = row_y + i * row_h
        d.rectangle([32, y, 992, y + row_h - 2], fill=WHITE)
        d.rectangle([32, y, 35, y + row_h - 2], fill=GOLD)
        pic(d, 44, y + 2)
        tx, tw = 112, 868
        head_lines = wrap(d, head, font(SANS_BOLD, 24), tw)
        body_lines = wrap(d, body, font(SANS, 16), tw)
        # A row holds one headline line and two body lines; fail loudly.
        assert len(head_lines) <= 1, head
        assert len(body_lines) <= 2, (head, body_lines)
        d.text((tx, y + 2), head, font=font(SANS_BOLD, 24), fill=INK)
        by = y + 30
        for line in body_lines:
            d.text((tx, by), line, font=font(SANS, 16), fill=(40, 44, 56))
            by += 17

    # ---- footer
    d.rectangle([32, 950, 992, 952], fill=NAVY)
    d.text((W // 2, 958),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 CNN \u00b7 BBC \u00b7 "
           "The Japan Times \u00b7 FIFA.com",
           font=font(SANS, 16), fill=GRAY, anchor="ma")
    d.text((W // 2, 978),
           "NHK \u00b7 The Hindu \u00b7 Dawn \u00b7 Mediazona \u00b7 Meduza \u00b7 "
           "Kyiv Independent \u00b7 The Straits Times",
           font=font(SANS, 16), fill=GRAY, anchor="ma")
    d.text((W // 2, 998),
           "Nvidia up about 33% \u00b7 Russian war dead near 500,000 \u00b7 "
           "First 48-team Women's World Cup",
           font=font(SANS, 16), fill=GRAY, anchor="ma")
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.normpath(os.path.join(here, "..", "assets", "entry.png"))
    img = draw_front_page()
    assert img.size == (1024, 1024)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG")
    size = os.path.getsize(out_path)
    assert size <= 1048576, size
    print("Wrote %s (%d bytes, 1024x1024)" % (out_path, size))


if __name__ == "__main__":
    main()
