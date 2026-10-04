"""
fingerprint_intel.py — TLS fingerprint threat-intelligence (IOC) matching.

The probe computes three stable TLS fingerprints and ships them as facts:
  * JARM    (tls_fingerprint.tls_fingerprint) — active 10-probe server hash
  * JA4S    (tls_fingerprint.ja4s / tls_scan)  — ServerHello fingerprint
  * JA4X    (tls_scan.certificate.ja4x)         — X.509 structural fingerprint

A server's selection behaviour across these is a stable property of its TLS
stack + configuration, so a fingerprint can identify the SOFTWARE behind an
endpoint — including C2 frameworks and malware tooling that ship recognisable
default TLS profiles (Cobalt Strike, Metasploit/Meterpreter HTTPS handlers, etc).

The probe has the match MECHANISM (ja4x.match_suspicious / ja4s.match_suspicious)
but its registries are empty stubs AND, critically, the probe's findings layer
that would call them "never ran on the production detection path" (see
attack_paths.py). So the manager computed, shipped and stored these fingerprints
and then matched NONE of them — a whole IOC dimension went unused.

This module brings fingerprint-IOC matching onto the manager's detection path:
a curated, cited, EXTENSIBLE registry + an exact-match mechanism, mirroring the
probe's stance — "what matters is the match mechanism, not a bundled blocklist".

HONESTY RULES (shape everything here):
  * A fingerprint match is an INDICATOR, never proof. Fingerprints can collide
    and legitimate software can share a TLS profile with tooling, so an IOC hit
    is always SUSPECTED — the finding says "this endpoint's TLS fingerprint
    matches known-suspicious tooling: investigate", not "this host is C2".
  * Match is EXACT against the registry — never a prefix/substring, which would
    manufacture attributions.
  * The registry is deliberately small and every entry is sourced. Operators
    extend it with a signed external feed (VEDHA_INTEL_DIR / packaged snapshot
    `tls_fingerprint_intel.json`) — no code change, same path discipline as the
    KEV/EPSS snapshots.
"""
from __future__ import annotations

import json
from typing import Any, Optional

try:
    from intel_paths import resolve as _resolve_intel
except Exception:  # noqa: BLE001 — module usable even if intel_paths is absent
    _resolve_intel = None

# ── curated seed registry (small, cited, extensible) ──────────────────────────
# fingerprint -> short threat-intel label. Sources are PUBLIC fingerprint research
# (the Salesforce JARM project and FoxIO JA4+ suite and the open threat-intel that
# tracks default C2 TLS profiles). These are DEFENSIVE detection signatures — the
# TLS equivalent of a Sigma/Suricata rule — used to flag suspicious infrastructure
# on the operator's own network. Kept intentionally minimal; the value is the
# match mechanism + the external-feed loader, not a bundled blocklist.
SUSPICIOUS_JARM: dict[str, str] = {
    # Cobalt Strike default HTTPS team-server profile — one of the most widely
    # documented C2 JARM signatures in open threat intel.
    "07d14d16d21d21d07c42d41d00041d24a458a375eef0c576d23a7bab9a9fb1":
        "Cobalt Strike default team-server (default TLS profile)",
}
SUSPICIOUS_JA4S: dict[str, str] = {
    # Seeded empty by default — populate from a signed feed. Format documented in
    # ja4s.py (e.g. t130200_1301_234ea6891581).
}
SUSPICIOUS_JA4X: dict[str, str] = {
    # Seeded empty by default — populate from a signed feed. Format documented in
    # ja4x.py.
}

# External feed filename (optional). A signed JSON of {"jarm": {...}, "ja4s":
# {...}, "ja4x": {...}} installed into VEDHA_INTEL_DIR (or packaged snapshots/)
# merges over the seeds, so ops extend coverage without a code change.
_FEED_NAME = "tls_fingerprint_intel.json"

RULE_ID = "POSTURE-TLS-SUSPICIOUS-FINGERPRINT"


def _normalize(fp: Any) -> Optional[str]:
    """Fingerprints are compared case-insensitively with surrounding whitespace
    stripped; an all-zero JARM ('no TLS / all probes silent') is not a match."""
    if not isinstance(fp, str):
        return None
    s = fp.strip().lower()
    if not s or set(s) <= {"0"}:
        return None
    return s


def load_registry() -> dict[str, dict[str, str]]:
    """Return {'jarm':{fp:label}, 'ja4s':{...}, 'ja4x':{...}}, the curated seeds
    merged with an optional signed external feed. Best-effort and fail-open: a
    missing/corrupt feed yields just the seeds, never an exception into detection.
    Keys are normalized (lower-cased) so lookups are case-insensitive."""
    reg = {
        "jarm": {(_normalize(k) or k): v for k, v in SUSPICIOUS_JARM.items()},
        "ja4s": {(_normalize(k) or k): v for k, v in SUSPICIOUS_JA4S.items()},
        "ja4x": {(_normalize(k) or k): v for k, v in SUSPICIOUS_JA4X.items()},
    }
    if _resolve_intel is None:
        return reg
    try:
        path = _resolve_intel(_FEED_NAME)
        if not path.is_file():
            return reg
        feed = json.loads(path.read_text(encoding="utf-8"))
        for kind in ("jarm", "ja4s", "ja4x"):
            entries = feed.get(kind)
            if isinstance(entries, dict):
                for fp, label in entries.items():
                    norm = _normalize(fp)
                    if norm and isinstance(label, str) and label.strip():
                        reg[kind][norm] = label.strip()
    except Exception:  # noqa: BLE001 — a bad feed must never break detection
        pass
    return reg


