"""The agent build kit: a small zip that holds ONLY what is needed to build and publish the Windows agent.

The point is what is NOT in it (the manager, console, detection engine, vulnerability rules, tests, keys) and that
what IS in it is enough: the closure check passes there, the compile list equals the repository's, and the release
tool inside the kit can build and verify a release.
"""
from __future__ import annotations

import importlib.util
import os
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
    for needed in ("VERSION", "install.cmd", "KIT-README.txt", "KIT-FILES.txt", "probe/windows/kit-install.ps1", "scripts/agent_release.py", "probe/install.sh",
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


def test_there_is_exactly_one_thing_to_double_click_and_it_is_the_install_script(built):
    root_files = [n for n in built["names"] if "/" not in n]
    assert sorted(root_files) == ["KIT-FILES.txt", "KIT-README.txt", "VERSION", "install.cmd"]
    cmd = zipfile.ZipFile(built["zip"]).read("install.cmd").decode("ascii")
    assert "probe\\windows\\kit-install.ps1" in cmd and "ExecutionPolicy Bypass" in cmd and "%*" in cmd
    assert "\r\n" in cmd                                                       # Windows line endings
    assert "probe/windows/kit-install.cmd" not in built["names"]               # not shipped twice


def test_the_install_script_starts_from_the_kit_without_the_repository(built, tmp_path, monkeypatch):
    pwsh = __import__("shutil").which("pwsh")
    if not pwsh:
        pytest.skip("no PowerShell here")
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    done = subprocess.run([pwsh, "-NoProfile", "-File", str(built["root"] / "probe" / "windows" / "kit-install.ps1"),
                           "-CheckOnly", "-Yes", "-NoPause", "-Server", "ubuntu@203.0.113.7",
                           "-ManagerUrl", "https://api.example.com"],
                          capture_output=True, text=True, timeout=120)
    out = done.stdout + done.stderr
    assert "Vedha agent build kit 1.0" in out and "Checking this PC" in out, out        # it ran from the kit alone
    if sys.platform != "win32":
        assert done.returncode == 1 and "must run on Windows" in out                   # and refuses cleanly elsewhere
        assert "Nothing was built or changed" in out


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


# ── the one-line bootstrap: download from a private link, check, unpack, publish ──────────────────────

import hashlib
import shutil
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVER = {"server": "ubuntu@203.0.113.7", "manager_url": "https://api.example.com"}


def _serve(data: bytes):
    seen: list[str] = []

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            seen.append(self.path)
            self.send_response(200)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}", seen


def _run(command: str, cwd: Path):
    return subprocess.run([shutil.which("pwsh"), "-NoProfile", "-Command", command], cwd=cwd,
                          capture_output=True, text=True, timeout=180)


def _command(url, sha, dest, **kw):
    # The test serves plain http on localhost and unpacks into a temp folder; the real command is https and C:\...
    cmd = kit.bootstrap_command("https://placeholder.example.com/kit.zip", sha, install_dir="C:\\VedhaKit", powershell="pwsh",
                                extra_args="-CheckOnly", **SERVER, **kw)
    return cmd.replace("https://placeholder.example.com/kit.zip", url).replace("C:\\VedhaKit", str(dest)).replace(
        "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ", "")


