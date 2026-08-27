"""
test_ssh_scanner.py — SSH configuration audit (Tier 2.x, §6 of the VA checklist).

The socket handshake can't run portably in CI, so these cover the pure logic that
carries the security verdict:
  * SSH identification-string (banner) parsing
  * SSH_MSG_KEXINIT wire parsing (RFC 4253 §7.1 name-lists)
  * algorithm evaluation against the vendored weakness DB (ported from ssh-audit,
    MIT — algorithm→[versions, failures, warnings, infos])
  * Terrapin (CVE-2023-48795) strict-kex heuristic

Faithful verdicts mirror ssh-audit's MASTER_DB (e.g. diffie-hellman-group1-sha1 =
1024-bit modulus + Logjam + SHA-1; aes128-cbc = weak *mode* warning, not a failure).
"""

from __future__ import annotations

import asyncio
import struct

from scanner import ssh_scanner as ssh
from scanner import ssh_kexdb
from scanner import findings
from scanner.scanner_base import ScopeGuard


# ── helpers to craft wire bytes ───────────────────────────────────────────────

def _nl(items) -> bytes:
    """Encode an SSH name-list: uint32 length + comma-joined ASCII."""
    body = ",".join(items).encode()
    return struct.pack(">I", len(body)) + body


def _kexinit(kex, hostkey, enc, mac, *, comp=("none",), lang=(),
             include_type_byte=True) -> bytes:
    p = b"\x14" if include_type_byte else b""      # SSH_MSG_KEXINIT = 20
    p += b"\x00" * 16                               # cookie
    p += _nl(kex) + _nl(hostkey)
    p += _nl(enc) + _nl(enc)                        # c2s, s2c
    p += _nl(mac) + _nl(mac)
    p += _nl(comp) + _nl(comp)
    p += _nl(lang) + _nl(lang)
    p += b"\x00"                                    # first_kex_packet_follows
    p += b"\x00\x00\x00\x00"                        # reserved
    return p


# ── banner parsing ────────────────────────────────────────────────────────────

