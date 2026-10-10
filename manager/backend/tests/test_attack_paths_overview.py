"""
GET /attack-paths/overview and GET /attack-paths/focus/{id} — what the dashboard says.

The expectations come from the analyzer run on the repo's validation fixtures (real
output, not hand-made dicts), because the failures this guards against were found that
way: a crown jewel that is itself exposed was told "fix the gateway", an exposed-only
engagement read "No routes modelled", and a route count that tracks entry points was
the headline.

Pure row/summary/focus builders first, then the two routes against a scripted database.
"""
from __future__ import annotations

import asyncio
import copy
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.graph.analyzer import PathAnalyzer
from app.graph.coverage import coverage_report, freshness_report
from app.graph.overview import (
    EXPOSED, FIX_ASSETS_SHOWN, NO_TARGETS, NOT_COMPUTED, REACHABLE, UNRECORDED, UNREACHABLE,
    build_focus, build_row, build_summary, classify, fix_asset_ids, fix_point_ids, jewel_facts,
    risk_share, row_sort_key,
)
from app.graph.validation import build_graph
from app.routers import attack_paths as R

FIXTURES = Path(__file__).parent / "fixtures" / "attack_paths"
NOW = datetime(2026, 10, 9, 9, 0, tzinfo=timezone.utc)


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / f"{name}.json").read_text())


def _analyse(fx: dict, targets: list[str] | None = None):
    """(stored-shaped analysis, stored path rows) exactly as `_recompute_and_store` builds them."""
    graph = build_graph(fx)
    analyzer = PathAnalyzer(graph)
    wanted = list(fx["targets"]) if targets is None else targets
    paths = [p for t in wanted for p in analyzer.find_paths_to_target(t)]
    paths.sort(key=lambda p: p["risk_score"], reverse=True)
    analysis = {"choke": analyzer.choke_analysis(wanted), "coverage": coverage_report(graph),
                "freshness": freshness_report(graph), "diagnostics": analyzer.diagnose(wanted)}
    return analysis, paths


def _exposed_jewel(fx: dict, *, only: bool) -> dict:
    """The fixture with its crown jewel itself exposed (and exploitable). `only` also
    removes the exposure of every entry host, so the jewel is the single way in."""
    out = copy.deepcopy(fx)
    entry = next(a for a in out["assets"] if a.get("environment") == "dmz")
    for a in out["assets"]:
        if only and a is not entry and a.get("environment") == "dmz":
            a.pop("environment")
        if a["id"] == out["targets"][0]:
            a["environment"] = "dmz"
    if only:
        entry.pop("environment")
    out["exploitable"] = sorted(set(out["exploitable"]) | {out["targets"][0]})
    return out


def _row(fx_or_analysis, count=None, name="Acme", labels=None):
    analysis, paths = _analyse(fx_or_analysis) if isinstance(fx_or_analysis, dict) and "assets" in fx_or_analysis \
        else (fx_or_analysis, [])
    return build_row(engagement_id=uuid.UUID(int=1), name=name, status="active",
                     computed_at=NOW if analysis is not None else None,
                     path_count=len(paths) if count is None else count, analysis=analysis, labels=labels)


# ── states, from real analyzer output ────────────────────────────────────────

def test_eight_entries_behind_one_gateway_is_one_host_to_fix_not_eight_routes():
    row = _row(_fixture("09_single_bottleneck_many_entries"))
    assert row["state"] == REACHABLE
    assert (row["jewels_total"], row["jewels_reachable"], row["jewels_exposed"]) == (1, 1, 0)
    assert row["fix_set_size"] == 1 and row["fix_assets"] == ["gw"] and row["ways_in"] == 1
    assert row["path_count"] == 8                 # the capped list tracks the entry points; it is not the headline


def test_two_independent_routes_need_two_fixes_and_say_so():
    row = _row(_fixture("08_redundant_routes"))
    assert row["state"] == REACHABLE and row["fix_set_size"] == 2 and row["ways_in"] == 2
    assert sorted(row["fix_assets"]) == ["gw1", "gw2"]


def test_a_jewel_that_is_itself_exposed_is_exposed_not_fixable_by_its_gateway():
    fx = _exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=False)
    analysis, _ = _analyse(fx)
    assert analysis["choke"]["targets"][0]["exposed_directly"] is True
    row = _row(fx)
    assert row["state"] == EXPOSED and row["jewels_exposed"] == 1 and row["jewels_reachable"] == 1
    assert row["ways_in"] is None                  # "1 separate way in" would be false: it is exposed outright
    assert row["why_empty"] == []


