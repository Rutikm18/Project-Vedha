"""Phase 3 — supervisor: per-class policy, capped retries, kill-switch honored,
no wall-clock backoff. Pure via injected spawn/sleep/stop."""
from __future__ import annotations

from agent import supervisor as sup


def _recorder():
    calls = {"spawn": 0, "sleep": []}
    return calls


def test_success_stops_after_one_spawn():
    calls = _recorder()
    def spawn(cmd): calls["spawn"] += 1; return 0
    rc = sup.supervise(["x"], spawn=spawn, sleep=lambda s: calls["sleep"].append(s))
    assert rc == 0 and calls["spawn"] == 1 and calls["sleep"] == []


def test_fatal_config_stops_immediately_no_backoff():
    calls = _recorder()
    def spawn(cmd): calls["spawn"] += 1; return 20
    rc = sup.supervise(["x"], spawn=spawn, sleep=lambda s: calls["sleep"].append(s))
    assert rc == 20 and calls["spawn"] == 1 and calls["sleep"] == []


def test_retryable_backs_off_and_gives_up_after_cap():
    calls = _recorder()
    def spawn(cmd): calls["spawn"] += 1; return 10
    rc = sup.supervise(["x"], spawn=spawn, sleep=lambda s: calls["sleep"].append(s), max_retries=3)
    assert rc == 10 and calls["spawn"] == 3
    assert calls["sleep"] and all(s <= 30 for s in calls["sleep"])   # capped backoff


def test_fatal_identity_reenrolls_then_succeeds():
    seq = iter([30, 0])
    calls = _recorder()
    def spawn(cmd): calls["spawn"] += 1; return next(seq)
    rc = sup.supervise(["x"], spawn=spawn, sleep=lambda s: None, max_retries=4)
    assert rc == 0 and calls["spawn"] == 2


def test_awaiting_approval_polls_without_counting_toward_cap():
    seq = iter([40, 40, 40, 40, 0])   # 4 pending polls then approved
    calls = _recorder()
    def spawn(cmd): calls["spawn"] += 1; return next(seq)
    rc = sup.supervise(["x"], spawn=spawn, sleep=lambda s: calls["sleep"].append(s), max_retries=2)
    # would have exceeded max_retries=2 if polls counted; must still reach success
    assert rc == 0 and calls["spawn"] == 5


def test_kill_switch_returns_zero_without_spawning():
    calls = _recorder()
    def spawn(cmd): calls["spawn"] += 1; return 0
    rc = sup.supervise(["x"], spawn=spawn, sleep=lambda s: None, stop_check=lambda: True)
    assert rc == 0 and calls["spawn"] == 0
