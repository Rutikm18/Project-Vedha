"""Tests for agent/diagnostics.py, agent/runtime_status.py and the new CLI commands.

These are what a client leans on when an install goes wrong, so they pin three
promises: the diagnosis names the real cause and the exact fix; nothing here
changes the client's machine; and the support bundle never contains a secret.
"""
from __future__ import annotations

import datetime
import http.server
import json
import os
import socket
import ssl
import subprocess
import sys
import threading
import zipfile
from pathlib import Path

import pytest

from agent import diagnostics as dg
from agent import runtime_status as rs
from agent.doctor import Check
from agent.version import AGENT_VERSION

PROBE = Path(__file__).resolve().parent.parent
SECRETS = [
    "vet_AbCdEf123456_-xyz",
    "vpat_ZzYyXx987654",
    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.c2lnbmF0dXJlMTIz",
    "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC\n-----END PRIVATE KEY-----",
]


# ── redaction ────────────────────────────────────────────────────────────────

class TestRedaction:
    @pytest.mark.parametrize("secret", SECRETS)
    def test_credentials_are_removed_from_free_text(self, secret):
        text = f"before {secret} after"
        out = dg.redact_text(text)
        assert secret not in out
        assert out.startswith("before") and out.endswith("after")

    @pytest.mark.parametrize("line", [
        "Authorization: Bearer abcdef1234567890abcdef",
        "token=Sup3rS3cretPassw0rd",
        'password: "Sup3rS3cretPassw0rd"',
        "PROBE_ENROLL_TOKEN=Sup3rS3cretPassw0rd",
        "api_key = Sup3rS3cretPassw0rd",
        "probe_enroll_token: Sup3rS3cretPassw0rd",
        "Set DEVICE_SECRET=Sup3rS3cretPassw0rd for the agent",
        "https://user:Sup3rS3cretPassw0rd@proxy.example.com:3128",
        '{"device_secret": "Sup3rS3cretPassw0rd"}',
    ])
    def test_key_value_and_url_credentials(self, line):
        out = dg.redact_text(line)
        assert "Sup3rS3cretPassw0rd" not in out and "abcdef1234567890abcdef" not in out

    def test_ordinary_text_is_untouched(self):
        text = "Registered as 'DESKTOP-1-probe'. WebSocket connected. 12 hosts, 3 open ports."
        assert dg.redact_text(text) == text

    def test_ip_masking_is_optional(self):
        text = "scanning 10.20.30.40 and 192.168.1.77"
        assert dg.redact_text(text) == text
        assert dg.redact_text(text, mask_ips=True) == "scanning 10.20.30.x and 192.168.1.x"

    def test_env_values_with_sensitive_names_are_removed_whatever_they_hold(self):
        out = dg.redact_env({"PROBE_ENROLL_TOKEN": "anything", "PROBE_PAT": "x", "DEVICE_KEY": "y",
                             "PLATFORM_URL": "https://m.example.com", "PROBE_NAME": "PC1"})
        assert out["PROBE_ENROLL_TOKEN"] == out["PROBE_PAT"] == out["DEVICE_KEY"] == "[removed]"
        assert out["PLATFORM_URL"] == "https://m.example.com" and out["PROBE_NAME"] == "PC1"


# ── configuration file ───────────────────────────────────────────────────────

class TestEnvFile:
    def test_bom_does_not_corrupt_the_first_key(self):
        values = dg.parse_env_text("\ufeffPLATFORM_URL=https://m.example.com\n# c\nVERIFY_TLS=true\n")
        assert values == {"PLATFORM_URL": "https://m.example.com", "VERIFY_TLS": "true"}

    def test_quotes_and_blank_lines(self):
        assert dg.parse_env_text('A="x y"\n\nB=\'z\'\nnoequals\n') == {"A": "x y", "B": "z"}

    def test_windows_default_location_and_override(self):
        assert dg.default_env_file({"ProgramData": r"C:\ProgramData"}, "nt") == Path(r"C:\ProgramData") / "vedha-agent" / "agent.env"
        assert dg.default_env_file({"ProgramData": "x", "VEDHA_AGENT_ENV": "/etc/v.env"}, "nt") == Path("/etc/v.env")
        assert dg.default_env_file({}, "posix") is None
        assert dg.default_env_file({"VEDHA_AGENT_ENV": "/etc/v.env"}, "posix") == Path("/etc/v.env")

    def test_loading_never_overrides_an_explicit_variable(self, tmp_path):
        f = tmp_path / "agent.env"
        f.write_text("\ufeffPLATFORM_URL=https://from-file\nNEW=1\n", encoding="utf-8")
        env = {"PLATFORM_URL": "https://explicit"}
        assert dg.load_env_file(f, env) is True
        assert env == {"PLATFORM_URL": "https://explicit", "NEW": "1"}

    def test_missing_file_is_fine(self, tmp_path):
        assert dg.load_env_file(tmp_path / "nope.env", {}) is False
        assert dg.load_env_file(None, {}) is False


