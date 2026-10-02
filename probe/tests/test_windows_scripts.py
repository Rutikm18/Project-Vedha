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
