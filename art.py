"""Flat vector drawing primitives and the nine panel pictures.

House rules, applied without exception: flat fill only.  No gradients, no
shadows, no strokes around shapes, no human faces.  Every panel starts by
flooding its box with one saturated colour, so a panel is never a thin
sketch floating on paper.

Every routine draws in normalised space (0..1 across and down the box), so
the same picture serves a wide card at the top of the page and a narrower
one at the bottom without being redrawn.
"""

import math

from PIL import Image, ImageDraw

ACCENT = "#D8412F"
INK = "#12181F"
PAPER = "#F4F0E8"


class Canvas:
    """A box that maps 0..1 coordinates onto real pixels."""

    def __init__(self, draw, box):
        self.d = draw
        self.x, self.y, self.w, self.h = box

    # -- coordinate mapping ------------------------------------------------
    def _px(self, fx):
        return self.x + fx * self.w

    def _py(self, fy):
        return self.y + fy * self.h

    # -- primitives --------------------------------------------------------
    def bg(self, colour):
        self.d.rectangle([self.x, self.y, self.x + self.w - 1,
                          self.y + self.h - 1], fill=colour)

    def band(self, fy0, fy1, colour):
        self.d.rectangle([self.x, self._py(fy0), self.x + self.w - 1,
                          self._py(fy1)], fill=colour)

    def rect(self, fx, fy, fw, fh, colour):
        self.d.rectangle([self._px(fx), self._py(fy),
                          self._px(fx + fw), self._py(fy + fh)], fill=colour)

    def rrect(self, fx, fy, fw, fh, radius, colour):
        x0, y0 = self._px(fx), self._py(fy)
        x1, y1 = self._px(fx + fw), self._py(fy + fh)
        r = max(1, min(radius * min(self.w, self.h), (x1 - x0) / 2, (y1 - y0) / 2))
        self.d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=colour)

    def circ(self, fcx, fcy, fr, colour):
        rx, ry = fr * self.w, fr * self.h
        self.d.ellipse([self._px(fcx) - rx, self._py(fcy) - ry,
                        self._px(fcx) + rx, self._py(fcy) + ry], fill=colour)

    def dot(self, fcx, fcy, fr, colour):
        """A circle that stays round whatever the box aspect is."""
        r = fr * self.h
        self.d.ellipse([self._px(fcx) - r, self._py(fcy) - r,
                        self._px(fcx) + r, self._py(fcy) + r], fill=colour)

    def poly(self, points, colour):
        self.d.polygon([(self._px(px), self._py(py)) for px, py in points],
                       fill=colour)

    def arcband(self, fcx, fcy, fr, start, end, colour, width=0.035):
        """An arc drawn as a filled band, not a stroked path."""
        steps = 40
        outer, inner = [], []
        rw = width * self.h
        for i in range(steps + 1):
            a = math.radians(start + (end - start) * i / steps)
            outer.append((self._px(fcx) + math.cos(a) * (fr * self.h + rw / 2),
                          self._py(fcy) + math.sin(a) * (fr * self.h + rw / 2)))
            inner.append((self._px(fcx) + math.cos(a) * (fr * self.h - rw / 2),
                          self._py(fcy) + math.sin(a) * (fr * self.h - rw / 2)))
        self.d.polygon(outer + inner[::-1], fill=colour)

    def star(self, fcx, fcy, fr, colour, points=6, inner=0.45, rot=-90):
        pts = []
        for i in range(points * 2):
            a = math.radians(rot + i * 180.0 / points)
            r = fr * (1.0 if i % 2 == 0 else inner)
            pts.append((self._px(fcx) + math.cos(a) * r * self.h,
                        self._py(fcy) + math.sin(a) * r * self.h))
        self.d.polygon(pts, fill=colour)

    def bar(self, fx0, fy0, fx1, fy1, thick, colour):
        """A thick straight bar from one point to another, as a filled quad.

        Needed for anything rotated - a gavel's head has to sit across its
        handle, not beside it, and an axis-aligned rectangle cannot do that.
        """
        x0, y0, x1, y1 = self._px(fx0), self._py(fy0), self._px(fx1), self._py(fy1)
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length * thick * self.h / 2, dx / length * thick * self.h / 2
        self.d.polygon([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny),
                        (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], fill=colour)

    def flame(self, fcx, fbase, fw, fh, colour, lean=0.0):
        self.poly([
            (fcx - fw / 2, fbase),
            (fcx - fw / 2 + lean * 0.4, fbase - fh * 0.45),
            (fcx + lean * 0.9, fbase - fh),
            (fcx + fw / 2 + lean * 0.3, fbase - fh * 0.40),
            (fcx + fw / 2, fbase),
        ], colour)

    def smoke(self, fx, fy, count=3, spread=0.10, size=0.07, colour="#8E9AA3",
              rise=0.13):
        for i in range(count):
            self.dot(fx + spread * (i - (count - 1) / 2.0) * 1.4,
                     fy - rise * i, size * (1 - 0.14 * i), colour)

    def wave(self, fy, amp, colour, period=0.33, thickness=0.10):
        """A filled sine band across the box: water, smoke, ground haze."""
        steps = 48
        top, bottom = [], []
        for i in range(steps + 1):
            fx = i / steps
            yy = fy + math.sin(fx / period * math.tau) * amp
            top.append((self._px(fx), self._py(yy)))
            bottom.append((self._px(fx), self._py(yy + thickness)))
        self.d.polygon(top + bottom[::-1], fill=colour)

    def sunburst(self, fcx, fcy, colour, count=9, r0=0.30, r1=1.25):
        for i in range(count):
            a = math.tau * i / count
            self.poly([
                (fcx + math.cos(a) * r0 * 0.6, fcy + math.sin(a) * r0 * 0.6),
                (fcx + math.cos(a - 0.055) * r1, fcy + math.sin(a - 0.055) * r1),
                (fcx + math.cos(a + 0.055) * r1, fcy + math.sin(a + 0.055) * r1),
            ], colour)


