from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

from agent.agent import (
    _flush_spool_over_http,
    _ws_run_job,
    _ws_stage_job_offer,
    _ws_take_confirmed_job,
)
from agent.result_spool import ResultSpool


def test_offer_is_staged_and_only_sends_ack():
    ws = AsyncMock()
    job = {"job_id": "job-1", "job_type": "discovery"}
    state = {"current_job_id": None, "pending_job": None}

    accepted = asyncio.run(_ws_stage_job_offer(ws, job, state))

    assert accepted is True
    assert state["pending_job"] == job
    frame = json.loads(ws.send.await_args.args[0])
    assert frame == {
        "type": "job_ack",
        "job_id": "job-1",
        "accepted": True,
    }


def test_staged_job_is_not_released_without_positive_confirmation():
    job = {"job_id": "job-1", "job_type": "discovery"}
    state = {"current_job_id": None, "pending_job": job}

    assert _ws_take_confirmed_job(
        {"type": "job_claim", "job_id": "job-1", "claimed": False},
        state,
    ) is None
    assert state["pending_job"] is None


def test_positive_confirmation_releases_exactly_the_staged_job():
    job = {"job_id": "job-1", "job_type": "discovery"}
    state = {"current_job_id": None, "pending_job": job}

    assert _ws_take_confirmed_job(
        {"type": "job_claim", "job_id": "other", "claimed": True},
        state,
    ) is None
    assert state["pending_job"] == job

    assert _ws_take_confirmed_job(
        {
            "type": "job_claim",
            "job_id": "job-1",
            "claimed": True,
            "attempt_id": "attempt-1",
            "attempt_number": 1,
            "fence": 1,
            "lease_expires_at": "2026-08-03T00:00:00+00:00",
        },
        state,
    ) == {
        **job,
        "attempt_id": "attempt-1",
        "attempt_number": 1,
        "fence": 1,
        "lease_expires_at": "2026-08-03T00:00:00+00:00",
    }
    assert state["pending_job"] is None


def test_busy_probe_declines_additional_offer():
    ws = AsyncMock()
    state = {
        "current_job_id": "job-running",
        "pending_job": None,
    }

    accepted = asyncio.run(
        _ws_stage_job_offer(
            ws,
            {"job_id": "job-2", "job_type": "discovery"},
            state,
        )
    )

    assert accepted is False
    assert state["pending_job"] is None
    assert json.loads(ws.send.await_args.args[0])["accepted"] is False


def test_ws_job_does_not_duplicate_task_runner_result_submission():
    ws = AsyncMock()
    runner = SimpleNamespace(
        run_job=lambda job, agent_id: SimpleNamespace(
            error=None,
            scan_type="discovery",
        ),
    )
    state = {"current_job_id": None, "pending_job": None}

    asyncio.run(_ws_run_job(
        ws,
        runner,
        "agent-1",
        {"job_id": "job-1", "job_type": "discovery"},
        state,
        pushed=True,
    ))

    frames = [json.loads(call.args[0]) for call in ws.send.await_args_list]
    assert [frame["type"] for frame in frames] == ["heartbeat", "heartbeat"]
    assert all(frame["type"] != "result" for frame in frames)


def test_http_spool_flush_removes_only_manager_acknowledged_result(tmp_path):
    spool = ResultSpool(tmp_path / "spool")
    spool.save("job-1", {
        "success": True,
        "result": {"ok": True},
        "error": None,
    })
    transport = SimpleNamespace(submit_result=lambda job_id, payload: False)

    asyncio.run(_flush_spool_over_http(transport, spool))
    assert spool.exists("job-1")

    transport.submit_result = lambda job_id, payload: True
    asyncio.run(_flush_spool_over_http(transport, spool))
    assert not spool.exists("job-1")
