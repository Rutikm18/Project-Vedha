"""Pure helpers for controlled Probe capability and accuracy validation."""
from __future__ import annotations

import ipaddress
from typing import Any


VALIDATION_SUITES: dict[str, list[str]] = {
    "baseline": ["uc_discovery_only"],
    "web": [
        "uc_discovery_only",
        "uc_external_web_triage",
        "uc_web_app_triage",
    ],
    "infrastructure": [
        "uc_discovery_only",
        "uc_db_exposure",
        "uc_windows_estate",
    ],
    "inventory": [
        "uc_discovery_only",
        "uc_iot_device_survey",
        "uc_ai_endpoint_sweep",
    ],
    "exposure": [
        "uc_discovery_only",
        "uc_udp_service_exposure",
        "uc_snmp_exposure",
    ],
    "full": [
        "uc_discovery_only",
        "uc_full_assessment",
    ],
    "ot-passive": ["uc_ot_passive"],
}


def resolve_use_cases(
    suites: list[str] | None,
    explicit: list[str] | None,
) -> list[str]:
    """Resolve suites plus explicit use-cases, preserving first-seen order."""
    selected: list[str] = []
    for suite in suites or ["baseline"]:
        if suite not in VALIDATION_SUITES:
            raise ValueError(
                f"unknown validation suite {suite!r}; "
                f"allowed: {sorted(VALIDATION_SUITES)}"
            )
        selected.extend(VALIDATION_SUITES[suite])
    selected.extend(explicit or [])
    return list(dict.fromkeys(selected))


def validate_targets(
    targets: list[str],
    scope_cidrs: list[str],
    excluded_cidrs: list[str] | None = None,
) -> None:
    """Require every IP/CIDR target to be fully allowed and not excluded."""
    if not targets:
        raise ValueError("at least one --target is required")
    try:
        allowed = [ipaddress.ip_network(value, strict=False) for value in scope_cidrs]
        excluded = [
            ipaddress.ip_network(value, strict=False)
            for value in (excluded_cidrs or [])
        ]
    except ValueError as exc:
        raise ValueError(f"manager returned an invalid engagement scope: {exc}") from exc
    if not allowed:
        raise ValueError("engagement has no authorized scope")

    for value in targets:
        try:
            target = ipaddress.ip_network(value, strict=False)
        except ValueError as exc:
            raise ValueError(
                f"validation target {value!r} must be an IP address or CIDR"
            ) from exc
        if not any(
            target.version == network.version and target.subnet_of(network)
            for network in allowed
        ):
            raise ValueError(f"target {value!r} is outside the engagement scope")
        if any(
            target.version == network.version and target.overlaps(network)
            for network in excluded
        ):
            raise ValueError(f"target {value!r} overlaps an engagement exclusion")


def target_address_count(targets: list[str]) -> int:
    """Return the conservative number of addresses represented by targets."""
    total = 0
    for value in targets:
        try:
            total += ipaddress.ip_network(value, strict=False).num_addresses
        except ValueError as exc:
            raise ValueError(
                f"validation target {value!r} must be an IP address or CIDR"
            ) from exc
    return total


def validate_ground_truth(data: Any) -> dict[str, Any]:
    """Validate the small, explicit inventory used for accuracy scoring."""
    if not isinstance(data, dict) or not isinstance(data.get("hosts"), list):
        raise ValueError("ground truth must be an object with a 'hosts' list")
    normalized_hosts = []
    seen_ips: set[str] = set()
    for index, host in enumerate(data["hosts"]):
        if not isinstance(host, dict):
            raise ValueError(f"ground truth hosts[{index}] must be an object")
        try:
            ip = str(ipaddress.ip_address(str(host.get("ip", ""))))
        except ValueError as exc:
            raise ValueError(
                f"ground truth hosts[{index}].ip must be a valid IP address"
            ) from exc
        if ip in seen_ips:
            raise ValueError(f"ground truth contains duplicate host {ip}")
        seen_ips.add(ip)

        ports = []
        ports_scored = "ports" in host
        services_scored = False
        for port_index, item in enumerate(host.get("ports", [])):
            if not isinstance(item, dict):
                raise ValueError(
                    f"ground truth hosts[{index}].ports[{port_index}] "
                    "must be an object"
                )
            try:
                port = int(item["port"])
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(
                    f"ground truth hosts[{index}].ports[{port_index}].port "
                    "must be an integer"
                ) from exc
            if not 1 <= port <= 65535:
                raise ValueError(f"ground truth port {port} is outside 1-65535")
            protocol = str(item.get("protocol", "tcp")).lower()
            if protocol not in {"tcp", "udp"}:
                raise ValueError(
                    f"ground truth port {port} protocol must be tcp or udp"
                )
            services_scored = services_scored or "service" in item
            service = item.get("service")
            ports.append({
                "port": port,
                "protocol": protocol,
                "service": str(service).lower() if service else None,
            })

        cves_scored = "cves" in host
        cves = []
        for cve in host.get("cves", []):
            normalized = str(cve).strip().upper()
            if normalized:
                cves.append(normalized)
        normalized_hosts.append({
            "ip": ip,
            "ports": ports,
            "ports_scored": ports_scored,
            "services_scored": services_scored,
            "cves": cves,
            "cves_scored": cves_scored,
        })
    return {"hosts": normalized_hosts}