# ── runtime status ───────────────────────────────────────────────────────────

class TestRuntimeStatus:
    def test_write_then_read(self, tmp_path):
        p = tmp_path / "status.json"
        assert rs.write(p, "online", detail="d", version="2.1.0", manager="https://m", now=100.0)
        rec = rs.read(p)
        assert rec["state"] == "online" and rec["pid"] == os.getpid() and rec["updated_at"] == 100.0

    def test_since_is_kept_while_the_state_does_not_change(self, tmp_path):
        p = tmp_path / "status.json"
        rs.write(p, "retrying", now=100.0)
        rs.write(p, "retrying", now=160.0)
        assert rs.read(p)["since"] == 100.0
        rs.write(p, "online", now=200.0)
        assert rs.read(p)["since"] == 200.0

    def test_unknown_state_or_no_path_is_refused_quietly(self, tmp_path):
        assert rs.write(tmp_path / "s.json", "exploded") is False
        assert rs.write(None, "online") is False
        assert not (tmp_path / "s.json").exists()

    def test_an_unwritable_location_never_raises(self, tmp_path):
        blocker = tmp_path / "file"
        blocker.write_text("x")
        assert rs.write(blocker / "sub" / "status.json", "online") is False

    def test_garbage_files_read_as_nothing(self, tmp_path):
        p = tmp_path / "s.json"
        for content in ("", "not json", "[1,2]", '{"state": "weird"}'):
            p.write_text(content)
            assert rs.read(p) is None
        assert rs.read(tmp_path / "missing.json") is None

    def test_strings_are_bounded(self, tmp_path):
        p = tmp_path / "s.json"
        rs.write(p, "failed", reason="r" * 5000, remediation="m" * 5000)
        rec = rs.read(p)
        assert len(rec["reason"]) <= 200 and len(rec["remediation"]) <= 400

    def test_process_alive(self):
        assert rs.process_alive(os.getpid()) is True
        assert rs.process_alive(0) is False and rs.process_alive(-5) is False
        assert rs.process_alive("x") is False and rs.process_alive(None) is False

    def test_a_dead_process_is_not_online_whatever_it_last_said(self):
        record = {"state": "online", "pid": 4242, "updated_at": 100.0, "reason": ""}
        eff = rs.effective(record, now=130.0, alive=lambda pid: False)
        assert eff["state"] == "not-running" and eff["recorded_state"] == "online" and eff["running"] is False
        live = rs.effective(record, now=130.0, alive=lambda pid: True)
        assert live["state"] == "online" and live["age_seconds"] == 30

    def test_no_record_means_not_running(self):
        assert rs.effective(None)["state"] == "not-running"

    def test_path_lives_beside_the_state_file(self):
        assert rs.path_for("/x/y/state.json") == Path("/x/y/status.json")


# ── how the manager probe is classified (pure) ───────────────────────────────

def probe(**kw):
    base = dict(url="https://m.example.com", host="m.example.com", port=443, dns_ok=True, tcp_ok=True,
                tls_ok=True, http_status=200)
    base.update(kw)
    return dg.ManagerProbe(**base)


