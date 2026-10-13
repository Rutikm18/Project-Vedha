from datetime import datetime, timezone

from app.services.environment_route_map import project_routes


def fixtures():
    assets = [
        {
            "id": "source",
            "engagement_id": "a",
            "hostname": "Gateway",
            "criticality": "medium",
        },
        {
            "id": "target",
            "engagement_id": "a",
            "hostname": "Customer data",
            "criticality": "critical",
        },
        {
            "id": "target",
            "engagement_id": "b",
            "hostname": "Customer data",
            "criticality": "high",
        },
    ]
    finding = {
        "id": "f",
        "engagement_id": "a",
        "asset_id": "target",
        "title": "Access review",
        "severity": "high",
        "status": "open",
        "verification_state": "confirmed",
        "remediation": "Restrict access.\nRecheck.",
    }
    edge = {
        "source": "source",
        "target": "target",
        "finding": "f",
        "basis": "observed",
        "exploited": True,
    }
    path = {
        "id": "path",
        "engagement_id": "a",
        "path_nodes": ["source", "target"],
        "path_edges": [edge, edge],
    }
    return assets, [finding], [path]


def run(assets, findings, paths):
    return project_routes(
        assets,
        findings,
        paths,
        as_of=datetime.now(timezone.utc),
        names={"a": "Assessment A", "b": "Assessment B"},
    )


def test_scoped_nodes_stored_edges_and_operator_criticality_are_not_upgraded_to_proof():
    graph = run(*fixtures())
    assert len(graph["nodes"]) == 3
    assert [n["id"] for n in graph["nodes"] if n["type"] == "crown"] == ["a:target"]
    assert len(graph["edges"]) == 1
    assert graph["edges"][0]["status"] == "theoretical"
    assert graph["findings"]["a:f"]["findingConfirmed"]
    assert graph["grade"] is None


def test_foreign_unresolved_and_destination_mismatches_are_reported_not_drawn():
    assets, findings, paths = fixtures()
    paths[0]["path_edges"][0] = {
        "source": "foreign",
        "target": "target",
        "finding": "f",
    }
    paths[0]["path_edges"][1] = {
        "source": "source",
        "target": "target",
        "finding": "missing",
    }
    graph = run(assets, findings, paths)
    assert graph["edges"] == []
    assert graph["omittedConnections"] == 2
    findings[0]["asset_id"] = "source"
    assert run(assets, findings, fixtures()[2])["edges"] == []


def test_only_recorded_coverage_gated_auto_resolution_counts_as_a_scan_fix():
    assets, findings, paths = fixtures()
    findings[0].update(status="remediated", resolution_method="manual")
    assert not run(assets, findings, paths)["findings"]["a:f"]["fixed"]
    findings[0].update(resolution_method="auto", resolution_run_id="recorded-run")
    assert run(assets, findings, paths)["findings"]["a:f"]["fixed"]
