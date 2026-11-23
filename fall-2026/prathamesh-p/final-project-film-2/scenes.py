"""scenes.py: Honest Shortlist final project film (show-tell style, Claude palette, flat drawings).

The shared components (card, stamp, tag, block, arrow, panel, CONSTRUCTED label, Pace) are copied unchanged
from the pitch film's scenes.py (branch prathamesh-p-final-project-film, 65ff4a0). The rules it follows:
  * every drawing of the planned system, a comparison or a plan carries CONSTRUCTED from frame 0;
  * real console text sits in dark panels, verbatim or shortened with an ellipsis, with no local paths;
  * the SEEDED demo says SEEDED; terracotta only on dots; Pace keeps animations off the clip midpoint;
  * every scene adds a new non-text shape after its first frame (Gate A); clips end inside the measured audio;
  * scene classes are written literally as "class B<nn>_<Name>" subclassing Scene (run.sh finds them by regex).
"""
from manim import *
import numpy as np
import json as _json, os as _os, glob as _glob

STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
KRAFT_T, KRAFT_L, KRAFT_R = "#F3E9D8", "#DCC9AA", "#C7AE86"
DARK_TOP, DARK_L = "#3A3530", "#26221F"
BAR1, BAR2 = "#8B8F96", "#B4AFA6"
SERIF = "EB Garamond"
MONO = "PT Mono"
config.background_color = STAGE

# PT Mono ships with the toolkit but is not installed on this Windows machine: register it from file.
try:
    import manimpango as _mp
    _home = _os.environ.get("ART_HOME") or "C:/info7375/brutalist.art-latest"
    for _f in _glob.glob(_os.path.join(_home, "runtime", "fonts", "PT_Mono", "*.ttf")):
        _mp.register_font(_f)
    if MONO not in _mp.list_fonts():
        MONO = "Consolas"
except Exception:
    MONO = "Consolas"

# ── pacing: the measured narration is the clock ─────────────────────────────────────────────────
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json"), encoding="utf-8"))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
except Exception:
    _TARGET = {}


def _elapsed(scene):
    rt = getattr(getattr(scene, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


class Pace:
    """play(frac, ...) starts an animation at frac x the beat's audio length, but never lets it overlap the
    midpoint window [T/2 - 0.5, T/2 + 0.5]; finish() holds to 0.06 s before the end of the audio."""

    def __init__(self, scene):
        self.s = scene
        self.T = _TARGET.get(type(scene).__name__.split("_")[0], 0) or 10.0
        self.lo, self.hi = self.T / 2 - 0.5, self.T / 2 + 0.5

    def play(self, frac, *anims, rt=0.7):
        now = _elapsed(self.s)
        start = max(now, frac * self.T)
        if start < self.hi and start + rt > self.lo:          # would cross the midpoint window
            if self.lo - start >= 0.3:
                rt = self.lo - start                            # shrink to land before it
            else:
                start = self.hi                                 # or start after it
        room = self.T - 0.15 - start
        rt = max(0.2, min(rt, room))
        if start - now > 0.04:
            self.s.wait(start - now)
        self.s.play(*anims, run_time=rt)

    def finish(self):
        left = self.T - 0.06 - _elapsed(self.s)
        if left > 0.04:
            self.s.wait(left)


# ── shared components ────────────────────────────────────────────────────────────────────────────
def T(s, size=36, color=INK, bold=False, font=None):
    return Text(s, font=font or SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


def constructed():
    """The CONSTRUCTED label, top-left, present from frame 0 on every mocked-up beat."""
    d = Dot([-5.95, 2.95, 0], radius=0.08, color=TERRA)
    t = T("CONSTRUCTED", 32).next_to(d, RIGHT, buff=0.3)
    return VGroup(d, t)


def tag(s, x, y, size=34):
    """A label with a terracotta dot to its left (labels sit beside, never inside, an outline)."""
    d = Dot([x, y, 0], radius=0.07, color=TERRA)
    t = T(s, size).next_to(d, RIGHT, buff=0.3)
    return VGroup(d, t)


def card(x, y, w=3.0, h=2.2, rows=3, empty_last=False):
    """A posting / shortlist card: kraft offset shadow, cream face, ink outline, ghost scribble rows."""
    sh = RoundedRectangle(corner_radius=0.12, width=w, height=h, fill_color=KRAFT_R, fill_opacity=1,
                          stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    face = RoundedRectangle(corner_radius=0.12, width=w, height=h, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    gap = h / (rows + 1)
    lines = VGroup()
    for i in range(rows):
        yy = y + h / 2 - gap * (i + 1)
        if empty_last and i == rows - 1:
            ln = DashedLine([x - w / 2 + 0.3, yy, 0], [x + w / 2 - 0.3, yy, 0], color=BAR2, stroke_width=4, dash_length=0.12)
        else:
            ln = Line([x - w / 2 + 0.3, yy, 0], [x + w / 2 - 0.3 - 0.5 * (i % 2), yy, 0], color=GHOST, stroke_width=8)
        lines.add(ln)
    g = VGroup(sh, face, lines)
    g.rows_y = [y + h / 2 - gap * (i + 1) for i in range(rows)]
    return g


def stamp(kind, x, y, r=0.3):
    """A round stamp: check (supported), cross (contradicted), dash (insufficient)."""
    ring = Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    s = r * 0.55
    if kind == "check":
        mark = VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.7, 0], color=INK, stroke_width=7),
                      Line([x - s * 0.3, y - s * 0.7, 0], [x + s, y + s * 0.8, 0], color=INK, stroke_width=7))
    elif kind == "cross":
        mark = VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=7),
                      Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=7))
    else:
        mark = Line([x - s, y, 0], [x + s, y, 0], color=INK, stroke_width=8)
    return VGroup(ring, mark)