def match_fact_data(data: dict, registry: dict[str, dict[str, str]] | None = None
                    ) -> list[dict]:
    """Return the IOC matches found in ONE tls_scan / tls_fingerprint fact's data.

    Reads the three fingerprint fields where the probe puts them:
      * data['tls_fingerprint']        -> JARM
      * data['ja4s']                   -> JA4S
      * data['certificate']['ja4x']    -> JA4X
    Each match is {kind, fingerprint, label}. Empty list when nothing matches."""
    registry = registry if registry is not None else load_registry()
    if not isinstance(data, dict):
        return []
    out: list[dict] = []

    def _check(kind: str, raw: Any) -> None:
        norm = _normalize(raw)
        if norm is None:
            return
        label = registry.get(kind, {}).get(norm)
        if label:
            out.append({"kind": kind.upper(), "fingerprint": raw.strip(), "label": label})

    _check("jarm", data.get("tls_fingerprint"))
    _check("ja4s", data.get("ja4s"))
    cert = data.get("certificate")
    if isinstance(cert, dict):
        _check("ja4x", cert.get("ja4x"))
    return out


# ── posture sub-layer ─────────────────────────────────────────────────────────
def detect_fingerprint_intel_traced(asset, exposure: dict[str, dict] | None = None):
    """Match every tls_scan / tls_fingerprint fact on this asset against the IOC
    registry. Returns (findings, traces). Findings are always SUSPECTED — a
    fingerprint match is a strong INDICATOR to investigate, not host-confirmed
    compromise (fingerprints collide; legitimate software can share a profile).

    Lazy imports of the posture primitives avoid an import cycle (posture_rules
    imports this module's sub-layer only at call time)."""
    from datetime import datetime, timezone
    from posture_rules import (OUTCOME_MATCH, OUTCOME_NO_MATCH, PostureFinding,
                               TraceRow, compute_risk, make_posture_id)

    exposure = exposure or {}
    exp = exposure.get(asset.ip, {})
    internet_facing = exp.get("internet_facing")
    auth_enforced = exp.get("auth_enforced")
    registry = load_registry()
    now = datetime.now(timezone.utc).isoformat()

    out: list = []
    traces: list = []
    seen: set[tuple] = set()
    had_tls_fact = False

    for f in asset.facts:
        if f.scanner not in ("tls_scan", "tls_fingerprint"):
            continue
        data = f.data if isinstance(f.data, dict) else {}
        had_tls_fact = True
        matches = match_fact_data(data, registry)
        if not matches:
            continue
        for m in matches:
            key = (m["kind"], m["fingerprint"], f.port)
            if key in seen:
                continue
            seen.add(key)
            # IOC match is strong but not host-confirmed -> SUSPECTED, deliberately
            # NOT _state_for (tls_scan is validated, but the INFERENCE 'this is
            # tooling' is not authoritative — mirrors correlate.py's composite).
            state = "suspected"
            severity = "high"
            risk, priority = compute_risk(severity, state, internet_facing, auth_enforced)
            ref = (f"{f.source_file}:{f.source_line}" if f.source_file
                   else f"{f.scanner}:{f.target}:{f.port}")
            out.append(PostureFinding(
                finding_id=make_posture_id(asset.ip, f"{RULE_ID}:{m['kind']}", f.port),
                asset_ip=asset.ip, rule_id=RULE_ID,
                title=f"TLS fingerprint matches known-suspicious tooling ({m['kind']})",
                category="threat_intel", severity=severity, state=state,
                confidence=65, cwe="CWE-506", mitre="T1071.001", port=f.port,
                proto=f.proto or "tcp", evidence_refs=[ref], evidence=m,
                remediation=(
                    "Investigate the host: its TLS fingerprint matches a profile "
                    f"associated with {m['label']}. Confirm the owning process and "
                    "whether the endpoint is sanctioned; fingerprints can collide, "
                    "so treat this as a lead for triage, not proof. If unexplained, "
                    "treat as a potential C2 / malicious-infrastructure indicator "
                    "and begin incident response."),
                fp_notes=(
                    "Exact match against a curated IOC registry (extensible via the "
                    "signed VEDHA_INTEL_DIR feed). SUSPECTED by design — a shared or "
                    "reused fingerprint can occur on legitimate software."),
                internet_facing=internet_facing, auth_enforced=auth_enforced,
                risk_score=risk, priority=priority, created_at=now, scanner=f.scanner))
            traces.append(TraceRow(RULE_ID, f.scanner, OUTCOME_MATCH, asset.ip,
                                   port=f.port, evidence=m))
    if had_tls_fact and not out:
        # TLS fingerprints were present and checked clean against the registry.
        traces.append(TraceRow(RULE_ID, "tls_scan", OUTCOME_NO_MATCH, asset.ip))
    return out, traces
