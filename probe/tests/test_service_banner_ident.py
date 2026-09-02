"""
test_service_banner_ident.py — the service-identification upgrade.

Covers: the expanded soft-match table (real-world banners for the services a
network VA meets), structured HTTP head extraction, the TLS-tunnelled rung
(HTTPS on an arbitrary port yields a real banner + a positive `tls` fact), the
client-first null-rung skip, greet-timeout recall for slow speak-first daemons,
and preferring a decrypted TLS reply over plaintext noise.
"""

from __future__ import annotations

import asyncio
import datetime as _dt
import ssl

import pytest

from scanner.scanner_base import ScopeGuard
from scanner.service_banner import (
    ServiceBannerScanner, match_service, parse_http_head, PROBE_LADDER,
    _CLIENT_FIRST,
)


# ── soft-match table ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("banner,service,product,version", [
    # speak-first protocols by leading bytes
    (b"\xff\xfd\x18\xff\xfd \xff\xfd#\xff\xfd'", "telnet", None, None),
    (b"RFB 003.008\n", "vnc", None, "003.008"),
    (b"AMQP\x00\x00\x09\x01", "amqp", None, None),
    (b"\x15\x03\x01\x00\x02\x02\x28", "tls", None, None),
    # datastores
    (b"E\x00\x00\x00\x66SFATAL\x00VFATAL\x00C0A000\x00Munsupported frontend protocol 65363.19778\x00", "postgresql", "PostgreSQL", None),
    (b"HTTP/1.0 200 OK\r\nConnection: close\r\nContent-Type: text/plain\r\n\r\nIt looks like you are trying to access MongoDB over HTTP on the native driver port.\r\n", "mongodb", "MongoDB", None),
    (b'{\n  "name" : "node-1",\n  "cluster_name" : "es",\n  "version" : {\n    "number" : "7.10.2",\n    "build_flavor" : "default",\n    "lucene_version" : "8.7.0"\n  },\n  "tagline" : "You Know, for Search"\n}', "elasticsearch", "Elasticsearch", "7.10.2"),
    (b"J\x00\x00\x00\x0a8.0.32\x00\x08\x00\x00\x00\x0a\x1b\x3c\n\x4b\x21\x22\x00\xff\xff\xff\x02\x00\xff\xdf\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2a\x3b\x1c\x0e\x17\x11\x2d\x49\x3f\x28\x5c\x66\x00caching_sha2_password\x00", "mysql", "MySQL", "8.0.32"),
    (b"\x45\x00\x00\x00\xffj\x04Host '10.0.0.9' is not allowed to connect to this MariaDB server", "mysql", "MariaDB", None),
    (b"-DENIED Redis is running in protected mode because protected mode is enabled\r\n", "redis", "Redis", None),
    (b"-ERR unknown command `GET`, with args beginning with:\r\n", "redis", "Redis", None),
    # container / CI / observability over HTTP
    (b"HTTP/1.1 404 Not Found\r\nApi-Version: 1.41\r\nDocker-Experimental: false\r\nServer: Docker/20.10.7 (linux)\r\n\r\n404 page not found\n", "docker", "Docker", "20.10.7"),
    (b'HTTP/1.1 403 Forbidden\r\nContent-Type: application/json\r\n\r\n{"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User \\"system:anonymous\\" cannot get path \\"/\\"","reason":"Forbidden","code":403}', "kubernetes-api", "Kubernetes", None),
    (b"HTTP/1.1 403 Forbidden\r\nX-Jenkins: 2.401.3\r\nServer: Jetty(10.0.13)\r\n\r\n", "http", "Jenkins", "2.401.3"),
    (b"HTTP/1.1 200 OK\r\nSet-Cookie: grafana_session=abc; Path=/\r\n\r\n", "http", "Grafana", None),
    (b"HTTP/1.1 200 OK\r\n\r\n<html><head><title>Node Exporter</title></head></html>", "http", "Node Exporter", None),
    # HTTP servers with non-generic header shapes
    (b"HTTP/1.1 404 Not Found\r\nServer: Apache-Coyote/1.1\r\n\r\n<h3>Apache Tomcat/9.0.65</h3>", "http", "Apache Tomcat", "9.0.65"),
    (b"HTTP/1.1 200 OK\r\nServer: Jetty(9.4.43.v20210629)\r\n\r\n", "http", "Jetty", "9.4.43"),
    (b"HTTP/1.1 404 Not Found\r\nServer: Microsoft-HTTPAPI/2.0\r\n\r\n", "http", "Microsoft-HTTPAPI", "2.0"),
    (b"HTTP/1.1 200 OK\r\nServer: CUPS/2.3\r\n\r\n", "ipp", "CUPS", "2.3"),
    (b"HTTP/1.1 400 Bad Request\r\nServer: squid/4.13\r\n\r\n", "http-proxy", "Squid", "4.13"),
    (b"HTTP/1.1 200 OK\r\nServer: Linux/3.10 UPnP/1.0 MiniUPnPd/2.1\r\n\r\n", "upnp", None, None),
    (b"HTTP/1.1 200 OK\r\nServer: openresty/1.19.3.1\r\n\r\n", "http", "openresty", "1.19.3.1"),
    (b"HTTP/1.1 200 OK\r\nServer: Kestrel\r\nContent-Length: 0\r\n\r\n", "http", "Kestrel", None),
    (b"HTTP/1.1 200 OK\r\nServer: GoAhead-Webs\r\n\r\n", "http", "GoAhead-Webs", None),
    (b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html></html>", "http", None, None),
    # ftp / smtp / mail
    (b"220-FileZilla Server 1.6.1\r\n220 Please visit https://filezilla-project.org/\r\n", "ftp", "FileZilla Server", "1.6.1"),
    (b"220 Microsoft FTP Service\r\n", "ftp", "Microsoft FTP Service", None),
    (b"220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------\r\n", "ftp", "Pure-FTPd", None),
    (b"220 mail.corp.local Microsoft ESMTP MAIL Service, Version: 10.0.17763.1 ready at  Mon, 1 Sep 2026 10:00:00 +0000 \r\n", "smtp", "Microsoft ESMTP", "10.0.17763.1"),
    (b"220 mx.example.org ESMTP Exim 4.96 Mon, 01 Sep 2026 10:00:00 +0000\r\n", "smtp", "Exim", "4.96"),
    (b"220 host.example.org ESMTP Sendmail 8.15.2/8.15.2; Mon, 1 Sep 2026\r\n", "smtp", "Sendmail", "8.15.2/8.15.2"),
    (b"+OK Dovecot (Ubuntu) ready.\r\n", "pop3", "Dovecot", None),
    (b"* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] Dovecot ready.\r\n", "imap", "Dovecot", None),
    (b"* OK [CAPABILITY IMAP4rev1] host Cyrus IMAP v2.4.17 server ready\r\n", "imap", "Cyrus IMAP", "2.4.17"),
    (b"* OK The Microsoft Exchange IMAP4 service is ready.\r\n", "imap", "Microsoft Exchange", None),
    # media / signalling
    (b"RTSP/1.0 401 Unauthorized\r\nCSeq: 1\r\nWWW-Authenticate: Digest realm=\"cam\"\r\n\r\n", "rtsp", None, None),
    (b"SIP/2.0 200 OK\r\nVia: SIP/2.0/UDP 10.0.0.1\r\n\r\n", "sip", None, None),
    # shells on a socket
    (b"bash-5.1$ ", "shell", None, None),
    (b"Microsoft Windows [Version 10.0.19045]\r\n(c) Microsoft Corporation.\r\n\r\nC:\\Windows\\system32>", "shell", None, None),
    (b"# ", "shell", None, None),
    (b"\r\nUbuntu 22.04 LTS\r\nlogin: ", "telnet", None, None),
])
def test_match_service_table(banner, service, product, version):
    r = match_service(banner)
    assert r is not None, f"no match for {banner[:40]!r}"
    assert r["service"] == service
    assert r["product"] == product
    assert r["version"] == version


