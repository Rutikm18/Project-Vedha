#!/usr/bin/env python3
"""
probe_local_run.py — thin dev wrapper.

The local-run driver now SHIPS inside the probe as `agent/local_run.py` and is a
first-class subcommand of the production entrypoint:

    python -m agent.agent local-run <target> [profile] [stage] [service_filter]

This wrapper is kept so the documented dev invocation still works from a checkout:

    export PYTHONPATH="$PWD"
    echo "192.168.1.0/24" > /tmp/s.txt          # scope allowlist (must contain the target)
    .venv/bin/python3 tools/probe_local_run.py <target> [profile] [stage] [service_filter]

All logic (arg validation, PROBE_LOCAL_PORTS, proto/state port labels, the JSON
summary) lives in agent/local_run.py — single source of truth.
"""
import sys

from agent.local_run import run

if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
