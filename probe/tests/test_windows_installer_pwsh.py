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
    an http:// manager without the explicit flag are all refused;
  * the real install path (https stub, a recording stand-in for the packaged installer.ps1 and
    for icacls.exe): the packaged installer gets the manager, token, scope and -NoPause; its
    exit code 3 ("installed, not connected yet") is a warning, any other non-zero a failure;
    the installer/uninstaller are kept under ProgramData\vedha-agent\tools, the verified
    manifest is kept, the staging folder is gone, and the token never reaches the output.
"""
from __future__ import annotations

import importlib.util
import json
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
TOKEN = "vet_localtoken1"


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
    out, _ = _against(release, "none", "-Token", "vet_wrongtoken1")
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


# ── the real install path ────────────────────────────────────────────────────

FAKE_PACKAGED_INSTALLER = """\
param([string]$Manager = '', [string]$Token = '', [string]$Scope = '', [switch]$NoPause, [string]$Unexpected = '')
$record = [ordered]@{ Manager = $Manager; TokenLength = $Token.Length; Scope = $Scope; NoPause = [bool]$NoPause }
Set-Content -LiteralPath (Join-Path $env:VEDHA_TEST_OUT 'inner-args.json') -Value ($record | ConvertTo-Json)
Write-Host 'fake packaged installer ran'
exit ([int]$env:VEDHA_TEST_INNER_EXIT)
"""


@pytest.fixture(scope="module")
def tls_files(tmp_path_factory):
    import datetime
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID
    d = tmp_path_factory.mktemp("tls")
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1")])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=2))
            .add_extension(x509.SubjectAlternativeName([x509.IPAddress(__import__("ipaddress").ip_address("127.0.0.1"))]), False)
            .sign(key, hashes.SHA256()))
    (d / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    (d / "key.pem").write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                  serialization.NoEncryption()))
    return d / "cert.pem", d / "key.pem"


@pytest.fixture(scope="module")
def release_with_fake_installer(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("psinstall")
    tool.keygen(tmp / "ed.pem")
    tool.keygen_p256(tmp / "p256.pem")
    win = tmp / "win.zip"
    with zipfile.ZipFile(win, "w") as zf:
        zf.writestr("vedha-agent/vedha-agent.exe", b"MZ fake exe")
        zf.writestr("install.ps1", FAKE_PACKAGED_INSTALLER)
        zf.writestr("install.cmd", "@echo off\r\n")
        zf.writestr("uninstall.ps1", "# uninstall\n")
        zf.writestr("uninstall.cmd", "@echo off\r\n")
        zf.writestr("README.txt", "readme")
    return tool.build_release(
        key_path=tmp / "ed.pem", out=tmp / "out", arches=["amd64"], version="3.4.5",
        builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(b"img" * 20),
        p256_key_path=tmp / "p256.pem", windows_zip=win,
    )


def _install(release, tls, tmp_path, *, inner_exit=0, scope=None, trust=None, replace=False):
    out_dir, programdata = tmp_path / "out", tmp_path / "ProgramData"
    out_dir.mkdir()
    programdata.mkdir()
    if trust is not None:             # a release key this computer pinned earlier (a dict, or raw text for a damaged file)
        trust_file = programdata / "vedha-agent" / "release" / "trust.json"
        trust_file.parent.mkdir(parents=True)
        trust_file.write_text(trust if isinstance(trust, str) else json.dumps(trust))
    httpd = stub.serve(release, TOKEN, tls=tls)
    try:
        env = {**os.environ, "DOTNET_SYSTEM_GLOBALIZATION_INVARIANT": "1", "VEDHA_TEST_OUT": str(out_dir),
               "VEDHA_TEST_INNER_EXIT": str(inner_exit), "ProgramData": str(programdata)}
        cmd = [PS, "-NoProfile", "-File", str(HARNESS), "-Installer", str(release / "install.ps1"),
               "-Port", str(httpd.server_address[1]), "-Install"]
        if scope:
            cmd += ["-Scope", scope]
        if replace:
            cmd += ["-ReplaceReleaseKey"]
        if PS.lower().endswith(("powershell", "powershell.exe")):
            cmd[1:1] = ["-ExecutionPolicy", "Bypass"]
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=180, env=env)
        return done.stdout + done.stderr, out_dir, programdata, list(httpd.requests)
    finally:
        httpd.shutdown()


def _can_install_here() -> bool:
    """Linux/macOS: Windows-only calls are replaced by recording stand-ins. Windows: the real icacls and
    administrator check run, so it needs an elevated session (CI runners are)."""
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


@pytest.mark.skipif(not _can_install_here(), reason="the install path needs an elevated Windows session")
class TestInstallPath:
    def test_the_packaged_installer_gets_the_right_arguments_and_the_install_is_tidy(self, release_with_fake_installer, tls_files, tmp_path):
        out, out_dir, programdata, requests = _install(release_with_fake_installer, tls_files, tmp_path, scope="10.9.0.0/24")
        assert "RESULT: PASS" in out and "INSTALLED-NOT-CONNECTED: False" in out, out
        record = json.loads((out_dir / "inner-args.json").read_text())
        assert record["Manager"].startswith("https://127.0.0.1:") and record["Scope"] == "10.9.0.0/24"
        assert record["NoPause"] is True and record["TokenLength"] == len(TOKEN)
        root = programdata / "vedha-agent"
        assert {p.name for p in (root / "tools").iterdir()} == {"install.ps1", "install.cmd", "uninstall.ps1", "uninstall.cmd"}
        assert (root / "release" / "manifest.json").read_bytes() == (release_with_fake_installer / "manifest.json").read_bytes()
        assert not (root / "staging").exists() or not list((root / "staging").iterdir())         # staging removed
        if sys.platform != "win32":          # the stand-in recorded the call; on Windows the real icacls ran
            icacls = (out_dir / "icacls.log").read_text()
            assert "/inheritance:r" in icacls and "*S-1-5-18" in icacls and "*S-1-5-32-544" in icacls   # locked first
        assert ("GET", "/agent/package/windows", 200) in requests

    def test_no_scope_means_none_is_passed_so_the_packaged_installer_auto_detects(self, release_with_fake_installer, tls_files, tmp_path):
        _, out_dir, _, _ = _install(release_with_fake_installer, tls_files, tmp_path)
        assert json.loads((out_dir / "inner-args.json").read_text())["Scope"] == ""

    def test_exit_3_means_installed_but_not_connected_yet_and_is_not_a_failure(self, release_with_fake_installer, tls_files, tmp_path):
        out, _, programdata, _ = _install(release_with_fake_installer, tls_files, tmp_path, inner_exit=3)
        assert "RESULT: PASS" in out and "INSTALLED-NOT-CONNECTED: True" in out, out
        assert "has not connected yet" in out
        assert (programdata / "vedha-agent" / "tools" / "uninstall.ps1").exists()      # still removable

    def test_exit_4_means_the_update_was_undone_and_says_so(self, release_with_fake_installer, tls_files, tmp_path):
        out, _, programdata, _ = _install(release_with_fake_installer, tls_files, tmp_path, inner_exit=4)
        assert "RESULT: FAIL" in out and "previous version was put back" in out, out
        assert not (programdata / "vedha-agent" / "release" / "trust.json").exists()      # nothing is pinned for a failed install

    @pytest.mark.parametrize("code", [1, 2, 7])
    def test_any_other_exit_code_is_a_failure_and_leaves_no_staging(self, release_with_fake_installer, tls_files, tmp_path, code):
        out, _, programdata, _ = _install(release_with_fake_installer, tls_files, tmp_path, inner_exit=code)
        assert "RESULT: FAIL" in out and f"exit code {code}" in out, out
        assert not (programdata / "vedha-agent" / "tools").exists()
        staging = programdata / "vedha-agent" / "staging"
        assert not staging.exists() or not list(staging.iterdir())

    def test_the_token_never_appears_in_the_output(self, release_with_fake_installer, tls_files, tmp_path):
        out, _, _, _ = _install(release_with_fake_installer, tls_files, tmp_path)
        assert "RESULT: PASS" in out, out                # the install really ran
        assert TOKEN not in out

    def test_an_http_manager_cannot_install(self, release_with_fake_installer, tmp_path):
        """The Windows agent needs https: plain http only works with -VerifyOnly against a test server."""
        httpd = stub.serve(release_with_fake_installer, TOKEN)
        try:
            env = {**os.environ, "DOTNET_SYSTEM_GLOBALIZATION_INVARIANT": "1", "ProgramData": str(tmp_path)}
            cmd = [PS, "-NoProfile", "-File", str(HARNESS), "-Installer", str(release_with_fake_installer / "install.ps1"),
                   "-Port", str(httpd.server_address[1]), "-Install"]
            # -Install builds an https:// address; point it at the plain-http stub to prove the TLS handshake is required
            done = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
            assert "RESULT: FAIL" in done.stdout, done.stdout + done.stderr
        finally:
            httpd.shutdown()


@pytest.mark.skipif(not _can_install_here(), reason="the install path needs an elevated Windows session")
class TestPinnedReleaseKey:
    """The release key is pinned on the first good install and then protects every later one."""

    def _release_key(self, release) -> str:
        import re
        return re.search(r"VedhaReleaseP256Spki = '([^']+)'", (release / "install.ps1").read_text()).group(1)

    def test_a_good_install_pins_the_key_and_the_release(self, release_with_fake_installer, tls_files, tmp_path):
        out, _, programdata, _ = _install(release_with_fake_installer, tls_files, tmp_path)
        assert "RESULT: PASS" in out and "release key pinned" in out, out
        trust = json.loads((programdata / "vedha-agent" / "release" / "trust.json").read_text())
        assert trust["p256_spki"] == self._release_key(release_with_fake_installer)
        assert trust["key_id"] == json.loads((release_with_fake_installer / "manifest.json").read_text())["p256_key_id"]
        assert trust["release_version"] == "3.4.5" and trust["manager"].startswith("https://127.0.0.1:")

    def test_the_same_key_installs_again(self, release_with_fake_installer, tls_files, tmp_path):
        key = self._release_key(release_with_fake_installer)
        out, _, _, _ = _install(release_with_fake_installer, tls_files, tmp_path,
                                trust={"schema": 1, "p256_spki": key, "release_version": "3.4.4"})
        assert "RESULT: PASS" in out, out

    def test_a_different_key_is_refused_before_anything_is_downloaded(self, release_with_fake_installer, tls_files, tmp_path):
        other = tool.p256_spki_b64(tool.load_p256_private_key(_other_p256(tmp_path)))
        out, _, programdata, requests = _install(release_with_fake_installer, tls_files, tmp_path,
                                                 trust={"schema": 1, "p256_spki": other, "release_version": "3.4.4"})
        assert "RESULT: FAIL" in out and "trusts Vedha release key" in out and "do not install" in out, out
        assert not [r for r in requests if r[1].startswith("/agent/package")], requests      # no token was ever sent
        assert not [r for r in requests if "manifest" in r[1]], requests
        kept = json.loads((programdata / "vedha-agent" / "release" / "trust.json").read_text())
        assert kept["p256_spki"] == other                                                       # the pin was not overwritten

    def test_replace_release_key_is_the_explicit_way_to_rotate(self, release_with_fake_installer, tls_files, tmp_path):
        other = tool.p256_spki_b64(tool.load_p256_private_key(_other_p256(tmp_path)))
        out, _, programdata, _ = _install(release_with_fake_installer, tls_files, tmp_path, replace=True,
                                          trust={"schema": 1, "p256_spki": other, "release_version": "3.4.4"})
        assert "RESULT: PASS" in out and "replacing the pinned release key" in out, out
        kept = json.loads((programdata / "vedha-agent" / "release" / "trust.json").read_text())
        assert kept["p256_spki"] == self._release_key(release_with_fake_installer)

    def test_an_older_release_than_the_installed_one_is_refused(self, release_with_fake_installer, tls_files, tmp_path):
        key = self._release_key(release_with_fake_installer)
        out, _, _, requests = _install(release_with_fake_installer, tls_files, tmp_path,
                                       trust={"schema": 1, "p256_spki": key, "release_version": "9.0.0"})
        assert "RESULT: FAIL" in out and "older release" in out.lower() and "already installed" in out, out
        assert not [r for r in requests if r[1].startswith("/agent/package")]

    def test_replace_release_key_does_not_allow_an_older_release(self, release_with_fake_installer, tls_files, tmp_path):
        key = self._release_key(release_with_fake_installer)
        out, _, _, _ = _install(release_with_fake_installer, tls_files, tmp_path, replace=True,
                                trust={"schema": 1, "p256_spki": key, "release_version": "9.0.0"})
        assert "RESULT: FAIL" in out and "already installed" in out, out

    def test_a_damaged_pin_file_stops_the_install_instead_of_switching_protection_off(self, release_with_fake_installer, tls_files, tmp_path):
        out, _, _, requests = _install(release_with_fake_installer, tls_files, tmp_path, trust="{not json")
        assert "RESULT: FAIL" in out and "cannot be read" in out, out
        assert not [r for r in requests if r[1].startswith("/agent/package")]


def _other_p256(tmp_path) -> Path:
    path = tmp_path / "other-p256.pem"
    tool.keygen_p256(path)
    return path
