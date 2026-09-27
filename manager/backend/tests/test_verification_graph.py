from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import app.ai.verification_graph as graph_mod
from app.ai.verification_graph import graph_available, run_verification
from app.detection.verification import compute_verdict


@pytest.mark.asyncio
async def test_run_verification_matches_core_without_llm():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 80}
    v = await run_verification(ev, llm=None)
    assert v.state == "corroborated"


def test_graph_available_is_boolean():
    assert isinstance(graph_available(), bool)


@pytest.mark.asyncio
async def test_graph_skips_llm_for_low_value_verdict():
    ev = {"source_confidence": "inferred", "state": "potential", "confidence": 55}
    llm = AsyncMock()
    llm.verify_rationale = AsyncMock(return_value={"rationale": "unused"})

    verdict = await run_verification(ev, llm=llm)

    assert verdict.state == "inferred"
    llm.verify_rationale.assert_not_awaited()


@pytest.mark.asyncio
async def test_graph_conditionally_reviews_and_can_only_downgrade():
    ev = {
        "source_confidence": "inferred",
        "state": "suspected",
        "confidence": 35,
        "priority": "high",
    }
    llm = AsyncMock()
    llm.verify_rationale = AsyncMock(return_value={
        "rationale": "Likely a backported build.",
        "suspected_false_positive": True,
    })

    verdict = await run_verification(ev, llm=llm)

    assert verdict.state == "contradicted"
    assert verdict.confidence == 35
    llm.verify_rationale.assert_awaited_once_with(ev)


@pytest.mark.asyncio
async def test_runtime_adapter_is_not_stored_in_graph_state(monkeypatch):
    captured = {}

    class CapturingGraph:
        async def ainvoke(self, state, *, config):
            captured["state"] = state
            captured["config"] = config
            return {"verdict": compute_verdict(state["evidence"])}

    monkeypatch.setattr(graph_mod, "_VERIFICATION_GRAPH", CapturingGraph())
    llm = AsyncMock()
    ev = {"confidence": 80}

    await run_verification(ev, llm=llm)

    assert set(captured["state"]) == {"evidence", "review_requested"}
    assert captured["config"]["configurable"]["verification_llm"] is llm


@pytest.mark.asyncio
async def test_graph_orchestration_failure_preserves_core_fallback(monkeypatch):
    class BrokenGraph:
        async def ainvoke(self, state, *, config):
            raise RuntimeError("graph runtime failed")

    monkeypatch.setattr(graph_mod, "_VERIFICATION_GRAPH", BrokenGraph())
    ev = {"source_confidence": "inferred", "state": "potential", "confidence": 72}

    verdict = await run_verification(ev)

    assert verdict == compute_verdict(ev)