def test_an_exposed_only_engagement_is_exposed_not_no_routes():
    """Zero stored routes (a route needs a different entry) must not read as 'nothing modelled'."""
    fx = _exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=True)
    analysis, paths = _analyse(fx)
    assert paths == [] and analysis["choke"]["targets"][0]["best_likelihood"] == 1.0
    row = _row(fx)
    assert row["state"] == EXPOSED and row["path_count"] == 0 and row["top_risk"] == 100.0
    assert row["why_empty"] == []


def test_a_jewel_nothing_reaches_is_unreachable_and_keeps_its_reasons():
    row = _row(_fixture("05_exposure_is_not_ownership"))
    assert row["state"] == UNREACHABLE and row["jewels_total"] == 1 and row["jewels_reachable"] == 0
    assert row["ways_in"] is None and row["path_count"] == 0


def test_no_crown_jewel_marked_is_its_own_state():
    fx = _fixture("09_single_bottleneck_many_entries")
    analysis, _ = _analyse(fx, targets=[])
    assert analysis["choke"]["targets"] == []
    row = _row(analysis, count=0)
    assert row["state"] == NO_TARGETS and row["jewels_total"] == 0 and row["jewels_reachable"] == 0


def test_never_computed_is_not_zero_anything():
    row = _row(None, count=None)
    assert row["state"] == NOT_COMPUTED and row["computed"] is False
    assert row["path_count"] is None and row["jewels_total"] is None and row["jewels_reachable"] is None
    assert row["fix_set_size"] is None and row["computed_at"] is None and row["why_empty"] == []


def test_missing_per_jewel_data_is_unknown_not_zero():
    row = _row({"choke": {"entry_points": 2, "min_fix_set": {"size": 1, "assets": ["a"], "independent_routes": {}}},
                "coverage": None, "freshness": None, "diagnostics": {"reasons": []}}, count=3)
    assert row["state"] == UNRECORDED
    assert row["jewels_total"] is None and row["jewels_reachable"] is None and row["jewels_exposed"] is None
    one_missing = {"choke": {"targets": [{"asset_id": "j", "risk": 12.0}]}}          # no best_likelihood
    assert classify(one_missing) == UNRECORDED and jewel_facts(one_missing) is None


def test_analyses_stored_before_exposed_directly_existed_still_classify():
    analysis, _ = _analyse(_exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=False))
    for t in analysis["choke"]["targets"]:
        t.pop("exposed_directly")                  # as stored before the flag existed
    assert classify(analysis) == EXPOSED           # a likelihood of 1.0 can only mean "its own entry point"
    plain, _ = _analyse(_fixture("09_single_bottleneck_many_entries"))
    for t in plain["choke"]["targets"]:
        t.pop("exposed_directly", None)
    assert classify(plain) == REACHABLE


def test_a_long_fix_set_names_a_few_hosts_and_counts_the_rest():
    ids = [f"h{i}" for i in range(7)]
    analysis = {"choke": {"targets": [{"asset_id": "j", "best_likelihood": 0.5, "risk": 50.0}],
                          "min_fix_set": {"size": 7, "assets": ids, "independent_routes": {"j": 7}}}}
    row = _row(analysis, count=9, labels={i: i.upper() for i in ids})
    assert row["fix_set_size"] == 7 and row["fix_assets"] == ["H0", "H1", "H2"] and row["fix_assets_more"] == 4
    assert fix_asset_ids(analysis) == (ids[:FIX_ASSETS_SHOWN], 4)


def test_a_host_with_no_label_falls_back_to_its_id_rather_than_vanishing():
    analysis = {"choke": {"targets": [{"asset_id": "j", "best_likelihood": 0.5, "risk": 5.0}],
                          "min_fix_set": {"size": 1, "assets": ["zz"], "independent_routes": {"j": 1}}}}
    assert _row(analysis, count=1, labels={})["fix_assets"] == ["zz"]


def test_coverage_and_staleness_stay_as_recorded_or_missing():
    row = _row(_fixture("09_single_bottleneck_many_entries"))
    assert row["coverage"] in ("observed", "partial")
    bare = _row({"choke": {"targets": [{"asset_id": "j", "best_likelihood": 0.5, "risk": 5.0}]}}, count=1)
    assert bare["coverage"] is None and bare["stale_assets"] is None


# ── ordering and the summary ─────────────────────────────────────────────────

def _state_row(name, state, reachable=0, risk=0.0, fix=None):
    return {"name": name, "state": state, "computed": state != NOT_COMPUTED, "jewels_reachable": reachable,
            "top_risk": risk, "fix_set_size": fix, "jewels_total": reachable or None}


