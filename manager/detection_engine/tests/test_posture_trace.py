"""
test_posture_trace.py — the detection trace: every rule evaluation records an
OUTCOME, so a non-finding explains itself. This is the fix for the core defect
(the pipeline could not tell "checked and clean" from "never actually checked").

The load-bearing assertions:
  * MISSING_INPUT (probe drift) is NEVER rendered as NO_MATCH (silent false-clean).
  * detect_posture output is byte-for-byte unchanged (behaviour-preserving).
  * a rule that raises is isolated (ERROR), it does not blind the batch.
"""
from __future__ import annotations

from models import Asset, Fact, SourceConfidence
import posture_rules as P


def _fact(scanner, port, data, status="open", target="192.168.1.77"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred,
                source_file="s.jsonl", source_line=1)


def _asset(*facts, ip="192.168.1.77"):
    a = Asset(ip=ip, is_ip_keyed=True)
    for f in facts:
        a.add_fact(f)
    return a


def _outcome(traces, rule_id):
    return {t.outcome for t in traces if t.rule_id == rule_id}


# ── the distinction that fixes the silent false-negative ──────────────────────
class TestAbsentVersusClean:
    RULE = "POSTURE-SMB-V1-ENABLED"

    def test_key_present_true_is_match(self):
        _f, tr = P.detect_posture_traced(_asset(_fact("smb_scan", 445, {"smbv1_enabled": True})))
        assert _outcome(tr, self.RULE) == {P.OUTCOME_MATCH}
        assert P.verdict_for_rule(tr, self.RULE)[0] == P.VERDICT_FINDING

    def test_key_present_false_is_clean_no_match(self):
        # collected `false` is REAL data → genuinely clean, not drift.
        _f, tr = P.detect_posture_traced(_asset(_fact("smb_scan", 445, {"smbv1_enabled": False})))
        assert _outcome(tr, self.RULE) == {P.OUTCOME_NO_MATCH}
        assert P.verdict_for_rule(tr, self.RULE)[0] == P.VERDICT_CLEAN

    def test_key_absent_is_missing_input_not_clean(self):
        # THE bug this whole change exists to kill: the scanner ran, the smb fact is
        # present, but the field the rule reads is GONE (agent drift). This must be
        # MISSING_INPUT, never NO_MATCH — otherwise a vulnerable host looks clean.
        _f, tr = P.detect_posture_traced(_asset(_fact("smb_scan", 445, {"other": 1})))
        outcomes = _outcome(tr, self.RULE)
        assert P.OUTCOME_MISSING_INPUT in outcomes
        assert P.OUTCOME_NO_MATCH not in outcomes            # <-- the invariant
        verdict, reasons = P.verdict_for_rule(tr, self.RULE)
        assert verdict == P.VERDICT_SCHEMA_DRIFT
        assert reasons and "smbv1_enabled" in reasons[0]

    def test_missing_input_invariant_across_all_rules(self):
        """I10 structurally: for EVERY rule with a declared contract, feeding a fact
        for its scanner with none of its required paths yields MISSING_INPUT and
        never NO_MATCH."""
        for rule in P.RULES:
            if not rule.requires:
                continue
            a = _asset(_fact(rule.scanners[0], 445, {"unrelated_key": 1}))
            _f, tr = P.detect_posture_traced(a)
            outc = _outcome(tr, rule.rule_id)
            assert P.OUTCOME_MISSING_INPUT in outc, rule.rule_id
            assert P.OUTCOME_NO_MATCH not in outc, rule.rule_id


# ── no_evidence: the scanner never ran → not assessed, not "clean" ─────────────
class TestNoEvidence:
    def test_scanner_absent_yields_no_evidence(self):
        # only a port_scan fact → smb/rdp/tls rules were never assessed.
        _f, tr = P.detect_posture_traced(_asset(_fact("port_scan", 445, {"open": True})))
        assert _outcome(tr, "POSTURE-SMB-V1-ENABLED") == {P.OUTCOME_NO_EVIDENCE}
        assert P.verdict_for_rule(tr, "POSTURE-SMB-V1-ENABLED")[0] == P.VERDICT_NO_EVIDENCE

    def test_no_evidence_is_asset_scoped_not_per_fact(self):
        # smb fact present → smb rule assessed; rdp rule (no rdp fact) → exactly one
        # no_evidence row, not one per smb fact.
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}),
                   _fact("smb_scan", 139, {"smbv1_enabled": False}))
        _f, tr = P.detect_posture_traced(a)
        rdp = [t for t in tr if t.rule_id == "POSTURE-RDP-NO-NLA"]
        assert len(rdp) == 1 and rdp[0].outcome == P.OUTCOME_NO_EVIDENCE