class TestClassify:
    def one(self, p):
        (check,) = dg.classify_probe(p)
        return check

    def test_healthy(self):
        c = self.one(probe())
        assert c.status == "pass" and "reachable" in c.detail

    def test_dns_failure_names_the_host_and_a_command(self):
        c = self.one(probe(dns_ok=False, tcp_ok=False, tls_ok=False, http_status=0, dns_error="not known"))
        assert c.status == "fail" and "m.example.com" in c.detail and "nslookup" in c.remediation

    def test_dns_failure_for_the_proxy_says_so(self):
        c = self.one(probe(dns_ok=False, tcp_ok=False, tls_ok=False, http_status=0, via_proxy="http://px:3128"))
        assert "proxy" in c.detail

    def test_blocked_port_points_at_firewall_or_proxy_option(self):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, tcp_error="timed out"))
        assert c.status == "fail" and "firewall" in c.remediation and "-Proxy" in c.remediation

    @pytest.mark.parametrize("error", [
        "[Errno 111] Connection refused",
        "[WinError 10061] No connection could be made because the target machine actively refused it",
    ])
    def test_refused_connection_checks_the_address_first_not_just_blames_the_firewall(self, error):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, tcp_error=error))
        assert c.status == "fail" and "Check the manager address" in c.remediation
        assert "silently dropping" not in c.remediation and "-Proxy" in c.remediation

    def test_timeout_says_a_firewall_is_dropping_the_traffic(self):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, tcp_error="[WinError 10060] timed out"))
        assert "silently dropping" in c.remediation

    def test_other_network_errors_get_a_neutral_message(self):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, tcp_error="[Errno 101] Network is unreachable"))
        assert "not open" in c.remediation and "silently dropping" not in c.remediation

    def test_with_a_proxy_the_proxy_option_is_not_suggested_again(self):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, tcp_error="x", via_proxy="http://px:3128"))
        assert "-Proxy" not in c.remediation and "through the proxy" in c.detail

    def test_proxy_login_required(self):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, proxy_status=407, via_proxy="http://px:3128"))
        assert "407" in c.detail and "login" in c.detail

    def test_proxy_refusal(self):
        c = self.one(probe(tcp_ok=False, tls_ok=False, http_status=0, proxy_status=403, via_proxy="http://px:3128"))
        assert "403" in c.detail and "m.example.com" in c.remediation

    def test_untrusted_certificate_names_the_signer_and_both_fixes(self):
        c = self.one(probe(tls_ok=False, http_status=0,
                           tls_error="[SSL: CERTIFICATE_VERIFY_FAILED] self-signed certificate in chain",
                           cert_issuer="CN=Zscaler Root CA,O=Zscaler Inc."))
        assert c.status == "fail"
        assert "Zscaler Root CA" in c.detail
        assert "TLS inspection" in c.remediation and "-CaBundle" in c.remediation

    def test_other_tls_failures_are_not_called_inspection(self):
        c = self.one(probe(tls_ok=False, http_status=0, tls_error="[SSL: WRONG_VERSION_NUMBER]"))
        assert "handshake" in c.detail and "inspection" not in c.detail.lower()

    def test_no_http_answer(self):
        c = self.one(probe(http_status=0, http_error="empty"))
        assert c.status == "fail" and "/health" in c.remediation

    def test_manager_5xx_is_a_warning_not_a_client_fault(self):
        assert self.one(probe(http_status=503)).status == "warn"

    def test_a_filter_answering_403(self):
        c = self.one(probe(http_status=403))
        assert c.status == "fail" and "uncategorised" in c.remediation


# ── the real probe, against local servers ────────────────────────────────────

class _Health(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        body = b'{"status":"healthy"}'
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # noqa: D401
        pass


def _serve(handler=_Health, ssl_context=None):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    if ssl_context is not None:
        server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _closed_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def tls_material(tmp_path_factory):
    """A throwaway CA-signed-by-nobody certificate for localhost, like a TLS-inspection gateway's."""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test Inspection Gateway"),
                      x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=2))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(key, hashes.SHA256()))
    d = tmp_path_factory.mktemp("tls")
    (d / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    (d / "key.pem").write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL,
                                                  serialization.NoEncryption()))
    return d