def test_the_command_has_exactly_the_shape_a_person_pastes(built):
    sha = hashlib.sha256(built["zip"].read_bytes()).hexdigest()
    cmd = kit.bootstrap_command("https://b.s3.amazonaws.com/k.zip?X-Amz-Signature=ab&X-Amz-Expires=3600", sha,
                                allow_tokenless=True, **SERVER)
    assert "\n" not in cmd and cmd.count("Invoke-WebRequest") == 1
    assert f"-ne '{sha}'" in cmd and "-AllowTokenlessInstall" in cmd
    assert "Expand-Archive" in cmd and "-Force" in cmd
    assert "Remove-Item -LiteralPath $dir" not in cmd                       # never deletes an existing build folder
    assert "ExecutionPolicy Bypass" in cmd                                   # a default Windows policy cannot block the script
    assert "kit-install.ps1" in cmd and "-Yes -NoPause" in cmd               # the one script does the checks and the publish
    assert "publish-release.ps1" not in cmd and "winget" not in cmd          # nothing is duplicated in the command
    assert "Tls12" in cmd


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_download_check_unpack_and_run_the_publish_plan(built, tmp_path):
    data = built["zip"].read_bytes()
    httpd, base, seen = _serve(data)
    try:
        dest = tmp_path / "VedhaKit"
        done = _run(_command(base + "/kit.zip?sig=abc&exp=1", hashlib.sha256(data).hexdigest(), dest), tmp_path)
    finally:
        httpd.shutdown()
    out = done.stdout + done.stderr
    assert "Vedha agent build kit 1.0" in out, out                            # downloaded, verified, unpacked, started
    assert (dest / "probe" / "windows" / "kit-install.ps1").is_file() and (dest / "install.cmd").is_file()
    assert seen == ["/kit.zip?sig=abc&exp=1"]
    assert not list(Path(tmp_path).glob("vedha-agent-build-kit.zip"))      # the download is removed


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_a_kit_that_does_not_match_its_checksum_is_not_unpacked(built, tmp_path):
    data = built["zip"].read_bytes()
    httpd, base, _ = _serve(data[:-1] + b"X")                              # tampered in transit
    try:
        dest = tmp_path / "VedhaKit"
        done = _run(_command(base + "/kit.zip", hashlib.sha256(data).hexdigest(), dest), tmp_path)
    finally:
        httpd.shutdown()
    assert done.returncode != 0 and "does not match its checksum" in (done.stdout + done.stderr)
    assert not dest.exists()


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_unpacking_over_an_existing_folder_keeps_what_is_already_there(built, tmp_path):
    data = built["zip"].read_bytes()
    dest = tmp_path / "VedhaKit"
    (dest / "probe" / "windows" / "dist" / "vedha-agent").mkdir(parents=True)
    (dest / "probe" / "windows" / "dist" / "vedha-agent" / "vedha-agent.exe").write_bytes(b"built earlier")
    (dest / "probe" / "windows" / ".venv-win").mkdir()
    (dest / "probe" / "windows" / ".venv-win" / "marker").write_text("keep me")
    httpd, base, _ = _serve(data)
    try:
        done = _run(_command(base + "/kit.zip", hashlib.sha256(data).hexdigest(), dest), tmp_path)
    finally:
        httpd.shutdown()
    assert "Vedha agent build kit 1.0" in done.stdout + done.stderr
    assert (dest / "probe" / "windows" / "dist" / "vedha-agent" / "vedha-agent.exe").read_bytes() == b"built earlier"
    assert (dest / "probe" / "windows" / ".venv-win" / "marker").read_text() == "keep me"


@pytest.mark.parametrize("url", ["http://x.example.com/k.zip", "https://x.example.com/k zip", "https://x.example.com/k'.zip",
                                 "https://x.example.com/k\".zip", "https://x.example.com/k`whoami`.zip", "ftp://x/k.zip", ""])
def test_a_link_that_could_break_out_of_its_quotes_is_refused(url):
    with pytest.raises(ValueError):
        kit.bootstrap_command(url, "a" * 64, **SERVER)


@pytest.mark.parametrize("field, value", [("server", "ubuntu@host; calc"), ("server", "a b"), ("manager_url", "http://x.com"),
                                          ("manager_url", "https://x.com/'; calc; '"), ("sha256", "abc"),
                                          ("install_dir", "C:\\a b\\c"), ("install_dir", "C:\\x'; calc; '"),
                                          ("extra_args", "; calc")])
def test_other_values_are_checked_too(field, value):
    args = {"url": "https://x.example.com/k.zip", "sha256": "a" * 64, **SERVER}
    kwargs = {field: value}
    if field in ("server", "manager_url"):
        args[field] = value
        kwargs = {}
    elif field == "sha256":
        args["sha256"] = value
        kwargs = {}
    with pytest.raises(ValueError):
        kit.bootstrap_command(**args, **kwargs)


def test_the_cli_prints_the_command_with_the_zips_own_checksum(tmp_path, capsys):
    assert kit.main(["--out", str(tmp_path), "--url", "https://x.example.com/k.zip?sig=1", "--server", "ubuntu@203.0.113.7",
                     "--manager-url", "https://api.example.com", "--allow-tokenless"]) == 0
    out = capsys.readouterr().out
    zip_path = next(tmp_path.glob("*.zip"))
    assert hashlib.sha256(zip_path.read_bytes()).hexdigest() in out and "-AllowTokenlessInstall" in out


def test_the_command_can_carry_the_ssh_key_path_and_refuses_a_bad_one():
    cmd = kit.bootstrap_command("https://x.example.com/k.zip", "a" * 64, ssh_key="C:\\Users\\WZ\\keys\\server.pem", **SERVER)
    assert "-SshKey 'C:\\Users\\WZ\\keys\\server.pem' -ManagerUrl" in cmd
    assert "-SshKey" not in kit.bootstrap_command("https://x.example.com/k.zip", "a" * 64, **SERVER)
    for bad in ("server.pem", "C:\\k'; calc; '", "C:\\a\\..\\b.pem", "C:\\a;b.pem"):
        with pytest.raises(ValueError):
            kit.bootstrap_command("https://x.example.com/k.zip", "a" * 64, ssh_key=bad, **SERVER)


