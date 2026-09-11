"""
Auth-surface observation — what login a web service ASKS for.

This is the probe half of default-credential detection, and the boundary matters:
the probe records what the device ADVERTISES (an HTTP auth challenge, or a
password form) and stops there. It never sends a username or password. Confirming
that a default credential actually works is an active step, gated by rules of
engagement, and belongs nowhere near a discovery scan.

The manager reads this fact and decides whether the vendor is one with documented
defaults. That split is what keeps the probe facts-only and keeps a credential
list out of the scanner entirely.

Note the scheme values are deliberately coarse (basic/digest/other/form/none):
the finding is "this thing has a login and its vendor ships defaults", so the
exact challenge dialect is evidence, not the verdict.
"""
from __future__ import annotations

from scanner.web_scanner import parse_auth_surface


class TestAuthChallenge:
    def test_basic_realm_is_parsed(self):
        s = parse_auth_surface({"WWW-Authenticate": 'Basic realm="Hikvision"'}, "")
        assert s["scheme"] == "basic"
        assert s["realm"] == "Hikvision"
        assert s["vendor"] == "hikvision"

    def test_digest_realm_is_parsed(self):
        s = parse_auth_surface(
            {"WWW-Authenticate": 'Digest realm="NETGEAR", nonce="abc"'}, "")
        assert s["scheme"] == "digest"
        assert s["realm"] == "NETGEAR"
        assert s["vendor"] == "netgear"

    def test_header_lookup_is_case_insensitive(self):
        """web_scanner lowercases header keys; other callers may not."""
        lower = parse_auth_surface({"www-authenticate": 'Basic realm="X"'}, "")
        upper = parse_auth_surface({"WWW-Authenticate": 'Basic realm="X"'}, "")
        assert lower["scheme"] == upper["scheme"] == "basic"

    def test_unknown_challenge_scheme_is_other_not_a_guess(self):
        s = parse_auth_surface({"WWW-Authenticate": "Negotiate"}, "")
        assert s["scheme"] == "other"
        assert s["realm"] is None

    def test_realm_absent_from_challenge(self):
        s = parse_auth_surface({"WWW-Authenticate": "Basic"}, "")
        assert s["scheme"] == "basic" and s["realm"] is None


class TestLoginForm:
    def test_password_input_is_detected_as_a_form(self):
        body = '<form action="/login"><input type="password" name="pass"></form>'
        assert parse_auth_surface({}, body)["scheme"] == "form"

    def test_single_quoted_password_input_is_detected(self):
        body = "<input type='password'>"
        assert parse_auth_surface({}, body)["scheme"] == "form"

    def test_ordinary_page_has_no_auth_surface(self):
        s = parse_auth_surface({}, "<html><body>welcome</body></html>")
        assert s["scheme"] == "none"
        assert s["realm"] is None and s["vendor"] is None

    def test_challenge_wins_over_form(self):
        """An explicit challenge is stronger evidence than a heuristic form match."""
        body = '<input type="password">'
        s = parse_auth_surface({"WWW-Authenticate": 'Basic realm="R"'}, body)
        assert s["scheme"] == "basic"


class TestVendorHint:
    def test_vendor_found_in_realm(self):
        s = parse_auth_surface({"WWW-Authenticate": 'Basic realm="DAHUA DVR"'}, "")
        assert s["vendor"] == "dahua"

    def test_vendor_found_in_body(self):
        s = parse_auth_surface({}, "<title>TP-LINK Router</title><input type='password'>")
        assert s["vendor"] == "tp-link"

    def test_unknown_vendor_is_none_not_a_guess(self):
        s = parse_auth_surface({"WWW-Authenticate": 'Basic realm="AcmeCorp"'}, "")
        assert s["vendor"] is None


class TestRobustness:
    def test_empty_inputs_are_survivable(self):
        s = parse_auth_surface({}, "")
        assert s == {"scheme": "none", "realm": None, "vendor": None}

    def test_none_inputs_are_survivable(self):
        """A scanner must never crash on a response it didn't get."""
        s = parse_auth_surface(None, None)
        assert s["scheme"] == "none"

    def test_body_scan_is_bounded(self):
        """A huge body must not make vendor-hunting expensive."""
        body = ("x" * 500_000) + "hikvision"
        s = parse_auth_surface({}, body)
        assert s["vendor"] is None          # beyond the inspection window
