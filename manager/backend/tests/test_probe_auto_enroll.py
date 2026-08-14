"""
test_probe_auto_enroll.py — trust-on-first-use enrollment gate + CIDR policy.

The auto-approve DB path (_get_or_create_auto_enroll_site → _provision_agent_for_site)
needs a live Postgres, so it's exercised by the integration path; here we guard the
pure decision surface: the master switch is OFF by default (secure), and the coarse
authorized-CIDR policy parses correctly.
"""
from __future__ import annotations

import types

import app.routers.probe_enrollment as pe
from app.config import Settings


def test_auto_enroll_is_off_by_default():
    # Secure by default: no probe joins without a token or approval unless the
    # operator explicitly opts the whole Manager in.
    assert Settings().probe_auto_enroll is False


def test_auto_enroll_cidrs_defaults_to_rfc1918(monkeypatch):
    monkeypatch.setattr(pe, "get_settings",
                        lambda: types.SimpleNamespace(probe_auto_enroll_cidrs=""))
    assert pe.auto_enroll_cidrs() == ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]


def test_auto_enroll_cidrs_parses_and_trims_custom(monkeypatch):
    monkeypatch.setattr(pe, "get_settings",
                        lambda: types.SimpleNamespace(
                            probe_auto_enroll_cidrs="192.168.1.0/24, 10.9.0.0/16 ,"))
    assert pe.auto_enroll_cidrs() == ["192.168.1.0/24", "10.9.0.0/16"]


def test_auto_enroll_site_name_is_stable():
    # A rename would orphan previously auto-enrolled probes' Site — keep it fixed.
    assert pe._AUTO_ENROLL_SITE_NAME == "auto-enroll"
