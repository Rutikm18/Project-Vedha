"""connect.py — OPTIONAL Manager mode + uplink security (Phase 6).

The agent is fully usable without ever connecting (see self_scan). `connect` is
the opt-in mode that enrolls with a Manager and runs the daemon. It adds the
security the review requires: the agent verifies every job's Ed25519 signature
against a PINNED key and then re-checks each target against its OWN typed scope
(a signed job can only ever request a subset — never widen scope), and it honors
a local kill switch.

Enrollment env mapping is VERIFIED against agent/agent.py, not guessed:
  - PAT   → OPERATOR_TOKEN / PROBE_PAT / VEDHA_PAT   (daemon reads VEDHA_PAT)
  - token → PROBE_ENROLL_TOKEN                        (daemon: _enroll_device)
  - pairing → set neither; the daemon device-enrolls and prints the pairing code
"""
from __future__ import annotations

import base64
import json
import os

from agent import scope_model as sm
from agent.exit_state import CONTRACT_VERSION


def connect_env(mode: str, pat: str | None, token: str | None, base: dict) -> dict:
    env = dict(base)
    if mode == "pat" and pat:
        env["VEDHA_PAT"] = pat
    elif mode == "token" and token:
        env["PROBE_ENROLL_TOKEN"] = token
    # pairing: set no credential env — the daemon device-enrolls + prints a code
    return env


def canonical_job_bytes(job: dict) -> bytes:
    """Deterministic bytes the Manager signs and the agent verifies (sig excluded)."""
    payload = {k: v for k, v in job.items() if k != "sig"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def verify_job(job: dict, pinned_pub_b64: str, now: float) -> tuple[bool, str]:
    """Verify contract version, Ed25519 signature (pinned key), and validity window."""
    if job.get("contract_version") != CONTRACT_VERSION:
        return False, f"contract version mismatch: {job.get('contract_version')} != {CONTRACT_VERSION}"
    sig_b64 = job.get("sig")
    if not sig_b64:
        return False, "missing signature"
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(pinned_pub_b64))
        pub.verify(base64.b64decode(sig_b64), canonical_job_bytes(job))
    except InvalidSignature:
        return False, "signature verification failed"
    except Exception as exc:  # malformed key/sig
        return False, f"signature verification error: {exc}"
    nb, ex = job.get("not_before"), job.get("expires")
    if nb is not None and now < float(nb):
        return False, "job not yet valid (not_before)"
    if ex is not None and now > float(ex):
        return False, "job expired"
    return True, ""


def admit_job(job: dict, pinned_pub_b64: str, segments: list[sm.Segment],
              now: float, manager_ip: str | None = None) -> tuple[bool, str]:
    """The independent ceiling: a job is admitted only if it is validly signed AND
    every target falls inside the agent's own active IT/IoT scope."""
    ok, reason = verify_job(job, pinned_pub_b64, now)
    if not ok:
        return False, reason
    targets = job.get("targets") or []
    if not targets:
        return False, "job has no targets"
    for t in targets:
        allowed, why = sm.target_allowed(t, segments, manager_ip)
        if not allowed:
            return False, f"target {t} outside authorized scope ({why})"
    return True, ""


def kill_switch_active(state_dir: str) -> bool:
    return os.path.exists(os.path.join(state_dir, "STOP"))


# ── optional launcher (IO; not unit-tested) ──────────────────────────────────
def run(config_values: dict, *, mode: str = "pairing", pat: str | None = None,
        token: str | None = None, state_dir: str = ".", spawn=None) -> int:
    """Opt-in: enroll + run the daemon under the supervisor, honoring the kill
    switch. Reuses the verified env mapping + Phase-3 supervisor."""
    import subprocess
    import sys

    from agent import supervisor

    base = {k: v for k, v in {
        "PLATFORM_URL": config_values.get("manager_url", ""),
        "PROBE_NAME": config_values.get("name", ""),
        "VERIFY_TLS": "true" if config_values.get("verify_tls", True) else "false",
    }.items() if v}
    env = connect_env(mode, pat, token, {**os.environ, **base})

    def _spawn(cmd):
        return subprocess.run(cmd, env=env, cwd=state_dir).returncode

    return supervisor.supervise(
        [sys.executable, "-m", "agent.agent"],
        spawn=spawn or _spawn,
        stop_check=lambda: kill_switch_active(state_dir),
    )
