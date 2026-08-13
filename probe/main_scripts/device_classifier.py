"""
device_classifier.py — infer a device's ROLE from collection-layer facts.

This is an INFERENCE layer, not a collector. It consumes the factual output of
the other scanners (os_fingerprint's OS family, port_scanner's open TCP/UDP
ports, service_banner's service/product) and fuses them into a device-type guess:

    workstation | server | network_device | printer | hypervisor | iot | unknown

CORE PRINCIPLES (mirrors os_fingerprint's calibration):
  * Evidence-based: a role is only ever asserted from *observed* ports/OS/services,
    never from a hostname or a single weak hint.
  * Honest confidence: confidence is the winning share of evidence, CAPPED by how
    many INDEPENDENT signals agree. One open port (e.g. 9100) is a hint (<=0.5),
    not a verdict; it can never reach absolute certainty.
  * Transparent: the returned `signals` and `evidence` show exactly what drove the
    guess, and `role_detail` flags high-specificity composites (Domain Controller,
    print server, VMware hypervisor) so nothing is a black box.

No network I/O here — pure logic, so its accuracy is unit-testable in isolation.
"""

from __future__ import annotations

from collections import defaultdict

# Device roles this layer distinguishes.
WORKSTATION = "workstation"
SERVER = "server"
NETWORK_DEVICE = "network_device"      # router / switch / firewall / AP
PRINTER = "printer"
HYPERVISOR = "hypervisor"
IOT = "iot"                            # camera / sensor / embedded media
UNKNOWN = "unknown"

# --------------------------------------------------------------------------- #
# Port -> role signals. Each entry: port -> [(role, weight, evidence_label), ...].
# Weights encode specificity: 9100 (raw print) is far more diagnostic of a printer
# than 80 (http) is of anything, so it scores higher. A port can vote for more
# than one role (445 fits both a workstation and a server); the surrounding ports
# then break the tie. Port number is a *hint*, never a conclusion on its own.
# --------------------------------------------------------------------------- #
_TCP_SIGNALS: dict[int, list[tuple[str, int, str]]] = {
    # Printers — extremely distinctive.
    9100: [(PRINTER, 3, "raw_print_9100")],
    515:  [(PRINTER, 2, "lpd_515")],
    631:  [(PRINTER, 2, "ipp_631")],
    # Hypervisors (VMware ESXi / Workstation control planes).
    902:  [(HYPERVISOR, 3, "vmware_authd_902")],
    903:  [(HYPERVISOR, 2, "vmware_903")],
    5988: [(HYPERVISOR, 1, "cim_http_5988")],
    5989: [(HYPERVISOR, 1, "cim_https_5989")],
    # Windows endpoint surface.
    139:  [(WORKSTATION, 1, "netbios_139")],
    445:  [(WORKSTATION, 1, "smb_445"), (SERVER, 1, "smb_445")],
    3389: [(WORKSTATION, 1, "rdp_3389"), (SERVER, 1, "rdp_3389")],
    # Server roles.
    88:   [(SERVER, 3, "kerberos_88")],        # Domain Controller tell
    389:  [(SERVER, 2, "ldap_389")],
    636:  [(SERVER, 2, "ldaps_636")],
    3268: [(SERVER, 2, "global_catalog_3268")],
    25:   [(SERVER, 2, "smtp_25")],
    1433: [(SERVER, 2, "mssql_1433")],
    3306: [(SERVER, 2, "mysql_3306")],
    5432: [(SERVER, 2, "postgres_5432")],
    53:   [(SERVER, 1, "dns_53"), (NETWORK_DEVICE, 1, "dns_53")],
    80:   [(SERVER, 1, "http_80"), (NETWORK_DEVICE, 1, "http_80")],
    443:  [(SERVER, 1, "https_443")],
    # Network gear.
    23:   [(NETWORK_DEVICE, 2, "telnet_23"), (IOT, 1, "telnet_23")],
    161:  [(NETWORK_DEVICE, 2, "snmp_tcp_161")],
    # IoT / embedded media.
    554:  [(IOT, 3, "rtsp_554")],
    1883: [(IOT, 3, "mqtt_1883")],
    5683: [(IOT, 2, "coap_5683")],
}

# UDP-side signals (open|filtered still counts as a hint — see classify_from_results).
_UDP_SIGNALS: dict[int, list[tuple[str, int, str]]] = {
    161:  [(NETWORK_DEVICE, 2, "snmp_161")],
    5353: [(WORKSTATION, 1, "mdns_5353"), (IOT, 1, "mdns_5353")],
    1900: [(NETWORK_DEVICE, 1, "ssdp_1900"), (IOT, 1, "ssdp_1900")],
    5683: [(IOT, 2, "coap_5683")],
}

# OS family (from os_fingerprint) -> role leanings. Weak on its own by design.
_OS_SIGNALS: dict[str, list[tuple[str, int, str]]] = {
    "Windows":            [(WORKSTATION, 1, "os_windows"), (SERVER, 1, "os_windows")],
    "Linux/Unix/macOS":   [(SERVER, 1, "os_unix"), (WORKSTATION, 1, "os_unix")],
    "Network/Embedded":   [(NETWORK_DEVICE, 2, "os_embedded"), (IOT, 1, "os_embedded")],
}