class TestParseBanner:
    def test_openssh_with_comments(self):
        b = ssh.parse_ssh_banner("SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
        assert b["protocol"] == "2.0"
        assert b["software"] == "OpenSSH_8.2p1"
        assert b["comments"] == "Ubuntu-4ubuntu0.5"

    def test_dropbear_no_comments_from_bytes(self):
        b = ssh.parse_ssh_banner(b"SSH-2.0-dropbear_2020.81\r\n")
        assert b["software"] == "dropbear_2020.81"
        assert b["comments"] is None

    def test_rejects_non_ssh(self):
        assert ssh.parse_ssh_banner("HTTP/1.1 200 OK") is None


# ── KEXINIT parsing ───────────────────────────────────────────────────────────

class TestParseKexinit:
    def test_parses_all_name_lists(self):
        p = _kexinit(["curve25519-sha256"], ["ssh-ed25519"],
                     ["aes128-ctr"], ["hmac-sha2-256"])
        k = ssh.parse_kexinit(p)
        assert k["kex_algorithms"] == ["curve25519-sha256"]
        assert k["server_host_key_algorithms"] == ["ssh-ed25519"]
        assert k["encryption_s2c"] == ["aes128-ctr"]
        assert k["mac_s2c"] == ["hmac-sha2-256"]

    def test_handles_payload_without_leading_type_byte(self):
        p = _kexinit(["curve25519-sha256"], ["ssh-ed25519"],
                     ["aes128-ctr"], ["hmac-sha2-256"], include_type_byte=False)
        k = ssh.parse_kexinit(p)
        assert k["kex_algorithms"] == ["curve25519-sha256"]

    def test_empty_language_list(self):
        p = _kexinit(["curve25519-sha256"], ["ssh-ed25519"],
                     ["aes128-ctr"], ["hmac-sha2-256"], lang=())
        k = ssh.parse_kexinit(p)
        assert k["languages_s2c"] == []


# ── algorithm evaluation (the security verdict) ───────────────────────────────

class TestEvaluate:
    def _eval(self, kex, hostkey, enc, mac):
        return ssh.evaluate_algorithms(
            ssh.parse_kexinit(_kexinit(kex, hostkey, enc, mac)))

    def test_group1_sha1_is_failure_with_modulus_and_sha1_reasons(self):
        r = self._eval(["diffie-hellman-group1-sha1"], ["ssh-ed25519"],
                       ["aes128-ctr"], ["hmac-sha2-256"])
        f = [x for x in r["failures"] if x["algorithm"] == "diffie-hellman-group1-sha1"]
        assert f, "group1-sha1 must be a failure"
        reasons = " ".join(f[0]["reasons"])
        assert "SHA-1" in reasons
        assert "1024" in reasons

    def test_cbc_cipher_is_warning_not_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["aes128-cbc"], ["hmac-sha2-256"])
        assert not any(x["algorithm"] == "aes128-cbc" for x in r["failures"])
        assert any(x["algorithm"] == "aes128-cbc" for x in r["warnings"])

    def test_arcfour_is_rc4_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["arcfour"], ["hmac-sha2-256"])
        assert any(x["algorithm"] == "arcfour" for x in r["failures"])

    def test_hmac_md5_is_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["aes128-ctr"], ["hmac-md5"])
        assert any(x["algorithm"] == "hmac-md5" for x in r["failures"])

    def test_ssh_rsa_hostkey_is_sha1_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-rsa"],
                       ["aes128-ctr"], ["hmac-sha2-256"])
        assert any(x["algorithm"] == "ssh-rsa" for x in r["failures"])

    def test_modern_set_is_clean(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["chacha20-poly1305@openssh.com"],
                       ["hmac-sha2-256-etm@openssh.com"])
        assert r["failures"] == []

    def test_unknown_algorithm_is_recorded_not_failed(self):
        r = self._eval(["totally-made-up-kex"], ["ssh-ed25519"],
                       ["aes128-ctr"], ["hmac-sha2-256"])
        assert any(x["algorithm"] == "totally-made-up-kex" for x in r["unknown"])
        assert not any(x["algorithm"] == "totally-made-up-kex" for x in r["failures"])


# ── Terrapin (CVE-2023-48795) ─────────────────────────────────────────────────

class TestTerrapin:
    def test_strict_kex_present_is_not_vulnerable(self):
        r = ssh.evaluate_algorithms(ssh.parse_kexinit(_kexinit(
            ["curve25519-sha256", "kex-strict-s-v00@openssh.com"],
            ["ssh-ed25519"], ["chacha20-poly1305@openssh.com"],
            ["hmac-sha2-256-etm@openssh.com"])))
        assert r["supports_strict_kex"] is True
        assert r["terrapin_vulnerable"] is False

    def test_chacha20_without_strict_kex_is_vulnerable(self):
        r = ssh.evaluate_algorithms(ssh.parse_kexinit(_kexinit(
            ["curve25519-sha256"], ["ssh-ed25519"],
            ["chacha20-poly1305@openssh.com"],
            ["hmac-sha2-256-etm@openssh.com"])))
        assert r["supports_strict_kex"] is False
        assert r["terrapin_vulnerable"] is True


# ── scanner (network isolated via a patched probe) ────────────────────────────

class TestSSHScanner:
    def _scanner(self):
        return ssh.SSHScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                              rate=1e9, concurrency=4, timeout=0.1, ports=[22])

    def test_weak_server_reports_open_with_failures(self):
        sc = self._scanner()
        kex = _kexinit(["diffie-hellman-group1-sha1"], ["ssh-rsa"],
                       ["aes128-cbc"], ["hmac-md5"])
        sc._probe = lambda target, port: ("SSH-2.0-OpenSSH_5.3", kex)
        res = asyncio.run(sc.scan_target("10.0.0.9"))
        assert len(res) == 1
        r = res[0]
        assert r.status == "open" and r.port == 22
        assert r.data["banner"]["software"] == "OpenSSH_5.3"
        algos = {f["algorithm"] for f in r.data["failures"]}
        assert {"diffie-hellman-group1-sha1", "hmac-md5"} <= algos

    def test_no_response_is_filtered(self):
        sc = self._scanner()
        sc._probe = lambda target, port: (None, None)
        res = asyncio.run(sc.scan_target("10.0.0.9"))
        assert res[0].status == "filtered"


