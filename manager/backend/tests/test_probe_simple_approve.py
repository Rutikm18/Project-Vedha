"""test_probe_simple_approve.py — one-click probe approval helpers (item 5)."""
from __future__ import annotations

import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock

from app.routers import probe_enrollment as pe


def _db_names(names):
    """db.execute(...).scalars().all() → the given agent-name list."""
    db = MagicMock()
    r = MagicMock()
    r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=names)))
    db.execute = AsyncMock(return_value=r)
    return db


class TestNextProbeName:
    def test_first_is_01(self):
        assert asyncio.run(pe._next_probe_name(_db_names([]), uuid.uuid4())) == "vedha_probe_01"

    def test_increments_past_highest_with_gaps(self):
        names = ["vedha_probe_01", "vedha_probe_03", "some-other-probe"]
        assert asyncio.run(pe._next_probe_name(_db_names(names), uuid.uuid4())) == "vedha_probe_04"

    def test_ignores_non_matching_and_non_numeric(self):
        names = ["custom-probe", None, "vedha_probe_x"]
        assert asyncio.run(pe._next_probe_name(_db_names(names), uuid.uuid4())) == "vedha_probe_01"


class TestSimpleApproveInput:
    def test_defaults_are_all_optional(self):
        b = pe.SimpleApproveInput()
        assert b.probe_name is None
        assert b.authorized_cidrs is None
        assert b.approved_capabilities is None
        assert b.excluded_cidrs == []

    def test_overrides_accepted(self):
        b = pe.SimpleApproveInput(probe_name="edge-01",
                                  approved_capabilities=["nmap"],
                                  authorized_cidrs=["10.0.0.0/24"])
        assert b.probe_name == "edge-01"
        assert b.approved_capabilities == ["nmap"]
        assert b.authorized_cidrs == ["10.0.0.0/24"]
