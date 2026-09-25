"""
citations.py — ground regulatory citations in AI answers against our own packs.

The domain brief tells the model to cite only controls it was given; this is the
check that it did. Citation-shaped references (Art. 32(1)(a), §500.17, Annex 1 §7,
16 CFR 314.4(c)(5), Req 4.2.1, A.8.24, SC-8, CC6.7, 3.3.17, Section 8(5)) are
extracted from the answer and compared with the same extraction run over every
control string in the compliance packs, so the allow-list can never drift from
the packs.

Verdict semantics: a citation is VERIFIED when the packs contain it, a sub-clause
of it (the packs cite Art. 32(1)(a), the model says Art. 32), or its parent (the
packs cite §500.5, the model says §500.5(a)). Everything else is UNVERIFIED and
surfaced to the reader — the text itself is never edited.

Known limitation: article numbers are matched without their instrument, so a
real "Art. 33" cited under the wrong regulation still verifies.
"""
from __future__ import annotations

import re
from functools import lru_cache

_SUB = r"((?:\(\w{1,4}\))*)"
_PATTERNS: tuple[tuple[re.Pattern, str], ...] = (
    # Order matters: compound forms first, their spans are then blanked out.
    (re.compile(r"\bannex\s+(\d+)\s*§\s*(\d+)"), "annex {0} §{1}"),
    (re.compile(r"\b(\d+)\s+cfr\s+(\d+(?:\.\d+)?)" + _SUB), "{0} cfr {1}{2}"),
    (re.compile(r"\b(?:art\.|article)\s*(\d+[a-z]?)" + _SUB), "art. {0}{1}"),
    (re.compile(r"\bsection\s+(\d+[a-z]?)" + _SUB), "section {0}{1}"),
    (re.compile(r"§\s*(\d+(?:\.\d+)*)" + _SUB), "§{0}{1}"),
    (re.compile(r"\breq(?:uirement)?\.?\s+(\d+(?:\.\d+){1,3})"), "req {0}"),
    (re.compile(r"\ba\.(\d{1,2}\.\d{1,2})\b"), "a.{0}"),
    (re.compile(r"\bcc(\d\.\d{1,2})\b"), "cc{0}"),
    (re.compile(r"\b(ac|at|au|ca|cm|cp|ia|ir|ma|mp|pe|pl|pm|ps|pt|ra|sa|sc|si|sr)-(\d{1,2})\b"), "{0}-{1}"),
    (re.compile(r"(?<![\d.])(3\.[1-4]\.\d{1,2})(?!\.?\d)"), "{0}"),   # SAMA CSF subdomains
)


def extract_citations(text: str) -> list[str]:
    """Normalized citation tokens in order of first appearance."""
    work = (text or "").lower()
    found: list[str] = []
    for pattern, fmt in _PATTERNS:
        def take(m: re.Match) -> str:
            token = fmt.format(*[g or "" for g in m.groups()])
            if token not in found:
                found.append(token)
            return " " * len(m.group(0))   # blank the span so a shorter pattern can't re-match it
        work = pattern.sub(take, work)
    return found


@lru_cache(maxsize=1)
def known_citations() -> frozenset[str]:
    from app.compliance.registry import FRAMEWORKS, known_control_ids
    from app.services import finding_compliance

    strings = set(known_control_ids())
    # Framework metadata is ours too: a model quoting "CERT-In Directions under
    # Section 70B(6)" or a reporting reference such as "NIS2 Art. 23(4)(a)" is grounded.
    for fw in FRAMEWORKS.values():
        strings.update([fw.name, fw.source, fw.note or ""])
        strings.update(r.reference for r in fw.reporting)
    for per_framework in finding_compliance._MAP.values():
        for entry in per_framework.values():
            strings.update(entry.get("controls", []))
    known: set[str] = set()
    for s in strings:
        known.update(extract_citations(s))
    return frozenset(known)


def _grounded(token: str, known: frozenset[str]) -> bool:
    if token in known:
        return True
    # sub-clause relationship in either direction: "art. 32" ↔ "art. 32(1)(a)"
    return any(k.startswith(token + "(") or token.startswith(k + "(") for k in known)


def check_citations(text: str) -> dict[str, list[str]]:
    known = known_citations()
    verified: list[str] = []
    unverified: list[str] = []
    for token in extract_citations(text):
        (verified if _grounded(token, known) else unverified).append(token)
    return {"verified": verified, "unverified": unverified}
