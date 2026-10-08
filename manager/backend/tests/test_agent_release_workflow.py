"""
test_agent_release_workflow.py — the release pipeline's security shape, pinned.

The workflow (.github/workflows/agent-release.yml) is what turns "we have a signing scheme" into
"every release is actually signed". These tests keep its trust boundaries from eroding in a
later edit: signing keys live in one job, builds never see them, publishing builds nothing,
releases are verified against PINNED public keys and proven on Windows before they ship, and no
untrusted expression is spliced into a shell script.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

WORKFLOW = Path(__file__).resolve().parents[3] / ".github" / "workflows" / "agent-release.yml"
TEXT = WORKFLOW.read_text(encoding="utf-8")
WF = yaml.safe_load(TEXT)
JOBS = WF["jobs"]
SIGNING_SECRETS = ("AGENT_RELEASE_SIGNING_KEY", "AGENT_RELEASE_P256_KEY")


def _job_text(name: str) -> str:
    return yaml.safe_dump(JOBS[name])


def _runs(job: str):
    return [s["run"] for s in JOBS[job]["steps"] if "run" in s]


def test_triggers_are_agent_tags_and_manual_dispatch():
    on = WF.get("on") or WF.get(True)           # PyYAML reads the bare key `on` as True
    assert on["push"]["tags"] == ["agent-v*"]
    assert "workflow_dispatch" in on


def test_default_permissions_are_read_only():
    assert WF["permissions"] == {"contents": "read"}


@pytest.mark.parametrize("secret", SIGNING_SECRETS)
def test_signing_keys_exist_only_in_the_sign_job(secret):
    holders = [name for name in JOBS if secret in _job_text(name)]
    assert holders == ["sign"], holders


def test_the_sign_job_runs_in_the_protected_environment():
    assert JOBS["sign"]["environment"] == "agent-release"


def test_build_jobs_never_receive_signing_keys_or_write_access():
    for name in ("plan", "test", "images", "sbom", "windows-package"):
        text = _job_text(name)
        assert not any(s in text for s in SIGNING_SECRETS), name
        assert "contents: write" not in text.replace("'", ""), name
    assert "contents" not in (JOBS["windows-package"].get("permissions") or {})


def test_only_publish_can_write_contents():
    for name, job in JOBS.items():
        perms = job.get("permissions") or {}
        assert (perms.get("contents") == "write") == (name == "publish"), name


def test_no_expression_is_spliced_into_a_shell_script():
    """`${{ … }}` inside `run:` is how branch names and inputs become shell injection.
    Everything reaches scripts through `env:` instead."""
    for name in JOBS:
        for body in _runs(name):
            assert "${{" not in body, (name, body[:80])


def test_a_tag_must_equal_the_version_file():
    plan = "\n".join(_runs("plan"))
    assert "does not match VERSION" in plan and "agent-v" in plan


def test_release_is_verified_against_pinned_public_keys():
    sign = "\n".join(_runs("sign"))
    assert "agent_release.py verify" in sign
    assert '--public-key "$ED25519_PUB"' in sign and '--p256-public-key "$P256_PUB"' in sign
    env = next(s["env"] for s in JOBS["sign"]["steps"] if s.get("name", "").startswith("Assemble"))
    assert "vars.AGENT_RELEASE_PUBLIC_KEY" in env["ED25519_PUB"]
    assert "vars.AGENT_RELEASE_P256_PUBLIC_KEY" in env["P256_PUB"]


def test_signing_refuses_to_run_without_keys():
    sign = "\n".join(_runs("sign"))
    assert "Release signing is not configured" in sign


def test_the_key_files_are_private_and_removed():
    sign = "\n".join(_runs("sign"))
    assert "umask 077" in sign and "trap 'rm -rf" in sign


def test_windows_is_authenticode_signed_before_packaging_and_proven():
    runs = _runs("windows-package")
    sign_idx = next(i for i, r in enumerate(runs) if "Set-AuthenticodeSignature" in r)
    pack_idx = next(i for i, r in enumerate(runs) if "package-zip.ps1" in r)
    assert sign_idx < pack_idx
    assert "Get-AuthenticodeSignature" in runs[sign_idx] and "-ne 'Valid'" in runs[sign_idx]
    assert "AGENT_REQUIRE_AUTHENTICODE" in TEXT and "NOT Authenticode-signed" in TEXT
    assert "-Release" in runs[pack_idx]


def test_authenticode_certificate_is_removed_from_the_runner():
    cleanup = next(s for s in JOBS["windows-package"]["steps"] if s.get("if") == "always()")
    assert "codesign.pfx" in cleanup["run"] and "Remove-Item" in cleanup["run"]


def test_signed_thumbprint_is_pinned_into_the_manifest():
    sign = "\n".join(_runs("sign"))
    assert "--authenticode-thumbprint" in sign


def test_publishing_waits_for_signing_and_the_windows_proof():
    assert set(JOBS["publish"]["needs"]) >= {"sign", "windows-verify"}
    assert JOBS["windows-verify"]["needs"] and "sign" in JOBS["windows-verify"]["needs"]


def test_publish_builds_nothing():
    for body in _runs("publish"):
        code = re.sub(r"<<(\w+)\n.*?^\s*\1\s*$", "", body, flags=re.S | re.M)      # release-note text is not code
        assert not re.search(r"\b(docker|pip|npm|make|nuitka|python3?)\b", code), code[:80]


def test_releases_are_immutable():
    publish = "\n".join(_runs("publish"))
    assert "gh release view" in publish and "Releases are immutable" in publish
    assert "--clobber" not in publish and "gh release delete" not in publish


def test_windows_verify_refuses_every_tamper_mode_in_windows_powershell():
    text = "\n".join(_runs("windows-verify"))
    for mode in ("manifest", "signature", "package", "truncated", "oversize", "redirect"):
        assert f"Tamper = '{mode}'" in text, mode
    assert "windows-installer-e2e.ps1" in text
    assert "-Shell pwsh" in text                                   # PowerShell 7 as well as 5.1
    assert "-ExpectFailure" in text and "-ClientToken" in text     # tampering and a bad token are both refused


def test_third_party_actions_use_release_tags_not_branches():
    for uses in re.findall(r"uses:\s*([^\s#]+)", TEXT):
        assert "@" in uses, uses
        assert uses.split("@")[1] not in {"main", "master", "latest"}, uses


# ── the pieces around the workflow ───────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize("compose", ["docker-compose.yml", "manager/docker-compose.yml"])
def test_compose_passes_both_release_public_keys_to_the_api(compose):
    """Without the P-256 key in the container, a production manager silently withholds the
    Windows package. The key must reach the API through both compose files."""
    text = (REPO_ROOT / compose).read_text(encoding="utf-8")
    assert "AGENT_RELEASE_PUBLIC_KEY: ${AGENT_RELEASE_PUBLIC_KEY:-}" in text
    assert "AGENT_RELEASE_P256_PUBLIC_KEY: ${AGENT_RELEASE_P256_PUBLIC_KEY:-}" in text
    yaml.safe_load(text)                                    # still valid YAML


def test_every_release_target_exists_in_the_makefile():
    text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    for target in ("agent-keygen", "agent-keygen-p256", "agent-release", "agent-verify", "agent-publish", "agent-pull"):
        assert re.search(rf"^{target}:", text, re.M), target
    assert re.search(r"^\.PHONY:.*\bagent-pull\b.*\bagent-keygen-p256\b|^\.PHONY:.*\bagent-keygen-p256\b.*\bagent-pull\b", text, re.M)


def test_the_runbook_the_workflow_points_at_exists_and_covers_the_pipeline():
    assert "docs/operations/AGENT_DISTRIBUTION.md" in TEXT
    doc = (REPO_ROOT / "docs" / "operations" / "AGENT_DISTRIBUTION.md").read_text(encoding="utf-8")
    for needle in ("AGENT_RELEASE_P256_PUBLIC_KEY", "agent-release.yml", "make agent-pull", "-VerifyOnly",
                   "Authenticode", "agent-release` (add required reviewers", "Rotating a key"):
        assert needle in doc, needle
    for secret in (*SIGNING_SECRETS, "WINDOWS_CODESIGN_PFX_BASE64"):
        assert secret in doc, secret                         # every secret the workflow reads is documented
