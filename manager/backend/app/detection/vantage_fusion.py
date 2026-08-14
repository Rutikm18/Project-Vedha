"""
vantage_fusion.py — fuse the exposure_matrix results of MULTIPLE probes.

A single probe's exposure_matrix answers "is this port open from MY vantage?".
The risk question — "is it reachable from the INTERNET?" — only has an answer once
you compare an external probe with an internal one. The probe never collapses
vantages (probe/scanner/vantage_matrix.py); it ships each vantage's raw
observation. This module is the fleet-level reconciliation the manager does across
probes for the SAME target, without ever averaging or overwriting a vantage:

    * external      — an EXTERNAL-vantage probe saw the port OPEN (highest risk)
    * internal_only — only internal probes saw it open
    * ambiguous     — only open|filtered anywhere (no confirmed open)
    * not_exposed   — closed/filtered/unreachable from every probe that looked

Pure logic — no DB — so the fusion is unit-testable in isolation.
"""
from __future__ import annotations

EXTERNAL = "external"
INTERNAL_ONLY = "internal_only"
AMBIGUOUS = "ambiguous"
NOT_EXPOSED = "not_exposed"
UNKNOWN = "unknown"

_EXTERNAL_HINTS = ("internet", "external", "wan", "public", "edge")
_NON_OPEN = ("closed", "filtered", "unreachable", "error")


def _is_external(vantage: str, declared: set[str]) -> bool:
    if vantage in declared:
        return True
    low = vantage.lower()
    return any(h in low for h in _EXTERNAL_HINTS)


def _collect(results, declared: set[str]):
    """(ip → {(proto,port): {vantage: status}}, ip → set(vantages))."""
    per_ip: dict[str, dict[tuple[str, int], dict[str, str]]] = {}
    per_ip_vantages: dict[str, set[str]] = {}
    for res in results or []:
        for entry in (res or {}).get("exposure") or []:
            if not isinstance(entry, dict):
                continue
            ip = entry.get("ip")
            ports = entry.get("ports")
            if not ip or not isinstance(ports, dict):
                continue
            declared |= set(entry.get("external_vantages") or [])
            portmap = per_ip.setdefault(ip, {})
            for key, info in ports.items():
                by_v = (info or {}).get("by_vantage") if isinstance(info, dict) else None
                if not isinstance(by_v, dict) or "/" not in str(key):
                    continue
                proto, _, port_s = str(key).partition("/")
                try:
                    port = int(port_s)
                except ValueError:
                    continue
                slot = portmap.setdefault((proto.lower(), port), {})
                for vname, status in by_v.items():
                    slot[vname] = status or "unknown"
                    per_ip_vantages.setdefault(ip, set()).add(vname)
    return per_ip, per_ip_vantages


def _verdict(by_v: dict[str, str], declared: set[str]) -> str:
    ext_open = any(_is_external(v, declared) and s == "open" for v, s in by_v.items())
    if ext_open:
        return EXTERNAL
    if any(not _is_external(v, declared) and s == "open" for v, s in by_v.items()):
        return INTERNAL_ONLY
    if any(s == "open|filtered" for s in by_v.values()):
        return AMBIGUOUS
    if by_v and all(s in _NON_OPEN for s in by_v.values()):
        return NOT_EXPOSED
    return UNKNOWN


def fuse_exposure_results(results, *, external_vantages=None) -> dict[str, dict]:
    """Fuse several probes' exposure_matrix results into one per-target matrix.

    `results` is a list of probe result dicts (each carrying `result["exposure"]`).
    A vantage is external if it appears in `external_vantages`, in any result's
    `external_vantages`, or its name contains an external hint. Returns
    ip → {ports, externally_exposed, internal_only, vantages, external_vantages}.
    """
    declared = set(external_vantages or [])
    per_ip, per_ip_vantages = _collect(results, declared)

    out: dict[str, dict] = {}
    for ip, portmap in per_ip.items():
        ports_out: dict[str, dict] = {}
        externally_exposed: set[int] = set()
        internal_only: set[int] = set()
        for (proto, port), by_v in sorted(portmap.items()):
            verdict = _verdict(by_v, declared)
            if verdict == EXTERNAL:
                externally_exposed.add(port)
            elif verdict == INTERNAL_ONLY:
                internal_only.add(port)
            ports_out[f"{proto}/{port}"] = {
                "by_vantage": dict(by_v),
                "exposure": verdict,
                "open_from": sorted(v for v, s in by_v.items() if s == "open"),
            }
        vantages = per_ip_vantages.get(ip, set())
        out[ip] = {
            "ports": ports_out,
            "externally_exposed": sorted(externally_exposed),
            "internal_only": sorted(internal_only),
            "vantages": sorted(vantages),
            "external_vantages": sorted(v for v in vantages if _is_external(v, declared)),
        }
    return out


def fused_service_exposure(results, *, external_vantages=None) -> dict[tuple[str, str, int], str]:
    """(ip, proto, port) → fused exposure verdict, ready to stamp onto Service rows.

    The multi-probe upgrade of app/discovery/exposure.service_exposure(): where
    that took ONE probe's verdict, this fuses ALL probes that scanned the target,
    so an internet-open port is marked `external` even if the ingesting probe is
    internal.
    """
    fused = fuse_exposure_results(results, external_vantages=external_vantages)
    out: dict[tuple[str, str, int], str] = {}
    for ip, host in fused.items():
        for key, info in host["ports"].items():
            proto, _, port_s = key.partition("/")
            out[(ip, proto, int(port_s))] = info["exposure"]
    return out
