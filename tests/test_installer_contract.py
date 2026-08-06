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
        ["sh", str(INSTALLER), "--token", "secret"],
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