# --------------------------------------------------------------- panels ----
def p_cop31(c):
    """The gavel coming down: head across the handle, block beneath, delegates.

    A decision being adopted is one specific gesture, and this panel is built
    around it: a mallet head set across its handle at an angle, raised clear
    of a block, with impact ticks at the point of contact.  Two earlier
    versions drew the head as an axis-aligned slab, which read as a document
    on a desk and left the caption to do all the work.
    """
    c.bg("#1D4E5C")
    c.band(0.0, 0.22, "#256B78")
    # far wall of national flags, flat blocks
    for i in range(7):
        c.rect(0.03 + i * 0.138, 0.035, 0.078, 0.100,
               ["#2F8F9D", "#3A9BA6", "#2F8F9D", "#48A7B0"][i % 4])
    c.rect(0.0, 0.22, 1.0, 0.010, ACCENT)

    # the block it strikes: a low plinth, clearly separate from the gavel
    c.poly([(0.26, 0.615), (0.74, 0.615), (0.80, 0.660), (0.20, 0.660)],
           "#0A2A31")
    c.rect(0.20, 0.660, 0.60, 0.028, "#071F25")

    # the gavel, tilted: handle from lower right up to the head at upper left
    c.bar(0.80, 0.505, 0.475, 0.360, 0.050, "#8C5A2B")      # handle
    c.bar(0.385, 0.300, 0.545, 0.395, 0.115, "#E8DCC8")     # head, across it
    c.bar(0.372, 0.293, 0.398, 0.308, 0.115, "#C9BCA4")     # head, near face
    c.bar(0.532, 0.387, 0.558, 0.402, 0.115, "#C9BCA4")     # head, far face

    # impact ticks at the point of contact
    for dx, dy in ((-0.052, 0.010), (0.040, -0.040), (-0.078, -0.026),
                   (0.062, 0.026)):
        c.rect(0.365 + dx, 0.470 + dy, 0.018, 0.018, ACCENT)

    # delegate desks, receding
    for row, fy in enumerate((0.755, 0.885)):
        shade = "#2A6270" if row == 0 else "#163E48"
        for i in range(5):
            c.rrect(0.03 + i * 0.195, fy, 0.155, 0.092, 0.015, shade)
            c.dot(0.055 + i * 0.195, fy + 0.030, 0.020, "#B9D6D8")


