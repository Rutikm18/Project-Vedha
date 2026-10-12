"""Conservative finding-to-local-rule readiness; never fabricates a proof."""

from uuid import UUID

NORMALIZATION_VERSION = "finding-readiness@1"


def finding_readiness(
    finding: dict, assets: dict[str, dict], services: dict[str, dict]
) -> dict:
    """Input dictionaries are frozen scoped DB projections, not HTTP payloads.

    Existing raw findings are not normalized application-read assertions. Even a
    'confirmed' finding or unauthenticated banner cannot activate the data rule.
    """
    asset = assets.get(finding.get("asset_id"))
    raw = finding.get("evidence")
    evidence = raw if isinstance(raw, dict) else {}
    service = None
    service_id = evidence.get("service_id")
    if isinstance(service_id, str):
        try:
            service_id = str(UUID(service_id))
            candidate = services.get(service_id)
            if asset and candidate and candidate["asset_id"] == asset["id"]:
                service = candidate
        except ValueError:
            pass
    prerequisites = [
        {
            "key": "finding_asset_binding",
            "label": "Finding belongs to an assessed asset",
            "state": "supported" if asset else "missing",
            "detail": "Scoped asset reference exists."
            if asset
            else "Resolve the finding's assessed asset.",
        },
        {
            "key": "finding_service_binding",
            "label": "Exact datastore listener is identified",
            "state": "supported" if service else "missing",
            "detail": "Explicit scoped service reference exists."
            if service
            else "Bind the finding to a service ID, protocol, port and observed instance.",
        },
        {
            "key": "entry_context",
            "label": "Entry vantage and unauthenticated context are recorded",
            "state": "missing",
            "detail": "Normalize source-backed entry, principal and scenario evidence.",
        },
        {
            "key": "service_reachable_from_declared_entry",
            "label": "The declared entry can reach this listener",
            "state": "missing",
            "detail": "A subnet tag or general exposure label does not establish this relation.",
        },
        {
            "key": "unauthenticated_datastore_data_read_supported",
            "label": "Application data can be read without authentication",
            "state": "missing",
            "detail": "Require an explicit scoped read-operation observation; banners and metadata responses are insufficient.",
        },
        {
            "key": "observation_validity",
            "label": "Source time, validity and lineage are known",
            "state": "missing",
            "detail": "Normalize collection time and approved freshness policy; ingestion time is not a substitute.",
        },
    ]
    service_name = (
        (service or {}).get("service_name")
        or evidence.get("service")
        or evidence.get("service_name")
    )
    datastore = isinstance(service_name, str) and service_name.lower() in {
        "redis",
        "memcached",
        "mongodb",
        "elasticsearch",
        "couchdb",
        "cassandra",
        "mysql",
        "postgres",
        "postgresql",
        "mssql",
        "oracle",
    }
    if not datastore:
        prerequisites = prerequisites[:2] + [
            {
                "key": "reviewed_rule_applicability",
                "label": "A reviewed rule applies to this finding",
                "state": "missing",
                "detail": "This rule family has not been matched from explicit service evidence.",
            }
        ]
    return {
        "finding_id": finding["id"],
        "title": finding["title"],
        "severity": finding["severity"],
        "lifecycle": finding["status"],
        "asset_id": asset["id"] if asset else None,
        "service_id": service["id"] if service else None,
        "asset_label": (asset.get("hostname") or asset.get("ip_address") or asset["id"])
        if asset
        else "Asset binding unavailable",
        "goal": "Assess unauthenticated application-data read on the bound datastore"
        if datastore
        else "Rule applicability has not been established",
        "goal_state": "indeterminate" if datastore else "not_evaluated",
        "proof_status": "missing_prerequisites" if datastore else "not_evaluated",
        "rule_applicability": "candidate" if datastore else "unmapped",
        "realization": "not_observed_chain",
        "supported_proofs": 0,
        "prerequisites": prerequisites,
        "rule_version": "binding-contract@1",
        "rule_activation": "experimental_not_activated",
        "next_action": "Review missing evidence and confirm this rule applies to the finding.",
        "owner_ref": asset.get("owner") if asset else None,
        "verification_required": "Reassess the same listener and entry scenario with source-backed evidence.",
    }
