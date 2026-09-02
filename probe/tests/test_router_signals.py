"""
test_router_signals.py — router.py consumes service_banner's POSITIVE signals
(the `tls` fact, the soft-matched `service`) before falling back to the
absence heuristic, and the web branch is told which ports were observed
speaking TLS.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from scanner.scanner_base import ScanResult, ScopeGuard
from scanner.web_scanner import WebScanner
from workflow.asset import Asset, PortFact
from workflow.router import looks_like_db, looks_like_http, looks_like_ssh, looks_like_tls, route_branches
from workflow.workflow_engine import run_engagement


def _open(port: int) -> PortFact:
    return PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))


class TestPositiveTls:
    def test_handshake_fact_routes_even_on_client_first_port(self):
        assert looks_like_tls(443, {"tls": True, "banner": "HTTP/1.1 200 OK"}) is True

    def test_alert_record_service_routes(self):
        assert looks_like_tls(9444, {"service": "tls", "banner": "\x15\x03\x01"}) is True

    def test_absence_heuristic_still_works(self):
        assert looks_like_tls(9443, {"banner": None}) is True
        assert looks_like_tls(443, {"banner": None}) is False
        assert looks_like_tls(9443, None) is False


class TestStructuredService:
    def test_db_by_service_field(self):
        assert looks_like_db({"service": "postgresql", "banner": "E\x00\x00"}) is True
        assert looks_like_db({"banner": "SFATAL unsupported frontend protocol"}) is True
        assert looks_like_db({"service": "http", "first_line": "HTTP/1.1 200 OK"}) is False

    def test_http_by_service_field(self):
        assert looks_like_http({"service": "docker", "first_line": "HTTP/1.1 404 Not Found"}) is True
        assert looks_like_http({"service": "kubernetes-api"}) is True
        assert looks_like_http({"service": "ssh"}) is False

    def test_ssh_by_service_field(self):
        assert looks_like_ssh({"service": "ssh", "banner": "SSH-2.0-Go"}) is True


def test_https_on_odd_port_routes_tls_and_web():
    a = Asset(host="10.0.0.5", open_ports={9444: _open(9444)},
              services={9444: {"tls": True, "tls_version": "TLSv1.3",
                               "first_line": "HTTP/1.1 200 OK", "service": "http"}})
    assert route_branches(a)[9444] == {"tls", "web"}


class TestWebSchemes:
    def test_observed_tls_prefers_https(self):
        w = WebScanner(ScopeGuard.from_list(["10.0.0.0/8"]), ports=[9444], tls_ports={9444})
        assert w._schemes_for(9444) == ("https", "http")
        assert w._schemes_for(8080) == ("http", "https")

    def test_static_table_still_applies(self):
        w = WebScanner(ScopeGuard.from_list(["10.0.0.0/8"]), ports=[443])
        assert w._schemes_for(443)[0] == "https"


def test_workflow_hands_observed_tls_ports_to_web_scanner(monkeypatch):
    """9000 is in the static WEB table but NOT the TLS table: only the banner's
    observed `tls` fact can tell the web branch to fetch it as https."""
    captured: dict = {}

    def fake(component_id, data, *, port):
        class Scanner:
            name = component_id

            def __init__(self, *args, **kwargs):
                captured.setdefault(component_id, kwargs)

            async def scan_target(self, host):
                return [ScanResult(scanner=component_id, target=host, port=port,
                                   proto="tcp", status="open", data=data)]
        return Scanner

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                        fake("host_discovery", {"alive": True}, port=None))
    monkeypatch.setattr("workflow.workflow_engine.PortScanner",
                        fake("port_scan", {}, port=9000))
    monkeypatch.setattr("workflow.workflow_engine.ServiceBannerScanner",
                        fake("service_banner", {"tls": True, "first_line": "HTTP/1.1 200 OK",
                                                "service": "http"}, port=9000))
    monkeypatch.setattr("workflow.workflow_engine.WebScanner",
                        fake("web_scan", {"status": 200}, port=9000))
    monkeypatch.setattr("workflow.workflow_engine.TLSScanner",
                        fake("tls_scan", {"version": "TLSv1.3"}, port=9000))

    asyncio.run(run_engagement(["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
                               service_filter={"web", "tls"}))
    assert captured["web_scan"]["tls_ports"] == {9000}
    assert captured["web_scan"]["ports"] == [9000]
    assert captured["tls_scan"]["ports"] == [9000]      # routed by the positive fact


# ── negative TLS evidence outranks the absence guess ─────────────────────────
class TestTlsProbedNegative:
    """service_banner now ATTEMPTS a TLS handshake on every unidentified port and
    records `tls_probed`. A port that was tried and did not speak TLS is proven
    not-TLS — that must beat the "silent, so maybe TLS" inference.

    Regression from a live Windows 11 host: SMB 445, MSRPC 135 and RDP 3389 are
    silent by design, so the absence rule routed all three to tls_scan, which
    performed three handshakes and produced zero facts on every single scan.
    """

    def test_probed_and_failed_is_not_tls(self):
        assert looks_like_tls(445, {"banner": None, "tls_probed": True}) is False
        assert looks_like_tls(135, {"banner": None, "tls_probed": True}) is False
        assert looks_like_tls(3389, {"banner": None, "tls_probed": True}) is False

    def test_probed_and_succeeded_still_routes(self):
        assert looks_like_tls(9444, {"tls": True, "tls_probed": True}) is True

    def test_absence_guess_kept_for_facts_without_the_flag(self):
        # Older probe build, or --no-tls: the inference is all we have.
        assert looks_like_tls(9443, {"banner": None}) is True

    def test_binary_protocol_ports_route_nowhere(self):
        a = Asset(host="10.0.0.9",
                  open_ports={p: _open(p) for p in (135, 445, 3389)},
                  services={p: {"banner": None, "tls_probed": True}
                            for p in (135, 445, 3389)})
        assert route_branches(a) == {}


def test_service_banner_records_tls_probed(tmp_path):
    """The flag must actually be emitted, or the router change is inert."""
    import asyncio as _a
    from scanner.service_banner import ServiceBannerScanner

    async def _run():
        async def handle(reader, writer):
            writer.close()                      # accept, say nothing, close
        server = await _a.start_server(handle, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        sc = ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                  ports=[port], timeout=1.0, greet_timeout=0.2)
        try:
            return await sc.scan_target("127.0.0.1")
        finally:
            server.close()
            await server.wait_closed()

    (res,) = _a.run(_run())
    assert res.data["tls_probed"] is True
    assert res.data.get("tls") is None
    assert looks_like_tls(9999, res.data) is False


def test_no_tls_flag_omits_the_marker():
    """--no-tls means no handshake was tried, so the absence guess must remain
    available rather than being silently suppressed by a stale flag."""
    from scanner.service_banner import ServiceBannerScanner
    sc = ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]), ports=[1],
                              try_tls=False)
    assert "tls" not in [n for n, _ in sc._ladder_for(9999)]