def p_factory(c):
    """Sawtooth factory roof, fire climbing out of it, smoke above."""
    c.bg("#6E4B3A")
    c.band(0.0, 0.18, "#8A5F49")
    c.sunburst(0.5, 0.62, "#B4653F", count=7, r0=0.34, r1=1.1)
    # smoke
    c.smoke(0.42, 0.30, count=4, spread=0.13, size=0.075, colour="#9A8578")
    c.smoke(0.70, 0.26, count=3, spread=0.11, size=0.062, colour="#8A756A")
    # sawtooth body
    c.rect(0.06, 0.55, 0.88, 0.34, "#3B2C25")
    for i in range(4):
        bx = 0.06 + i * 0.22
        c.poly([(bx, 0.55), (bx + 0.20, 0.55), (bx + 0.20, 0.44),
                (bx + 0.02, 0.52)], "#4A3730")
    # windows
    for i in range(6):
        c.rect(0.10 + i * 0.135, 0.66, 0.075, 0.09, "#C8763F")
    # chimney with fire on top
    c.rect(0.68, 0.34, 0.075, 0.22, "#33241E")
    c.flame(0.717, 0.36, 0.20, 0.30, ACCENT, lean=0.05)
    c.flame(0.717, 0.36, 0.11, 0.18, "#F2A03C", lean=0.03)
    c.flame(0.24, 0.56, 0.22, 0.26, "#E2673A", lean=-0.04)
    c.flame(0.24, 0.56, 0.11, 0.15, "#F6B34C", lean=-0.02)
    c.rect(0.0, 0.89, 1.0, 0.11, "#241A16")


def p_mercury(c):
    """A cratered planet, an orbit arc, and a spacecraft on it."""
    c.bg("#12263A")
    for i, (fx, fy, fr) in enumerate(((0.12, 0.16, 0.010), (0.26, 0.09, 0.008),
                                      (0.80, 0.14, 0.011), (0.91, 0.32, 0.008),
                                      (0.07, 0.40, 0.007), (0.68, 0.06, 0.006))):
        c.dot(fx, fy, fr, "#6E86A0")
    c.arcband(0.50, 0.56, 0.40, 190, 350, "#2C4763", 0.030)
    c.dot(0.50, 0.58, 0.245, "#9AA0A2")
    c.dot(0.42, 0.50, 0.052, "#82898C")
    c.dot(0.60, 0.63, 0.070, "#82898C")
    c.dot(0.53, 0.44, 0.030, "#82898C")
    c.dot(0.36, 0.66, 0.035, "#8C9396")
    # spacecraft riding the arc: body, two solar wings, a dish
    c.rect(0.695, 0.305, 0.085, 0.062, "#D9DDE0")
    c.poly([(0.700, 0.310), (0.600, 0.245), (0.600, 0.325), (0.700, 0.345)],
           "#2F6FB0")
    c.poly([(0.780, 0.310), (0.880, 0.245), (0.880, 0.325), (0.780, 0.345)],
           "#3B82C4")
    for i in range(3):
        c.rect(0.615 + i * 0.024, 0.262, 0.008, 0.062, "#6FA3D8")
        c.rect(0.795 + i * 0.024, 0.262, 0.008, 0.062, "#7FB0E0")
    c.dot(0.737, 0.278, 0.028, "#F0C24B")
    c.rect(0.0, 0.93, 1.0, 0.07, "#0B1826")


def p_belgium(c):
    """An airport with the sky crossed out: grounded, from Monday."""
    c.bg("#2F6FB0")
    c.band(0.0, 0.42, "#3B82C4")
    c.sunburst(0.5, 0.24, "#4A90CE", count=8, r0=0.30, r1=1.0)
    # control tower
    c.rect(0.80, 0.30, 0.055, 0.40, "#DCE3E8")
    c.rrect(0.775, 0.24, 0.105, 0.075, 0.012, "#F0F4F6")
    c.rect(0.792, 0.255, 0.070, 0.032, "#1E3F5C")
    # aircraft, nose down, parked
    c.poly([(0.10, 0.62), (0.52, 0.56), (0.60, 0.585), (0.60, 0.63),
            (0.14, 0.70)], "#EDF1F4")
    c.poly([(0.34, 0.60), (0.44, 0.44), (0.50, 0.44), (0.46, 0.615)], "#D5DEE4")
    c.poly([(0.20, 0.665), (0.26, 0.78), (0.30, 0.78), (0.28, 0.665)], "#D5DEE4")
    c.dot(0.135, 0.655, 0.016, "#1E3F5C")
    # the strike mark: a heavy red slash across the airfield
    c.poly([(0.06, 0.84), (0.62, 0.84), (0.66, 0.90), (0.10, 0.90)], ACCENT)
    c.rect(0.0, 0.90, 1.0, 0.10, "#20486E")