def block(x, y, w=1.5, h=0.9, fill=KRAFT_R):
    """A kraft block on a dark plinth (a pale block alone fails Gate V contrast)."""
    plinth = Rectangle(width=w + 0.2, height=0.16, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([x, y - h / 2 - 0.08, 0])
    body = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    lid = Rectangle(width=w, height=h * 0.22, fill_color=KRAFT_T, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h * 0.39, 0])
    return VGroup(plinth, body, lid)


def box(x, y, w=4.2, h=2.4):
    """An open kraft box seen from the front: back wall, floor line, front lip."""
    # Grey back wall: a large pale kraft wall failed Gate V low-contrast (0.24 < 0.30) in B02 and B09
    # (show-tell gate trap (3): "use DIM grey for big backing shapes").
    back = Rectangle(width=w, height=h, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    lip = Rectangle(width=w + 0.3, height=0.45, fill_color=KRAFT_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y - h / 2 + 0.22, 0])
    return VGroup(back, lip)


def arrow(a, b, color=INK):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), color=color, stroke_width=6, buff=0.15,
                 max_tip_length_to_length_ratio=0.18)


def panel(x, y, w, h):
    """A dark terminal panel for REAL text lines."""
    return RoundedRectangle(corner_radius=0.1, width=w, height=h, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def mono(s, size=32):
    return T(s, size, color=CARD, font=MONO)


def board(x, y):
    """A job-board stack: three offset kraft sheets."""
    return VGroup(*[Rectangle(width=1.3, height=1.6, fill_color=c, fill_opacity=1, stroke_color=INK, stroke_width=4)
                    .move_to([x + 0.12 * i, y - 0.12 * i, 0]) for i, c in enumerate((KRAFT_L, KRAFT_T, CARD))])




def fit(m, maxw=11.4):
    """Shrink a text group only if it would leave the safe area (keeps size where it already fits)."""
    if m.width > maxw:
        left = m.get_left()[0]
        m.scale_to_fit_width(maxw)
        m.shift(RIGHT * (left - m.get_left()[0]))
    return m


def mono_rows(rows, x_left, y_top, step=0.55, size=32):
    ms = VGroup(*[mono(r, size).move_to([0, y_top - step * i, 0]) for i, r in enumerate(rows)])
    for m in ms:
        m.align_to(np.array([x_left, 0, 0]), LEFT)
    return ms


def status(s, x, y, size=32):
    return T(s, size, bold=True).move_to([x, y, 0])


# ── beats ────────────────────────────────────────────────────────────────────────────────────────
class B00_Title(Scene):
    def construct(self):
        p = Pace(self)
        title = T("Honest Shortlist", 80, bold=True).move_to([0, 1.75, 0])
        rule = Rectangle(width=6.0, height=0.12, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0, 0.95, 0])
        name = T("Prathamesh Pathak", 46).move_to([0, 0.25, 0])
        film = T("Final project film · INFO 7375 · 2026-11-23", 36).move_to([0, -0.5, 0])
        d1 = T("Narration: synthetic voice (Kokoro af_bella)", 36).move_to([0, -1.6, 0])
        d2 = T("reading my script", 36).move_to([0, -2.2, 0])
        self.add(title)
        p.play(0.04, GrowFromCenter(rule), rt=0.6)
        p.play(0.12, FadeIn(name), FadeIn(film), rt=0.6)
        p.play(0.22, FadeIn(d1), FadeIn(d2), rt=0.6)
        ends = VGroup(Dot([-3.15, 0.95, 0], radius=0.12, color=TERRA), Dot([3.15, 0.95, 0], radius=0.12, color=TERRA))
        p.play(0.66, GrowFromCenter(ends), rt=0.4)
        p.finish()


