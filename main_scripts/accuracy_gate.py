#!/usr/bin/env python3
"""
accuracy_gate.py — turn `accuracy.py` from an instrument into a MERGE GATE
(RESEARCH_IMPROVEMENTS.md roadmap #4 / Tier 1.3).

`accuracy.py` can already score precision/recall/F1 and OPEN precision/recall.
What was missing is the thing that makes those numbers matter: a corpus on disk,
thresholds, and a non-zero exit code when a change makes the scanner worse. This
module supplies all three so accuracy is MEASURED on every change instead of
asserted in a README.

THE PROVENANCE RULE (the reason this file is not just a for-loop)
-----------------------------------------------------------------
There are two different instruments here and conflating them is the classic way
a scanner "proves" accuracy it does not have:

  * A REGRESSION corpus is labeled with what this engine currently produces. It
    catches drift — a refactor that changes behaviour — and nothing else. If the
    engine is wrong today, the corpus faithfully enshrines the wrong answer.
  * A GROUND-TRUTH corpus is labeled by an INDEPENDENT observer (nmap from the
    same vantage, a second probe, hand verification). Only this one can tell you
    the scanner is CORRECT.

So every corpus must declare `provenance`, and only independently-labeled
corpora count toward the accuracy thresholds. A regression corpus that drifts
still fails the gate — it just cannot be cited as evidence of accuracy.

`accuracy.py`'s own discipline still applies to ground truth: a port a host
LISTENs on locally is not necessarily OPEN remotely. Labels must be the
remote-validated state from the scanner's vantage, never a local `ss -ltn` dump.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .accuracy import evaluate_corpus, format_report

# Labels produced by an observer independent of this engine. Only these count as
# evidence of ACCURACY; everything else is regression-only.
INDEPENDENT_PROVENANCE = frozenset({
    "nmap",                     # scored against nmap from the same vantage
    "manual_remote_validation",  # hand-verified remotely by an operator
    "second_vantage",           # a second probe acting as validator
    "vendor_documented",        # the target's own documented exposure
})

# Regression baselines: useful, but explicitly NOT accuracy evidence.
REGRESSION_PROVENANCE = frozenset({"self_regression"})

DEFAULT_THRESHOLDS: dict[str, float] = {
    "min_precision": 0.95,      # false positives destroy operator trust fastest
    "min_recall": 0.90,
    "min_open_precision": 0.98,  # a phantom OPEN port is the worst single defect
    "min_open_recall": 0.95,
    "min_state_accuracy": 0.95,
}


class CorpusError(ValueError):
    """A corpus is malformed or unlabeled — a gate failure, never a silent pass."""


def load_corpus(path: Path) -> dict:
    """Load and structurally validate one corpus file."""
    try:
        corpus = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CorpusError(f"{path.name}: unreadable corpus ({exc})") from exc
    if not isinstance(corpus, dict):
        raise CorpusError(f"{path.name}: corpus must be a JSON object")
    corpus.setdefault("name", path.stem)

    prov = corpus.get("provenance")
    if prov not in (INDEPENDENT_PROVENANCE | REGRESSION_PROVENANCE):
        raise CorpusError(
            f"{path.name}: provenance must be one of "
            f"{sorted(INDEPENDENT_PROVENANCE | REGRESSION_PROVENANCE)}, got {prov!r}. "
            "An unlabeled corpus cannot be scored — it would let an untested "
            "change pass the gate.")
    if not corpus.get("facts"):
        raise CorpusError(f"{path.name}: corpus has no facts to score")
    # A corpus with no labels at all scores a vacuous 1.0 on everything.
    if not corpus.get("expected_findings") and not corpus.get("ground_truth_states"):
        raise CorpusError(
            f"{path.name}: corpus has neither expected_findings nor "
            "ground_truth_states — it would pass vacuously")
    return corpus


def load_corpora(directory: str | Path) -> list[dict]:
    """Every *.json corpus in `directory`, sorted by name for stable reports."""
    d = Path(directory)
    if not d.is_dir():
        raise CorpusError(f"{d}: corpus directory does not exist")
    return [load_corpus(p) for p in sorted(d.glob("*.json"))]


def is_independent(corpus: dict) -> bool:
    """True when this corpus's labels can support an ACCURACY claim."""
    return corpus.get("provenance") in INDEPENDENT_PROVENANCE