class TestProbeManager:
    def test_plain_http_manager_is_reachable_and_the_clock_is_read(self):
        server = _serve()
        try:
            p = dg.probe_manager(f"http://127.0.0.1:{server.server_port}", environ={})
        finally:
            server.shutdown()
        assert (p.dns_ok, p.tcp_ok, p.tls_ok, p.http_status) == (True, True, True, 200)
        assert p.clock_offset_s is None or abs(p.clock_offset_s) < 5     # BaseHTTPRequestHandler sends no Date header
        assert dg.classify_probe(p)[0].status == "pass"

    def test_closed_port_stops_at_tcp(self):
        p = dg.probe_manager(f"http://127.0.0.1:{_closed_port()}", environ={}, timeout=2)
        assert p.dns_ok and not p.tcp_ok and p.tcp_error
        assert "firewall" in dg.classify_probe(p)[0].remediation

    def test_unknown_host_stops_at_dns(self):
        p = dg.probe_manager("https://no-such-host.invalid", environ={}, timeout=2)
        assert not p.dns_ok and p.dns_error
        assert dg.classify_probe(p)[0].status == "fail"

    def test_url_without_a_host(self):
        p = dg.probe_manager("not a url", environ={})
        assert not p.dns_ok

    def test_untrusted_certificate_is_detected_and_its_signer_named(self, tls_material):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(tls_material / "cert.pem", tls_material / "key.pem")
        server = _serve(ssl_context=ctx)
        try:
            p = dg.probe_manager(f"https://localhost:{server.server_port}", environ={}, timeout=5)
        finally:
            server.shutdown()
        assert p.tcp_ok and not p.tls_ok
        assert "Test Inspection Gateway" in p.cert_issuer
        check = dg.classify_probe(p)[0]
        assert "not trusted" in check.detail and "Test Inspection Gateway" in check.detail
        assert "-CaBundle" in check.remediation

    def test_a_ca_bundle_makes_that_same_server_trusted(self, tls_material):
        """Behind TLS inspection the agent works once given the company root (PROBE_CA_BUNDLE);
        the doctor must see it the same way the agent does."""
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(tls_material / "cert.pem", tls_material / "key.pem")
        server = _serve(ssl_context=ctx)
        try:
            p = dg.probe_manager(f"https://localhost:{server.server_port}",
                                 environ={"PROBE_CA_BUNDLE": str(tls_material / "cert.pem")}, timeout=5)
        finally:
            server.shutdown()
        assert p.tls_ok and p.http_status == 200
        assert dg.classify_probe(p)[0].status == "pass"

    def test_verification_can_be_switched_off_like_the_agent(self, tls_material):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(tls_material / "cert.pem", tls_material / "key.pem")
        server = _serve(ssl_context=ctx)
        try:
            p = dg.probe_manager(f"https://localhost:{server.server_port}", environ={"VERIFY_TLS": "false"}, timeout=5)
        finally:
            server.shutdown()
        assert p.tls_ok and p.http_status == 200

    def _fake_proxy(self, answer: bytes):
        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)

        def run():
            conn, _ = listener.accept()
            conn.recv(4096)
            conn.sendall(answer)
            conn.close()
            listener.close()

        threading.Thread(target=run, daemon=True).start()
        return listener.getsockname()[1]

    @pytest.mark.parametrize("answer,status,needle", [
        (b"HTTP/1.1 407 Proxy Authentication Required\r\n\r\n", 407, "login"),
        (b"HTTP/1.1 403 Forbidden\r\n\r\n", 403, "refused"),
    ])
    def test_proxy_refusals_are_named(self, answer, status, needle):
        port = self._fake_proxy(answer)
        p = dg.probe_manager("https://manager.example.com",
                             environ={"HTTPS_PROXY": f"http://127.0.0.1:{port}"}, timeout=3)
        assert p.via_proxy and p.proxy_status == status and not p.tcp_ok
        assert needle in dg.classify_probe(p)[0].detail

    def test_no_proxy_bypasses_the_proxy(self):
        p = dg.probe_manager("https://manager.example.com", timeout=1,
                             environ={"HTTPS_PROXY": "http://127.0.0.1:9", "NO_PROXY": ".example.com"})
        assert p.via_proxy == ""

    def test_proxy_lookup_honours_scheme(self):
        assert dg._proxy_for("https://m", {"HTTPS_PROXY": "a", "HTTP_PROXY": "b"}) == "a"
        assert dg._proxy_for("http://m", {"HTTPS_PROXY": "a", "HTTP_PROXY": "b"}) == "b"
        assert dg._proxy_for("https://m", {"ALL_PROXY": "c"}) == "c"
        assert dg._proxy_for("https://m", {}) == ""


# ── status & doctor ──────────────────────────────────────────────────────────

@pytest.fixture
def agent_env(tmp_path):
    data = tmp_path / "vedha-agent"
    data.mkdir()
    return {"STATE_FILE": str(data / "state.json"), "PLATFORM_URL": "https://m.example.com",
            "PROBE_NETWORK_SEGMENTS": "192.168.1.0/24"}, data


class TestStatus:
    def test_not_started(self, agent_env):
        env, _ = agent_env
        info = dg.collect_status(env)
        assert info["state"] == "not-running" and info["enrolled"] is False and info["agent_version"] == AGENT_VERSION
        text = dg.format_status(info)
        assert "NOT RUNNING" in text and "192.168.1.0/24" in text

    def test_online(self, agent_env):
        env, data = agent_env
        rs.write(data / "status.json", "online", detail="registered", now=1000.0)
        (data / "state.json").write_text(json.dumps({"agent_id": "a-1", "token": "SECRET-TOKEN-VALUE"}))
        info = dg.collect_status(env, now=1010.0)
        assert info["state"] == "online" and info["enrolled"] is True and "pid" not in info
        assert "SECRET-TOKEN-VALUE" not in json.dumps(info) and "SECRET-TOKEN-VALUE" not in dg.format_status(info)
        assert "ONLINE" in dg.format_status(info)

    def test_pairing_instructions_are_shown(self, agent_env):
        env, data = agent_env
        rs.write(data / "status.json", "awaiting-approval", pairing_code="ABCD-1234", pairing_url="https://m/fleet/enroll")
        text = dg.format_status(dg.collect_status(env))
        assert "ABCD-1234" in text and "https://m/fleet/enroll" in text

    def test_failure_shows_why_and_fix(self, agent_env):
        env, data = agent_env
        rs.write(data / "status.json", "failed", reason="cannot reach the manager", remediation="allow outbound 443")
        text = dg.format_status(dg.collect_status(env, alive=lambda pid: True))
        assert "cannot reach the manager" in text and "allow outbound 443" in text

    def test_missing_scope_is_called_out(self, agent_env):
        env, data = agent_env
        env = {k: v for k, v in env.items() if k != "PROBE_NETWORK_SEGMENTS"}
        rs.write(data / "status.json", "online")
        assert "will not send jobs" in dg.format_status(dg.collect_status(env, alive=lambda pid: True))


