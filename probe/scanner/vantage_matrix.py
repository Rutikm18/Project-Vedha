"""
vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.

Exposure is path-dependent: TCP/445 can be OPEN from the corporate LAN, FILTERED
from the guest Wi-Fi, and unreachable from the internet — and all three are true.
port_scanner already stamps every result with its `vantage`; this layer compares
those per-vantage observations WITHOUT collapsing them into one universal state,
and answers the questions that actually matter for risk:

    * Is this port reachable from an EXTERNAL/internet vantage?   (highest risk)
    * Is it internal-only?
    * Is it exposed nowhere we looked?

CORE PRINCIPLE: never average or overwrite vantages. A port is only "external"
if a vantage we treat as external actually saw it OPEN — an internal OPEN never
implies internet exposure, and silence from the internet never disproves it if
another vantage confirms internal reachability.

Pure logic — no network I/O — so it is unit-testable in isolation.
"""

from __future__ import annotations

# Exposure verdicts, ordered by risk.
EXTERNAL = "external"              # OPEN from an external/internet vantage
INTERNAL_ONLY = "internal_only"   # OPEN from >=1 internal vantage, not external
AMBIGUOUS = "ambiguous"           # only open|filtered anywhere (no confirmed open)
NOT_EXPOSED = "not_exposed"       # closed/filtered/unreachable everywhere observed
UNKNOWN = "unknown"

_EXTERNAL_NAME_HINTS = ("internet", "external", "wan", "public", "edge")


def _is_external(name: str, declared: set[str]) -> bool:
    if name in declared:
        return True
    low = name.lower()
    return any(h in low for h in _EXTERNAL_NAME_HINTS)


def _extract(result) -> tuple[str | None, int | None, str | None]:
    """(proto, port, status) from a ScanResult or a plain dict."""
    if isinstance(result, dict):
        return result.get("proto"), result.get("port"), result.get("status")
    return (getattr(result, "proto", None), getattr(result, "port", None),
            getattr(result, "status", None))


def reconcile_vantages(observations: dict[str, list], *,
                       external_vantages: set[str] | None = None) -> dict:
    """Compare per-vantage observations of one target.

    `observations` maps a vantage name -> its list of ScanResults (or dicts).
    A vantage is treated as external if it is in `external_vantages` or its name
    contains an external hint ("internet", "external", "wan", ...).

    Returns a per-port exposure matrix plus roll-ups: the externally-reachable
    ports (the finding that matters most) and the internal-only ports.
    """
    declared = external_vantages or set()

    # (proto, port) -> {vantage: status}. Preserved verbatim — no collapsing.
    matrix: dict[tuple[str, int], dict[str, str]] = {}
    for vname, results in observations.items():
        for r in results:
            proto, port, status = _extract(r)
            if port is None:
                continue
            matrix.setdefault((proto or "tcp", port), {})[vname] = status or "unknown"

    ports_out: dict[str, dict] = {}
    externally_exposed: set[int] = set()
    internal_only: set[int] = set()

    for (proto, port), by_v in sorted(matrix.items()):
        ext_open = any(_is_external(v, declared) and s == "open"
                       for v, s in by_v.items())
        int_open = any(not _is_external(v, declared) and s == "open"
                       for v, s in by_v.items())
        any_ambiguous = any(s == "open|filtered" for s in by_v.values())

        if ext_open:
            exposure = EXTERNAL
            externally_exposed.add(port)
        elif int_open:
            exposure = INTERNAL_ONLY
            internal_only.add(port)
        elif any_ambiguous:
            exposure = AMBIGUOUS
        elif by_v and all(s in ("closed", "filtered", "unreachable", "error")
                          for s in by_v.values()):
            exposure = NOT_EXPOSED
        else:
            exposure = UNKNOWN

        ports_out[f"{proto}/{port}"] = {
            "by_vantage": dict(by_v),
            "exposure": exposure,
            "open_from": sorted(v for v, s in by_v.items() if s == "open"),
        }

    return {
        "ports": ports_out,
        "externally_exposed": sorted(externally_exposed),
        "internal_only": sorted(internal_only),
        "vantages": sorted(observations.keys()),
        "external_vantages": sorted(v for v in observations
                                    if _is_external(v, declared)),
    }