def test_sort_puts_exposed_first_then_most_reachable_then_the_unassessable_last():
    rows = [_state_row("Never", NOT_COMPUTED), _state_row("None marked", NO_TARGETS),
            _state_row("Unknown", UNRECORDED), _state_row("Nothing", UNREACHABLE),
            _state_row("Few", REACHABLE, 1, 40), _state_row("Many", REACHABLE, 3, 10),
            _state_row("Many risky", REACHABLE, 3, 60), _state_row("Exposed", EXPOSED, 1, 100)]
    assert [r["name"] for r in sorted(rows, key=row_sort_key)] == [
        "Exposed", "Many risky", "Many", "Few", "Nothing", "Unknown", "None marked", "Never"]


def test_sort_never_uses_the_capped_route_count():
    a = _row(_fixture("09_single_bottleneck_many_entries"), name="Eight entries")     # 8 stored routes
    b = _row(_fixture("08_redundant_routes"), name="Two ways in")                      # 4 stored routes
    assert a["path_count"] > b["path_count"]
    assert [r["name"] for r in sorted([b, a], key=row_sort_key)] == ["Eight entries", "Two ways in"]   # by name: equal on the facts


def test_summary_counts_engagements_not_assets():
    rows = [_row(_fixture("09_single_bottleneck_many_entries"), name="A"),
            _row(_fixture("08_redundant_routes"), name="B"),
            _row(_exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=True), name="C"),
            _row(_fixture("05_exposure_is_not_ownership"), name="D"),
            _row(_analyse(_fixture("09_single_bottleneck_many_entries"), targets=[])[0], count=0, name="E"),
            _row(None, count=None, name="F")]
    s = build_summary(rows)
    assert s == {"engagements": 6, "computed": 5, "assessed": 4, "with_reachable": 3, "exposed": 1, "single_fix": 1,
                 "not_computed": 1, "no_targets": 1, "unrecorded": 0, "jewels_total": 4, "jewels_reachable": 3,
                 "compared": 0, "changed": 0}


# ── the focus card's data ────────────────────────────────────────────────────

def _route(paths):
    top = paths[0]
    return {"id": uuid.uuid4(), "risk_score": top["risk_score"], "freshness": "fresh",
            "nodes": top["nodes"], "edges": top["edges"]}


def test_focus_tags_roles_and_only_marks_hosts_on_the_fix_list():
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    focus = build_focus(engagement_id=uuid.UUID(int=1), name="Acme", computed_at=NOW, analysis=analysis,
                        path_count=len(paths), route=_route(paths), labels={"gw": "edge-gw-01"})
    nodes = focus["route"]["nodes"]
    assert [n["role"] for n in nodes] == ["entry", "via", "jewel"]
    assert [n["label"] for n in nodes][1] == "edge-gw-01"
    assert [n["on_fix_list"] for n in nodes] == [False, True, False]
    assert len(focus["route"]["hops"]) == 2 and focus["fix"]["size"] == 1
    assert focus["ranked"][0]["label"] == "edge-gw-01" and focus["ranked"][0]["share"] == 1.0
    assert focus["ranked"][0]["cuts_off"] == 1


def test_focus_marks_nothing_when_no_route_host_is_on_the_fix_list():
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    analysis["choke"]["min_fix_set"]["assets"] = ["somewhere-else"]
    analysis["choke"]["ranked"] = []
    focus = build_focus(engagement_id=uuid.UUID(int=1), name="Acme", computed_at=NOW, analysis=analysis,
                        path_count=len(paths), route=_route(paths), labels={})
    assert not any(n["on_fix_list"] for n in focus["route"]["nodes"])


def test_focus_for_an_exposed_only_engagement_names_the_jewel_and_draws_no_route():
    fx = _exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=True)
    analysis, paths = _analyse(fx)
    focus = build_focus(engagement_id=uuid.UUID(int=1), name="Hooli", computed_at=NOW, analysis=analysis,
                        path_count=0, route=None, labels={"jewel": "fin-db-01"})
    assert focus["state"] == EXPOSED and focus["route"] is None and focus["ranked"] == []
    assert focus["exposed"] == [{"asset_id": "jewel", "label": "fin-db-01"}]


def test_focus_for_a_never_computed_engagement_is_just_that():
    focus = build_focus(engagement_id=uuid.UUID(int=1), name="Umbrella", computed_at=None, analysis=None,
                        path_count=None, route=None, labels={})
    assert focus["state"] == NOT_COMPUTED and focus["computed"] is False and focus["route"] is None
    assert focus["fix"] is None and focus["path_count"] is None


