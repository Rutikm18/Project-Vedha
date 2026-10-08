"""
test_windows_remote_install.py — static contract for the one-command Windows installer.

PowerShell cannot be run on the Linux test machines, so what these tests pin is
everything a text check CAN prove: the files build into a release, stay ASCII (Windows
PowerShell 5.1 reads a BOM-less file in the ANSI code page), keep their security-relevant
shape (verify before download-install, no redirects on a token-bearing request, the token
never in the service wrapper) and use the exact constants the Python side signs with. The
behaviour itself is proven on a real Windows runner by .github/workflows/agent-release.yml
(`install.ps1 -VerifyOnly` against a throwaway-signed release).
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
WIN = REPO / "probe" / "windows"

_spec = importlib.util.spec_from_file_location("agent_release_tool", REPO / "scripts" / "agent_release.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)

REMOTE_PS1 = WIN / "install-remote.ps1"
REMOTE_CMD = WIN / "install-remote.cmd"
SHIPPED = ["install-remote.ps1", "install-remote.cmd", "install.ps1", "install.cmd",
           "uninstall.ps1", "uninstall.cmd", "package-zip.ps1", "run.cmd"]


def _text(name: str) -> str:
    return (WIN / name).read_bytes().decode("ascii")      # fails on any non-ASCII byte


@pytest.mark.parametrize("name", SHIPPED)
def test_shipped_windows_scripts_are_ascii(name):
    _text(name)


def test_remote_installer_has_exactly_one_of_each_release_marker():
    text = _text("install-remote.ps1")
    assert len(tool.P256_MARKER.findall(text)) == 1
    assert len(tool.WIN_VERSION_MARKER.findall(text)) == 1


def test_remote_installer_builds_into_a_release(tmp_path):
    out = tmp_path / "installer.ps1"
    tool.embed_windows_installer(REMOTE_PS1, out, p256_spki="QUJD" * 10, version="9.9.9")
    stamped = out.read_bytes().decode("ascii")
    assert "$script:VedhaReleaseP256Spki = 'QUJDQUJDQUJDQUJDQUJDQUJDQUJDQUJDQUJDQUJD'" in stamped
    assert "$script:VedhaReleaseVersion = '9.9.9'" in stamped
    assert "\r\n" in stamped and "\n" not in stamped.replace("\r\n", "")      # written CRLF


def test_default_release_sources_exist():
    assert tool.WIN_INSTALLER == REMOTE_PS1 and REMOTE_PS1.is_file()
    assert tool.WIN_LAUNCHER == REMOTE_CMD and REMOTE_CMD.is_file()


# ── install-remote.ps1: the security-relevant shape ─────────────────────────

def _body(text: str, func: str) -> str:
    """Source of one top-level function (up to the next top-level `function`/section)."""
    m = re.search(rf"^function {re.escape(func)}\b.*?(?=^function |^# --- |^\$failed)", text, re.S | re.M)
    assert m, func
    return m.group(0)


def test_verification_happens_before_download_and_install():
    main = _body(_text("install-remote.ps1"), "Install-VedhaAgent")
    order = ["Get-VerifiedPackage", "Save-File", "Get-Sha256Hex", "Expand-SafeZip",
             "Assert-Authenticode", "& $inner"]
    positions = [main.index(step) for step in order]
    assert positions == sorted(positions), dict(zip(order, positions))


def test_signature_failure_aborts_before_any_download():
    verified = _body(_text("install-remote.ps1"), "Get-VerifiedPackage")
    assert "Test-P256Signature" in verified
    assert verified.index("Test-P256Signature") < verified.index("ConvertFrom-Json")
    assert "Nothing was downloaded or installed" in verified
    assert "Save-File" not in verified              # the package is only fetched after this returns


def test_token_bearing_requests_never_follow_redirects():
    opener = _body(_text("install-remote.ps1"), "Open-Response")
    assert "AllowAutoRedirect = $false" in opener
    assert "Authorization" in opener and "Bearer" in opener


@pytest.mark.parametrize("forbidden", [
    "Invoke-Expression", "iex ", "ServerCertificateValidationCallback", "-SkipCertificateCheck",
    "Set-ExecutionPolicy", "DownloadString", "Invoke-WebRequest", "Invoke-RestMethod",
])
def test_remote_installer_avoids_unsafe_constructs(forbidden):
    code = re.sub(r"<#.*?#>", "", _text("install-remote.ps1"), flags=re.S)     # ignore the help comment
    assert forbidden not in code


def test_remote_installer_never_puts_the_token_on_a_child_command_line():
    code = re.sub(r"<#.*?#>", "", _text("install-remote.ps1"), flags=re.S)
    assert not re.search(r"Start-Process|&\s*['\"]?powershell|powershell(\.exe)?\s+-", code, re.I)
    # the token reaches the packaged installer as a parameter of an in-process call
    assert "& $inner -Manager $managerUrl -Scope $Scope -Token $Token" in code


def test_zip_extraction_rejects_traversal_and_streams():
    expand = _body(_text("install-remote.ps1"), "Expand-SafeZip")
    for needle in (r"\.\.", "Contains(':')", "StartsWith($root", "MaxUnpackedBytes", "MaxEntries"):
        assert needle in expand, needle


def test_https_is_required_unless_explicitly_waived():
    cleaned = _body(_text("install-remote.ps1"), "Get-CleanManager")
    assert "AllowInsecureHttp" in cleaned and "Refusing an http://" in cleaned


def test_release_version_is_pinned_to_the_signed_manifest():
    verified = _body(_text("install-remote.ps1"), "Get-VerifiedPackage")
    assert "$script:VedhaReleaseVersion" in verified


# ── the constants must match what the Python side signs with ────────────────

def test_cng_constants_match_the_release_tool(tmp_path):
    """The installer slices the SPKI the release tool actually produces: pin its
    constants against a freshly generated key rather than trusting the two to agree."""
    import base64
    code = _text("install-remote.ps1")
    spki = base64.b64decode(tool.keygen_p256(tmp_path / "p256.pem"))
    assert len(spki) == 91 and spki[26] == 4
    assert spki[:26].hex() in code                  # the prefix the script insists on
    assert "[Array]::Copy($spki, 27, $blob, 8, 64)" in code      # X || Y, straight after 0x04
    assert "0x31534345" in code                     # BCRYPT_ECDSA_PUBLIC_P256_MAGIC, 'ECS1'
    assert bytes.fromhex("45435331").decode() == "ECS1"
    assert "New-Object byte[] 72" in code           # 8-byte header + X + Y
    assert "-ne 91" in code and "-ne 64" in code    # SPKI length, signature length


# ── packaged install.ps1: the token handling ─────────────────────────────────

def _wrapper_here_string(text: str) -> str:
    m = re.search(r'@"\r?\n(.*?)\r?\n"@', text, re.S)
    assert m
    return m.group(1)


def test_service_wrapper_never_embeds_the_token():
    wrapper = _wrapper_here_string(_text("install.ps1"))
    assert "$Token" not in wrapper
    assert "set /p PROBE_ENROLL_TOKEN=<" in wrapper                 # read from the locked file
    assert "vet_" not in wrapper


def test_token_is_removed_once_the_agent_has_enrolled():
    text = _text("install.ps1")
    wrapper = _wrapper_here_string(text)
    assert "device_refresh_secret" in wrapper and "del /q" in wrapper
    assert "Remove-Item $tokenFile" in text


def test_install_folder_is_locked_to_system_and_administrators():
    text = _text("install.ps1")
    assert "*S-1-5-18:(OI)(CI)F" in text and "*S-1-5-32-544:(OI)(CI)F" in text
    assert "/inheritance:r" in text
    assert text.index("icacls.exe") < text.index("Set-Content -Path $tokenFile")      # locked before a token is written


def test_token_format_is_validated_in_both_scripts():
    for name in ("install.ps1", "install-remote.ps1"):
        assert r"^vet_[A-Za-z0-9_\-]+$" in _text(name)


def test_package_zip_release_switch_skips_baking_a_manager():
    text = _text("package-zip.ps1")
    assert "ParameterSetName = 'Release'" in text and "[switch]$Release" in text
    assert "if ($Manager)" in text          # the placeholder is only replaced when a manager was given


# ── install-remote.cmd ───────────────────────────────────────────────────────

def test_launcher_never_splices_arguments_into_a_powershell_command():
    for line in _text("install-remote.cmd").splitlines():
        if line.lstrip().lower().startswith("powershell"):
            assert not re.search(r"%~?[0-9]", line), line
            assert "%VEDHA_" not in line, line


def test_launcher_checks_values_then_elevation_then_installs():
    text = _text("install-remote.cmd")
    assert text.index("-notmatch") < text.index("fltmc >nul") < text.index("irm (")
    assert "https://" in text and "^https://" in text          # the launcher is https-only
    assert "-ExecutionPolicy Bypass" in text                   # process-local, set by the user's own command


# ── a real PowerShell parse, when one is installed ───────────────────────────

@pytest.mark.skipif(not (shutil.which("pwsh") or shutil.which("powershell")), reason="no PowerShell on this machine")
@pytest.mark.parametrize("name", [n for n in SHIPPED if n.endswith(".ps1")])
def test_scripts_parse_in_powershell(name):
    exe = shutil.which("pwsh") or shutil.which("powershell")
    script = (
        "$e = $null; $t = $null; "
        f"[void][System.Management.Automation.Language.Parser]::ParseFile('{WIN / name}', [ref]$t, [ref]$e); "
        "if ($e -and $e.Count) { $e | ForEach-Object { Write-Output $_.Message }; exit 1 }"
    )
    result = subprocess.run([exe, "-NoProfile", "-Command", script], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_uninstaller_is_kept_with_the_install():
    text = _text("install.ps1")
    assert "'uninstall.ps1', 'uninstall.cmd'" in text and "Copy-Item $source (Join-Path $installDir $name)" in text
    assert "uninstall.ps1" in _text("package-zip.ps1")          # and the package carries it
