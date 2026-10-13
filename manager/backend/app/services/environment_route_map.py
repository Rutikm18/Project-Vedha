"""A sealed display projection of stored models, never a new attack inference."""

import hashlib

from sqlalchemy import String, case, cast, func, select

from app.models.asset import Asset
from app.models.attack_path import AttackPath
from app.models.engagement import Engagement
from app.models.finding import Finding

ROUTE_MAP_VERSION = "stored-environment-routes@1"
MAX_NODES, MAX_EDGES, MAX_FINDINGS, MAX_MODELS = 300, 600, 1000, 200


def value(v):
    return str(getattr(v, "value", v))


def qualified(engagement_id, entity_id):
    return f"{engagement_id}:{entity_id}"


def project_routes(assets, findings, paths, *, as_of, names, truncated=False):
    """Input rows must already be authorized and bounded by the capture adapter.

    Legacy `exploited`, finding verdict, CVSS and reachability basis never promote
    a whole hop to confirmed. Invalid or foreign references remain omitted gaps.
    """
    nodes, records, edges = {}, {}, {}
    omitted = 0
    for a in assets[:MAX_NODES]:
        key = qualified(a["engagement_id"], a["id"])
        nodes[key] = {
            "id": key,
            "assetId": str(a["id"]),
            "engagementId": str(a["engagement_id"]),
            "engagementName": names[str(a["engagement_id"])],
            "label": a.get("hostname") or a.get("ip_address") or str(a["id"]),
            "type": "crown" if value(a["criticality"]) == "critical" else "asset",
            "column": 3 if value(a["criticality"]) == "critical" else 2,
        }
    for f in findings[:MAX_FINDINGS]:
        key = qualified(f["engagement_id"], f["id"])
        records[key] = {
            "id": key,
            "findingId": str(f["id"]),
            "engagementId": str(f["engagement_id"]),
            "assetId": str(f["asset_id"]),
            "title": f["title"],
            "severity": value(f["severity"]),
            "lifecycle": value(f["status"]),
            "plainReason": "This finding supports a stored possible connection. The full connection has not been confirmed by a test.",
            "fixSteps": [
                line.strip(" -*•\t")[:400]
                for line in (f.get("remediation") or "").splitlines()
                if line.strip()
            ][:6],
            "fixed": value(f["status"]) == "remediated"
            and f.get("resolution_method") == "auto"
            and bool(f.get("resolution_run_id")),
            "findingConfirmed": f.get("verification_state") == "confirmed",
        }
    entries = set()
    for p in paths[:MAX_MODELS]:
        scope = str(p["engagement_id"])
        pnodes = [qualified(scope, n) for n in (p.get("path_nodes") or [])]
        for raw in p.get("path_edges") or []:
            if not isinstance(raw, dict):
                omitted += 1
                continue
            source, target = (
                qualified(scope, raw.get("source")),
                qualified(scope, raw.get("target")),
            )
            fid = qualified(scope, raw.get("finding"))
            finding = records.get(fid)
            if (
                source not in nodes
                or target not in nodes
                or source not in pnodes
                or target not in pnodes
                or not finding
                or finding["assetId"] != str(raw.get("target"))
                or finding["lifecycle"] == "fp"
            ):
                omitted += 1
                continue
            identity = f"{source}|{target}|{fid}"
            eid = hashlib.sha256(identity.encode()).hexdigest()[:24]
            if eid not in edges and len(edges) >= MAX_EDGES:
                truncated = True
                omitted += 1
                continue
            edges[eid] = {
                "id": eid,
                "from": source,
                "to": target,
                "findingId": fid,
                "status": "theoretical",
                "basis": str(raw.get("basis") or "unrecorded")[:80],
                "sourcePathId": str(p["id"]),
                "stale": bool(raw.get("stale")),
            }
            if pnodes and source == pnodes[0]:
                entries.add(source)
    for key in entries:
        nodes[key]["entry"] = True
        if nodes[key]["type"] != "crown":
            nodes[key].update(type="entry", column=0)
    return {
        "id": "captured-route-map",
        "takenAt": as_of.isoformat(),
        "grade": None,
        "nodes": list(nodes.values()),
        "edges": list(edges.values()),
        "findings": records,
        "source": "stored_models",
        "coverage": "partial",
        "version": ROUTE_MAP_VERSION,
        "truncated": truncated,
        "omittedConnections": omitted,
        "capturedModels": len(paths[:MAX_MODELS]),
    }


async def capture_route_map(db, tenant_id, ids, as_of, names):
    # Scope is reasserted at each read; JSON finding references never authorize.
    aq = (
        select(
            Asset.id,
            Asset.engagement_id,
            Asset.hostname,
            Asset.ip_address,
            Asset.criticality,
        )
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id, Asset.engagement_id.in_(ids))
        .order_by(Asset.engagement_id, Asset.id)
        .limit(MAX_NODES + 1)
    )
    fq = (
        select(
            Finding.id,
            Finding.engagement_id,
            Finding.asset_id,
            Finding.title,
            Finding.severity,
            Finding.status,
            func.substr(Finding.remediation, 1, 2400).label("remediation"),
            Finding.verification_state,
            Finding.resolution_method,
            Finding.resolution_run_id,
        )
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id, Finding.engagement_id.in_(ids))
        .order_by(Finding.engagement_id, Finding.id)
        .limit(MAX_FINDINGS + 1)
    )
    length = func.octet_length(cast(AttackPath.path_edges, String))
    node_length = func.octet_length(cast(AttackPath.path_nodes, String))
    bounded = (length <= 65536) & (node_length <= 32000)
    pq = (
        select(
            AttackPath.id,
            AttackPath.engagement_id,
            case((bounded, AttackPath.path_nodes), else_=None).label("path_nodes"),
            case((bounded, AttackPath.path_edges), else_=None).label("path_edges"),
            (~bounded).label("limited"),
        )
        .join(Engagement, AttackPath.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id, AttackPath.engagement_id.in_(ids))
        .order_by(AttackPath.engagement_id, AttackPath.id)
        .limit(MAX_MODELS + 1)
    )
    assets = [dict(r._mapping) for r in (await db.execute(aq)).all()]
    findings = [dict(r._mapping) for r in (await db.execute(fq)).all()]
    paths = [dict(r._mapping) for r in (await db.execute(pq)).all()]
    truncated = (
        len(assets) > MAX_NODES
        or len(findings) > MAX_FINDINGS
        or len(paths) > MAX_MODELS
        or any(p["limited"] for p in paths)
    )
    return project_routes(
        assets,
        findings,
        paths,
        as_of=as_of,
        names={str(k): v for k, v in names.items()},
        truncated=truncated,
    )
