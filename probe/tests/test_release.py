"""Phase 10 — release integrity + SBOM. Pure: the checksum manifest that the
strict-security verify_download (Phase 7) consumes, and a CycloneDX SBOM from
requirements."""
from __future__ import annotations

from agent import release as rel


def test_manifest_and_verify_roundtrip(tmp_path):
    (tmp_path / "a.txt").write_text("alpha")
    (tmp_path / "b.txt").write_text("beta")
    manifest = rel.sha256_manifest(str(tmp_path), ["a.txt", "b.txt"])
    assert set(manifest) == {"a.txt", "b.txt"}
    ok, bad = rel.verify_manifest(str(tmp_path), manifest)
    assert ok and bad == []


def test_verify_detects_tamper(tmp_path):
    (tmp_path / "a.txt").write_text("alpha")
    manifest = rel.sha256_manifest(str(tmp_path), ["a.txt"])
    (tmp_path / "a.txt").write_text("ALPHA-tampered")
    ok, bad = rel.verify_manifest(str(tmp_path), manifest)
    assert not ok and bad == ["a.txt"]


def test_parse_requirements_skips_comments_and_inline():
    text = "# header\n\nhttpx>=0.27\nimpacket>=0.11.0     # smb\n"
    reqs = rel.parse_requirements(text)
    assert reqs == [("httpx", ">=0.27"), ("impacket", ">=0.11.0")]


def test_sbom_is_cyclonedx_with_components():
    text = "httpx>=0.27\nwebsockets>=12.0\ncryptography>=42.0\n"
    sbom = rel.sbom_from_requirements(text, component_name="vedha-agent", version="1.0.0")
    assert sbom["bomFormat"] == "CycloneDX"
    assert sbom["metadata"]["component"]["name"] == "vedha-agent"
    names = {c["name"] for c in sbom["components"]}
    assert {"httpx", "websockets", "cryptography"} <= names
    for c in sbom["components"]:
        assert c["type"] == "library" and c["name"] and "version" in c
