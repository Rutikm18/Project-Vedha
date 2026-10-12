"""The release tool (build machine) and release_trust (the agent) are two halves of one contract.

These tests build a REAL release with scripts/agent_release.py (Docker and the Windows build replaced
by fakes) and hand its installer, manifest and P-256 signature to the agent's verifier, so the signed
fields the agent depends on (windows_installer.sha256, version, agent_version, expires, the key line
in the installer) can never drift apart silently.
"""
from __future__ import annotations

import importlib.util
import json
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from agent import release_trust as rt

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("agent_release_tool_trust", REPO / "scripts" / "agent_release.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)


def build(tmp_path, **kw):
    tool.keygen(tmp_path / "ed.pem")
    tool.keygen_p256(tmp_path / "p256.pem")
    win = tmp_path / "win.zip"
    with zipfile.ZipFile(win, "w") as zf:
        zf.writestr("vedha-agent/vedha-agent.exe", b"MZ")
        zf.writestr("install.ps1", "# inner\n")
    final = tool.build_release(
        key_path=tmp_path / "ed.pem", out=tmp_path / "out", arches=["amd64"], version=kw.pop("version", "1.0.500"),
        builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(b"img" * 20),
        p256_key_path=tmp_path / "p256.pem", windows_zip=win, agent_version=kw.pop("agent_version", "2.3.0"), **kw,
    )
    spki = tool.p256_spki_b64(tool.load_p256_private_key(tmp_path / "p256.pem"))
    return (final, spki, (final / "install.ps1").read_bytes(), (final / "manifest.json").read_bytes(),
            (final / tool.P256_SIG_FILE).read_text())


def test_a_release_built_by_the_tool_passes_the_agents_verifier(tmp_path):
    _, spki, installer, manifest, sig = build(tmp_path)
    verdict = rt.verify_update(rt.Pin(spki, "1.0.499"), manifest, sig, installer, current_agent_version="2.2.8")
    assert verdict.ok, verdict
    assert verdict.manifest["agent_version"] == "2.3.0" and "expires" not in verdict.manifest


def test_the_tools_installer_is_refused_if_any_byte_changes(tmp_path):
    _, spki, installer, manifest, sig = build(tmp_path)
    verdict = rt.verify_update(rt.Pin(spki), manifest, sig, installer + b"\n# extra", current_agent_version="2.2.8")
    assert verdict.reason == "installer-mismatch"


def test_expires_days_is_signed_into_the_manifest_and_enforced(tmp_path):
    _, spki, installer, manifest, sig = build(tmp_path, expires_days=30)
    expires = datetime.fromisoformat(json.loads(manifest)["expires"])
    assert timedelta(days=29) < expires - datetime.now(timezone.utc) < timedelta(days=31)
    assert rt.verify_update(rt.Pin(spki), manifest, sig, installer, current_agent_version="2.2.8").ok
    later = datetime.now(timezone.utc) + timedelta(days=31)
    verdict = rt.verify_update(rt.Pin(spki), manifest, sig, installer, current_agent_version="2.2.8", now=later)
    assert verdict.reason == "expired"


@pytest.mark.parametrize("days", [0, -1, 4000])
def test_a_silly_expiry_is_refused_by_the_tool(tmp_path, days):
    with pytest.raises(tool.ReleaseError, match="expires-days"):
        build(tmp_path, expires_days=days)


def test_the_key_the_tool_embeds_is_the_one_the_agent_pins(tmp_path):
    _, spki, installer, manifest, sig = build(tmp_path)
    assert f"$script:VedhaReleaseP256Spki = '{spki}'".encode() in installer
    (tmp_path / "second").mkdir()
    other_spki = build(tmp_path / "second")[1]                  # a different release key
    assert rt.verify_update(rt.Pin(other_spki), manifest, sig, installer, current_agent_version="2.2.8").reason == "bad-signature"
