"""Phase 7 — bootstrap logic: per-OS Python install command, and the optional
strict-security verification of the fetched installer (skippable in this initial
phase). Pure."""
from __future__ import annotations

import hashlib

from agent import bootstrap as b


def test_python_install_cmd_per_pm():
    assert "python3-venv" in b.python_install_cmd("linux", "apt")
    assert b.python_install_cmd("linux", "dnf")[:2] == ["dnf", "install"]
    assert b.python_install_cmd("linux", "pacman")[0] == "pacman"
    assert "python" in " ".join(b.python_install_cmd("macos", "brew"))
    assert "Python" in " ".join(b.python_install_cmd("windows", "winget"))
    assert b.python_install_cmd("linux", "unknown") == []   # manual → empty


def test_security_mode_defaults_permissive_but_strict_available():
    assert b.security_mode(strict=False, insecure=False) == "permissive"  # initial-phase default
    assert b.security_mode(strict=True, insecure=False) == "strict"
    assert b.security_mode(strict=False, insecure=True) == "permissive"
    # strict wins a conflicting pair (safer)
    assert b.security_mode(strict=True, insecure=True) == "strict"


def test_verify_download_match_is_ok_in_both_modes():
    data = b"installer-bytes"
    good = hashlib.sha256(data).hexdigest()
    ok, _ = b.verify_download(data, good, "strict")
    assert ok
    ok2, _ = b.verify_download(data, good, "permissive")
    assert ok2


def test_verify_download_mismatch_fails_strict_but_warns_permissive():
    data = b"installer-bytes"
    ok_s, reason_s = b.verify_download(data, "deadbeef", "strict")
    assert not ok_s and "mismatch" in reason_s.lower()
    ok_p, reason_p = b.verify_download(data, "deadbeef", "permissive")
    assert ok_p and reason_p                    # continues, but with a warning reason


def test_verify_download_missing_checksum_fails_strict_only():
    data = b"x"
    ok_s, _ = b.verify_download(data, None, "strict")
    assert not ok_s
    ok_p, _ = b.verify_download(data, None, "permissive")
    assert ok_p
