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
    # The only child process is the elevated copy of this same installer, started in one place.
    assert len(re.findall(r"Start-Process", code)) == 1
    elevate = _body(code, "Enter-VedhaElevation")
    assert "Start-Process" in elevate and "-Verb RunAs" in elevate and "-Wait" in elevate
    # The elevated copy's command never contains the token: it reads it from the environment,
    # which is set just before and removed right after (even when starting it fails).
    command = _body(code, "Get-VedhaElevationCommand")
    assert "$InstallToken" not in command and "$Token" not in command
    assert "$env:VEDHA_INSTALL_TOKEN" in command
    assert elevate.index("$env:VEDHA_INSTALL_TOKEN = $Token") < elevate.index("Start-Process")
    assert "finally" in elevate and "Remove-Item Env:" in elevate
    # the token reaches the packaged installer as a parameter of an in-process call
    assert "Token = $Token" in code and "& $inner @innerArgs" in code


def test_elevation_is_attempted_once_only_when_needed_and_never_loops():
    code = re.sub(r"<#.*?#>", "", _text("install-remote.ps1"), flags=re.S)
    elevate = _body(code, "Enter-VedhaElevation")
    assert "if ($VerifyOnly -or (Test-VedhaAdmin)) { return $false }" in elevate      # no prompt for -VerifyOnly or an admin
    assert elevate.index("return $false") < elevate.index("if ($Elevated)") < elevate.index("Start-Process")
    assert "-Elevated" in _body(code, "Get-VedhaElevationCommand")                     # the copy refuses to elevate again
    main = _body(code, "Install-VedhaAgent")
    order = ["Assert-CleanToken", "Assert-CleanScope", "Enter-VedhaElevation", "Assert-Environment", "Get-VerifiedPackage"]
    positions = [main.index(step) for step in order]
    assert positions == sorted(positions), dict(zip(order, positions))               # validate first, then elevate, then do the work
    assert "Assert-Environment" in code and "IsInRole" in _body(code, "Test-VedhaAdmin")
    # an elevated copy that still lacks the token explains why
    assert "did not reach the Administrator window" in _body(code, "Assert-CleanToken")


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


# ── the contract between install-remote.ps1 and the packaged installer (install.ps1) ──────────

def test_the_packaged_installer_accepts_every_argument_install_remote_passes():
    inner = _text("install.ps1")
    start = inner.index("param(")
    params = inner[start:inner.index("\n)", start)]
    for name in ("Manager", "Token", "Scope", "NoPause"):
        assert re.search(rf"\${name}\b", params), name
    remote = re.sub(r"<#.*?#>", "", _text("install-remote.ps1"), flags=re.S)
    assert "Manager = $managerUrl" in remote and "NoPause = $true" in remote and "innerArgs.Scope = $Scope" in remote


def test_install_remote_understands_the_packaged_installers_exit_codes():
    """install.ps1: 0 = connected / waiting for approval, 3 = installed but not connected yet."""
    inner = _text("install.ps1")
    assert "return 3" in inner and "return 0" in inner
    remote = _text("install-remote.ps1")
    assert "$innerExit -ne 0 -and $innerExit -ne 3" in remote
    assert "InstalledNotConnected" in remote and "exit 3" in remote


def test_the_packaged_installer_keeps_the_token_out_of_the_task_and_removes_it_after_use():
    inner = _text("install.ps1")
    assert "Remove-VedhaTokenLine" in inner                          # the token line leaves agent.env once online
    assert "Set-VedhaAcl" in inner and "*S-1-5-18" in inner          # data folder: SYSTEM and Administrators only
    task = inner[inner.index("function Register-VedhaTask"):inner.index("# The installer\n")]
    assert "Token" not in task                                       # never in the Scheduled Task definition


def test_the_installer_and_uninstaller_are_kept_with_the_install():
    remote = _text("install-remote.ps1")
    assert "'install.ps1', 'install.cmd', 'uninstall.ps1', 'uninstall.cmd'" in remote
    assert "Join-Path $root 'tools'" in remote
    # and those are the files the packaged uninstall path needs
    assert "-Uninstall" in _text("uninstall.ps1") and "-Uninstall" in _text("uninstall.cmd")


def test_the_windows_agent_needs_an_https_manager_everywhere():
    assert "^https://" in _text("install.ps1")                       # the packaged installer's rule
    remote = _text("install-remote.ps1")
    assert "The Windows agent needs an https:// manager address" in remote
    assert "-AllowInsecureHttp" not in _text("install-remote.cmd")


def test_package_zip_release_switch_skips_baking_a_manager():
    text = _text("package-zip.ps1")
    assert "ParameterSetName = 'Release'" in text and "[switch]$Release" in text
    assert re.search(r"Mandatory\s*=\s*\$true,\s*ParameterSetName\s*=\s*'Customer'\)\]\[string\]\$Manager", text)
    release_branch = text[text.index("if ($Release) {\n  # The manager placeholder stays"):]
    assert "__VEDHA_MANAGER_URL__" not in release_branch.split("} else {")[0]          # not replaced for a release


def test_token_shape_is_checked_before_anything_is_downloaded():
    assert r"^vet_[A-Za-z0-9_\-]{8,}$" in _text("install-remote.ps1")
    assert r"^vet_[A-Za-z0-9_\-]{8,}$" in _text("install-remote.cmd")


@pytest.mark.skipif(shutil.which("pwsh") is None, reason="no PowerShell on this machine")
@pytest.mark.parametrize("scope, expect_scope", [("", False), ("10.0.0.0/24", True)])
def test_the_elevated_copys_command_has_no_token_and_works_from_any_window(scope, expect_scope):
    code = re.sub(r"<#.*?#>", "", _text("install-remote.ps1"), flags=re.S)
    func = _body(code, "Get-VedhaElevationCommand")
    out = subprocess.run(
        ["pwsh", "-NoProfile", "-Command",
         f"{func}\nGet-VedhaElevationCommand -ManagerUrl 'https://api.vedhasec.com' -InstallScope '{scope}'"],
        capture_output=True, text=True, timeout=60, check=True).stdout.strip()
    assert out.startswith("[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ")
    assert "irm 'https://api.vedhasec.com/agent/install.ps1'" in out
    assert "-Manager 'https://api.vedhasec.com'" in out
    assert "-Token $env:VEDHA_INSTALL_TOKEN" in out and "vet_" not in out
    assert out.endswith("-PauseAtEnd -Elevated")
    assert ("-Scope '10.0.0.0/24'" in out) is expect_scope
    assert '"' not in out                                  # it is wrapped in double quotes when started