# ── defaults baked into the kit, and the one-screen settings flow ────────────────────────────────

def test_the_defaults_file_carries_the_values_install_cmd_shows_and_is_validated(tmp_path):
    import json
    target = kit.build(tmp_path, default_server="ubuntu@16.4.75.44", default_manager_url="https://api.vedhasec.com/",
                       default_tokenless=True)
    with zipfile.ZipFile(target) as zf:
        data = json.loads(zf.read("probe/windows/kit-defaults.json"))
        assert "probe/windows/kit-defaults.json" in zf.read("KIT-FILES.txt").decode()
    assert data == {"server": "ubuntu@16.4.75.44", "manager_url": "https://api.vedhasec.com", "tokenless": True}
    for bad in ({"default_server": "u@h; calc"}, {"default_manager_url": "http://x.com"}, {"default_manager_url": "https://x/'"}):
        with pytest.raises(ValueError):
            kit.build(tmp_path / "bad", **bad)


def test_without_defaults_the_file_is_empty_not_missing(built):
    import json
    assert json.loads(zipfile.ZipFile(built["zip"]).read("probe/windows/kit-defaults.json")) == {
        "server": "", "manager_url": "", "tokenless": False}


def _run_install(root, tmp_path, stdin, *extra):
    return subprocess.run([shutil.which("pwsh"), "-NoProfile", "-File", str(root / "probe" / "windows" / "kit-install.ps1"),
                           "-NoPause", "-CheckOnly", *extra], input=stdin, capture_output=True, text=True, timeout=120,
                          env={**os.environ, "USERPROFILE": str(tmp_path / "home")})


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_the_settings_screen_shows_the_defaults_and_one_enter_accepts_them(tmp_path):
    target = kit.build(tmp_path / "k", default_server="ubuntu@16.4.75.44", default_manager_url="https://api.vedhasec.com",
                       default_tokenless=True)
    root = tmp_path / "kit"
    zipfile.ZipFile(target).extractall(root)
    (tmp_path / "home").mkdir()
    done = _run_install(root, tmp_path, "\n")
    out = done.stdout + done.stderr
    assert "These settings will be used" in out, out
    assert "ubuntu@16.4.75.44" in out and "https://api.vedhasec.com" in out and "yes (you approve each machine in Fleet)" in out
    assert "Press Enter to start, or type 1-4 to change one" in out
    assert "Checking this PC" in out                                # one Enter and it moved on to the checks
    assert "free on" not in out and "GB free" not in out           # no disk check any more


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_typing_a_number_changes_that_value_and_the_new_value_is_used_and_remembered(tmp_path):
    target = kit.build(tmp_path / "k", default_server="ubuntu@16.4.75.44", default_manager_url="https://api.vedhasec.com")
    root = tmp_path / "kit"
    zipfile.ZipFile(target).extractall(root)
    (tmp_path / "home").mkdir()
    done = _run_install(root, tmp_path, "1\nec2-user@10.0.0.9\n3\nhttps://manager.example.org\n4\n\n")
    out = done.stdout + done.stderr
    assert "ec2-user@10.0.0.9" in out and "https://manager.example.org" in out, out
    assert "Installs without token . yes" in out                      # option 4 turned it on
    assert "Checking the server ec2-user@10.0.0.9" in out or "Checking the server" in out


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_a_value_typed_wrongly_is_refused_and_asked_again(tmp_path):
    target = kit.build(tmp_path / "k", default_server="ubuntu@16.4.75.44", default_manager_url="https://api.vedhasec.com")
    root = tmp_path / "kit"
    zipfile.ZipFile(target).extractall(root)
    (tmp_path / "home").mkdir()
    done = _run_install(root, tmp_path, "3\nhttp://not-https.example.com\nhttps://good.example.com\n\n")
    out = done.stdout + done.stderr
    assert "That does not look right" in out and "https://good.example.com" in out, out


@pytest.mark.skipif(not shutil.which("pwsh"), reason="no PowerShell here")
def test_yes_mode_asks_nothing_and_needs_the_values(tmp_path):
    target = kit.build(tmp_path / "k")                                 # a kit with no defaults
    root = tmp_path / "kit"
    zipfile.ZipFile(target).extractall(root)
    (tmp_path / "home").mkdir()
    done = _run_install(root, tmp_path, "", "-Yes")
    assert "-Yes needs a server login" in done.stdout + done.stderr
