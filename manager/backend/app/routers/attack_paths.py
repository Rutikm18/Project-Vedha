"""
Attack path analysis API (AttackPathService) — BETA: the model, ranking and
response shapes may still change.

GET /engagements/{id}/attack-paths            — paginated paths sorted by risk
GET /engagements/{id}/attack-paths/{path_id}  — full path detail, hop-by-hop
GET /engagements/{id}/chokepoints             — chokepoint assets + remediation priority
GET /engagements/{id}/attack-path-zones       — the stored routes aggregated into the subnets they cross
GET /engagements/{id}/blast-radius/{asset_id} — assets reachable if asset is owned
GET /engagements/{id}/attack-graph            — D3-compatible graph JSON
GET /attack-paths/overview                    — stored results for every engagement (dashboard)
GET /attack-paths/focus/{engagement_id}       — the "fix first" card for one engagement (read-only)

Paths are computed from the engagement's assets/services/findings, scored, and
persisted to the ``attack_paths`` table so ``/{path_id}`` can return a stable,
shareable record. The graph engine runs in-memory (NetworkX); Neo4j is mirrored
only when enabled.
"""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import delete, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder
from app.graph.coverage import coverage_report, freshness_report
from app.graph.overview import (
    HISTORY_POINTS, build_focus, build_row, build_summary, fix_asset_ids, row_sort_key, snapshot_facts,
    snapshots_to_prune,
)
from app.graph.visualizer import GraphVisualizer
from app.graph.zones import build_zones
from app.models.asset import Asset
from app.models.attack_path import AttackPath
from app.models.attack_path_analysis import AttackPathAnalysis
from app.models.attack_path_snapshot import AttackPathSnapshot
from app.models.engagement import Engagement
from app.models.enums import AssetCriticality
from app.models.probe_site import ProbeSite
from app.schemas.auth import CurrentUser
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements/{engagement_id}", tags=["attack-paths (beta)"])
logger = structlog.get_logger()

# Tenant-wide, read-only. Operators only: the customer portal has no attack-path view.
overview_router = APIRouter(prefix="/attack-paths", tags=["attack-paths (beta)"])
OVERVIEW_ROLES = ["admin", "manager", "tester", "analyst", "auditor"]


# ── GET /attack-paths/overview — what the stored analyses say, per engagement ─

# The most engagements one overview ranks. Rows are small (only the sub-keys the overview
# reads are loaded), so this is generous; past it `summary.truncated` says so.
MAX_RANKED_ENGAGEMENTS = 1000


