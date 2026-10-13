"""test_airgap_package.py — the air-gapped Windows agent packager (scripts/airgap_package.py).

The packager runs on any OS (so the owner can repackage on macOS without a Windows box),
and its output MUST be byte-compatible with what the packaged install.ps1 verifies: the same
files, the facade URL baked in, no leftover placeholders, and a SHA256SUMS.txt in exactly the
form install.ps1's regex accepts. A real agent exe cannot be compiled here, so these tests use
a stub exe and exercise everything around it — which is the packaging logic that can regress.
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("airgap_package", REPO / "scripts" / "airgap_package.py")
ap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ap)

# The exact line format the packaged installer accepts (install.ps1 Test-PackageHashes).
_SUMS_LINE = re.compile(r"^([0-9a-f]{64})\s+\*?(.+)$")


def _stub_agent(tmp_path: Path) -> Path:
    agent = tmp_path / "vedha-agent"
    agent.mkdir()
    (agent / "vedha-agent.exe").write_bytes(b"MZ stub compiled agent\x00\x01")
    (agent / "python3.dll").write_bytes(b"stub dll")
    return agent


def _build(tmp_path: Path, manager="https://get.vedhasec.com", version="1.0.404", agent=None) -> Path:
    out = tmp_path / "out.zip"
    ap.build_airgap_zip(agent=agent or _stub_agent(tmp_path), manager_url=manager, version=version, out_zip=out)
    return out


# ── the package has exactly the right shape ──────────────────────────────────

def test_package_contains_agent_scripts_and_metadata(tmp_path):
    names = set(zipfile.ZipFile(_build(tmp_path)).namelist())
    for required in ("vedha-agent/vedha-agent.exe", "install.cmd", "install.ps1",
                     "uninstall.cmd", "uninstall.ps1", "run.cmd",
                     "README.txt", "ALLOWLIST.txt", "SHA256SUMS.txt"):
        assert required in names, required
    # the compiled binary ships; no Python source of ours does
    assert not any(n.endswith((".py", ".pyc")) for n in names)


def test_no_placeholders_survive_and_facade_is_baked_in(tmp_path):
    z = zipfile.ZipFile(_build(tmp_path))
    for name in ("install.ps1", "run.cmd", "ALLOWLIST.txt"):
        text = z.read(name).decode("utf-8", "replace")
        assert "__VEDHA_" not in text, f"placeholder left in {name}"
        assert "{{" not in text, f"template token left in {name}"
    assert "https://get.vedhasec.com" in z.read("install.ps1").decode("utf-8")
    allow = z.read("ALLOWLIST.txt").decode("utf-8")
    assert "get.vedhasec.com" in allow and "1.0.404" in allow


def test_sha256sums_is_installer_readable_and_correct(tmp_path):
    z = zipfile.ZipFile(_build(tmp_path))
    listed = {}
    for line in z.read("SHA256SUMS.txt").decode("utf-8").splitlines():
        if not line.strip():
            continue
        m = _SUMS_LINE.match(line)
        assert m, f"install.ps1 would reject this line: {line}"
        listed[m.group(2).strip()] = m.group(1)
    # every file (except the sums file itself) is listed with its real hash
    for info in z.infolist():
        if info.is_dir() or info.filename == "SHA256SUMS.txt":
            continue
        assert info.filename in listed, f"missing from SHA256SUMS: {info.filename}"
        assert listed[info.filename] == hashlib.sha256(z.read(info.filename)).hexdigest()
    assert "SHA256SUMS.txt" not in listed  # it never lists itself


def test_line_endings_follow_the_gitattributes_contract(tmp_path):
    # .gitattributes enforces, on every platform: .cmd = CRLF (cmd.exe needs it),
    # .ps1/.txt = LF. The packager preserves bytes, so baking the URL must not flip either.
    z = zipfile.ZipFile(_build(tmp_path))
    assert b"\r\n" in z.read("install.cmd"), ".cmd must stay CRLF"
    assert b"\r\n" in z.read("run.cmd"), "run.cmd must stay CRLF"
    assert b"\r\n" not in z.read("install.ps1"), ".ps1 must stay LF (baking must not introduce CRLF)"


def test_sidecar_sha256_and_release_json(tmp_path):
    out = _build(tmp_path)
    sha_side = out.with_suffix(out.suffix + ".sha256").read_text()
    assert re.match(r"^[0-9a-f]{64}  out\.zip\n$", sha_side)
    import json
    info = json.loads(out.with_suffix(".release.json").read_text())
    assert info["manager"] == "https://get.vedhasec.com" and info["package_version"] == "1.0.404"
    assert re.fullmatch(r"[0-9a-f]{64}", info["exe_sha256"])


# ── accepts a win zip too, and refuses bad input loudly ──────────────────────

def test_accepts_a_prebuilt_windows_zip(tmp_path):
    # Make a vedha-agent-win.zip-shaped archive and feed it in.
    agent = _stub_agent(tmp_path)
    win_zip = tmp_path / "vedha-agent-win.zip"
    with zipfile.ZipFile(win_zip, "w") as z:
        z.write(agent / "vedha-agent.exe", "vedha-agent/vedha-agent.exe")
        z.write(agent / "python3.dll", "vedha-agent/python3.dll")
    out = tmp_path / "from-zip.zip"
    ap.build_airgap_zip(agent=win_zip, manager_url="https://get.vedhasec.com", version="1.0.404", out_zip=out)
    assert "vedha-agent/vedha-agent.exe" in zipfile.ZipFile(out).namelist()


def test_http_manager_is_refused(tmp_path):
    with pytest.raises(ap.AirgapError, match="https://"):
        ap.build_airgap_zip(agent=_stub_agent(tmp_path), manager_url="http://lab.local", out_zip=tmp_path / "x.zip")


def test_agent_without_exe_is_refused(tmp_path):
    empty = tmp_path / "vedha-agent"
    empty.mkdir()
    with pytest.raises(ap.AirgapError, match="vedha-agent.exe"):
        ap.build_airgap_zip(agent=empty, manager_url="https://get.vedhasec.com", out_zip=tmp_path / "x.zip")
