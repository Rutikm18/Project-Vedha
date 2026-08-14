"""
test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.

Scores findings (precision/recall/F1) and port states (OPEN precision/recall,
state accuracy) against labeled corpora, and validates the real findings engine on
a fixture corpus — including the anti-false-positive proof (a clean host yields
zero findings ⇒ zero FP). Pure — no network.
"""
from __future__ import annotations

from main_scripts import accuracy as A


# ── findings scoring ─────────────────────────────────────────────────────────
def test_perfect_findings_score():
    exp = [("SMB-V1-ENABLED", "t", 445), ("SVC-TELNET-CLEARTEXT", "t", 23)]
    s = A.score_findings(exp, [dict(rule_id=r, target=t, port=p) for r, t, p in exp])
    assert s["tp"] == 2 and s["fp"] == 0 and s["fn"] == 0
    assert s["precision"] == 1.0 and s["recall"] == 1.0 and s["f1"] == 1.0


def test_false_positive_lowers_precision():
    exp = [("SMB-V1-ENABLED", "t", 445)]
    prod = [dict(rule_id="SMB-V1-ENABLED", target="t", port=445),
            dict(rule_id="SVC-RDP-EXPOSED", target="t", port=3389)]   # not expected -> FP
    s = A.score_findings(exp, prod)
    assert s["fp"] == 1 and s["precision"] == 0.5 and s["recall"] == 1.0


def test_false_negative_lowers_recall():
    exp = [("SMB-V1-ENABLED", "t", 445), ("SVC-TELNET-CLEARTEXT", "t", 23)]
    prod = [dict(rule_id="SMB-V1-ENABLED", target="t", port=445)]     # missed telnet -> FN
    s = A.score_findings(exp, prod)
    assert s["fn"] == 1 and s["recall"] == 0.5 and s["precision"] == 1.0


def test_by_rule_breakdown():
    exp = [("SMB-V1-ENABLED", "t", 445)]
    prod = [dict(rule_id="SVC-RDP-EXPOSED", target="t", port=3389)]
    s = A.score_findings(exp, prod)
    assert s["by_rule"]["SMB-V1-ENABLED"]["fn"] == 1
    assert s["by_rule"]["SVC-RDP-EXPOSED"]["fp"] == 1


def test_empty_expected_and_produced_is_perfect():
    s = A.score_findings([], [])
    assert s["tp"] == 0 and s["fp"] == 0 and s["precision"] == 1.0 and s["recall"] == 1.0


# ── port-state scoring ───────────────────────────────────────────────────────
def test_open_precision_recall_and_accuracy():
    gt = {("h", 22): "open", ("h", 80): "open", ("h", 23): "closed", ("h", 443): "filtered"}
    facts = [
        {"scanner": "port_scan", "target": "h", "port": 22, "status": "open"},     # TP
        {"scanner": "port_scan", "target": "h", "port": 80, "status": "filtered"},  # FN (missed open)
        {"scanner": "port_scan", "target": "h", "port": 23, "status": "open"},      # FP (closed called open)
        {"scanner": "port_scan", "target": "h", "port": 443, "status": "filtered"}, # state match
    ]
    s = A.score_port_states(gt, facts)
    assert s["open_true_positives"] == 1 and s["open_false_negatives"] == 1 and s["open_false_positives"] == 1
    assert s["open_precision"] == 0.5 and s["open_recall"] == 0.5
    assert s["state_accuracy"] == 0.5     # 22 + 443 correct out of 4


def test_unscanned_open_port_is_false_negative():
    gt = {("h", 9200): "open"}
    s = A.score_port_states(gt, [])       # nothing scanned it
    assert s["open_false_negatives"] == 1 and s["open_recall"] == 0.0
    assert s["mismatches"][0]["observed"] == "unscanned"


# ── corpus evaluation against the real engine ────────────────────────────────
def test_corpus_matches_real_engine_output():
    corpus = {
        "name": "smbv1+telnet",
        "facts": [
            {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
             "data": {"smbv1_enabled": True}},
            {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},
        ],
        "expected_findings": [
            ["SMB-V1-ENABLED", "t", 445],
            ["SVC-TELNET-CLEARTEXT", "t", 23],
        ],
    }
    r = A.evaluate_corpus(corpus)
    assert r["findings"]["precision"] == 1.0 and r["findings"]["recall"] == 1.0
    assert r["findings"]["fp"] == 0 and r["findings"]["fn"] == 0


def test_corpus_flags_a_missed_expected_finding():
    corpus = {
        "name": "missed",
        "facts": [{"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
                   "data": {"smbv1_enabled": True}}],
        # label expects a telnet finding the engine can't produce (no telnet fact) -> FN
        "expected_findings": [["SMB-V1-ENABLED", "t", 445], ["SVC-TELNET-CLEARTEXT", "t", 23]],
    }
    r = A.evaluate_corpus(corpus)
    assert r["findings"]["fn"] == 1 and r["findings"]["recall"] == 0.5


def test_clean_host_has_zero_false_positives():
    # The anti-FP proof: a hardened host produces no findings.
    corpus = {
        "name": "clean",
        "facts": [
            {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
             "data": {"smbv1_enabled": False, "signing_required": True, "signing_supported": True}},
            {"scanner": "port_scan", "target": "t", "port": 22, "proto": "tcp", "status": "open"},
        ],
        "expected_findings": [],
    }
    r = A.evaluate_corpus(corpus)
    assert r["produced_findings"] == 0
    assert r["findings"]["fp"] == 0 and r["findings"]["precision"] == 1.0


def test_corpus_scores_port_states_when_ground_truth_given():
    corpus = {
        "name": "states",
        "facts": [{"scanner": "port_scan", "target": "h", "port": 22, "status": "open"}],
        "expected_findings": [],
        "ground_truth_states": {"h:22": "open"},
    }
    r = A.evaluate_corpus(corpus)
    assert r["port_states"]["open_recall"] == 1.0 and r["port_states"]["state_accuracy"] == 1.0
