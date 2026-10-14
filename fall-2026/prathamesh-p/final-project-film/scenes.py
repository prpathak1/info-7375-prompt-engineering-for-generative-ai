"""scenes.py: Honest Shortlist pitch film (show-tell style, Claude palette, flat drawings).

All 15 beats are composed from one shared component set: card, stamp, tag, box/block, arrow,
panel (real text), and the CONSTRUCTED label. Gate-trap rules from show-tell SKILL.md that this
file follows:
  * every drawing of the proposed system / a shortlist / an interface carries CONSTRUCTED from frame 0;
  * labels sit beside shapes (never inside an outline), ink only, size >= 32, inside +-6.2 x +-3.3;
  * terracotta only on dots; nothing animates across the clip midpoint (GATE T / Gate V sample it);
  * every scene adds a new non-text shape after its first frame (Gate A);
  * each clip ends inside its beat's measured audio (`actual_duration_s` in beat_sheet.json);
  * scene classes are written literally as "class B<nn>_<Name>" subclassing Scene, because run.sh finds
    them with a text regex (so never write that pattern with the parenthesis in a comment, either).
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


# ── beats ────────────────────────────────────────────────────────────────────────────────────────
class B00_Title(Scene):
    def construct(self):
        p = Pace(self)
        title = T("Honest Shortlist", 80, bold=True).move_to([0, 1.55, 0])
        rule = Rectangle(width=6.0, height=0.12, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0, 0.75, 0])
        name = T("Prathamesh Pathak", 46).move_to([0, 0.05, 0])
        role = T("Target role: AI / agent engineer (applied AI)", 36).move_to([0, -0.75, 0])
        disc = T("Narration: synthetic voice (Kokoro) reading my script", 36).move_to([0, -1.85, 0])
        self.add(title)
        p.play(0.04, GrowFromCenter(rule), rt=0.6)
        p.play(0.12, FadeIn(name), FadeIn(role), rt=0.6)
        p.play(0.22, FadeIn(disc), rt=0.6)
        ends = VGroup(Dot([-3.15, 0.75, 0], radius=0.12, color=TERRA), Dot([3.15, 0.75, 0], radius=0.12, color=TERRA))
        p.play(0.66, GrowFromCenter(ends), rt=0.4)
        p.finish()


class B01_Silence(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(-2.4, 0.1, w=4.2, h=3.6, rows=4, empty_last=True)
        p.play(0.02, FadeIn(c), rt=0.6)
        lbl = T("sponsorship", 34).move_to([1.3, c.rows_y[3], 0])
        q = T("?", 64, bold=True).move_to([3.6, c.rows_y[3], 0])
        p.play(0.2, FadeIn(lbl), rt=0.5)
        persona = tag("fictional F-1 student", -4.3, -2.6)
        p.play(0.3, FadeIn(persona), rt=0.5)
        ring = Circle(radius=0.55, stroke_color=INK, stroke_width=5).move_to(q.get_center())
        p.play(0.62, FadeIn(q), Create(ring), rt=0.7)
        p.finish()


class B02_Watch(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        boards = VGroup(board(-5.0, 1.2), board(-5.0, -1.2))
        bl = T("job boards", 34).move_to([-4.9, -2.65, 0])
        p.play(0.02, FadeIn(boards), FadeIn(bl), rt=0.6)
        gate = VGroup(Rectangle(width=0.25, height=1.4, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([-2.6, 0.95, 0]),
                      Rectangle(width=0.25, height=1.4, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([-2.6, -0.95, 0]))
        a1 = arrow((-3.9, 0), (-1.0, 0))
        p.play(0.15, FadeIn(gate), GrowArrow(a1), rt=0.7)
        bx = box(2.4, -0.1, w=5.2, h=3.4)
        cards = VGroup(*[card(0.9 + 1.5 * i, 0.3, w=1.2, h=1.6, rows=2) for i in range(3)])
        rl = T("GitHub repo", 34).move_to([2.4, -2.45, 0])
        p.play(0.27, FadeIn(bx), FadeIn(rl), rt=0.6)
        p.play(0.62, LaggedStart(*[FadeIn(k) for k in cards], lag_ratio=0.3), rt=1.0)
        p.finish()


class B03_Labels(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(-2.4, 0.0, w=4.4, h=4.0, rows=4)
        p.play(0.02, FadeIn(c), rt=0.6)
        ys = c.rows_y
        s1, s2, s3 = stamp("check", 0.5, ys[0]), stamp("cross", 0.5, ys[1]), stamp("dash", 0.5, ys[2])
        l1 = T("supported", 34).next_to(s1, RIGHT, buff=0.35)
        l2 = T("contradicted", 34).next_to(s2, RIGHT, buff=0.35)
        l3 = T("insufficient", 34).next_to(s3, RIGHT, buff=0.35)
        p.play(0.12, GrowFromCenter(s1), FadeIn(l1), rt=0.5)
        p.play(0.22, GrowFromCenter(s2), FadeIn(l2), rt=0.5)
        p.play(0.32, GrowFromCenter(s3), FadeIn(l3), rt=0.5)
        s4 = stamp("check", 0.5, ys[3])
        bd = board(5.0, -2.2).scale(0.6)
        loop = CurvedArrow(np.array([1.0, ys[3] - 0.1, 0]), np.array([4.4, -2.0, 0]), color=INK, stroke_width=6, angle=-PI / 3)
        p.play(0.66, GrowFromCenter(s4), FadeIn(bd), Create(loop), rt=0.9)
        p.finish()


class B04_NotYet(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(-4.0, 0.2, w=3.6, h=3.2, rows=4, empty_last=True)
        p.play(0.02, FadeIn(c), rt=0.5)
        st = stamp("dash", -1.6, c.rows_y[3])
        sl = T("insufficient", 34).move_to([0.0, c.rows_y[3], 0])
        p.play(0.12, GrowFromCenter(st), FadeIn(sl), rt=0.5)
        t1 = tag("LinkedIn job alerts", 1.7, 1.4)
        t2 = tag("chat assistant", 1.7, 0.6)
        p.play(0.3, FadeIn(t1), FadeIn(t2), rt=0.6)
        clock = VGroup(Circle(radius=0.4, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1),
                       Line([0, 0, 0], [0, 0.28, 0], color=INK, stroke_width=6),
                       Line([0, 0, 0], [0.22, 0, 0], color=INK, stroke_width=6)).move_to([-1.6, -2.1, 0])
        nl = T("not yet examined · JS1, Oct 31", 34).next_to(clock, RIGHT, buff=0.35)
        p.play(0.62, FadeIn(clock), FadeIn(nl), rt=0.7)
        p.finish()


class B05_SixtySeconds(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        dial = VGroup(Circle(radius=0.75, stroke_color=INK, stroke_width=6, fill_color=CARD, fill_opacity=1),
                      Line([0, 0, 0], [0, 0.55, 0], color=INK, stroke_width=7)).move_to([-5.0, 1.0, 0])
        dl = T("60 s", 36).next_to(dial, DOWN, buff=0.3)
        p.play(0.02, FadeIn(dial), FadeIn(dl), rt=0.5)
        readme = card(-2.4, 1.0, w=2.2, h=2.4, rows=4)
        rl = T("README", 34).next_to(readme, DOWN, buff=0.3)
        p.play(0.14, FadeIn(readme), FadeIn(rl), rt=0.5)
        term = panel(-2.4, -2.1, 3.6, 0.8)
        cmd = mono("$ run sample", 32).move_to([-2.4, -2.1, 0])
        p.play(0.26, FadeIn(term), FadeIn(cmd), rt=0.5)
        sc = card(1.3, 1.0, w=2.4, h=2.4, rows=3)
        evt = VGroup(*[Rectangle(width=2.6, height=0.42, fill_color=(KRAFT_T if i != 2 else KRAFT_R), fill_opacity=1,
                                 stroke_color=INK, stroke_width=3).move_to([4.6, 1.8 - 0.55 * i, 0]) for i in range(4)])
        fl = T("failures", 34).move_to([4.6, -0.75, 0])
        fdot = Dot([4.6, 0.7, 0], radius=0.09, color=TERRA)
        links = VGroup(*[arrow((2.55, y), (3.25, y)) for y in (1.8, 1.25)])
        p.play(0.62, FadeIn(sc), FadeIn(evt), FadeIn(fl), rt=0.7)
        p.play(0.76, Create(links), GrowFromCenter(fdot), rt=0.6)
        p.finish()


def _skill_row(scene, p, items, start=0.04, step=0.1):
    xs = np.linspace(-4.0, 4.0, len(items)) if len(items) > 1 else [0.0]
    groups = []
    for i, (name, x) in enumerate(zip(items, xs)):
        b = block(x, 0.4, w=2.0, h=1.3)
        page = card(x, -1.45, w=1.3, h=0.9, rows=2)
        lab = T(name, 34).move_to([x, 1.75, 0])
        groups.append(VGroup(b, page, lab))
        p.play(start + step * i, FadeIn(b), FadeIn(lab), rt=0.5)
    return groups


class B06_Skills1(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        g = _skill_row(self, p, ["contract · JS1", "loop · JS2", "permissions · JS2"])
        ev = T("evidence: tests, traces", 34).move_to([0, -2.6, 0])
        p.play(0.62, *[FadeIn(x[1]) for x in g], FadeIn(ev), rt=0.8)
        p.finish()


class B07_Skills2(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        items = ["grounding · JS3", "memory · JS4", "evaluation", "human gate · JS5"]
        xs = [-4.65, -1.55, 1.55, 4.65]
        for i, (name, x) in enumerate(zip(items, xs)):
            b = block(x, 0.5, w=1.9, h=1.2)
            lab = T(name, 32).move_to([x, 1.75, 0])
            p.play(0.04 + 0.09 * i, FadeIn(b), FadeIn(lab), rt=0.45)
        sc = card(4.65, -1.75, w=1.6, h=1.1, rows=2)
        seal = Dot([5.3, -1.35, 0], radius=0.14, color=TERRA)
        p.play(0.64, FadeIn(sc), rt=0.5)
        p.play(0.78, GrowFromCenter(seal), rt=0.4)
        p.finish()


class B08_Fence(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        posts = VGroup(*[Rectangle(width=0.22, height=3.6, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([0.0, 0.0, 0]),
                         Rectangle(width=0.22, height=3.6, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([0.6, 0.0, 0])])
        p.play(0.02, FadeIn(posts), rt=0.5)
        boards = VGroup(*[board(-5.3 + 1.5 * i, 0.7).scale(0.7) for i in range(3)])
        bl = T("Greenhouse · Lever · Ashby", 34).move_to([-3.6, -1.0, 0])
        p.play(0.12, FadeIn(boards), FadeIn(bl), rt=0.6)
        # (fix 2) the short arrow here was removed: its small arrowhead is the likely 39 px "text run"
        # GATE T flagged at the B08 midpoint (type_check.py notes arrowheads slip its filters).
        # size 36: at 32 this all-lowercase line measured 39 px < GATE T's 41 px floor at 2160p
        nl = T("never: apply · email · message · log in", 36).move_to([2.45, -2.3, 0])
        stop = VGroup(*[stamp("cross", 1.6 + 1.25 * i, 0.7, r=0.32) for i in range(4)])
        p.play(0.62, LaggedStart(*[GrowFromCenter(s) for s in stop], lag_ratio=0.2), FadeIn(nl), rt=0.9)
        p.finish()


class B09_Baseline(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        t1 = box(-3.8, 0.3, w=3.4, h=2.4)
        l1 = T("run 1: 0 new", 34).move_to([-3.8, -1.55, 0])
        p.play(0.02, FadeIn(t1), FadeIn(l1), rt=0.6)
        t2 = box(1.4, 0.3, w=3.4, h=2.4)
        l2 = T("run 2", 34).move_to([1.4, -1.55, 0])
        p.play(0.16, FadeIn(t2), FadeIn(l2), rt=0.6)
        new = VGroup(*[card(0.7 + 1.3 * i, 0.55, w=1.0, h=1.3, rows=2) for i in range(2)])
        p.play(0.28, LaggedStart(*[FadeIn(k) for k in new], lag_ratio=0.3), rt=0.7)
        diff = card(5.0, 0.3, w=1.6, h=2.2, rows=3)
        marks = VGroup(*[Dot([4.3, diff.rows_y[i], 0], radius=0.08, color=TERRA) for i in (0, 2)])
        sl = T("SEEDED if not day 2", 34).move_to([2.6, -2.6, 0])
        p.play(0.62, FadeIn(diff), FadeIn(sl), rt=0.6)
        p.play(0.76, GrowFromCenter(marks), rt=0.4)
        p.finish()


class B10_FalseFriends(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(-3.2, 0.3, w=3.8, h=3.4, rows=4, empty_last=True)
        p.play(0.02, FadeIn(c), rt=0.5)
        v = tag("Visa", 0.0, 1.6)
        w = tag("authorized to work", 0.0, 0.7)
        p.play(0.1, FadeIn(v), rt=0.4)
        p.play(0.2, FadeIn(w), rt=0.4)
        st = stamp("dash", -0.5, c.rows_y[3])
        sl = T("insufficient", 34).next_to(st, RIGHT, buff=0.35)
        p.play(0.3, GrowFromCenter(st), FadeIn(sl), rt=0.5)
        co = block(4.4, -1.4, w=2.0, h=1.2, fill=BAR2)
        cl = T("public H-1B employer data", 32).move_to([2.8, -2.75, 0])
        p.play(0.66, FadeIn(co), FadeIn(cl), rt=0.7)
        p.finish()


class B11_Have(Scene):
    def construct(self):
        p = Pace(self)
        nl = T("new to me", 36).move_to([-4.6, 2.6, 0])
        tags = VGroup(*[RoundedRectangle(corner_radius=0.1, width=2.2, height=0.5, stroke_color=BAR1, stroke_width=4,
                                         fill_opacity=0).move_to([-4.6, 1.7 - 0.75 * i, 0]) for i in range(4)])
        self.add(nl)
        p.play(0.02, LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.2), rt=0.8)
        pn = panel(2.1, -0.3, 8.0, 4.9)
        rl = T("real · git log", 34).move_to([2.1, 2.6, 0])
        p.play(0.14, FadeIn(pn), FadeIn(rl), rt=0.5)
        rows = [("ce1a06c  2026-09-27", 1.6), ("Week 01 video: expected vs", 1.1), ("observed (prathamesh-p)", 0.6),
                ("1b5a589  2026-10-03", -0.4), ("Final sample run + recipe", -0.9), ("0.1.2 (DRAFT, sample run", -1.4),
                ("passing)", -1.9)]
        ms = [mono(s).move_to([0, y, 0]) for s, y in rows]
        for m in ms:
            m.align_to(np.array([-1.5, 0, 0]), LEFT)
        p.play(0.24, *[FadeIn(m) for m in ms[:3]], rt=0.5)
        p.play(0.33, *[FadeIn(m) for m in ms[3:]], rt=0.5)
        dots = VGroup(Dot([-2.45, 1.6, 0], radius=0.08, color=TERRA), Dot([-2.45, -0.4, 0], radius=0.08, color=TERRA))
        p.play(0.66, GrowFromCenter(dots), rt=0.4)
        p.finish()


class B12_Measure(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(-2.6, 0.3, w=3.6, h=3.2, rows=4, empty_last=True)
        p.play(0.02, FadeIn(c), rt=0.5)
        sheet = VGroup(*[Rectangle(width=2.4, height=0.5, fill_color=CARD, fill_opacity=1, stroke_color=BAR1, stroke_width=3)
                         .move_to([2.2, 1.2 - 0.6 * i, 0]) for i in range(4)])
        p.play(0.14, FadeIn(sheet), rt=0.5)
        ml = T("to measure · JS1", 34).move_to([2.2, -1.75, 0])
        p.play(0.24, FadeIn(ml), rt=0.4)
        d = Dot([0.6, 1.2, 0], radius=0.09, color=TERRA)
        p.play(0.68, GrowFromCenter(d), rt=0.4)
        p.finish()


class B13_ExistsWill(Scene):
    def construct(self):
        p = Pace(self)
        el = T("exists today · 2026-10-14", 34).move_to([0, 2.95, 0])
        pn = panel(0, 1.25, 11.6, 2.75)
        self.add(el)
        p.play(0.02, FadeIn(pn), rt=0.4)
        rows = ["[smoke] GATE AUDIO passed — mean_volume",
                "-24.2 dB (floor -40 dB)",
                "[smoke] SMOKE PASS — … built a real,",
                "watchable slate cut end to end."]
        ms = VGroup(*[mono(r).move_to([0, 2.2 - 0.6 * i, 0]) for i, r in enumerate(rows)])
        p.play(0.1, FadeIn(ms), rt=0.5)
        wl = T("will exist (planned)", 34).move_to([-4.3, -0.65, 0])
        axis = Rectangle(width=11.0, height=0.1, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0, -1.55, 0])
        p.play(0.2, FadeIn(wl), GrowFromCenter(axis), rt=0.5)
        dates = ["Oct 21", "Oct 31", "Nov 10", "Nov 23", "Dec 1", "Dec 13", "Dec 20"]
        xs = np.linspace(-5.2, 5.2, 7)
        ticks = VGroup(*[Circle(radius=0.16, stroke_color=INK, stroke_width=5, fill_color=STAGE, fill_opacity=1)
                         .move_to([x, -1.55, 0]) for x in xs])
        dl = VGroup(*[T(d, 32).move_to([x, -2.25 - 0.45 * (i % 2), 0]) for i, (d, x) in enumerate(zip(dates, xs))])
        p.play(0.3, FadeIn(dl), rt=0.4)
        p.play(0.62, LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=0.15), rt=1.0)
        p.finish()


class B14_Close(Scene):
    def construct(self):
        p = Pace(self)
        self.add(constructed())
        c = card(0, 0.75, w=3.6, h=2.6, rows=3, empty_last=True)
        st = stamp("dash", 2.5, c.rows_y[2])
        p.play(0.02, FadeIn(c), rt=0.4)
        title = T("Honest Shortlist", 60, bold=True).move_to([0, -1.65, 0])
        p.play(0.1, FadeIn(title), rt=0.4)
        p.play(0.62, GrowFromCenter(st), rt=0.4)
        p.finish()
