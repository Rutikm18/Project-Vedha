"""test_onprem_bundle_tool.py — scripts/onprem_bundle.py: one customer, one sealed bundle.

Docker and age are replaced by fakes (the fake "encryptor" copies the tar), so
the test can open the bundle and check what the customer's loader will check:
a signed manifest that lists every file with its hash, the vendor key embedded
in the loader, and a ledger line recording who got which bundle.
"""
from __future__ import annotations

import base64
import importlib.util
import json
import shutil
import tarfile
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

REPO = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location("onprem_bundle", REPO / "scripts" / "onprem_bundle.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)

RECIPIENT = "age1" + "q" * 58


def _fake_saver(tags, dest: Path):
    dest.write_bytes(("docker save " + " ".join(tags)).encode() * 20)


def _fake_ids(tags):
    return {tag: "sha256:" + "a" * 64 for tag in tags}


def _copy_encryptor(source: Path, dest: Path, recipients):
    assert recipients == [RECIPIENT]
    shutil.copy2(source, dest)


@pytest.fixture
def key(tmp_path):
    path = tmp_path / "vendor.pem"
    return path, tool.release.keygen(path)


def _build(tmp_path, key_path, **kw):
    return tool.build_bundle(
        customer=kw.pop("customer", "ACME Bank Ltd"), recipients=kw.pop("recipients", [RECIPIENT]),
        key_path=key_path, out=tmp_path / "out", version="1.0.400", build_images=False,
        saver=_fake_saver, ids=_fake_ids, encryptor=_copy_encryptor, **kw,
    )


def _open(tmp_path, entry) -> Path:
    dest = tmp_path / "opened"
    with tarfile.open(tmp_path / "out" / entry["file"]) as tar:
        tar.extractall(dest, filter="data")
    return next(dest.iterdir())


def test_bundle_is_signed_and_lists_every_file(tmp_path, key):
    key_path, public = key
    entry = _build(tmp_path, key_path)
    assert entry["file"] == "vedha-onprem-acme-bank-ltd-1.0.400.tar.age"
    root = _open(tmp_path, entry)

    manifest_bytes = (root / "manifest.json").read_bytes()
    signature = base64.b64decode((root / "manifest.json.sig").read_text().strip())
    Ed25519PublicKey.from_public_bytes(base64.b64decode(public)).verify(signature, manifest_bytes)

    manifest = json.loads(manifest_bytes)
    assert manifest["customer"] == "ACME Bank Ltd" and manifest["bundle_id"] == entry["bundle_id"]
    on_disk = sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                     if p.is_file() and p.name not in ("manifest.json", "manifest.json.sig"))
    assert sorted(f["path"] for f in manifest["files"]) == on_disk
    assert "compose/.env.example" in on_disk  # dotfiles are covered too
    for item in manifest["files"]:
        assert tool.release.sha256_file(root / item["path"]) == item["sha256"]
    tags = {i["tag"] for i in manifest["images"]}
    assert {"vedha-backend:1.0.400", "vedha-frontend:1.0.400", "postgres:16-alpine"} <= tags
    env = (root / "compose" / ".env.example").read_text()
    assert "VEDHA_BACKEND_IMAGE=vedha-backend:1.0.400" in env


def test_loader_embeds_the_vendor_key_and_ledger_records_the_bundle(tmp_path, key):
    key_path, public = key
    entry = _build(tmp_path, key_path)
    loader = (tmp_path / "out" / "vedha-onprem-load.sh").read_text()
    assert f'VEDHA_VENDOR_SPKI="{tool.release.spki_b64_from_raw(public)}"' in loader
    sha_line = (tmp_path / "out" / "vedha-onprem-acme-bank-ltd-1.0.400.sha256").read_text()
    assert sha_line.split()[0] == entry["sha256"]
    ledger = [json.loads(line) for line in (tmp_path / "out" / "ledger.jsonl").read_text().splitlines()]
    assert ledger[-1]["bundle_id"] == entry["bundle_id"]
    assert RECIPIENT not in json.dumps(ledger)  # only a fingerprint of the recipient


def test_agent_release_is_included_when_it_verifies(tmp_path, key):
    key_path, public = key
    agent_out = tmp_path / "agent"
    tool.release.build_release(
        key_path=key_path, out=agent_out, arches=["amd64"], version="1.0.400",
        builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(b"image" * 10),
    )
    entry = _build(tmp_path, key_path, agent_release_dir=agent_out)
    root = _open(tmp_path, entry)
    assert (root / "agent-release" / "CURRENT").read_text().strip() == "1.0.400"
    assert (root / "agent-release" / "PUBLIC_KEY").read_text().strip() == public
    from app import agent_release
    agent_release.clear_cache()
    assert agent_release.load_release(root / "agent-release", public).version == "1.0.400"


def test_refuses_a_bundle_without_a_valid_recipient(tmp_path, key):
    key_path, _ = key
    with pytest.raises(tool.ReleaseError, match="recipient"):
        _build(tmp_path, key_path, recipients=[])
    with pytest.raises(tool.ReleaseError, match="not an age recipient"):
        _build(tmp_path, key_path, recipients=["hunter2"])


def test_one_bundle_per_customer_and_version(tmp_path, key):
    key_path, _ = key
    _build(tmp_path, key_path)
    with pytest.raises(tool.ReleaseError, match="already exists"):
        _build(tmp_path, key_path)


def test_repo_loader_carries_an_empty_vendor_marker():
    text = (REPO / "deploy" / "onprem" / "vedha-onprem-load.sh").read_text()
    assert text.count('\nVEDHA_VENDOR_SPKI=""\n') == 1