class TestDoctorChecks:
    def names(self, checks):
        return {c.name: c for c in checks}

    def test_not_running_agent_is_a_failure_with_a_start_command(self, agent_env):
        env, _ = agent_env
        checks = self.names(dg.local_checks(env, dg.collect_status(env)))
        assert checks["agent"].status == "fail" and checks["agent"].remediation
        assert checks["data-folder"].status == "pass"

    def test_online_agent_passes(self, agent_env):
        env, data = agent_env
        rs.write(data / "status.json", "online")
        checks = self.names(dg.local_checks(env, dg.collect_status(env, alive=lambda pid: True)))
        assert checks["agent"].status == "pass" and "scope" not in checks

    def test_leftover_install_token_after_enrolment_warns(self, agent_env):
        env, data = agent_env
        (data / "state.json").write_text('{"agent_id": "a"}')
        rs.write(data / "status.json", "online")
        env = {**env, "PROBE_ENROLL_TOKEN": "vet_xxxxxxxx"}
        checks = self.names(dg.local_checks(env, dg.collect_status(env, alive=lambda pid: True)))
        assert checks["install-token"].status == "warn" and "-Repair" in checks["install-token"].remediation

    def test_unwritable_data_folder_fails(self, tmp_path):
        blocker = tmp_path / "file"
        blocker.write_text("x")
        env = {"STATE_FILE": str(blocker / "sub" / "state.json")}
        checks = self.names(dg.local_checks(env, dg.collect_status(env)))
        assert checks["data-folder"].status == "fail"

    def test_summary_leads_with_the_first_problem(self):
        checks = [Check("a", "pass", "fine"), Check("manager", "fail", "cannot connect", "allow port 443"),
                  Check("b", "warn", "meh")]
        assert "1 problem" in dg.summarise(checks) and "allow port 443" in dg.summarise(checks)
        assert "warning" in dg.summarise([Check("b", "warn", "meh")])
        assert "healthy" in dg.summarise([Check("a", "pass", "fine")])

    def test_run_doctor_without_a_manager_address(self, agent_env):
        env, _ = agent_env
        env = {k: v for k, v in env.items() if k != "PLATFORM_URL"}
        manager = [c for c in dg.run_doctor(env) if c.name == "manager"]
        assert manager and manager[0].status == "fail" and "-Manager" in manager[0].remediation


# ── support bundle ───────────────────────────────────────────────────────────

