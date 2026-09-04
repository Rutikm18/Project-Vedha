"""
test_accuracy_gate.py — the accuracy MERGE GATE (roadmap #4 / Tier 1.3).

`accuracy.py` could always compute precision/recall; what it could not do was
FAIL. These tests cover the gate that makes the numbers binding, and — more
importantly — the two ways an accuracy harness lies to you:

  1. A corpus with no labels scores a vacuous 1.0 on everything.
  2. A corpus labeled from the engine's own output proves only that behaviour
     has not drifted, yet gets quoted as proof the scanner is accurate.

The gate must refuse (1) outright and clearly mark (2). Pure — no network.
"""
from __future__ import annotations

import json

import pytest

from main_scripts import accuracy_gate as G

_CORPUS_DIR = "tests/fixtures/accuracy_corpus"


def _write(tmp_path, name, corpus):
    p = tmp_path / f"{name}.json"
    p.write_text(json.dumps(corpus), encoding="utf-8")
    return p


_FACT = {"scanner": "smb_scan", "target": "10.0.0.10", "port": 445,
         "status": "open", "data": {"smbv1_enabled": True}}

# Port-state scoring only reads port_scan/syn_scan/mass_scan facts — a protocol
# fact is deliberately NOT a port-state observation.
def _port_fact(status="open", port=445):
    return {"scanner": "port_scan", "target": "10.0.0.10", "port": port,
            "status": status, "data": {"reason": "connect_success"}}


# ── the shipped corpora ──────────────────────────────────────────────────────
class TestShippedCorpora:
    def test_gate_passes_on_the_committed_corpora(self):
        """CI's actual assertion: the engine still matches every labeled corpus."""
        gate = G.run_gate(_CORPUS_DIR)
        assert gate["passed"], "\n".join(gate["violations"])

    def test_every_shipped_corpus_declares_provenance(self):
        for c in G.load_corpora(_CORPUS_DIR):
            assert c["provenance"] in (
                G.INDEPENDENT_PROVENANCE | G.REGRESSION_PROVENANCE)

    def test_report_marks_regression_corpora_as_not_accuracy_evidence(self):
        report = G.format_gate_report(G.run_gate(_CORPUS_DIR))
        assert "NOT accuracy evidence" in report

    def test_an_independently_labeled_corpus_is_committed(self):
        """Without one of these the gate proves only non-drift, never accuracy."""
        gate = G.run_gate(_CORPUS_DIR)
        assert gate["independent_corpora"] >= 1
        assert "WARNING" not in G.format_gate_report(gate)

    def test_every_independent_corpus_scores_perfectly(self):
        """Locks in the measured results: every port state agrees with nmap on
        both the loopback corpus and the live Windows 11 LAN host."""
        gate = G.run_gate(_CORPUS_DIR)
        independent = [x for x in gate["results"] if x["independent"]]
        assert len(independent) >= 2
        for r in independent:
            p = r["port_states"]
            assert p["state_accuracy"] == 1.0, r["name"]
            assert p["open_precision"] == 1.0 and p["open_recall"] == 1.0, r["name"]
        by_name = {r["name"]: r["port_states"]["total"] for r in independent}
        assert by_name["loopback_ports_1_1024_nmap_validated"] == 1024
        assert by_name["lab65_win11_nmap_positive_evidence"] == 903

    def test_unlabeled_findings_dimension_is_marked_in_the_report(self):
        report = G.format_gate_report(G.run_gate(_CORPUS_DIR))
        assert "did not affect the gate" in report

    def test_regression_only_directory_still_warns(self, tmp_path):
        _write(tmp_path, "r", {"provenance": "self_regression",
                               "facts": [_port_fact()],
                               "ground_truth_states": {"10.0.0.10:445": "open"}})
        assert "WARNING" in G.format_gate_report(G.run_gate(tmp_path))


# ── refusing to pass vacuously ───────────────────────────────────────────────
class TestCorpusValidation:
    def test_unlabeled_provenance_is_rejected(self, tmp_path):
        _write(tmp_path, "c", {"facts": [_FACT], "expected_findings": []})
        with pytest.raises(G.CorpusError, match="provenance"):
            G.load_corpora(tmp_path)

    def test_unknown_provenance_is_rejected(self, tmp_path):
        _write(tmp_path, "c", {"provenance": "vibes", "facts": [_FACT],
                               "expected_findings": [["R", "t", 1]]})
        with pytest.raises(G.CorpusError, match="provenance"):
            G.load_corpora(tmp_path)

    def test_corpus_without_any_labels_is_rejected(self, tmp_path):
        # The vacuous-pass trap: no labels => precision/recall are 1.0 by default.
        _write(tmp_path, "c", {"provenance": "nmap", "facts": [_FACT]})
        with pytest.raises(G.CorpusError, match="vacuously"):
            G.load_corpora(tmp_path)

    def test_corpus_without_facts_is_rejected(self, tmp_path):
        _write(tmp_path, "c", {"provenance": "nmap", "facts": [],
                               "expected_findings": [["R", "t", 1]]})
        with pytest.raises(G.CorpusError, match="no facts"):
            G.load_corpora(tmp_path)

    def test_malformed_json_is_a_gate_error_not_a_crash(self, tmp_path):
        (tmp_path / "bad.json").write_text("{not json", encoding="utf-8")
        with pytest.raises(G.CorpusError, match="unreadable"):
            G.load_corpora(tmp_path)

    def test_missing_directory_is_rejected(self):
        with pytest.raises(G.CorpusError, match="does not exist"):
            G.load_corpora("no/such/dir")

    def test_ground_truth_states_alone_is_a_valid_corpus(self, tmp_path):
        _write(tmp_path, "c", {"provenance": "nmap", "facts": [_port_fact()],
                               "ground_truth_states": {"10.0.0.10:445": "open"}})
        assert len(G.load_corpora(tmp_path)) == 1


