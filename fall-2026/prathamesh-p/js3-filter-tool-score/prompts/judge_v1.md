You are judging one job posting for one FICTIONAL job-seeker persona. Your answer is stored as a labeled
JUDGMENT (a model opinion), never as fact. It is checked by a strict validator, and any deviation from the
format below is rejected and recorded as rejected.

## Task

Decide whether this posting is **relevant** or **not_relevant** for the persona below.

A posting is relevant when all of the following hold:
1. The job is computer-network engineering or architecture work, the kind covered by SOC 15-1241 (Computer Network
   Architects): designing, building, operating, or securing networks. Software roles that only touch networking are
   not that kind of work.
2. Nothing in the posting rules the persona out on work authorization. The persona is on an F-1 visa, needs
   sponsorship, is not a U.S. person for ITAR/EAR purposes, and holds no security clearance.
3. The persona's networking skills meaningfully overlap what the posting asks for.

## Persona (fictional résumé, JSON)

{{RESUME_JSON}}

## Posting (JSON; "lists" is the posting's bullet lists as plain text)

{{POSTING_JSON}}

## Output contract (follow exactly)

Reply with ONE JSON object and nothing else. Do not use a code fence, and do not put any prose before or after the object.
The object must have exactly these three keys:

{"posting_id": "{{POSTING_ID}}", "verdict": "relevant" or "not_relevant", "citations": [ ... ]}

- `posting_id`: exactly "{{POSTING_ID}}".
- `verdict`: exactly the lowercase string "relevant" or "not_relevant".
- `citations`: a non-empty list. Each item has exactly these four keys:
  - `resume_field`: a dotted path made of **dictionary keys only**. Do not use list indexes such as "education.0.degree", and do not
    point into a list of objects such as "experience", "education" or "projects", because those cannot be cited. It must be exactly one of
    these paths:
    "fictional", "attested", "attestation_note", "_comment",
    "personal.name", "personal.location", "personal.phone", "personal.email", "personal.linkedin", "personal.github",
    "visa.type", "visa.current_status", "visa.needs_sponsorship", "visa.us_person_for_itar", "visa.holds_security_clearance",
    "target.soc_code", "target.soc_title", "target.title_terms", "target.commitment",
    "constraints.excluded", "constraints.open_to_relocation",
    "skills.networking", "skills.security", "skills.automation", "skills.cloud", "skills.vendors",
    "skills.familiar_with_not_shipped", "certifications".
  - `resume_value`: a value found at that path. If the path holds a list, give one element of it exactly as written.
    If it holds a string, give that string or an exact part of it. If it holds true/false, give that boolean.
  - `posting_field`: one of "text", "descriptionPlain", "lists", "additionalPlain", "categories.location",
    "categories.team", "categories.commitment".
  - `posting_value`: text copied **verbatim** from that posting field. It must be a short exact substring, with no
    paraphrase and no ellipsis.

Cite the specific evidence your verdict rests on. A citation whose value is not literally present in the named
field invalidates the whole answer.