def test_existing_matches_unchanged():
    # Regression guard for the pre-existing signatures the rig validated.
    assert match_service(b"SSH-2.0-OpenSSH_8.4p1 Debian-5\r\n")["version"] == "8.4p1"
    assert match_service(b"HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n\r\n")["product"] == "nginx"
    assert match_service(b"220 (vsFTPd 3.0.3)\r\n")["product"] == "vsftpd"
    assert match_service(b"\x00\x01\x02 random noise") is None


def test_cpe_for_new_products():
    from scanner.cpe import to_cpe
    assert to_cpe("http", "Apache Tomcat", "9.0.65")["cpe23"] == \
        "cpe:2.3:a:apache:tomcat:9.0.65:*:*:*:*:*:*:*"
    assert to_cpe("http", "Jetty", "9.4.43")["product"] == "jetty"
    assert to_cpe("docker", "Docker", "20.10.7")["vendor"] == "docker"
    assert to_cpe("smtp", "Exim", "4.96")["cpe23"].startswith("cpe:2.3:a:exim:exim:4.96")
    # Apache httpd must NOT have been shadowed by the Tomcat keys.
    assert to_cpe("http", "Apache", "2.4.41")["product"] == "http_server"


# ── structured HTTP head ─────────────────────────────────────────────────────

