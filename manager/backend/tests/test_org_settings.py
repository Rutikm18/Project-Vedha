"""Organisation policy: validation and the pure rules (network, session, blackout, exclusions)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.services import org_settings as os_


def utc(*a):
    return datetime(*a, tzinfo=timezone.utc)


# ── defaults leave behaviour unchanged ───────────────────────────────────────

def test_defaults_restrict_nothing():
    auth, scan, cust = os_.AuthPolicy(), os_.ScanPolicy(), os_.CustomerDefaults()
    assert auth.ip_allowlist == [] and auth.operator_session_max_hours is None
    assert os_.sign_in_allowed(auth, role="analyst", address="203.0.113.9")
    assert os_.active_blackout(scan, utc(2026, 10, 3, 12)) is None
    assert scan.admin_override is True and scan.global_exclusions == []
    assert cust.poc_locked_severities == ["critical", "high"] and cust.poc_duration_days == 14


# ── validation ───────────────────────────────────────────────────────────────

def test_unknown_keys_are_refused():
    with pytest.raises(ValidationError):
        os_.AuthPolicy.model_validate({"ip_allowlist": [], "bypass": True})


def test_allowlist_is_validated_normalised_and_deduplicated():
    p = os_.AuthPolicy(ip_allowlist=["10.0.0.0/8", "10.0.0.0/8", "192.168.1.5", "2001:db8::/32"])
    assert p.ip_allowlist == ["10.0.0.0/8", "192.168.1.5/32", "2001:db8::/32"]
    for bad in (["not-an-ip"], ["10.0.0.0/33"], ["10.0.0.0/8; drop"], [""]):
        with pytest.raises(ValidationError):
            os_.AuthPolicy(ip_allowlist=bad)


def test_list_sizes_and_session_hours_are_bounded():
    with pytest.raises(ValidationError):
        os_.AuthPolicy(ip_allowlist=[f"10.{i}.0.0/16" for i in range(51)])
    for hours in (0, -1, 721):
        with pytest.raises(ValidationError):
            os_.AuthPolicy(operator_session_max_hours=hours)
    assert os_.AuthPolicy(operator_session_max_hours=8).operator_session_max_hours == 8


def test_window_shapes():
    ok = dict(name="Close", kind="weekly", timezone="Asia/Kolkata", days=[4], start="18:00", end="23:00")
    assert os_.BlackoutWindow(**ok).days == [4]
    for patch in ({"days": []}, {"days": [7]}, {"days": [1, 1]}, {"start": "25:00"}, {"start": "9:00"},
                  {"end": "18:00"}, {"timezone": "Mars/Base"}, {"name": ""}):
        with pytest.raises(ValidationError):
            os_.BlackoutWindow(**{**ok, **patch})
    with pytest.raises(ValidationError):                         # one-off needs zoned, ordered instants
        os_.BlackoutWindow(name="x", kind="once", starts_at="2026-10-01T00:00:00", ends_at="2026-10-02T00:00:00")
    with pytest.raises(ValidationError):
        os_.BlackoutWindow(name="x", kind="once", starts_at="2026-10-02T00:00:00Z", ends_at="2026-10-01T00:00:00Z")


def test_exclusions_and_customer_defaults_validate():
    assert os_.ScanPolicy(global_exclusions=["10.0.0.5", "172.16.0.0/12"]).global_exclusions == ["10.0.0.5/32", "172.16.0.0/12"]
    with pytest.raises(ValidationError):
        os_.ScanPolicy(global_exclusions=["host.example.com"])
    assert os_.CustomerDefaults(poc_locked_severities=["high", "high", "critical"]).poc_locked_severities == ["high", "critical"]
    for bad in ({"poc_locked_severities": ["urgent"]}, {"poc_locked_features": ["admin"]}, {"poc_duration_days": 0}):
        with pytest.raises(ValidationError):
            os_.CustomerDefaults(**bad)


# ── sign-in network rule ─────────────────────────────────────────────────────

def test_allowlist_decides_for_operators_and_fails_closed():
    p = os_.AuthPolicy(ip_allowlist=["10.0.0.0/8", "2001:db8::/32"])
    assert os_.sign_in_allowed(p, role="manager", address="10.4.5.6")
    assert os_.sign_in_allowed(p, role="analyst", address="2001:db8::1")
    assert not os_.sign_in_allowed(p, role="manager", address="203.0.113.9")
    for unusable in (None, "", "unknown", "garbage"):
        assert not os_.sign_in_allowed(p, role="tester", address=unusable)


def test_ipv4_and_ipv6_are_not_confused():
    assert not os_.ip_allowed(["10.0.0.0/8"], "2001:db8::1")


def test_admins_are_always_exempt_so_a_wrong_list_cannot_lock_everyone_out():
    p = os_.AuthPolicy(ip_allowlist=["10.0.0.0/8"], ip_allowlist_applies_to_portal=True)
    assert os_.sign_in_allowed(p, role="admin", address="203.0.113.9")


def test_customers_are_only_held_to_the_list_when_asked():
    p = os_.AuthPolicy(ip_allowlist=["10.0.0.0/8"])
    assert os_.sign_in_allowed(p, role="client", address="203.0.113.9")
    p = os_.AuthPolicy(ip_allowlist=["10.0.0.0/8"], ip_allowlist_applies_to_portal=True)
    assert not os_.sign_in_allowed(p, role="client", address="203.0.113.9")
    assert os_.sign_in_allowed(p, role="client", address="10.9.9.9")


# ── absolute session limit ───────────────────────────────────────────────────

def test_session_limit_is_per_audience_and_absolute():
    p = os_.AuthPolicy(operator_session_max_hours=8, customer_session_max_hours=24)
    now = utc(2026, 10, 3, 12)
    assert not os_.session_expired(p, role="analyst", auth_time=now - timedelta(hours=7, minutes=59), now=now)
    assert os_.session_expired(p, role="analyst", auth_time=now - timedelta(hours=8, minutes=1), now=now)
    assert not os_.session_expired(p, role="client", auth_time=now - timedelta(hours=20), now=now)
    assert os_.session_expired(p, role="client", auth_time=now - timedelta(hours=25), now=now)


def test_no_limit_or_no_sign_in_time_never_expires():
    now = utc(2026, 10, 3, 12)
    assert not os_.session_expired(os_.AuthPolicy(), role="manager", auth_time=now - timedelta(days=400), now=now)
    # a token from before the claim existed: treated as just signed in
    assert not os_.session_expired(os_.AuthPolicy(operator_session_max_hours=1), role="manager", auth_time=None, now=now)


# ── blackout windows ─────────────────────────────────────────────────────────

def weekly(**kw):
    base = dict(name="Freeze", kind="weekly", timezone="UTC", days=[4], start="18:00", end="23:00")
    return os_.ScanPolicy(blackouts=[os_.BlackoutWindow(**{**base, **kw})])


def test_same_day_window_includes_start_excludes_end():
    p = weekly()                                    # Fridays 18:00-23:00 UTC; 2026-10-02 is a Friday
    assert os_.active_blackout(p, utc(2026, 10, 2, 18, 0)).name == "Freeze"
    assert os_.active_blackout(p, utc(2026, 10, 2, 22, 59)) is not None
    assert os_.active_blackout(p, utc(2026, 10, 2, 23, 0)) is None
    assert os_.active_blackout(p, utc(2026, 10, 2, 17, 59)) is None
    assert os_.active_blackout(p, utc(2026, 10, 3, 19, 0)) is None          # Saturday


def test_a_window_can_cross_midnight_into_the_next_day():
    p = weekly(start="22:00", end="06:00")           # Friday 22:00 -> Saturday 06:00
    assert os_.active_blackout(p, utc(2026, 10, 2, 23, 0)) is not None      # Fri night
    assert os_.active_blackout(p, utc(2026, 10, 3, 5, 59)) is not None      # Sat early
    assert os_.active_blackout(p, utc(2026, 10, 3, 6, 0)) is None
    assert os_.active_blackout(p, utc(2026, 10, 2, 21, 0)) is None
    assert os_.active_blackout(p, utc(2026, 10, 3, 22, 30)) is None         # Saturday night is not listed


def test_windows_are_read_in_their_own_time_zone_including_dst():
    # 18:00-23:00 New York on Fridays. In October (EDT, UTC-4) that is 22:00-03:00 UTC.
    p = weekly(timezone="America/New_York")
    assert os_.active_blackout(p, utc(2026, 10, 2, 22, 30)) is not None
    assert os_.active_blackout(p, utc(2026, 10, 2, 21, 30)) is None
    # In January (EST, UTC-5) the same local window is 23:00-04:00 UTC: DST honoured.
    assert os_.active_blackout(p, utc(2027, 1, 1, 23, 30)) is not None       # Fri 2027-01-01 18:30 EST
    assert os_.active_blackout(p, utc(2027, 1, 1, 22, 30)) is None


def test_a_one_off_window_is_half_open():
    p = os_.ScanPolicy(blackouts=[os_.BlackoutWindow(
        name="Migration", kind="once", starts_at="2026-10-10T00:00:00Z", ends_at="2026-10-11T00:00:00Z")])
    assert os_.active_blackout(p, utc(2026, 10, 10, 0, 0)).name == "Migration"
    assert os_.active_blackout(p, utc(2026, 10, 10, 23, 59)) is not None
    assert os_.active_blackout(p, utc(2026, 10, 11, 0, 0)) is None
    assert os_.active_blackout(p, utc(2026, 10, 9, 23, 59)) is None


# ── exclusions ───────────────────────────────────────────────────────────────

def test_global_exclusions_merge_without_duplicates_and_keep_order():
    p = os_.ScanPolicy(global_exclusions=["10.0.0.0/24", "192.168.0.1/32"])
    assert os_.merge_global_exclusions(["10.0.0.0/24", "172.16.0.0/12"], p) == ["10.0.0.0/24", "172.16.0.0/12", "192.168.0.1/32"]
    assert os_.merge_global_exclusions(None, os_.ScanPolicy()) == []


def test_a_scan_wholly_inside_the_exclusions_is_detected():
    ex = ["10.0.0.0/16"]
    assert os_.entirely_excluded(["10.0.5.0/24", "10.0.9.9"], ex)
    assert not os_.entirely_excluded(["10.0.5.0/24", "10.1.0.1"], ex)          # one target outside
    assert not os_.entirely_excluded(["10.0.0.0/8"], ex)                        # bigger than the exclusion
    assert not os_.entirely_excluded(["10.0.0.1-10.0.0.9"], ex)                 # ranges: not claimed covered
    assert not os_.entirely_excluded([], ex) and not os_.entirely_excluded(["10.0.0.1"], [])