# ── findings integration ──────────────────────────────────────────────────────

class TestSSHFindings:
    def _fact(self, **data):
        return {"scanner": "ssh_scan", "target": "10.0.0.9", "port": 22,
                "status": "open", "data": data}

    def test_weak_algorithms_raise_finding(self):
        fact = self._fact(
            failures=[{"category": "mac", "algorithm": "hmac-md5",
                       "reasons": ["using broken MD5 hash algorithm"]}],
            warnings=[], terrapin_vulnerable=False)
        out = findings.run_findings([fact])
        assert any(f.rule_id == "SSH-WEAK-ALGO" for f in out)

    def test_terrapin_raises_finding(self):
        fact = self._fact(failures=[], warnings=[], terrapin_vulnerable=True)
        out = findings.run_findings([fact])
        assert any(f.rule_id == "SSH-TERRAPIN" for f in out)

    def test_clean_server_raises_nothing(self):
        fact = self._fact(failures=[], warnings=[], terrapin_vulnerable=False)
        out = findings.run_findings([fact])
        assert not any(f.rule_id.startswith("SSH-") for f in out)


# ── vendored DB (ssh_kexdb) — the "content" half, ported verbatim from ssh-audit ─

class TestVendoredDB:
    def test_full_db_is_large_not_a_subset(self):
        # The full MASTER_DB has hundreds of entries across four categories — this
        # guards against silently regressing back to a hand-curated subset (which
        # would turn real weak algorithms into 'unknown' = false negatives).
        total = sum(len(ssh_kexdb.MASTER_DB[c]) for c in ("kex", "key", "enc", "mac"))
        assert total > 300, f"expected the full vendored DB, got only {total} entries"

    def test_lookup_exact_and_unknown(self):
        assert ssh_kexdb.lookup("kex", "diffie-hellman-group1-sha1")[0]   # fails
        assert ssh_kexdb.lookup("enc", "aes128-cbc")[0] == []             # warn only
        assert ssh_kexdb.lookup("enc", "aes128-cbc")[1]                   # has a warning
        assert ssh_kexdb.lookup("kex", "totally-made-up") is None         # unknown

    def test_gss_wildcard_match(self):
        # GSS algorithms carry variable base64 after a fixed prefix; ssh-audit
        # matches them against DB keys ending in '-*'.
        fails = ssh_kexdb.lookup("kex", "gss-group1-sha1-toWM5Slw5Ew8Mqkay+al2g==")
        assert fails is not None and fails[0], "GSS wildcard must resolve to a failure"


# ── full-DB coverage: algorithms the old hand-subset did NOT contain ───────────

class TestFullDBCoverage:
    def _eval(self, kex, hostkey, enc, mac):
        return ssh.evaluate_algorithms(
            ssh.parse_kexinit(_kexinit(kex, hostkey, enc, mac)))

    def test_rijndael_cbc_cipher_is_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["rijndael128-cbc"], ["hmac-sha2-256"])
        assert any(x["algorithm"] == "rijndael128-cbc" for x in r["failures"])

    def test_3des_ctr_cipher_is_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["3des-ctr"], ["hmac-sha2-256"])
        assert any(x["algorithm"] == "3des-ctr" for x in r["failures"])

    def test_hmac_ripemd160_is_failure(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["aes128-ctr"], ["hmac-ripemd160"])
        assert any(x["algorithm"] == "hmac-ripemd160" for x in r["failures"])

    def test_gss_kex_offered_by_server_is_failure(self):
        r = self._eval(["gss-group1-sha1-toWM5Slw5Ew8Mqkay+al2g=="], ["ssh-ed25519"],
                       ["aes128-ctr"], ["hmac-sha2-256"])
        algos = {x["algorithm"] for x in r["failures"]}
        assert "gss-group1-sha1-toWM5Slw5Ew8Mqkay+al2g==" in algos