class B01_Card(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(-3.0, -0.45, w=4.4, h=3.4, rows=3)
        p.play(0.02, FadeIn(c), rt=0.6)
        sl = T("sponsorship", 34).next_to(c, UP, buff=0.25).align_to(c, LEFT)
        p.play(0.12, FadeIn(sl), rt=0.4)
        slip = card(3.2, 1.0, w=4.4, h=1.3, rows=1)
        sq = T("the sentence it rests on", 32).next_to(slip, UP, buff=0.25)
        a = arrow((-0.7, c.rows_y[0]), (0.95, 1.0))
        p.play(0.24, FadeIn(slip), GrowArrow(a), FadeIn(sq), rt=0.7)
        st = stamp("dash", -0.15, c.rows_y[2], r=0.36)
        sil = T("posting doesn't say", 34).move_to([3.0, c.rows_y[2], 0])
        p.play(0.62, GrowFromCenter(st), FadeIn(sil), rt=0.6)
        p.finish()


class B02_Tally(Scene):
    def construct(self):
        p = Pace(self)
        head = T("7 network postings · 3 employers", 36).move_to([0, 2.7, 0])
        self.add(head)
        xs = np.linspace(-5.4, 5.4, 7)
        cards = VGroup(*[card(x, 0.9, w=1.35, h=1.8, rows=3) for x in xs])
        p.play(0.03, LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.12), rt=1.0)
        crosses = VGroup(*[stamp("cross", x, -0.55) for x in xs[:2]])
        dashes = VGroup(*[stamp("dash", x, -0.55) for x in xs[2:]])
        l1 = T("2 clearance required (inferred)", 32).move_to([-3.4, -1.45, 0])
        p.play(0.2, GrowFromCenter(crosses), FadeIn(l1), rt=0.6)
        l2 = T("5 silent", 32).move_to([2.7, -1.45, 0])
        p.play(0.36, GrowFromCenter(dashes), FadeIn(l2), rt=0.6)
        zero = T("0 offer sponsorship", 44, bold=True).move_to([0, -2.35, 0])
        src = T("Reallocation mode run · 2026-10-20", 32).move_to([0, -3.05, 0])
        p.play(0.56, FadeIn(zero), FadeIn(src), rt=0.6)
        p.finish()


