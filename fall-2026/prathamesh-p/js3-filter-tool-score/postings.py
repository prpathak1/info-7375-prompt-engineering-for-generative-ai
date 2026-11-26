"""Load every collected posting into one normalized record per (board, id). Offline; reads raw/ only.

Duplicate captures of the same board and id are judged once, from the newest capture (FILTER.md section 3).
Seeded captures (filename contains SEEDED) are test material, not collected postings, and are skipped.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"

# filename stem prefix -> (platform, board). Older captures (JS1 naming) have no platform prefix.
LEGACY = {"zoox": ("lever", "zoox"), "cloudflare": ("greenhouse", "cloudflare"), "openai": ("ashby", "openai")}


def board_of(path: Path):
    stem = path.name.split(".")[0]
    if "SEEDED" in path.name:
        return None
    if "-" in stem and stem.split("-", 1)[0] in ("lever", "greenhouse", "ashby"):
        platform, board = stem.split("-", 1)
        return platform, board
    return LEGACY.get(stem)


_BLOCK = re.compile(r"</?(p|li|ul|ol|br|div|h[1-6]|tr)[^>]*>", re.I)


def html_to_text(s) -> str:
    """HTML (possibly entity-escaped, as Greenhouse sends it) -> plain text with one block per line."""
    if not s:
        return ""
    s = html.unescape(str(s))          # Greenhouse content arrives as &lt;p&gt;...
    s = _BLOCK.sub("\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in s.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def normalize(platform: str, board: str, j: dict, captured: str) -> dict:
    if platform == "lever":
        parts = [j.get("descriptionPlain") or ""]
        for lst in j.get("lists") or []:
            parts.append(lst.get("text") or "")
            parts.append(html_to_text(lst.get("content")))
        parts.append(j.get("additionalPlain") or "")
        cats = j.get("categories") or {}
        return {"platform": platform, "board": board, "id": str(j.get("id")), "title": j.get("text"),
                "location": cats.get("location"), "body": "\n".join(p for p in parts if p),
                "url": j.get("hostedUrl"), "date": j.get("createdAt"), "captured": captured}
    if platform == "greenhouse":
        loc = j.get("location") or {}
        return {"platform": platform, "board": board, "id": str(j.get("id")), "title": j.get("title"),
                "location": loc.get("name") if isinstance(loc, dict) else loc, "body": html_to_text(j.get("content")),
                "url": j.get("absolute_url"), "date": j.get("first_published") or j.get("updated_at"), "captured": captured}
    return {"platform": platform, "board": board, "id": str(j.get("id")), "title": j.get("title"),
            "location": j.get("location"), "body": j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml")),
            "url": j.get("jobUrl"), "date": j.get("publishedAt"), "captured": captured}


def load_all(raw_dir: Path = RAW) -> list[dict]:
    """Return one record per (board, id), newest capture wins. Sorted by (board, id) so order is stable."""
    best = {}
    for f in sorted(Path(raw_dir).glob("*/*.json")):
        ob = board_of(f)
        if ob is None:
            continue
        platform, board = ob
        captured = f.parent.name
        d = json.loads(f.read_text(encoding="utf-8"))
        jobs = d if isinstance(d, list) else d.get("jobs", [])
        for j in jobs:
            rec = normalize(platform, board, j, captured)
            key = (board, rec["id"])
            if key not in best or captured >= best[key]["captured"]:
                best[key] = rec
    return [best[k] for k in sorted(best)]