# ── provenance semantics ─────────────────────────────────────────────────────
class TestProvenance:
    def test_nmap_labels_count_as_accuracy_evidence(self):
        assert G.is_independent({"provenance": "nmap"}) is True

    def test_self_regression_labels_do_not(self):
        assert G.is_independent({"provenance": "self_regression"}) is False

    def test_gate_counts_the_two_kinds_separately(self, tmp_path):
        _write(tmp_path, "a", {"provenance": "nmap", "facts": [_port_fact()],
                               "ground_truth_states": {"10.0.0.10:445": "open"}})
        _write(tmp_path, "b", {"provenance": "self_regression",
                               "facts": [_port_fact()],
                               "ground_truth_states": {"10.0.0.10:445": "open"}})
        gate = G.run_gate(tmp_path)
        assert gate["independent_corpora"] == 1
        assert gate["regression_corpora"] == 1


# ── thresholds actually bind ─────────────────────────────────────────────────
class TestThresholds:
    def test_phantom_open_port_trips_open_precision(self):
        result = {"name": "c", "findings": {},
                  "port_states": {"total": 2, "open_precision": 0.5,
                                  "open_recall": 1.0, "state_accuracy": 1.0,
                                  "open_false_positives": 1}}
        v = G.check_thresholds(result, G.DEFAULT_THRESHOLDS)
        assert any("OPEN precision" in x for x in v)

    def test_missed_open_port_trips_open_recall(self):
        result = {"name": "c", "findings": {},
                  "port_states": {"total": 4, "open_precision": 1.0,
                                  "open_recall": 0.5, "state_accuracy": 1.0,
                                  "open_false_negatives": 2}}
        v = G.check_thresholds(result, G.DEFAULT_THRESHOLDS)
        assert any("OPEN recall" in x for x in v)

    def test_false_positive_finding_trips_precision(self):
        result = {"name": "c",
                  "findings": {"tp": 1, "fp": 5, "fn": 0, "precision": 0.16,
                               "recall": 1.0, "false_positives": ["X"]}}
        v = G.check_thresholds(result, G.DEFAULT_THRESHOLDS)
        assert any("precision" in x for x in v)

    def test_unlabeled_dimension_is_skipped_not_scored_as_perfect(self):
        # zero labels => no violation, but also no false confidence
        result = {"name": "c", "findings": {"tp": 0, "fp": 0, "fn": 0,
                                            "precision": 1.0, "recall": 1.0}}
        assert G.check_thresholds(result, G.DEFAULT_THRESHOLDS) == []

    def test_clean_result_produces_no_violations(self):
        result = {"name": "c",
                  "findings": {"tp": 3, "fp": 0, "fn": 0, "precision": 1.0,
                               "recall": 1.0},
                  "port_states": {"total": 3, "open_precision": 1.0,
                                  "open_recall": 1.0, "state_accuracy": 1.0}}
        assert G.check_thresholds(result, G.DEFAULT_THRESHOLDS) == []

    def test_thresholds_are_overridable(self, tmp_path):
        # A genuinely missed open port fails by default...
        _write(tmp_path, "a", {"provenance": "nmap",
                               "facts": [_port_fact("filtered")],
                               "ground_truth_states": {"10.0.0.10:445": "open"}})
        assert G.run_gate(tmp_path)["passed"] is False
        # ...and passes only when the operator explicitly lowers the bar.
        relaxed = G.run_gate(tmp_path, {"min_open_recall": 0.0,
                                        "min_state_accuracy": 0.0})
        assert relaxed["passed"] is True

    def test_matching_port_state_scores_perfectly(self, tmp_path):
        _write(tmp_path, "a", {"provenance": "nmap", "facts": [_port_fact("open")],
                               "ground_truth_states": {"10.0.0.10:445": "open"}})
        gate = G.run_gate(tmp_path)
        assert gate["passed"] is True
        assert gate["results"][0]["port_states"]["open_recall"] == 1.0


class TestCli:
    def test_cli_exits_zero_on_passing_corpora(self, capsys):
        assert G._main([_CORPUS_DIR]) == 0

    def test_cli_exits_two_on_a_corpus_error(self, capsys):
        assert G._main(["no/such/dir"]) == 2

    def test_cli_json_mode_is_machine_readable(self, capsys):
        G._main([_CORPUS_DIR, "--json"])
        assert json.loads(capsys.readouterr().out)["passed"] is True