def test_risk_removed_is_not_bounded_but_the_share_is():
    """Three crown jewels behind one gateway: the raw figure is the sum over jewels."""
    fx = _fixture("09_single_bottleneck_many_entries")
    fx["assets"] += [{"id": "jewel2", "ip": "10.0.2.30", "criticality": "critical"},
                     {"id": "jewel3", "ip": "10.0.2.31", "criticality": "critical"}]
    fx["exploitable"] += ["jewel2", "jewel3"]
    fx["targets"] = ["jewel", "jewel2", "jewel3"]
    analysis, _ = _analyse(fx)
    gw = analysis["choke"]["ranked"][0]
    assert gw["risk_removed"] == pytest.approx(36.45)                 # 3 x 12.15
    assert risk_share(gw, analysis["choke"]["targets"]) == 1.0        # all of the modelled risk, never more
    assert risk_share({"risk_removed": 999}, analysis["choke"]["targets"]) == 1.0
    assert risk_share(gw, []) is None                                  # no modelled risk to take a share of


def test_fix_point_ids_are_the_fix_set_plus_the_top_hosts_by_risk_removed():
    choke = {"min_fix_set": {"assets": ["a"]}, "ranked": [
        {"asset_id": "b", "risk_removed": 5}, {"asset_id": "c", "risk_removed": 0}, {"asset_id": "d", "risk_removed": 1},
        {"asset_id": "e", "risk_removed": 1}, {"asset_id": "f", "risk_removed": 1}]}
    assert fix_point_ids(choke) == {"a", "b", "d"}                     # first three ranked, and only if they remove any


# ── the routes ───────────────────────────────────────────────────────────────

def test_both_routes_are_registered_beta_and_get_only():
    paths = {(r.path, tuple(sorted(r.methods))) for r in R.overview_router.routes}
    assert ("/attack-paths/overview", ("GET",)) in paths
    assert ("/attack-paths/focus/{engagement_id}", ("GET",)) in paths
    assert R.overview_router.tags == ["attack-paths (beta)"]
    from app.main import app
    spec = app.openapi()["paths"]
    for p in ("/attack-paths/overview", "/attack-paths/focus/{engagement_id}"):
        assert list(spec[p]) == ["get"] and spec[p]["get"]["tags"] == ["attack-paths (beta)"]


def _role_check(path):
    route = next(r for r in R.overview_router.routes if r.path == path)
    calls = [d.call for d in route.dependant.dependencies if "check" in getattr(d.call, "__name__", "")]
    assert len(calls) == 1, f"{path} must require an operator role"
    return calls[0]


ROUTES = ["/attack-paths/overview", "/attack-paths/focus/{engagement_id}"]


@pytest.mark.parametrize("path", ROUTES)
@pytest.mark.parametrize("role", R.OVERVIEW_ROLES)
def test_operator_roles_are_allowed(path, role):
    user = SimpleNamespace(role=role, tenant_id=uuid.uuid4())
    assert asyncio.run(_role_check(path)(user)) is user


@pytest.mark.parametrize("path", ROUTES)
@pytest.mark.parametrize("role", ["client", "agent", "anonymous"])
def test_customer_and_machine_roles_are_refused(path, role):
    with pytest.raises(HTTPException) as exc:
        asyncio.run(_role_check(path)(SimpleNamespace(role=role, tenant_id=uuid.uuid4())))
    assert exc.value.status_code == 403


class _Result:
    def __init__(self, rows=(), scalar=None, one=None):
        self._rows, self._scalar, self._one = list(rows), scalar, one

    def all(self):
        return self._rows

    def first(self):
        return self._rows[0] if self._rows else None

    def scalar_one(self):
        return self._scalar

    def scalar_one_or_none(self):
        return self._one

    def scalars(self):
        return self


class _ScriptedDB:
    """One scripted result per execute(), in order; get() answers from a dict. Records the SQL."""

    def __init__(self, *results, got=None):
        self._results, self._got, self.sql, self.stmts = list(results), got or {}, [], []

    async def execute(self, stmt, params=None):
        self.sql.append(str(stmt))
        self.stmts.append(stmt)
        return self._results.pop(0)

    async def get(self, model, key):
        self.sql.append(f"GET {model.__name__}")
        return self._got.get(model.__name__)


def _only_reads(db) -> bool:
    """Every statement the route issued is a SELECT (a column called `updated_at` is not a write)."""
    return all(s.lstrip().lower().startswith(("select", "get ")) for s in db.sql)


E1, E2, E3 = (uuid.UUID(int=i) for i in (11, 12, 13))
A, B = uuid.UUID(int=101), uuid.UUID(int=102)
SINGLE = [{"asset_id": str(A), "best_likelihood": 0.5, "exposed_directly": False, "risk": 50.0}]


def _picked(eid, name, targets=None, fix=None, count=0, at=NOW, status="active", cov="partial", stale=0, reasons=None):
    """One row of the overview's projected query: ids, then the sub-keys of the analysis."""
    return (eid, name, status, at, count, targets, fix, 2, cov, stale, reasons or [])


