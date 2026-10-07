"""
Attack path analysis API (AttackPathService).

GET /engagements/{id}/attack-paths            — paginated paths sorted by risk
GET /engagements/{id}/attack-paths/{path_id}  — full path detail, hop-by-hop
GET /engagements/{id}/chokepoints             — chokepoint assets + remediation priority
GET /engagements/{id}/blast-radius/{asset_id} — assets reachable if asset is owned
GET /engagements/{id}/attack-graph            — D3-compatible graph JSON

Paths are computed from the engagement's assets/services/findings, scored, and
persisted to the ``attack_paths`` table so ``/{path_id}`` can return a stable,
shareable record. The graph engine runs in-memory (NetworkX); Neo4j is mirrored
only when enabled.
"""
from __future__ import annotations

import hashlib
import uuid
from decimal import Decimal

import structlog
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import DB, AuthUser
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder
from app.graph.visualizer import GraphVisualizer
from app.models.asset import Asset
from app.models.attack_path import AttackPath
from app.models.engagement import Engagement
from app.models.enums import AssetCriticality
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements/{engagement_id}", tags=["attack-paths"])
logger = structlog.get_logger()


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

    stored = (await db.execute(
        select(AttackPath.id).where(AttackPath.engagement_id == engagement_id).limit(1)
    )).first()
    diagnostics = None
    if refresh or stored is None:
        # First read of a never-computed engagement still produces a result.
        diagnostics = await _recompute_and_store(db, engagement_id, target_asset_id)

    q = select(AttackPath).where(AttackPath.engagement_id == engagement_id)
    q = q.order_by(AttackPath.risk_score.desc().nullslast(), AttackPath.id)
    rows = (await db.execute(q.offset((page - 1) * page_size).limit(page_size))).scalars().all()
    total = len((await db.execute(
        select(AttackPath.id).where(AttackPath.engagement_id == engagement_id)
    )).all())

    body = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_path_summary(r) for r in rows],
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
            "explanation": _explain_hop(edge, labels),
        })

    return {
        "id": str(path.id),
        "risk_score": float(path.risk_score) if path.risk_score is not None else None,
        "node_count": len(path.path_nodes or []),
        "nodes": [labels.get(str(n), str(n)) for n in (path.path_nodes or [])],
        "hops": hops,
        "chokepoints": [labels.get(str(c), str(c)) for c in (path.chokepoints or [])],
    }


# ── GET /chokepoints ──────────────────────────────────────────────────────────

@router.get("/chokepoints", summary="Chokepoint assets with remediation priority")
async def list_chokepoints(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    analyzer, _graph = await _build_analyzer(db, engagement_id)

    paths = _all_paths_to_critical(analyzer, await _critical_asset_ids(db, engagement_id))
    chokepoints = analyzer.identify_chokepoints(paths)
    labels = await _asset_labels(db, engagement_id)
    for c in chokepoints:
        c["label"] = labels.get(str(c["asset_id"]), c["asset_id"])
    return {"count": len(chokepoints), "chokepoints": chokepoints}


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


async def _target_ids(db: AsyncSession, engagement_id: uuid.UUID,
                      target_asset_id: uuid.UUID | None) -> list[str]:
    if target_asset_id:
        return [str(target_asset_id)]
    return await _critical_asset_ids(db, engagement_id)


async def _recompute_and_store(
    db: AsyncSession, engagement_id: uuid.UUID, target_asset_id: uuid.UUID | None
) -> dict:
    """Recompute and UPSERT the engagement's paths. Returns the analyzer's
    diagnostics so the caller can explain an empty result."""
    await _lock_engagement_paths(db, engagement_id)
    analyzer, _graph = await _build_analyzer(db, engagement_id)
    targets = await _target_ids(db, engagement_id, target_asset_id)
    paths = _all_paths_to_critical(analyzer, targets)

    chokepoints = analyzer.identify_chokepoints(paths)
    choke_ids = [c["asset_id"] for c in chokepoints]

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
        row.chokepoints = choke_ids
    await db.flush()
    logger.info("graph.paths.stored", engagement=str(engagement_id), count=len(wanted),
                removed=len(stale))
    return analyzer.diagnose(targets)


async def _asset_labels(db: AsyncSession, engagement_id: uuid.UUID) -> dict[str, str]:
    rows = (await db.execute(
        select(Asset.id, Asset.hostname, Asset.ip_address).where(
            Asset.engagement_id == engagement_id
        )
    )).all()
    return {str(r[0]): (r[1] or r[2] or str(r[0])) for r in rows}


def _path_summary(r: AttackPath) -> dict:
    return {
        "id": str(r.id),
        "risk_score": float(r.risk_score) if r.risk_score is not None else None,
        "hops": max(len(r.path_nodes or []) - 1, 0),
        "source": str(r.path_nodes[0]) if r.path_nodes else None,
        "target": str(r.path_nodes[-1]) if r.path_nodes else None,
        "chokepoint_count": len(r.chokepoints or []),
    }


def _explain_hop(edge: dict, labels: dict[str, str]) -> str:
    src = labels.get(str(edge.get("source")), edge.get("source"))
    dst = labels.get(str(edge.get("target")), edge.get("target"))
    technique = edge.get("technique", "movement")
    verb = {
        "CONNECTS_TO": "pivots over the network to",
        "SAME_SEGMENT": "moves laterally within the same segment to",
        "CREDENTIAL_REUSE": "reuses captured credentials to access",
    }.get(technique, "reaches")
    suffix = f" and exploits it (CVSS {edge.get('cvss')})" if edge.get("exploited") else ""
    return f"From {src}, the attacker {verb} {dst}{suffix}."
