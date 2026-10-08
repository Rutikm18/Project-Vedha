"""Windows scripts must not hard-code a manager address or weaken Defender by default.

The legacy Windows scripts defaulted to an old test IP over plain HTTP, and
setup.ps1 excluded python.exe from Defender machine-wide. Customers get the
manager address from Fleet; these tests keep the old defaults from creeping back.
"""
from __future__ import annotations

import re
from pathlib import Path

WIN = Path(__file__).resolve().parent.parent / "windows"
PLACEHOLDER = "__VEDHA_MANAGER_URL__"


def _text(name: str) -> str:
    return (WIN / name).read_text(encoding="utf-8")


def test_no_hardcoded_old_manager_ip_anywhere_in_windows_scripts():
    offenders = [p.name for p in WIN.iterdir()
                 if p.is_file() and "13.127.147.205" in p.read_text(encoding="utf-8", errors="ignore")]
    assert offenders == []


def test_no_plain_http_default_manager_in_windows_scripts():
    for name in ("run.cmd", "install.ps1", "package-zip.ps1", "setup.ps1", "probe.env.template"):
        assert not re.search(r"PLATFORM_URL\s*=\s*http://\d", _text(name)), name
        assert not re.search(r"\$Manager\s*=\s*'http://", _text(name)), name


def test_launchers_carry_the_placeholder_the_packager_replaces():
    assert PLACEHOLDER in _text("run.cmd")
    assert PLACEHOLDER in _text("install.ps1")
    assert PLACEHOLDER in _text("package-zip.ps1")      # the -replace target
    assert re.search(r"Mandatory\s*=\s*\$true\)\]\[string\]\$Manager", _text("package-zip.ps1"))


def test_launchers_refuse_to_run_unconfigured():
    assert "__" in _text("run.cmd") and "exit /b 1" in _text("run.cmd")
    assert "-like '__*'" in _text("install.ps1")


def test_setup_ps1_is_labelled_lab_only_and_defender_exclusion_is_opt_in():
    text = _text("setup.ps1")
    assert "NOT FOR CUSTOMER SITES" in text
    assert "[switch]$DefenderExcludePython" in text
    # the process-wide exclusion only appears inside the opt-in branch
    idx = text.index("-ExclusionProcess 'python.exe'")
    assert "if ($DefenderExcludePython)" in text[:idx]


# ── compiled Windows build: closure-only, folder layout, licence setting ─────

def test_build_script_compiles_only_the_closure_and_checks_the_output():
    text = _text("build-agent-exe.ps1")
    assert "tools\\agent_closure.py --check" in text and "--export" in text
    assert "--standalone" in text and "--onefile" not in text       # folder build
    assert "no_docstrings" in text and "no_asserts" in text
    assert "--nofollow-import-to=paramiko" in text and "--nofollow-import-to=winrm" in text
    assert "runtime-check" in text                                   # compiled binary self-check
    assert "pyinstaller" not in text.lower()                         # decompilable; removed


def test_build_script_fails_when_source_or_bytecode_would_ship():
    text = _text("build-agent-exe.ps1")
    assert "*.py, *.pyc" in text and "main_scripts" in text
    assert "build output contains Python source or bytecode" in text


def test_launchers_use_the_folder_layout_and_turn_the_unsealed_licence_off():
    assert "vedha-agent\\vedha-agent.exe" in _text("run.cmd")
    assert 'set "LICENSE_ENFORCED=false"' in _text("run.cmd")
    install = _text("install.ps1")
    assert "$AppDir" in install and "-Recurse" in install
    assert "LICENSE_ENFORCED=false" in install            # written to agent.env for the unsealed build
    assert "$AgentDir" in _text("package-zip.ps1")


def test_windows_ci_builds_checks_and_smoke_tests_on_a_windows_runner():
    ci = (Path(__file__).resolve().parents[2] / ".github" / "workflows" / "agent-windows-build.yml").read_text()
    assert "runs-on: windows-latest" in ci
    for step in ("agent_closure.py --check", "build-agent-exe.ps1", "runtime-check", "findings", "package-zip.ps1"):
        assert step in ci, step


# ── the one-command installer (install.ps1 / install.cmd) ────────────────────

def test_the_one_command_is_documented_and_install_cmd_passes_arguments_through():
    cmd = _text("install.cmd")
    assert "%*" in cmd and '-File "%~dp0install.ps1"' in cmd and "-ExecutionPolicy Bypass" in cmd
    readme = _text("README-CUSTOMER.txt")
    assert "install.cmd -Token vet_" in readme
    assert "Get-FileHash" in readme                      # the customer is told how to check the zip
    assert "support-bundle" in readme and "doctor" in readme and "ALLOWLIST.txt" in readme


