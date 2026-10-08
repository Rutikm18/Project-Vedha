"""
validation.py — ground-truth harness for attack-path accuracy (P5, FM-31).

Every other test asserts what the code does. This measures whether what it does is
RIGHT, against small networks whose true attack paths are written down by hand. It
exists because graph code fails quietly: a wrong edge or a missing hub still returns
a plausible-looking path, and LLM-/heuristic-generated attack graphs have been
measured at up to 84% noise paths. Node counts do not catch that; structure does.

A fixture is JSON: a tiny network (assets, which are exploitable, scope, posture,
identity mode), the crown jewels, and `truth`:

  valid_hops          every host-to-host step that is genuinely possible
  expected_paths      paths that MUST be found                    (recall)
  forbidden_hops      steps that must NEVER appear                (false positives)
  unreachable_targets targets that must have NO path
  expected_freshness  {"a>b>c": "fresh|partly_stale|stale"}
  independent_routes  {target: n}  vertex-disjoint routes
  min_fix_set         the smallest cut, as a set of host ids
  top_choke           the host that fixing removes the most risk

Metrics:
  recall              expected paths found / expected paths
  cascade_validity    for each predicted path, the fraction of its hops that are valid
                      BEFORE THE FIRST INVALID ONE. An attack path is a chain: once a
                      step is false, everything after it is false too, however real
                      the later hops look — so a path is credited only up to its first
                      mistake. Averaged over predicted paths.
  fabricated_paths    predicted paths whose very first hop is invalid

A fixture passes only if recall is 1, nothing forbidden appears, no unreachable target
is reached, no path is fabricated and cascade validity is exactly 1.

Run on a directory:  python -m app.graph.validation tests/fixtures/attack_paths
"""
from __future__ import annotations

import json
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder

FIXED_NOW = datetime(2026, 10, 8, tzinfo=timezone.utc)


@dataclass
class _Asset:
    id: str
    ip_address: str | None
    site_id: str | None = None
    hostname: str | None = None
    fqdn: str | None = None
    device_role: str | None = None
    criticality: str = "medium"
    environment: str | None = None
    tags: dict = field(default_factory=dict)
    last_seen: datetime | None = None


@dataclass
class _Finding:
    id: uuid.UUID
    asset_id: str
    title: str = "fixture weakness"
    severity: str = "high"
    cvss_score: Decimal | None = Decimal("8.0")
    exploitable: bool = True
    exploit_validated: bool = False
    status: str = "open"


def build_graph(fixture: dict[str, Any], now: datetime = FIXED_NOW):
    """The graph the production assembly produces for this fixture's network."""
    assets = []
    for a in fixture["assets"]:
        age = a.get("last_seen_days_ago")
        assets.append(_Asset(
            id=a["id"], ip_address=a.get("ip"), site_id=a.get("site"), hostname=a.get("hostname"),
            fqdn=a.get("fqdn"), device_role=a.get("role"), criticality=a.get("criticality", "medium"),
            environment=a.get("environment"),
            last_seen=(now - timedelta(days=age)) if age is not None else None))
    findings = [_Finding(uuid.uuid4(), aid) for aid in fixture.get("exploitable", [])]
    roe = {"asset_identity": fixture.get("identity", "global"),
           "attack_path_reachability": fixture.get("posture", "flat")}
    return GraphBuilder().assemble("fixture", assets, [], findings, scope_cidrs=fixture.get("scope", []),
                                   rules_of_engagement=roe, now=now)


def cascade_validity(nodes: list[str], valid_hops: set[tuple[str, str]]) -> float:
    """Share of a path's hops that hold before the first one that does not."""
    hops = list(zip(nodes, nodes[1:]))
    if not hops:
        return 1.0
    good = 0
    for hop in hops:
        if hop not in valid_hops:
            break
        good += 1
    return good / len(hops)


