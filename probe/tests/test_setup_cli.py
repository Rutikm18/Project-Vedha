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
