"""
B4 (manager half) — `paused` must survive the heartbeat, not be coerced away.

The heartbeat handler does:

    try:    agent.status = AgentStatus(body.status)
    except ValueError:
        agent.status = AgentStatus.online

So any status the enum does not know becomes `online` — which is exactly the
lie this task removes. A probe refusing work because its result spool is full
would keep reporting as a healthy idle probe, and the manager would keep
dispatching to it.

Carrying `paused` in the enum fixes both halves at once: the fleet view shows
the real state, and the two dispatch paths (push_job, and the enqueue
eligibility query) already select on `online`, so a paused probe stops being
offered work without either of them changing.
"""
from __future__ import annotations

from app.models.agent import AgentStatus


def test_paused_is_a_known_status():
    assert AgentStatus("paused") is AgentStatus.paused


def test_paused_is_distinct_from_idle_and_from_busy():
    """The whole point: 'will decline every job' is not 'ready for work'."""
    assert AgentStatus.paused not in (AgentStatus.online, AgentStatus.busy,
                                      AgentStatus.offline)


def test_the_existing_statuses_are_unchanged():
    for name in ("online", "offline", "busy"):
        assert AgentStatus(name).value == name


def test_dispatch_selects_online_so_a_paused_probe_is_skipped():
    """Both dispatch paths gate on `online`. Pinning that here means adding
    `paused` cannot silently start routing jobs to a saturated probe."""
    import inspect

    from app.routers import agents as agents_router
    from app.websocket import manager as ws_manager

    push = inspect.getsource(ws_manager.AgentConnectionManager.push_job)
    assert 'status not in ("online",)' in push

    enqueue = inspect.getsource(agents_router.enqueue_agent_job)
    assert "Agent.status == AgentStatus.online" in enqueue