@overview_router.get("/overview", summary="Stored attack-path results for every engagement (beta)")
async def attack_paths_overview(
    db: DB,
    current_user: Annotated[CurrentUser, require_role(OVERVIEW_ROLES)],
    limit: int = Query(default=50, ge=1, le=200),
):
    """One line per engagement of the caller's tenant: how many crown jewels the last
    computation could reach, whether one is exposed outright, the smallest set of hosts
    that cuts the routes, and how much of the network it covered. READ-ONLY: it reads the
    stored analyses and never computes, so an engagement nobody has opened is
    `not_computed`, which is not the same claim as "0 reachable".

    Every engagement of the tenant is ranked FIRST and the limit applied after, and
    `summary` counts all of them, so neither the ordering nor the totals depend on how
    many rows are shown."""
    tenant_id = current_user.tenant_id
    a = AttackPathAnalysis.analysis
    picked = (await db.execute(
        select(Engagement.id, Engagement.name, Engagement.status,
               AttackPathAnalysis.computed_at, AttackPathAnalysis.path_count,
               a["choke"]["targets"], a["choke"]["min_fix_set"], a["choke"]["entry_points"],
               a["coverage"]["confidence"], a["freshness"]["stale_assets"], a["diagnostics"]["reasons"])
        .select_from(Engagement)
        .outerjoin(AttackPathAnalysis, AttackPathAnalysis.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
        .order_by(Engagement.created_at.desc())
        .limit(MAX_RANKED_ENGAGEMENTS)
    )).all()

    history = await _history_by_engagement(db, tenant_id)
    inputs: dict[str, dict] = {}
    rows = []
    for eid, name, status, at, count, targets, fix, entry, cov, stale, reasons in picked:
        inputs[str(eid)] = dict(name=name, status=status, computed_at=at, path_count=count,
                                analysis=_stored_subset(at, targets, fix, entry, cov, stale, reasons),
                                history=history.get(eid))
        rows.append(build_row(engagement_id=eid, **inputs[str(eid)]))
    summary = build_summary(rows)
    summary["truncated"] = len(picked) >= MAX_RANKED_ENGAGEMENTS
    rows.sort(key=row_sort_key)
    shown = rows[:limit]

    # Host names only for the few rows that are actually returned.
    wanted: dict[uuid.UUID, list[str]] = {}
    for row in shown:
        ids, _more = fix_asset_ids(inputs[row["engagement_id"]]["analysis"])
        if ids:
            wanted[uuid.UUID(row["engagement_id"])] = ids
    labels = await _fix_asset_labels(db, wanted)
    if labels:
        shown = [build_row(engagement_id=r["engagement_id"], **inputs[r["engagement_id"]],
                           labels=labels.get(uuid.UUID(r["engagement_id"]))) for r in shown]
    return {"total": len(picked), "shown": len(shown), "summary": summary, "engagements": shown}


def _stored_subset(computed_at, targets, fix, entry, coverage, stale, reasons) -> dict | None:
    """The part of a stored analysis the overview reads, rebuilt from the projected
    sub-keys. `None` means no analysis row at all (never computed); a key the analysis did
    not record is left out, so the reader sees it as unknown rather than as zero."""
    if computed_at is None:
        return None
    choke = {k: v for k, v in (("targets", targets), ("min_fix_set", fix), ("entry_points", entry)) if v is not None}
    return {
        "choke": choke,
        "coverage": {"confidence": coverage} if coverage else None,
        "freshness": {"stale_assets": stale} if stale is not None else None,
        "diagnostics": {"reasons": reasons or []},
    }


# ── GET /attack-paths/focus/{engagement_id} — the dashboard's "fix first" card ─

@overview_router.get("/focus/{engagement_id}", summary="Fix-first detail for one engagement (beta, read-only)")
async def attack_paths_focus(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[CurrentUser, require_role(OVERVIEW_ROLES)],
):
    """The highest-risk STORED route, the smallest fix set and the hosts whose fix removes
    the most modelled risk. Unlike `GET /engagements/{id}/attack-paths` this never
    recomputes: an engagement with no stored routes (computed with none, or a crown jewel
    that is exposed outright) is answered from its stored analysis, and a GET writes nothing."""
    engagement = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    stored = await db.get(AttackPathAnalysis, engagement_id)
    if stored is None:
        return build_focus(engagement_id=engagement_id, name=engagement.name, computed_at=None,
                           analysis=None, path_count=None, route=None, labels={})
    top = (await db.execute(
        select(AttackPath).where(AttackPath.engagement_id == engagement_id)
        .order_by(AttackPath.risk_score.desc().nullslast(), AttackPath.id).limit(1)
    )).scalars().first()
    labels = await _asset_labels(db, engagement_id)
    route = None
    if top is not None:
        route = {"id": top.id, "risk_score": float(top.risk_score) if top.risk_score is not None else None,
                 "freshness": path_freshness(top.path_edges or []),
                 "nodes": list(top.path_nodes or []), "edges": list(top.path_edges or [])}
    return build_focus(engagement_id=engagement_id, name=engagement.name, computed_at=stored.computed_at,
                       analysis=stored.analysis or {}, path_count=stored.path_count, route=route, labels=labels)


async def _fix_asset_labels(db: AsyncSession, wanted: dict[uuid.UUID, list[str]]) -> dict[uuid.UUID, dict[str, str]]:
    """Labels for just the hosts the overview names, with the same disambiguation as
    the engagement page (a label two machines share gets its site appended). Two
    bounded queries instead of loading every asset of every engagement: the named
    hosts, then any other host that shares one of their labels."""
    if not wanted:
        return {}
    asset_ids = {uuid.UUID(i) for ids in wanted.values() for i in ids if _is_uuid(i)}
    named = (await db.execute(
        select(Asset.id, Asset.engagement_id, Asset.hostname, Asset.ip_address, Asset.site_id)
        .where(Asset.id.in_(asset_ids))
    )).all() if asset_ids else []
    names = {r[2] for r in named if r[2]}
    ips = {r[3] for r in named if r[3]}
    rows = named
    if names or ips:
        rows = (await db.execute(
            select(Asset.id, Asset.engagement_id, Asset.hostname, Asset.ip_address, Asset.site_id)
            .where(Asset.engagement_id.in_(list(wanted)),
                   or_(Asset.hostname.in_(names) if names else False,
                       Asset.ip_address.in_(ips) if ips else False))
        )).all()
    site_ids = {r[4] for r in rows if r[4] is not None}
    site_names: dict[str, str] = {}
    if site_ids:
        site_names = {str(s.id): s.name for s in (await db.execute(
            select(ProbeSite).where(ProbeSite.id.in_(site_ids))
        )).scalars().all()}
    by_engagement: dict[uuid.UUID, list[tuple]] = {}
    for aid, eid, host, ip, site in rows:
        by_engagement.setdefault(eid, []).append((aid, host, ip, site))
    return {eid: disambiguated_labels(r, site_names) for eid, r in by_engagement.items()}


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


# ── GET /attack-paths — compute (refresh) + paginated list ───────────────────

@router.get("/attack-paths", summary="List attack paths sorted by risk score")
async def list_attack_paths(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    refresh: bool = Query(
        default=False,
        description="Recompute paths from current data. Off by default: reading "
                    "the list must not rewrite it (stable ids, no compute on GET).",
    ),
    target_asset_id: uuid.UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    # "Never computed" is the absence of the stored analysis row, not of route rows: a
    # computed engagement with zero routes (or only an exposed jewel) has an analysis
    # and no routes, and reading it must not recompute and write on every open.
    never_computed = await db.get(AttackPathAnalysis, engagement_id) is None
    diagnostics = None
    if refresh or never_computed:
        # First read of a never-computed engagement still produces a result.
        diagnostics = await _recompute_and_store(db, engagement_id, target_asset_id)

    q = select(AttackPath).where(AttackPath.engagement_id == engagement_id)
    q = q.order_by(AttackPath.risk_score.desc().nullslast(), AttackPath.id)
    rows = (await db.execute(q.offset((page - 1) * page_size).limit(page_size))).scalars().all()
    total = len((await db.execute(
        select(AttackPath.id).where(AttackPath.engagement_id == engagement_id)
    )).all())

    labels = await _asset_labels(db, engagement_id) if rows else {}
    body = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_path_summary(r, labels) for r in rows],
    }
    if total == 0:
        # An empty list must say WHY (FM-30): "no paths" and "nothing to compute
        # from" look identical otherwise.
        if diagnostics is None:
            analyzer, _graph = await _build_analyzer(db, engagement_id)
            diagnostics = analyzer.diagnose(await _target_ids(db, engagement_id, target_asset_id))
        body["why_empty"] = diagnostics
    return body


