#!/usr/bin/env python3
"""Render the news infographic for Wednesday 18 November 2026.

Draws a 1024x1024 newspaper-style infographic with Pillow: a masthead
naming the day, a hero panel on Iran's strikes on Kuwait and Bahrain,
four panels on the day's other big stories (Xi-Putin in Shenzhen,
Peltola's Alaska win, the Board of Peace report, Ebola in DR Congo)
and an "also today" strip. Writes the PNG to /tmp for preview and the
base64 of it (one line) to image_b64.txt next to this script, so the
repository holds no binary file.

Build-time only: the grader never runs this file; main.py ships the
image. Needs Pillow and the Liberation fonts.
"""
import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PNG_PREVIEW = Path("/tmp/news18_entry.png")
B64_OUT = HERE / "image_b64.txt"

W, H = 1024, 1024
CREAM = (251, 243, 226)
NAVY = (27, 42, 74)
GOLD = (201, 162, 39)
INK = (30, 32, 38)
MUTED = (90, 96, 110)
CARD = (255, 255, 255)
BORDER = (216, 205, 180)
STRIP = (238, 228, 203)
RED = (192, 57, 43)
GREEN = (39, 120, 90)
BLUE = (41, 98, 168)
PURPLE = (122, 74, 178)
TEAL = (14, 130, 145)

