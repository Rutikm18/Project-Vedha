"""
attack_matrix.py — roll a mixed finding set up into a MITRE ATT&CK tactic /
technique matrix.

Every detection track now tags findings with ATT&CK techniques — the posture
rules (`mitre`), the host-posture/IOA rules, the fingerprint-IOC layer, and the
composite attack paths (`mitre_techniques`). What was missing was the view that
turns those per-finding tags into the question an operator and a report actually
ask: "across this engagement, which adversary tactics and techniques is the
estate exposed to, and which findings drive each one?"

This is the exposure-side analogue of the red/blue DetectionCorrelator's ATT&CK
coverage summary: that one grades whether the blue team DETECTED simulated
techniques; this one maps the VA's own findings onto the matrix so the report can
show tactic coverage and let a reader pivot from a technique to its evidence.

Pure, deterministic, dependency-free. An unknown technique id is never dropped —
it lands in an `unmapped` bucket so a newly-introduced technique surfaces for
curation instead of silently vanishing (same discipline as the detectors: make
the gap visible, never guess).
"""
from __future__ import annotations

from typing import Any

# ── technique -> (name, primary ATT&CK tactic) ────────────────────────────────
# Curated for exactly the techniques this engine's rules emit (see the detectors
# in detection_engine/posture_rules.py, host_posture.py, fingerprint_intel.py and
# this package's attack_paths.py). Each technique's PRIMARY tactic is used; many
# ATT&CK techniques list several, and the primary is the one that matches how the
# finding presents in a network VA.
TECHNIQUES: dict[str, tuple[str, str]] = {
    "T1005": ("Data from Local System", "Collection"),
    "T1021": ("Remote Services", "Lateral Movement"),
    "T1021.001": ("Remote Services: RDP", "Lateral Movement"),
    "T1021.005": ("Remote Services: VNC", "Lateral Movement"),
    "T1039": ("Data from Network Shared Drive", "Collection"),
    "T1040": ("Network Sniffing", "Credential Access"),
    "T1071.001": ("Application Layer Protocol: Web Protocols", "Command and Control"),
    "T1078": ("Valid Accounts", "Initial Access"),
    "T1078.001": ("Valid Accounts: Default Accounts", "Initial Access"),
    "T1087.002": ("Account Discovery: Domain Account", "Discovery"),
    "T1087.003": ("Account Discovery: Email Account", "Discovery"),
    "T1133": ("External Remote Services", "Initial Access"),
    "T1135": ("Network Share Discovery", "Discovery"),
    "T1190": ("Exploit Public-Facing Application", "Initial Access"),
    "T1210": ("Exploitation of Remote Services", "Lateral Movement"),
    "T1213": ("Data from Information Repositories", "Collection"),
    "T1496": ("Resource Hijacking", "Impact"),
    "T1498.002": ("Network DoS: Reflection Amplification", "Impact"),
    "T1505": ("Server Software Component", "Persistence"),
    "T1543.003": ("Create or Modify System Process: Windows Service", "Persistence"),
    "T1557": ("Adversary-in-the-Middle", "Credential Access"),
    "T1557.001": ("AiTM: LLMNR/NBT-NS Poisoning and SMB Relay", "Credential Access"),
    "T1562.001": ("Impair Defenses: Disable or Modify Tools", "Defense Evasion"),
    "T1571": ("Non-Standard Port", "Command and Control"),
    "T1574.009": ("Hijack Execution Flow: Unquoted Path", "Privilege Escalation"),
    "T1590.002": ("Gather Victim Network Info: DNS", "Reconnaissance"),
    "T1602.001": ("Data from Config Repository: SNMP", "Collection"),
    "T1610": ("Deploy Container", "Execution"),
}

# ATT&CK Enterprise kill-chain order, so the matrix renders tactics left-to-right
# the way the ATT&CK Navigator does.
TACTIC_ORDER = [
    "Reconnaissance", "Resource Development", "Initial Access", "Execution",
    "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access",
    "Discovery", "Lateral Movement", "Collection", "Command and Control",
    "Exfiltration", "Impact",
]
_UNMAPPED_TACTIC = "Unmapped"


