"""
test_fd_limit.py — FIX 1: ulimit-aware concurrency for full-range scans.

A full 1-65535 connect scan must never lose ports to EMFILE ("too many open
files"). safe_connect_concurrency caps the concurrent-connection batch below the
fd soft limit (after raising it), honoring the operator's request when it fits.
"""
from __future__ import annotations

import scanner.scanner_base as sb
from scanner.port_scanner import resolve_profile


def test_caps_below_soft_limit(monkeypatch):
    monkeypatch.setattr(sb, "raise_fd_limit", lambda: (1024, 4096))
    assert sb.safe_connect_concurrency(5000) == 1024 - 200   # capped under ceiling
    assert sb.safe_connect_concurrency(100) == 100           # already fits → honored


def test_no_rlimit_caps_modestly(monkeypatch):
    # Platform with no resource limits (e.g. Windows) → conservative 512 cap.
    monkeypatch.setattr(sb, "raise_fd_limit", lambda: (0, 0))
    assert sb.safe_connect_concurrency(5000) == 512
    assert sb.safe_connect_concurrency(100) == 100


def test_floor_when_limit_tiny(monkeypatch):
    monkeypatch.setattr(sb, "raise_fd_limit", lambda: (50, 100))
    assert sb.safe_connect_concurrency(5000) == 16           # floor, never below


def test_get_fd_limit_returns_pair():
    soft, hard = sb.get_fd_limit()
    assert isinstance(soft, int) and isinstance(hard, int)


def test_full_profile_covers_the_whole_tcp_space():
    full = resolve_profile("full")
    assert len(full) == 65535 and full[0] == 1 and full[-1] == 65535
    # the exact rig ports that top1000 misses are all present in full
    for p in (4444, 8081, 9000, 9201, 9205, 9500, 9600, 50000):
        assert p in full


def test_top1000_misses_arbitrary_high_ports_full_does_not():
    top = set(resolve_profile("top1000"))
    full = set(resolve_profile("full"))
    missed_by_top = {4444, 9000, 9201, 9500, 50000}
    assert missed_by_top & top == set()      # top1000 genuinely misses these
    assert missed_by_top <= full             # full covers them → why full is the fix