def check_thresholds(result: dict, thresholds: dict[str, float]) -> list[str]:
    """Threshold violations for one scored corpus (empty list = passed)."""
    name = result.get("name", "corpus")
    out: list[str] = []
    f = result.get("findings") or {}
    # Only score a dimension the corpus author actually LABELED. A corpus that
    # labels port states but not findings must not have every produced finding
    # counted as a false positive — that would punish a partially-labeled corpus
    # for the labels it never claimed to provide. Equally, a dimension with no
    # labels at all reports a vacuous 1.0 and must not be treated as a pass.
    findings_labeled = result.get("findings_labeled", True)
    if findings_labeled and f.get("tp", 0) + f.get("fp", 0) + f.get("fn", 0) > 0:
        if f.get("precision", 1.0) < thresholds["min_precision"]:
            out.append(f"{name}: findings precision {f['precision']} < "
                       f"{thresholds['min_precision']} (false positives: "
                       f"{', '.join(f.get('false_positives', [])) or 'none listed'})")
        if f.get("recall", 1.0) < thresholds["min_recall"]:
            out.append(f"{name}: findings recall {f['recall']} < "
                       f"{thresholds['min_recall']} (missed: "
                       f"{', '.join(f.get('false_negatives', [])) or 'none listed'})")
    p = result.get("port_states")
    if p and p.get("total", 0) > 0:
        if p.get("open_precision", 1.0) < thresholds["min_open_precision"]:
            out.append(f"{name}: OPEN precision {p['open_precision']} < "
                       f"{thresholds['min_open_precision']} "
                       f"({p.get('open_false_positives')} phantom open ports)")
        if p.get("open_recall", 1.0) < thresholds["min_open_recall"]:
            out.append(f"{name}: OPEN recall {p['open_recall']} < "
                       f"{thresholds['min_open_recall']} "
                       f"({p.get('open_false_negatives')} missed open ports)")
        if p.get("state_accuracy", 1.0) < thresholds["min_state_accuracy"]:
            out.append(f"{name}: state accuracy {p['state_accuracy']} < "
                       f"{thresholds['min_state_accuracy']}")
    return out


def run_gate(directory: str | Path,
             thresholds: dict[str, float] | None = None) -> dict[str, Any]:
    """Score every corpus in `directory` and collect threshold violations.

    Returns {passed, violations, results, independent_corpora, regression_corpora}.
    `passed` is False if ANY corpus violates a threshold — a regression corpus
    drifting is still a failure, it simply is not accuracy evidence.
    """
    th = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    corpora = load_corpora(directory)
    results, violations = [], []
    independent = regression = 0
    for corpus in corpora:
        result = evaluate_corpus(corpus)
        # Record which dimensions this corpus actually claims to label.
        result["findings_labeled"] = "expected_findings" in corpus
        result["provenance"] = corpus.get("provenance")
        result["independent"] = is_independent(corpus)
        if result["independent"]:
            independent += 1
        else:
            regression += 1
        results.append(result)
        violations.extend(check_thresholds(result, th))
    return {
        "passed": not violations,
        "violations": violations,
        "results": results,
        "independent_corpora": independent,
        "regression_corpora": regression,
        "thresholds": th,
    }


def format_gate_report(gate: dict) -> str:
    lines = []
    for r in gate["results"]:
        body = format_report(r)
        if not r.get("findings_labeled", True):
            # accuracy.py always prints a findings block; without labels its
            # "false positives" are just unlabeled output, not defects. Say so,
            # or the report reads as a failure the gate correctly ignored.
            body += ("\n  (findings dimension NOT labeled in this corpus — the "
                     "line above is unscored and did not affect the gate)")
        body += ("   [independent — accuracy evidence]" if r["independent"]
                 else "   [regression baseline only — NOT accuracy evidence]")
        lines.append(body)
    lines.append("")
    lines.append(f"corpora: {gate['independent_corpora']} independent, "
                 f"{gate['regression_corpora']} regression-only")
    if gate["violations"]:
        lines.append("THRESHOLD VIOLATIONS:")
        lines.extend(f"  - {v}" for v in gate["violations"])
    else:
        lines.append("all corpora within thresholds")
    if not gate["independent_corpora"]:
        lines.append("WARNING: no independently-labeled corpus present, so these "
                     "numbers prove only that behaviour has not drifted — they do "
                     "NOT prove the scanner is accurate. Add a corpus labeled by "
                     "nmap or a second vantage (see the fixtures README).")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Score every labeled corpus and gate on accuracy thresholds")
    ap.add_argument("directory", help="directory of *.json corpora")
    ap.add_argument("--json", action="store_true", help="emit the full result as JSON")
    for key, val in DEFAULT_THRESHOLDS.items():
        ap.add_argument(f"--{key.replace('_', '-')}", type=float, default=val)
    args = ap.parse_args(argv)
    overrides = {k: getattr(args, k) for k in DEFAULT_THRESHOLDS}
    try:
        gate = run_gate(args.directory, overrides)
    except CorpusError as exc:
        print(f"corpus error: {exc}")
        return 2
    print(json.dumps(gate, indent=2, default=str) if args.json
          else format_gate_report(gate))
    return 0 if gate["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(_main())
