"""
version.py — loose version comparison for CVE range matching.

Real service banners carry versions that are NOT PEP 440 / SemVer clean:
OpenSSH `8.2p1`, OpenSSL `1.1.1k`, Debian epochs `1:2.4.41`, distro suffixes
`8.2p1 Ubuntu-4ubuntu0.5`. NVD `versionStart*/versionEnd*` bounds, by contrast, are
usually clean dotted numbers. This module normalizes a version string into a
comparable numeric tuple so an observed version can be tested against an NVD range.

Normalization rules (pragmatic, cover the dominant real cases):
  * lowercase, strip a leading 'v', take the first whitespace token, drop a
    Debian epoch `N:`;
  * OpenSSH portable `pN` -> `.N`  (8.2p1 -> 8.2.1);
  * a trailing OpenSSL-style letter -> its alphabet ordinal (1.1.1k -> 1.1.1.11);
  * then take the leading run of dotted integers.

Comparison is zero-padded tuple comparison. This is deliberately for CANDIDATE
matching — the correlator never asserts a CVE from a banner version alone (distro
backports patch without bumping the version); it tags findings "verify patch
level". The suffix precision here is best-effort, recorded in evidence.
"""

from __future__ import annotations

import re


def parse_version(v) -> tuple[int, ...]:
    """Normalize a version string into a comparable tuple of ints."""
    if v is None:
        return (0,)
    s = str(v).strip().lower()
    if not s:
        return (0,)
    s = s.split()[0]                      # first token ("8.2p1 Ubuntu-…" -> "8.2p1")
    if s.startswith("v"):
        s = s[1:]
    if ":" in s:                          # Debian epoch "1:2.4.41" -> "2.4.41"
        s = s.split(":", 1)[1]
    s = re.sub(r"p(\d+)", r".\1", s)      # OpenSSH portable 8.2p1 -> 8.2.1
    # trailing single letter after a digit (OpenSSL 1.1.1k) -> .<ordinal>
    s = re.sub(r"(?<=\d)([a-z])(?![a-z0-9])", lambda m: "." + str(ord(m.group(1)) - 96), s)
    nums = re.findall(r"\d+", s)
    return tuple(int(n) for n in nums[:8]) or (0,)


def compare(a, b) -> int:
    """Return -1/0/1 for version a vs b (zero-padded tuple comparison)."""
    ta, tb = parse_version(a), parse_version(b)
    n = max(len(ta), len(tb))
    ta += (0,) * (n - len(ta))
    tb += (0,) * (n - len(tb))
    return (ta > tb) - (ta < tb)


def in_range(version, *, start_incl=None, start_excl=None,
             end_incl=None, end_excl=None, exact=None) -> bool:
    """Is `version` inside the NVD-style bound set? An `exact` match (no range
    bounds) requires equality. With bounds, a missing bound is open on that side.
    Returns False if nothing constrains the match (avoids matching everything)."""
    if exact is not None and not any((start_incl, start_excl, end_incl, end_excl)):
        return compare(version, exact) == 0
    constrained = False
    if start_incl is not None:
        constrained = True
        if compare(version, start_incl) < 0:
            return False
    if start_excl is not None:
        constrained = True
        if compare(version, start_excl) <= 0:
            return False
    if end_incl is not None:
        constrained = True
        if compare(version, end_incl) > 0:
            return False
    if end_excl is not None:
        constrained = True
        if compare(version, end_excl) >= 0:
            return False
    return constrained
