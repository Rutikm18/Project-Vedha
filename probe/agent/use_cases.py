"""
use_cases.py — the finite, pre-defined library of scan scenarios the manager
can assign to a probe.

Rule: the probe can ONLY execute use-cases from this list. The manager sends a
use_case_id; the probe resolves it here to a scan_type + profile. Any job whose
use_case_id is not in this table is rejected before any packet leaves the host.

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
            "Host and port discovery."
        ),
        "scan_type": "discovery",
        "profile": "iot",
        "expected_runtime_hint": "3–10 min per /24",
    },
    "uc_web_app_triage": {
        "display_name": "Web Application Triage",
        "description": (
            "Web-layer fingerprint: response headers, server tech stack, and "
            "security-header posture on all web ports (80, 443, 8080, 8443, 8000…). "
            "Use before a dedicated web application pentest."
        ),
        "scan_type": "web_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_udp_service_exposure": {
        "display_name": "UDP Service Exposure",
        "description": (
            "Probe UDP services: DNS (53/UDP), SNMP public community (161/UDP), "
            "NTP (123/UDP), NetBIOS Name Service (137/UDP). Confirms which UDP "
            "services answer — surface missed by TCP-only scans."
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
}


def resolve(use_case_id: str | None, job_type: str | None, params: dict) -> tuple[str, str]:
    """Return (scan_type, profile) for a job.

    Resolution order:
    1. use_case_id  → look up in USE_CASES (authoritative)
    2. scan_type in params  → pass-through (direct dispatch, no use-case)
    3. job_type fallback → "discovery"

    Raises ValueError if use_case_id is given but not in the library —
    the caller must reject the job without scanning.
    """
    if use_case_id:
        uc = USE_CASES.get(use_case_id)
        if uc is None:
            raise ValueError(
                f"Unknown use_case_id '{use_case_id}'. "
                f"Allowed: {sorted(USE_CASES)}"
            )
        return uc["scan_type"], uc["profile"]

    scan_type = params.get("scan_type") or job_type or "discovery"
    profile = params.get("profile", "it")
    return scan_type, profile