def p_brazil(c):
    """A house reduced to a roof on the ground, water still standing."""
    c.bg("#5A6B72")
    c.band(0.0, 0.24, "#6B7C83")
    c.smoke(0.24, 0.20, count=3, spread=0.12, size=0.070, colour="#84939A")
    c.smoke(0.66, 0.16, count=3, spread=0.10, size=0.062, colour="#78878E")
    # broken wall stubs
    c.rect(0.10, 0.52, 0.16, 0.26, "#8E9AA0")
    c.rect(0.34, 0.58, 0.11, 0.20, "#7C888E")
    c.rect(0.74, 0.54, 0.15, 0.24, "#8E9AA0")
    # collapsed roof
    c.poly([(0.06, 0.56), (0.42, 0.34), (0.46, 0.44), (0.14, 0.66)], ACCENT)
    c.poly([(0.46, 0.66), (0.86, 0.50), (0.88, 0.58), (0.50, 0.72)], "#B8382A")
    # rubble
    for fx, fy, fw, fh in ((0.18, 0.74, 0.08, 0.05), (0.30, 0.78, 0.06, 0.04),
                           (0.52, 0.76, 0.09, 0.05), (0.64, 0.80, 0.06, 0.04),
                           (0.44, 0.72, 0.05, 0.035)):
        c.rect(fx, fy, fw, fh, "#B9C2C6")
    # standing water
    c.wave(0.86, 0.018, "#41525A", thickness=0.14)
    c.wave(0.88, 0.014, "#33444B", thickness=0.12)


def p_missile(c):
    """An intercept: climbing missile, radar rings, burst high right."""
    c.bg("#152A45")
    c.band(0.0, 0.34, "#1C3555")
    for fr in (0.16, 0.28, 0.40):
        c.arcband(0.86, 0.90, fr, 180, 360, "#27476B", 0.016)
    # trail
    c.arcband(0.30, 0.95, 0.52, 250, 300, "#3E6E9E", 0.030)
    # missile body
    c.poly([(0.24, 0.74), (0.36, 0.40), (0.40, 0.42), (0.30, 0.76)], "#D7DDE2")
    c.poly([(0.36, 0.40), (0.385, 0.30), (0.40, 0.42)], ACCENT)
    c.poly([(0.27, 0.66), (0.20, 0.72), (0.26, 0.70)], "#B6BEC5")
    c.flame(0.245, 0.80, 0.10, 0.16, "#F2A03C", lean=-0.02)
    # interceptor burst
    c.star(0.74, 0.28, 0.115, "#F2C14E", points=7, inner=0.42)
    c.star(0.74, 0.28, 0.062, "#FFF0C4", points=7, inner=0.45)
    c.rect(0.0, 0.92, 1.0, 0.08, "#0E1D31")


def p_boat(c):
    """A boat down by the bow, half swamped, water over the gunwale.

    The caption says "capsizes", so the drawing has to show it: the hull is
    tilted steeply, the bow is under the surface, and the water line cuts
    across the deck rather than sitting politely below it.  A level boat on
    flat water contradicts the words beside it.
    """
    c.bg("#1F4E63")
    c.band(0.0, 0.26, "#2A6377")
    c.smoke(0.18, 0.20, count=2, spread=0.09, size=0.050, colour="#3C7A8C")

    # hull, listing bow-down to the left: a trapezoid rotated about its middle
    c.poly([(0.06, 0.72), (0.30, 0.50), (0.88, 0.44), (0.94, 0.60),
            (0.62, 0.74), (0.20, 0.80)], "#C2703A")
    # the swamped deck face, visible because the boat is rolled toward us
    c.poly([(0.12, 0.70), (0.32, 0.53), (0.84, 0.48), (0.88, 0.57),
            (0.58, 0.68), (0.22, 0.75)], "#A85E2F")
    # cabin, tilted with the hull
    c.poly([(0.38, 0.50), (0.60, 0.455), (0.64, 0.555), (0.42, 0.60)],
           "#E4E9EC")
    for i in range(3):
        c.poly([(0.415 + i * 0.062, 0.515 - i * 0.008),
                (0.455 + i * 0.062, 0.508 - i * 0.008),
                (0.455 + i * 0.062, 0.556 - i * 0.008),
                (0.415 + i * 0.062, 0.562 - i * 0.008)], "#2A6377")
    # a broken mast, snapped and leaning into the water
    c.bar(0.66, 0.470, 0.80, 0.300, 0.022, "#8A5A34")

    # water over the gunwale: the surface cuts across the deck
    c.wave(0.66, 0.020, "#2F7387", thickness=0.24)
    c.wave(0.78, 0.016, "#276273", thickness=0.22)
    c.wave(0.90, 0.012, "#1B4A59", thickness=0.14)


