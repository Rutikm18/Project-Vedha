"""
A job pinned to an agent that no longer exists must not be stranded forever.

OBSERVED 2026-09-05: two jobs sat `pending` for a day. Each carried a
`preferred_agent_id` pointing at an agent id that no longer existed, so no probe
would claim them — pinning is a hard constraint, and nothing reaps a pin nobody
can satisfy. They also silently consumed slots in the per-engagement queue cap.

The cause is structural, not a one-off: every probe re-registration mints a NEW
agent id. In one session a single probe cycled through four. Any job pinned to a
previous id is orphaned the moment its probe re-enrols.

The distinction this encodes:
  * pin -> a LIVE agent      = operator intent, hard constraint, respected.
  * pin -> a NONEXISTENT id  = stale metadata, ignored, job falls back.

Falling back is safe because capability AND network-reachability checks still
run: a job can never be routed to a probe that cannot reach its scope.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers import agents as ag


def _db_heartbeat(value):
    """A db whose Agent.last_heartbeat lookup yields `value` (None = unknown)."""
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: value))
    return db


def _ago(seconds: float):
    return datetime.now(timezone.utc) - timedelta(seconds=seconds)


class TestPinnedAgentLiveness:
    """Row EXISTENCE is not the test — that was the first version and it was
    wrong. A re-registered probe leaves its old row behind as `offline` forever,
    and the observed orphans were pinned to rows that existed but whose last
    heartbeat was ~11 hours old. Recency is the real discriminator."""

    @pytest.mark.asyncio
    async def test_recently_seen_agent_is_live(self):
        assert await ag._pinned_agent_is_live(_db_heartbeat(_ago(20)),
                                              uuid.uuid4()) is True

    @pytest.mark.asyncio
    async def test_restarting_probe_keeps_its_pin(self):
        """The 15-minute window exists so a redeploy does not steal a job an
        operator deliberately routed to a specific probe."""
        assert await ag._pinned_agent_is_live(_db_heartbeat(_ago(120)),
                                              uuid.uuid4()) is True

    @pytest.mark.asyncio
    async def test_long_dead_agent_releases_its_pin(self):
        """The observed case: ~11 hours silent."""
        assert await ag._pinned_agent_is_live(_db_heartbeat(_ago(11 * 3600)),
                                              uuid.uuid4()) is False

    @pytest.mark.asyncio
    async def test_boundary_is_the_configured_window(self):
        w = ag.PINNED_AGENT_STALE_AFTER_SECONDS
        assert await ag._pinned_agent_is_live(_db_heartbeat(_ago(w - 30)),
                                              uuid.uuid4()) is True
        assert await ag._pinned_agent_is_live(_db_heartbeat(_ago(w + 30)),
                                              uuid.uuid4()) is False

    @pytest.mark.asyncio
    async def test_window_is_far_longer_than_the_90s_liveness_check(self):
        """Reusing the 90s online/offline threshold would release pins during an
        ordinary restart."""
        assert ag.PINNED_AGENT_STALE_AFTER_SECONDS >= 600

    @pytest.mark.asyncio
    async def test_unknown_agent_is_not_live(self):
        assert await ag._pinned_agent_is_live(_db_heartbeat(None),
                                              uuid.uuid4()) is False

    @pytest.mark.asyncio
    @pytest.mark.parametrize("bad", ["not-a-uuid", "", None, 12345])
    async def test_malformed_pin_never_strands_a_job(self, bad):
        assert await ag._pinned_agent_is_live(_db_heartbeat(None), bad) is False

    @pytest.mark.asyncio
    async def test_string_form_of_a_real_id_is_accepted(self):
        """Pins arrive from JSON params, so they are strings, not UUIDs."""
        assert await ag._pinned_agent_is_live(_db_heartbeat(_ago(5)),
                                              str(uuid.uuid4())) is True


class TestPinSemantics:
    """Documents the rule the claim loop implements."""

    def test_live_pin_is_a_hard_constraint(self):
        src = ag.__file__
        with open(src) as fh:
            body = fh.read()
        i = body.index("dangling_pin_ignored")
        window = body[i - 900:i + 200]
        assert "_pinned_agent_is_live" in window
        assert "continue" in window, "a live pin must still skip other probes"

    def test_dangling_pin_is_logged_not_silent(self):
        """An ignored pin changes routing, so it must be visible in the log."""
        with open(ag.__file__) as fh:
            body = fh.read()
        assert "agent.job.dangling_pin_ignored" in body

    def test_fallback_still_runs_the_eligibility_gate(self):
        """The safety property: ignoring a stale pin must NOT bypass capability
        or reachability, or a job could be scanned from the wrong vantage."""
        with open(ag.__file__) as fh:
            body = fh.read()
        i = body.index("dangling_pin_ignored")
        after = body[i:i + 700]
        assert "_agent_can_execute_job" in after