class B03_History(Scene):
    def construct(self):
        p = Pace(self)
        h1 = T("Zoox: 1,364 H-1B approvals", 44, bold=True).move_to([0, 2.85, 0])
        h2 = T("80 Days to Stay · 2026-10-20", 32).move_to([0, 2.2, 0])
        self.add(h1)
        p.play(0.03, FadeIn(h2), rt=0.4)
        pn = panel(0, -0.65, 11.4, 3.7)
        p.play(0.1, FadeIn(pn), rt=0.4)
        rows = ["silent  0 sentence(s)  zoox", "  Senior Network Security Engineer",
                "silent  0 sentence(s)  zoox", "  Staff Network Security Architect",
                "silent  0 sentence(s)  zoox", "  Senior Manager, Network Engineering & …"]
        ms = mono_rows(rows, -5.2, 0.75)
        p.play(0.18, FadeIn(ms), rt=0.6)
        dots = VGroup(*[Dot([-5.55, 0.75 - 1.1 * i, 0], radius=0.08, color=TERRA) for i in range(3)])
        p.play(0.62, GrowFromCenter(dots), rt=0.4)
        p.finish()


class B04_Alerts(Scene):
    def construct(self):
        p = Pace(self)
        top = T("LinkedIn alerts: documented, not tested by me", 34).move_to([0, 2.7, 0])
        box_ = DashedVMobject(Rectangle(width=11.4, height=0.9, stroke_color=BAR1, stroke_width=4), num_dashes=60).move_to([0, 2.7, 0])
        self.add(top)
        p.play(0.03, Create(box_), rt=0.6)
        seen = T("what I saw · LinkedIn search · 2026-10-31", 36, bold=True).move_to([0, 1.3, 0])
        rule = Rectangle(width=8.0, height=0.08, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0, 0.8, 0])
        p.play(0.36, FadeIn(seen), GrowFromCenter(rule), rt=0.6)
        rows = [tag("match reasoning: behind a click", -4.6, 0.0),
                tag("'without sponsorship': not flagged", -4.6, -0.9),
                tag("closed postings: still listed", -4.6, -1.8)]
        p.play(0.44, LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), rt=0.9)
        p.finish()