class TestParseHttpHead:
    def test_status_server_title(self):
        raw = (b"HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\nX-Powered-By: PHP/7.4.3\r\n"
               b"Content-Type: text/html\r\n\r\n<html><head><title>  Admin\n Console </title>")
        h = parse_http_head(raw)
        assert h["http_status"] == 200
        assert h["http_server"] == "nginx/1.18.0"
        assert h["http_powered_by"] == "PHP/7.4.3"
        assert h["http_title"] == "Admin Console"

    def test_basic_auth_challenge(self):
        h = parse_http_head(b"HTTP/1.0 401 Unauthorized\r\nWWW-Authenticate: Basic realm=\"router\"\r\n\r\n")
        assert h["http_status"] == 401
        assert h["http_auth_scheme"] == "basic"

    def test_bare_lf_headers(self):
        h = parse_http_head(b"HTTP/1.0 302 Found\nLocation: https://x/\n\n")
        assert h["http_status"] == 302
        assert h["http_location"] == "https://x/"

    def test_non_http_is_empty(self):
        assert parse_http_head(b"SSH-2.0-OpenSSH_9.0\r\n") == {}
        assert parse_http_head(b"") == {}

    def test_rtsp_is_http_shaped(self):
        assert parse_http_head(b"RTSP/1.0 200 OK\r\nServer: cam/1.0\r\n\r\n")["http_server"] == "cam/1.0"


# ── ladder shape ─────────────────────────────────────────────────────────────

def _scanner(**kw) -> ServiceBannerScanner:
    return ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]), ports=[1], **kw)


class TestLadder:
    def test_tls_rung_present_after_http(self):
        names = [n for n, _ in PROBE_LADDER]
        assert names.index("tls") == names.index("http") + 1

    def test_client_first_ports_skip_null_rung(self):
        s = _scanner()
        assert 80 in _CLIENT_FIRST
        assert [n for n, _ in s._ladder_for(80)][0] == "http"
        assert [n for n, _ in s._ladder_for(9999)][0] == "null"

    def test_no_tls_flag_drops_rung(self):
        assert "tls" not in [n for n, _ in _scanner(try_tls=False)._ladder_for(9999)]

    def test_greet_timeout_tracks_operator_timeout(self):
        assert _scanner(timeout=3.0).greet_timeout == 3.0
        assert _scanner(timeout=0.5).greet_timeout == 1.5      # floor
        assert _scanner(timeout=30.0).greet_timeout == 5.0     # cap
        assert _scanner(greet_timeout=0.2).greet_timeout == 0.2


# ── live behaviour against local servers ─────────────────────────────────────

async def _serve(handler, *, ssl_ctx=None):
    server = await asyncio.start_server(handler, "127.0.0.1", 0, ssl=ssl_ctx)
    return server, server.sockets[0].getsockname()[1]


def test_slow_greeting_still_identifies():
    """A speak-first daemon that delays its 220 (reverse-DNS stall) must not be
    reported as "no banner" — the greet wait is bounded by the operator timeout,
    not a fixed 1.5s."""
    async def _run():
        async def handle(reader, writer):
            await asyncio.sleep(1.7)
            writer.write(b"220 slow.example ESMTP Postfix (Debian)\r\n")
            await writer.drain()
            writer.close()

        server, port = await _serve(handle)
        scanner = ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                       ports=[port], timeout=3.0, try_tls=False)
        try:
            return await scanner.scan_target("127.0.0.1")
        finally:
            server.close()
            await server.wait_closed()

    (res,) = asyncio.run(_run())
    assert res.data["service"] == "smtp"
    assert res.data["product"] == "Postfix"
    assert res.data["probe"] == "null"