def _call(db, user=None, limit=50):
    user = user or SimpleNamespace(role="admin", tenant_id=uuid.UUID(int=77))
    return asyncio.run(R.attack_paths_overview(db=db, current_user=user, limit=limit))


def test_handler_ranks_every_engagement_before_it_applies_the_limit():
    """The best engagement is the OLDEST: a limit applied in SQL order would drop it."""
    never = (E3, "Never opened", "draft", None, None, None, None, None, None, None, None)
    quiet = _picked(E2, "Quiet", targets=[{"asset_id": "x", "best_likelihood": 0.0, "risk": 0.0}],
                    fix={"size": 0, "assets": [], "independent_routes": {}})
    acme = _picked(E1, "Acme", targets=SINGLE, count=8,
                   fix={"size": 1, "assets": [str(A)], "independent_routes": {str(A): 1}})
    db = _ScriptedDB(_Result(rows=[never, quiet, acme]),                                        # newest first
                     _Result(rows=[]),                                                          # history
                     _Result(rows=[(A, E1, "vpn-gw", "10.0.0.5", None)]),                       # the named host
                     _Result(rows=[(A, E1, "vpn-gw", "10.0.0.5", None)]))                       # peers sharing a label
    out = _call(db, limit=1)
    assert out["total"] == 3 and out["shown"] == 1
    assert [r["name"] for r in out["engagements"]] == ["Acme"]
    assert out["engagements"][0]["fix_assets"] == ["vpn-gw"]
    assert out["summary"]["engagements"] == 3 and out["summary"]["not_computed"] == 1
    assert out["summary"]["with_reachable"] == 1 and out["summary"]["truncated"] is False


def test_handler_totals_count_all_engagements_even_when_few_are_shown():
    rows = [_picked(uuid.UUID(int=100 + i), f"E{i}", targets=SINGLE, count=1,
                    fix={"size": 1, "assets": [], "independent_routes": {}}) for i in range(5)]
    out = _call(_ScriptedDB(_Result(rows=rows), _Result(rows=[])), limit=2)
    assert out["shown"] == 2 and out["summary"]["with_reachable"] == 5 and out["summary"]["single_fix"] == 5


def test_handler_reads_only_the_subkeys_it_needs_and_stays_tenant_scoped_and_read_only():
    db = _ScriptedDB(_Result(rows=[]), _Result(rows=[]))
    out = _call(db, user=SimpleNamespace(role="manager", tenant_id=uuid.UUID(int=77)))
    assert out["total"] == 0 and out["engagements"] == [] and out["summary"]["engagements"] == 0
    assert len(db.sql) == 2 and all("engagements.tenant_id" in q for q in db.sql)       # rows, then history
    from sqlalchemy.dialects import postgresql
    sql = str(db.stmts[0].compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})).lower()
    for key in ("'targets'", "'min_fix_set'", "'entry_points'", "'confidence'", "'stale_assets'", "'reasons'"):
        assert key in sql, key                                                       # the sub-keys the rows read
    for key in ("'segments'", "'ranked'", "'scope_without_observed_hosts'"):
        assert key not in sql, key                                                   # not the whole document
    assert _only_reads(db)


def test_handler_labels_hosts_only_for_the_rows_it_returns():
    a = _picked(E1, "Acme", targets=SINGLE, count=1, fix={"size": 1, "assets": [str(A)], "independent_routes": {}})
    b = _picked(E2, "Beta", targets=SINGLE, count=1, fix={"size": 1, "assets": [str(B)], "independent_routes": {}})
    db = _ScriptedDB(_Result(rows=[a, b]), _Result(rows=[]), _Result(rows=[(A, E1, "a-host", "10.0.0.5", None)]),
                     _Result(rows=[(A, E1, "a-host", "10.0.0.5", None)]))
    out = _call(db, limit=1)
    assert out["engagements"][0]["name"] == "Acme" and len(db.sql) == 4          # rows, history, two label queries
    assert str(B) not in " ".join(db.sql)


def test_a_label_two_sites_share_gets_its_site_appended():
    site_x, site_y = uuid.UUID(int=901), uuid.UUID(int=902)
    rows = [(A, E1, None, "10.0.0.5", site_x), (B, E1, None, "10.0.0.5", site_y)]
    sites = [SimpleNamespace(id=site_x, name="HQ"), SimpleNamespace(id=site_y, name="Branch")]
    db = _ScriptedDB(_Result(rows=[rows[0]]), _Result(rows=rows), _Result(rows=sites))
    labels = asyncio.run(R._fix_asset_labels(db, {E1: [str(A)]}))
    assert labels[E1][str(A)] == "10.0.0.5 @ HQ"


def test_no_named_hosts_means_no_label_queries():
    db = _ScriptedDB()
    assert asyncio.run(R._fix_asset_labels(db, {})) == {} and db.sql == []