class B05_Chat(Scene):
    def construct(self):
        p = Pace(self)
        lh = T("chat, pasted posting · 2026-10-31", 32).move_to([-3.2, 2.7, 0])
        rh = T("my agent v1 · same posting", 32).move_to([3.4, 2.7, 0])
        self.add(lh, rh)
        cl = card(-3.2, 0.85, w=5.2, h=2.4, rows=3)
        cr = card(3.4, 0.85, w=4.4, h=2.4, rows=3)
        p.play(0.03, FadeIn(cl), FadeIn(cr), rt=0.6)
        v1 = T("Not relevant", 40, bold=True).move_to([-3.2, -0.95, 0])
        v2 = T("8+ years", 32).move_to([-3.2, -1.6, 0])
        v3 = T("sponsorship: posting is silent", 32).move_to([-3.2, -2.2, 0])
        p.play(0.12, FadeIn(v1), FadeIn(v2), FadeIn(v3), rt=0.6)
        r1 = T("relevant", 40, bold=True).move_to([3.4, -0.95, 0])
        p.play(0.72, FadeIn(r1), rt=0.4)
        ul = Rectangle(width=2.2, height=0.08, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([3.4, -1.35, 0])
        dot = Dot([2.0, -0.95, 0], radius=0.1, color=TERRA)
        foot = T("Zoox · Senior Network Security Engineer", 32).move_to([0, -3.15, 0])
        p.play(0.8, GrowFromCenter(ul), GrowFromCenter(dot), FadeIn(foot), rt=0.5)
        p.finish()


class B06_Dropped(Scene):
    def construct(self):
        p = Pace(self)
        lab = T("real console · 2026-10-20", 32).move_to([0, 2.95, 0])
        pn = panel(0, 1.65, 11.4, 1.7)
        self.add(lab)
        p.play(0.02, FadeIn(pn), rt=0.4)
        ms = mono_rows(["[lever] Shield AI: found 22 jobs", "[lever-full] shieldai: 653 postings"], -5.2, 2.0)
        p.play(0.08, FadeIn(ms), rt=0.5)
        full = 10.0
        b1 = Rectangle(width=full * 22 / 653, height=0.55, fill_color=INK, fill_opacity=1, stroke_width=0)
        b1.move_to([-5.0 + b1.width / 2, -0.35, 0])
        b2 = Rectangle(width=full, height=0.55, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
        b2.move_to([-5.0 + full / 2, -1.25, 0])
        n1 = T("22", 34, bold=True).move_to([-5.7, -0.35, 0])
        n2 = T("653", 34, bold=True).move_to([-5.75, -1.25, 0])
        p.play(0.3, GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT), FadeIn(n1), FadeIn(n2), rt=0.8)
        drop = T("631 dropped · no error", 40, bold=True).move_to([0, -2.4, 0])
        dot = Dot([-3.35, -2.4, 0], radius=0.1, color=TERRA)
        p.play(0.6, FadeIn(drop), GrowFromCenter(dot), rt=0.5)
        p.finish()


class B07_Grid(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        cols = [-0.3, 2.2, 4.7]
        heads = VGroup(*[T(s, 32).move_to([x, 2.1, 0]) for s, x in zip(["watches", "evidence", "says silent"], cols)])
        rows_y = [1.0, -0.4, -1.8]
        names = VGroup(T("LinkedIn alerts", 34).move_to([0, rows_y[0], 0]),
                       T("chat assistant", 34).move_to([0, rows_y[1], 0]),
                       T("Honest Shortlist", 34, bold=True).move_to([0, rows_y[2] + 0.2, 0]),
                       T("(planned)", 32).move_to([0, rows_y[2] - 0.4, 0]))
        for n in names:
            n.align_to(np.array([-6.0, 0, 0]), LEFT)
        p.play(0.03, FadeIn(heads), FadeIn(names), rt=0.6)
        marks = [["check", "dash", "cross"], ["cross", "check", "check"], ["check", "check", "check"]]
        for r, (ry, row) in enumerate(zip(rows_y, marks)):
            p.play(0.12 + 0.12 * r, *[GrowFromCenter(stamp(k, x, ry, r=0.32)) for k, x in zip(row, cols)], rt=0.5)
        dot = Dot([-6.25, rows_y[2] + 0.2, 0], radius=0.09, color=TERRA)
        p.play(0.7, GrowFromCenter(dot), rt=0.3)
        p.finish()


class B08_Pipeline(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        feeds = T("Greenhouse · Lever · Ashby (public)", 34).move_to([0, -2.05, 0])
        p.play(0.02, FadeIn(feeds), rt=0.4)
        xs = np.linspace(-5.15, 5.15, 6)
        names = [("fetch",), ("new only",), ("title rule",), ("extract",), ("label",), ("re-fetch", "approve")]
        st = ["RAN", "RAN", "RAN", "IN MODE", "PLANNED", "PLANNED"]
        blocks = VGroup(*[block(x, 0.2, w=1.3, h=0.9, fill=(KRAFT_R if i < 4 else BAR2)) for i, x in enumerate(xs)])
        p.play(0.08, LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.15), rt=1.0)
        arrows = VGroup(*[arrow((xs[i] + 0.7, 0.2), (xs[i + 1] - 0.7, 0.2)) for i in range(5)])
        labels = VGroup()
        for x, nm in zip(xs, names):
            for j, s in enumerate(nm):
                labels.add(T(s, 32).move_to([x, -0.85 - 0.5 * j, 0]))
        p.play(0.2, *[GrowArrow(a) for a in arrows], FadeIn(labels), rt=0.7)
        stats = VGroup(*[status(s, x, 1.15 + 0.55 * (i % 2)) for i, (s, x) in enumerate(zip(st, xs))])
        p.play(0.3, FadeIn(stats), rt=0.5)
        never = T("never: apply · email · message · log in", 34).move_to([0, -2.9, 0])
        nd = Dot([-4.3, -2.9, 0], radius=0.08, color=TERRA)
        p.play(0.64, FadeIn(never), GrowFromCenter(nd), rt=0.5)
        p.finish()


class B09_LiveRun(Scene):
    def construct(self):
        p = Pace(self)
        lab = T("real · JS2 live run · 2026-11-10 09:52 EST", 34).move_to([0, 2.95, 0])
        pn = panel(0, -0.05, 11.4, 3.5)
        self.add(lab)
        p.play(0.02, FadeIn(pn), rt=0.4)
        rows = ["[loop] status=incomplete exit=3", "boards=4 requests=4/6 seconds=8.757/120",
                "lever-zoox  ok  postings=234 new=31", "...-js2-does-not-exist  failed_http_404",
                "attempts=1  no retry (GATE section 4)"]
        ms = mono_rows(rows, -5.2, 1.2)
        p.play(0.08, FadeIn(ms[:3]), rt=0.5)
        p.play(0.36, FadeIn(ms[3:]), rt=0.5)
        dot = Dot([-5.55, 1.2 - 0.55 * 3, 0], radius=0.09, color=TERRA)
        ring = SurroundingRectangle(VGroup(ms[3], ms[4]), color=CARD, stroke_width=3, buff=0.12)
        p.play(0.7, GrowFromCenter(dot), Create(ring), rt=0.5)
        p.finish()


class B10_NewOnly(Scene):
    def construct(self):
        p = Pace(self)
        pn = panel(0, 2.15, 11.4, 1.0)
        self.add(pn)
        m1 = mono("lever-zoox  ok  postings=234 new=31").move_to([0, 2.15, 0])
        p.play(0.02, FadeIn(m1), rt=0.4)
        cap = T("new vs my 2026-10-31 state (227 IDs)", 34).move_to([0, 1.2, 0])
        p.play(0.1, FadeIn(cap), rt=0.4)
        ring = Rectangle(width=1.9, height=0.07, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([m1.get_right()[0] - 0.95, 1.76, 0])
        p.play(0.2, GrowFromCenter(ring), rt=0.5)
        pn2 = panel(0, -0.9, 11.4, 1.6)
        ms = mono_rows(["Rule.test_road_network_tools_is_not_", "relevant_in_real_day1_data"], -5.2, -0.62)
        p.play(0.56, FadeIn(pn2), FadeIn(ms), rt=0.5)
        ff = tag("false friend: 'Road Network Tools'", -4.0, -2.4)
        p.play(0.66, FadeIn(ff), rt=0.4)
        p.finish()


class B11_Extract(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        im = T("IN MODE · 2026-10-20", 32).move_to([3.6, 2.95, 0])
        pn = panel(0, 1.0, 11.4, 2.0)
        p.play(0.02, FadeIn(im), FadeIn(pn), rt=0.4)
        ms = mono_rows(["has-sentences  2 sentence(s)  shieldai", "Network Engineer (R4843)",
                        "fields=additionalPlain,descriptionPlain,lists"], -5.2, 1.55)
        fit(ms, 10.3)
        p.play(0.08, FadeIn(ms), rt=0.5)
        pl = T("CONSTRUCTED · PLANNED", 32).move_to([0, -0.5, 0])
        xs = [-4.0, 0.0, 4.0]
        sts = [stamp(k, x, -1.45, r=0.38) for k, x in zip(["check", "cross", "dash"], xs)]
        lbs = [T(s, 34).move_to([x, -2.35, 0]) for s, x in zip(["supported", "contradicted", "insufficient (default)"], xs)]
        p.play(0.56, FadeIn(pl), *[GrowFromCenter(s) for s in sts], *[FadeIn(l) for l in lbs], rt=0.7)
        dot = Dot([4.0, -2.95, 0], radius=0.09, color=TERRA)
        p.play(0.8, GrowFromCenter(dot), rt=0.3)
        p.finish()


class B12_Validator(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        rl = T("RAN · JS1 · 2026-10-31", 32).move_to([3.6, 2.95, 0])
        pn = panel(0, 1.05, 11.4, 2.0)
        p.play(0.02, FadeIn(rl), FadeIn(pn), rt=0.4)
        ms = mono_rows(["Validator.test_rejects_uncited_or_", "fabricated_justification", "Ran 50 tests, OK"], -5.2, 1.6)
        p.play(0.06, FadeIn(ms), rt=0.5)
        pl = T("CONSTRUCTED · PLANNED", 32).move_to([0, -0.55, 0])
        b1 = block(-2.4, -1.6, w=2.2, h=0.9, fill=BAR2)
        b2 = block(2.4, -1.6, w=2.2, h=0.9, fill=BAR2)
        a = arrow((-1.2, -1.6), (1.2, -1.6))
        l1 = T("re-fetch", 34).move_to([-2.4, -2.6, 0])
        l2 = T("my approval", 34).move_to([2.4, -2.6, 0])
        p.play(0.56, FadeIn(pl), FadeIn(b1), FadeIn(b2), GrowArrow(a), FadeIn(l1), FadeIn(l2), rt=0.7)
        p.finish()


class B13_Resources(Scene):
    def construct(self):
        p = Pace(self)
        ys = [2.3, 1.2, 0.1, -1.4]
        rows = [("boards: public, no account", None), ("compute: my laptop · Python stdlib", None),
                ("Claude: my Claude Code subscription", "50 judge calls in JS1 · 2026-10-31"),
                ("daily runs, many boards: not measured", None)]
        txt = VGroup()
        for (s, sub), y in zip(rows, ys):
            t = T(s, 36).move_to([0, y, 0]).align_to(np.array([-4.3, 0, 0]), LEFT)
            txt.add(t)
            if sub:
                txt.add(T(sub, 32).move_to([0, y - 0.6, 0]).align_to(np.array([-4.3, 0, 0]), LEFT))
        self.add(txt[0])
        p.play(0.02, FadeIn(txt[1:]), rt=0.5)
        kinds = ["check", "check", "check", "dash"]
        for i, (k, y) in enumerate(zip(kinds, ys)):
            p.play(0.08 + 0.12 * i if i < 3 else 0.82, GrowFromCenter(stamp(k, -5.2, y, r=0.32)), rt=0.4)
        p.finish()


class B14_Baseline(Scene):
    def construct(self):
        p = Pace(self)
        lab = T("real · JS1 experiment · 2026-10-31", 32).move_to([0, 2.95, 0])
        pn = panel(0, 1.3, 11.4, 2.3)
        self.add(lab)
        p.play(0.02, FadeIn(pn), rt=0.4)
        ms = mono_rows(["labels: 20 of 20 'not fit'", "always not_relevant: dev 10/10",
                        "always not_relevant: held-out 10/10"], -5.2, 1.95, step=0.62)
        p.play(0.08, FadeIn(ms), rt=0.5)
        big = T("100%", 72, bold=True).move_to([-2.6, -1.35, 0])
        p.play(0.4, FadeIn(big), rt=0.5)
        st = stamp("cross", 0.4, -1.35, r=0.42)
        nt = T("pass rate alone proved nothing", 34).move_to([0, -2.65, 0])
        p.play(0.7, GrowFromCenter(st), FadeIn(nt), rt=0.5)
        p.finish()


class B15_HeldOut(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        h1 = T("about 40 postings · more boards", 36).move_to([0, 2.15, 0])
        h2 = T("labelled by me before any output", 32).move_to([0, 1.55, 0])
        p.play(0.02, FadeIn(h1), FadeIn(h2), rt=0.5)
        groups = [(-4.3, "entry-level fits"), (0.0, "not fit"), (4.3, "false friends")]
        cards = VGroup()
        labs = VGroup()
        for gx, s in groups:
            for k in range(3):
                cards.add(card(gx - 0.9 + 0.9 * k, 0.15, w=0.8, h=1.1, rows=2))
            labs.add(T(s, 32).move_to([gx, -0.85, 0]))
        p.play(0.12, LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.06), FadeIn(labs), rt=1.0)
        m1 = Rectangle(width=4.0, height=0.45, stroke_color=INK, stroke_width=4).move_to([-3.0, -1.8, 0])
        m2 = Rectangle(width=4.0, height=0.45, stroke_color=INK, stroke_width=4).move_to([3.0, -1.8, 0])
        t1 = T("false positives", 32).move_to([-3.0, -2.55, 0])
        t2 = T("false negatives", 32).move_to([3.0, -2.55, 0])
        p.play(0.62, Create(m1), Create(m2), FadeIn(t1), FadeIn(t2), rt=0.6)
        p.finish()


class B16_Seeded(Scene):
    def construct(self):
        p = Pace(self)
        sl = T("SEEDED · constructed empty response · 2026-11-10", 34, bold=True).move_to([0, 2.95, 0])
        pn = panel(0, 0.9, 11.4, 3.2)
        self.add(sl)
        p.play(0.02, FadeIn(pn), rt=0.4)
        ms = mono_rows(["[loop] *** SEEDED *** status=finished", "exit=0  ashby-openai  ok_empty  new=0",
                        "verify.py [SEEDED]: FAIL", "posting count is 0 but the previous",
                        "snapshot had 826 ids"], -5.2, 2.0)
        p.play(0.06, FadeIn(ms[:2]), rt=0.5)
        p.play(0.18, FadeIn(ms[2:]), rt=0.5)
        wk = T("worked if (planned):", 32, bold=True).move_to([0, -1.15, 0])
        crit = [("most real fits found", -3.1, -1.8), ("no clearance/citizen-only 'relevant'", 3.1, -1.8),
                ("beats always-insufficient", -3.1, -2.5), ("verify catches every planted failure", 3.1, -2.5)]
        cs = VGroup(*[T(s, 32).move_to([x, y, 0]) for s, x, y in crit])
        fit(cs, 12.2)
        p.play(0.56, FadeIn(wk), FadeIn(cs), rt=0.6)
        dot = Dot([-5.55, 2.0 - 0.55 * 2, 0], radius=0.09, color=TERRA)
        p.play(0.84, GrowFromCenter(dot), rt=0.3)
        p.finish()


class B17_Close(Scene):
    def construct(self):
        p = Pace(self)
        l1 = T("zero tolerance: 'relevant' when sponsorship is ruled out", 34).move_to([0.4, 2.5, 0])
        l2 = T("missed real fits: a rate I report", 34).move_to([0.4, 1.5, 0])
        fit(l1, 10.6)
        for l in (l1, l2):
            l.align_to(np.array([-5.1, 0, 0]), LEFT)
        self.add(l1)
        s1 = stamp("cross", -5.7, 2.5, r=0.3)
        p.play(0.03, GrowFromCenter(s1), rt=0.4)
        s2 = stamp("dash", -5.7, 1.5, r=0.3)
        p.play(0.2, FadeIn(l2), GrowFromCenter(s2), rt=0.5)
        title = T("Honest Shortlist", 72, bold=True).move_to([0, -0.6, 0])
        rule = Rectangle(width=6.0, height=0.12, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0, -1.45, 0])
        close = T("every claim carries its evidence", 38).move_to([0, -2.2, 0])
        p.play(0.56, FadeIn(title), GrowFromCenter(rule), FadeIn(close), rt=0.7)
        ends = VGroup(Dot([-3.15, -1.45, 0], radius=0.12, color=TERRA), Dot([3.15, -1.45, 0], radius=0.12, color=TERRA))
        p.play(0.8, GrowFromCenter(ends), rt=0.4)
        p.finish()
