"""self_scan.py — scan THIS host's own IP, no Manager (Phase 5).

Assembles the scope model (Phase 1) and the durable queue (Phase 4): detect the
host's own IPv4, refuse inside a container/WSL2 namespace or when the IP is on
the permanent denylist, scope to that single host, run the existing local engine
(`agent.local_run`), and archive a run summary through the durable queue. Safe by
construction — it can only ever target the machine it runs on.
"""
from __future__ import annotations

import os
import socket
import sys
import time
from dataclasses import dataclass

from agent import scope_model as sm


@dataclass
class SelfScanPlan:
    target: str
    scope: list[sm.Segment]
    scope_file_line: str
    profile: str
    stage: str


def plan_self_scan(primary_ip: str | None, container: str | None,
                   profile: str = "it", stage: str = "deep_scan"
                   ) -> tuple[SelfScanPlan | None, str]:
    """Pure decision. Returns (plan, reason); reason is non-empty on refusal."""
    refusal = sm.refusal_reason(container)
    if refusal:
        return None, refusal
    if not primary_ip:
        return None, sm.ipv6_scope_note(None) or "no own IPv4 detected on this host"
    if sm.is_denied(primary_ip):
        return None, "own IP is on the permanent denylist; nothing to scan"
    seg = sm.Segment(cidr=f"{primary_ip}/32", type="IT", profile=profile, site="self")
    return SelfScanPlan(target=primary_ip, scope=[seg], scope_file_line=primary_ip,
                        profile=profile, stage=stage), ""


def execute(plan: SelfScanPlan, scope_file_path: str, *, engine_run, queue=None,
            now=time.time) -> int:
    """Write the own-IP scope file, run the engine, archive the summary."""
    with open(scope_file_path, "w", encoding="utf-8") as fh:
        fh.write(plan.scope_file_line + "\n")
    os.environ["PROBE_SCOPE_FILE"] = scope_file_path
    rc = engine_run([plan.target, plan.profile, plan.stage])
    if queue is not None:
        job_id = f"self-{plan.target}-{int(now())}"
        queue.enqueue(job_id, {"kind": "self-scan", "target": plan.target,
                               "profile": plan.profile, "stage": plan.stage, "rc": rc})
    return rc


def run_from(primary_ip: str | None, container: str | None, scope_file_path: str, *,
             engine_run, queue=None, now=time.time,
             profile: str = "it", stage: str = "deep_scan") -> int:
    plan, reason = plan_self_scan(primary_ip, container, profile, stage)
    if plan is None:
        print(f"self-scan refused: {reason}", file=sys.stderr)
        return 20  # fatal-config class (see exit_state)
    return execute(plan, scope_file_path, engine_run=engine_run, queue=queue, now=now)


# ── real IO wiring (not unit-tested; exercised by the CI smoke) ──────────────
def primary_ipv4() -> str | None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("1.1.1.1", 80))
        ip = s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()
    return ip if ip and not ip.startswith("127.") and ip.count(".") == 3 else None


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def detect_host_container() -> str | None:
    return sm.detect_container(
        dockerenv_exists=os.path.exists("/.dockerenv"),
        cgroup_text=_read("/proc/1/cgroup"),
        proc_version=_read("/proc/version"),
    )


def run(profile: str = "it", stage: str = "deep_scan", state_dir: str = ".") -> int:
    from agent.local_run import run as engine
    queue = None
    try:
        from agent.result_queue import ResultQueue, host_sealed_cipher
        queue = ResultQueue(state_dir, cipher=host_sealed_cipher(state_dir))
    except Exception:
        queue = None  # archiving is best-effort; the engine writes its own local archive
    scope_file = os.path.join(state_dir, ".self-scan-scope")
    return run_from(primary_ipv4(), detect_host_container(), scope_file,
                    engine_run=engine, queue=queue, profile=profile, stage=stage)


def main(argv: list[str] | None = None) -> int:
    """Runnable entry: `python -m agent.self_scan [--profile it|iot] [--stage …]`.
    The brain CLI (later) delegates to `run()`; this is the standalone convenience."""
    import argparse
    p = argparse.ArgumentParser(prog="vedha self-scan",
                                description="Scan only this host's own IP (no Manager).")
    p.add_argument("--profile", default="it", choices=["it", "iot"])
    p.add_argument("--stage", default="deep_scan")
    p.add_argument("--state-dir", default=".")
    a = p.parse_args(argv)
    return run(profile=a.profile, stage=a.stage, state_dir=a.state_dir)


if __name__ == "__main__":
    raise SystemExit(main())
