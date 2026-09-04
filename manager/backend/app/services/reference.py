"""
reference.py — human-readable references for things a customer has to talk about.

WHY. A scan job was identified only by its UUID, and the UI showed the first eight
hex characters of it. Nobody can read `a3f9c2d1` down a phone line, quote it in a
ticket, or tell it apart from `a3f9c2de` at a glance — and hex has no structure, so
it says nothing about when the thing happened.

THE SCHEME

    SCN-260902-7K3MQP
    │   │      └─ 6 characters of Crockford base32, derived from the row's UUID
    │   └─ YYMMDD, the day it was created
    └─ what kind of thing it is

Each part earns its place:

  * The PREFIX means a reference is self-describing. "SCN-260902-7K3MQP" is
    obviously a scan; a bare code would need context to interpret.
  * The DATE makes references naturally sortable and instantly situates them —
    an operator reading a ticket knows the age without a lookup.
  * CROCKFORD BASE32 (RFC-style, alphabet 0-9 A-Z minus I, L, O, U) is chosen over
    hex or base64 because it is designed to survive being read aloud and typed
    back: the letters most often confused with digits are simply absent, and
    decoding is case-insensitive and treats I/L as 1 and O as 0. That matters
    because the whole point of this identifier is that a human relays it.

DERIVED, THEN STORED. The suffix is a deterministic function of the row's UUID, so
existing rows can be backfilled without a counter, a sequence, or a race. But the
result is STORED, not recomputed on read: once a customer has quoted a reference
in a ticket, it must never change because we improved the algorithm.

COLLISIONS. 32**6 ≈ 1.07 billion suffixes. References are only ever compared
within a day+prefix, so at even 10,000 jobs a day the chance of any collision is
about 5 in 100,000. The uniqueness that matters is still the UUID's; this is a
label for humans, and `is_reference` exists so lookups can accept either.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

# Crockford base32: no I, L, O or U — the characters people mistype or misread.
_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_SUFFIX_LEN = 6

# What each prefix labels. Add here rather than passing loose strings around, so
# every reference in the product comes from one vocabulary.
PREFIX_SCAN_JOB = "SCN"
PREFIX_ENGAGEMENT = "ENG"
PREFIX_FINDING = "FND"
PREFIX_REPORT = "RPT"

_PREFIXES = frozenset({PREFIX_SCAN_JOB, PREFIX_ENGAGEMENT, PREFIX_FINDING, PREFIX_REPORT})

_REFERENCE_RE = re.compile(r"^(?P<prefix>[A-Z]{3})-(?P<date>\d{6})-(?P<suffix>[0-9A-Z]{6})$")

# Crockford's documented decode aliases, so a reference typed back by a human
# ("O" for zero, "l" for one) still resolves instead of 404-ing.
_DECODE_ALIASES = str.maketrans({"I": "1", "L": "1", "O": "0", "U": "V"})


def _encode(value: int, length: int) -> str:
    out = []
    for _ in range(length):
        out.append(_ALPHABET[value % 32])
        value //= 32
    return "".join(reversed(out))


def suffix_for(identifier: uuid.UUID | str) -> str:
    """The stable code for one row. Deterministic, so a backfill and a fresh
    insert agree on the same answer for the same UUID."""
    if isinstance(identifier, str):
        identifier = uuid.UUID(identifier)
    # Fold the whole 128 bits down rather than slicing one end: UUIDv1/v7 carry a
    # timestamp at one end and a node/counter at the other, so taking either
    # alone clusters the output for rows created together.
    return _encode(identifier.int % (32 ** _SUFFIX_LEN), _SUFFIX_LEN)


def make_reference(prefix: str, identifier: uuid.UUID | str,
                   created_at: datetime | None = None) -> str:
    """Build a reference. `created_at` should be the row's own creation time so a
    backfilled reference matches what the row would have been given at insert."""
    if prefix not in _PREFIXES:
        raise ValueError(f"unknown reference prefix {prefix!r}; "
                         f"add it to reference.py rather than passing a literal")
    when = created_at or datetime.now(timezone.utc)
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return f"{prefix}-{when.astimezone(timezone.utc):%y%m%d}-{suffix_for(identifier)}"


def scan_job_reference(job_id: uuid.UUID | str,
                       created_at: datetime | None = None) -> str:
    return make_reference(PREFIX_SCAN_JOB, job_id, created_at)


def normalize(text: str) -> str:
    """Canonicalise a reference a human typed: trim, upper-case, and apply
    Crockford's decode aliases so O/I/L land on 0/1."""
    cleaned = (text or "").strip().upper().replace(" ", "")
    prefix, _, rest = cleaned.partition("-")
    # Only the base32 SUFFIX is alias-folded; the prefix and date are literal.
    date, _, suffix = rest.partition("-")
    return f"{prefix}-{date}-{suffix.translate(_DECODE_ALIASES)}" if suffix else cleaned


def is_reference(text: str) -> bool:
    """True when `text` looks like one of our references rather than a UUID, so a
    lookup can accept either without guessing."""
    m = _REFERENCE_RE.match(normalize(text))
    return bool(m) and m.group("prefix") in _PREFIXES
