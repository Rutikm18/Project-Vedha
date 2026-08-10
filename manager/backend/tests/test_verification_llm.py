from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.detection.verification import verify_finding


@pytest.mark.asyncio
async def test_no_llm_matches_deterministic():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 80}
    v = await verify_finding(ev, llm=None)
    assert v.state == "corroborated"
    assert v.rationale  # deterministic reason present


@pytest.mark.asyncio
async def test_llm_error_falls_back_to_deterministic():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 55,
          "kev": True, "priority": "high"}
    llm = AsyncMock()
    llm.verify_rationale = AsyncMock(side_effect=RuntimeError("provider down"))
    v = await verify_finding(ev, llm=llm)
    assert v.state in ("corroborated", "inferred")  # deterministic stands
    assert v.needs_review is True                    # from deterministic rule


@pytest.mark.asyncio
async def test_llm_can_flag_false_positive_and_lower():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 35,
          "kev": True, "priority": "high"}
    llm = AsyncMock()
    llm.verify_rationale = AsyncMock(return_value={
        "rationale": "Version string matches but the service banner suggests a backported build.",
        "suspected_false_positive": True,
    })
    v = await verify_finding(ev, llm=llm)
    assert v.needs_review is True
    assert v.state == "contradicted"          # low conf + FP flag → contradicted
    assert "backported" in v.rationale
