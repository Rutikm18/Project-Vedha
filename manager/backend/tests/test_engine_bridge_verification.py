from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.detection import engine_bridge
from app.detection.verification import VerificationVerdict


@pytest.mark.asyncio
async def test_stamp_verification_sets_columns_when_enabled():
    f = SimpleNamespace(evidence={"source_confidence": "inferred", "state": "suspected",
                                  "confidence": 80},
                        verification_state=None, verification_confidence=None,
                        verification_rationale=None, needs_review=False,
                        verification_method=None)

    with patch.object(engine_bridge, "run_verification",
                      new=AsyncMock(return_value=VerificationVerdict(
                          state="corroborated", confidence=80, needs_review=False,
                          rationale="ok"))):
        await engine_bridge._stamp_verification([f], llm=None)

    assert f.verification_state == "corroborated"
    assert f.verification_confidence == 80
    assert f.verification_method == "passive"
