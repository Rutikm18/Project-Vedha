"""
use_cases.py — the finite, pre-defined library of scan scenarios the manager
can assign to a probe.

Rule: the probe can ONLY execute use-cases from this list. The manager sends a
use_case_id; the probe resolves it here to a scan_type + profile + intensity. Any
job whose use_case_id is not in this table is rejected before any packet leaves
the host.

`intensity` (workflow/intensity.py) is the optional third knob: how hard each
stage probes (port breadth + rate/concurrency/timeout/retries). It defaults to
"standard" — a no-op baseline — so a use-case that omits it behaves exactly as it
did before intensity existed.

This keeps the field-deployed component's action space finite and auditable.
"""
from __future__ import annotations

USE_CASES: dict[str, dict] = {
    "uc_discovery_only": {
        "display_name": "Network Discovery",
        "description": "Fast host-discovery + port scan only. Use for 'what's alive here?' triage.",
        "scan_type": "discovery",
        "profile": "it",
        "expected_runtime_hint": "2–5 min per /24",
    },
    "uc_full_assessment": {
        "display_name": "Full Assessment",
        "description": "Complete assessment: discovery → ports → banners → all service branches.",
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    "uc_external_web_triage": {
        "display_name": "External Web Triage",
        "description": "Web + TLS surface only. Fast check for exposed web services and cert facts.",
        "scan_type": "web_tls_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_db_exposure": {
        "display_name": "Database Exposure Check",
        "description": "Protocol-handshake fingerprint of database ports. Are any DBs exposed or unauthenticated?",
        "scan_type": "db_fingerprint",
        "profile": "it",
        "expected_runtime_hint": "3–10 min",
    },
    "uc_windows_estate": {
        "display_name": "Windows Estate",
        "description": "SMB dialect + signing detection. Is SMBv1 enabled? Is SMB signing required?",
        "scan_type": "smb_enum",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_ot_passive": {
        "display_name": "OT / ICS Passive Discovery",
        "description": "PASSIVE ONLY — zero active packets. Safe for OT/ICS/SCADA segments.",
        "scan_type": "passive_discovery",
        "profile": "ot",
        "expected_runtime_hint": "listen-only, duration set by operator",
    },
    "uc_ai_endpoint_sweep": {
        "display_name": "AI / MCP Endpoint Sweep",
        "description": "Discover exposed AI inference endpoints and MCP servers.",
        "scan_type": "mcp_discovery",
        "profile": "it",
        "expected_runtime_hint": "3–8 min",
    },
    "uc_rescan_delta": {
        "display_name": "Re-scan (delta from prior engagement)",
        "description": "Full re-assessment identical to uc_full_assessment. Manager diffs against prior run.",
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    # ── Real-world customer use-cases ──────────────────────────────────────────
    "uc_iot_device_survey": {
        "display_name": "IoT / Embedded Device Survey",
        "description": (
            "Inventory IoT and embedded devices on the IoT port set: "
            "MQTT (1883/8883), RTSP (554), CoAP (5683), Telnet (23), printer/DVR ports. "
            "Discovery + service banner."
        ),
        "scan_type": "service_fingerprint",
        "profile": "iot",
        "expected_runtime_hint": "3–10 min per /24",
    },
    "uc_web_app_triage": {
        "display_name": "Web Application Triage",
        "description": (
            "Web-layer fingerprint: HTTP methods (OPTIONS), response headers, "
            "server tech stack, and security-header posture on all web ports "
            "(80, 443, 8080, 8443, 8000…). Use before a dedicated web app pentest."
        ),
        "scan_type": "web_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_udp_service_exposure": {
        "display_name": "UDP Service Exposure",
        "description": (
            "UDP attack surface + amplification checks: NTP monlist (123), "
            "DNS open recursion (53), Memcached (11211), SNMP public (161), "
            "NetBIOS-NS (137)."
        ),
        "scan_type": "udp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    "uc_snmp_exposure": {
        "display_name": "SNMP Exposure Check",
        "description": (
            "Read-only SNMP sysDescr checks using common community strings. "
            "Use to find default or weak read communities on routers, printers, "
            "switches, and monitoring appliances."
        ),
        "scan_type": "snmp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    # ── Capabilities unlocked by the main_scripts scanners ─────────────────────
    "uc_device_inventory": {
        "display_name": "Device Inventory",
        "description": (
            "Fingerprint every live host and infer its ROLE — workstation, "
            "server, network device, printer, hypervisor, or IoT — by fusing OS "
            "family, open ports, and service banners. Discovery → ports → banner "
            "→ evidence-based device classification (never a hostname guess)."
        ),
        "scan_type": "device_inventory",
        "profile": "it",
        "intensity": "standard",
        "expected_runtime_hint": "5–15 min per /24",
    },
    "uc_full_port_audit": {
        "display_name": "Full-Port Audit",
        "description": (
            "Exhaustive TCP audit across the entire 1–65535 space with a bounded "
            "worker pool, then a per-host completeness + self-health record so a "
            "clean empty result is distinguishable from a degraded one. Finds "
            "services hiding on non-standard high ports."
        ),
        "scan_type": "full_port_audit",
        "profile": "it",
        "intensity": "deep",
        "expected_runtime_hint": "20–90 min per host",
    },
    "uc_exposure_matrix": {
        "display_name": "Multi-Vantage Exposure",
        "description": (
            "Vantage-labeled port scan for reachability reconciliation: records "
            "which ports are OPEN from THIS probe's vantage without collapsing "
            "path-dependent state. The manager fuses ≥2 probes to separate "
            "internet-exposed ports from internal-only ones."
        ),
        "scan_type": "exposure_matrix",
        "profile": "it",
        "intensity": "standard",
        "expected_runtime_hint": "5–15 min per /24",
    },
}


# ── Numeric protocol ──────────────────────────────────────────────────────────
# The Manager dispatches a use-case by a stable NUMBER, not a string, so the wire
# stays compact and the operator picks "80" for a full-port audit. Codes are
# banded for room to grow and MUST stay identical on the Manager side (see
# manager/backend/app/routers/agents.py::_USE_CASE_CODES; a parity test enforces
# it). Never renumber an existing code — only append.
#   1–9   discovery/inventory   10–19 assessment      20–29 web/tls
#   30–39 windows/smb           40–49 database        50–59 network services
#   60–69 iot/ai                70–79 ot              80–99 deep/specialized
USE_CASE_CODES: dict[int, str] = {
    1:  "uc_discovery_only",
    2:  "uc_device_inventory",
    10: "uc_full_assessment",
    11: "uc_rescan_delta",
    20: "uc_external_web_triage",
    21: "uc_web_app_triage",
    30: "uc_windows_estate",
    40: "uc_db_exposure",
    50: "uc_snmp_exposure",
    51: "uc_udp_service_exposure",
    60: "uc_iot_device_survey",
    61: "uc_ai_endpoint_sweep",
    70: "uc_ot_passive",
    80: "uc_full_port_audit",
    81: "uc_exposure_matrix",
}

# Intensity as a number: 1 light, 2 standard, 3 deep (workflow/intensity.py).
INTENSITY_CODES: dict[int, str] = {1: "light", 2: "standard", 3: "deep"}


def _as_int(value) -> int | None:
    """Coerce an int-or-numeric-string to int, else None (non-numeric)."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value)
    return None


def use_case_for_code(code) -> str:
    """Map a numeric use-case code → use_case_id (raises on an unknown code)."""
    num = _as_int(code)
    uc_id = USE_CASE_CODES.get(num) if num is not None else None
    if uc_id is None:
        raise ValueError(
            f"Unknown use-case code {code!r}. Allowed: {sorted(USE_CASE_CODES)}"
        )
    return uc_id


def normalize_intensity(value) -> str | None:
    """Accept an intensity as a number (1/2/3) OR a name; return the name.

    None stays None (the use-case default applies). Raises on an unknown code."""
    if value is None:
        return None
    num = _as_int(value)
    if num is not None:
        name = INTENSITY_CODES.get(num)
        if name is None:
            raise ValueError(
                f"Unknown intensity code {value!r}. Allowed: {sorted(INTENSITY_CODES)}"
            )
        return name
    return str(value)   # already a name (light/standard/deep) — validated downstream


def resolve(
    use_case_id: str | None, job_type: str | None, params: dict
) -> tuple[str, str, str]:
    """Return (scan_type, profile, intensity) for a job.

    Resolution order:
    1. use_case_id  → look up in USE_CASES (authoritative)
    2. params["uc"] numeric code → mapped to a use_case_id (the numeric protocol)
    3. scan_type in params  → pass-through (direct dispatch, no use-case)
    4. job_type fallback → "discovery"

    intensity may be a number (1/2/3) or a name and comes from
    params["intensity"] (operator override) else the use-case default else
    "standard". Raises ValueError if a use_case_id/code is given but unknown —
    the caller must reject the job without scanning.
    """
    # A numeric use-case code stands in for use_case_id when the string is absent.
    if not use_case_id and params.get("uc") is not None:
        use_case_id = use_case_for_code(params["uc"])

    param_intensity = normalize_intensity(params.get("intensity"))

    if use_case_id:
        uc = USE_CASES.get(use_case_id)
        if uc is None:
            raise ValueError(
                f"Unknown use_case_id '{use_case_id}'. "
                f"Allowed: {sorted(USE_CASES)}"
            )
        intensity = param_intensity or uc.get("intensity") or "standard"
        return uc["scan_type"], uc["profile"], intensity

    scan_type = params.get("scan_type") or job_type or "discovery"
    profile = params.get("profile", "it")
    intensity = param_intensity or "standard"
    return scan_type, profile, intensity