def test_prefers_decrypted_tls_reply_over_plaintext_noise(monkeypatch):
    s = _scanner(greet_timeout=0.1)
    replies = {
        "null": (b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09", None),   # longer, garbage
        "http": (b"", None),
        "tls": (b"hello", {"tls": True, "tls_version": "TLSv1.2"}),  # shorter, decrypted
        "generic": (b"", None), "redis": (b"", None), "memcached": (b"", None),
    }

    async def fake_rung(target, port, rung_name, payload):
        return replies[rung_name]

    monkeypatch.setattr(s, "_rung", fake_rung)
    (res,) = asyncio.run(s.scan_target("127.0.0.1"))
    assert res.data["tls"] is True
    assert res.data["tls_version"] == "TLSv1.2"
    assert res.data["probe"] == "tls"
    assert res.data["banner"] == "hello"


def test_matched_rung_banner_is_the_one_reported(monkeypatch):
    """The banner and the match must come from the SAME rung (an earlier, longer
    but unidentified reply must not be reported alongside a later match)."""
    s = _scanner(greet_timeout=0.1)
    replies = {
        "null": (b"lots of unidentifiable bytes here ................", None),
        "http": (b"HTTP/1.1 200 OK\r\nServer: nginx\r\n\r\n", None),
    }

    async def fake_rung(target, port, rung_name, payload):
        return replies[rung_name]

    monkeypatch.setattr(s, "_rung", fake_rung)
    (res,) = asyncio.run(s.scan_target("127.0.0.1"))
    assert res.data["product"] == "nginx"
    assert res.data["probe"] == "http"
    assert res.data["banner"].startswith("HTTP/1.1 200 OK")
    assert res.data["http_status"] == 200


def test_closed_port_yields_nothing():
    async def _run():
        server, port = await _serve(lambda r, w: w.close())
        server.close()
        await server.wait_closed()
        s = ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                 ports=[port], timeout=1.0)
        return await s.scan_target("127.0.0.1")
    assert asyncio.run(_run()) == []


def _self_signed(tmp_path):
    cryptography = pytest.importorskip("cryptography")
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = _dt.datetime.now(_dt.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - _dt.timedelta(days=1))
            .not_valid_after(now + _dt.timedelta(days=1))
            .sign(key, hashes.SHA256()))
    cert_path = tmp_path / "cert.pem"
    key_path = tmp_path / "key.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()))
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(cert_path), str(key_path))
    return ctx


def test_https_on_arbitrary_port_identifies_and_flags_tls(tmp_path):
    """The HTTPS-on-9443 case: plaintext rungs see nothing useful, the TLS rung
    completes a handshake, sends the GET inside it and gets the real Server
    header — plus a POSITIVE tls fact the router can use."""
    server_ctx = _self_signed(tmp_path)

    async def _run():
        async def handle(reader, writer):
            try:
                await asyncio.wait_for(reader.read(1024), timeout=2.0)
            except asyncio.TimeoutError:
                pass
            writer.write(b"HTTP/1.1 200 OK\r\nServer: nginx/1.25.3\r\n"
                         b"Content-Type: text/html\r\n\r\n<title>secure admin</title>")
            await writer.drain()
            writer.close()

        server, port = await _serve(handle, ssl_ctx=server_ctx)
        scanner = ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                       ports=[port], timeout=2.0, greet_timeout=0.3)
        try:
            return await scanner.scan_target("127.0.0.1")
        finally:
            server.close()
            await server.wait_closed()

    (res,) = asyncio.run(_run())
    d = res.data
    assert d["tls"] is True
    assert d["tls_version"].startswith("TLSv1")
    assert d["probe"] == "tls"
    assert d["service"] == "http"
    assert d["product"] == "nginx"
    assert d["version"] == "1.25.3"
    assert d["http_title"] == "secure admin"
    assert d["cpe"] == "cpe:2.3:a:nginx:nginx:1.25.3:*:*:*:*:*:*:*"
    assert "(over TLS)" in res.evidence
    # Basic-over-cleartext must NOT be claimed for a TLS-protected port.
    assert "http_basic_auth_cleartext" not in d


def test_basic_auth_over_plaintext_is_recorded():
    async def _run():
        async def handle(reader, writer):
            await reader.read(1024)
            writer.write(b"HTTP/1.0 401 Unauthorized\r\nWWW-Authenticate: Basic realm=\"cam\"\r\n"
                         b"Server: GoAhead-Webs\r\n\r\n")
            await writer.drain()
            writer.close()

        server, port = await _serve(handle)
        scanner = ServiceBannerScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                       ports=[port], timeout=1.0, greet_timeout=0.2,
                                       try_tls=False)
        try:
            return await scanner.scan_target("127.0.0.1")
        finally:
            server.close()
            await server.wait_closed()

    (res,) = asyncio.run(_run())
    assert res.data["http_basic_auth_cleartext"] is True
    assert res.data["http_auth_scheme"] == "basic"
    assert res.data["product"] == "GoAhead-Webs"
    assert res.data["cpe_vendor"] == "embedthis" if "cpe_vendor" in res.data else True