# ── the focus route never computes and never writes ──────────────────────────

def _focus(db, eid=E1, user=None):
    user = user or SimpleNamespace(role="analyst", tenant_id=uuid.UUID(int=77))
    return asyncio.run(R.attack_paths_focus(engagement_id=eid, db=db, current_user=user))


@pytest.fixture
def no_compute(monkeypatch):
    async def boom(*a, **k):
        raise AssertionError("the focus route must never compute")
    for name in ("_recompute_and_store", "_build_analyzer", "_store_analysis"):
        monkeypatch.setattr(R, name, boom)


def test_focus_answers_from_the_stored_analysis_without_computing(no_compute):
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    top = SimpleNamespace(id=uuid.uuid4(), risk_score=paths[0]["risk_score"], path_nodes=paths[0]["nodes"],
                          path_edges=paths[0]["edges"])
    stored = SimpleNamespace(computed_at=NOW, path_count=len(paths), analysis=analysis)
    db = _ScriptedDB(_Result(one=SimpleNamespace(id=E1, name="Acme")),                 # the tenant-scoped engagement
                     _Result(rows=[top]),                                                # the top stored route
                     _Result(rows=[]),                                                   # labels: assets
                     got={"AttackPathAnalysis": stored})
    out = _focus(db)
    assert out["state"] == REACHABLE and out["route"]["nodes"][1]["on_fix_list"] is True
    assert _only_reads(db)


def test_focus_for_an_exposed_only_engagement_has_no_stored_route_and_still_answers(no_compute):
    analysis, _ = _analyse(_exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=True))
    stored = SimpleNamespace(computed_at=NOW, path_count=0, analysis=analysis)
    db = _ScriptedDB(_Result(one=SimpleNamespace(id=E1, name="Hooli")), _Result(rows=[]), _Result(rows=[]),
                     got={"AttackPathAnalysis": stored})
    out = _focus(db)
    assert out["state"] == EXPOSED and out["route"] is None and out["exposed"][0]["asset_id"] == "jewel"


def test_focus_for_a_never_computed_engagement_computes_nothing(no_compute):
    db = _ScriptedDB(_Result(one=SimpleNamespace(id=E1, name="Umbrella")), got={})
    out = _focus(db)
    assert out["state"] == NOT_COMPUTED and out["computed"] is False


def test_focus_is_tenant_scoped_and_404s_for_another_tenants_engagement(no_compute):
    db = _ScriptedDB(_Result(one=None))
    with pytest.raises(HTTPException) as exc:
        _focus(db)
    assert exc.value.status_code == 404 and "engagements.tenant_id" in db.sql[0]


# ── history: snapshots, retention, trend ─────────────────────────────────────

from datetime import timedelta  # noqa: E402

from app.graph.overview import (  # noqa: E402
    HISTORY_POINTS, MAX_SNAPSHOTS_PER_ENGAGEMENT, snapshot_facts, snapshots_to_prune, trend,
)


def test_a_snapshot_holds_the_headline_numbers_of_one_computation():
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    facts = snapshot_facts(analysis, len(paths))
    assert facts["state"] == REACHABLE
    assert (facts["jewels_total"], facts["jewels_reachable"], facts["jewels_exposed"]) == (1, 1, 0)
    assert (facts["fix_set_size"], facts["entry_points"], facts["path_count"]) == (1, 8, 8)
    assert facts["assets_seen"] and facts["coverage"] in ("observed", "partial")


def test_a_snapshot_of_an_exposed_or_unrecorded_analysis_keeps_unknown_as_unknown():
    exposed, _ = _analyse(_exposed_jewel(_fixture("09_single_bottleneck_many_entries"), only=True))
    assert snapshot_facts(exposed, 0)["state"] == EXPOSED and snapshot_facts(exposed, 0)["jewels_exposed"] == 1
    legacy = snapshot_facts({"choke": {"entry_points": 1}}, 3)
    assert legacy["state"] == UNRECORDED
    assert legacy["jewels_total"] is None and legacy["jewels_reachable"] is None and legacy["jewels_exposed"] is None
    assert legacy["fix_set_size"] is None and legacy["coverage"] is None and legacy["assets_seen"] is None


NOW_UTC = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)


def _snap(i, **delta):
    return (f"s{i}", NOW_UTC - timedelta(**delta))


def test_every_computation_of_the_last_week_is_kept():
    rows = [_snap(i, hours=h) for i, h in enumerate([1, 5, 30, 100, 160])]
    assert snapshots_to_prune(rows, NOW_UTC) == []


