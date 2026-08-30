from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge


@pytest.mark.asyncio
async def test_run_records_coverage_and_invokes_resolution():
    engagement_id = uuid.uuid4()
    result = {
        "facts": [{"scanner": "tls_scan", "target": "10.0.0.5:443", "status": "open"}],
        "scanner_runs": [{"id": "tls_scan", "status": "completed"}],
    }

    added = []
    db = MagicMock()
    db.add = MagicMock(side_effect=lambda o: added.append(o))
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

    # evaluate_resolutions is imported INTO engine_bridge, so patch it there.
    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_all_from_facts_traced", return_value=([], [], {"coverage": {}, "verdicts": {}})), \
         patch.object(engine_bridge, "evaluate_resolutions",
                      new=AsyncMock(return_value=2)) as mock_eval:
        await engine_bridge.create_findings_from_facts(db, engagement_id, result)

    run = added[0]  # the DetectionRun is the first row added
    assert run.stats["coverage"]["assets"] == ["10.0.0.5"]
    assert run.stats["auto_resolved"] == 2
    mock_eval.assert_awaited_once()
