"""
verifier.py — Phase 3: the generalized verifier, the anti-false-positive
backbone. EVERY Finding passes through verify() exactly once.

It lifts the evidence-tiered confidence model (originally hand-rolled inside
the probe's mcp_ai_scanner) into one shared, calibrated pass that assigns:
  - confidence       0-100, derived from an explicit evidence tier then
                     adjusted by transparent downgrade rules
  - evidence_reason  one human-readable line naming every factor applied
  - checks{}         the machine-readable audit of each signal/penalty

DESIGN RULES:
  - The verifier NEVER UPGRADES a deterministic state. confirmed (from
    authoritative credentialed data) stays confirmed; the verifier only
    ever LOWERS confidence / downgrades suspected→potential. Anti-FP means
    erring toward doubt, never toward false certainty.
  - Every adjustment is logged in checks{} with its penalty — nothing is a
    hidden fudge factor. A reviewer can reconstruct the exact arithmetic.
  - Pure and deterministic: same Finding (+ context) → same confidence,
    every run. No clock, no randomness, no network.

Evidence tiers (high → low), per the spec:
  4 authoritative_credentialed  the host's own credentialed inventory said so
  3 protocol_confirmed          a real protocol handshake (db greeting, TLS)
  2 multi_signal_corroborated   ≥2 independent evidence refs agree
  1 single_banner_inferred      one inferred banner/header, uncorroborated
"""
from __future__ import annotations

from enum import IntEnum

from models import Finding, FindingState, SourceConfidence

# scanners whose facts are a real protocol handshake, not a free-text banner —
# a version from these is "protocol-confirmed" even though it's network-
# observed (still not authoritative: distro backports can mask it, so it
# never reaches the credentialed tier).
_PROTOCOL_SCANNERS = {"db_scan", "tls_scan", "smb_scan"}


class EvidenceTier(IntEnum):
    single_banner_inferred = 1
    multi_signal_corroborated = 2
    protocol_confirmed = 3
    authoritative_credentialed = 4


_TIER_BASE = {4: 95, 3: 85, 2: 70, 1: 50}


def _evidence_scanners(finding: Finding) -> set[str]:
    """The scanner names behind this finding's evidence refs. A ref looks
    like 'file.jsonl:42' — the scanner isn't in the ref itself, but the
    finding's notes carry the basis (e.g. 'db_scan engine=...'); we read
    the protocol signal from there. Best-effort: absence just means we
    can't claim the protocol tier, which fails safe (lower tier)."""
    found: set[str] = set()
    blob = " ".join(finding.notes).lower()
    for s in _PROTOCOL_SCANNERS:
        if s in blob:
            found.add(s)
    return found


def classify_tier(finding: Finding) -> EvidenceTier:
    if finding.source_confidence == SourceConfidence.authoritative:
        return EvidenceTier.authoritative_credentialed
    if _evidence_scanners(finding):
        return EvidenceTier.protocol_confirmed
    if len(set(finding.evidence_refs)) >= 2:
        return EvidenceTier.multi_signal_corroborated
    return EvidenceTier.single_banner_inferred


def deception_score(distinct_products: int, contradictory_os: bool) -> float:
    """A starter honeypot/deception heuristic (0.0-1.0). Real hosts run a
    handful of services from a few vendors; a host advertising a large,
    incoherent spread of unrelated products — or contradictory OS signals
    (claims Windows on one port, Linux SSH on another, an embedded RTOS on
    a third) — is a classic tarpit/honeypot tell. Deliberately conservative:
    only a clearly implausible host scores high enough to penalize, so we
    don't punish legitimately busy servers.
    """
    score = 0.0
    if distinct_products >= 8:      # an implausible vendor spread for one host
        score += 0.5
    elif distinct_products >= 6:
        score += 0.25
    if contradictory_os:
        score += 0.4
    return min(1.0, score)


def verify(finding: Finding, *, reachability: str = "open",
           deception: float = 0.0) -> Finding:
    """Calibrate and stamp a Finding. Mutates and returns it.

    reachability: "open" (default) | "filtered" — a filtered port can't be
        confirmed reachable, so any finding inferred from it is less certain.
    deception:    0.0-1.0 from deception_score() for the finding's host.
    """
    tier = classify_tier(finding)
    conf = _TIER_BASE[int(tier)]
    checks: dict = {"evidence_tier": tier.name,
                    "evidence_refs": len(set(finding.evidence_refs)),
                    "base_confidence": conf}
    reasons = [f"{tier.name} (base {conf})"]

    def penalize(amount: int, key: str, why: str, value=True):
        nonlocal conf
        conf -= amount
        checks[key] = value
        reasons.append(f"{why} (-{amount})")

    # Backport-aware downgrade — the single biggest FP source for inferred
    # findings: a distro can backport the security fix while keeping the
    # upstream version string unchanged, so a version-only match is suspect.
    if any("backport-possible" in n for n in finding.notes):
        penalize(20, "backport_possible", "version-inferred, backport-possible")

    # AI-normalized candidates get extra scrutiny — capped, never trusted
    # like a rule-based or credentialed match.
    if finding.ai_assisted:
        if conf > 60:
            checks["ai_assisted_cap"] = 60
            reasons.append(f"AI-normalized, capped {conf}→60")
            conf = 60
        else:
            checks["ai_assisted"] = True

    # Reachability — a filtered port isn't confirmed reachable.
    if reachability == "filtered":
        penalize(15, "port_filtered", "port filtered, reachability unconfirmed")

    # Global auth gate (the carried-forward MCP false-negative lesson):
    # auth being enforced lowers exploitability confidence for this finding.
    if finding.auth_enforced is True:
        penalize(10, "auth_enforced", "authentication enforced")

    # Honeypot/deception heuristic.
    if deception >= 0.5:
        penalize(25, "deception_suspected", "implausible host fingerprint, possible honeypot",
                 value=round(deception, 2))
    elif deception >= 0.25:
        penalize(10, "deception_possible", "somewhat implausible host fingerprint",
                 value=round(deception, 2))

    conf = max(0, min(100, conf))
    finding.confidence = conf
    finding.checks = checks
    finding.evidence_reason = "; ".join(reasons)

    # State is only ever LOWERED, never raised (see module docstring).
    # A confirmed/authoritative finding is immune — credentialed truth isn't
    # second-guessed by heuristics. A weak suspected finding becomes potential.
    if (finding.state == FindingState.suspected
            and finding.source_confidence != SourceConfidence.authoritative
            and conf < 40):
        finding.state = FindingState.potential
        checks["state_downgraded"] = "suspected→potential (confidence < 40)"

    return finding