def p_protest(c):
    """A crowd with placards. Heads are plain discs; no faces anywhere."""
    c.bg("#D2683A")
    c.band(0.0, 0.22, "#DE7A2C")
    c.sunburst(0.5, 0.10, "#E08A45", count=10, r0=0.16, r1=0.75)
    # placards behind
    for fx, fy, fw, fh, col in ((0.10, 0.18, 0.20, 0.20, "#F4F0E8"),
                                (0.38, 0.10, 0.22, 0.22, ACCENT),
                                (0.68, 0.20, 0.20, 0.18, "#F4F0E8")):
        c.rect(fx, fy, fw, fh, col)
        c.rect(fx + fw / 2 - 0.008, fy + fh, 0.016, 0.28, "#7A3A1C")
    # scribbles on the placards, flat bars
    for fx, fy, fw in ((0.13, 0.235, 0.14), (0.13, 0.285, 0.10),
                       (0.415, 0.155, 0.15), (0.415, 0.205, 0.11),
                       (0.71, 0.245, 0.14), (0.71, 0.295, 0.09)):
        c.rect(fx, fy, fw, 0.022, "#3A2116" if fy > 0.2 else "#F4F0E8")
    # crowd: shoulders and discs
    for i, fx in enumerate((0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92)):
        h = 0.62 if i % 2 == 0 else 0.68
        c.poly([(fx - 0.075, 1.0), (fx - 0.055, h + 0.06), (fx + 0.055, h + 0.06),
                (fx + 0.075, 1.0)], ["#8C3B22", "#A8452A", "#7A321C"][i % 3])
        c.dot(fx, h, 0.042, "#4A2416")
    c.rect(0.0, 0.96, 1.0, 0.04, "#8C3B22")


def p_shipfire(c):
    """A cargo ship burning off the coast, crew already gone."""
    c.bg("#33414F")
    c.band(0.0, 0.26, "#3F4F5F")
    c.smoke(0.34, 0.26, count=4, spread=0.14, size=0.080, colour="#7C8A96")
    c.smoke(0.60, 0.30, count=3, spread=0.11, size=0.065, colour="#6C7A86")
    # hull, sitting in the water
    c.poly([(0.04, 0.66), (0.94, 0.66), (0.88, 0.82), (0.12, 0.82)], "#1E2A36")
    c.rect(0.04, 0.635, 0.90, 0.030, ACCENT)
    # deck cargo, forward of the fire
    for i in range(3):
        c.rect(0.08 + i * 0.125, 0.565, 0.100, 0.070,
               ["#4E6172", "#5A6E80", "#445565"][i % 3])
    # superstructure, aft: a bridge block standing on the deck, with a funnel
    c.rect(0.66, 0.44, 0.19, 0.225, "#D3DAE0")
    c.rect(0.66, 0.44, 0.19, 0.030, "#8E9AA3")
    c.rect(0.69, 0.50, 0.13, 0.045, "#1E2A36")
    c.rect(0.70, 0.585, 0.055, 0.080, "#2A3642")
    # fire amidships, licking up past the bridge
    c.flame(0.47, 0.58, 0.34, 0.40, ACCENT, lean=0.05)
    c.flame(0.47, 0.58, 0.18, 0.24, "#F2A03C", lean=0.02)
    c.flame(0.60, 0.57, 0.16, 0.22, "#E2673A", lean=0.07)
    # sea
    c.wave(0.84, 0.020, "#2A3844", thickness=0.20)
    c.wave(0.92, 0.014, "#22303B", thickness=0.14)


PANELS = {
    "cop31": p_cop31,
    "factory": p_factory,
    "mercury": p_mercury,
    "belgium": p_belgium,
    "brazil": p_brazil,
    "missile": p_missile,
    "boat": p_boat,
    "protest": p_protest,
    "shipfire": p_shipfire,
}


def draw_panel(draw, name, box):
    """Draw one panel, clipped hard to its box.

    The pictures reach past their own edges on purpose - a sunburst wants to
    run off the tile, water wants to run off the bottom - so each is drawn on
    a surface of exactly the panel's size and pasted in.  Without this the
    rays from one tile would lie across the headlines of the next, which is
    how a page ends up with text nobody can read.
    """
    x, y, w, h = [int(round(v)) for v in box]
    w, h = max(w, 1), max(h, 1)
    layer = Image.new("RGB", (w, h), "#000000")
    PANELS[name](Canvas(ImageDraw.Draw(layer), (0, 0, w, h)))
    draw._image.paste(layer, (x, y))
    return layer
