from __future__ import annotations

import pytest

from app.ai.verification_graph import graph_available, run_verification


@pytest.mark.asyncio
async def test_run_verification_matches_core_without_llm():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 80}
    v = await run_verification(ev, llm=None)
    assert v.state == "corroborated"


def test_graph_available_is_boolean():
    assert isinstance(graph_available(), bool)
