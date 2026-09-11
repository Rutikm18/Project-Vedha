"""Phase 6 — optional connect + uplink security. Enrollment env mapping is pure;
signed-job verification + independent scope re-check use real Ed25519 (skipped if
cryptography is absent)."""
from __future__ import annotations

import base64
import json

import pytest

from agent import connect as c
from agent import scope_model as sm


# ── enrollment env mapping (VERIFIED against agent/agent.py) ─────────────────
def test_pairing_sets_no_credential_env():
    env = c.connect_env("pairing", pat=None, token=None, base={"PLATFORM_URL": "https://m"})
    assert "VEDHA_PAT" not in env and "PROBE_ENROLL_TOKEN" not in env
    assert env["PLATFORM_URL"] == "https://m"


def test_pat_mode_sets_vedha_pat():
    env = c.connect_env("pat", pat="vpat_abc", token=None, base={})
    assert env["VEDHA_PAT"] == "vpat_abc"


def test_token_mode_sets_probe_enroll_token():
    env = c.connect_env("token", pat=None, token="vet_xyz", base={})
    assert env["PROBE_ENROLL_TOKEN"] == "vet_xyz"


# ── signed-job verification + independent scope re-check ─────────────────────
def _keypair():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    sk = Ed25519PrivateKey.generate()
    pub = sk.public_key().public_bytes_raw()
    return sk, base64.b64encode(pub).decode()


def _signed(job: dict, sk) -> dict:
    sig = sk.sign(c.canonical_job_bytes(job))
    return {**job, "sig": base64.b64encode(sig).decode()}


SEGMENTS = [sm.Segment(cidr="10.20.0.0/24", type="IT", profile="it", site="hq"),
            sm.Segment(cidr="10.99.0.0/24", type="OT", active=False, site="plant")]
NOW = 1_000_000.0
BASE_JOB = {"contract_version": "1.0.0", "job_id": "j1", "uc": 10, "intensity": 2,
            "scope_cidrs": ["10.20.0.0/24"], "targets": ["10.20.0.5"], "site": "hq",
            "not_before": NOW - 10, "expires": NOW + 1000}


def test_valid_signed_job_verifies():
    pytest.importorskip("cryptography")
    sk, pub = _keypair()
    ok, reason = c.verify_job(_signed(BASE_JOB, sk), pub, now=NOW)
    assert ok, reason


def test_tampered_job_is_rejected():
    pytest.importorskip("cryptography")
    sk, pub = _keypair()
    job = _signed(BASE_JOB, sk)
    job["targets"] = ["10.20.0.99"]        # mutate after signing
    ok, reason = c.verify_job(job, pub, now=NOW)
    assert not ok and "signature" in reason.lower()


def test_expired_job_is_rejected():
    pytest.importorskip("cryptography")
    sk, pub = _keypair()
    job = _signed({**BASE_JOB, "expires": NOW - 1}, sk)
    ok, reason = c.verify_job(job, pub, now=NOW)
    assert not ok and "expired" in reason.lower()


def test_wrong_contract_version_is_rejected():
    pytest.importorskip("cryptography")
    sk, pub = _keypair()
    job = _signed({**BASE_JOB, "contract_version": "2.0.0"}, sk)
    ok, reason = c.verify_job(job, pub, now=NOW)
    assert not ok and "version" in reason.lower()


def test_admit_job_enforces_local_scope_after_signature():
    pytest.importorskip("cryptography")
    sk, pub = _keypair()
    # signed, but a target outside the local IT scope must still be refused
    job = _signed({**BASE_JOB, "targets": ["10.20.0.5", "10.99.0.5"]}, sk)
    ok, reason = c.admit_job(job, pub, SEGMENTS, now=NOW)
    assert not ok and ("scope" in reason.lower() or "denylist" in reason.lower())

    ok2, _ = c.admit_job(_signed(BASE_JOB, sk), pub, SEGMENTS, now=NOW)
    assert ok2   # all targets inside IT scope


# ── kill switch ──────────────────────────────────────────────────────────────
def test_kill_switch_detects_stop_file(tmp_path):
    assert not c.kill_switch_active(str(tmp_path))
    (tmp_path / "STOP").write_text("")
    assert c.kill_switch_active(str(tmp_path))
