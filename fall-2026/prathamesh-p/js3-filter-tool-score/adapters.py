"""adapters.py: the three public ATS posting APIs (GATE.md D-1, D-9), mapped onto one posting shape.

One posting shape, which is what JS1's record rule (jobwatch.decide) reads:
    {"id": str, "text": <title>, "descriptionPlain": str, "lists": list, "additionalPlain": str}
Lever postings already have this shape. Their extra fields are kept, because the JS1 rule also reads `lists`.

Python standard library only. This module never touches the network or the disk. It only builds URLs and parses bytes it is given.
"""
from __future__ import annotations

import html
import json
import re

ALLOWED_HOSTS = ("api.lever.co", "boards-api.greenhouse.io", "api.ashbyhq.com")
PLATFORMS = ("lever", "greenhouse", "ashby")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


class FormatChanged(Exception):
    """HTTP 200, but not JSON, or JSON without the platform's expected shape (GATE section 4: no retry, escalate)."""


def board_url(platform: str, slug: str) -> str:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")
    if not SLUG_RE.match(slug):
        raise ValueError(f"board slug {slug!r} refused")
    if platform == "lever":
        return f"https://api.lever.co/v0/postings/{slug}?mode=json"
    if platform == "greenhouse":
        return f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    return f"https://api.ashbyhq.com/posting-api/job-board/{slug}"


def _plain(html_text) -> str:
    """Greenhouse `content` is HTML that has itself been HTML-escaped: unescape, drop tags, unescape entities, squeeze spaces."""
    s = html.unescape(html_text or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def _id(raw_id, platform: str) -> str:
    if isinstance(raw_id, bool) or not isinstance(raw_id, (str, int)) or raw_id == "":
        raise FormatChanged(f"{platform}: posting without a usable id ({raw_id!r})")
    return str(raw_id)


def parse(platform: str, body: bytes) -> list[dict]:
    try:
        data = json.loads(body)
    except (ValueError, UnicodeDecodeError) as e:
        raise FormatChanged(f"{platform}: body is not JSON ({e.__class__.__name__})") from e

    if platform == "lever":
        if not isinstance(data, list) or not all(isinstance(p, dict) for p in data):
            raise FormatChanged("lever: expected a JSON list of posting objects")
        out = []
        for p in data:
            q = dict(p)
            q["id"] = _id(p.get("id"), platform)
            q["text"] = str(p.get("text") or "")
            q["descriptionPlain"] = str(p.get("descriptionPlain") or "")
            q["lists"] = p.get("lists") if isinstance(p.get("lists"), list) else []
            q["additionalPlain"] = str(p.get("additionalPlain") or "")
            out.append(q)
        return out

    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list) or not all(isinstance(j, dict) for j in data["jobs"]):
        raise FormatChanged(f'{platform}: expected an object with a "jobs" list')
    if platform == "greenhouse":
        return [{"id": _id(j.get("id"), platform), "text": str(j.get("title") or ""),
                 "descriptionPlain": _plain(j.get("content")), "lists": [], "additionalPlain": ""} for j in data["jobs"]]
    if platform == "ashby":
        return [{"id": _id(j.get("id"), platform), "text": str(j.get("title") or ""),
                 "descriptionPlain": str(j.get("descriptionPlain") or ""), "lists": [], "additionalPlain": ""} for j in data["jobs"]]
    raise ValueError(f"unknown platform {platform!r}")