# Confidence ceiling by number of independent agreeing signals. Never 1.0 —
# role inference from network surface is probabilistic, not proof.
_CEILING = {0: 0.0, 1: 0.5, 2: 0.75, 3: 0.9}


def classify_device(*, os_guess: str | None = None,
                    open_tcp_ports: list[int] | None = None,
                    open_udp_ports: list[int] | None = None,
                    services: list[str] | None = None) -> dict:
    """Fuse OS family + open ports + service products into a device-role guess.

    Returns {device_type, confidence, role_detail, signals, evidence}. `evidence`
    is the sorted list of signal labels backing the winner; `role_detail` names a
    high-specificity composite when detected (e.g. "domain_controller").
    """
    tcp = sorted(set(open_tcp_ports or []))
    udp = sorted(set(open_udp_ports or []))
    services = [s.lower() for s in (services or []) if s]

    scores: dict[str, int] = defaultdict(int)
    support: dict[str, set[str]] = defaultdict(set)

    def _apply(table: dict, key) -> None:
        for role, weight, label in table.get(key, []):
            scores[role] += weight
            support[role].add(label)

    for p in tcp:
        _apply(_TCP_SIGNALS, p)
    for p in udp:
        _apply(_UDP_SIGNALS, p)
    if os_guess:
        _apply(_OS_SIGNALS, os_guess)

    # Service-product hints reinforce role without re-guessing service from port.
    for prod in services:
        if any(w in prod for w in ("iis", "apache", "nginx", "exchange", "mssql")):
            scores[SERVER] += 1
            support[SERVER].add(f"service_{prod[:24]}")
        if "cups" in prod or "jetdirect" in prod or "printer" in prod:
            scores[PRINTER] += 2
            support[PRINTER].add(f"service_{prod[:24]}")
        if "routeros" in prod or "cisco" in prod or "mikrotik" in prod:
            scores[NETWORK_DEVICE] += 2
            support[NETWORK_DEVICE].add(f"service_{prod[:24]}")

    # High-specificity composites — these override the generic winner's *label*
    # (they are strong, structured evidence), while confidence still derives from
    # the signal count so we never overclaim.
    role_detail = None
    tcp_set = set(tcp)
    if {88, 389} <= tcp_set and (445 in tcp_set or 53 in tcp_set):
        role_detail = "domain_controller"          # a server subtype
        scores[SERVER] += 2
        support[SERVER].add("composite_domain_controller")
    elif 9100 in tcp_set and (515 in tcp_set or 631 in tcp_set):
        role_detail = "print_server"
        support[PRINTER].add("composite_print_server")
    elif 902 in tcp_set:
        role_detail = "vmware_hypervisor"
        support[HYPERVISOR].add("composite_vmware")

    total = sum(scores.values())
    if total == 0:
        return {"device_type": UNKNOWN, "confidence": 0.0, "role_detail": None,
                "signals": {"scores": {}, "os_guess": os_guess,
                            "open_tcp": tcp, "open_udp": udp, "support_count": 0},
                "evidence": []}

    best = max(scores, key=lambda r: (scores[r], len(support[r])))
    n_support = len(support[best])
    ceiling = _CEILING.get(n_support, 0.95)
    confidence = round(min(scores[best] / total, ceiling), 2)
    return {
        "device_type": best,
        "confidence": confidence,
        "role_detail": role_detail,
        "signals": {
            "scores": dict(scores),
            "os_guess": os_guess,
            "open_tcp": tcp,
            "open_udp": udp,
            "support_count": n_support,
        },
        "evidence": sorted(support[best]),
    }


def classify_from_results(results) -> dict:
    """Convenience adapter: extract classifier inputs from a list of ScanResult
    objects produced by port_scanner / os_fingerprint / service_banner, then
    classify.

    ONLY confirmed-OPEN ports feed the classifier. UDP 'open|filtered' is silence
    (the udp_scanner probes a fixed service list, so a host that runs none of them
    shows *every* probe port as open|filtered) — treating that as evidence would
    manufacture phantom network-device/iot signals and dilute the real guess. A
    device signal requires a genuine protocol response (status == 'open')."""
    open_tcp: list[int] = []
    open_udp: list[int] = []
    os_guess = None
    services: list[str] = []
    for r in results:
        data = getattr(r, "data", None) or {}
        status = getattr(r, "status", None)
        port = getattr(r, "port", None)
        proto = getattr(r, "proto", None)
        if data.get("os_guess"):
            os_guess = data["os_guess"]
        if port is not None and proto == "tcp" and status == "open":
            open_tcp.append(port)
        if port is not None and proto == "udp" and status == "open":
            open_udp.append(port)          # confirmed response only, not silence
        for key in ("product", "service"):
            if data.get(key):
                services.append(str(data[key]))
    return classify_device(os_guess=os_guess, open_tcp_ports=open_tcp,
                           open_udp_ports=open_udp, services=services)