def test_the_installer_never_changes_the_clients_security_settings():
    """Troubleshooting explains and the client's IT applies the fix. Nothing here may touch
    the firewall, Defender/antivirus, certificate stores, proxy settings or execution policy."""
    forbidden = (
        "Add-MpPreference", "Set-MpPreference", "ExclusionPath", "ExclusionProcess", "ExclusionExtension",
        "New-NetFirewallRule", "Set-NetFirewallRule", "Disable-NetFirewallRule", "netsh", "advfirewall",
        "Import-Certificate", "Import-PfxCertificate", "certutil", "Cert:\\", "X509Store",
        "Set-ExecutionPolicy", "Internet Settings", "Set-ItemProperty", "reg add", "reg.exe", "sc.exe config",
        "Disable-", "Stop-Service", "Invoke-WebRequest", "Invoke-RestMethod", "DownloadFile", "DownloadString",
    )
    for name in ("install.ps1", "uninstall.ps1", "install.cmd", "uninstall.cmd"):
        text = _text(name)
        for needle in forbidden:
            assert needle not in text, f"{name} must not contain {needle!r}"


def test_the_installer_checks_the_connection_before_it_changes_anything():
    text = _text("install.ps1")
    check = text.index("'doctor', '--preinstall'")
    first_change = text.index("Copy-Item -LiteralPath $source -Destination $AppDir")
    assert check < first_change
    assert text.index("Test-PackageHashes -Root $PSScriptRoot") < first_change   # integrity first too
    assert "-SkipPreflight" in text                         # an escape hatch for a wrong diagnosis


def test_the_installer_leaves_a_log_keeps_its_window_open_and_diagnoses_failures():
    text = _text("install.ps1")
    assert "Start-Transcript" in text and "Hide-VedhaSecrets" in text      # a log, with the token removed
    assert "Press Enter to close this window" in text                       # the elevated window never vanishes
    assert "-ElevatedChild" in text and "-Verb RunAs" in text
    assert "'doctor')" in text and "support-bundle" in text                 # failure -> diagnosis -> what to send


def test_the_installer_restores_the_old_install_if_the_new_one_fails():
    text = _text("install.ps1")
    assert '$backup = "$AppDir.old"' in text
    assert "Putting the previous installation back" in text


def test_the_installer_locks_down_the_identity_and_settings_and_removes_the_used_token():
    text = _text("install.ps1")
    assert "icacls.exe" in text and "*S-1-5-18" in text and "*S-1-5-32-544" in text     # SYSTEM + Administrators
    assert "Set-VedhaAcl -Path $DataDir" in text
    assert "Remove-VedhaTokenLine" in text
    assert "Write-Utf8NoBom" in text


def test_the_scheduled_task_runs_the_agent_directly_as_system_and_restarts_it():
    text = _text("install.ps1")
    assert "New-ScheduledTaskAction -Execute $exe -Argument 'run'" in text
    assert "-UserId 'SYSTEM'" in text and "-AtStartup" in text and "-RestartCount 999" in text
    assert "agent-service.cmd" not in text                   # the old cmd wrapper (and its unrotated redirect) is gone


def test_scripts_for_customers_are_plain_ascii_and_batch_files_use_crlf():
    for name in ("install.ps1", "uninstall.ps1", "package-zip.ps1", "README-CUSTOMER.txt", "ALLOWLIST.template.txt"):
        data = (WIN / name).read_bytes()
        assert all(b < 128 for b in data), f"{name} must be ASCII (Windows PowerShell 5.1 misreads UTF-8 without a BOM)"
        assert b"\r\n" not in data or name.endswith(".txt"), name
    for name in ("install.cmd", "uninstall.cmd"):
        data = (WIN / name).read_bytes()
        assert b"\r\n" in data and b"\n" not in data.replace(b"\r\n", b""), f"{name} must use CRLF"


def test_the_package_carries_checksums_an_allowlist_and_the_values_it_bakes_in():
    text = _text("package-zip.ps1")
    for needle in ("SHA256SUMS.txt", "ALLOWLIST.txt", "__VEDHA_MANAGER_URL__", "__VEDHA_PACKAGE_VERSION__",
                   "{{EXE_SHA256}}", "{{MANAGER_HOST}}", "vedha-agent-win.zip", ".sha256"):
        assert needle in text, needle
    template = _text("ALLOWLIST.template.txt")
    for needle in ("{{EXE_SHA256}}", "{{MANAGER_HOST}}", "{{VERSION}}", "TCP 443", "C:\\Program Files\\Vedha Agent"):
        assert needle in template, needle


def test_the_uninstaller_wrapper_just_calls_the_installer():
    text = _text("uninstall.ps1")
    assert "install.ps1" in text and "-Uninstall" in text and "-Purge:$Purge" in text
    assert "-Uninstall" in _text("uninstall.cmd")


def test_gitattributes_pins_crlf_for_batch_files():
    attrs = (WIN.parents[1] / ".gitattributes").read_text()
    assert "probe/windows/*.cmd text eol=crlf" in attrs