# ── GET /attack-paths/{path_id} ───────────────────────────────────────────────

@router.get("/attack-paths/{path_id}", summary="Attack path detail, hop-by-hop")
async def get_attack_path(
    engagement_id: uuid.UUID,
    path_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    path = (await db.execute(
        select(AttackPath).where(
            AttackPath.id == path_id,
            AttackPath.engagement_id == engagement_id,
        )
    )).scalar_one_or_none()
    if not path:
        raise HTTPException(404, "Attack path not found")

    # Hydrate hop labels from assets for a readable explanation.
    labels = await _asset_labels(db, engagement_id)
    hops = []
    for edge in (path.path_edges or []):
        hops.append({
            "from": labels.get(str(edge.get("source")), edge.get("source")),
            "to": labels.get(str(edge.get("target")), edge.get("target")),
            "technique": edge.get("technique"),
            "weight": edge.get("weight"),
            "exploited": edge.get("exploited"),
            "cvss": edge.get("cvss"),
            "via": edge.get("via") or [],
            "basis": edge.get("basis"),
            "likelihood": edge.get("likelihood"),
            "stale": bool(edge.get("stale")),
            "capability": edge.get("capability"),       # P2: foothold/lateral/priv_esc for the final step
            "explanation": _explain_hop(edge, labels),
        })

    return {
        "id": str(path.id),
        "risk_score": float(path.risk_score) if path.risk_score is not None else None,
        "freshness": path_freshness(path.path_edges or []),
        "node_count": len(path.path_nodes or []),
        "nodes": [labels.get(str(n), str(n)) for n in (path.path_nodes or [])],
        "hops": hops,
        "chokepoints": [labels.get(str(c), str(c)) for c in (path.chokepoints or [])],
    }


# ── GET /chokepoints ──────────────────────────────────────────────────────────

@router.get("/chokepoints", summary="Which hosts to fix first, and the smallest set that cuts every path")
async def list_chokepoints(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    """Reads the analysis stored by the last recompute. Only an engagement that was
    never computed is analysed on the spot (and not stored: a GET does not write)."""
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    stored = await db.get(AttackPathAnalysis, engagement_id)
    if stored is not None:
        choke, computed_at, source = (stored.analysis or {}).get("choke") or {}, stored.computed_at, "stored"
    else:
        analyzer, _graph = await _build_analyzer(db, engagement_id)
        choke = analyzer.choke_analysis(await _target_ids(db, engagement_id, None))
        computed_at, source = None, "computed"
    labels = await _asset_labels(db, engagement_id)
    body = labelled_choke(choke, labels)
    return {"count": len(body["ranked"]), "chokepoints": body["ranked"], "min_fix_set": body["min_fix_set"],
            "targets": body["targets"], "entry_points": body.get("entry_points", 0),
            "method": body.get("method"), "source": source,
            "computed_at": computed_at.isoformat() if computed_at else None}


# ── GET /attack-path-analysis ─────────────────────────────────────────────────

@router.get("/attack-path-analysis",
            summary="Stored engagement-level analysis: choke points, coverage, freshness, why-empty")
async def attack_path_analysis(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    """Everything about the engagement as a whole that the last recompute found.
    Read-only: an engagement that was never computed answers `computed: false`
    instead of computing on a GET."""
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    stored = await db.get(AttackPathAnalysis, engagement_id)
    if stored is None:
        return {"computed": False, "detail": "no attack-path computation has run for this engagement yet"}
    analysis = stored.analysis or {}
    labels = await _asset_labels(db, engagement_id)
    return {
        "computed": True,
        "computed_at": stored.computed_at.isoformat(),
        "path_count": stored.path_count,
        "choke": labelled_choke(analysis.get("choke") or {}, labels),
        "coverage": analysis.get("coverage"),
        "freshness": analysis.get("freshness"),
        "diagnostics": analysis.get("diagnostics"),
        "target_selection": _labelled_target_selection(analysis.get("target_selection"), labels),
    }


def _labelled_target_selection(selection: dict | None, labels: dict[str, str]) -> dict:
    """The stored target selection (P4b) with host labels added to any suggested
    crown jewels, so the page can say 'targets suggested automatically: dc01 (domain
    controller)'. `basis` is operator / suggested / explicit / none."""
    selection = selection or {"basis": "operator", "suggested": []}
    return {
        "basis": selection.get("basis", "operator"),
        "suggested": [{"asset_id": s["asset_id"], "reason": s.get("reason"),
                       "label": labels.get(str(s["asset_id"]), str(s["asset_id"]))}
                      for s in (selection.get("suggested") or [])],
    }


# ── GET /attack-path-zones ────────────────────────────────────────────────────

# The most stored routes aggregated into one zone view (an engagement stores at most 5 per entry
# point per crown jewel, so this is rarely reached; `routes_truncated` says when it was).
MAX_ZONE_ROUTES = 500


@router.get("/attack-path-zones",
            summary="The stored routes aggregated into the subnets they cross (beta, read-only)")
async def attack_path_zones(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    """Which subnets the stored routes start in, end in, cross and need fixing in, and on what
    basis each crossing rests. Read-only: it aggregates what is stored and never computes, so an
    engagement nobody computed answers `computed: false`."""
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    stored = await db.get(AttackPathAnalysis, engagement_id)
    if stored is None:
        return {**build_zones(analysis=None, routes=[], engagement_id=engagement_id), "routes_truncated": False}
    rows = (await db.execute(
        select(AttackPath.path_nodes, AttackPath.path_edges)
        .where(AttackPath.engagement_id == engagement_id).limit(MAX_ZONE_ROUTES)
    )).all()
    routes = [{"nodes": list(nodes or []), "edges": list(edges or [])} for nodes, edges in rows]
    analysis = stored.analysis or {}
    site_ids = {uuid.UUID(s["site"]) for s in (analysis.get("coverage") or {}).get("segments") or []
                if isinstance(s, dict) and s.get("site") and _is_uuid(s["site"])}
    site_names: dict[str, str] = {}
    if site_ids:
        site_names = {str(s.id): s.name for s in (await db.execute(
            select(ProbeSite).where(ProbeSite.id.in_(site_ids))
        )).scalars().all()}
    return {**build_zones(analysis=analysis, routes=routes, site_names=site_names,
                          computed_at=stored.computed_at, engagement_id=engagement_id),
            "routes_truncated": len(rows) >= MAX_ZONE_ROUTES}


# ── GET /blast-radius/{asset_id} ──────────────────────────────────────────────

@router.get("/blast-radius/{asset_id}", summary="Assets reachable if this asset is compromised")
async def blast_radius(
    engagement_id: uuid.UUID,
    asset_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    analyzer, _graph = await _build_analyzer(db, engagement_id)
    result = analyzer.find_blast_radius(str(asset_id))
    labels = await _asset_labels(db, engagement_id)
    result["reachable_labels"] = [labels.get(str(a), a) for a in result["reachable"]]
    return result


# ── GET /attack-graph ─────────────────────────────────────────────────────────

@router.get("/attack-graph", summary="D3-compatible attack graph JSON")
async def attack_graph(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    target_asset_id: uuid.UUID | None = Query(default=None),
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    analyzer, graph = await _build_analyzer(db, engagement_id)

    if target_asset_id:
        paths = analyzer.find_paths_to_target(str(target_asset_id))
    else:
        paths = _all_paths_to_critical(analyzer, await _critical_asset_ids(db, engagement_id))
    for i, p in enumerate(paths):
        p["id"] = f"path-{i}"

    return GraphVisualizer(graph).to_d3(paths)


# ── helpers ───────────────────────────────────────────────────────────────────
# `get_or_404` lives in app/utils/db.py — imported at top of file.

async def _build_analyzer(db: AsyncSession, engagement_id: uuid.UUID) -> tuple[PathAnalyzer, "object"]:
    builder = GraphBuilder()
    graph = await builder.build_from_db(db, engagement_id)
    return PathAnalyzer(graph), graph


async def _critical_asset_ids(db: AsyncSession, engagement_id: uuid.UUID) -> list[str]:
    rows = (await db.execute(
        select(Asset.id).where(
            Asset.engagement_id == engagement_id,
            Asset.criticality == AssetCriticality.critical,
        )
    )).all()
    return [str(r[0]) for r in rows]


def _all_paths_to_critical(analyzer: PathAnalyzer, critical_ids: list[str]) -> list[dict]:
    paths: list[dict] = []
    for aid in critical_ids:
        paths.extend(analyzer.find_paths_to_target(aid))
    paths.sort(key=lambda p: p["risk_score"], reverse=True)
    return paths


def path_id_for(engagement_id: uuid.UUID, nodes: list[str]) -> uuid.UUID:
    """Deterministic path id: the same node sequence in the same engagement always
    gets the same id, so a shared /attack-paths/{id} link survives a recompute
    (FM-24). Hash, not uuid5, so the id space stays engagement-scoped."""
    raw = f"{engagement_id}|{'>'.join(str(n) for n in nodes)}".encode()
    return uuid.UUID(bytes=hashlib.sha256(raw).digest()[:16], version=4)


async def _lock_engagement_paths(db: AsyncSession, engagement_id: uuid.UUID) -> None:
    """Serialise path recomputes per engagement for the rest of the transaction,
    so two concurrent refreshes cannot interleave their delete/insert (FM-24).
    Postgres advisory lock; a no-op on databases without it (unit tests)."""
    key = (engagement_id.int ^ (engagement_id.int >> 64)) & 0x7FFFFFFFFFFFFFFF
    try:
        await db.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": key ^ 0x5A5A})
    except Exception as exc:  # noqa: BLE001 — non-Postgres backends
        logger.debug("graph.paths.lock_unavailable", error=str(exc))


async def _suggest_target_assets(db: AsyncSession, engagement_id: uuid.UUID) -> list[dict[str, str]]:
    """Crown-jewel suggestions (P4b) for an engagement with nothing marked critical:
    domain controllers, virtualization hosts and datastores, from role evidence and
    observed datastore services. Each carries the reason it was picked."""
    from app.detection.crown_jewels import suggest_crown_jewels
    from app.models.service import Service

    assets = (await db.execute(
        select(Asset.id, Asset.asset_type, Asset.device_role, Asset.role_detail, Asset.role_confidence)
        .where(Asset.engagement_id == engagement_id)
    )).all()
    asset_views = [{"id": a[0], "asset_type": a[1], "device_role": a[2],
                    "role_detail": a[3], "role_confidence": a[4]} for a in assets]
    asset_ids = [a[0] for a in assets]
    services = (await db.execute(
        select(Service.asset_id, Service.port).where(Service.asset_id.in_(asset_ids))
    )).all() if asset_ids else []
    service_views = [{"asset_id": s[0], "port": s[1]} for s in services]
    return suggest_crown_jewels(asset_views, service_views)


async def _resolve_targets(db: AsyncSession, engagement_id: uuid.UUID,
                           target_asset_id: uuid.UUID | None) -> tuple[list[str], dict]:
    """The path targets and how they were chosen (P4b). Operator-marked critical
    assets always win; only when none is marked do we fall back to SUGGESTED crown
    jewels, and the returned selection says which, so the UI never presents an
    auto-picked target as a deliberate scoping choice."""
    if target_asset_id:
        return [str(target_asset_id)], {"basis": "explicit", "suggested": []}
    critical = await _critical_asset_ids(db, engagement_id)
    if critical:
        return critical, {"basis": "operator", "suggested": []}
    suggestions = await _suggest_target_assets(db, engagement_id)
    ids = [s["asset_id"] for s in suggestions]
    return ids, {"basis": "suggested" if ids else "none", "suggested": suggestions}


async def _target_ids(db: AsyncSession, engagement_id: uuid.UUID,
                      target_asset_id: uuid.UUID | None) -> list[str]:
    ids, _selection = await _resolve_targets(db, engagement_id, target_asset_id)
    return ids


async def _recompute_and_store(
    db: AsyncSession, engagement_id: uuid.UUID, target_asset_id: uuid.UUID | None, trigger: str = "manual"
) -> dict:
    """Recompute and UPSERT the engagement's paths. Returns the analyzer's
    diagnostics so the caller can explain an empty result."""
    await _lock_engagement_paths(db, engagement_id)
    analyzer, graph = await _build_analyzer(db, engagement_id)
    targets, target_selection = await _resolve_targets(db, engagement_id, target_asset_id)
    paths = _all_paths_to_critical(analyzer, targets)

    # Engagement-wide facts are computed once, measured on the network (not counted
    # on the truncated path list) and stored once (FM-25/26).
    choke = analyzer.choke_analysis(targets)

    # Upsert by deterministic id: unchanged paths keep their id, vanished paths
    # are removed, new ones inserted. Never a blanket delete-then-insert.
    wanted: dict[uuid.UUID, dict] = {}
    for p in paths:
        wanted.setdefault(path_id_for(engagement_id, p["nodes"]), p)
    existing = {
        r.id: r for r in (await db.execute(
            select(AttackPath).where(AttackPath.engagement_id == engagement_id)
        )).scalars().all()
    }
    stale = [pid for pid in existing if pid not in wanted]
    if stale:
        await db.execute(delete(AttackPath).where(
            AttackPath.engagement_id == engagement_id, AttackPath.id.in_(stale)))
    for pid, p in wanted.items():
        row = existing.get(pid)
        if row is None:
            row = AttackPath(id=pid, engagement_id=engagement_id)
            db.add(row)
        row.path_nodes = [str(n) for n in p["nodes"]]
        row.path_edges = p["edges"]
        row.risk_score = Decimal(str(p["risk_score"]))
        row.chokepoints = path_chokepoints(p["nodes"], choke)         # only the ones ON this path
    diagnostics = analyzer.diagnose(targets)
    payload = {
        "choke": choke, "diagnostics": diagnostics,
        "coverage": coverage_report(graph), "freshness": freshness_report(graph),
        "target_selection": target_selection,       # P4b: operator vs suggested crown jewels
    }
    computed_at = await _store_analysis(db, engagement_id, payload, len(wanted))
    await _record_snapshot(db, engagement_id, payload, len(wanted), trigger, computed_at)
    await db.flush()
    logger.info("graph.paths.stored", engagement=str(engagement_id), count=len(wanted),
                removed=len(stale))
    return diagnostics


async def refresh_if_materialised(db: AsyncSession, engagement_id: uuid.UUID) -> bool:
    """Bring an engagement's STORED attack paths and analysis up to date after its
    findings changed. Called by the detection run — reading never recomputes.

    Only when someone already has stored results: before that, the first read
    computes them, so an engagement nobody looks at costs nothing. Without this a
    stored path list silently describes the network as it was at the last manual
    refresh, however many findings have been fixed or found since. Runs in a
    savepoint so a failure here can never poison the caller's transaction.
    Returns True when it recomputed."""
    has_paths = (await db.execute(
        select(AttackPath.id).where(AttackPath.engagement_id == engagement_id).limit(1)
    )).first() is not None
    if not has_paths and await db.get(AttackPathAnalysis, engagement_id) is None:
        return False
    async with db.begin_nested():
        await _recompute_and_store(db, engagement_id, None, trigger="detection")
    return True


async def _store_analysis(db: AsyncSession, engagement_id: uuid.UUID, payload: dict, path_count: int) -> datetime:
    """Replace the engagement's stored analysis (one row per engagement). Returns its timestamp."""
    now = datetime.now(timezone.utc)
    row = await db.get(AttackPathAnalysis, engagement_id)
    if row is None:
        db.add(AttackPathAnalysis(engagement_id=engagement_id, computed_at=now,
                                  path_count=path_count, analysis=payload))
    else:
        row.computed_at, row.path_count, row.analysis = now, path_count, payload
    return now


async def _record_snapshot(db: AsyncSession, engagement_id: uuid.UUID, payload: dict, path_count: int,
                           trigger: str, computed_at: datetime) -> None:
    """Add this computation's headline numbers to the engagement's history, then drop what the
    retention rule no longer keeps (every computation for a week, then one a day, at most 90).
    History is small and is only ever read for a trend; a failure here must not lose the analysis,
    which is why callers run the recompute inside a savepoint where it is not a user's own click."""
    db.add(AttackPathSnapshot(engagement_id=engagement_id, computed_at=computed_at, trigger=trigger,
                              **snapshot_facts(payload, path_count)))
    await db.flush()
    rows = (await db.execute(
        select(AttackPathSnapshot.id, AttackPathSnapshot.computed_at)
        .where(AttackPathSnapshot.engagement_id == engagement_id)
    )).all()
    doomed = snapshots_to_prune([(r[0], r[1]) for r in rows], computed_at)
    if doomed:
        await db.execute(delete(AttackPathSnapshot).where(AttackPathSnapshot.id.in_(doomed)))


async def _history_by_engagement(db: AsyncSession, tenant_id: uuid.UUID) -> dict[uuid.UUID, list[dict]]:
    """The last HISTORY_POINTS computations of every engagement of the tenant, oldest first. One
    query; tenant-scoped through the engagement."""
    S = AttackPathSnapshot
    rn = func.row_number().over(partition_by=S.engagement_id, order_by=S.computed_at.desc()).label("rn")
    sub = (select(S.engagement_id, S.computed_at, S.state, S.jewels_reachable, S.jewels_exposed,
                  S.assets_seen, S.coverage, rn)
           .join(Engagement, Engagement.id == S.engagement_id)
           .where(Engagement.tenant_id == tenant_id).subquery())
    rows = (await db.execute(
        select(sub.c.engagement_id, sub.c.computed_at, sub.c.state, sub.c.jewels_reachable, sub.c.jewels_exposed,
               sub.c.assets_seen, sub.c.coverage)
        .where(sub.c.rn <= HISTORY_POINTS).order_by(sub.c.engagement_id, sub.c.computed_at)
    )).all()
    out: dict[uuid.UUID, list[dict]] = {}
    for eid, at, state, reachable, exposed, seen, cov in rows:
        out.setdefault(eid, []).append({
            "at": at.isoformat(), "state": state, "reachable": reachable, "exposed": exposed,
            "assets_seen": seen, "coverage": cov,
        })
    return out


def path_chokepoints(path_nodes: list[str], choke: dict) -> list[str]:
    """The choke points that lie on THIS path (in path order). Each path row used to
    carry the whole engagement's list, which says nothing about the path (FM-26)."""
    wanted = {r["asset_id"] for r in (choke.get("ranked") or []) if r.get("risk_removed", 0) > 0}
    return [str(n) for n in path_nodes if str(n) in wanted]


def labelled_choke(choke: dict, labels: dict[str, str]) -> dict:
    """Stored/computed choke analysis with host labels added (ids stay authoritative)."""
    def label(aid):
        return labels.get(str(aid), str(aid))
    fix = choke.get("min_fix_set") or {"size": 0, "assets": [], "independent_routes": {}}
    return {
        **choke,
        "ranked": [{**r, "label": label(r["asset_id"]),
                    "targets_cut_off_labels": [label(t) for t in r.get("targets_cut_off") or []]}
                   for r in choke.get("ranked") or []],
        "min_fix_set": {"size": fix.get("size", 0),
                        "assets": [{"asset_id": a, "label": label(a)} for a in fix.get("assets") or []],
                        "independent_routes": {label(k): v for k, v in (fix.get("independent_routes") or {}).items()},
                        # D8: crown jewels exposed outright — their OWN exposure must be removed.
                        "exposed_targets": [{"asset_id": a, "label": label(a)}
                                            for a in fix.get("exposed_targets") or []]},
        "targets": [{**x, "label": label(x["asset_id"])} for x in choke.get("targets") or []],
    }


async def _asset_labels(db: AsyncSession, engagement_id: uuid.UUID) -> dict[str, str]:
    rows = (await db.execute(
        select(Asset.id, Asset.hostname, Asset.ip_address, Asset.site_id).where(
            Asset.engagement_id == engagement_id
        )
    )).all()
    site_ids = {r[3] for r in rows if r[3] is not None}
    site_names: dict[str, str] = {}
    if site_ids:
        site_names = {str(s.id): s.name for s in (await db.execute(
            select(ProbeSite).where(ProbeSite.id.in_(site_ids))
        )).scalars().all()}
    return disambiguated_labels(rows, site_names)


def disambiguated_labels(rows, site_names: dict[str, str]) -> dict[str, str]:
    """asset id -> a label a person can tell apart. Under per-site identity two
    machines can share an address (10.0.0.5 at HQ and at the branch); a path that
    names "10.0.0.5" twice is unreadable, so a label that is not unique gets its
    site appended. Unique labels are left exactly as they were."""
    base = {str(r[0]): (r[1] or r[2] or str(r[0])) for r in rows}
    counts: dict[str, int] = {}
    for label in base.values():
        counts[label] = counts.get(label, 0) + 1
    out = dict(base)
    for r in rows:
        aid, site = str(r[0]), r[3] if len(r) > 3 else None
        if counts[base[aid]] > 1 and site is not None:
            out[aid] = f"{base[aid]} @ {site_names.get(str(site)) or str(site)[:8]}"
    return out


def path_freshness(edges: list[dict]) -> str:
    """fresh / partly_stale / stale, from the per-hop `stale` flags."""
    flags = [bool(e.get("stale")) for e in edges or []]
    if not flags or not any(flags):
        return "fresh"
    return "stale" if all(flags) else "partly_stale"


def _path_summary(r: AttackPath, labels: dict[str, str] | None = None) -> dict:
    """One row of the path list. `source`/`target` stay the authoritative node ids;
    the labels are what a person reads (a host name, or its address, with its site
    when the address alone is ambiguous)."""
    labels = labels or {}
    source = str(r.path_nodes[0]) if r.path_nodes else None
    target = str(r.path_nodes[-1]) if r.path_nodes else None
    return {
        "id": str(r.id),
        "risk_score": float(r.risk_score) if r.risk_score is not None else None,
        "hops": max(len(r.path_nodes or []) - 1, 0),
        "source": source,
        "target": target,
        "source_label": labels.get(source, source) if source else None,
        "target_label": labels.get(target, target) if target else None,
        "freshness": path_freshness(r.path_edges or []),
        "chokepoint_count": len(r.chokepoints or []),
        # The whole route, host by host, so a list can draw how routes converge
        # without one request per path. `asset_id` is the asset's own id (the one
        # the choke-point analysis uses), not the graph node key.
        "nodes": [{"asset_id": str(n).removeprefix("asset:"), "label": labels.get(str(n), str(n))}
                  for n in (r.path_nodes or [])],
    }


def _explain_hop(edge: dict, labels: dict[str, str]) -> str:
    src = labels.get(str(edge.get("source")), edge.get("source"))
    dst = labels.get(str(edge.get("target")), edge.get("target"))
    technique = edge.get("technique", "movement")
    via = edge.get("via") or []
    verb = {
        "CONNECTS_TO": "pivots over the network to",
        "SAME_SEGMENT": "moves laterally within the same segment to",
        "CREDENTIAL_REUSE": "reuses captured credentials to access",
        "RELAY": "relays coerced authentication to take over",
        "SAME_HOST": "is already on the same machine, which also answers as",
        "SAME_SUBNET": f"moves laterally within subnet {via[0] if via else ''} to",
        "CROSS_SUBNET": f"crosses from subnet {via[0] if via else '?'} into "
                        f"{via[-1] if via else '?'} to reach",
        "GATEWAY_ROUTE": f"routes through the compromised gateway into "
                         f"{via[-1] if via else 'another subnet'} to reach",
    }.get(technique, "reaches")
    suffix = f" and exploits it (CVSS {edge.get('cvss')})" if edge.get("exploited") else ""
    basis = edge.get("basis")
    caveats = []
    if technique == "RELAY":
        caveats.append("This NTLM relay assumes a coercion primitive is reachable and that LDAP "
                       "channel binding / EPA does not block it — verify before relying on it.")
    elif basis == "possible":
        caveats.append("This step reuses a shared/default credential; it holds only where that "
                       "credential has not been changed.")
    if basis == "assumed" and technique != "RELAY":
        caveats.append("Reachability between these subnets is assumed, not observed — verify segmentation.")
    elif basis == "assumed_cross_site":
        caveats.append("These are different SITES' private networks. That they are connected at all is "
                       "assumed and unlikely by default — confirm whether the sites are linked.")
    elif basis == "same_host_name":
        caveats.append("The two addresses are linked as one machine by host name only — confirm they are "
                       "the same device.")
    elif basis == "same_host_fqdn":
        caveats.append("The two addresses are linked as one machine by their shared fully qualified name.")
    if edge.get("stale"):
        caveats.append("The destination was not seen recently, so this step may no longer hold.")
    return f"From {src}, the attacker {verb} {dst}{suffix}." + "".join(" " + c for c in caveats)
