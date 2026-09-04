"""
router.py — dynamic Gate-5 branch routing from OBSERVED service_banner
content, not just port number. Solves the "HTTPS-on-9443" problem: a port
outside the static TLS_PORTS table still gets routed to tls_scan if its
banner says so.

TWO KINDS OF SIGNAL, STRONGEST FIRST:

1. POSITIVE — service_banner attempted a TLS handshake on every port its
   plaintext rungs could not identify and records `tls: True` when one
   completed (plus `service: "tls"` when a TLS-only listener answered a
   plaintext probe with an alert record). It also soft-matches banners into
   a `service` field (ssh / mysql / redis / postgresql / http ...). Those are
   direct observations and route with no inference at all.

2. ABSENCE (fallback, kept from before the positive signal existed) —
   service_banner.py's _GENERIC_PROBE (b"\r\n") sent to a raw TLS-only port
   does NOT provoke a recognizable TLS alert byte sequence on most stacks —
   the target's TLS stack treats the garbage input as a protocol violation
   and closes the connection with no response at all. So an open port with
   banner=None that ISN'T one of the well-known silent-by-design protocols
   (the _CLIENT_FIRST set, which service_banner.py already sends a real HTTP
   probe to) still looks exactly like an HTTPS server moved to a weird port,
   and tls_scan is cheap and harmless to try speculatively — if it's not
   actually TLS, tls_scanner just reports a handshake failure.

HTTP detection has a strong positive signal — the literal "HTTP/1." status
line — since service_banner.py already sends a real HTTP GET (in plaintext
and, when that fails, inside a TLS tunnel), and even on ports it doesn't
expect, an HTTP server typically responds to a bare "\r\n" with a 400-class
error that still starts "HTTP/1.x".
"""
from __future__ import annotations

import re as _re

from .asset import Asset

# service_banner soft-match labels that mean "a database / cache is listening" —
# the structured form of the regexes below, present whenever the banner matched.
_DB_SERVICES = {"mysql", "postgresql", "redis", "mongodb", "memcached",
                "elasticsearch", "couchdb"}

# HTTP-shaped services the web assessment branch understands.
_WEB_SERVICES = {"http", "http-proxy", "docker", "kubernetes-api",
                 "elasticsearch", "couchdb"}

_DB_SIGNATURES = (
    _re.compile(r"[0-9]+\.[0-9]+\.[0-9]+-(log|mariadb|ubuntu)", _re.I),  # MySQL/MariaDB greeting
    _re.compile(r"NOAUTH|redis_version", _re.I),                          # Redis
    _re.compile(r"ismaster|mongodb", _re.I),                             # MongoDB
    _re.compile(r"unsupported frontend protocol", _re.I),                # PostgreSQL
    _re.compile(r"mysql_native_password|caching_sha2_password", _re.I),  # MySQL 5/8
)

# Mirrors service_banner.py's own _CLIENT_FIRST set — ports where silence is
# EXPECTED regardless of protocol (an HTTP probe was already sent there), so
# banner=None on one of these is not a TLS signal, just "nothing interesting
# came back to our HTTP probe."
_CLIENT_FIRST = {80, 8080, 8000, 8888, 443, 8443}


def looks_like_http(banner_fact: dict) -> bool:
    fact = banner_fact or {}
    first_line = fact.get("first_line") or ""
    if first_line.startswith("HTTP/1.") or first_line.startswith("HTTP/2"):
        return True
    return fact.get("service") in _WEB_SERVICES


def looks_like_tls(port: int, banner_fact: dict | None) -> bool:
    """True when the port was OBSERVED speaking TLS (a completed handshake, or a
    TLS alert to our plaintext probe).

    EVIDENCE ORDER — positive, then negative, then (last) the absence guess:

    1. `tls`/`service == "tls"` — service_banner completed a handshake or was
       answered with a TLS alert record. Direct observation; route it.
    2. `tls_probed` WITHOUT `tls` — service_banner tried a handshake on this port
       and it failed. That is direct evidence the port does NOT speak TLS, and it
       outranks any inference. Before this check existed the absence rule below
       fired anyway, so every silent binary protocol (SMB 445, MSRPC 135, RDP
       3389) was speculatively re-probed by tls_scan on a live Windows host —
       three handshakes, zero facts, every scan.
    3. The absence guess, kept only for facts with neither flag (an older probe
       build, or --no-tls): an open port that returned no banner and is not one of
       the silent-by-design web ports still looks like HTTPS-on-a-weird-port, and
       tls_scan is cheap and harmless to try speculatively.
    """
    if banner_fact is None:
        return False    # no banner attempt was made at all (port not open)
    if banner_fact.get("tls") or banner_fact.get("service") == "tls":
        return True     # positive observation — no inference needed
    if banner_fact.get("tls_probed"):
        return False    # tried and failed: negative evidence, not silence
    if port in _CLIENT_FIRST:
        return False   # silence here is the normal HTTP-probe-got-nothing case
    return banner_fact.get("banner") is None


def looks_like_db(banner_fact: dict | None) -> bool:
    """True when a service banner carries a database greeting signature, so a DB
    on a non-standard port still routes to db_scan. Never matches HTTP."""
    if not banner_fact:
        return False
    if banner_fact.get("service") in _DB_SERVICES:
        return True
    if looks_like_http(banner_fact):
        return False
    hay = f"{banner_fact.get('banner') or ''} {banner_fact.get('first_line') or ''}"
    return any(rx.search(hay) for rx in _DB_SIGNATURES)


def looks_like_ssh(banner_fact: dict | None) -> bool:
    """True when a service banner is an SSH identification string, so an SSH
    server on a non-standard port (e.g. 2222) still routes to ssh_scan. SSH has
    an unambiguous POSITIVE signal — the protocol requires the server to send
    'SSH-<proto>-<software>' as its first bytes (RFC 4253 §4.2) — so, unlike the
    TLS heuristic, this is a direct content match, not an absence inference."""
    if not banner_fact:
        return False
    if banner_fact.get("service") == "ssh":
        return True
    hay = f"{banner_fact.get('banner') or ''} {banner_fact.get('first_line') or ''}"
    return hay.lstrip().startswith("SSH-")


def route_branches(asset: Asset, candidate_branches: tuple[str, ...] = ("tls", "web", "db", "ssh")
                   ) -> dict[int, set[str]]:
    """For every open port with a banner fact, returns {port: {branches}}
    that observed content (not the static port table) justifies routing to.
    gates.py's gate_5_branch_eligible still makes the final per-branch
    decision (profile + --services filter), so the caller passes whatever
    this returns as that function's `dynamically_routed` hint, on a
    per-(port, branch) basis — this function never decides eligibility on
    its own, only "does the evidence support this branch."
    """
    routed: dict[int, set[str]] = {}
    for port in asset.open_ports_for_deep_scan():
        fact = asset.services.get(port)
        branches: set[str] = set()
        if "web" in candidate_branches and fact and looks_like_http(fact):
            branches.add("web")
        if "tls" in candidate_branches and looks_like_tls(port, fact):
            branches.add("tls")
        if "db" in candidate_branches and looks_like_db(fact):
            branches.add("db")
        if "ssh" in candidate_branches and looks_like_ssh(fact):
            branches.add("ssh")
        if branches:
            routed[port] = branches
    return routed