def test_older_than_a_week_keeps_only_the_latest_of_each_day():
    day10 = datetime(2026, 10, 10, tzinfo=timezone.utc)
    rows = [("a", day10.replace(hour=6)), ("b", day10.replace(hour=18)), ("c", day10.replace(hour=12)),
            ("d", datetime(2026, 10, 9, 8, tzinfo=timezone.utc)), ("recent", NOW_UTC - timedelta(days=2))]
    assert sorted(snapshots_to_prune(rows, NOW_UTC)) == ["a", "c"]          # b (18:00) is the day's last; d is alone on its day


def test_exactly_seven_days_old_is_still_inside_the_week():
    assert snapshots_to_prune([("edge", NOW_UTC - timedelta(days=7)), ("edge2", NOW_UTC - timedelta(days=7, minutes=-1))], NOW_UTC) == []


def test_no_engagement_keeps_more_than_the_cap_and_the_oldest_go_first():
    rows = [(f"s{i}", NOW_UTC - timedelta(minutes=i)) for i in range(MAX_SNAPSHOTS_PER_ENGAGEMENT + 5)]   # all inside the week
    doomed = snapshots_to_prune(rows, NOW_UTC)
    assert len(doomed) == 5 and set(doomed) == {f"s{i}" for i in range(MAX_SNAPSHOTS_PER_ENGAGEMENT, MAX_SNAPSHOTS_PER_ENGAGEMENT + 5)}
    assert snapshots_to_prune([], NOW_UTC) == []


def _pt(day, reachable, exposed=0, seen=10, coverage="observed"):
    return {"at": f"2026-10-{day:02d}T09:00:00+00:00", "state": "reachable", "reachable": reachable, "exposed": exposed,
            "assets_seen": seen, "coverage": coverage}


def test_one_computation_is_no_trend_not_no_change():
    assert trend([]) is None and trend([_pt(1, 2)]) is None


def test_a_computation_without_per_jewel_data_is_a_gap_not_a_zero():
    assert trend([_pt(1, 2), {**_pt(2, 0), "reachable": None, "state": "unrecorded"}]) is None
    assert trend([{**_pt(1, 0), "reachable": None}, _pt(2, 2)]) is None


def test_the_trend_compares_the_last_two_and_calls_a_change_a_change():
    flat = trend([_pt(1, 1), _pt(2, 3), _pt(3, 3)])
    assert flat["changed"] is False and (flat["reachable_from"], flat["reachable_to"]) == (3, 3)
    moved = trend([_pt(1, 3), _pt(2, 4)])
    assert moved["changed"] is True and (moved["reachable_from"], moved["reachable_to"]) == (3, 4)
    assert moved["since"] == "2026-10-01T09:00:00+00:00" and "better" not in str(moved) and "worse" not in str(moved)
    assert trend([_pt(1, 2, exposed=0), _pt(2, 2, exposed=1)])["changed"] is True      # a newly exposed jewel is a change


def test_a_change_that_came_with_different_inputs_says_so():
    assert trend([_pt(1, 1, seen=10), _pt(2, 2, seen=14)])["inputs_changed"] is True      # more hosts seen
    assert trend([_pt(1, 1, coverage="partial"), _pt(2, 2, coverage="observed")])["inputs_changed"] is True
    assert trend([_pt(1, 1), _pt(2, 2)])["inputs_changed"] is False
    assert trend([_pt(1, 1, seen=None), _pt(2, 2, seen=14)])["inputs_changed"] is False   # unknown is not "changed"


def test_a_row_carries_at_most_twelve_points_and_its_change():
    history = [_pt(d, d % 4) for d in range(1, 20)]
    analysis, _ = _analyse(_fixture("09_single_bottleneck_many_entries"))
    row = build_row(engagement_id=uuid.UUID(int=1), name="A", status="active", computed_at=NOW, path_count=1,
                    analysis=analysis, history=history)
    assert len(row["history"]) == HISTORY_POINTS and row["history"][-1] == history[-1]
    assert row["change"]["reachable_to"] == history[-1]["reachable"]
    never = build_row(engagement_id=uuid.UUID(int=2), name="N", status="draft", history=history)
    assert never["history"] == [] and never["change"] is None                      # nothing to say about an uncomputed engagement


def test_the_summary_counts_engagements_with_a_change_to_report():
    analysis, _ = _analyse(_fixture("09_single_bottleneck_many_entries"))
    mk = lambda name, hist: build_row(engagement_id=uuid.uuid4(), name=name, status="active", computed_at=NOW,  # noqa: E731
                                      path_count=1, analysis=analysis, history=hist)
    rows = [mk("moved", [_pt(1, 1), _pt(2, 2)]), mk("flat", [_pt(1, 2), _pt(2, 2)]), mk("new", [_pt(2, 2)]), mk("none", None)]
    s = build_summary(rows)
    assert (s["compared"], s["changed"]) == (2, 1)


