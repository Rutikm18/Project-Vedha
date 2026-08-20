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
    # Ordered by the numeric USE_CASE_CODES taxonomy (discovery → assessment →
    # web → windows → db → network-services → iot/ai → ot → deep) so the catalog
    # reads — and the UI renders — in the natural security-workflow sequence.
    # Customer-facing copy: names lead with the asset/outcome; descriptions follow
    # a "what we do → why it matters" shape.

    # ── Discovery / inventory (codes 1–9) ──────────────────────────────────────
    "uc_discovery_only": {
        "display_name": "Network Discovery",
        "description": (
            "Maps every live device and the open ports each exposes — a fast, "
            "no-impact inventory of what is actually on this network."
        ),
        "scan_type": "discovery",
        "profile": "it",
        "expected_runtime_hint": "2–5 min per /24",
    },
    "uc_device_inventory": {
        "display_name": "Device Inventory & Classification",
        "description": (
            "Identifies each live device and infers its role — workstation, "
            "server, network device, printer, hypervisor, or IoT — from OS family, "
            "open ports, and service banners (evidence-based, never a hostname guess)."
        ),
        "scan_type": "device_inventory",
        "profile": "it",
        "intensity": "standard",
        "expected_runtime_hint": "5–15 min per /24",
    },
    # ── Full assessment (codes 10–19) ──────────────────────────────────────────
    "uc_full_assessment": {
        "display_name": "Full Security Assessment",
        "description": (
            "The complete sweep: discovers hosts, maps every service, fingerprints "
            "the OS, and inspects TLS, web, SMB, database, and SNMP exposure — your "
            "baseline security posture in one run."
        ),
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    "uc_rescan_delta": {
        "display_name": "Re-scan & Change Detection",
        "status": "coming_soon",
        "description": (
            "Re-runs a full assessment and highlights what changed since the last "
            "run — new hosts, newly opened ports, and configuration drift."
        ),
        "scan_type": "assessment",
        "profile": "it",
        "expected_runtime_hint": "15–60 min per /24",
    },
    # ── Web / TLS (codes 20–29) ────────────────────────────────────────────────
    "uc_external_web_triage": {
        "display_name": "Web & TLS/SSL Security Check",
        "status": "coming_soon",
        "description": (
            "Scans web servers for exposed HTTP/HTTPS services and grades TLS/SSL "
            "configuration — protocol versions, cipher strength, and certificate health."
        ),
        "scan_type": "web_tls_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    "uc_web_app_triage": {
        "display_name": "Web Application Security Check",
        "status": "coming_soon",
        "description": (
            "Fingerprints web applications — supported HTTP methods, response and "
            "security headers, and server technology — a pre-flight before a full "
            "web-app penetration test."
        ),
        "scan_type": "web_scan",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    # ── Windows / SMB (codes 30–39) ────────────────────────────────────────────
    "uc_windows_estate": {
        "display_name": "Windows & File-Sharing (SMB) Security",
        "description": (
            "Confirms Windows file-sharing is hardened — that the legacy SMBv1 "
            "protocol is disabled and that SMB signing is required to block relay "
            "and tampering attacks."
        ),
        "scan_type": "smb_enum",
        "profile": "it",
        "expected_runtime_hint": "5–15 min",
    },
    # ── Database (codes 40–49) ─────────────────────────────────────────────────
    "uc_db_exposure": {
        "display_name": "Database Exposure Check",
        "status": "coming_soon",
        "description": (
            "Checks whether databases (MySQL, PostgreSQL, SQL Server, Redis, "
            "MongoDB) are reachable on the network and whether they accept "
            "unauthenticated connections."
        ),
        "scan_type": "db_fingerprint",
        "profile": "it",
        "expected_runtime_hint": "3–10 min",
    },
    # ── Network services (codes 50–59) ─────────────────────────────────────────
    "uc_snmp_exposure": {
        "display_name": "SNMP Weak-Credential Check",
        "description": (
            "Tests routers, switches, printers, and appliances for SNMP services "
            "that accept default or weak community strings — a common way attackers "
            "read and alter device configuration."
        ),
        "scan_type": "snmp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    "uc_udp_service_exposure": {
        "display_name": "UDP & Amplification Exposure",
        "description": (
            "Probes UDP services (DNS, NTP, SNMP, memcached, NetBIOS) for open "
            "resolvers and amplification weaknesses that attackers abuse to launch "
            "reflected DDoS attacks."
        ),
        "scan_type": "udp_scan",
        "profile": "it",
        "expected_runtime_hint": "2–8 min",
    },
    # ── IoT / AI (codes 60–69) ─────────────────────────────────────────────────
    "uc_iot_device_survey": {
        "display_name": "IoT & Embedded Device Discovery",
        "description": (
            "Finds IoT and embedded devices — IP cameras (RTSP), MQTT brokers, "
            "printers, DVRs, and Telnet-exposed gear — and captures their service "
            "banners for inventory."
        ),
        "scan_type": "service_fingerprint",
        "profile": "iot",
        "expected_runtime_hint": "3–10 min per /24",
    },
    "uc_ai_endpoint_sweep": {
        "display_name": "AI & MCP Endpoint Discovery",
        "status": "coming_soon",
        "description": (
            "Discovers exposed AI inference endpoints and Model Context Protocol "
            "(MCP) servers — a fast-growing, often-unmonitored attack surface."
        ),
        "scan_type": "mcp_discovery",
        "profile": "it",
        "expected_runtime_hint": "3–8 min",
    },
    # ── OT / ICS (codes 70–79) ─────────────────────────────────────────────────
    "uc_ot_passive": {
        "display_name": "OT / ICS Passive Discovery",
        "status": "coming_soon",
        "description": (
            "Listen-only discovery for operational-technology (OT/ICS/SCADA) "
            "networks — inventories devices with zero active packets, so fragile "
            "industrial equipment is never probed."
        ),
        "scan_type": "passive_discovery",
        "profile": "ot",
        "expected_runtime_hint": "listen-only, duration set by operator",
    },
    # ── Deep / specialized (codes 80–99) ───────────────────────────────────────
    "uc_full_port_audit": {
        "display_name": "Full-Port Audit (all 65,535)",
        "description": (
            "Scans every TCP port on a host to surface services hiding on "
            "non-standard ports, with a completeness + self-health check so a clean "
            "result is genuinely clean, not just an incomplete scan."
        ),
        "scan_type": "full_port_audit",
        "profile": "it",
        "intensity": "deep",
        "expected_runtime_hint": "20–90 min per host",
    },
    "uc_exposure_matrix": {
        "display_name": "Internet-Exposure Mapping",
        "description": (
            "Records which ports are reachable from each probe's vantage point; "
            "with two or more probes, the platform separates truly internet-exposed "
            "services from internal-only ones."
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