# ── false-positive guards (the ssh-rsa vs rsa-sha2 distinction) ────────────────

class TestNoFalsePositives:
    def _eval(self, kex, hostkey, enc, mac):
        return ssh.evaluate_algorithms(
            ssh.parse_kexinit(_kexinit(kex, hostkey, enc, mac)))

    def test_rsa_sha2_hostkeys_are_not_failures(self):
        # rsa-sha2-256/512 are the MODERN signature algorithms and must NOT be
        # flagged (only the legacy ssh-rsa SHA-1 host key algorithm is a failure).
        r = self._eval(["curve25519-sha256"], ["rsa-sha2-512", "rsa-sha2-256"],
                       ["aes128-ctr"], ["hmac-sha2-256"])
        assert r["failures"] == []

    def test_ed25519_hostkey_is_clean(self):
        r = self._eval(["curve25519-sha256"], ["ssh-ed25519"],
                       ["aes256-gcm@openssh.com"], ["hmac-sha2-256-etm@openssh.com"])
        assert r["failures"] == [] and r["terrapin_vulnerable"] is False


# ── Terrapin fidelity fixes vs ssh-audit ──────────────────────────────────────

class TestTerrapinFidelity:
    def _ev(self, kex, enc, mac):
        return ssh.evaluate_algorithms(ssh.parse_kexinit(
            _kexinit(kex, ["ssh-ed25519"], enc, mac)))

    def test_chacha20_without_openssh_suffix_still_vulnerable(self):
        # ssh-audit matches chacha20-poly1305 by PREFIX, so the un-suffixed name
        # is caught too.
        r = self._ev(["curve25519-sha256"], ["chacha20-poly1305"], ["hmac-sha2-256"])
        assert r["terrapin_vulnerable"] is True

    def test_cbc_plus_etm_is_vulnerable_without_strict_kex(self):
        r = self._ev(["curve25519-sha256"], ["aes128-cbc"],
                     ["hmac-sha2-256-etm@openssh.com"])
        assert r["terrapin_vulnerable"] is True

    def test_cbc_without_etm_mac_is_not_terrapin(self):
        # A CBC cipher alone (no ETM MAC) is not the Terrapin condition.
        r = self._ev(["curve25519-sha256"], ["aes128-cbc"], ["hmac-sha2-256"])
        assert r["terrapin_vulnerable"] is False


# ── parity: the capability is wired into the PRODUCT tree (main_scripts) ───────

class TestMainScriptsParity:
    def test_main_scripts_scanner_and_findings_agree(self):
        from main_scripts import ssh_scanner as mssh
        from main_scripts import findings as mfindings
        # engine parity: same weak-algorithm verdict from the main_scripts tree
        r = mssh.evaluate_algorithms(mssh.parse_kexinit(_kexinit(
            ["diffie-hellman-group1-sha1"], ["ssh-rsa"], ["aes128-cbc"], ["hmac-md5"])))
        algos = {x["algorithm"] for x in r["failures"]}
        assert {"diffie-hellman-group1-sha1", "ssh-rsa", "hmac-md5"} <= algos
        # findings parity: the product tree derives the SSH findings
        fact = {"scanner": "ssh_scan", "target": "10.0.0.9", "port": 22,
                "status": "open",
                "data": {"failures": r["failures"], "terrapin_vulnerable": True}}
        ids = {f.rule_id for f in mfindings.run_findings([fact])}
        assert "SSH-WEAK-ALGO" in ids and "SSH-TERRAPIN" in ids

    def test_main_scripts_vendored_db_matches_scanner_tree(self):
        from main_scripts import ssh_kexdb as mkexdb
        a = sum(len(ssh_kexdb.MASTER_DB[c]) for c in ("kex", "key", "enc", "mac"))
        b = sum(len(mkexdb.MASTER_DB[c]) for c in ("kex", "key", "enc", "mac"))
        assert a == b
