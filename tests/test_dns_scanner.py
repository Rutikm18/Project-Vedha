"""
test_dns_scanner.py — DNS AXFR / DNSSEC / version.bind audit.

The live dnspython network path needs a real name server (a manual check against
a public AXFR test target like zonetransfer.me), so these cover the parts that
carry the verdict and the safety guarantees:
  * zone-name derivation (pure)
  * the AXFR record cap (a huge/hostile zone must never be fully dumped)
  * ScanResult shaping via a monkeypatched probe (no network)
  * findings (zone transfer / version disclosure / unsigned zone) + secure silence
  * scanner/ + main_scripts/ parity
"""

from __future__ import annotations

import asyncio

from scanner import dns_scanner as dnsx
from scanner import findings
from scanner.scanner_base import ScopeGuard


# ── zone derivation (pure) ────────────────────────────────────────────────────

class TestDeriveZones:
    def test_hostname_target_reduces_to_registrable_and_parent(self):
        assert dnsx.derive_zones("ns1.corp.example.com") == ["example.com", "corp.example.com"]

    def test_ip_target_derives_nothing(self):
        assert dnsx.derive_zones("10.0.0.1") == []
        assert dnsx.derive_zones("::1") == []

    def test_explicit_zone_used_as_is(self):
        assert dnsx.derive_zones("10.0.0.1", extra=["example.com"]) == ["example.com"]

    def test_extra_before_target_derived(self):
        z = dnsx.derive_zones("ns1.example.com", extra=["dc.internal.local"])
        assert "internal.local" in z and "example.com" in z
        assert z.index("internal.local") < z.index("example.com")

    def test_bounded(self):
        z = dnsx.derive_zones("a.b.c.d.example.com",
                              extra=[f"z{i}.dom{i}.com" for i in range(20)])
        assert len(z) <= dnsx.MAX_ZONES


# ── AXFR record cap (safety: never dump a huge/hostile zone) ──────────────────

class TestAxfrBounded:
    def test_axfr_stops_at_cap(self):
        sc = dnsx.DNSScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                             rate=1e9, concurrency=1, timeout=0.1)

        class _RRset(list):
            def to_text(self):
                return "host A 10.0.0.1"

        class _Msg:
            def __init__(self, n):
                self.answer = [_RRset(range(n))]   # n "records"

        def _fake_xfr(*a, **k):
            for _ in range(1000):                  # would be ~1,000,000 records
                yield _Msg(1000)

        import dns.query
        orig = dns.query.xfr
        dns.query.xfr = _fake_xfr
        try:
            res = sc._axfr("10.0.0.2", 53, "example.com")
        finally:
            dns.query.xfr = orig
        assert res["transferred"] is True and res["capped"] is True
        # stopped early: nowhere near the ~1,000,000 records the fake would emit
        assert res["record_count"] <= dnsx.MAX_AXFR_RECORDS + 1000
        assert len(res["sample"]) <= dnsx.MAX_SAMPLE

    def test_axfr_refused_reports_not_transferred(self):
        sc = dnsx.DNSScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                             rate=1e9, concurrency=1, timeout=0.1)
        import dns.query

        def _boom(*a, **k):
            raise RuntimeError("REFUSED")

        orig = dns.query.xfr
        dns.query.xfr = _boom
        try:
            res = sc._axfr("10.0.0.2", 53, "example.com")
        finally:
            dns.query.xfr = orig
        assert res["transferred"] is False and "reason" in res


# ── scanner (network isolated via a patched _probe) ───────────────────────────

class TestDNSScanner:
    def _sc(self):
        return dnsx.DNSScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                               rate=1e9, concurrency=2, timeout=0.1, ports=[53])

    def test_zone_transfer_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {
            "dns": True, "version_bind": "9.11.3-Ubuntu", "hostname_bind": "ns1",
            "axfr": {"example.com": {"transferred": True, "record_count": 42}},
            "zone_transfer": True, "dnssec": {"example.com": False}}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["zone_transfer"] is True and r.proto == "udp"

    def test_no_dns_is_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"dns": None, "reason": "no_dns"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"

    def test_dnspython_missing_is_error(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"dns": None, "error": "dnspython_not_installed"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "error" and "dnspython" in (r.error or "")


# ── findings ──────────────────────────────────────────────────────────────────

class TestDNSFindings:
    def _fact(self, **data):
        return {"scanner": "dns_scan", "target": "10.0.0.2", "port": 53,
                "status": "open", "data": data}

    def test_zone_transfer_version_and_unsigned(self):
        fact = self._fact(
            version_bind="9.11.3-1ubuntu1.2-Ubuntu", hostname_bind="ns1",
            zone_transfer=True,
            axfr={"example.com": {"transferred": True, "record_count": 42},
                  "corp.example.com": {"transferred": False, "reason": "TransferError"}},
            dnssec={"example.com": False, "corp.example.com": None})
        by = {f.rule_id: f for f in findings.run_findings([fact])}
        assert by["DNS-ZONE-TRANSFER"].severity == "high"
        assert "example.com" in by["DNS-ZONE-TRANSFER"].data["zones"]
        assert by["DNS-VERSION-DISCLOSURE"].severity == "info"
        assert by["DNS-DNSSEC-ABSENT"].data["unsigned_zones"] == ["example.com"]

    def test_dnssec_absent_only_for_confirmed_zone(self):
        # DNSSEC=False for a zone that DIDN'T transfer must NOT raise a finding
        # (we only flag zones we proved authoritative via AXFR — avoids noise).
        fact = self._fact(version_bind=None, zone_transfer=False,
                          axfr={"example.com": {"transferred": False}},
                          dnssec={"example.com": False})
        assert not any(f.rule_id.startswith("DNS-") for f in findings.run_findings([fact]))

    def test_secure_server_silent(self):
        fact = self._fact(version_bind=None, zone_transfer=False, axfr={}, dnssec={})
        assert not any(f.rule_id.startswith("DNS-") for f in findings.run_findings([fact]))


# ── parity across trees ───────────────────────────────────────────────────────

class TestParity:
    def test_scanner_and_findings_in_main_scripts(self):
        from main_scripts.dns_scanner import DNSScanner, derive_zones
        from main_scripts import findings as mf
        assert derive_zones("ns1.example.com") == ["example.com"]
        fact = {"scanner": "dns_scan", "target": "10.0.0.2", "port": 53, "status": "open",
                "data": {"zone_transfer": True,
                         "axfr": {"x.com": {"transferred": True, "record_count": 3}},
                         "dnssec": {"x.com": False}, "version_bind": "9.0"}}
        ids = {f.rule_id for f in mf.run_findings([fact])}
        assert {"DNS-ZONE-TRANSFER", "DNS-VERSION-DISCLOSURE", "DNS-DNSSEC-ABSENT"} <= ids
        assert DNSScanner