def _techniques_of(finding: Any) -> list[str]:
    """Pull ATT&CK technique ids from a finding, whether it is a posture dict
    (`mitre`: single id), a composite dict (`mitre_techniques`: list), or an
    object with those attributes. Deduped, order-preserving, blanks dropped."""
    def _get(obj, key):
        if isinstance(obj, dict):
            return obj.get(key)
        return getattr(obj, key, None)

    out: list[str] = []
    single = _get(finding, "mitre")
    if isinstance(single, str) and single.strip():
        out.append(single.strip())
    multi = _get(finding, "mitre_techniques")
    if isinstance(multi, (list, tuple)):
        out.extend(t.strip() for t in multi if isinstance(t, str) and t.strip())
    # dedupe preserving order
    seen: set[str] = set()
    uniq: list[str] = []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _finding_ref(finding: Any) -> dict:
    """A compact, stable handle for a finding in the matrix output."""
    def _get(key):
        if isinstance(finding, dict):
            return finding.get(key)
        return getattr(finding, key, None)

    return {
        "finding_id": _get("finding_id"),
        "rule_id": _get("rule_id"),
        "asset_ip": _get("asset_ip") or _get("target"),
        "severity": str(_get("severity")) if _get("severity") is not None else None,
        "title": _get("title"),
    }


def build_attack_matrix(findings: list) -> dict:
    """Roll `findings` (posture + host-posture + IOC + composite descriptors, as
    dicts or objects) into an ATT&CK tactic/technique matrix.

    Returns:
      {
        "tactics": [ { "tactic", "technique_count", "finding_count",
                       "techniques": [ { "technique_id", "name", "finding_count",
                                         "findings": [ref, ...] } ] } ],
        "techniques_seen": [tid, ...],      # sorted, deduped
        "unmapped_techniques": [tid, ...],  # ids not in the curated table
        "counts": { "tactics", "techniques", "findings_mapped" },
      }
    Tactics are emitted in ATT&CK kill-chain order; any unmapped technique is
    collected under a trailing 'Unmapped' tactic rather than dropped."""
    # tactic -> technique_id -> list[finding ref]
    acc: dict[str, dict[str, list[dict]]] = {}
    techniques_seen: set[str] = set()
    unmapped: set[str] = set()
    mapped_findings = 0

    for f in findings or []:
        tids = _techniques_of(f)
        if not tids:
            continue
        ref = _finding_ref(f)
        counted = False
        for tid in tids:
            techniques_seen.add(tid)
            if tid in TECHNIQUES:
                tactic = TECHNIQUES[tid][1]
            else:
                tactic = _UNMAPPED_TACTIC
                unmapped.add(tid)
            acc.setdefault(tactic, {}).setdefault(tid, []).append(ref)
            counted = True
        if counted:
            mapped_findings += 1

    ordered_tactics = [t for t in TACTIC_ORDER if t in acc]
    if _UNMAPPED_TACTIC in acc:
        ordered_tactics.append(_UNMAPPED_TACTIC)

    tactics_out: list[dict] = []
    for tactic in ordered_tactics:
        techs = acc[tactic]
        tech_list: list[dict] = []
        for tid in sorted(techs):
            refs = techs[tid]
            tech_list.append({
                "technique_id": tid,
                "name": TECHNIQUES.get(tid, (tid, tactic))[0],
                "finding_count": len(refs),
                "findings": refs,
            })
        tactics_out.append({
            "tactic": tactic,
            "technique_count": len(tech_list),
            "finding_count": sum(t["finding_count"] for t in tech_list),
            "techniques": tech_list,
        })

    return {
        "tactics": tactics_out,
        "techniques_seen": sorted(techniques_seen),
        "unmapped_techniques": sorted(unmapped),
        "counts": {
            "tactics": len(tactics_out),
            "techniques": len(techniques_seen),
            "findings_mapped": mapped_findings,
        },
    }
