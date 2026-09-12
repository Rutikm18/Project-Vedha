"""Daemon integration — the independent admission gate wired into TaskRunner:
the permanent denylist (defense-in-depth beyond CIDR scope) + gated signed-job
verification. Pure."""
from __future__ import annotations

import base64

import pytest

from agent import job_admission as ja


def test_drop_denied_removes_never_scan_targets():
    kept, denied = ja.drop_denied(["10.20.0.5", "169.254.169.254", "127.0.0.1", "224.0.0.1"])
    assert kept == ["10.20.0.5"]
    assert set(denied) == {"169.254.169.254", "127.0.0.1", "224.0.0.1"}


def test_drop_denied_keeps_clean_targets():
    kept, denied = ja.drop_denied(["10.20.0.5", "192.168.1.10"])
    assert kept == ["10.20.0.5", "192.168.1.10"] and denied == []


def test_signed_job_check_skipped_without_pinned_key():
    ok, reason = ja.verify_signed_job({"targets": ["10.0.0.5"]}, pinned_key_b64=None)
    assert ok and "skipped" in reason


def test_signed_job_required_when_key_set_but_unsigned():
    ok, reason = ja.verify_signed_job({"targets": ["10.0.0.5"]}, pinned_key_b64="AAAA")
    assert not ok and "unsigned" in reason.lower()


def test_signed_job_accepts_valid_and_rejects_tampered():
    pytest.importorskip("cryptography")
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from agent import connect
    sk = Ed25519PrivateKey.generate()
    pub = base64.b64encode(sk.public_key().public_bytes_raw()).decode()
    job = {"contract_version": "1.0.0", "job_id": "j1", "uc": 10, "intensity": 2,
           "scope_cidrs": ["10.20.0.0/24"], "targets": ["10.20.0.5"], "site": "hq",
           "not_before": 0, "expires": 9_999_999_999}
    job["sig"] = base64.b64encode(sk.sign(connect.canonical_job_bytes(job))).decode()

    ok, _ = ja.verify_signed_job(job, pinned_key_b64=pub, now=1000.0)
    assert ok
    job["targets"] = ["10.20.0.99"]     # tamper after signing
    ok2, reason = ja.verify_signed_job(job, pinned_key_b64=pub, now=1000.0)
    assert not ok2 and "signature" in reason.lower()