def run_fixture(fixture: dict[str, Any], now: datetime = FIXED_NOW) -> dict[str, Any]:
    truth = fixture.get("truth", {})
    graph = build_graph(fixture, now)
    analyzer = PathAnalyzer(graph)
    targets = list(fixture["targets"])

    predicted: list[dict[str, Any]] = []
    for t in targets:
        predicted.extend(analyzer.find_paths_to_target(t, max_paths_per_source=10))

    valid = {tuple(h) for h in truth.get("valid_hops", [])}
    forbidden = {tuple(h) for h in truth.get("forbidden_hops", [])}
    expected = [list(p) for p in truth.get("expected_paths", [])]
    got = [p["nodes"] for p in predicted]

    failures: list[str] = []
    missing = [p for p in expected if p not in got]
    for p in missing:
        failures.append(f"missing expected path {' > '.join(p)}")
    recall = 1.0 if not expected else (len(expected) - len(missing)) / len(expected)

    scores = [cascade_validity(nodes, valid) for nodes in got] if valid else []
    if valid:
        for nodes, s in zip(got, scores):
            if s < 1.0:
                failures.append(f"invalid step in {' > '.join(nodes)} (valid up to {s:.0%})")
    fabricated = sum(1 for nodes, s in zip(got, scores) if s == 0.0 and len(nodes) > 1)

    seen_hops = {(a, b) for nodes in got for a, b in zip(nodes, nodes[1:])}
    for hop in sorted(seen_hops & forbidden):
        failures.append(f"forbidden hop appeared: {hop[0]} > {hop[1]}")

    reached = {p["target"] for p in predicted}
    for t in truth.get("unreachable_targets", []):
        if t in reached:
            failures.append(f"target {t} must be unreachable but has a path")

    for key, want in (truth.get("expected_freshness") or {}).items():
        match = next((p for p in predicted if ">".join(p["nodes"]) == key), None)
        if match is None:
            failures.append(f"freshness check: no path {key}")
        elif match["freshness"] != want:
            failures.append(f"path {key} is {match['freshness']}, expected {want}")

    if any(k in truth for k in ("independent_routes", "min_fix_set", "top_choke")):
        choke = analyzer.choke_analysis(targets)
        if "independent_routes" in truth and choke["min_fix_set"]["independent_routes"] != truth["independent_routes"]:
            failures.append(f"independent routes {choke['min_fix_set']['independent_routes']} != {truth['independent_routes']}")
        if "min_fix_set" in truth and sorted(choke["min_fix_set"]["assets"]) != sorted(truth["min_fix_set"]):
            failures.append(f"minimum fix set {choke['min_fix_set']['assets']} != {truth['min_fix_set']}")
        if "top_choke" in truth and (not choke["ranked"] or choke["ranked"][0]["asset_id"] != truth["top_choke"]):
            top = choke["ranked"][0]["asset_id"] if choke["ranked"] else None
            failures.append(f"top choke point is {top}, expected {truth['top_choke']}")

    metrics = {
        "predicted_paths": len(got),
        "recall": round(recall, 3),
        "cascade_validity": round(sum(scores) / len(scores), 3) if scores else 1.0,
        "fabricated_paths": fabricated,
    }
    return {"name": fixture.get("name", "unnamed"), "passed": not failures, "metrics": metrics, "failures": failures}


def load_fixtures(directory: Path) -> list[dict[str, Any]]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(directory).glob("*.json"))]


def evaluate_directory(directory: Path, now: datetime = FIXED_NOW) -> dict[str, Any]:
    reports = [run_fixture(f, now) for f in load_fixtures(directory)]
    return {
        "fixtures": len(reports),
        "passed": sum(1 for r in reports if r["passed"]),
        "mean_recall": round(sum(r["metrics"]["recall"] for r in reports) / len(reports), 3) if reports else 0.0,
        "mean_cascade_validity": round(
            sum(r["metrics"]["cascade_validity"] for r in reports) / len(reports), 3) if reports else 0.0,
        "reports": reports,
    }


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python -m app.graph.validation <fixtures-directory>", file=sys.stderr)
        return 2
    result = evaluate_directory(Path(argv[0]))
    if not result["fixtures"]:
        print(f"no fixtures found in {argv[0]}", file=sys.stderr)
        return 1                       # checking nothing is not a pass
    for r in result["reports"]:
        m = r["metrics"]
        print(f"{'PASS' if r['passed'] else 'FAIL'}  {r['name']:<34} recall={m['recall']:.2f} "
              f"cascade={m['cascade_validity']:.2f} fabricated={m['fabricated_paths']}")
        for f in r["failures"]:
            print(f"        - {f}")
    print(f"\n{result['passed']}/{result['fixtures']} fixtures pass; mean recall {result['mean_recall']:.2f}, "
          f"mean cascade validity {result['mean_cascade_validity']:.2f}")
    return 0 if result["passed"] == result["fixtures"] else 1


if __name__ == "__main__":
    sys.exit(main())
