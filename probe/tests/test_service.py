"""Phase 9 — per-OS service install: units rendered FROM the config object, with
restart limits (deliberate-stop respected), and a working uninstall. Pure render
+ command generation; install/uninstall round-trip via an injected runner."""
from __future__ import annotations

from agent import service as svc

VALUES = {"manager_url": "https://m.example.com", "name": "host-probe", "scope": "10.20.0.0/24"}


# ── render (pure) ────────────────────────────────────────────────────────────
def test_systemd_unit_has_limits_env_and_statedir():
    path, body = svc.render_unit("linux", VALUES, "/opt/p/.venv/bin/python", "/opt/p", "/var/lib/vedha-agent")
    assert path.endswith("/vedha-agent.service")
    assert "ExecStart=/opt/p/.venv/bin/python -m agent.agent" in body
    assert "Restart=on-failure" in body
    assert "StartLimitBurst=" in body and "StartLimitIntervalSec=" in body   # not infinite self-heal
    assert "StateDirectory=vedha-agent" in body
    assert "PLATFORM_URL=https://m.example.com" in body
    assert "PROBE_NETWORK_SEGMENTS=10.20.0.0/24" in body


def test_launchd_plist_restart_on_failure_only():
    path, body = svc.render_unit("macos", VALUES, "/opt/p/.venv/bin/python", "/opt/p", "/x")
    assert path.endswith("com.vedha.agent.plist")
    assert "<key>KeepAlive</key>" in body and "SuccessfulExit" in body   # restart only on failure
    assert "ThrottleInterval" in body                                     # throttle, not a busy loop
    assert "agent.agent" in body


def test_windows_task_is_a_schtasks_command():
    path, body = svc.render_unit("windows", VALUES, r"C:\p\.venv\Scripts\python.exe", r"C:\p", r"C:\state")
    assert path == "SCHTASKS"
    assert "schtasks" in body.lower() and "VedhaAgent" in body and "agent.agent" in body


# ── activation / uninstall commands (pure, mirror each other) ────────────────
def test_activation_commands_per_os():
    assert any("daemon-reload" in " ".join(c) for c in svc.commands_for("linux", "/e/vedha-agent.service", "b"))
    assert any("enable" in " ".join(c) for c in svc.commands_for("linux", "/e/x", "b"))
    assert any("load" in " ".join(c) for c in svc.commands_for("macos", "/p.plist", "b"))
    assert svc.commands_for("windows", "SCHTASKS", "schtasks /Create /TN VedhaAgent")[0][0] == "schtasks"


def test_uninstall_commands_per_os():
    assert any("disable" in " ".join(c) for c in svc.uninstall_commands("linux", "/e/vedha-agent.service"))
    assert any("unload" in " ".join(c) for c in svc.uninstall_commands("macos", "/p.plist"))
    assert any("/Delete" in " ".join(c) for c in svc.uninstall_commands("windows", "SCHTASKS"))


# ── install/uninstall file round-trip (injected runner) ──────────────────────
def test_install_writes_unit_then_uninstall_removes_it(tmp_path):
    calls = []
    runner = lambda cmd: calls.append(cmd) or 0
    unit = tmp_path / "vedha-agent.service"

    rc = svc.install("linux", VALUES, "/py", "/probe", "/state",
                     runner=runner, path_override=str(unit))
    assert rc == 0 and unit.exists()
    assert any("daemon-reload" in " ".join(c) for c in calls)

    rc2 = svc.uninstall("linux", str(unit), runner=runner)
    assert rc2 == 0 and not unit.exists()
    assert any("disable" in " ".join(c) for c in calls)
