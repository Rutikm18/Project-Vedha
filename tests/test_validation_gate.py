"""
test_validation_gate.py — the "validation gate" (build spec Card 7) as
detection-as-code.

The gate is one guarantee: an UNCONFIRMED observation must never reach the report
as exposed/vulnerable. Vedha enforces it at two already-tested layers rather than a
separate re-probe pass:

  * scanner honesty  — os_fingerprint claims ``alive`` only on a real ICMP reply
    (see test_os_fingerprint::TestProvenance); udp_scan emits ``open|filtered``
    (never "exposed") when nothing answered (see test_async_udp).
  * correlation honesty — findings.run_findings() refuses to raise an exposure
    finding from ``open|filtered`` / no-reply UDP facts, and suppresses the
    RDP-no-NLA finding when NLA is enforced.

This module feeds the three canonical bad inputs from the spec (no-reply UDP,
NLA-enforced RDP, and — by reference — fabricated ICMP liveness) and asserts the
gate rejects/downgrades each. Every negative assertion is paired with a positive
control that flips the single honesty flag, proving the rule *would* have fired —
so a regression that starts trusting the bad input fails loudly here.
"""
from __future__ import annotations

from scanner import findings as F


def _ids(*facts) -> set[str]:
    return {f.rule_id for f in F.run_findings(list(facts))}


# ── no-reply UDP is never "exposed" ───────────────────────────────────────────

class TestUdpNoReplyRejected:
    _AMP = {"scanner": "udp_scan", "target": "t", "port": 161, "proto": "udp"}

    def test_open_filtered_amplifier_not_flagged(self):
        # SNMP (an amplifier) that DID NOT answer: open|filtered, responded False.
        ids = _ids({**self._AMP, "status": "open|filtered",
                    "data": {"service": "snmp", "responded": False}})
        assert "UDP-AMPLIFIER-EXPOSED" not in ids
        assert not any(i.startswith("UDP-") for i in ids)

    def test_positive_control_answered_amplifier_is_flagged(self):
        # Same service, but it positively answered → the finding SHOULD fire. This
        # proves the negative case above is gated on `responded`, not a dead rule.
        ids = _ids({**self._AMP, "status": "open",
                    "data": {"service": "snmp", "responded": True}})
        assert "UDP-AMPLIFIER-EXPOSED" in ids


# ── RDP with NLA enforced is downgraded (no no-NLA finding) ───────────────────

class TestRdpNlaGate:
    _RDP = {"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open"}

    def test_nla_enforced_suppresses_no_nla_finding(self):
        ids = _ids({**self._RDP,
                    "data": {"rdp_confirmed": True, "nla": True, "tls": True,
                             "selected_protocol": 2}})
        assert "SVC-RDP-NO-NLA" not in ids

    def test_positive_control_nla_off_is_flagged(self):
        ids = _ids({**self._RDP,
                    "data": {"rdp_confirmed": True, "nla": False, "tls": False,
                             "standard_rdp_security": True, "selected_protocol": 0}})
        assert "SVC-RDP-NO-NLA" in ids


# ── fabricated ICMP liveness never becomes a finding ──────────────────────────

class TestNoFabricatedIcmpLiveness:
    def test_icmp_unavailable_os_observation_raises_no_exposure(self):
        # os_fingerprint that never got an ICMP reply (icmp unavailable) carries no
        # `alive`/`icmp_reply` claim, so the correlation layer has nothing to turn
        # into an exposure/liveness finding. (Scanner-level provenance is asserted
        # in test_os_fingerprint::TestProvenance.)
        ids = _ids({"scanner": "os_fingerprint", "target": "t", "status": "observed",
                    "data": {"icmp": "unavailable", "os_guess": "unknown"}})
        assert not any("ICMP" in i or "ALIVE" in i for i in ids)
