"""
posture_confidence.py — calibrated, auditable confidence for posture findings.

The CVE track already earns confidence honestly (verifier.py: evidence tiers →
transparent, logged downgrades, never a hidden fudge factor, only-ever-lower). The
posture track did not: it stamped a flat `_STATE_CONF[state]` (90/65/45) with no
evidence calibration and no audit trail. This module closes that gap and adds the one
piece neither track had — CROSS-SIGNAL CORROBORATION.

Two design rules, borrowed straight from verifier.py:
  * CONFIDENCE ("how likely is this a true positive") is separate from IMPACT
    (compute_risk's risk_score, "how bad if it's real"). This module only touches
    confidence; it never changes severity/risk/state.
  * Every factor is recorded in precision_factors{} — a reviewer can reconstruct the
    exact arithmetic. Nothing is a hidden multiplier.

The new idea: independent posture signals that compose a real attack path on ONE host
are far more likely to be true positives than any one alone (two independent
observations agreeing is strong evidence). So a finding that participates in a
corroborated attack chain gets a confidence FLOOR — the network-VA analogue of
AttackLens's cross_matrix "exploitable + reachable + running = 0.95" guarantee. The
floor applies ONLY when a genuine partner signal is present, so it can never falsely
inflate a lone finding.
"""
from __future__ import annotations

from typing import Any

from posture_rules import is_validated

# Evidence-tier base confidence (parallels verifier.py's _TIER_BASE). A validated
# scanner's posture finding is a DIRECT protocol observation (a real SMB/RDP/TLS
# handshake), not a version inference — that is inherently high-confidence. An
# unvalidated scanner is a single, uncorroborated signal until proven.
_VALIDATED_BASE = 85
_UNVALIDATED_BASE = 55

# Cross-signal attack chains. If ≥2 members co-occur on ONE host, every member
# finding's confidence is floored at the chain's value — the independent signals
# corroborate a real attack path. Ordered strongest-first; a finding in several
# chains takes the highest floor. These are DETECTION-time corroboration floors,
# complementary to (not a duplicate of) engine_bridge's attack-PATH findings.
ATTACK_CHAINS: list[tuple[str, frozenset[str], int]] = [
    # SMBv1 + SMB-signing-off = wormable transport AND NTLM-relay surface on one host.
    ("ntlm_relay_surface",
     frozenset({"POSTURE-SMB-V1-ENABLED", "POSTURE-SMB-SIGNING-OFF"}), 92),
    # RDP reachable AND without NLA = a confirmed pre-auth RDP attack surface.
    ("rdp_preauth_surface",
     frozenset({"POSTURE-RDP-NO-NLA", "POSTURE-RDP-EXPOSED"}), 88),
    # ≥2 TLS weaknesses on one host = systemic weak crypto, not a one-off.
    ("weak_tls_cluster",
     frozenset({"POSTURE-TLS-DEPRECATED-VERSION", "POSTURE-TLS-WEAK-CIPHER",
                "POSTURE-TLS-SELF-SIGNED", "POSTURE-TLS-EXPIRED-CERT"}), 85),
    # Enumerable/exposed Windows infra: RPC map + SMB weakness + default SNMP.
    ("exposed_windows_infra",
     frozenset({"POSTURE-MSRPC-EPMAP-EXPOSED", "POSTURE-SMB-V1-ENABLED",
                "POSTURE-SMB-SIGNING-OFF", "POSTURE-SNMP-DEFAULT-COMMUNITY"}), 82),
]

# Downgrade penalties (transparent, each logged). Confidence-affecting only — these
# say "we're less sure this observation is real", NOT "it's less exploitable" (that is
# impact, and compute_risk already handles auth/exposure there).
_PENALTY_UNREACHABLE = 20   # a filtered/unconfirmed port: we can't confirm the service
_PENALTY_DECEPTION_HI = 25  # implausible host fingerprint → possible honeypot/tarpit
_PENALTY_DECEPTION_LO = 10


def corroborating_chains(rule_id: str, host_rule_ids: set[str]) -> list[tuple[str, int]]:
    """Chains this rule belongs to where ≥1 OTHER member also fired on the host.
    A lone member (no partner) corroborates nothing and is deliberately excluded."""
    out: list[tuple[str, int]] = []
    for name, members, floor in ATTACK_CHAINS:
        if rule_id in members and (host_rule_ids & members) - {rule_id}:
            out.append((name, floor))
    return out


def assess_confidence(*, rule_id: str, scanner: str, evidence_ref_count: int,
                      reachable: bool, host_rule_ids: set[str],
                      deception: float = 0.0) -> tuple[int, dict[str, Any]]:
    """Return (confidence 0-100, precision_factors). Pure and deterministic:
    same inputs → same output, no clock/network/randomness (verifier.py's rule)."""
    factors: dict[str, Any] = {}
    validated = is_validated(scanner)
    conf = _VALIDATED_BASE if validated else _UNVALIDATED_BASE
    factors["base"] = {"tier": "validated_protocol" if validated else "unvalidated_single",
                       "value": conf}

    # ≥2 independent evidence refs agree → a small corroboration bump.
    if evidence_ref_count >= 2:
        conf += 5
        factors["multi_evidence"] = {"refs": evidence_ref_count, "delta": 5}

    # Cross-signal attack-chain corroboration → confidence FLOOR (the strong logic).
    chains = corroborating_chains(rule_id, host_rule_ids)
    if chains:
        floor = max(f for _, f in chains)
        applied = max(0, floor - conf)
        factors["chain_corroboration"] = {"chains": [n for n, _ in chains],
                                          "floor": floor, "applied": applied}
        conf = max(conf, floor)

    # ── downgrades (never raise) ──
    if not reachable:
        conf -= _PENALTY_UNREACHABLE
        factors["reachability_unconfirmed"] = -_PENALTY_UNREACHABLE
    if deception >= 0.5:
        conf -= _PENALTY_DECEPTION_HI
        factors["deception_suspected"] = -_PENALTY_DECEPTION_HI
    elif deception >= 0.25:
        conf -= _PENALTY_DECEPTION_LO
        factors["deception_possible"] = -_PENALTY_DECEPTION_LO

    conf = max(0, min(100, conf))
    factors["final"] = conf
    return conf, factors


def calibrate_host_findings(findings: list, *, reachable_by_id: dict,
                            deception: float = 0.0) -> None:
    """Second pass over ONE host's posture findings: now that every rule that fired on
    the host is known, calibrate each finding's confidence (with cross-signal
    corroboration) and stamp precision_factors. Mutates in place. `reachable_by_id`
    maps a finding's id() → whether its port was confirmed reachable."""
    host_rule_ids = {f.rule_id for f in findings}
    for f in findings:
        conf, factors = assess_confidence(
            rule_id=f.rule_id, scanner=f.scanner,
            evidence_ref_count=len(getattr(f, "evidence_refs", []) or []),
            reachable=reachable_by_id.get(id(f), True),
            host_rule_ids=host_rule_ids, deception=deception)
        f.confidence = conf
        f.precision_factors = factors
