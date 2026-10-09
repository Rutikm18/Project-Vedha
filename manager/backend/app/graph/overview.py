"""
overview.py — what the attack-paths overview and the dashboard's "fix first" card say.

Pure: takes what an engagement's stored analysis holds (see
routers/attack_paths._recompute_and_store) and the labels of the few hosts it names,
and returns the small, flat rows the dashboard shows. It never computes anything and
never reads the database, so "what does the overview say?" is testable without one.

Every row is in exactly one STATE, and each state is a different claim:

  exposed        a crown jewel is itself an exploitable internet-exposed host. It has no
                 route to cut, so it is the worst case, not an empty one;
  reachable      at least one crown jewel can be reached by a modelled route;
  unreachable    crown jewels are marked and none can be reached. NOT "safe": the model
                 may simply have lacked input, and the reasons are carried along;
  no_targets     nothing is marked critical, so there was nothing to protect;
  unrecorded     computed, but this analysis did not record per-jewel data. Counts stay
                 None (unknown), never 0;
  not_computed   nobody has computed paths for this engagement — NOT "0 routes".

Other rules the rows follow:
  * `path_count` is the length of a CAPPED list (at most 5 routes per entry point per
    crown jewel). It tracks entry points, not exposure, so it is never ranked on;
  * coverage is reported as the analysis recorded it ("observed" / "partial"), or
    None when the analysis predates the coverage report — never filled in.
"""
from __future__ import annotations

from typing import Any

# How many hosts of the minimum fix set a row names; the rest are counted.
FIX_ASSETS_SHOWN = 3

# How many hosts of a route the focus card names with a share of the risk they remove.
FOCUS_RANKED_SHOWN = 3

# A route multiplies at least one step probability, and the highest step value is 0.95, so
# only a jewel that is its own entry point scores this high. Used for analyses stored before
# `exposed_directly` existed.
EXPOSED_LIKELIHOOD = 0.9999

EXPOSED = "exposed"
REACHABLE = "reachable"
UNREACHABLE = "unreachable"
NO_TARGETS = "no_targets"
UNRECORDED = "unrecorded"
NOT_COMPUTED = "not_computed"

STATE_ORDER = {EXPOSED: 0, REACHABLE: 1, UNREACHABLE: 2, UNRECORDED: 3, NO_TARGETS: 4, NOT_COMPUTED: 5}

# States where the model assessed at least one crown jewel.
ASSESSED = (EXPOSED, REACHABLE, UNREACHABLE)


def _num(value: Any) -> float | None:
    """A finite number, or None. Booleans are not numbers here."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if value == value and abs(value) != float("inf") else None


def fix_asset_ids(analysis: dict[str, Any] | None, shown: int = FIX_ASSETS_SHOWN) -> tuple[list[str], int]:
    """(the first `shown` hosts of the minimum fix set, how many more there are)."""
    fix = ((analysis or {}).get("choke") or {}).get("min_fix_set") or {}
    ids = [str(a) for a in (fix.get("assets") or [])]
    return ids[:shown], max(len(ids) - shown, 0)


def jewel_facts(analysis: dict[str, Any] | None) -> dict[str, Any] | None:
    """What the analysis says about the engagement's crown jewels, or None when it does
    not say (an analysis stored without per-jewel data). Absent is unknown, not zero.

    total      crown jewels the model considered
    reachable  of those, how many a modelled route (or direct exposure) reaches
    exposed    of those, how many are themselves exposed to the internet
    exposed_ids  asset ids of the exposed ones
    top_risk   the highest modelled risk (0-100 ordering weight) among the jewels
    ways_in    the most independent (vertex-disjoint) routes into any reachable,
               non-exposed jewel; None when there is none to count
    """
    choke = (analysis or {}).get("choke") or {}
    targets = choke.get("targets")
    if not isinstance(targets, list):
        return None
    reachable = exposed = 0
    exposed_ids: list[str] = []
    risks: list[float] = []
    ways: list[int] = []
    independent = (choke.get("min_fix_set") or {}).get("independent_routes") or {}
    for t in targets:
        if not isinstance(t, dict):
            return None
        likelihood = _num(t.get("best_likelihood"))
        if likelihood is None:
            return None
        flag = t.get("exposed_directly")
        is_exposed = bool(flag) if isinstance(flag, bool) else likelihood >= EXPOSED_LIKELIHOOD
        if is_exposed:
            exposed += 1
            exposed_ids.append(str(t.get("asset_id")))
        if likelihood > 0:
            reachable += 1
            routes = _num(independent.get(str(t.get("asset_id"))))
            if routes and routes > 0 and not is_exposed:
                ways.append(int(routes))
        risk = _num(t.get("risk"))
        if risk is not None:
            risks.append(risk)
    return {
        "total": len(targets), "reachable": reachable, "exposed": exposed, "exposed_ids": exposed_ids,
        "top_risk": round(max(risks), 2) if risks else None,
        "ways_in": max(ways) if ways else None,
    }


def classify(analysis: dict[str, Any] | None) -> str:
    """The state of one engagement's stored analysis (see the module docstring)."""
    if analysis is None:
        return NOT_COMPUTED
    facts = jewel_facts(analysis)
    if facts is None:
        return UNRECORDED
    if facts["total"] == 0:
        return NO_TARGETS
    if facts["exposed"] > 0:
        return EXPOSED
    return REACHABLE if facts["reachable"] > 0 else UNREACHABLE


