"""
test_agent_stub_manager.py — the CI fixture that stands in for the manager when the
Windows installer is run end to end (scripts/ci/agent_stub_manager.py).

The PowerShell installer is proven on a real Windows runner (agent-release.yml). This
file proves the FIXTURE: that it serves what the manager serves, and that each tamper
mode really produces a release a correct client must refuse. The client below is a
Python transcription of install-remote.ps1's checks, in the same order.
"""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import urllib.error
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tool = _load("agent_release_tool", "scripts/agent_release.py")
stub = _load("agent_stub_manager", "scripts/ci/agent_stub_manager.py")

TOKEN = "vet_ci_test_token"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_opener = urllib.request.build_opener(NoRedirect)


def _get(base, path, token=None):
    req = urllib.request.Request(base + path)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with _opener.open(req, timeout=10) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


@pytest.fixture(scope="module")
def release(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("rel")
    ed, p256 = tmp / "ed.pem", tmp / "p256.pem"
    tool.keygen(ed)
    spki = tool.keygen_p256(p256)
    win = tmp / "win.zip"
    win.write_bytes(b"PK\x03\x04 pretend zip " * 500)
    ps = tmp / "install-remote.ps1"
    ps.write_bytes(b"$script:VedhaReleaseP256Spki = ''\n$script:VedhaReleaseVersion = ''\n")
    cmd = tmp / "install-remote.cmd"
    cmd.write_bytes(b"@echo off\r\n")
    final = tool.build_release(
        key_path=ed, out=tmp / "out", arches=["amd64"], version="7.7.7",
        builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(b"img" * 50),
        p256_key_path=p256, windows_zip=win,
        windows_installer_source=ps, windows_launcher_source=cmd,
    )
    return final, spki


def _client(base, spki, token=TOKEN):
    """install-remote.ps1's checks, in its order. Returns the verified package bytes or raises."""
    status, manifest = _get(base, "/agent/manifest.json")
    assert status == 200
    status, sig = _get(base, "/agent/manifest.json.p256.sig")
    assert status == 200
    try:
        tool.verify_manifest_p256(spki, sig.decode(), manifest)
    except Exception as exc:
        raise AssertionError("signature") from exc
    entry = next(p for p in json.loads(manifest)["packages"] if p["os"] == "windows" and p["cpu"] == "amd64")
    status, body = _get(base, "/agent/package/windows", token)
    if status != 200:
        raise AssertionError(f"http {status}")
    if len(body) != entry["size"]:
        raise AssertionError("size")
    if hashlib.sha256(body).hexdigest() != entry["sha256"]:
        raise AssertionError("sha256")
    return body


def _serve(release_dir, tamper="none"):
    httpd = stub.serve(release_dir, TOKEN, tamper=tamper)
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}"


def test_honest_release_passes_the_client_checks(release):
    final, spki = release
    httpd, base = _serve(final)
    try:
        assert _client(base, spki) == (final / "vedha-agent-7.7.7-windows-amd64.zip").read_bytes()
    finally:
        httpd.shutdown()


def test_stub_serves_the_files_the_manager_serves(release):
    final, _ = release
    httpd, base = _serve(final)
    try:
        for path, name in (("/agent/install.ps1", "install.ps1"), ("/agent/install.cmd", "install.cmd"),
                           ("/agent/manifest.json", "manifest.json"),
                           ("/agent/manifest.json.sig", "manifest.json.sig"),
                           ("/agent/manifest.json.p256.sig", "manifest.json.p256.sig")):
            status, body = _get(base, path)
            assert status == 200 and body == (final / name).read_bytes(), path
        assert _get(base, "/agent/nope")[0] == 404
    finally:
        httpd.shutdown()


@pytest.mark.parametrize("token", [None, "", "not-a-vet-token", "vet_some_other_token"])
def test_package_needs_the_right_token_and_says_why(release, token):
    final, _ = release
    httpd, base = _serve(final)
    try:
        status, body = _get(base, "/agent/package/windows", token)
        assert status == 401 and "detail" in json.loads(body)
    finally:
        httpd.shutdown()


@pytest.mark.parametrize("mode,why", [
    ("manifest", "signature"), ("signature", "signature"),
    ("package", "sha256"), ("truncated", "size"), ("oversize", "size"), ("redirect", "http 302"),
])
def test_every_tamper_mode_is_caught_by_a_correct_client(release, mode, why):
    final, spki = release
    httpd, base = _serve(final, mode)
    try:
        with pytest.raises(AssertionError, match=why):
            _client(base, spki)
    finally:
        httpd.shutdown()


def test_a_tampered_manifest_never_reaches_the_package_download(release):
    """Signature failure must stop the client BEFORE it sends the token anywhere."""
    final, spki = release
    httpd, base = _serve(final, "manifest")
    try:
        with pytest.raises(AssertionError, match="signature"):
            _client(base, spki)
        assert not any(path == "/agent/package/windows" for _, path, _ in httpd.requests)
    finally:
        httpd.shutdown()


def test_unknown_tamper_mode_is_rejected(release):
    with pytest.raises(ValueError):
        stub.serve(release[0], TOKEN, tamper="melt")
