"""
exposure.py — reachability-aware risk from the probe's exposure_matrix use-case.

Exposure is path-dependent: TCP/3389 can be OPEN from the internet, FILTERED from
the guest network, and unreachable internally — and all three are true. The probe
never collapses those vantages (probe/scanner/vantage_matrix.py); it rides the
verdict back as `result["exposure"] = [{ip, ports: {"tcp/443": {exposure}}, …}]`.

Two pure operations the manager needs:
  * service_exposure(result)      — flatten to (ip, proto, port) → verdict, to
                                    stamp onto Service rows during promotion.
  * escalate_for_exposure(sev, e) — a finding on an INTERNET-reachable service is
                                    materially higher risk than the same issue on
                                    an internal-only one; bump it one level.

Pure logic — no DB — so both are unit-testable in isolation.
"""
from __future__ import annotations

from app.models.enums import FindingSeverity

EXTERNAL = "external"
INTERNAL_ONLY = "internal_only"
AMBIGUOUS = "ambiguous"
NOT_EXPOSED = "not_exposed"

# Severity ladder, low → high. Escalation moves one rung up, capped at critical.
_LADDER = [
    FindingSeverity.info,
    FindingSeverity.low,
    FindingSeverity.medium,
    FindingSeverity.high,
    FindingSeverity.critical,
]


def service_exposure(result: dict | None) -> dict[tuple[str, str, int], str]:
    """(ip, proto, port) → exposure verdict, from a probe exposure_matrix result.

    Keys mirror the Service natural key so promotion is a direct lookup. Malformed
    entries are skipped; a non-exposure result yields an empty map (a no-op).
    """
    out: dict[tuple[str, str, int], str] = {}
    for host in (result or {}).get("exposure") or []:
        if not isinstance(host, dict):
            continue
        ip = host.get("ip")
        ports = host.get("ports")
        if not ip or not isinstance(ports, dict):
            continue
        for key, info in ports.items():
            # key looks like "tcp/443"; info is {"exposure": "...", ...}
            if not isinstance(info, dict) or "/" not in str(key):
                continue
            proto, _, port_s = str(key).partition("/")
            try:
                port = int(port_s)
            except ValueError:
                continue
            verdict = info.get("exposure")
            if verdict:
                out[(ip, proto.lower(), port)] = verdict
    return out


def escalate_for_exposure(
    severity: FindingSeverity, exposure: str | None,
) -> FindingSeverity:
    """Bump a finding one severity rung when its service is internet-reachable.

    Only EXTERNAL escalates — internal_only / ambiguous / not_exposed / unknown
    leave the severity as-is (we never inflate risk without a confirmed external
    open). Already-critical stays critical.
    """
    if exposure != EXTERNAL:
        return severity
    try:
        idx = _LADDER.index(severity)
    except ValueError:
        return severity
    return _LADDER[min(idx + 1, len(_LADDER) - 1)]
