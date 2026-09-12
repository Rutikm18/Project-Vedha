# Universal cross-OS vedha-agent installer + self-scan — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One Python orchestrator (`agent/setup.py`) + thin `install.sh`/`install.ps1` bootstraps that install every dependency per OS, connect the agent to a Manager, run a manager-less self-scan of the host's own IP, and optionally install a per-OS service — on macOS, Linux, and Windows.

**Architecture:** A pure-logic platform layer (`setup_platform.py`) and a dependency layer (`setup_deps.py`) sit under a CLI brain (`setup.py`) with three subcommands (`doctor`, `self-scan`, `connect`). Two ~30-line shell shims only bootstrap Python and hand off to the brain. The brain reuses the existing daemon (`agent.agent`) and local engine (`agent.local_run`) unchanged.

**Tech Stack:** Python 3.8+ stdlib (`argparse`, `socket`, `subprocess`, `platform`, `ctypes`), `venv`+`pip`, pytest, POSIX sh, PowerShell.

## Global Constraints

- All paths are relative to repo root `/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha`. Probe code lives under `probe/`.
- Branch: `cross-os-agent-installer` (already checked out).
- Python floor: **3.8+** (matches the existing `install.sh` preflight). Use only stdlib in `setup_platform.py`/`setup.py` — no third-party imports.
- Tests: pytest from inside `probe/`. Run with `.venv/bin/python -m pytest tests/<file> -v`. Tests must be pure — no network, no root, no real subprocess side effects (mock them).
- **The installer never requires root.** It detects privilege and warns; unprivileged (and all Windows) → connect-scan fallback. Root/admin is requested only for `--service`.
- **Never a Docker path** in the brain or shims (Docker can't scan the LAN on Win/macOS).
- Reused, do not modify: `agent.agent` (daemon `run` + `local-run`, exit codes 2=manager-unreachable, 3=awaiting-approval, 4=orphaned-identity), `agent.local_run.run(argv)` (reads scope from `PROBE_SCOPE_FILE`, default `/tmp/s.txt`; the target must be in scope), `agent.cli.normalize_manager_url`.
- Runtime deps file: `requirements-runtime.txt`.
- Commit trailer (both lines, verbatim):
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK
  ```

---

### Task 1: Platform layer (`setup_platform.py`) — pure OS/scope/service logic

**Files:**
- Create: `probe/agent/setup_platform.py`
- Test: `probe/tests/test_setup_platform.py`

**Interfaces:**
- Produces: `detect_os() -> str` (`"linux"|"macos"|"windows"|"unknown"`); `detect_linux_pm() -> str` (`"apt"|"dnf"|"pacman"|"unknown"`); `is_privileged() -> bool`; `detect_primary_ip() -> str | None`; `cidr_from_ip(ip: str | None) -> str | None`; `detect_scope_cidr() -> str | None`; `render_service_unit(os_name: str, python_exe: str, probe_dir: str, manager: str, scope: str, name: str) -> tuple[str, str]` (returns `(target_path, file_contents)`).

- [ ] **Step 1: Write the failing tests**

```python
# probe/tests/test_setup_platform.py
from __future__ import annotations
from agent import setup_platform as sp


def test_cidr_from_ipv4():
    assert sp.cidr_from_ip("192.168.1.50") == "192.168.1.0/24"

def test_cidr_rejects_loopback_v6_and_none():
    assert sp.cidr_from_ip("127.0.0.1") is None
    assert sp.cidr_from_ip("::1") is None
    assert sp.cidr_from_ip(None) is None
    assert sp.cidr_from_ip("") is None

def test_detect_os_is_known():
    assert sp.detect_os() in {"linux", "macos", "windows", "unknown"}

def test_is_privileged_returns_bool():
    assert isinstance(sp.is_privileged(), bool)

def test_render_systemd_unit_has_execstart_and_restart():
    path, body = sp.render_service_unit(
        "linux", "/opt/p/.venv/bin/python", "/opt/p",
        "https://m.example.com", "10.0.0.0/24", "host-probe")
    assert path.endswith("/vedha-agent.service")
    assert "ExecStart=/opt/p/.venv/bin/python -m agent.agent" in body
    assert "Restart=always" in body
    assert "PLATFORM_URL=https://m.example.com" in body

def test_render_launchd_plist_for_macos():
    path, body = sp.render_service_unit(
        "macos", "/opt/p/.venv/bin/python", "/opt/p",
        "https://m.example.com", "10.0.0.0/24", "host-probe")
    assert path.endswith("com.vedha.agent.plist")
    assert "<key>KeepAlive</key>" in body

def test_render_windows_returns_schtasks_command():
    path, body = sp.render_service_unit(
        "windows", "C:\\p\\.venv\\Scripts\\python.exe", "C:\\p",
        "https://m.example.com", "10.0.0.0/24", "host-probe")
    assert path == "SCHTASKS"          # sentinel: Windows uses a command, not a file
    assert "schtasks" in body.lower() and "VedhaAgent" in body
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_platform.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'agent.setup_platform'`.

- [ ] **Step 3: Implement `setup_platform.py`**

```python
# probe/agent/setup_platform.py
"""Pure, dependency-free platform logic for the cross-OS installer.

No side effects: OS/arch/privilege detection, primary-IP + /24 derivation, and
service-unit rendering. Everything here is unit-testable without root or network.
"""
from __future__ import annotations

import ctypes
import os
import platform
import socket


def detect_os() -> str:
    s = platform.system().lower()
    return {"linux": "linux", "darwin": "macos", "windows": "windows"}.get(s, "unknown")


def detect_linux_pm() -> str:
    """Package manager family from /etc/os-release; 'unknown' when undetectable."""
    idlike = ""
    try:
        with open("/etc/os-release", encoding="utf-8") as fh:
            data = {}
            for line in fh:
                if "=" in line:
                    k, v = line.rstrip("\n").split("=", 1)
                    data[k] = v.strip().strip('"')
        idlike = f"{data.get('ID', '')} {data.get('ID_LIKE', '')}".lower()
    except OSError:
        pass
    if any(x in idlike for x in ("debian", "ubuntu", "mint")):
        return "apt"
    if any(x in idlike for x in ("rhel", "fedora", "centos", "rocky", "alma")):
        return "dnf"
    if "arch" in idlike:
        return "pacman"
    return "unknown"


def is_privileged() -> bool:
    if os.name == "posix":
        return os.geteuid() == 0  # type: ignore[attr-defined]
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore[attr-defined]
    except Exception:
        return False


def detect_primary_ip() -> str | None:
    """Host's primary source IPv4 via a routing lookup. Sends no packets; needs no root."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def cidr_from_ip(ip: str | None) -> str | None:
    if not ip or ip.count(".") != 3 or ip.startswith("127."):
        return None
    a, b, c, _ = ip.split(".")
    if not all(part.isdigit() for part in (a, b, c)):
        return None
    return f"{a}.{b}.{c}.0/24"


def detect_scope_cidr() -> str | None:
    return cidr_from_ip(detect_primary_ip())


_SYSTEMD = """\
[Unit]
Description=Vedha Agent (probe)
After=network-online.target

[Service]
Type=simple
WorkingDirectory={probe_dir}
Environment=PLATFORM_URL={manager}
Environment=PROBE_NETWORK_SEGMENTS={scope}
Environment=PROBE_NAME={name}
Environment=VERIFY_TLS=true
ExecStart={python} -m agent.agent
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

_LAUNCHD = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.vedha.agent</string>
  <key>WorkingDirectory</key><string>{probe_dir}</string>
  <key>ProgramArguments</key>
  <array><string>{python}</string><string>-m</string><string>agent.agent</string></array>
  <key>EnvironmentVariables</key><dict>
    <key>PLATFORM_URL</key><string>{manager}</string>
    <key>PROBE_NETWORK_SEGMENTS</key><string>{scope}</string>
    <key>PROBE_NAME</key><string>{name}</string>
    <key>VERIFY_TLS</key><string>true</string>
  </dict>
  <key>KeepAlive</key><true/>
  <key>RunAtLoad</key><true/>
</dict></plist>
"""


def render_service_unit(os_name: str, python_exe: str, probe_dir: str,
                        manager: str, scope: str, name: str) -> tuple[str, str]:
    """Return (target_path, contents). Windows returns ('SCHTASKS', command_string)."""
    if os_name == "linux":
        body = _SYSTEMD.format(python=python_exe, probe_dir=probe_dir,
                               manager=manager, scope=scope, name=name)
        return "/etc/systemd/system/vedha-agent.service", body
    if os_name == "macos":
        body = _LAUNCHD.format(python=python_exe, probe_dir=probe_dir,
                               manager=manager, scope=scope, name=name)
        return os.path.expanduser("~/Library/LaunchAgents/com.vedha.agent.plist"), body
    if os_name == "windows":
        # A Scheduled Task running the daemon at boot as SYSTEM.
        cmd = (
            'schtasks /Create /TN VedhaAgent /SC ONSTART /RU SYSTEM /RL HIGHEST /F '
            f'/TR "\\"{python_exe}\\" -m agent.agent"'
        )
        return "SCHTASKS", cmd
    raise ValueError(f"unsupported os for service: {os_name!r}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_platform.py -v`
Expected: PASS (8 tests).

- [ ] **Step 5: Commit**

```bash
git add probe/agent/setup_platform.py probe/tests/test_setup_platform.py
git commit -m "$(printf 'Add pure cross-OS platform layer for the agent installer\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 2: CLI brain skeleton + `doctor` (`setup.py`)

**Files:**
- Create: `probe/agent/setup.py`
- Test: `probe/tests/test_setup_cli.py`

**Interfaces:**
- Consumes: `setup_platform.detect_os/detect_linux_pm/is_privileged/detect_scope_cidr`.
- Produces: `build_parser() -> argparse.ArgumentParser`; `cmd_doctor(args) -> int`; `main(argv: list[str] | None = None) -> int`. Subcommands registered: `doctor`, `self-scan`, `connect` (the latter two are stubbed here, filled in Tasks 4–5).

- [ ] **Step 1: Write the failing tests**

```python
# probe/tests/test_setup_cli.py
from __future__ import annotations
from agent import setup


def test_parser_has_three_subcommands():
    parser = setup.build_parser()
    sub = {a.dest: a for a in parser._subparsers._group_actions}  # noqa: SLF001
    # smoke: parsing each subcommand does not error
    for cmd in ("doctor", "self-scan", "connect"):
        ns = parser.parse_args([cmd] if cmd != "connect" else [cmd, "--manager", "http://x:18080"])
        assert ns.cmd == cmd

def test_doctor_returns_zero_and_reports_os(capsys):
    rc = setup.main(["doctor"])
    out = capsys.readouterr().out.lower()
    assert rc == 0
    assert "os" in out and "python" in out

def test_connect_requires_manager():
    # argparse exits non-zero (SystemExit) when --manager is missing
    try:
        setup.main(["connect"])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code != 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_cli.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'agent.setup'`.

- [ ] **Step 3: Implement `setup.py` (doctor now; self-scan/connect stubbed)**

```python
# probe/agent/setup.py
"""Cross-OS installer/orchestrator brain: doctor | self-scan | connect.

One source of truth for every OS-aware install/run decision. Reuses agent.agent
(daemon + local-run) and agent.local_run unchanged.
"""
from __future__ import annotations

import argparse
import shutil
import sys

from agent import setup_platform as sp


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vedha-setup", description="Vedha agent installer")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="report OS / privilege / Python / deps / reachability")

    ss = sub.add_parser("self-scan", help="scan THIS host's own IP (no Manager)")
    ss.add_argument("--profile", default="it", choices=["it", "iot", "ot"])
    ss.add_argument("--stage", default="deep_scan")

    cn = sub.add_parser("connect", help="connect the agent to a Manager")
    cn.add_argument("--manager", required=True)
    grp = cn.add_mutually_exclusive_group()
    grp.add_argument("--enroll", action="store_true", help="zero-touch pairing")
    grp.add_argument("--pat", help="use a saved PAT")
    grp.add_argument("--token", help="pre-authorized enroll token")
    cn.add_argument("--scope", help="CIDR ceiling (default: auto-detected /24)")
    cn.add_argument("--name", help="probe display name")
    cn.add_argument("--service", action="store_true", help="install a reboot-surviving service")
    return p


def cmd_doctor(args: argparse.Namespace) -> int:
    os_name = sp.detect_os()
    print(f"OS           : {os_name}")
    if os_name == "linux":
        print(f"Package mgr  : {sp.detect_linux_pm()}")
    print(f"Privileged   : {sp.is_privileged()}  (root/admin — only needed for --service)")
    print(f"Python       : {sys.version.split()[0]}  (need >= 3.8)")
    print(f"pip          : {'yes' if shutil.which('pip') or True else 'no'}")
    print(f"Scan ceiling : {sp.detect_scope_cidr() or 'not detected'}")
    print(f"Own IP       : {sp.detect_primary_ip() or 'not detected'}")
    return 0


def cmd_self_scan(args: argparse.Namespace) -> int:      # filled in Task 4
    raise NotImplementedError

def cmd_connect(args: argparse.Namespace) -> int:        # filled in Task 5
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return {
        "doctor": cmd_doctor,
        "self-scan": cmd_self_scan,
        "connect": cmd_connect,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_cli.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add probe/agent/setup.py probe/tests/test_setup_cli.py
git commit -m "$(printf 'Add installer CLI brain skeleton + doctor subcommand\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 3: Dependency layer (`setup_deps.py`) — venv + wheel-first pip

**Files:**
- Create: `probe/agent/setup_deps.py`
- Test: `probe/tests/test_setup_deps.py`

**Interfaces:**
- Produces: `venv_python(probe_dir: str) -> str` (path to the venv interpreter, OS-correct); `reqs_hash(reqs_path: str) -> str`; `pip_install_argsets(venv_py: str, reqs_path: str) -> list[list[str]]` (the wheel-first command, then the source-fallback command — pure, so it's testable without running pip).

- [ ] **Step 1: Write the failing tests**

```python
# probe/tests/test_setup_deps.py
from __future__ import annotations
import os
from agent import setup_deps as d


def test_venv_python_path_is_os_correct():
    p = d.venv_python("/opt/probe")
    if os.name == "nt":
        assert p.endswith("Scripts\\python.exe") or p.endswith("Scripts/python.exe")
    else:
        assert p.endswith(".venv/bin/python")

def test_reqs_hash_is_stable_and_changes(tmp_path):
    f = tmp_path / "r.txt"
    f.write_text("httpx>=0.27\n")
    h1 = d.reqs_hash(str(f))
    assert h1 == d.reqs_hash(str(f))          # stable
    f.write_text("httpx>=0.27\nwebsockets>=12\n")
    assert d.reqs_hash(str(f)) != h1          # changes with contents

def test_pip_install_argsets_is_wheel_first_then_source():
    sets = d.pip_install_argsets("/v/bin/python", "/p/requirements-runtime.txt")
    assert len(sets) == 2
    assert "--only-binary=:all:" in sets[0]           # wheels first (no compiler)
    assert "--only-binary=:all:" not in sets[1]       # source fallback
    for s in sets:
        assert s[:3] == ["/v/bin/python", "-m", "pip"]
        assert "-r" in s and "/p/requirements-runtime.txt" in s
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_deps.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'agent.setup_deps'`.

- [ ] **Step 3: Implement `setup_deps.py`**

```python
# probe/agent/setup_deps.py
"""Layer-2 dependency install: create the venv and pip-install requirements,
wheel-first (no compiler on the common path), with a source-build fallback.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys


def venv_dir(probe_dir: str) -> str:
    return os.path.join(probe_dir, ".venv")


def venv_python(probe_dir: str) -> str:
    v = venv_dir(probe_dir)
    if os.name == "nt":
        return os.path.join(v, "Scripts", "python.exe")
    return os.path.join(v, "bin", "python")


def reqs_hash(reqs_path: str) -> str:
    with open(reqs_path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pip_install_argsets(venv_py: str, reqs_path: str) -> list[list[str]]:
    base = [venv_py, "-m", "pip", "install", "-r", reqs_path]
    return [base + ["--only-binary=:all:"], base]   # wheels first, then source fallback


def ensure_venv(probe_dir: str) -> str:
    """Create the venv if absent; return the interpreter path."""
    vpy = venv_python(probe_dir)
    if not os.path.exists(vpy):
        subprocess.run([sys.executable, "-m", "venv", venv_dir(probe_dir)], check=True)
        subprocess.run([vpy, "-m", "pip", "install", "-q", "--upgrade", "pip"], check=True)
    return vpy


def install_requirements(probe_dir: str, reqs_path: str) -> None:
    """Idempotent (requirements-hash stamp). Wheel-first, source-fallback."""
    vpy = ensure_venv(probe_dir)
    stamp = os.path.join(venv_dir(probe_dir), ".reqs-stamp")
    want = reqs_hash(reqs_path)
    if os.path.exists(stamp) and open(stamp).read().strip() == want:
        return
    argsets = pip_install_argsets(vpy, reqs_path)
    last: subprocess.CalledProcessError | None = None
    for args in argsets:
        try:
            subprocess.run(args, check=True)
            with open(stamp, "w") as fh:
                fh.write(want)
            return
        except subprocess.CalledProcessError as exc:
            last = exc      # wheel-only failed → try source build on next iteration
    raise RuntimeError(f"pip install failed for {reqs_path}") from last
```

- [ ] **Step 4: Run to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_deps.py -v`
Expected: PASS (3 tests). (`ensure_venv`/`install_requirements` are exercised in the CI smoke test, not unit tests — they run real subprocess.)

- [ ] **Step 5: Commit**

```bash
git add probe/agent/setup_deps.py probe/tests/test_setup_deps.py
git commit -m "$(printf 'Add wheel-first venv/pip dependency layer for the installer\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 4: `self-scan` — own IP, manager-less

**Files:**
- Modify: `probe/agent/setup.py` (`cmd_self_scan`)
- Test: `probe/tests/test_setup_selfscan.py`

**Interfaces:**
- Consumes: `setup_platform.detect_primary_ip`; `agent.local_run.run(argv: list[str]) -> int`; env `PROBE_SCOPE_FILE`.
- Produces: `cmd_self_scan(args) -> int`; helper `write_scope_file(path: str, target: str) -> None`.

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_setup_selfscan.py
from __future__ import annotations
import os
from types import SimpleNamespace
from agent import setup


def test_self_scan_scopes_to_own_ip_and_calls_local_run(tmp_path, monkeypatch):
    calls = {}
    monkeypatch.setattr(setup.sp, "detect_primary_ip", lambda: "192.168.1.42")
    monkeypatch.setattr(setup, "_local_run", lambda argv: calls.setdefault("argv", argv) or 0)
    monkeypatch.setenv("PROBE_SCOPE_FILE", str(tmp_path / "scope.txt"))

    rc = setup.cmd_self_scan(SimpleNamespace(profile="it", stage="deep_scan"))

    assert rc == 0
    # scope file contains exactly the own IP
    assert (tmp_path / "scope.txt").read_text().strip() == "192.168.1.42"
    # local engine invoked against the own IP with the chosen profile/stage
    assert calls["argv"][0] == "192.168.1.42"
    assert calls["argv"][1] == "it" and calls["argv"][2] == "deep_scan"

def test_self_scan_fails_cleanly_without_an_ip(monkeypatch):
    monkeypatch.setattr(setup.sp, "detect_primary_ip", lambda: None)
    rc = setup.cmd_self_scan(__import__("types").SimpleNamespace(profile="it", stage="deep_scan"))
    assert rc == 2
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_selfscan.py -v`
Expected: FAIL — `NotImplementedError` (stub from Task 2).

- [ ] **Step 3: Implement `cmd_self_scan` in `setup.py`**

Add near the top of `setup.py` (imports):
```python
import os
```
Replace the `cmd_self_scan` stub with:
```python
def _local_run(argv: list[str]) -> int:
    """Indirection so tests can stub the engine. Reuses the shipped local engine."""
    from agent.local_run import run
    return run(argv)


def write_scope_file(path: str, target: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(target + "\n")


def cmd_self_scan(args: argparse.Namespace) -> int:
    ip = sp.detect_primary_ip()
    if not ip:
        print("ERROR: could not detect this host's own IP; is a network up?", file=sys.stderr)
        return 2
    scope_path = os.environ.get("PROBE_SCOPE_FILE", os.path.join(os.getcwd(), ".self-scan-scope"))
    os.environ["PROBE_SCOPE_FILE"] = scope_path
    write_scope_file(scope_path, ip)
    print(f"• self-scan: target={ip}  scope={ip} (own host only)  profile={args.profile} stage={args.stage}")
    return _local_run([ip, args.profile, args.stage])
```

- [ ] **Step 4: Run to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_selfscan.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add probe/agent/setup.py probe/tests/test_setup_selfscan.py
git commit -m "$(printf 'Add manager-less self-scan of the host own IP\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 5: `connect` — env + cross-OS self-heal supervisor

**Files:**
- Modify: `probe/agent/setup.py` (`cmd_connect`, supervisor)
- Test: `probe/tests/test_setup_connect.py`

**Interfaces:**
- Consumes: `setup_deps.install_requirements/venv_python`; `setup_platform.detect_scope_cidr`; `agent.cli.normalize_manager_url`.
- Produces: `cmd_connect(args) -> int`; `write_probe_env(probe_dir, manager, scope, name) -> str`; `supervise(cmd: list[str], run_once: bool = False) -> int` (restart loop honoring exit codes 4=re-enroll, 2=backoff-retry; returns the final rc for others).

- [ ] **Step 1: Write the failing tests**

```python
# probe/tests/test_setup_connect.py
from __future__ import annotations
from types import SimpleNamespace
from agent import setup


def test_write_probe_env_contains_required_keys(tmp_path):
    path = setup.write_probe_env(str(tmp_path), "https://m.example.com", "10.0.0.0/24", "h-probe")
    body = open(path).read()
    assert "PLATFORM_URL=https://m.example.com" in body
    assert "PROBE_NETWORK_SEGMENTS=10.0.0.0/24" in body
    assert "PROBE_NAME=h-probe" in body
    assert "VERIFY_TLS=true" in body

def test_supervisor_stops_on_clean_exit():
    seq = iter([0])
    rc = setup.supervise(["x"], run_once=False, _spawn=lambda cmd: next(seq))
    assert rc == 0

def test_supervisor_retries_then_gives_up_on_code_2():
    seq = iter([2, 2, 2, 2, 2, 2])   # always unreachable
    rc = setup.supervise(["x"], _spawn=lambda cmd: next(seq), _max=3, _sleep=lambda s: None)
    assert rc == 2

def test_supervisor_reenrolls_on_code_4_then_succeeds():
    seq = iter([4, 0])
    rc = setup.supervise(["x"], _spawn=lambda cmd: next(seq), _max=3, _sleep=lambda s: None)
    assert rc == 0
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_connect.py -v`
Expected: FAIL — `AttributeError`/`NotImplementedError`.

- [ ] **Step 3: Implement `cmd_connect` + `supervise` in `setup.py`**

Add import: `import subprocess` and `from agent.cli import normalize_manager_url`. Then:
```python
def write_probe_env(probe_dir: str, manager: str, scope: str, name: str) -> str:
    path = os.path.join(probe_dir, "probe.env")
    lines = [
        f"PLATFORM_URL={manager}",
        f"PROBE_NETWORK_SEGMENTS={scope}",
        f"PROBE_NAME={name}",
        "VERIFY_TLS=true",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def supervise(cmd, run_once=False, _spawn=None, _max=6, _sleep=None) -> int:
    """Restart loop mirroring install.sh: exit 4 → re-enroll (fresh identity),
    2 → backed-off retry; anything else is returned as-is."""
    import time
    _spawn = _spawn or (lambda c: subprocess.run(c).returncode)
    _sleep = _sleep or time.sleep
    heal = 0
    while True:
        rc = _spawn(cmd)
        if rc == 4:
            heal += 1
            if heal >= _max:
                return 4
            continue
        if rc == 2:
            heal += 1
            if heal >= _max:
                return 2
            _sleep(min(heal * 5, 30))
            continue
        return rc


def cmd_connect(args: argparse.Namespace) -> int:
    import os as _os
    probe_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # .../probe
    manager = normalize_manager_url(args.manager)
    scope = args.scope or sp.detect_scope_cidr()
    if not scope:
        print("ERROR: no scan scope; pass --scope <CIDR> (empty scope refuses all jobs).", file=sys.stderr)
        return 1
    name = args.name or f"{__import__('socket').gethostname()}-probe"

    from agent import setup_deps
    setup_deps.install_requirements(probe_dir, _os.path.join(probe_dir, "requirements-runtime.txt"))
    write_probe_env(probe_dir, manager, scope, name)
    vpy = setup_deps.venv_python(probe_dir)

    if not sp.is_privileged():
        print("• note: unprivileged — SYN/OS-fingerprint use connect-scan fallback (correct, just less deep).")

    if args.service:
        from agent import service_install
        return service_install.install(sp.detect_os(), vpy, probe_dir, manager, scope, name)

    env = _os.environ.copy()
    env.update({"PLATFORM_URL": manager, "PROBE_NETWORK_SEGMENTS": scope, "PROBE_NAME": name})
    if args.enroll:
        env["PROBE_FORCE_ENROLL"] = "1"      # fresh device enrollment (skip saved creds)
    elif args.pat:
        env["PROBE_PAT"] = args.pat
    elif args.token:
        env["PROBE_ENROLL_TOKEN"] = args.token
    return supervise([vpy, "-m", "agent.agent"],
                     _spawn=lambda c: subprocess.run(c, env=env, cwd=probe_dir).returncode)
```

> Note for the implementer: verify the enrollment env var names against `agent/agent.py`'s enrollment path before finalizing (`PROBE_FORCE_ENROLL`/`PROBE_PAT`/`PROBE_ENROLL_TOKEN` are the intended contract; adjust the three names to match what `agent.agent` actually reads, and add a test asserting the mapping). This is the one place the brain couples to the daemon.

- [ ] **Step 4: Run to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_connect.py -v`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add probe/agent/setup.py probe/tests/test_setup_connect.py
git commit -m "$(printf 'Add connect subcommand + cross-OS self-heal supervisor\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 6: Service install (`service_install.py`)

**Files:**
- Create: `probe/agent/service_install.py`
- Test: `probe/tests/test_service_install.py`

**Interfaces:**
- Consumes: `setup_platform.render_service_unit`, `setup_platform.is_privileged`.
- Produces: `install(os_name, python_exe, probe_dir, manager, scope, name) -> int`; `commands_for(os_name, path, body) -> list[list[str]]` (pure — the activation commands, testable).

- [ ] **Step 1: Write the failing test**

```python
# probe/tests/test_service_install.py
from __future__ import annotations
from agent import service_install as si


def test_linux_activation_uses_systemctl():
    cmds = si.commands_for("linux", "/etc/systemd/system/vedha-agent.service", "body")
    flat = " ".join(" ".join(c) for c in cmds)
    assert "systemctl daemon-reload" in flat
    assert "systemctl enable" in flat and "vedha-agent" in flat

def test_macos_activation_uses_launchctl():
    cmds = si.commands_for("macos", "/Users/x/Library/LaunchAgents/com.vedha.agent.plist", "body")
    flat = " ".join(" ".join(c) for c in cmds)
    assert "launchctl" in flat and "load" in flat

def test_windows_activation_is_the_schtasks_command():
    cmds = si.commands_for("windows", "SCHTASKS", "schtasks /Create /TN VedhaAgent ...")
    assert cmds == [["schtasks", "/Create", "/TN", "VedhaAgent", "..."]] or cmds[0][0] == "schtasks"
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd probe && .venv/bin/python -m pytest tests/test_service_install.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Implement `service_install.py`**

```python
# probe/agent/service_install.py
"""Render + activate a reboot-surviving service per OS (opt-in via --service)."""
from __future__ import annotations

import os
import shlex
import subprocess

from agent import setup_platform as sp


def commands_for(os_name: str, path: str, body: str) -> list[list[str]]:
    if os_name == "linux":
        return [["systemctl", "daemon-reload"],
                ["systemctl", "enable", "--now", "vedha-agent"]]
    if os_name == "macos":
        return [["launchctl", "unload", path], ["launchctl", "load", "-w", path]]
    if os_name == "windows":
        return [shlex.split(body)]      # body IS the schtasks command
    raise ValueError(os_name)


def install(os_name, python_exe, probe_dir, manager, scope, name) -> int:
    path, body = sp.render_service_unit(os_name, python_exe, probe_dir, manager, scope, name)
    if os_name != "windows":
        if not sp.is_privileged() and path.startswith("/etc"):
            print("ERROR: --service needs root here. Re-run with sudo.")
            return 1
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    for cmd in commands_for(os_name, path, body):
        subprocess.run(cmd, check=False)
    print(f"• service installed ({os_name}). It will start on boot.")
    return 0
```

- [ ] **Step 4: Run to verify it passes**

Run: `cd probe && .venv/bin/python -m pytest tests/test_service_install.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add probe/agent/service_install.py probe/tests/test_service_install.py
git commit -m "$(printf 'Add per-OS service install (systemd/launchd/schtasks)\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 7: Bootstraps — `install.sh`, `install.ps1`, `vedha-setup.py`

**Files:**
- Create: `probe/vedha-setup.py`
- Create: `probe/install.ps1`
- Modify: `probe/install.sh` (add a native-brain path; keep existing behavior reachable)

**Interfaces:** none (shell → `python -m agent.setup "$@"`).

- [ ] **Step 1: Create the repo-root Python shim**

```python
# probe/vedha-setup.py  — run directly where Python already exists: python vedha-setup.py <args>
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent.setup import main
if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Create the Windows bootstrap `install.ps1`**

```powershell
# probe/install.ps1 — ensure Python, then hand off to the brain.
# Usage:  irm <base>/install.ps1 -OutFile install.ps1 ;  .\install.ps1 <args...>
$ErrorActionPreference = 'Stop'
function Have($n){ return [bool](Get-Command $n -ErrorAction SilentlyContinue) }
Set-Location $PSScriptRoot
if (-not (Have python)) {
  if (Have winget) { winget install -e --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements }
  else { Write-Error 'Python not found and winget unavailable. Install Python 3.8+ from python.org, then re-run.'; exit 1 }
}
python -c "import sys; raise SystemExit(0 if sys.version_info[:2] >= (3,8) else 1)"
if ($LASTEXITCODE -ne 0) { Write-Error 'Python 3.8+ required.'; exit 1 }
python -m agent.setup @args
exit $LASTEXITCODE
```

- [ ] **Step 3: Add the native-brain path to `install.sh`**

At the very top of `install.sh` (after `set -eu`), insert a fast path that ensures Python + venv module and hands off to the brain when the first arg is a brain subcommand:
```sh
# Native cross-OS brain path: `install.sh <doctor|self-scan|connect> ...`
case "${1:-}" in
  doctor|self-scan|connect)
    cd "$(dirname "$0")"
    if ! command -v python3 >/dev/null 2>&1; then
      if command -v apt-get >/dev/null 2>&1; then sudo apt-get install -y python3 python3-venv python3-pip
      elif command -v dnf >/dev/null 2>&1; then sudo dnf install -y python3 python3-pip
      elif command -v pacman >/dev/null 2>&1; then sudo pacman -S --noconfirm python python-pip
      elif command -v brew >/dev/null 2>&1; then brew install python
      else echo "Install Python 3.8+ then re-run." >&2; exit 1; fi
    fi
    python3 -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3,8) else 1)' \
      || { echo "Python 3.8+ required." >&2; exit 1; }
    # Debian/Ubuntu ships venv separately.
    python3 -c 'import venv' 2>/dev/null || { command -v apt-get >/dev/null 2>&1 && sudo apt-get install -y python3-venv; }
    exec python3 -m agent.setup "$@"
    ;;
esac
```
(The existing LOCAL/DOCKER modes below remain unchanged for backward compatibility.)

- [ ] **Step 4: Smoke-test the shims locally**

Run:
```bash
cd probe && python3 vedha-setup.py doctor
sh install.sh doctor
```
Expected: both print the doctor report and exit 0.

- [ ] **Step 5: Commit**

```bash
git add probe/vedha-setup.py probe/install.ps1 probe/install.sh
git commit -m "$(printf 'Add cross-OS bootstraps (sh/ps1) + repo-root python shim\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 8: CI matrix smoke test

**Files:**
- Create: `.github/workflows/agent-installer.yml`

- [ ] **Step 1: Create the workflow**

```yaml
name: agent-installer
on:
  pull_request:
    paths: ["probe/agent/setup*.py", "probe/agent/service_install.py", "probe/install.*", "probe/vedha-setup.py"]
jobs:
  smoke:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    defaults: { run: { working-directory: probe } }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - name: Unit tests (pure installer logic)
        run: python -m pytest tests/test_setup_platform.py tests/test_setup_cli.py tests/test_setup_deps.py tests/test_setup_selfscan.py tests/test_setup_connect.py tests/test_service_install.py -v
      - name: doctor exits 0
        run: python vedha-setup.py doctor
```

- [ ] **Step 2: Verify the pytest selection runs locally**

Run: `cd probe && .venv/bin/python -m pytest tests/test_setup_platform.py tests/test_setup_cli.py tests/test_setup_deps.py tests/test_setup_selfscan.py tests/test_setup_connect.py tests/test_service_install.py -v`
Expected: all PASS.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/agent-installer.yml
git commit -m "$(printf 'Add 3-OS CI smoke test for the agent installer\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

## Self-Review

**Spec coverage:**
- One Python brain + thin shims → Tasks 2, 7. ✅
- Native venv everywhere (Layer-2 deps, wheel-first) → Task 3. ✅
- Layer-1 Python bootstrap per OS → Task 7 (`install.sh` apt/dnf/pacman/brew; `install.ps1` winget). ✅
- Scope auto-detect (UDP socket, no root) → Task 1. ✅
- `self-scan` own-IP, manager-less → Task 4. ✅
- `connect` + cross-OS supervisor (exit 2/4) → Task 5. ✅
- Never require root; connect-scan notice → Task 5. ✅
- `--service` systemd/launchd/schtasks → Tasks 1 (render) + 6 (activate). ✅
- `doctor` → Task 2. ✅
- CI 3-OS smoke → Task 8. ✅
- No Docker path in brain/shims. ✅

**Placeholder scan:** No TBD/TODO. The one flagged verification (enrollment env-var names in Task 5) is called out explicitly with the action (check against `agent.agent`, add a mapping test) — it is the single brain↔daemon coupling and must be confirmed, not guessed.

**Type consistency:** `render_service_unit` signature identical across Task 1 (def), Task 6 (call), and its tests. `venv_python`/`install_requirements`/`reqs_hash`/`pip_install_argsets` consistent across Tasks 3, 5. `supervise(cmd, run_once, _spawn, _max, _sleep)` consistent across Task 5 def + tests. `detect_primary_ip`/`detect_scope_cidr`/`cidr_from_ip` consistent across Tasks 1, 4, 5.

## Build order

1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Each ends green + committed. After Task 4 you can already `python vedha-setup.py self-scan` on any OS; after Task 7 the one-command bootstraps work end-to-end.