# ── per-rule isolation: a raising detector cannot blind the batch ─────────────
class TestRuleIsolation:
    def test_raising_rule_is_error_and_others_still_fire(self, monkeypatch):
        boom = [r for r in P.RULES if r.rule_id == "POSTURE-RDP-EXPOSED"][0]
        monkeypatch.setattr(boom, "detect", lambda f: (_ for _ in ()).throw(RuntimeError("boom")))
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}),
                   _fact("rdp_scan", 3389, {"rdp_confirmed": True, "nla": True,
                                            "nla_required": True}))
        findings, tr = P.detect_posture_traced(a)
        # the SMBv1 finding still lands despite the RDP rule exploding
        assert any(f.rule_id == "POSTURE-SMB-V1-ENABLED" for f in findings)
        assert P.OUTCOME_ERROR in _outcome(tr, "POSTURE-RDP-EXPOSED")
        assert P.verdict_for_rule(tr, "POSTURE-RDP-EXPOSED")[0] == P.VERDICT_RULE_ERROR


# ── behaviour preservation: findings must be identical to the old path ─────────
class TestBehaviourPreserved:
    def _mixed(self):
        return _asset(
            _fact("smb_scan", 445, {"smbv1_enabled": True, "smb2_supported": True,
                                    "signing_required": False}),
            _fact("rdp_scan", 3389, {"rdp_confirmed": True, "nla": False,
                                     "nla_required": False}),
            _fact("tls_scan", 443, {"accepted_versions": ["TLSv1.0", "TLSv1.2"]}))

    def test_detect_posture_matches_traced_findings(self):
        a = self._mixed()
        via_wrapper = P.detect_posture(a)
        traced, _tr = P.detect_posture_traced(a)
        assert [f.finding_id for f in via_wrapper] == [f.finding_id for f in traced]
        # and it actually found the planted issues
        ids = {f.rule_id for f in via_wrapper}
        assert {"POSTURE-SMB-V1-ENABLED", "POSTURE-SMB-SIGNING-OFF",
                "POSTURE-RDP-NO-NLA", "POSTURE-TLS-DEPRECATED-VERSION"} <= ids

    def test_dedup_still_one_finding_per_rule_port_but_trace_per_eval(self):
        # two smb facts on the same port, both vulnerable → one finding, two MATCH traces.
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}),
                   _fact("smb_scan", 445, {"smbv1_enabled": True}))
        findings, tr = P.detect_posture_traced(a)
        smb_f = [f for f in findings if f.rule_id == "POSTURE-SMB-V1-ENABLED"]
        smb_matches = [t for t in tr if t.rule_id == "POSTURE-SMB-V1-ENABLED"
                       and t.outcome == P.OUTCOME_MATCH]
        assert len(smb_f) == 1 and len(smb_matches) == 2


# ── coverage roll-up ──────────────────────────────────────────────────────────
class TestSummarize:
    def test_summarize_counts_blind_rules(self):
        # smb fact missing the required key (drift) + a clean rdp fact.
        a = _asset(_fact("smb_scan", 445, {"nope": 1}),
                   _fact("rdp_scan", 3389, {"rdp_confirmed": True, "nla": True,
                                            "nla_required": True}))
        _f, tr = P.detect_posture_traced(a)
        s = P.summarize_traces(tr)
        assert s["rules_blind"] >= 1
        assert "POSTURE-SMB-V1-ENABLED" in s["blind_rule_ids"]
        assert s["rules_total"] == len(P.RULES)

    def test_every_verdict_is_reachable(self):
        # a verdict nobody can reach is dead diagnostics — prove each is produced.
        seen = set()
        # finding
        _f, tr = P.detect_posture_traced(_asset(_fact("smb_scan", 445, {"smbv1_enabled": True})))
        seen.add(P.verdict_for_rule(tr, "POSTURE-SMB-V1-ENABLED")[0])
        # clean
        _f, tr = P.detect_posture_traced(_asset(_fact("smb_scan", 445, {"smbv1_enabled": False})))
        seen.add(P.verdict_for_rule(tr, "POSTURE-SMB-V1-ENABLED")[0])
        # drift
        _f, tr = P.detect_posture_traced(_asset(_fact("smb_scan", 445, {"x": 1})))
        seen.add(P.verdict_for_rule(tr, "POSTURE-SMB-V1-ENABLED")[0])
        # no_evidence
        _f, tr = P.detect_posture_traced(_asset(_fact("port_scan", 80, {"open": True})))
        seen.add(P.verdict_for_rule(tr, "POSTURE-SMB-V1-ENABLED")[0])
        assert {P.VERDICT_FINDING, P.VERDICT_CLEAN, P.VERDICT_SCHEMA_DRIFT,
                P.VERDICT_NO_EVIDENCE} <= seen
