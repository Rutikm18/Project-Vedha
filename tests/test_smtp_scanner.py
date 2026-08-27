"""
test_smtp_scanner.py — SMTP hygiene (VRFY/EXPN user-enum + STARTTLS presence).

Pure protocol logic + ScanResult shaping via a monkeypatched probe + findings +
parity. (The real control socket path is exercised by the scratchpad ground-truth.)
"""

from __future__ import annotations

import asyncio

from scanner import smtp_scanner as smtp
from scanner import findings
from scanner.scanner_base import ScopeGuard


class TestPureLogic:
    def test_parse_ehlo_capabilities(self):
        caps = smtp.parse_ehlo_capabilities(
            "250-mail.example.com\r\n250-PIPELINING\r\n250-STARTTLS\r\n250 VRFY\r\n")
        assert "STARTTLS" in caps and "VRFY" in caps and "PIPELINING" in caps

    def test_vrfy_leaks(self):
        assert smtp.vrfy_leaks(250, 550) is True     # exists vs not
        assert smtp.vrfy_leaks(550, 250) is True     # symmetric
        assert smtp.vrfy_leaks(252, 252) is False    # ambiguous
        assert smtp.vrfy_leaks(250, 250) is False    # accept-all
        assert smtp.vrfy_leaks(502, 502) is False    # not implemented


class TestSMTPScanner:
    def _sc(self):
        return smtp.SMTPScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                                rate=1e9, concurrency=2, timeout=0.1, ports=[25])

    def test_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"smtp": True, "banner": "220 mail", "starttls": False,
                                  "vrfy_enabled": True, "expn_enabled": False,
                                  "vrfy_postmaster_code": 250, "vrfy_random_code": 550}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["vrfy_enabled"] is True

    def test_no_smtp_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"smtp": None, "reason": "no_smtp"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"


class TestSMTPFindings:
    def _fact(self, **d):
        return {"scanner": "smtp_scan", "target": "10.0.0.11", "port": 25,
                "status": "open", "data": {"smtp": True, **d}}

    def test_user_enum_and_no_starttls(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            vrfy_enabled=True, expn_enabled=False, starttls=False,
            vrfy_postmaster_code=250, vrfy_random_code=550)])}
        assert by["SMTP-USER-ENUM"].severity == "medium"
        assert by["SMTP-NO-STARTTLS"].severity == "low"

    def test_hardened_is_silent(self):
        out = findings.run_findings([self._fact(
            vrfy_enabled=False, expn_enabled=False, starttls=True)])
        assert not any(f.rule_id.startswith("SMTP-") for f in out)

    def test_expn_alone_triggers_enum(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            vrfy_enabled=False, expn_enabled=True, starttls=True)])}
        assert "SMTP-USER-ENUM" in by and "EXPN" in by["SMTP-USER-ENUM"].data["vectors"]


class TestParity:
    def test_main_scripts(self):
        from main_scripts.smtp_scanner import SMTPScanner, vrfy_leaks
        from main_scripts import findings as mf
        assert vrfy_leaks(250, 550) is True
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "smtp_scan", "target": "10.0.0.11", "port": 25, "status": "open",
            "data": {"smtp": True, "vrfy_enabled": True, "starttls": False}}])}
        assert {"SMTP-USER-ENUM", "SMTP-NO-STARTTLS"} <= ids
        assert SMTPScanner
