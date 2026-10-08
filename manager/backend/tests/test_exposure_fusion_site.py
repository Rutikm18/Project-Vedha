"""
test_exposure_fusion_site.py — P1b-3: exposure fusion is per ASSET, not per raw IP.

Fusion compares vantages for ONE host. With `per_site` identity a private address
at site A and the same address at site B are two machines, so what site A's probes
saw must never be stamped onto site B's services (and vice versa). A globally
routable address is one host wherever it is seen, so an external probe and an
internal one still fuse. In `global` mode nothing changes.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.detection.exposure_fusion_service import recompute_fused_exposure, scoped_results

SITE_A, SITE_B, SITE_X = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
AGENT_A, AGENT_B, AGENT_EXT = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()


def _fact(ip, vantage, status, port="tcp/443", external=()):
    return {"scanner": "exposure_matrix", "target": ip,
            "data": {"ports": {port: {"by_vantage": {vantage: status}}}, "external_vantages": list(external)}}


# ── the grouping ─────────────────────────────────────────────────────────────

def test_global_mode_never_splits_by_site():
    rows = [(AGENT_A, SITE_A, [_fact("10.0.0.5", "lan-a", "open")]),
            (AGENT_B, SITE_B, [_fact("10.0.0.5", "lan-b", "closed")])]
    scoped = scoped_results(rows, "global")
    assert list(scoped) == [None]
    assert len(scoped[None]) == 2                       # both probes' views, fused together as before


def test_per_site_private_ip_is_fused_only_with_its_own_site():
    rows = [(AGENT_A, SITE_A, [_fact("10.0.0.5", "lan-a", "open")]),
            (AGENT_B, SITE_B, [_fact("10.0.0.5", "lan-b", "closed")])]
    scoped = scoped_results(rows, "per_site")
    assert set(scoped) == {SITE_A, SITE_B}
    assert all(len(v) == 1 for v in scoped.values())


def test_per_site_public_ip_still_fuses_every_vantage():
    rows = [(AGENT_A, SITE_A, [_fact("8.8.8.8", "lan-a", "closed")]),
            (AGENT_EXT, SITE_X, [_fact("8.8.8.8", "internet", "open", external=["internet"])])]
    scoped = scoped_results(rows, "per_site")
    assert list(scoped) == [None] and len(scoped[None]) == 2


def test_a_probe_with_no_site_stays_global_in_per_site_mode():
    scoped = scoped_results([(AGENT_A, None, [_fact("10.0.0.5", "lan", "open")])], "per_site")
    assert list(scoped) == [None]


def test_one_probe_can_contribute_to_several_scopes():
    rows = [(AGENT_A, SITE_A, [_fact("10.0.0.5", "lan-a", "open"), _fact("8.8.8.8", "lan-a", "closed")])]
    assert set(scoped_results(rows, "per_site")) == {SITE_A, None}


def test_non_exposure_and_malformed_facts_are_ignored():
    rows = [(AGENT_A, SITE_A, [{"scanner": "banner", "target": "10.0.0.5"}, "junk", None,
                               {"scanner": "exposure_matrix", "target": "", "data": {}}])]
    assert scoped_results(rows, "per_site") == {}


# ── the stamping, against a fake session ─────────────────────────────────────

NOW = datetime.now(timezone.utc)


def _asset(ip, site=None, age=0):
    return SimpleNamespace(id=uuid.uuid4(), ip_address=ip, site_id=site, created_at=NOW - timedelta(minutes=age))


def _svc(asset, port=443, exposure=None):
    return SimpleNamespace(asset_id=asset.id, port=port, protocol="tcp", exposure=exposure)


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows

    def scalars(self):
        return SimpleNamespace(all=lambda: self._rows)


class FakeDB:
    def __init__(self, roe, rows, assets, services):
        self.engagement = SimpleNamespace(rules_of_engagement=roe)
        self.rows, self.assets, self.services = rows, assets, services

    async def get(self, model, key):
        return self.engagement

    async def execute(self, stmt):
        sql = str(stmt).lower()
        if "from scan_results" in sql:
            return _Result(self.rows)
        if "from assets" in sql:
            return _Result(self.assets)
        if "from services" in sql:
            wanted = set(stmt.compile().params.values())
            return _Result([s for s in self.services if s.asset_id in wanted])
        raise AssertionError(sql)

    async def flush(self):
        pass


def _run(db):
    return asyncio.run(recompute_fused_exposure(db, uuid.uuid4()))


def test_per_site_exposure_lands_on_the_right_machine():
    a, b = _asset("10.0.0.5", SITE_A), _asset("10.0.0.5", SITE_B)
    sa, sb = _svc(a), _svc(b)
    rows = [(AGENT_A, SITE_A, [_fact("10.0.0.5", "lan-a", "open")]),
            (AGENT_B, SITE_B, [_fact("10.0.0.5", "lan-b", "closed")])]
    changed = _run(FakeDB({"asset_identity": "per_site"}, rows, [a, b], [sa, sb]))
    assert changed == 2
    assert sa.exposure == "internal_only"               # site A's probe saw it open
    assert sb.exposure == "not_exposed"                 # site B's machine is a different host: closed there


def test_global_mode_keeps_the_old_behaviour_one_fused_verdict_per_ip():
    a = _asset("10.0.0.5")
    s = _svc(a)
    rows = [(AGENT_A, SITE_A, [_fact("10.0.0.5", "lan-a", "open")]),
            (AGENT_B, SITE_B, [_fact("10.0.0.5", "lan-b", "closed")])]
    _run(FakeDB({}, rows, [a], [s]))
    assert s.exposure == "internal_only"


def test_an_external_probe_marks_a_public_host_external_even_in_per_site_mode():
    host = _asset("8.8.8.8")
    s = _svc(host, port=80)
    rows = [(AGENT_A, SITE_A, [_fact("8.8.8.8", "lan-a", "closed", port="tcp/80")]),
            (AGENT_EXT, SITE_X, [_fact("8.8.8.8", "internet", "open", port="tcp/80", external=["internet"])])]
    _run(FakeDB({"asset_identity": "per_site"}, rows, [host], [s]))
    assert s.exposure == "external"


def test_a_legacy_unscoped_asset_is_stamped_until_a_site_adopts_it():
    legacy = _asset("10.0.0.5", None)
    s = _svc(legacy)
    rows = [(AGENT_A, SITE_A, [_fact("10.0.0.5", "lan-a", "open")])]
    _run(FakeDB({"asset_identity": "per_site"}, rows, [legacy], [s]))
    assert s.exposure == "internal_only"


def test_another_sites_observation_does_not_touch_a_machine_it_never_saw():
    a_only = _asset("10.0.0.5", SITE_A)                  # site B has no asset (and no row) for this address
    s = _svc(a_only)
    rows = [(AGENT_B, SITE_B, [_fact("10.0.0.5", "lan-b", "open")])]
    changed = _run(FakeDB({"asset_identity": "per_site"}, rows, [a_only], [s]))
    assert changed == 0 and s.exposure is None


def test_a_failure_is_swallowed_and_reported_as_zero():
    class Boom(FakeDB):
        async def execute(self, stmt):
            raise RuntimeError("db down")
    assert _run(Boom({}, [], [], [])) == 0