def build_row(
    *,
    engagement_id: Any,
    name: str,
    status: Any,
    computed_at: Any = None,
    path_count: int | None = None,
    analysis: dict[str, Any] | None = None,
    labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    """The overview row for one engagement. `analysis is None` = never computed."""
    labels = labels or {}
    state = classify(analysis)
    row: dict[str, Any] = {
        "engagement_id": str(engagement_id),
        "name": name,
        "status": str(getattr(status, "value", status) or ""),
        "state": state,
        "computed": analysis is not None,
        "computed_at": computed_at.isoformat() if computed_at is not None else None,
        "path_count": None,
        "entry_points": None,
        "crown_jewels": None,
        "jewels_total": None,
        "jewels_reachable": None,
        "jewels_exposed": None,
        "ways_in": None,
        "top_risk": None,
        "fix_set_size": None,
        "fix_assets": [],
        "fix_assets_more": 0,
        "coverage": None,
        "stale_assets": None,
        "why_empty": [],
    }
    if analysis is None:
        return row

    choke = analysis.get("choke") or {}
    fix = choke.get("min_fix_set") or {}
    ids, more = fix_asset_ids(analysis)
    coverage = analysis.get("coverage") or {}
    freshness = analysis.get("freshness") or {}
    facts = jewel_facts(analysis)
    row.update({
        "path_count": int(path_count or 0),
        "entry_points": choke.get("entry_points"),
        "fix_set_size": fix.get("size", len(fix.get("assets") or [])) if fix else None,
        "fix_assets": [labels.get(i, i) for i in ids],
        "fix_assets_more": more,
        "coverage": coverage.get("confidence") if coverage else None,
        "stale_assets": freshness.get("stale_assets") if freshness else None,
    })
    if facts is not None:
        exposed = state == EXPOSED
        row.update({
            "crown_jewels": facts["total"],
            "jewels_total": facts["total"],
            "jewels_reachable": facts["reachable"],
            "jewels_exposed": facts["exposed"],
            "ways_in": None if exposed else facts["ways_in"],
            "top_risk": facts["top_risk"],
        })
    if state in (UNREACHABLE, NO_TARGETS):
        reasons = (analysis.get("diagnostics") or {}).get("reasons") or []
        row["why_empty"] = [{"code": r.get("code"), "detail": r.get("detail")} for r in reasons
                            if isinstance(r, dict) and r.get("code")]
    return row


def row_sort_key(row: dict[str, Any]) -> tuple[int, int, float, str]:
    """Exposed first, then engagements with reachable jewels (most reachable, then highest
    modelled risk), then ones computed with none reachable, then the ones that cannot be
    assessed; ties by name so the order is stable. Never ranks on the capped route count."""
    state = row.get("state") or NOT_COMPUTED
    name = str(row.get("name") or "").lower()
    if state in (EXPOSED, REACHABLE):
        return (STATE_ORDER[state], -int(row.get("jewels_reachable") or 0), -float(row.get("top_risk") or 0), name)
    return (STATE_ORDER.get(state, 9), 0, 0.0, name)


def build_summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    """Counts over ALL of a tenant's engagements (not just the ones shown). Counts of
    engagements only: crown jewels and hosts of different networks are not added."""
    by = lambda *states: sum(1 for r in rows if r.get("state") in states)  # noqa: E731
    assessed = [r for r in rows if r.get("state") in ASSESSED]
    return {
        "engagements": len(rows),
        "computed": sum(1 for r in rows if r.get("computed")),
        "assessed": len(assessed),
        "with_reachable": by(EXPOSED, REACHABLE),
        "exposed": by(EXPOSED),
        "single_fix": sum(1 for r in rows if r.get("state") == REACHABLE and r.get("fix_set_size") == 1),
        "not_computed": by(NOT_COMPUTED),
        "no_targets": by(NO_TARGETS),
        "unrecorded": by(UNRECORDED),
        "jewels_total": sum(int(r.get("jewels_total") or 0) for r in assessed),
        "jewels_reachable": sum(int(r.get("jewels_reachable") or 0) for r in assessed),
    }


# ── the "fix first" card ─────────────────────────────────────────────────────

def fix_point_ids(choke: dict[str, Any] | None, top: int = FOCUS_RANKED_SHOWN) -> set[str]:
    """Hosts marked "fix here": the smallest cutting set, plus the few single hosts whose
    fix removes the most risk. Same rule as the route map (`fixPointIds` in the frontend)."""
    ids = {str(a) for a in ((choke or {}).get("min_fix_set") or {}).get("assets") or []}
    for r in ((choke or {}).get("ranked") or [])[:top]:
        if (_num(r.get("risk_removed")) or 0) > 0:
            ids.add(str(r.get("asset_id")))
    return ids


def risk_share(entry: dict[str, Any], targets: list[dict[str, Any]]) -> float | None:
    """Share (0-1) of the engagement's modelled risk that fixing this one host removes;
    None when there is no modelled risk to share. Bounded, unlike `risk_removed` itself
    (a sum over crown jewels)."""
    total = sum(max(_num(t.get("risk")) or 0.0, 0.0) for t in targets if isinstance(t, dict))
    if total <= 0:
        return None
    return round(max(0.0, min(1.0, (_num(entry.get("risk_removed")) or 0.0) / total)), 4)


def build_focus(
    *,
    engagement_id: Any,
    name: str,
    computed_at: Any,
    analysis: dict[str, Any] | None,
    path_count: int | None,
    route: dict[str, Any] | None,
    labels: dict[str, str],
) -> dict[str, Any]:
    """What the card shows for one engagement: its worst-case crown jewels, the highest-risk
    stored route (nodes tagged entry / via / jewel and whether each is on the fix list; hops
    with their basis), the smallest fix set and the top hosts by share of modelled risk
    removed. `route` is {id, risk_score, freshness, nodes: [asset id], edges: [dict]} or None.
    Nothing is computed: it reads what is stored."""
    def label(aid: Any) -> str:
        return labels.get(str(aid), str(aid))

    state = classify(analysis)
    out: dict[str, Any] = {
        "engagement_id": str(engagement_id), "name": name, "state": state,
        "computed": analysis is not None,
        "computed_at": computed_at.isoformat() if computed_at is not None else None,
        "path_count": int(path_count or 0) if analysis is not None else None,
        "exposed": [], "route": None, "fix": None, "ranked": [],
    }
    if analysis is None:
        return out

    choke = analysis.get("choke") or {}
    facts = jewel_facts(analysis)
    out["exposed"] = [{"asset_id": i, "label": label(i)} for i in (facts or {}).get("exposed_ids", [])]

    fix = choke.get("min_fix_set") or {}
    if fix:
        out["fix"] = {
            "size": fix.get("size", len(fix.get("assets") or [])),
            "assets": [{"asset_id": str(a), "label": label(a)} for a in fix.get("assets") or []],
            "independent_routes": {label(k): v for k, v in (fix.get("independent_routes") or {}).items()},
        }

    on_list = fix_point_ids(choke)
    targets = choke.get("targets") or []
    ranked = []
    for r in choke.get("ranked") or []:
        if (_num(r.get("risk_removed")) or 0) <= 0:
            continue
        ranked.append({
            "asset_id": str(r.get("asset_id")), "label": label(r.get("asset_id")),
            "share": risk_share(r, targets),
            "cuts_off": len(r.get("targets_cut_off") or []),
            "jewels_reachable": (facts or {}).get("reachable"),
        })
        if len(ranked) == FOCUS_RANKED_SHOWN:
            break
    out["ranked"] = ranked

    if route and route.get("nodes"):
        ids = [str(n).removeprefix("asset:") for n in route["nodes"]]
        last = len(ids) - 1
        out["route"] = {
            "path_id": str(route.get("id")),
            "risk_score": route.get("risk_score"),
            "freshness": route.get("freshness"),
            "nodes": [{
                "asset_id": aid, "label": label(aid),
                "role": "jewel" if i == last else ("entry" if i == 0 else "via"),
                "on_fix_list": aid in on_list,
            } for i, aid in enumerate(ids)],
            "hops": [{
                "basis": e.get("basis"), "technique": e.get("technique"),
                "stale": bool(e.get("stale")), "exploited": e.get("exploited"),
            } for e in route.get("edges") or [] if isinstance(e, dict)],
        }
    return out