class TestSupportBundle:
    def plant(self, env, data):
        (data / "logs").mkdir()
        (data / "logs" / "agent.log").write_text(
            "2026-10-08 INFO agent: starting\n"
            f"2026-10-08 INFO agent: enrolling with {SECRETS[0]}\n"
            f"2026-10-08 INFO transport: Authorization: Bearer {SECRETS[2]}\n"
            "2026-10-08 INFO engine: scanned 10.1.2.3 and 10.1.2.4\n", encoding="utf-8")
        (data / "logs" / "install-20261008-101500.log").write_text(
            f"install token {SECRETS[0]}\nPROBE_ENROLL_TOKEN=Sup3rS3cretPassw0rd\n", encoding="utf-8")
        (data / "state.json").write_text(json.dumps({"agent_id": "a-1", "token": "STATE-TOKEN-SHOULD-NEVER-SHIP",
                                                     "private_key": SECRETS[3]}))
        (data / "spool").mkdir()
        (data / "spool" / "result.json").write_text('{"findings": "SPOOL-RESULT-SHOULD-NEVER-SHIP"}')
        (data / "agent.env").write_text(
            "\ufeffPLATFORM_URL=https://m.example.com\nPROBE_ENROLL_TOKEN=Sup3rS3cretPassw0rd\n"
            "HTTPS_PROXY=http://user:Sup3rS3cretPassw0rd@px:3128\n", encoding="utf-8")
        rs.write(data / "status.json", "failed", reason="cannot reach the manager", remediation="allow 443")
        return {**env, "VEDHA_AGENT_ENV": str(data / "agent.env"), "PROBE_LOG_FILE": str(data / "logs" / "agent.log")}

    def read_all(self, path):
        with zipfile.ZipFile(path) as z:
            return {n: z.read(n).decode("utf-8", "replace") for n in z.namelist()}

    def test_no_secret_survives_anywhere_in_the_bundle(self, agent_env, tmp_path):
        env, data = agent_env
        env = self.plant(env, data)
        bundle = dg.build_support_bundle(tmp_path / "out.zip", environ=env)
        contents = self.read_all(bundle)
        blob = "\n".join(contents.values())
        for secret in (SECRETS[0], SECRETS[1], SECRETS[2], "Sup3rS3cretPassw0rd", "MIIEvQIBADANBgkq",
                       "STATE-TOKEN-SHOULD-NEVER-SHIP", "SPOOL-RESULT-SHOULD-NEVER-SHIP"):
            assert secret not in blob, secret

    def test_what_is_inside(self, agent_env, tmp_path):
        env, data = agent_env
        env = self.plant(env, data)
        names = set(self.read_all(dg.build_support_bundle(tmp_path / "out.zip", environ=env)))
        assert {"README.txt", "doctor.txt", "status.json", "system.txt", "configuration.txt",
                "agent.log", "install-20261008-101500.log"} <= names
        assert not any("state" in n and n != "status.json" for n in names)        # identity file never included
        assert not any("spool" in n or n.endswith(".pem") for n in names)

    def test_the_useful_diagnosis_is_kept(self, agent_env, tmp_path):
        env, data = agent_env
        env = self.plant(env, data)
        contents = self.read_all(dg.build_support_bundle(tmp_path / "out.zip", environ=env))
        assert "cannot reach the manager" in contents["status.json"]
        assert "RESULT:" in contents["doctor.txt"]
        assert "PLATFORM_URL=https://m.example.com" in contents["configuration.txt"]
        assert "PROBE_ENROLL_TOKEN=[removed]" in contents["configuration.txt"]
        assert "scanned 10.1.2.3" in contents["agent.log"]

    def test_ip_masking(self, agent_env, tmp_path):
        env, data = agent_env
        env = self.plant(env, data)
        contents = self.read_all(dg.build_support_bundle(tmp_path / "out.zip", environ=env, mask_ips=True))
        assert "10.1.2.x" in contents["agent.log"] and "10.1.2.3" not in contents["agent.log"]
        assert "masked" in contents["README.txt"]

    def test_works_with_nothing_installed(self, agent_env, tmp_path):
        env, _ = agent_env
        contents = self.read_all(dg.build_support_bundle(tmp_path / "out.zip", environ=env))
        assert "doctor.txt" in contents and "agent.log" not in contents

    def test_default_name_in_a_directory(self, agent_env, tmp_path):
        env, _ = agent_env
        path = dg.build_support_bundle(tmp_path, environ=env)
        assert path.parent == tmp_path and path.name.startswith("vedha-support-") and path.suffix == ".zip"

    def test_huge_logs_are_tailed_not_loaded_whole(self, tmp_path):
        log = tmp_path / "big.log"
        log.write_text("\n".join(f"line {i}" for i in range(50000)))
        tail = dg.read_tail(log, max_lines=100)
        assert len(tail) == 100 and tail[-1] == "line 49999"
        assert dg.read_tail(tmp_path / "missing.log") == []


# ── the command line ─────────────────────────────────────────────────────────

def run_cli(*args, env=None, cwd=None):
    full = {**os.environ, "PYTHONPATH": str(PROBE), "PYTHONIOENCODING": "utf-8"}
    for k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"):
        full.pop(k, None)
    full.update(env or {})
    return subprocess.run([sys.executable, "-m", "agent.agent", *args], capture_output=True, text=True,
                          timeout=60, env=full, cwd=cwd or PROBE)


