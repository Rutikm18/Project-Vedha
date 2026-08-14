#!/usr/bin/env python3
"""
accuracy.py — the ground-truth accuracy harness.

Turns the scanner's core claim ("evidence-backed, anti-false-positive") into a
MEASURED number: precision / recall / F1 for findings, and OPEN precision/recall +
state accuracy for port states, scored against a labeled ground-truth corpus.

This is the credibility moat: a new scanner is distrusted until it can show its
false-positive and false-negative rates. Pure scoring — no network — so it runs in
CI over fixture corpora and, in the field, over a corpus built from an independent
remote validator.

Ground-truth discipline (from the offensive-spec, Phase 26): a port a host is
LISTENing on locally is NOT necessarily OPEN remotely (host/network firewall,
routing, vantage). The `ground_truth` fed here must therefore be the REMOTE-
validated state, not a local listener list — otherwise firewalled-but-listening
ports get miscounted as false negatives.
"""
from __future__ import annotations

from typing import Any, Iterable


# ── ratio helper ────────────────────────────────────────────────────────────
def _ratio(num: int, denom: int, default: float = 1.0) -> float:
    return round(num / denom, 4) if denom else default


# ── findings accuracy (the anti-FP number) ──────────────────────────────────
def _finding_key(f: Any) -> tuple:
    if isinstance(f, dict):
        return (f.get("rule_id"), f.get("target"), f.get("port"))
    return (getattr(f, "rule_id", None), getattr(f, "target", None), getattr(f, "port", None))


def _expected_keys(expected: Iterable) -> set:
    out = set()
    for e in expected:
        if isinstance(e, dict):
            out.add((e.get("rule_id"), e.get("target"), e.get("port")))
        else:  # tuple/list (rule_id, target, port)
            e = list(e)
            out.add((e[0], e[1], e[2] if len(e) > 2 else None))
    return out


def score_findings(expected: Iterable, produced: Iterable) -> dict[str, Any]:
    """Precision / recall / F1 of produced findings vs a labeled expected set.

    Keyed on (rule_id, target, port). `expected`/`produced` accept Finding objects,
    dicts, or (rule_id, target, port) tuples."""
    exp = _expected_keys(expected)
    prod = {_finding_key(f) for f in produced}
    tp, fp, fn = exp & prod, prod - exp, exp - prod

    precision = _ratio(len(tp), len(tp) + len(fp))
    recall = _ratio(len(tp), len(tp) + len(fn))
    f1 = round(2 * precision * recall / (precision + recall), 4) if (precision + recall) else 0.0

    by_rule: dict[str, dict[str, int]] = {}
    for k in tp:
        by_rule.setdefault(k[0], {"tp": 0, "fp": 0, "fn": 0})["tp"] += 1
    for k in fp:
        by_rule.setdefault(k[0], {"tp": 0, "fp": 0, "fn": 0})["fp"] += 1
    for k in fn:
        by_rule.setdefault(k[0], {"tp": 0, "fp": 0, "fn": 0})["fn"] += 1

    return {
        "tp": len(tp), "fp": len(fp), "fn": len(fn),
        "precision": precision, "recall": recall, "f1": f1,
        "false_positives": sorted(str(k) for k in fp),
        "false_negatives": sorted(str(k) for k in fn),
        "by_rule": by_rule,
    }


# ── port-state accuracy ─────────────────────────────────────────────────────
def _observed_states(facts: Iterable) -> dict[tuple, str]:
    """(target, port) -> status, from port/syn/mass scan facts (last one wins)."""
    out: dict[tuple, str] = {}
    for raw in facts:
        f = raw if isinstance(raw, dict) else {
            "scanner": getattr(raw, "scanner", None), "target": getattr(raw, "target", None),
            "port": getattr(raw, "port", None), "status": getattr(raw, "status", None)}
        if f.get("scanner") not in ("port_scan", "syn_scan", "mass_scan"):
            continue
        if f.get("port") is None:
            continue
        out[(f.get("target"), f.get("port"))] = f.get("status")
    return out


def score_port_states(ground_truth: dict, facts: Iterable) -> dict[str, Any]:
    """OPEN precision/recall + overall state accuracy vs a remote-validated
    ground truth {(target, port): state}."""
    observed = _observed_states(facts)
    open_tp = open_fp = open_fn = matches = 0
    mismatches: list[dict] = []
    for (target, port), gt in ground_truth.items():
        obs = observed.get((target, port), "unscanned")
        if obs == gt:
            matches += 1
        else:
            mismatches.append({"target": target, "port": port, "ground_truth": gt, "observed": obs})
        gt_open, obs_open = gt == "open", obs == "open"
        open_tp += gt_open and obs_open
        open_fp += obs_open and not gt_open
        open_fn += gt_open and not obs_open

    total = len(ground_truth)
    return {
        "total": total,
        "open_true_positives": open_tp, "open_false_positives": open_fp,
        "open_false_negatives": open_fn,
        "open_precision": _ratio(open_tp, open_tp + open_fp),
        "open_recall": _ratio(open_tp, open_tp + open_fn),
        "state_accuracy": _ratio(matches, total),
        "mismatches": mismatches,
    }


# ── corpus evaluation ───────────────────────────────────────────────────────
def evaluate_corpus(corpus: dict) -> dict[str, Any]:
    """Run the findings engine over a labeled corpus and score it.

    corpus = {name, facts:[...], expected_findings:[[rule_id,target,port]...],
              ground_truth_states?: {"target:port": state}}."""
    from main_scripts.findings import run_findings

    facts = corpus.get("facts", [])
    produced = run_findings(facts)
    result: dict[str, Any] = {
        "name": corpus.get("name", "corpus"),
        "produced_findings": len(produced),
        "findings": score_findings(corpus.get("expected_findings", []), produced),
    }
    gts = corpus.get("ground_truth_states")
    if gts:
        gt = {(k.rsplit(":", 1)[0], int(k.rsplit(":", 1)[1])): v for k, v in gts.items()}
        result["port_states"] = score_port_states(gt, facts)
    return result


def format_report(result: dict) -> str:
    f = result["findings"]
    lines = [
        f"=== accuracy: {result['name']} ===",
        f"findings: produced={result['produced_findings']} tp={f['tp']} fp={f['fp']} fn={f['fn']}",
        f"  precision={f['precision']}  recall={f['recall']}  f1={f['f1']}",
    ]
    if f["false_positives"]:
        lines.append(f"  false positives: {', '.join(f['false_positives'])}")
    if f["false_negatives"]:
        lines.append(f"  false negatives: {', '.join(f['false_negatives'])}")
    if "port_states" in result:
        p = result["port_states"]
        lines.append(f"port states: open_precision={p['open_precision']} "
                     f"open_recall={p['open_recall']} state_accuracy={p['state_accuracy']}")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    import argparse
    import json
    ap = argparse.ArgumentParser(description="Score the scanner against a labeled corpus")
    ap.add_argument("corpus", help="corpus JSON file")
    ap.add_argument("--json", action="store_true", help="emit the full result as JSON")
    args = ap.parse_args(argv)
    with open(args.corpus, encoding="utf-8") as fh:
        corpus = json.load(fh)
    result = evaluate_corpus(corpus)
    print(json.dumps(result, indent=2, default=str) if args.json else format_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
