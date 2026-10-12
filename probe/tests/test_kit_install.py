"""kit-install.ps1 - the one script the build kit runs: checks first, then publishes.

The pure helpers are unit-tested by windows/tests/Test-KitInstall.ps1 (run here through PowerShell). The server
checks are exercised against a fake `ssh` placed first on PATH, so what the script does with each answer a real
server can give (not reachable, folder missing, docker refused, everything fine) is pinned without a server.
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

PS = shutil.which("pwsh")
pytestmark = pytest.mark.skipif(PS is None, reason="no PowerShell on this machine")
WIN = Path(__file__).resolve().parents[1] / "windows"
SCRIPT = WIN / "kit-install.ps1"


def test_the_helper_unit_tests_pass():
    done = subprocess.run([PS, "-NoProfile", "-File", str(WIN / "tests" / "Test-KitInstall.ps1")],
                          capture_output=True, text=True, timeout=180)
    assert done.returncode == 0 and "checks passed" in done.stdout, done.stdout + done.stderr


@pytest.fixture
def fake_ssh(tmp_path):
    """A `ssh` that answers like a server. Behaviour is chosen with FAKE_SSH_MODE."""
    if sys.platform == "win32":
        pytest.skip("the fake ssh is a shell script")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    ssh = bin_dir / "ssh"
    ssh.write_text("""#!/bin/sh
echo "$*" >> "$FAKE_SSH_LOG"
cmd="$*"
case "$FAKE_SSH_MODE" in
  unreachable) echo "ssh: connect to host x port 22: Connection timed out" >&2; exit 255 ;;
  needkey) case "$cmd" in *" -i "*|"-i "*) ;; *) echo "ubuntu@x: Permission denied (publickey)." >&2; exit 255 ;; esac ;;
esac
case "$cmd" in
  *vedha-ssh-ok*) echo vedha-ssh-ok; exit 0 ;;
  *compose-file-ok*)
    case "$FAKE_SSH_MODE" in
      nofolder)  echo compose-file-missing; echo env-file-missing; echo docker-ok ;;
      nodocker)  echo compose-file-ok; echo env-file-ok; echo docker-denied ;;
      *)         echo compose-file-ok; echo env-file-ok; echo docker-ok ;;
    esac; exit 0 ;;