class TestCli:
    def test_help_lists_the_troubleshooting_commands(self):
        out = run_cli("help")
        assert out.returncode == 0
        for word in ("doctor", "status", "support-bundle", "run"):
            assert word in out.stdout

    def test_a_mistyped_command_does_not_start_the_agent(self):
        out = run_cli("doctr")
        assert out.returncode == 2 and "Unknown command: doctr" in out.stdout

    def test_status_json_is_machine_readable(self, agent_env):
        env, data = agent_env
        rs.write(data / "status.json", "awaiting-approval", pairing_code="WXYZ-9999", pairing_url="https://m/x")
        out = run_cli("status", "--json", env={**env, "VEDHA_AGENT_ENV": str(data / "none.env")})
        info = json.loads(out.stdout)
        assert out.returncode == 1                                # anything but 'online' is a non-zero exit
        assert info["state"] == "awaiting-approval"               # the writer (this test process) is alive
        assert info["pairing_code"] == "WXYZ-9999"
        assert info["agent_version"] == AGENT_VERSION
        assert "pid" not in info

    def test_status_reflects_a_live_agent(self, agent_env):
        env, data = agent_env
        proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        try:
            (data / "status.json").write_text(json.dumps({
                "state": "online", "pid": proc.pid, "updated_at": 1.0, "since": 1.0, "detail": "ok"}))
            out = run_cli("status", "--json", env=env)
            info = json.loads(out.stdout)
            assert info["state"] == "online" and out.returncode == 0
        finally:
            proc.kill()

    def test_doctor_runs_and_exits_nonzero_on_failure(self, agent_env):
        env, _ = agent_env
        out = run_cli("doctor", env={**env, "PLATFORM_URL": f"http://127.0.0.1:{_closed_port()}"})
        assert out.returncode == 1
        assert "[FAIL] manager" in out.stdout and "RESULT:" in out.stdout

    def test_support_bundle_command(self, agent_env, tmp_path):
        env, data = agent_env
        target = tmp_path / "bundle.zip"
        out = run_cli("support-bundle", "--out", str(target), "--mask-ips", env={**env, "VEDHA_AGENT_ENV": str(data / "none.env")})
        assert out.returncode == 0 and target.exists()
        assert "no passwords, tokens or keys" in out.stdout and "(masked)" in out.stdout
        assert "doctor.txt" in zipfile.ZipFile(target).namelist()

    def test_support_bundle_out_needs_a_value(self, agent_env):
        env, _ = agent_env
        assert run_cli("support-bundle", "--out", env=env).returncode == 2

    def test_the_installers_config_file_is_picked_up_by_the_cli(self, agent_env):
        env, data = agent_env
        env = {k: v for k, v in env.items() if k != "PLATFORM_URL"}
        (data / "agent.env").write_text("\ufeffPLATFORM_URL=https://from-the-config-file.example.com\n", encoding="utf-8")
        out = run_cli("status", "--json", env={**env, "VEDHA_AGENT_ENV": str(data / "agent.env")})
        assert json.loads(out.stdout)["manager"] == "https://from-the-config-file.example.com"


# ── the agent writes its own status and log file ─────────────────────────────

