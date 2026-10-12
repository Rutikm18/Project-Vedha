"""The agent build kit: a small zip that holds ONLY what is needed to build and publish the Windows agent.

The point is what is NOT in it (the manager, console, detection engine, vulnerability rules, tests, keys) and that
what IS in it is enough: the closure check passes there, the compile list equals the repository's, and the release
tool inside the kit can build and verify a release.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


kit = _load("make_agent_build_kit_t", "scripts/make_agent_build_kit.py")


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("kit")
    target = kit.build(out)
    root = out / "x"
    with zipfile.ZipFile(target) as zf:
        names = zf.namelist()
        zf.extractall(root)
    return {"zip": target, "root": root, "names": names}


def test_it_holds_no_manager_code_no_rules_no_tests_and_no_secrets(built):
    for name in built["names"]:
        low = name.lower()
        assert not low.startswith(("manager/", "docs/", ".github/", "deploy/", ".git/")), name
        assert "findings.py" not in low and "detection_engine" not in low and "/tests/" not in low, name
        assert not low.endswith((".env", ".pem", ".pfx", ".md")), name
    assert not [n for n in built["names"] if n.startswith("probe/") and n.split("/")[1] in
                {"main_scripts", "cve", "tests", "Capabilties", "scans"}]


def test_it_is_small(built):
    assert built["zip"].stat().st_size < 3 * 1024 * 1024
    assert len(built["names"]) < 200


def test_the_expected_files_are_there(built):
    names = set(built["names"])
    for needed in ("VERSION", "KIT-README.txt", "KIT-FILES.txt", "scripts/agent_release.py", "probe/install.sh",
                   "probe/requirements-runtime.txt", "probe/tools/agent_closure.py", "probe/agent/agent.py",
                   "probe/agent/release_trust.py", "probe/agent/auto_update.py", "probe/windows/publish-release.ps1",
                   "probe/windows/build-agent-exe.ps1", "probe/windows/package-zip.ps1", "probe/windows/install-remote.ps1",
                   "probe/windows/install-remote.cmd", "probe/windows/install.ps1"):
        assert needed in names, needed


def test_every_file_in_the_agent_closure_is_in_the_kit(built):
    closure = kit._closure().compute(kit.PROBE)
    expected = {f"probe/{p.relative_to(kit.PROBE).as_posix()}" for p in closure.files}
    assert expected <= set(built["names"])
    in_kit = {n for n in built["names"] if n.startswith(("probe/agent/", "probe/scanner/", "probe/workflow/"))}
    assert in_kit == expected                              # and nothing else from those packages


def test_the_closure_check_passes_inside_the_kit_and_lists_the_same_modules(built):
    run = lambda *a: subprocess.run([sys.executable, "-I", *a], cwd=built["root"], capture_output=True, text=True, timeout=120)
    check = run("probe/tools/agent_closure.py", "--check")
    assert check.returncode == 0, check.stdout + check.stderr
    here = subprocess.run([sys.executable, "-I", str(kit.PROBE / "tools" / "agent_closure.py"), "--list"],
                          capture_output=True, text=True, timeout=120).stdout
    assert run("probe/tools/agent_closure.py", "--list").stdout == here


def test_the_release_tool_in_the_kit_can_build_and_verify_a_release(built, tmp_path):
    root = built["root"]
    spec = importlib.util.spec_from_file_location("kit_release_tool", root / "scripts" / "agent_release.py")
    tool = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = tool
    spec.loader.exec_module(tool)
    ed_pub = tool.keygen(tmp_path / "ed.pem")
    p256 = tool.keygen_p256(tmp_path / "p256.pem")
    win = tmp_path / "win.zip"
    with zipfile.ZipFile(win, "w") as zf:
        zf.writestr("vedha-agent/vedha-agent.exe", b"MZ")
        zf.writestr("install.ps1", "# inner\n")
    out = tool.build_release(key_path=tmp_path / "ed.pem", out=tmp_path / "out", arches=[], version="9.9.9",
                             builder=lambda *a: None, saver=lambda *a: None, p256_key_path=tmp_path / "p256.pem",
                             windows_zip=win, agent_version="2.2.9")
    manifest = tool.verify_release_dir(out, ed_pub, p256_public_key_b64=p256)
    assert manifest["version"] == "9.9.9" and manifest["packages"][0]["os"] == "windows"


def test_the_plan_runs_from_the_kit_without_the_repository(built):
    pwsh = __import__("shutil").which("pwsh")
    if not pwsh:
        pytest.skip("no PowerShell here")
    done = subprocess.run([pwsh, "-NoProfile", "-File", str(built["root"] / "probe" / "windows" / "publish-release.ps1"),
                           "-DryRun", "-Server", "ubuntu@203.0.113.7", "-ManagerUrl", "https://api.example.com",
                           "-ConfigureManager", "-AllowTokenlessInstall"],
                          capture_output=True, text=True, timeout=120)
    assert done.returncode == 0 and "Dry run: nothing was done" in done.stdout, done.stdout + done.stderr


def test_it_is_reproducible(built, tmp_path):
    second = kit.build(tmp_path)
    assert second.read_bytes() == built["zip"].read_bytes()


def test_a_forbidden_path_stops_the_build():
    with pytest.raises(SystemExit):
        kit.check_clean(["manager/backend/app/main.py"])
    with pytest.raises(SystemExit):
        kit.check_clean(["probe/scanner/findings.py"])
    with pytest.raises(SystemExit):
        kit.check_clean(["probe/windows/signing-key.pem"])
