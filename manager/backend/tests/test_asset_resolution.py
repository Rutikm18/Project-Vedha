"""
test_asset_resolution.py — P1b: the single asset-identity resolver
(app/services/asset_resolution.py). Pure selection logic + the DB-facing wrappers
against a recording fake session.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

from app.detection.asset_identity import MODE_GLOBAL, MODE_PER_SITE
from app.models.asset import Asset
from app.services.asset_resolution import (
    GLOBAL_IDENTITY, IdentityContext, find_asset, find_assets_batch, host_of, pick_asset,
    resolve_asset,
)

ENG = uuid.uuid4()
SITE_A, SITE_B = uuid.uuid4(), uuid.uuid4()
T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _asset(ip="10.0.0.5", site=None, age=0):
    a = Asset(engagement_id=ENG, ip_address=ip, site_id=site)
    a.id = uuid.uuid4()
    a.created_at = T0 + timedelta(days=age)
    return a


def _db(rows):
    db = MagicMock()
    result = MagicMock()
    result.scalars.return_value.all.return_value = list(rows)
    db.execute = AsyncMock(return_value=result)
    db.add = MagicMock()
    db.flush = AsyncMock()
    return db


PER_SITE_A = IdentityContext(MODE_PER_SITE, SITE_A)
PER_SITE_B = IdentityContext(MODE_PER_SITE, SITE_B)


# ── pure selection ───────────────────────────────────────────────────────────
def test_global_scope_prefers_unscoped_then_oldest():
    old, new = _asset(age=0), _asset(age=5)
    assert pick_asset([new, old], None) == (old, False)
    scoped, plain = _asset(site=SITE_A, age=0), _asset(age=9)
    assert pick_asset([scoped, plain], None) == (plain, False)
    assert pick_asset([scoped], None) == (scoped, False)       # only a scoped row exists
    assert pick_asset([], None) == (None, False)


def test_scoped_lookup_matches_its_site_exactly():
    a, b = _asset(site=SITE_A), _asset(site=SITE_B)
    assert pick_asset([a, b], SITE_B) == (b, False)


def test_scoped_lookup_adopts_the_legacy_row_instead_of_duplicating():
    legacy = _asset(site=None)
    assert pick_asset([legacy], SITE_A) == (legacy, True)


def test_scoped_lookup_does_not_adopt_another_sites_row():
    other = _asset(site=SITE_B)
    assert pick_asset([other], SITE_A) == (None, False)


def test_exact_row_beats_adoption():
    legacy, mine = _asset(site=None), _asset(site=SITE_A)
    assert pick_asset([legacy, mine], SITE_A) == (mine, False)


def test_selection_is_deterministic_regardless_of_row_order():
    rows = [_asset(age=i) for i in range(4)]
    assert pick_asset(rows, None)[0] is pick_asset(list(reversed(rows)), None)[0]


def test_host_of_strips_port_but_keeps_ipv6():
    assert host_of("10.0.0.5:443") == "10.0.0.5"
    assert host_of("10.0.0.5") == "10.0.0.5"
    assert host_of("fd00::1") == "fd00::1"
    assert host_of(None) is None and host_of("") is None


# ── DB-facing ────────────────────────────────────────────────────────────────
def test_duplicate_rows_never_raise_in_global_mode():
    # the old scalar_one_or_none() raised MultipleResultsFound here
    first, second = _asset(age=0), _asset(age=1)
    got = asyncio.run(find_asset(_db([second, first]), ENG, "10.0.0.5"))
    assert got is first


def test_global_mode_creates_an_unscoped_asset():
    db = _db([])
    got = asyncio.run(resolve_asset(db, ENG, "10.0.0.5", identity=GLOBAL_IDENTITY))
    assert got.site_id is None and got.ip_address == "10.0.0.5"
    db.add.assert_called_once()


def test_per_site_creates_separate_assets_for_the_same_private_ip():
    # site A already has 10.0.0.5; site B reports the same address -> a NEW asset
    a_row = _asset(site=SITE_A)
    db = _db([a_row])
    got = asyncio.run(resolve_asset(db, ENG, "10.0.0.5", identity=PER_SITE_B))
    assert got is not a_row and got.site_id == SITE_B
    db.add.assert_called_once()


def test_per_site_adopts_existing_history_for_the_first_site_to_report():
    legacy = _asset(site=None)
    db = _db([legacy])
    got = asyncio.run(resolve_asset(db, ENG, "10.0.0.5", identity=PER_SITE_A))
    assert got is legacy and legacy.site_id == SITE_A
    db.add.assert_not_called()


def test_public_ip_is_never_split_by_site():
    row = _asset(ip="1.1.1.1", site=None)
    got = asyncio.run(resolve_asset(_db([row]), ENG, "1.1.1.1", identity=PER_SITE_B))
    assert got is row and row.site_id is None


def test_probe_without_a_site_stays_global_in_per_site_mode():
    row = _asset(site=None)
    ctx = IdentityContext(MODE_PER_SITE, None)
    assert asyncio.run(resolve_asset(_db([row]), ENG, "10.0.0.5", identity=ctx)) is row


def test_cache_key_is_host_when_global_and_site_scoped_otherwise():
    db = _db([_asset(site=None)])
    cache: dict = {}
    asyncio.run(resolve_asset(db, ENG, "10.0.0.5", cache=cache))
    assert "10.0.0.5" in cache
    cache2: dict = {}
    asyncio.run(resolve_asset(_db([_asset(site=SITE_A)]), ENG, "10.0.0.5",
                              identity=PER_SITE_A, cache=cache2))
    assert (SITE_A, "10.0.0.5") in cache2


def test_batch_matches_single_lookup_policy():
    a_row, legacy = _asset(ip="10.0.0.5", site=SITE_A), _asset(ip="10.0.0.6", site=None)
    pub = _asset(ip="8.8.8.8", site=None)
    out = asyncio.run(find_assets_batch(_db([a_row, legacy, pub]), ENG,
                                        ["10.0.0.5", "10.0.0.6", "8.8.8.8", "10.0.0.7"],
                                        PER_SITE_A))
    assert out["10.0.0.5"] is a_row
    assert out["10.0.0.6"] is legacy and legacy.site_id == SITE_A      # adopted
    assert out["8.8.8.8"] is pub
    assert "10.0.0.7" not in out


def test_batch_in_global_mode_handles_duplicate_rows():
    first, second = _asset(age=0), _asset(age=3)
    out = asyncio.run(find_assets_batch(_db([second, first]), ENG, ["10.0.0.5"]))
    assert out["10.0.0.5"] is first
