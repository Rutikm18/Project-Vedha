"""service.py — per-OS service install with restart limits (Phase 9).

The unit is rendered FROM the resolved config object (no third hardcoded copy →
no config drift), and it delegates supervision to the OS service manager with a
HARD restart cap (systemd StartLimitBurst / launchd throttle+KeepAlive-on-failure
/ Windows task). The cap is what stops the infinite self-heal an EDR reads as
malware — a deliberate stop is respected.
"""
from __future__ import annotations

import os
import shlex
import subprocess

_SYSTEMD = """\
[Unit]
Description=Vedha Agent (probe)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec={interval}
StartLimitBurst={burst}

[Service]
Type=simple
WorkingDirectory={probe_dir}
StateDirectory=vedha-agent
Environment=PLATFORM_URL={manager}
Environment=PROBE_NETWORK_SEGMENTS={scope}
Environment=PROBE_NAME={name}
Environment=VERIFY_TLS=true
ExecStart={python} -m agent.agent
Restart=on-failure
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
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><dict><key>SuccessfulExit</key><false/></dict>
  <key>ThrottleInterval</key><integer>10</integer>
</dict></plist>
"""


def render_unit(os_name: str, values: dict, python_exe: str, probe_dir: str,
                state_dir: str, *, start_limit_burst: int = 5,
                start_limit_interval_s: int = 300) -> tuple[str, str]:
    """Return (target_path, body). Windows returns ('SCHTASKS', command_string)."""
    manager = values.get("manager_url", "")
    name = values.get("name", "")
    scope = values.get("scope", "")
    if os_name == "linux":
        body = _SYSTEMD.format(python=python_exe, probe_dir=probe_dir, manager=manager,
                               scope=scope, name=name, burst=start_limit_burst,
                               interval=start_limit_interval_s)
        return "/etc/systemd/system/vedha-agent.service", body
    if os_name == "macos":
        body = _LAUNCHD.format(python=python_exe, probe_dir=probe_dir, manager=manager,
                               scope=scope, name=name)
        return os.path.expanduser("~/Library/LaunchAgents/com.vedha.agent.plist"), body
    if os_name == "windows":
        cmd = (
            'schtasks /Create /TN VedhaAgent /SC ONSTART /RU SYSTEM /RL HIGHEST /F '
            f'/TR "\\"{python_exe}\\" -m agent.agent"'
        )
        return "SCHTASKS", cmd
    raise ValueError(f"unsupported os for service: {os_name!r}")


def commands_for(os_name: str, path: str, body: str) -> list[list[str]]:
    if os_name == "linux":
        return [["systemctl", "daemon-reload"],
                ["systemctl", "enable", "--now", "vedha-agent"]]
    if os_name == "macos":
        return [["launchctl", "unload", path], ["launchctl", "load", "-w", path]]
    if os_name == "windows":
        return [shlex.split(body)]
    raise ValueError(os_name)


def uninstall_commands(os_name: str, path: str) -> list[list[str]]:
    if os_name == "linux":
        return [["systemctl", "disable", "--now", "vedha-agent"], ["rm", "-f", path]]
    if os_name == "macos":
        return [["launchctl", "unload", path], ["rm", "-f", path]]
    if os_name == "windows":
        return [["schtasks", "/Delete", "/TN", "VedhaAgent", "/F"]]
    raise ValueError(os_name)


def _default_runner(cmd: list[str]) -> int:
    return subprocess.run(cmd, check=False).returncode


def install(os_name: str, values: dict, python_exe: str, probe_dir: str, state_dir: str, *,
            runner=_default_runner, path_override: str | None = None) -> int:
    path, body = render_unit(os_name, values, python_exe, probe_dir, state_dir)
    target = path_override or path
    if os_name != "windows":
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(body)
    for cmd in commands_for(os_name, target, body):
        runner(cmd)
    return 0


def uninstall(os_name: str, path: str, *, runner=_default_runner) -> int:
    for cmd in uninstall_commands(os_name, path):
        runner(cmd)
    if os_name != "windows" and path != "SCHTASKS" and os.path.exists(path):
        os.remove(path)
    return 0
