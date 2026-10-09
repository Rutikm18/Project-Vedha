"""
GET /attack-paths/overview — the tenant-wide, read-only summary the dashboard shows.

Pure row builder first (never computed != zero routes; an empty row keeps its reasons;
nothing is invented), then the route (operators only, tenant-scoped, labels looked up
in two bounded queries) with a scripted fake database.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.graph.overview import FIX_ASSETS_SHOWN, build_row, fix_asset_ids, row_sort_key
from app.routers import attack_paths as R

NOW = datetime(2026, 10, 9, 9, 0, tzinfo=timezone.utc)


def _analysis(*, fix=("a", "b"), targets=2, entry=2, coverage="partial", stale=1, reasons=None):
    return {
        "choke": {"entry_points": entry, "targets": [{"asset_id": f"t{i}"} for i in range(targets)],
                  "min_fix_set": {"size": len(fix), "assets": list(fix), "independent_routes": {}}},
        "coverage": {"confidence": coverage} if coverage else None,
        "freshness": {"stale_assets": stale} if stale is not None else None,
        "diagnostics": {"reasons": reasons or []},
    }


def _row(analysis, count=6, labels=None, name="Acme"):
    return build_row(engagement_id=uuid.UUID(int=1), name=name, status="active",
                     computed_at=NOW if analysis is not None else None, path_count=count,
                     analysis=analysis, labels=labels)


# ── the row ──────────────────────────────────────────────────────────────────

def test_never_computed_is_not_zero_routes():
    row = _row(None, count=None)
    assert row["computed"] is False
    assert row["path_count"] is None and row["fix_set_size"] is None       # no number is invented
    assert row["computed_at"] is None and row["coverage"] is None and row["why_empty"] == []


def test_computed_row_carries_the_facts_and_names_the_fix_hosts():
    row = _row(_analysis(), labels={"a": "vpn-gw", "b": "web-1"})
    assert row["computed"] is True and row["path_count"] == 6
    assert row["entry_points"] == 2 and row["crown_jewels"] == 2
    assert row["fix_set_size"] == 2 and row["fix_assets"] == ["vpn-gw", "web-1"] and row["fix_assets_more"] == 0
    assert row["coverage"] == "partial" and row["stale_assets"] == 1
    assert row["computed_at"] == NOW.isoformat() and row["status"] == "active"
    assert row["why_empty"] == []


def test_a_long_fix_set_names_a_few_hosts_and_counts_the_rest():
    ids = [f"h{i}" for i in range(7)]
    row = _row(_analysis(fix=ids), labels={i: i.upper() for i in ids})
    assert row["fix_set_size"] == 7
    assert row["fix_assets"] == ["H0", "H1", "H2"] and row["fix_assets_more"] == 4
    assert fix_asset_ids(_analysis(fix=ids)) == (ids[:FIX_ASSETS_SHOWN], 4)


def test_a_host_with_no_label_falls_back_to_its_id_rather_than_vanishing():
    assert _row(_analysis(fix=("zz",)), labels={})["fix_assets"] == ["zz"]


def test_zero_routes_keeps_the_reasons_the_analysis_recorded():
    reasons = [{"code": "no_targets", "detail": "no crown-jewel target: no asset in this engagement is marked critical"},
               {"code": "no_entry_points", "detail": "no asset is internet-exposed"}]
    row = _row(_analysis(fix=(), targets=0, entry=0, reasons=reasons), count=0)
    assert row["computed"] is True and row["path_count"] == 0
    assert [r["code"] for r in row["why_empty"]] == ["no_targets", "no_entry_points"]


def test_reasons_are_only_attached_to_an_empty_result():
    reasons = [{"code": "no_targets", "detail": "x"}]
    assert _row(_analysis(reasons=reasons), count=3)["why_empty"] == []


def test_missing_reports_stay_missing_not_clean():
    row = _row(_analysis(coverage=None, stale=None))
    assert row["coverage"] is None and row["stale_assets"] is None


def test_sort_puts_routes_first_then_empty_then_never_computed():
    rows = [_row(None, count=None, name="Never"), _row(_analysis(), count=0, name="Empty"),
            _row(_analysis(), count=2, name="Few"), _row(_analysis(), count=9, name="Many"),
            _row(_analysis(), count=2, name="Alpha")]
    assert [r["name"] for r in sorted(rows, key=row_sort_key)] == ["Many", "Alpha", "Few", "Empty", "Never"]


# ── the route ────────────────────────────────────────────────────────────────

def test_the_route_is_registered_beta_and_read_only():
    paths = {(r.path, tuple(sorted(r.methods))) for r in R.overview_router.routes}
    assert ("/attack-paths/overview", ("GET",)) in paths
    assert R.overview_router.tags == ["attack-paths (beta)"]
    # The app exposes it (this FastAPI wraps included routers, so read the OpenAPI document).
    from app.main import app
    op = app.openapi()["paths"]["/attack-paths/overview"]
    assert list(op) == ["get"] and op["get"]["tags"] == ["attack-paths (beta)"]


def _role_check():
    route = next(r for r in R.overview_router.routes if r.path == "/attack-paths/overview")
    calls = [d.call for d in route.dependant.dependencies if "check" in getattr(d.call, "__name__", "")]
    assert len(calls) == 1, "the overview must require an operator role"
    return calls[0]


@pytest.mark.parametrize("role", R.OVERVIEW_ROLES)
def test_operator_roles_are_allowed(role):
    user = SimpleNamespace(role=role, tenant_id=uuid.uuid4())
    assert asyncio.run(_role_check()(user)) is user


@pytest.mark.parametrize("role", ["client", "agent", "anonymous"])
def test_customer_and_machine_roles_are_refused(role):
    with pytest.raises(HTTPException) as exc:
        asyncio.run(_role_check()(SimpleNamespace(role=role, tenant_id=uuid.uuid4())))
    assert exc.value.status_code == 403


class _Result:
    def __init__(self, rows=(), scalar=None):
        self._rows, self._scalar = list(rows), scalar

    def all(self):
        return self._rows

    def scalar_one(self):
        return self._scalar

    def scalars(self):
        return self


class _ScriptedDB:
    """Returns one scripted result per execute(), in order, and records the SQL."""

    def __init__(self, *results):
        self._results, self.sql = list(results), []

    async def execute(self, stmt, params=None):
        self.sql.append(str(stmt))
        return self._results.pop(0)


def _call(db, user=None, limit=50):
    user = user or SimpleNamespace(role="admin", tenant_id=uuid.UUID(int=77))
    return asyncio.run(R.attack_paths_overview(db=db, current_user=user, limit=limit))


E1, E2, E3 = (uuid.UUID(int=i) for i in (11, 12, 13))
A, B = uuid.UUID(int=101), uuid.UUID(int=102)


def test_handler_builds_rows_labels_hosts_and_orders_them():
    picked = [
        (E3, "Never opened", "draft", None, None, None),
        (E2, "Quiet", "active", NOW, 0, _analysis(fix=(), targets=0, entry=0,
                                                   reasons=[{"code": "no_targets", "detail": "x"}])),
        (E1, "Acme", "active", NOW, 6, _analysis(fix=(str(A), str(B)))),
    ]
    db = _ScriptedDB(
        _Result(scalar=3),                                                     # engagement count
        _Result(rows=picked),                                                  # engagements + analyses
        _Result(rows=[(A, E1, "vpn-gw", "10.0.0.5", None), (B, E1, None, "10.0.0.9", None)]),   # the named hosts
        _Result(rows=[(A, E1, "vpn-gw", "10.0.0.5", None), (B, E1, None, "10.0.0.9", None)]),   # peers sharing a label
    )
    out = _call(db)
    assert out["total"] == 3 and out["shown"] == 3
    assert [r["name"] for r in out["engagements"]] == ["Acme", "Quiet", "Never opened"]
    acme = out["engagements"][0]
    assert acme["fix_assets"] == ["vpn-gw", "10.0.0.9"]                        # hostname, else address
    assert out["engagements"][1]["why_empty"][0]["code"] == "no_targets"
    assert out["engagements"][2]["computed"] is False


def test_handler_is_tenant_scoped_and_never_computes():
    db = _ScriptedDB(_Result(scalar=0), _Result(rows=[]))
    out = _call(db, user=SimpleNamespace(role="manager", tenant_id=uuid.UUID(int=77)))
    assert out == {"total": 0, "shown": 0, "engagements": []}
    assert len(db.sql) == 2 and all("engagements.tenant_id" in q for q in db.sql)
    assert not any("INSERT" in q.upper() or "UPDATE" in q.upper() or "DELETE" in q.upper() for q in db.sql)


def test_a_label_two_sites_share_gets_its_site_appended():
    site_x, site_y = uuid.UUID(int=901), uuid.UUID(int=902)
    rows = [(A, E1, None, "10.0.0.5", site_x), (B, E1, None, "10.0.0.5", site_y)]
    sites = [SimpleNamespace(id=site_x, name="HQ"), SimpleNamespace(id=site_y, name="Branch")]
    db = _ScriptedDB(_Result(rows=[rows[0]]), _Result(rows=rows), _Result(rows=sites))
    labels = asyncio.run(R._fix_asset_labels(db, {E1: [str(A)]}))
    assert labels[E1][str(A)] == "10.0.0.5 @ HQ"                               # not ambiguous with Branch's 10.0.0.5


def test_no_named_hosts_means_no_label_queries():
    db = _ScriptedDB()
    assert asyncio.run(R._fix_asset_labels(db, {})) == {}
    assert db.sql == []