# ── history: the database side ───────────────────────────────────────────────

def test_recording_a_snapshot_adds_one_row_and_prunes_what_retention_drops():
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    old = [(uuid.UUID(int=i), NOW_UTC - timedelta(days=30, hours=i)) for i in range(3)]       # three on the same old day
    db = _ScriptedDB(_Result(rows=old), _Result())
    added = []
    db.add = added.append
    async def flush(): return None
    db.flush = flush
    asyncio.run(R._record_snapshot(db, E1, analysis, len(paths), "detection", NOW_UTC))
    snap = added[0]
    assert snap.engagement_id == E1 and snap.trigger == "detection" and snap.computed_at == NOW_UTC
    assert snap.state == REACHABLE and snap.jewels_reachable == 1 and snap.path_count == 8
    assert len(db.sql) == 2 and db.sql[1].lstrip().lower().startswith("delete")                # two older same-day rows go


def test_recording_a_snapshot_deletes_nothing_when_retention_keeps_everything():
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    db = _ScriptedDB(_Result(rows=[(uuid.uuid4(), NOW_UTC - timedelta(hours=2))]))
    db.add = lambda row: None
    async def flush(): return None
    db.flush = flush
    asyncio.run(R._record_snapshot(db, E1, analysis, len(paths), "manual", NOW_UTC))
    assert len(db.sql) == 1


def test_a_recompute_records_its_snapshot_with_the_analysis_timestamp_and_its_trigger():
    from unittest.mock import AsyncMock, patch
    analysis, paths = _analyse(_fixture("09_single_bottleneck_many_entries"))
    graph = build_graph(_fixture("09_single_bottleneck_many_entries"))
    class DB:
        def __init__(self): self.rows = {}
        async def execute(self, *a, **k): return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []), all=lambda: [])
        def add(self, row): pass
        async def flush(self): pass
    async def build(_db, _eid): return PathAnalyzer(graph), graph
    async def targets(_db, _eid, _t): return ["jewel"], {"basis": "operator", "suggested": []}
    store = AsyncMock(return_value=NOW_UTC)
    record = AsyncMock()
    with patch.object(R, "_build_analyzer", build), patch.object(R, "_resolve_targets", targets), \
            patch.object(R, "_lock_engagement_paths", AsyncMock()), patch.object(R, "_store_analysis", store), \
            patch.object(R, "_record_snapshot", record):
        asyncio.run(R._recompute_and_store(DB(), E1, None, trigger="detection"))
    args = record.await_args.args
    assert args[1] == E1 and args[4] == "detection" and args[5] == NOW_UTC
    assert args[2]["choke"]["targets"][0]["asset_id"] == "jewel" and args[3] == 8


def test_history_is_one_tenant_scoped_query_returned_oldest_first():
    at1, at2 = NOW_UTC - timedelta(days=2), NOW_UTC - timedelta(days=1)
    db = _ScriptedDB(_Result(rows=[(E1, at1, "reachable", 2, 0, 10, "partial"), (E1, at2, "exposed", 3, 1, 12, "observed")]))
    out = asyncio.run(R._history_by_engagement(db, uuid.UUID(int=77)))
    assert [p["reachable"] for p in out[E1]] == [2, 3] and out[E1][1]["state"] == "exposed"
    assert out[E1][0]["at"] == at1.isoformat() and out[E1][1]["assets_seen"] == 12
    from sqlalchemy.dialects import postgresql
    sql = str(db.stmts[0].compile(dialect=postgresql.dialect())).lower()
    assert "engagements.tenant_id" in sql and "row_number()" in sql and "partition by" in sql
    assert _only_reads(db)


def test_the_overview_carries_each_rows_history_and_the_summary_counts_changes():
    a = _picked(E1, "Acme", targets=SINGLE, count=1, fix={"size": 1, "assets": [], "independent_routes": {}})
    b = _picked(E2, "Beta", targets=SINGLE, count=1, fix={"size": 1, "assets": [], "independent_routes": {}})
    hist = [(E1, NOW - timedelta(days=2), "reachable", 1, 0, 10, "observed"), (E1, NOW, "reachable", 2, 0, 10, "observed"),
            (E2, NOW, "reachable", 1, 0, 10, "observed")]
    out = _call(_ScriptedDB(_Result(rows=[a, b]), _Result(rows=hist)), limit=2)
    rows = {r["name"]: r for r in out["engagements"]}
    assert [p["reachable"] for p in rows["Acme"]["history"]] == [1, 2] and rows["Acme"]["change"]["changed"] is True
    assert rows["Beta"]["change"] is None                                           # one computation: no trend
    assert out["summary"]["compared"] == 1 and out["summary"]["changed"] == 1
