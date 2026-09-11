"""setup.py — the brain CLI that ties the hardened components together.

Subcommands (all built + unit-tested in earlier phases):
  doctor     — real pass/warn/fail diagnosis (Phase 2)
  config     — `config --effective` prints each value + its winning source (Phase 2)
  self-scan  — scan THIS host's own IP, no Manager (Phase 5)
  connect    — OPTIONAL: enroll + run the daemon under the supervisor (Phase 6)

Global `--strict` / `--insecure` select the security mode (Phase 7). Strict is
available now but permissive is the initial-phase default (verify-and-warn).
"""
from __future__ import annotations

import argparse
import ctypes
import os
import sys

from agent import bootstrap, config_model, deps, doctor

PROBE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../probe


def _is_privileged() -> bool:
    if os.name == "posix":
        return os.geteuid() == 0  # type: ignore[attr-defined]
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore[attr-defined]
    except Exception:
        return False


def _state_dir() -> str:
    sf = os.environ.get("STATE_FILE")
    if sf:
        return os.path.dirname(sf) or "."
    return os.path.join(os.path.expanduser("~"), "vedha-agent")


def _probe_env() -> dict:
    path = os.path.join(PROBE_DIR, "probe.env")
    try:
        with open(path, encoding="utf-8") as fh:
            return config_model.parse_env_file(fh.read())
    except OSError:
        return {}


def _resolved(cli: dict) -> tuple[dict, dict]:
    return config_model.resolve(cli=cli, env=dict(os.environ), probe_env=_probe_env(), pushed={})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vedha", description="Vedha agent")
    p.add_argument("--strict", action="store_true", help="strict security: fail-closed verification")
    p.add_argument("--insecure", action="store_true", help="skip strict verification (initial phase)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    cf = sub.add_parser("config")
    cf.add_argument("--effective", action="store_true", default=True)
    ss = sub.add_parser("self-scan")
    ss.add_argument("--profile", default="it", choices=["it", "iot"])
    ss.add_argument("--stage", default="deep_scan")
    cn = sub.add_parser("connect")
    cn.add_argument("--manager", required=True)
    cn.add_argument("--name")
    g = cn.add_mutually_exclusive_group()
    g.add_argument("--pat")
    g.add_argument("--token")
    return p


def cmd_doctor(_args) -> int:
    values, _ = _resolved({})
    checks = doctor.run(str(values.get("manager_url", "")), _is_privileged(), _state_dir())
    print(doctor.format_report(checks))
    return doctor.exit_code(checks)


def cmd_config(_args) -> int:
    values, sources = _resolved({})
    for field, value, src in config_model.render_effective(values, sources):
        print(f"{field:<20} {str(value)!r:<28} [{src}]")
    return 0


def cmd_self_scan(args) -> int:
    from agent import self_scan
    return self_scan.run(profile=args.profile, stage=args.stage, state_dir=_state_dir())


def cmd_connect(args) -> int:
    from agent import connect
    mode = bootstrap.security_mode(args.strict, args.insecure)
    values, _ = _resolved({"manager_url": args.manager, "name": args.name})
    reqs = os.path.join(PROBE_DIR, "requirements-runtime.txt")
    if os.path.exists(reqs):
        deps.install_requirements(PROBE_DIR, reqs, strict=(mode == "strict"))
    enroll = "pat" if args.pat else "token" if args.token else "pairing"
    return connect.run(values, mode=enroll, pat=args.pat, token=args.token, state_dir=_state_dir())


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    # thread the security mode down (connect reads args.strict/insecure directly)
    return {
        "doctor": cmd_doctor,
        "config": cmd_config,
        "self-scan": cmd_self_scan,
        "connect": cmd_connect,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
