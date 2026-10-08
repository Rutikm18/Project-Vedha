"""
test_windows_installer_pwsh.py — runs the REAL release-stamped Windows installer in PowerShell.

Skipped where no PowerShell exists. GitHub's Linux runners ship `pwsh` and the Windows job
has both Windows PowerShell 5.1 and pwsh, so CI runs this everywhere that matters; on Windows
the installer's own CNG signature check executes, elsewhere a managed ECDSA stands in for it
(see pwsh/installer_harness.ps1).

What it proves, against a stub manager (scripts/ci/agent_stub_manager.py) serving a
throwaway-keyed release:
  * an honest release verifies end to end (-VerifyOnly: manifest signature, token download,
    size, SHA-256, safe unpack, layout);
  * every tamper mode — manifest, signature, package, truncated, oversize, redirect — is
    REFUSED with the right reason, and a signature failure sends no token anywhere;
  * the zip unpacker refuses traversal, absolute, drive, alternate-stream and backslash paths;
  * a wrong or malformed token, an installer from another release, an unstamped installer and
    an http:// manager without the explicit flag are all refused.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HARNESS = Path(__file__).resolve().parent / "pwsh" / "installer_harness.ps1"


def _powershell() -> str | None:
    if sys.platform == "win32":
        return shutil.which("powershell") or shutil.which("pwsh")
    return shutil.which("pwsh")


PS = _powershell()
pytestmark = pytest.mark.skipif(PS is None, reason="no PowerShell on this machine")


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tool = _load("agent_release_tool", "scripts/agent_release.py")
stub = _load("agent_stub_manager", "scripts/ci/agent_stub_manager.py")
TOKEN = "vet_local"


@pytest.fixture(scope="module")
def release(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("psrel")
    tool.keygen(tmp / "ed.pem")
    tool.keygen_p256(tmp / "p256.pem")
    win = tmp / "win.zip"
    with zipfile.ZipFile(win, "w") as zf:                 # forward slashes, as a spec-compliant zip
        zf.writestr("vedha-agent/vedha-agent.exe", b"MZ fake exe")
        zf.writestr("vedha-agent/lib/x.dll", b"dll")
        zf.writestr("install.ps1", "# packaged installer\n")
        zf.writestr("uninstall.ps1", "# packaged uninstaller\n")
    return tool.build_release(
        key_path=tmp / "ed.pem", out=tmp / "out", arches=["amd64"], version="1.2.3",
        builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(b"img" * 20),
        p256_key_path=tmp / "p256.pem", windows_zip=win,
    )


def _run(installer: Path, port: int = 0, *extra: str):
    env = {**os.environ, "DOTNET_SYSTEM_GLOBALIZATION_INVARIANT": "1"}
    cmd = [PS, "-NoProfile", "-File", str(HARNESS), "-Installer", str(installer), "-Port", str(port), *extra]
    if PS.lower().endswith("powershell") or PS.lower().endswith("powershell.exe"):
        cmd[1:1] = ["-ExecutionPolicy", "Bypass"]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=180, env=env)
    return done.stdout + done.stderr


def _against(release_dir: Path, tamper: str = "none", *extra: str, installer: Path | None = None):
    httpd = stub.serve(release_dir, TOKEN, tamper=tamper)
    try:
        out = _run(installer or release_dir / "install.ps1", httpd.server_address[1], *extra)
        return out, list(httpd.requests)
    finally:
        httpd.shutdown()


def test_honest_release_verifies_end_to_end(release):
    out, requests = _against(release)
    assert "RESULT: PASS" in out, out
    assert "manifest signature OK" in out and "SHA-256 matches the signed manifest" in out
    assert "VERIFY-ONLY OK" in out and "nothing was installed" in out
    assert ("GET", "/agent/package/windows", 200) in requests


@pytest.mark.parametrize("mode,message", [
    ("manifest", "manifest signature does not verify"),
    ("signature", "manifest signature does not verify"),
    ("package", "does not match the signed manifest"),
    ("truncated", "signed manifest says"),
    ("oversize", "larger than the signed manifest"),
    ("redirect", "Redirects are refused"),
])
def test_every_tamper_mode_is_refused_for_the_right_reason(release, mode, message):
    out, _ = _against(release, mode)
    assert "RESULT: FAIL" in out and message in out, out


def test_a_bad_signature_sends_the_token_nowhere(release):
    for mode in ("manifest", "signature"):
        _, requests = _against(release, mode)
        assert not any(path == "/agent/package/windows" for _, path, _ in requests), mode


def test_wrong_token_is_reported_as_such(release):
    out, _ = _against(release, "none", "-Token", "vet_wrong")
    assert "RESULT: FAIL" in out and "install token was refused" in out, out


def test_malformed_token_is_refused_before_any_request(release):
    out, requests = _against(release, "none", "-Token", "nope")
    assert "install token is malformed" in out, out
    assert requests == []


def test_http_manager_needs_the_explicit_flag(release):
    out, requests = _against(release, "none", "-NoAllowHttp")
    assert "Refusing an http:// manager" in out, out
    assert requests == []


def test_an_installer_from_another_release_is_refused(release, tmp_path):
    stale = tmp_path / "install.ps1"
    stale.write_bytes((release / "install.ps1").read_bytes().replace(b"VedhaReleaseVersion = '1.2.3'",
                                                                    b"VedhaReleaseVersion = '9.9.9'"))
    out, _ = _against(release, "none", installer=stale)
    assert "belongs to '9.9.9'" in out, out


def test_an_unstamped_installer_cannot_verify_anything(release, tmp_path):
    import re
    unstamped = tmp_path / "install.ps1"
    text = (release / "install.ps1").read_text(encoding="ascii")
    unstamped.write_bytes(re.sub(r"(VedhaReleaseP256Spki = ')[^']*'", r"\1'", text).encode("ascii"))
    out, requests = _against(release, "none", installer=unstamped)
    assert "was not stamped by a release build" in out, out
    assert requests == []


def test_zip_unpacker_refuses_hostile_paths(tmp_path):
    zips = tmp_path / "zips"
    zips.mkdir()
    hostile = {"dotdot": "../evil.txt", "nested": "a/../../evil.txt", "absolute": "/abs.txt",
               "drive": "C:/x.txt", "stream": "a.txt:stream", "backslash": "..\\evil.txt"}
    for case, name in {**hostile, "good": "ok/file.txt", "deep": "d1/d2/f.bin"}.items():
        with zipfile.ZipFile(zips / f"{case}.zip", "w") as zf:
            zf.writestr(name, b"x")
    # any stamped installer will do: the unpacker does not depend on the release
    keys = tmp_path / "k"
    keys.mkdir()
    tool.keygen(keys / "ed.pem")
    tool.keygen_p256(keys / "p.pem")
    win = tmp_path / "w.zip"
    win.write_bytes(b"PK")
    rel = tool.build_release(key_path=keys / "ed.pem", out=tmp_path / "o", arches=["amd64"], version="0.0.1",
                             builder=lambda *a: None, saver=lambda t, d: d.write_bytes(b"i"),
                             p256_key_path=keys / "p.pem", windows_zip=win)
    out = _run(rel / "install.ps1", 1, "-ZipDir", str(zips))
    for case in hostile:
        line = next((l for l in out.splitlines() if l.startswith(f"ZIP {case} ")), "")
        assert "REFUSED" in line and "escaped=False" in line, (case, out)
    for case in ("good", "deep"):
        line = next((l for l in out.splitlines() if l.startswith(f"ZIP {case} ")), "")
        assert "EXTRACTED" in line, (case, out)