FONTS = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("LiberationSans-Regular.ttf", s)  # noqa: E731
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)  # noqa: E731
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, xy, text, fnt, color, max_w, leading):
    """Draw wrapped text; returns the y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rounded_card(draw, box, fill, outline, radius=10, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                           width=width)


# ---------------------------------------------------------------- icons
def icon_globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=20, end=160, fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=color, width=3)


def icon_ballot(draw, cx, cy, r, color):
    w = r * 1.5
    draw.rectangle([cx - w / 2, cy - r * 0.3, cx + w / 2, cy + r],
                   outline=color, width=4)
    draw.line([cx - w / 2, cy - r * 0.3, cx - w / 2 + 12, cy - r * 0.85,
               cx + w / 2 - 12, cy - r * 0.85, cx + w / 2, cy - r * 0.3],
              fill=color, width=4)
    draw.line([cx - w * 0.22, cy + r * 0.2, cx - w * 0.05, cy + r * 0.45,
               cx + w * 0.25, cy - r * 0.05], fill=color, width=5)


def icon_report(draw, cx, cy, r, color):
    # A report document: page with a folded corner and text lines.
    w, h = r * 1.15, r * 1.45
    x0, y0 = cx - w / 2, cy - h / 2
    x1, y1 = cx + w / 2, cy + h / 2
    fold = 14
    draw.polygon([(x0, y0), (x1 - fold, y0), (x1, y0 + fold), (x1, y1),
                  (x0, y1)], outline=color, width=4)
    draw.line([x1 - fold, y0, x1 - fold, y0 + fold, x1, y0 + fold],
              fill=color, width=3)
    for i, lw in enumerate((0.62, 0.72, 0.5)):
        ly = y0 + h * (0.32 + i * 0.2)
        draw.line([x0 + 10, ly, x0 + 10 + w * lw, ly], fill=color, width=4)


def icon_virus(draw, cx, cy, r, color):
    import math
    for k in range(8):
        ang = math.radians(k * 45)
        x1 = cx + r * 0.62 * math.cos(ang)
        y1 = cy + r * 0.62 * math.sin(ang)
        x2 = cx + r * 1.0 * math.cos(ang)
        y2 = cy + r * 1.0 * math.sin(ang)
        draw.line([x1, y1, x2, y2], fill=color, width=4)
        draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=color)
    draw.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62],
                 fill=color)
    draw.ellipse([cx - r * 0.28, cy - r * 0.28, cx - r * 0.02, cy - r * 0.02],
                 fill=CARD)
    draw.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.3, cy + r * 0.35],
                 fill=CARD)


def hero_scene(draw, box):
    """Night scene: drones over a Gulf air base, defences firing back."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=12, fill=(22, 35, 63))
    # Stars.
    for sx, sy in [(x0 + 30, y0 + 22), (x0 + 120, y0 + 40), (x0 + 210, y0 + 18),
                   (x0 + 290, y0 + 48), (x0 + 70, y0 + 70), (x0 + 250, y0 + 80),
                   (x0 + 330, y0 + 26), (x0 + 170, y0 + 95)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(200, 210, 235))
    # Moon.
    draw.ellipse([x1 - 62, y0 + 18, x1 - 22, y0 + 58], fill=(232, 214, 150))
    # Ground and base buildings.
    gy = y1 - 44
    draw.rectangle([x0, gy, x1, y1], fill=(13, 22, 40))
    draw.rectangle([x0 + 28, gy - 34, x0 + 110, gy], fill=(52, 66, 96))
    draw.rectangle([x0 + 130, gy - 20, x0 + 220, gy], fill=(44, 58, 86))
    draw.rectangle([x0 + 250, gy - 46, x0 + 300, gy], fill=(52, 66, 96))
    for wx in (x0 + 44, x0 + 70, x0 + 150, x0 + 180, x0 + 262):
        draw.rectangle([wx, gy - 16, wx + 10, gy - 6], fill=(240, 200, 90))
    # Runway lights.
    for rx in range(x0 + 16, x1 - 16, 36):
        draw.ellipse([rx, gy + 18, rx + 6, gy + 24], fill=(240, 200, 90))
    # Drones: small swept silhouettes with dotted trails.
    def drone(dx, dy, scale, flip=False):
        pts = [(dx, dy), (dx - 26 * scale, dy + 10 * scale),
               (dx - 8 * scale, dy + 4 * scale), (dx, dy + 12 * scale),
               (dx + 8 * scale, dy + 4 * scale), (dx + 26 * scale, dy + 10 * scale)]
        if flip:
            pts = [(2 * dx - px, py) for px, py in pts]
        draw.polygon(pts, fill=(210, 218, 235))
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 120, 90))
    drone(x0 + 90, y0 + 52, 1.0)
    drone(x0 + 220, y0 + 92, 0.8, flip=True)
    for i in range(5):
        tx = x0 + 118 + i * 16
        draw.ellipse([tx, y0 + 66 + i * 2, tx + 3, y0 + 69 + i * 2],
                     fill=(200, 210, 235))
    # Interception bursts.
    def burst(bx, by, r, color):
        for ang in range(0, 360, 30):
            import math
            rad = math.radians(ang)
            draw.line([bx, by, bx + r * math.cos(rad), by + r * math.sin(rad)],
                      fill=color, width=3)
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 230, 150))
    burst(x0 + 300, y0 + 70, 26, (255, 160, 60))
    burst(x0 + 160, y0 + 130, 20, (255, 190, 90))
    # Defence missile rising.
    draw.line([x0 + 60, gy - 30, x0 + 150, y0 + 132], fill=(255, 200, 120),
              width=3)
    draw.polygon([(x0 + 150, y0 + 132), (x0 + 142, y0 + 142),
                  (x0 + 154, y0 + 142)], fill=(255, 230, 150))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 123], fill=GOLD)
    d.text((W // 2, 16), "THE WORLD IN ONE PICTURE", font=SANS_B(21),
           fill=GOLD, anchor="ma")
    d.text((W // 2, 42), "WEDNESDAY 18 NOVEMBER 2026", font=SERIF_B(50),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 96), "WORLD NEWS  •  ONE DAY  •  ONE IMAGE",
           font=SANS(16), fill=(159, 176, 204), anchor="ma")

    # Hero card.
    hx, hy, hw, hh = 24, 136, 976, 280
    rounded_card(d, [hx, hy, hx + hw, hy + hh], CARD, BORDER)
    d.rectangle([hx, hy + 10, hx + 10, hy + hh - 10], fill=RED)
    d.text((hx + 28, hy + 16), "MIDDLE EAST  •  THE GULF", font=SANS_B(19),
           fill=RED)
    d.text((hx + 28, hy + 44), "IRAN STRIKES KUWAIT", font=SERIF_B(44),
           fill=INK)
    d.text((hx + 28, hy + 94), "& BAHRAIN", font=SERIF_B(44), fill=INK)
    hero_body = ("Iran fires missiles and drones at U.S. bases in Kuwait "
                 "and Bahrain before dawn; Gulf air defences intercept "
                 "them — the first Iranian attack on Kuwait since "
                 "September.")
    draw_text_block(d, (hx + 28, hy + 160), hero_body, SANS(21), INK,
                    560, 28)
    hero_scene(d, [hx + 620, hy + 14, hx + hw - 14, hy + hh - 14])

    # Grid cards.
    cards = [
        dict(x=24, y=430, color=GREEN, kicker="ASIA  •  DIPLOMACY",
             head="XI AND PUTIN MEET IN SHENZHEN",
             body=("Talks on the eve of Thursday's first trilateral summit "
                   "with Trump. Xi denounces protectionism; Putin calls "
                   "the three-way meeting “highly useful”."),
             icon=icon_globe),
        dict(x=524, y=430, color=BLUE, kicker="UNITED STATES",
             head="PELTOLA FLIPS ALASKA SENATE SEAT",
             body=("Democrat Mary Peltola beats Dan Sullivan; Democrats "
                   "take a 56–44 Senate majority. She is the first Alaska "
                   "Native ever elected to the Senate."),
             icon=icon_ballot),
        dict(x=24, y=674, color=PURPLE, kicker="MIDDLE EAST  •  GAZA",
             head="BOARD OF PEACE FAULTS BOTH SIDES",
             body=("Trump's Board of Peace says Israel and Hamas both "
                   "failed their commitments, leaving Gaza's ceasefire in "
                   "danger of collapse, in a report seen by Reuters."),
             icon=icon_report),
        dict(x=524, y=674, color=TEAL, kicker="AFRICA  •  HEALTH",
             head="EBOLA CASES DOUBLE IN DR CONGO",
             body=("The UN says the outbreak passed 11,000 cases and 5,400 "
                   "deaths, with children paying a terrible price; 400 to "
                   "500 new cases are still found each week."),
             icon=icon_virus),
    ]
    cw, chh = 476, 230
    for c in cards:
        x, y = c["x"], c["y"]
        rounded_card(d, [x, y, x + cw, y + chh], CARD, BORDER)
        d.rectangle([x + 10, y, x + cw - 10, y + 8], fill=c["color"])
        c["icon"](d, x + 48, y + 58, 30, c["color"])
        tx = x + 96
        d.text((tx, y + 18), c["kicker"], font=SANS_B(16), fill=c["color"])
        head_lines = wrap(d, c["head"], SERIF_B(27), cw - 112)
        hyy = y + 44
        for line in head_lines[:2]:
            d.text((tx, hyy), line, font=SERIF_B(27), fill=INK)
            hyy += 32
        draw_text_block(d, (x + 20, y + 118), c["body"], SANS(18), INK,
                        cw - 40, 24)

    # Also today strip.
    sx, sy, sw, sh = 24, 918, 976, 62
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=10, fill=STRIP)
    d.text((sx + 16, sy + 8), "ALSO TODAY", font=SANS_B(16), fill=INK)
    also = ("COP31 deadlocked in Antalya as 21 issues stay unresolved  •  "
            "Category 5 Cyclone Xavier batters the Northern Cook Islands  •  "
            "Trump meets Marcos in Manila, then flies to China  •  Putin not "
            "ready for serious Ukraine peace talks, sources tell NYT")
    draw_text_block(d, (sx + 16, sy + 30), also, SANS(16), INK, sw - 32, 20)

    # Footer.
    d.text((W // 2, 984),
           "All events happened or were first reported on Wednesday "
           "18 November 2026.",
           font=SERIF_I(17), fill=MUTED, anchor="ma")
    d.text((W // 2, 1004),
           "As reported by Reuters, AP, the UN and others  •  Drawn for "
           "make.fun",
           font=SERIF_I(15), fill=MUTED, anchor="ma")

    img.save(PNG_PREVIEW, "PNG", optimize=True)
    raw = PNG_PREVIEW.read_bytes()
    B64_OUT.write_text(base64.b64encode(raw).decode("ascii") + "\n",
                       encoding="ascii")
    print(f"PNG: {len(raw)} bytes, {img.size[0]}x{img.size[1]}")
    print(f"base64: {B64_OUT} ({B64_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
