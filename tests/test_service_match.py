"""
test_service_match.py — Tier 2.5: service soft-matching (banner -> product/version).

Pure regex classification of collected banners into a service + product + version.
This is what turns "port 2222 returned some bytes" into "OpenSSH 8.4p1 on 2222",
independent of the port number (services on non-standard ports still identify).
"""

from __future__ import annotations

import pytest

from scanner.service_banner import match_service, PROBE_LADDER


class TestSshMatch:
    def test_openssh_version(self):
        r = match_service(b"SSH-2.0-OpenSSH_8.4p1 Debian-5+deb11u1\r\n")
        assert r["service"] == "ssh"
        assert r["product"] == "OpenSSH"
        assert r["version"] == "8.4p1"

    def test_dropbear(self):
        r = match_service(b"SSH-2.0-dropbear_2020.81\r\n")
        assert r["service"] == "ssh"
        assert r["product"] == "dropbear"
        assert r["version"] == "2020.81"

    def test_generic_ssh(self):
        r = match_service(b"SSH-2.0-Go\r\n")
        assert r["service"] == "ssh"
        assert r["product"] == "Go"


class TestHttpMatch:
    def test_nginx_version(self):
        r = match_service(b"HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n\r\n")
        assert r["service"] == "http"
        assert r["product"] == "nginx"
        assert r["version"] == "1.18.0"

    def test_apache_version(self):
        r = match_service(b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\n")
        assert r["product"] == "Apache"
        assert r["version"] == "2.4.41"

    def test_iis_version(self):
        r = match_service(b"HTTP/1.1 200 OK\r\nServer: Microsoft-IIS/10.0\r\n")
        assert r["product"] == "Microsoft-IIS"
        assert r["version"] == "10.0"

    def test_nginx_without_version(self):
        r = match_service(b"HTTP/1.1 403 Forbidden\r\nServer: nginx\r\n")
        assert r["product"] == "nginx"
        assert r["version"] is None


class TestOtherServices:
    def test_vsftpd(self):
        r = match_service(b"220 (vsFTPd 3.0.3)\r\n")
        assert r["service"] == "ftp"
        assert r["product"] == "vsftpd"
        assert r["version"] == "3.0.3"

    def test_smtp_postfix(self):
        r = match_service(b"220 mail.example.com ESMTP Postfix (Ubuntu)\r\n")
        assert r["service"] == "smtp"
        assert r["product"] == "Postfix"

    def test_mariadb_handshake(self):
        # MySQL/MariaDB initial handshake carries the version as a C-string.
        r = match_service(b"\x4a\x00\x00\x00\x0a5.5.5-10.3.29-MariaDB-0ubuntu0\x00")
        assert r["service"] == "mysql"
        assert r["product"] == "MariaDB"
        assert r["version"] == "10.3.29"

    def test_redis_info(self):
        r = match_service(b"$100\r\nredis_version:6.0.9\r\nredis_mode:standalone\r\n")
        assert r["service"] == "redis"
        assert r["version"] == "6.0.9"

    def test_redis_noauth(self):
        r = match_service(b"-NOAUTH Authentication required.\r\n")
        assert r["service"] == "redis"


class TestNoMatch:
    def test_unrecognized_returns_none(self):
        assert match_service(b"\x00\x01\x02 random noise") is None

    def test_empty_returns_none(self):
        assert match_service(b"") is None


class TestProbeLadder:
    def test_ladder_starts_with_null_probe(self):
        # The ladder tries a read-only NULL probe first (speak-first services),
        # only sending bytes on later rungs.
        assert PROBE_LADDER[0][0] == "null"
        assert PROBE_LADDER[0][1] is None

    def test_ladder_has_http_and_generic(self):
        names = [name for name, _ in PROBE_LADDER]
        assert "http" in names
        assert "generic" in names


class TestScannerIntegration:
    def test_scanner_identifies_ssh_on_nonstandard_port(self):
        import asyncio
        from scanner.scanner_base import ScopeGuard
        from scanner.service_banner import ServiceBannerScanner

        async def _run():
            async def handle(reader, writer):
                writer.write(b"SSH-2.0-OpenSSH_8.4p1 Debian-5\r\n")
                await writer.drain()
                writer.close()

            server = await asyncio.start_server(handle, "127.0.0.1", 0)
            port = server.sockets[0].getsockname()[1]
            scope = ScopeGuard.from_list(["127.0.0.0/8"])
            scanner = ServiceBannerScanner(scope, ports=[port], timeout=2.0)
            try:
                return await scanner.scan_target("127.0.0.1")
            finally:
                server.close()
                await server.wait_closed()

        results = asyncio.run(_run())
        assert results
        data = results[0].data
        assert data["service"] == "ssh"          # identified despite odd port
        assert data["product"] == "OpenSSH"
        assert data["version"] == "8.4p1"
        assert data["probe"] == "null"           # matched on the read-only rung
