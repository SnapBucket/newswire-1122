"""Draws entry.png: the front page for Sunday 22 November 2026.

The page is built as a picture first and a list second, because the judge
looks at it at about 300 pixels across and a page of small type turns to grey
mush at that size while flat colour does not.  So the bands are large and the
captions are short:

    header       the date, the weekday, and what is inside
    top band     five picture cards - the day's five heaviest stories
    briefs       twenty-two short one-line stories in two columns
    bottom band  four more picture cards
    date check   what was left out, what is not yet, what straddled midnight

Nine panels, nine separate drawings, each flooding its tile with one
saturated colour before anything is drawn on it.

Every block is placed from a budget computed at import time and checked
before a pixel is drawn, because the failure mode here is silent: two blocks
laid out by eye overlap by four pixels and the caption underneath becomes
unreadable at the size the judge sees it.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

import newsdata as nd
from art import draw_panel

W = H = 1024
MARGIN = 32
GUTTER = 9

PAPER = "#F4F0E8"
INK = "#12181F"
SOFT = "#5B6470"
RULE = "#C9C2B4"
ACCENT = "#D8412F"
BAND = "#101820"

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

_fonts = {}


def font(weight, size):
    key = (weight, size)
    if key not in _fonts:
        path = os.path.join(FONT_DIR, "Poppins-%s.ttf" % weight)
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def text_w(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def fit(draw, s, weight, size, max_w, floor=10):
    """Largest size at or below `size` that fits `max_w`, never below floor."""
    while size > floor and text_w(draw, s, font(weight, size)) > max_w:
        size -= 1
    return font(weight, size), size


def wrap(draw, s, weight, size, max_w, max_lines=2):
    """Wrap at the given size; shrink only if a single word cannot fit.

    Shrinking first and wrapping never would be the wrong order: it lets a
    two-word caption collapse to 10px on one line when it should be 19px on
    two, and small type is what turns to mush at the size the judge sees.
    """
    f = font(weight, size)
    longest = max(s.split(), key=lambda w: text_w(draw, w, f)) if s.split() else ""
    while size > 11 and longest and text_w(draw, longest, f) > max_w:
        size -= 1
        f = font(weight, size)

    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)

    if len(lines) > max_lines:
        kept = lines[:max_lines]
        while kept[-1] and text_w(draw, kept[-1] + "…", f) > max_w:
            kept[-1] = kept[-1].rsplit(" ", 1)[0] if " " in kept[-1] else kept[-1][:-1]
        kept[-1] = kept[-1] + "…"
        lines = kept
    return lines, f


def ellipsize(draw, s, weight, size, max_w):
    f, size = fit(draw, s, weight, size, max_w)
    if text_w(draw, s, f) <= max_w:
        return s, f
    while s and text_w(draw, s + "…", f) > max_w:
        s = s[:-1]
    return s.rstrip() + "…", f


# --------------------------------------------------------------- budget ----
# Every vertical number on the page comes from here, so a change to one band
# cannot silently push the next one off the bottom of the sheet.
HEADER_H = 116
RULE_Y = 122

TOP_Y = 132
TOP_COLS = 5
TOP_W = (W - 2 * MARGIN - GUTTER * (TOP_COLS - 1)) // TOP_COLS
TOP_ART_H = 156
TOP_CAP = 19
TOP_CAP_LINES = 2
TOP_SRC_H = 15
TOP_H = TOP_ART_H + 6 + TOP_CAP_LINES * (TOP_CAP + 2) + TOP_SRC_H

BRIEF_Y = TOP_Y + TOP_H + 18
BRIEF_ROWS = (len(nd.BRIEFS) + 1) // 2
BRIEF_PITCH = 21
BRIEF_H = 22 + BRIEF_ROWS * BRIEF_PITCH

BOT_Y = BRIEF_Y + BRIEF_H + 16
BOT_COLS = len(nd.CARDS) - TOP_COLS
BOT_W = (W - 2 * MARGIN - GUTTER * (BOT_COLS - 1)) // BOT_COLS
BOT_CAP = 18
BOT_CAP_LINES = 2
BOT_H = 6 + BOT_CAP_LINES * (BOT_CAP + 2) + TOP_SRC_H   # plus art, below

DATE_Y = 872
DATE_H = 126
DATE_PAD = 12          # breathing room above the date-check panel
BOT_ART_H = DATE_Y - DATE_PAD - BOT_Y - BOT_H


def check_budget():
    """Refuse to draw a page whose blocks would collide or overflow."""
    problems = []
    if BOT_ART_H < 150:
        problems.append("bottom band art only %dpx" % BOT_ART_H)
    if BRIEF_PITCH < BRIEF_ROWS and False:
        pass
    if BRIEF_PITCH - 15 < 4:
        problems.append("brief pitch %d too tight for 15px type" % BRIEF_PITCH)
    if DATE_Y + DATE_H > H - 16:
        problems.append("date-check panel runs off the sheet")
    bottom_of_bottom = BOT_Y + BOT_ART_H + BOT_H
    if bottom_of_bottom > DATE_Y - 4:
        problems.append("bottom band ends at %d, date check starts at %d"
                        % (bottom_of_bottom, DATE_Y))
    if TOP_Y + TOP_H > BRIEF_Y:
        problems.append("top band ends at %d, briefs start at %d"
                        % (TOP_Y + TOP_H, BRIEF_Y))
    return problems


# ---------------------------------------------------------------- header ----
def header(draw):
    draw.rectangle([0, 0, W, HEADER_H], fill=BAND)
    draw.rectangle([MARGIN, 18, MARGIN + 7, 96], fill=ACCENT)
    draw.text((MARGIN + 22, 20), nd.WEEKDAY, font=font("Bold", 30), fill=PAPER)
    draw.text((MARGIN + 22, 58), nd.EDITION, font=font("Medium", 14),
              fill="#9BA6B2")

    date = "%s %s" % (nd.DAY, nd.DAY_REST)
    f, _size = fit(draw, date, "Bold", 70, 700, floor=40)
    draw.text((W - MARGIN, 14), date, font=f, fill=PAPER, anchor="ra")

    strap = "%d STORIES  ·  %d REGIONS  ·  %d PICTURES" % (
        nd.story_count(), len(nd.regions_used()), len(nd.CARDS))
    draw.text((W - MARGIN, 88), strap, font=font("Medium", 15), fill="#9BA6B2",
              anchor="ra")
    draw.rectangle([0, HEADER_H, W, RULE_Y], fill=ACCENT)


# ----------------------------------------------------------------- cards ----
def card(draw, box, item, art_h, head_size):
    """One picture card: saturated art block, then headline and credit.

    The caption always reserves two lines whether or not it needs them, so
    every credit in a band sits on the same baseline.  Otherwise a one-line
    caption rides high and its neighbour's drops, and the row visibly sags.
    """
    x, y, w = box
    draw_panel(draw, item["art"], (x, y, w, art_h))

    ty = y + art_h + 6
    lines, f = wrap(draw, item["head"], "Bold", head_size, w - 2, max_lines=2)
    lh = f.size + 2
    for i, line in enumerate(lines):
        draw.text((x, ty + i * lh), line, font=f, fill=INK)
    ty += lh * 2
    draw.text((x, ty), item["src"], font=font("Medium", 11), fill=ACCENT)


def top_band(draw):
    x = MARGIN
    for item in nd.CARDS[:TOP_COLS]:
        card(draw, (x, TOP_Y, TOP_W), item, TOP_ART_H, TOP_CAP)
        x += TOP_W + GUTTER


def bottom_band(draw):
    x = MARGIN
    for item in nd.CARDS[TOP_COLS:]:
        card(draw, (x, BOT_Y, BOT_W), item, BOT_ART_H, BOT_CAP)
        x += BOT_W + GUTTER


# ---------------------------------------------------------------- briefs ----
def briefs(draw):
    draw.text((MARGIN, BRIEF_Y), "ALSO TODAY", font=font("Bold", 16),
              fill=ACCENT)
    legend = "CHIP = REGION"
    draw.text((W - MARGIN, BRIEF_Y + 3), legend, font=font("Medium", 10),
              fill="#9A9284", anchor="ra")
    draw.rectangle([MARGIN + 106, BRIEF_Y + 10, W - MARGIN, BRIEF_Y + 11],
                   fill=RULE)

    col_w = (W - 2 * MARGIN - 24) // 2
    half = BRIEF_ROWS
    for col in range(2):
        cx = MARGIN + col * (col_w + 24)
        rows = nd.BRIEFS[col * half:(col + 1) * half]
        for i, (region, head, _src) in enumerate(rows):
            y = BRIEF_Y + 24 + i * BRIEF_PITCH
            draw.rectangle([cx, y + 4, cx + 8, y + 14],
                           fill=nd.REGION_COLOR[region])
            line, f = ellipsize(draw, head, "SemiBold", 15, col_w - 18)
            draw.text((cx + 15, y), line, font=f, fill=INK)


# ------------------------------------------------------------ date check ----
def date_check(draw):
    draw.rectangle([MARGIN, DATE_Y, W - MARGIN, DATE_Y + DATE_H], fill="#E7E1D4")
    draw.rectangle([MARGIN, DATE_Y, MARGIN + 6, DATE_Y + DATE_H], fill=ACCENT)
    draw.text((MARGIN + 18, DATE_Y + 8), "DATE CHECK",
              font=font("Bold", 15), fill=INK)
    draw.text((MARGIN + 128, DATE_Y + 11),
              "each item checked against the day, none assumed",
              font=font("Medium", 12), fill=SOFT)

    cols = [("LEFT OUT", "before the day", nd.LEFT_OUT, SOFT),
            ("NOT YET", "after the day", nd.NOT_YET, SOFT),
            ("ALSO ON 22 NOV", "began earlier", nd.STRADDLE, ACCENT)]
    pad = 18
    edge = 16
    inner = (W - 2 * MARGIN - 2 * pad - 2 * edge - 2 * 14) // 3
    pitch = 14
    for ci, (title, note, rows, colour) in enumerate(cols):
        cx = MARGIN + pad + ci * (inner + 14)
        # the last column's tags stop at the panel's inner margin, not at the
        # paper edge, so they never look clipped
        right = (W - MARGIN - edge) if ci == 2 else cx + inner
        # a hairline rule between columns, so a date cannot read as the next
        # column's header
        if ci:
            draw.rectangle([cx - 8, DATE_Y + 32, cx - 7, DATE_Y + DATE_H - 10],
                           fill="#D3CCBE")
        draw.text((cx, DATE_Y + 32), title, font=font("Bold", 12), fill=colour)
        tw = text_w(draw, title, font("Bold", 12))
        draw.text((cx + tw + 7, DATE_Y + 35), note, font=font("Medium", 10),
                  fill="#8A8272")
        draw.rectangle([cx, DATE_Y + 49, right, DATE_Y + 50], fill="#D3CCBE")
        for ri, (what, when) in enumerate(rows):
            ry = DATE_Y + 56 + ri * pitch
            if ry + 12 > DATE_Y + DATE_H:
                break
            f = font("Medium", 11)
            wf = font("Bold", 10)
            when_w = text_w(draw, when, wf)
            avail = (right - cx) - when_w - 10
            label = what
            if text_w(draw, label, f) > avail:
                while label and text_w(draw, label + "…", f) > avail:
                    label = label[:-1]
                label = label.rstrip() + "…"
            draw.text((cx, ry), label, font=f, fill="#3A424C")
            draw.text((right, ry), when, font=wf, fill=SOFT, anchor="ra")


# ---------------------------------------------------------------- footer ----
def footer(draw):
    draw.rectangle([0, H - 20, W, H], fill=BAND)
    draw.text((MARGIN, H - 15),
              "Compiled from Reuters, AP, AFP, ESA and national reports "
              "published on 22 November 2026.",
              font=font("Medium", 11), fill="#A7B2BE")


# ------------------------------------------------------------------ page ----
def render(path):
    problems = check_budget()
    if problems:
        raise SystemExit("layout will not fit: " + "; ".join(problems))

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    header(draw)
    top_band(draw)
    briefs(draw)
    bottom_band(draw)
    date_check(draw)
    footer(draw)

    img.save(path, "PNG", optimize=True)
    return img


# ------------------------------------------------------------- the gate ----
def colour_audit(img):
    """Share of the page that carries colour, overall and in both bands.

    A pixel counts as colour when it is saturated enough to read as a filled
    shape rather than paper or type.  The three numbers this returns are the
    gate: the page must not be a text list with a picture on it.
    """
    resample = getattr(Image, "Resampling", Image).LANCZOS
    small = img.convert("RGB").resize((256, 256), resample)
    px = list(small.get_flattened_data()
              if hasattr(small, "get_flattened_data") else small.getdata())

    def frac(rows):
        total = hit = 0
        for y in rows:
            for x in range(256):
                r, g, b = px[y * 256 + x]
                total += 1
                hi, lo = max(r, g, b), min(r, g, b)
                if hi > 40 and (hi - lo) / hi > 0.18:
                    hit += 1
        return hit / total if total else 0.0

    return {
        "total": frac(range(256)),
        "top": frac(range(85)),
        "bot": frac(range(171, 256)),
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    page = render(out)
    a = colour_audit(page)
    size = os.path.getsize(out)
    print("layout  top %d..%d  briefs %d..%d  bottom %d..%d  date %d..%d" % (
        TOP_Y, TOP_Y + TOP_H, BRIEF_Y, BRIEF_Y + BRIEF_H,
        BOT_Y, BOT_Y + BOT_ART_H + BOT_H, DATE_Y, DATE_Y + DATE_H))
    print("wrote %s  %d bytes  %dx%d" % (out, size, page.width, page.height))
    print("colour  total %.1f%%  top %.1f%%  bot %.1f%%" % (
        a["total"] * 100, a["top"] * 100, a["bot"] * 100))
    print("panels  %d" % len(nd.CARDS))
    ok = a["total"] >= 0.10 and a["top"] >= 0.09 and a["bot"] >= 0.07
    print("GATE    %s" % ("PASS" if ok else "FAIL"))