def _metric(expected: set[Any], observed: set[Any]) -> dict[str, Any]:
    true_positive = len(expected & observed)
    false_positive = len(observed - expected)
    false_negative = len(expected - observed)
    precision_denominator = true_positive + false_positive
    recall_denominator = true_positive + false_negative
    return {
        "scored": True,
        "expected": len(expected),
        "observed": len(observed),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": (
            true_positive / precision_denominator
            if precision_denominator else None
        ),
        "recall": (
            true_positive / recall_denominator
            if recall_denominator else None
        ),
    }


def _not_scored(reason: str) -> dict[str, Any]:
    return {"scored": False, "reason": reason}


def score_inventory(
    ground_truth: dict[str, Any],
    assets: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Score promoted inventory against explicit host/port/service/CVE truth."""
    truth = validate_ground_truth(ground_truth)
    expected_hosts = {host["ip"] for host in truth["hosts"]}
    observed_hosts = {
        str(asset.get("ip_address"))
        for asset in assets
        if asset.get("ip_address")
    }

    port_hosts = {host["ip"] for host in truth["hosts"] if host["ports_scored"]}
    service_hosts = {
        host["ip"] for host in truth["hosts"] if host["services_scored"]
    }
    cve_hosts = {host["ip"] for host in truth["hosts"] if host["cves_scored"]}
    expected_ports: set[tuple[str, str, int]] = set()
    expected_services: set[tuple[str, str, int, str]] = set()
    expected_cves: set[tuple[str, str]] = set()
    for host in truth["hosts"]:
        for port in host["ports"]:
            key = (host["ip"], port["protocol"], port["port"])
            if host["ports_scored"]:
                expected_ports.add(key)
            if host["services_scored"] and port["service"]:
                expected_services.add((*key, port["service"]))
        if host["cves_scored"]:
            expected_cves.update((host["ip"], cve) for cve in host["cves"])

    observed_ports: set[tuple[str, str, int]] = set()
    observed_services: set[tuple[str, str, int, str]] = set()
    asset_ip_by_id: dict[str, str] = {}
    for asset in assets:
        ip = asset.get("ip_address")
        if not ip:
            continue
        asset_ip_by_id[str(asset.get("id"))] = str(ip)
        for service in asset.get("services") or []:
            try:
                port = int(service["port"])
            except (KeyError, TypeError, ValueError):
                continue
            protocol = str(service.get("protocol") or "tcp").lower()
            key = (str(ip), protocol, port)
            if str(ip) in port_hosts:
                observed_ports.add(key)
            name = service.get("service")
            if name and str(ip) in service_hosts:
                observed_services.add((*key, str(name).lower()))

    observed_cves: set[tuple[str, str]] = set()
    for finding in findings:
        ip = asset_ip_by_id.get(str(finding.get("asset_id")))
        if not ip:
            continue
        if ip in cve_hosts:
            observed_cves.update(
                (ip, str(cve).upper())
                for cve in (finding.get("cve_ids") or [])
                if cve
            )

    return {
        "hosts": _metric(expected_hosts, observed_hosts),
        "ports": (
            _metric(expected_ports, observed_ports)
            if port_hosts else _not_scored("no host includes a 'ports' field")
        ),
        "services": (
            _metric(expected_services, observed_services)
            if service_hosts
            else _not_scored("no port includes a 'service' field")
        ),
        "cves": (
            _metric(expected_cves, observed_cves)
            if cve_hosts else _not_scored("no host includes a 'cves' field")
        ),
        "limitations": [
            "Service names require exact normalized string matches.",
            "CVE recall is meaningful only for vulnerabilities intentionally "
            "seeded and supported by the selected checks.",
            "UDP non-response is not proof that a service is closed.",
        ],
    }
