"""
default_creds_catalog.py — vendors that ship WIDELY-DOCUMENTED default credentials.

DATA only, and deliberately NOT a credential list to try.

This maps a fingerprinted vendor to the PUBLIC FACT that its devices ship with a
default login, plus a reference. That is enough for the manager to raise a
finding from an auth-surface observation alone — "this device is from a vendor
with published defaults and it is exposing a login; prove the default was
changed" — without anyone ever attempting to authenticate.

WHY VEDHA DOES NOT TRY THE CREDENTIAL
-------------------------------------
A login attempt is an active action: it can lock accounts, trip IDS, and on some
embedded devices wedge the management interface. It also changes what the tool IS
— from an assessment that observes to one that authenticates — which is a
different authorisation conversation with the customer. So confirmation lives
behind the existing RoE-gated active-validation path, and this catalog stays
purely declarative. The `default_login` string is shown to the operator as
context for remediation, never used by the scanner.

The table is an ALLOWLIST of vendors with published defaults. An unrecognised
vendor produces no finding — a banner that merely looks device-ish is not
evidence that a default password exists.
"""
from __future__ import annotations

_DEFAULTS: dict[str, dict] = {
    # ── cameras / NVRs ────────────────────────────────────────────────────────
    "hikvision": {"default_login": "admin/12345",
                  "reference": "vendor default; inactivated-device era firmware"},
    "dahua":     {"default_login": "admin/admin",
                  "reference": "vendor default"},
    "axis":      {"default_login": "root/pass",
                  "reference": "vendor default on pre-2020 firmware"},
    # ── network gear ──────────────────────────────────────────────────────────
    "netgear":   {"default_login": "admin/password", "reference": "vendor default"},
    "tp-link":   {"default_login": "admin/admin",    "reference": "vendor default"},
    "d-link":    {"default_login": "admin/(blank)",  "reference": "vendor default"},
    "zyxel":     {"default_login": "admin/1234",     "reference": "vendor default"},
    "mikrotik":  {"default_login": "admin/(blank)",  "reference": "RouterOS default"},
    "ubiquiti":  {"default_login": "ubnt/ubnt",      "reference": "vendor default"},
    # ── printers / storage ────────────────────────────────────────────────────
    "hp":        {"default_login": "admin/(blank)",  "reference": "JetDirect default"},
    "canon":     {"default_login": "ADMIN/canon",    "reference": "vendor default"},
    "epson":     {"default_login": "EPSONWEB/(blank)", "reference": "vendor default"},
    "brother":   {"default_login": "admin/access",   "reference": "vendor default"},
    "synology":  {"default_login": "admin/(blank)",  "reference": "first-boot default"},
    "qnap":      {"default_login": "admin/admin",    "reference": "vendor default"},
}


def has_known_defaults(vendor: str | None) -> dict | None:
    """Published default credentials for `vendor`, or None if not catalogued.

    Not-catalogued is a deliberate silence, not an "unknown" verdict: raising a
    default-credential finding against a vendor we have no published evidence for
    would be a guess, and a wrong one is the kind that makes an operator stop
    trusting the whole report.
    """
    if not vendor or not str(vendor).strip():
        return None
    return _DEFAULTS.get(str(vendor).strip().lower())
