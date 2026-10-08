"""Phase 7 — brain CLI: parser wiring + doctor runs. No network required for the
parser tests; doctor's connectivity check tolerates an unset manager."""
from __future__ import annotations

from agent import setup


def test_parser_accepts_all_subcommands():
    p = setup.build_parser()
    assert p.parse_args(["doctor"]).cmd == "doctor"
    assert p.parse_args(["config"]).cmd == "config"
    assert p.parse_args(["self-scan"]).cmd == "self-scan"
    assert p.parse_args(["connect", "--manager", "https://m"]).cmd == "connect"


def test_strict_and_insecure_flags_parse():
    ns = setup.build_parser().parse_args(["--strict", "doctor"])
    assert ns.strict is True and ns.insecure is False
    ns2 = setup.build_parser().parse_args(["--insecure", "self-scan"])
    assert ns2.insecure is True


def test_connect_requires_manager():
    try:
        setup.build_parser().parse_args(["connect"])
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code != 0


def test_doctor_command_returns_int_and_reports(capsys):
    rc = setup.cmd_doctor(object())
    out = capsys.readouterr().out.lower()
    assert isinstance(rc, int)
    assert "python" in out and "privilege" in out


def test_doctor_survives_a_cp1252_console():
    """`python -m agent.setup doctor` crashed on windows-latest: its report contains an arrow
    that a cp1252 console cannot encode. The output must degrade, never raise."""
    import os
    import subprocess
    import sys
    from pathlib import Path
    probe = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": str(probe), "PYTHONIOENCODING": "cp1252"}
    for k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        env.pop(k, None)
    out = subprocess.run([sys.executable, "-m", "agent.setup", "doctor"], cwd=str(probe), env=env,
                         capture_output=True, text=True, timeout=60)
    assert "UnicodeEncodeError" not in out.stderr and "Traceback" not in out.stderr, out.stderr[-600:]