esac
exit 0
""")
    ssh.chmod(ssh.stat().st_mode | stat.S_IEXEC)
    return bin_dir


def _server_check(fake_ssh, tmp_path, mode, *, keyfile=None):
    key_arg = f"-Key '{keyfile}'" if keyfile else "-Key ''"
    snippet = (f". '{SCRIPT}' -Yes -NoPause; "
               f"$r = Confirm-KitServer -Target 'ubuntu@203.0.113.7' {key_arg} -ComposeDir '/opt/Project-Vedha/manager'; "
               "Write-Host ('RESULT=[' + $r + '] PROBLEMS=' + $script:Problems.Count)")
    env = {**os.environ, "PATH": f"{fake_ssh}{os.pathsep}{os.environ['PATH']}", "FAKE_SSH_MODE": mode,
           "USERPROFILE": str(tmp_path), "FAKE_SSH_LOG": str(tmp_path / "ssh.log")}
    done = subprocess.run([PS, "-NoProfile", "-Command", snippet], capture_output=True, text=True, timeout=120, env=env)
    return done.stdout + done.stderr


def test_the_host_key_question_is_never_asked(fake_ssh, tmp_path):
    out = _server_check(fake_ssh, tmp_path, "ok")
    assert "continue connecting" not in out and "type yes" not in out
    calls = (tmp_path / "ssh.log").read_text().splitlines()
    assert calls and all("StrictHostKeyChecking=accept-new" in line for line in calls), calls


def test_a_healthy_server_passes_every_check(fake_ssh, tmp_path):
    out = _server_check(fake_ssh, tmp_path, "ok")
    assert "RESULT=[/opt/Project-Vedha/manager] PROBLEMS=0" in out, out
    assert "logged in to ubuntu@203.0.113.7" in out and "manager folder found" in out and "may run docker" in out


def test_an_unreachable_server_says_how_to_fix_it_and_stops_before_any_build(fake_ssh, tmp_path):
    out = _server_check(fake_ssh, tmp_path, "unreachable")
    assert "Cannot log in to ubuntu@203.0.113.7" in out and "PROBLEMS=1" in out, out
    assert "ubuntu on Ubuntu, ec2-user on Amazon Linux" in out
    assert "RESULT=[]" in out


def test_a_wrong_manager_folder_is_reported_with_the_command_that_finds_it(fake_ssh, tmp_path):
    out = _server_check(fake_ssh, tmp_path, "nofolder")
    assert "does not hold docker-compose.yml and .env" in out and "docker compose ls" in out, out
    assert "PROBLEMS=1" in out and "RESULT=[]" in out


def test_a_login_that_may_not_run_docker_is_caught_before_the_long_build(fake_ssh, tmp_path):
    out = _server_check(fake_ssh, tmp_path, "nodocker")
    assert "not allowed to run docker" in out and "usermod -aG docker" in out and "PROBLEMS=1" in out, out


def test_a_missing_key_file_is_caught_before_ssh_is_tried(fake_ssh, tmp_path):
    out = _server_check(fake_ssh, tmp_path, "ok", keyfile="C:\\no\\such\\key.pem")
    assert "ssh key file was not found" in out and "PROBLEMS=1" in out, out


def test_checks_run_before_anything_is_built_and_the_settings_file_is_only_written_after_they_pass():
    text = SCRIPT.read_text()
    main = text[text.index("function Invoke-KitMain"):]
    order = ["Confirm-KitPc", "Confirm-KitServer", "Problems.Count -gt 0", "ConvertTo-KitSettingsJson", "if ($CheckOnly)", "publish-release.ps1"]
    positions = [main.index(step) for step in order]
    assert positions == sorted(positions), dict(zip(order, positions))


def test_the_script_never_assigns_the_read_only_home_variable_and_relaxes_stderr_for_native_calls():
    text = SCRIPT.read_text()
    assert "$home =" not in text.lower().replace("$userhome =", "")
    assert text.count("$ErrorActionPreference = 'Continue'") >= 2           # ssh and python write warnings to stderr


def _server_check_stdin(fake_ssh, tmp_path, mode, stdin, *, trust_any_key=False, extra=""):
    override = "function Test-KitKeyPath { $true }; " if trust_any_key else ""
    snippet = (f". '{SCRIPT}' {extra} -NoPause; {override}"
               "$r = Confirm-KitServer -Target 'ubuntu@203.0.113.7' -Key '' -ComposeDir '/opt/Project-Vedha/manager'; "
               "Write-Host ('RESULT=[' + $r + '] PROBLEMS=' + $script:Problems.Count + ' KEY=[' + $script:KitSshKey + ']')")
    env = {**os.environ, "PATH": f"{fake_ssh}{os.pathsep}{os.environ['PATH']}", "FAKE_SSH_MODE": mode,
           "USERPROFILE": str(tmp_path), "FAKE_SSH_LOG": str(tmp_path / "ssh.log")}
    done = subprocess.run([PS, "-NoProfile", "-Command", snippet], input=stdin, capture_output=True, text=True, timeout=120, env=env)
    return done.stdout + done.stderr


def test_a_refused_login_asks_for_the_key_file_and_carries_on_with_it(fake_ssh, tmp_path):
    key = tmp_path / "mykey.pem"
    key.write_text("pretend")
    out = _server_check_stdin(fake_ssh, tmp_path, "needkey", f"{key}\n", trust_any_key=True)
    assert "The server did not accept the login" in out and "needs the key file" in out, out
    assert "search your PC for *.pem" in out
    assert f"RESULT=[/opt/Project-Vedha/manager] PROBLEMS=0 KEY=[{key}]" in out        # logged in, key remembered for the publish
    calls = (tmp_path / "ssh.log").read_text().splitlines()
    assert " -i " not in " " + calls[0] and any(f"-i {key}" in line for line in calls[1:])      # first try without a key, then with it


def test_pressing_enter_at_the_key_question_stops_with_one_clear_problem(fake_ssh, tmp_path):
    out = _server_check_stdin(fake_ssh, tmp_path, "needkey", "\n")
    assert "Cannot log in to ubuntu@203.0.113.7 without a key file" in out and "PROBLEMS=1" in out and "RESULT=[]" in out, out


def test_a_wrong_path_is_asked_again_and_it_gives_up_after_three_tries(fake_ssh, tmp_path):
    out = _server_check_stdin(fake_ssh, tmp_path, "needkey", "nonsense\nnonsense2\nnonsense3\n")
    assert out.count("does not look like a Windows path") >= 1 and "PROBLEMS=1" in out and "RESULT=[]" in out, out


def test_with_yes_it_never_asks_a_question(fake_ssh, tmp_path):
    out = _server_check_stdin(fake_ssh, tmp_path, "needkey", "", extra="-Yes")
    assert "Paste the full path" not in out and "PROBLEMS=1" in out and "RESULT=[]" in out, out