class TestAgentIntegration:
    def test_status_helper_is_inert_until_configured(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setattr(ag, "_STATUS_PATH", None)
        ag._status("online")          # must not raise or write anywhere

    def test_status_helper_writes_state_version_and_manager(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        monkeypatch.setenv("PLATFORM_URL", "https://m.example.com")
        ag._status("retrying", reason="r", remediation="f")
        rec = rs.read(tmp_path / "status.json")
        assert rec["state"] == "retrying" and rec["version"] == AGENT_VERSION and rec["manager"] == "https://m.example.com"

    # -- an unreachable manager at start-up --------------------------------------------

    @staticmethod
    def _transport(fail_times):
        import httpx

        class Response:
            status_code = 200

        class Client:
            calls = 0

            def get(self, *_a, **_k):
                Client.calls += 1
                if Client.calls <= fail_times:
                    raise httpx.ConnectError("[Errno 111] Connection refused")
                return Response()

        class T:
            _base_url = "https://m.example.com"
            _client = Client()

        return T(), Client

    def test_default_mode_gives_up_with_a_diagnosis_and_records_failed(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.delenv("PROBE_KEEP_RETRYING", raising=False)
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        monkeypatch.setattr(ag.time, "sleep", lambda *_: None)
        transport, _ = self._transport(fail_times=99)
        with pytest.raises(SystemExit) as stop:
            ag._wait_for_manager(transport, attempts=3, base_delay=0)
        assert stop.value.code == 2
        rec = rs.read(tmp_path / "status.json")
        assert rec["state"] == "failed" and rec["reason"] and rec["remediation"]

    def test_status_shows_retrying_after_the_first_failed_attempt(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.delenv("PROBE_KEEP_RETRYING", raising=False)
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        seen = []
        monkeypatch.setattr(ag.time, "sleep", lambda *_: seen.append(rs.read(tmp_path / "status.json")["state"]))
        transport, _ = self._transport(fail_times=99)
        with pytest.raises(SystemExit):
            ag._wait_for_manager(transport, attempts=2, base_delay=0)
        assert seen == ["retrying"]

    def test_keep_retrying_waits_for_the_manager_instead_of_exiting(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setenv("PROBE_KEEP_RETRYING", "true")
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        sleeps = []
        monkeypatch.setattr(ag.time, "sleep", lambda s: sleeps.append(s))
        transport, client = self._transport(fail_times=7)      # two full rounds of 3, then one more failure, then success
        ag._wait_for_manager(transport, attempts=3, base_delay=0)    # returns instead of raising SystemExit
        assert client.calls == 8
        assert 30.0 in sleeps and 60.0 in sleeps              # the pause between rounds grows
        assert max(sleeps) <= ag.KEEP_RETRYING_MAX_WAIT

    def test_keep_retrying_pause_is_capped(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setenv("PROBE_KEEP_RETRYING", "1")
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        sleeps = []
        monkeypatch.setattr(ag.time, "sleep", lambda s: sleeps.append(s))
        transport, _ = self._transport(fail_times=30)
        ag._wait_for_manager(transport, attempts=1, base_delay=0)
        assert max(sleeps) == ag.KEEP_RETRYING_MAX_WAIT

    def test_keep_retrying_is_off_unless_asked_for(self, monkeypatch):
        import agent.agent as ag
        monkeypatch.delenv("PROBE_KEEP_RETRYING", raising=False)
        assert ag._keep_retrying() is False
        for value in ("true", "1", "YES", "on"):
            monkeypatch.setenv("PROBE_KEEP_RETRYING", value)
            assert ag._keep_retrying() is True
        monkeypatch.setenv("PROBE_KEEP_RETRYING", "false")
        assert ag._keep_retrying() is False

    def test_reason_and_fix_are_split_for_the_status_file(self):
        import agent.agent as ag
        assert ag._reason_and_fix("connection refused — Nothing is listening") == ("connection refused", "Nothing is listening")
        reason, fix = ag._reason_and_fix("something odd")
        assert reason == "something odd" and "doctor" in fix

    def test_a_crash_is_recorded_in_the_log_and_the_status(self, tmp_path, monkeypatch, caplog):
        import logging
        import agent.agent as ag
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        with caplog.at_level(logging.CRITICAL, logger="agent"):
            try:
                raise ValueError("boom")
            except ValueError as exc:
                ag._record_crash(exc)
        rec = rs.read(tmp_path / "status.json")
        assert rec["state"] == "failed" and "ValueError: boom" in rec["reason"] and "support-bundle" in rec["remediation"]
        assert any("unexpected error" in r.getMessage() and r.exc_info for r in caplog.records)

    def test_narration_survives_a_console_that_cannot_be_written(self, monkeypatch):
        import agent.agent as ag

        class Broken:
            encoding = "utf-8"

            def write(self, *_):
                raise OSError(6, "The handle is invalid")

            def flush(self):
                raise OSError(6, "The handle is invalid")

        monkeypatch.setattr(ag.sys, "stdout", Broken())
        ag.say("this must not raise")

    def test_log_file_mirrors_logging_and_narration_and_is_size_capped(self, tmp_path, monkeypatch):
        import logging
        import agent.agent as ag
        log = tmp_path / "logs" / "agent.log"
        monkeypatch.setenv("PROBE_LOG_FILE", str(log))
        root = logging.getLogger()
        before = list(root.handlers)
        try:
            ag._attach_log_file("INFO")
            ag._attach_log_file("INFO")                        # idempotent
            added = [h for h in root.handlers if h not in before]
            assert len(added) == 1
            assert added[0].maxBytes == 10 * 1024 * 1024 and added[0].backupCount == 5
            logging.getLogger("engine").info("a log line")
            ag.say("a narrated line")
            added[0].flush()
            text = log.read_text(encoding="utf-8")
            assert "a log line" in text and "a narrated line" in text
        finally:
            for h in list(root.handlers):
                if h not in before:
                    root.removeHandler(h)
                    ag._SAY_LOG.removeHandler(h)
                    h.close()

    def test_an_unopenable_log_file_does_not_stop_the_agent(self, tmp_path, monkeypatch):
        import agent.agent as ag
        blocker = tmp_path / "file"
        blocker.write_text("x")
        monkeypatch.setenv("PROBE_LOG_FILE", str(blocker / "sub" / "agent.log"))
        ag._attach_log_file("INFO")       # must not raise

    def test_env_loader_survives_a_byte_order_mark(self, tmp_path, monkeypatch):
        import agent.agent as ag
        f = tmp_path / "x.env"
        f.write_text("\ufeffVEDHA_TEST_BOM_KEY=ok\n", encoding="utf-8")
        monkeypatch.delenv("VEDHA_TEST_BOM_KEY", raising=False)
        ag._load_env(f)
        assert os.environ.get("VEDHA_TEST_BOM_KEY") == "ok"
        monkeypatch.delenv("VEDHA_TEST_BOM_KEY", raising=False)
