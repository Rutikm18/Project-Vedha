from __future__ import annotations

import os
import subprocess
from pathlib import Path


INSTALLER = Path(__file__).parents[1] / "install.sh"


def test_installer_requires_only_manager_endpoint_in_dry_run() -> None:
    env = {
        **os.environ,
        "PROBE_INSTALL_DRY_RUN": "true",
        "PATH": os.environ.get("PATH", ""),
    }
    result = subprocess.run(
        ["sh", str(INSTALLER), "--manager", "https://manager.example.com/"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Manager: https://manager.example.com" in result.stdout
    assert "device-generated key" in result.stdout
    assert "PAT" not in result.stdout


def test_installer_rejects_missing_or_unknown_arguments() -> None:
    env = {**os.environ, "PROBE_INSTALL_DRY_RUN": "true"}
    missing = subprocess.run(
        ["sh", str(INSTALLER)], env=env, text=True, capture_output=True, check=False
    )
    unknown = subprocess.run(
        ["sh", str(INSTALLER), "--admin-password", "secret"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert missing.returncode == 2
    assert unknown.returncode == 2
    assert "unknown argument" in unknown.stdout


def test_installer_source_has_no_human_or_job_credentials() -> None:
    source = INSTALLER.read_text(encoding="utf-8")
    for forbidden in ("OPERATOR_TOKEN", "PROBE_PAT", "VEDHA_PAT", "JOB_ID"):
        assert forbidden not in source


def _dry_run(*args: str):
    env = {**os.environ, "PROBE_INSTALL_DRY_RUN": "true", "PATH": os.environ.get("PATH", "")}
    return subprocess.run(
        ["sh", str(INSTALLER), *args], env=env, text=True, capture_output=True, check=False
    )


def test_installer_accepts_enroll_token_and_insecure_for_http_manager() -> None:
    result = _dry_run(
        "--manager", "http://13.127.147.205:18080",
        "--enroll-token", "vet_preauthorized123",
        "--insecure",
    )

    assert result.returncode == 0, result.stderr
    assert "auto-enroll via pre-authorized token" in result.stdout
    assert "insecure http manager permitted" in result.stdout
    # the raw secret must never be echoed back
    assert "vet_preauthorized123" not in result.stdout


def test_installer_without_token_still_shows_manual_approval() -> None:
    result = _dry_run("--manager", "https://manager.example.com")

    assert result.returncode == 0, result.stderr
    assert "Fleet UI approval required" in result.stdout


def test_token_flag_selects_the_signed_manager_release() -> None:
    result = _dry_run("--manager", "https://api.vedhasec.com", "--token", "vet_fromfleet123456")

    assert result.returncode == 0, result.stderr
    assert "signed agent release from https://api.vedhasec.com/agent" in result.stdout
    assert "auto-enroll via pre-authorized token" in result.stdout
    assert "vet_fromfleet123456" not in result.stdout


def test_proxy_and_ca_flags_are_accepted(tmp_path) -> None:
    ca = tmp_path / "corp-ca.pem"
    ca.write_text("-----BEGIN CERTIFICATE-----\nMIIB\n-----END CERTIFICATE-----\n")
    result = _dry_run(
        "--manager", "https://api.vedhasec.com", "--token", "vet_x1234567",
        "--proxy", "http://proxy.corp:3128", "--no-proxy", ".corp.local",
        "--ca-bundle", str(ca), "--name", "branch-agent", "--require-signature",
    )

    assert result.returncode == 0, result.stderr
    assert "Proxy: http://proxy.corp:3128" in result.stdout
    assert f"Extra CA bundle: {ca}" in result.stdout


def test_flags_that_need_a_value_fail_cleanly() -> None:
    for flag in ("--token", "--proxy", "--ca-bundle", "--name"):
        result = _dry_run("--manager", "https://api.vedhasec.com", flag)
        assert result.returncode == 2, flag
        assert "requires" in result.stdout


def test_repo_installer_carries_empty_release_markers() -> None:
    """scripts/agent_release.py fills these in; the repo copy must keep exactly one
    empty marker each or the release build refuses to package it."""
    source = INSTALLER.read_text(encoding="utf-8")
    assert source.count('\nVEDHA_RELEASE_SPKI=""\n') == 1
    assert source.count('\nVEDHA_RELEASE_VERSION=""\n') == 1


# ── client distribution hardening ────────────────────────────────────────────

import base64
import hashlib
import importlib.util
import sys

REPO = Path(__file__).resolve().parents[2]


def _release_tool():
    spec = importlib.util.spec_from_file_location("agent_release", REPO / "scripts" / "agent_release.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["agent_release"] = mod
    spec.loader.exec_module(mod)
    return mod


def _signed_installer(tmp_path: Path) -> tuple[Path, str]:
    """The installer as a release ships it: a fresh key embedded."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization

    tool = _release_tool()
    raw = Ed25519PrivateKey.generate().public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    raw_b64 = base64.b64encode(raw).decode()
    out = tmp_path / "install.sh"
    tool.embed_installer(INSTALLER, out, spki_b64=tool.spki_b64_from_raw(raw_b64), version="9.9.9")
    return out, tool.key_id(raw_b64)


def test_token_can_come_from_a_file(tmp_path: Path) -> None:
    token = tmp_path / "token.txt"
    token.write_text("vet_abc123\n")
    result = _dry_run("--manager", "https://m.example.com", "--token-file", str(token))
    assert result.returncode == 0, result.stdout
    assert "signed agent release" in result.stdout
    assert "vet_abc123" not in result.stdout


def test_empty_or_missing_token_file_is_refused(tmp_path: Path) -> None:
    empty = tmp_path / "empty.txt"
    empty.write_text("\n")
    assert _dry_run("--manager", "https://m.example.com", "--token-file", str(empty)).returncode == 2
    assert _dry_run("--manager", "https://m.example.com", "--token-file", str(tmp_path / "nope")).returncode == 2


def test_signed_installer_shows_the_key_id_the_release_tool_computes(tmp_path: Path) -> None:
    installer, expected = _signed_installer(tmp_path)
    env = {**os.environ, "PROBE_INSTALL_DRY_RUN": "true"}
    result = subprocess.run(
        ["sh", str(installer), "--manager", "https://m.example.com", "--token", "vet_x"],
        env=env, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"Release signing key: {expected} (signature required)" in result.stdout


def test_signed_installer_cannot_be_told_to_skip_the_signature() -> None:
    source = INSTALLER.read_text(encoding="utf-8")
    # The embedded key forces the requirement after the environment is read.
    assert 'if [ -n "$VEDHA_RELEASE_SPKI" ]; then PROBE_REQUIRE_SIGNATURE=true; fi' in source


def test_upgrade_recreates_the_container_but_keeps_the_identity_volume() -> None:
    source = INSTALLER.read_text(encoding="utf-8")
    block = source[source.index('existing_image="$(docker inspect'):]
    block = block[: block.index("fi\nelse")]
    assert 'docker rm -f "$NAME"' in block and "run_probe_container" in block
    assert "docker volume rm" not in block
