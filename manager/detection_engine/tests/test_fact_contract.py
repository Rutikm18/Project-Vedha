"""
test_fact_contract.py — the machine-checkable contract between the probe's emitters
and the manager's rules. §3 of the pipeline-hardening plan, and the highest-leverage
test in it: it catches the one failure no other test can.

A posture rule declares `requires` — the fact.data paths it reads. If the probe stops
emitting one of those paths (an agent-side rename between builds), the rule silently
stops firing and a vulnerable host looks clean. Unit tests of the rule still pass. The
ONLY way to catch it is to compare the rules' declared inputs against what the
scanners actually emit — which is what this does, against a captured corpus.

Corpus lives in tests/fixtures/probe_corpus/ (seed shapes today; replace with real
captures from GET /engagements/{id}/raw-facts — see that dir's README).
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import posture_rules as P
from ingest import ingest_files

CORPUS_DIR = Path(__file__).parent / "fixtures" / "probe_corpus"


def _load_corpus() -> list[dict]:
    facts: list[dict] = []
    for fp in sorted(CORPUS_DIR.glob("*.json")):
        facts.extend(json.loads(fp.read_text()))
    return facts


def _emitted_paths_by_scanner(facts: list[dict]) -> dict[str, set[str]]:
    """Map scanner -> set of top-level data keys it has been observed to emit."""
    out: dict[str, set[str]] = {}
    for f in facts:
        scanner = f.get("scanner")
        data = f.get("data")
        if not scanner or not isinstance(data, dict):
            continue
        out.setdefault(scanner, set()).update(data.keys())
    return out


def _ingest_corpus():
    """Run the corpus through the REAL ingester, exactly as engine_bridge does:
    one JSON fact per line, then ingest_files()."""
    facts = _load_corpus()
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
        for fact in facts:
            fh.write(json.dumps(fact, default=str) + "\n")
        tmp = fh.name
    try:
        return facts, ingest_files([tmp])
    finally:
        Path(tmp).unlink(missing_ok=True)


def test_corpus_is_present_and_nonempty():
    facts = _load_corpus()
    assert facts, f"probe corpus is empty at {CORPUS_DIR}"


def test_corpus_survives_ingestion():
    """The gate the name-level check above cannot provide: a corpus whose field NAMES
    all look right is still worthless if ingest rejects the records wholesale. Every
    downstream rule reads ingest's Assets, so a fact that never becomes one can never
    fire anything — the host reports clean and nothing logs an error.

    Compare against the real ingester, not against json.loads."""
    facts, ing = _ingest_corpus()
    reasons = sorted({q.reason for q in ing.quarantined})
    assert not ing.quarantined, (
        f"{len(ing.quarantined)}/{len(facts)} corpus facts are rejected by ingest "
        f"and can never reach a rule. Reasons: {reasons}\n"
        "The corpus must be the shape the ingester actually accepts "
        "(see ingest.REQUIRED_FIELDS).")
    assert ing.assets, "corpus ingested to zero assets — no rule can fire"


def test_every_rule_input_is_emitted_by_its_scanner():
    """The gate: for every rule, every declared `requires` path must be emitted by at
    least one of that rule's scanners somewhere in the corpus. A rule reading a path
    no scanner emits can never fire."""
    emitted = _emitted_paths_by_scanner(_load_corpus())
    unsatisfied: list[str] = []
    for rule in P.RULES:
        for path in rule.requires:
            top = path.split(".")[0]                     # requires are data-relative
            if not any(top in emitted.get(s, set()) for s in rule.scanners):
                unsatisfied.append(
                    f"{rule.rule_id}: requires data.{path} but no scanner "
                    f"{rule.scanners} emits it")
    assert not unsatisfied, (
        "Rules read fact paths no scanner emits — they can never fire:\n  "
        + "\n  ".join(unsatisfied)
        + "\n(If the probe legitimately renamed a field, update the rule AND capture "
          "the new shape into tests/fixtures/probe_corpus/.)")


def test_report_unconsumed_evidence():
    """Reverse direction, informational: data the probe collects that NO rule reads.
    Not a failure — it's the backlog of detections you could write from data already
    on disk. Printed so it's visible in -s runs."""
    emitted = _emitted_paths_by_scanner(_load_corpus())
    consumed = {p.split(".")[0] for r in P.RULES for p in r.requires}
    unconsumed = {
        f"{scanner}.{key}" for scanner, keys in emitted.items()
        for key in keys if key not in consumed
    }
    # Assert nothing — just surface it. Detection backlog, not a defect.
    print(f"\n[fact-contract] {len(unconsumed)} emitted paths no rule consumes "
          f"(detection backlog): {sorted(unconsumed)[:20]}")
    assert True
