"""
host_discovery.py — determine which hosts are alive, with graded confidence.

METHOD (collection only, unprivileged): two fused proof-of-life signals, each
carrying its OWN confidence weight instead of collapsing to a single boolean.

1. TCP connect — lightweight connect() to a small set of very common ports.
   ANY response (open OR connection-refused) proves the host exists, because a
   refused connection means a host answered with a RST. This is *endpoint*
   evidence (the target's own stack replied), so it is the strongest thing an
   unprivileged scanner can obtain. First response wins (early-exit).

2. Neighbor / ARP freshness — AFTER the TCP probes (in fact BECAUSE of them: a
   connect() to an on-LAN IP forces the kernel to ARP-resolve it), we read the
   OS neighbor entry FOR THIS TARGET and grade its freshness:

     * Linux `ip neigh` exposes the kernel NUD state:
         REACHABLE / PERMANENT  -> fresh, kernel-confirmed L2 reachability
                                   (a solicited ARP reply set this) — HIGH proof
         DELAY / PROBE          -> kernel is revalidating right now  — MEDIUM
         STALE                  -> had a MAC once, unconfirmed now    — LOW
         FAILED / INCOMPLETE    -> resolution failed                  — NEGATIVE
     * macOS/BSD `arp`/`ndp` give no NUD state, so a resolved entry is graded
       as "cache" (freshness unknown) — deliberately LOW, never HIGH.

   This is the fix for the old flaw `ARP_CACHE_ENTRY == ALIVE`: a mere cache
   entry is NOT equivalent to a fresh active ARP reply, so it must not carry the
   same confidence. On-LAN L2 truth still catches hosts that silently drop all
   TCP (phones, IoT, privacy-hardened hosts): such a host must still ARP to
   function on the LAN, and our probe elicits a fresh REACHABLE entry for it.

Fusion: the strongest positive signal sets the headline state/confidence; a
second independent positive signal nudges confidence up (corroboration). The
per-signal outcome vector is recorded as structured evidence.

STATE MODEL (additive, in `data`): confirmed_alive / probably_alive /
recently_observed / inconclusive / unreachable_from_vantage, each with a 0-1
`confidence`. The legacy boolean `alive` and the `status` ("open"/"filtered")
are PRESERVED for the existing pipeline: for a vulnerability scanner a false
negative (a missed asset) is worse than a false positive, so any positive
signal — including a stale cache entry — keeps `alive=True` (a *candidate* worth
revalidating), while `state`/`confidence` expose exactly how trustworthy that is.

This is a userland (unprivileged) approach — it does not send raw ICMP/ARP.
For raw ICMP/ARP/SYN discovery use nmap_wrapper.py, or the tiered native engine
in docs/superpowers/specs/2026-08-10-native-host-discovery-engine-design.md
(this module implements the unprivileged Tier-D + neighbor-freshness slice).

No exploitation, no payloads — just "is something there, how sure are we, and
roughly what".
"""

from __future__ import annotations

import asyncio
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone

from .scanner_base import (
    BaseScanner, ScanResult, base_argparser, run_cli, setup_logging,
    main_entrypoint, LOG,
)

# Ports chosen because almost every live host answers on at least one of these
# (web, windows, ssh, dns). A RST counts as alive just as much as a SYN/ACK.
# 62078 is iPhone lockdownd — often open, a positive Apple-mobile signal.
PROBE_PORTS = [80, 443, 445, 22, 3389, 53, 135, 139, 62078]

# --------------------------------------------------------------------------- #
# MAC / OUI helpers — small curated vendor table + randomized-MAC detection.
# A full OUI database is huge; the strongest mobile signal is the
# locally-administered bit (MAC randomization), which needs no table at all.
# --------------------------------------------------------------------------- #
OUI_VENDORS = {
    # Apple
    "00:03:93": "Apple", "00:1b:63": "Apple", "00:25:00": "Apple",
    "3c:15:c2": "Apple", "a4:83:e7": "Apple", "f0:18:98": "Apple",
    "ac:bc:32": "Apple", "d0:81:7a": "Apple", "84:38:35": "Apple",
    # Samsung
    "00:12:fb": "Samsung", "34:23:87": "Samsung", "5c:0a:5b": "Samsung",
    "e8:50:8b": "Samsung", "8c:77:12": "Samsung",
    # Google / Pixel / Nest
    "3c:5a:b4": "Google", "f4:f5:d8": "Google", "94:eb:2c": "Google",
    "da:a1:19": "Google",
    # Xiaomi
    "64:09:80": "Xiaomi", "7c:1d:d9": "Xiaomi", "f8:a4:5f": "Xiaomi",
    # Huawei
    "00:e0:fc": "Huawei", "48:46:fb": "Huawei", "80:fb:06": "Huawei",
    # OnePlus / Oppo / Vivo
    "94:65:2d": "OnePlus", "c0:ee:fb": "OnePlus",
    # Intel (laptops/NICs)
    "00:1b:21": "Intel", "3c:97:0e": "Intel", "a4:c3:f0": "Intel",
    # Raspberry Pi
    "b8:27:eb": "Raspberry Pi", "dc:a6:32": "Raspberry Pi", "e4:5f:01": "Raspberry Pi",
    # Amazon (Echo/FireTV)
    "44:65:0d": "Amazon", "fc:65:de": "Amazon",
    # Common router/AP vendors
    "5c:8c:30": "Router/AP", "2c:3a:e8": "Espressif/IoT",
}

# Vendors that, when they own the OUI, strongly imply a handheld mobile device.
MOBILE_VENDORS = {"Apple", "Samsung", "Google", "Xiaomi", "Huawei", "OnePlus"}

_MAC_RE = re.compile(r"([0-9a-fA-F]{1,2}(?::[0-9a-fA-F]{1,2}){5})")
_BAD_MACS = {"ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00"}


def normalize_mac(mac: str) -> str | None:
    """Zero-pad each octet ('d2:58:2b:ff:cb:4' -> 'd2:58:2b:ff:cb:04'); lower."""
    m = _MAC_RE.search(mac or "")
    if not m:
        return None
    parts = m.group(1).split(":")
    if len(parts) != 6:
        return None
    norm = ":".join(p.rjust(2, "0").lower() for p in parts)
    if norm in _BAD_MACS or norm.startswith(("01:00:5e", "33:33", "01:80:c2")):
        return None  # broadcast / IPv4 & IPv6 multicast / STP — not a host
    return norm


def is_locally_administered(mac: str) -> bool:
    """True if the 2nd-least-significant bit of the first octet is set —
    i.e. a locally-administered / randomized MAC. Modern phones randomize
    their MAC per-SSID for privacy, so this is a strong 'mobile' tell."""
    try:
        first = int(mac.split(":", 1)[0], 16)
    except (ValueError, AttributeError):
        return False
    return bool(first & 0b10)


def vendor_for_mac(mac: str) -> str | None:
    if not mac:
        return None
    return OUI_VENDORS.get(mac[:8])  # first 3 octets = OUI prefix


def device_hint(mac: str | None, vendor: str | None, ports_open: set[int]) -> str | None:
    """Best-effort device classification from the L2/L3 evidence."""
    if 62078 in ports_open:
        return "apple-mobile (iphone/ipad — lockdownd)"
    if mac and is_locally_administered(mac):
        return "mobile/privacy device (randomized MAC)"
    if vendor in MOBILE_VENDORS:
        return f"mobile ({vendor})"
    if vendor:
        return vendor
    return None


# --------------------------------------------------------------------------- #
# Neighbor freshness model. The core correction: a resolved MAC is NOT proof of
# current liveness on its own — its FRESHNESS decides how much it is worth.
# --------------------------------------------------------------------------- #
FRESH_REACHABLE = "reachable"   # kernel-confirmed L2 reachability (fresh)
FRESH_PROBING = "probing"       # kernel revalidating now (DELAY/PROBE)
FRESH_STALE = "stale"           # had a MAC, unconfirmed now
FRESH_CACHE = "cache"           # resolved, freshness unknown (macOS/BSD arp)
FRESH_FAILED = "failed"         # resolution failed (INCOMPLETE/FAILED) — negative

# Linux `ip neigh` NUD state -> our freshness bucket.
_NUD_MAP = {
    "REACHABLE": FRESH_REACHABLE, "PERMANENT": FRESH_REACHABLE,
    "NOARP": FRESH_REACHABLE,
    "DELAY": FRESH_PROBING, "PROBE": FRESH_PROBING,
    "STALE": FRESH_STALE,
    "FAILED": FRESH_FAILED, "INCOMPLETE": FRESH_FAILED,
}

# Confidence weight of a single signal (0-1). Endpoint (TCP) evidence outranks
# L2 evidence because it proves the target's own stack answered; fresh L2 proof
# is close behind; a stale/unknown-freshness cache entry is deliberately weak.
_SIG_CONF = {
    "tcp_open":       0.97,   # SYN/ACK — port open, host definitely up
    "tcp_refused":    0.93,   # RST — host up, port closed (could be a middlebox)
    FRESH_REACHABLE:  0.95,   # fresh solicited ARP/NDP reply, on-LAN ground truth
    FRESH_PROBING:    0.75,   # entry mid-revalidation
    FRESH_STALE:      0.50,   # cache only, may be minutes old
    FRESH_CACHE:      0.55,   # resolved but freshness unknown (macOS)
}

# Confidence thresholds -> state.
STATE_CONFIRMED = "confirmed_alive"
STATE_PROBABLE = "probably_alive"
STATE_RECENT = "recently_observed"
STATE_INCONCLUSIVE = "inconclusive"
STATE_UNREACHABLE = "unreachable_from_vantage"


@dataclass
class Neighbor:
    """One OS neighbor-cache observation about a target, with graded freshness."""
    mac: str | None
    fresh: str            # one of the FRESH_* buckets
    raw_state: str        # the underlying NUD token or 'arp' for BSD


def parse_neighbor_line(line: str, want_ip: str | None = None) -> Neighbor | None:
    """Parse one `ip neigh` / `arp -n` / `ndp -n` line into a Neighbor.

    Handles both the Linux form ('<ip> dev <if> lladdr <mac> REACHABLE') and the
    BSD/macOS form ('? (<ip>) at <mac> on en0 ...' or '... (incomplete) ...').
    `want_ip`, if given, filters to the target IP so a multi-line dump can't
    cross-contaminate. Returns None for irrelevant / unparseable lines.
    """
    if want_ip and want_ip not in line:
        return None
    up = line.upper()

    # Negative first: an unresolved entry is a NEGATIVE liveness signal on-LAN.
    if "INCOMPLETE" in up or "FAILED" in up or "(INCOMPLETE)" in up:
        return Neighbor(mac=None, fresh=FRESH_FAILED,
                        raw_state="INCOMPLETE" if "INCOMPLETE" in up else "FAILED")

    mac = normalize_mac(line)
    if not mac:
        return None

    # Linux NUD token, if present (last-ish bareword in caps).
    for token, bucket in _NUD_MAP.items():
        if re.search(rf"\b{token}\b", up):
            return Neighbor(mac=mac, fresh=bucket, raw_state=token)

    # BSD/macOS: resolved but no freshness state available.
    return Neighbor(mac=mac, fresh=FRESH_CACHE, raw_state="arp")


def read_neighbor(ip: str) -> Neighbor | None:
    """Targeted, POST-probe neighbor lookup for a single IP (unprivileged).

    Reads only this IP's entry so the freshness reflects the state our own TCP
    probe just elicited (a solicited ARP reply flips a Linux entry to REACHABLE).
    Tries Linux `ip neigh` first (gives NUD state for v4 AND v6), then the
    BSD/macOS `arp`/`ndp` tools. Never raises — a missing tool or absent entry
    just yields None (graceful downgrade to TCP-only).
    """
    is_v6 = ":" in ip
    # CWE-78/88: keep argv as a list so the target is a single discrete argument —
    # a metacharacter- or space-laden value can never split into extra args or reach
    # a shell, and the neighbour tool treats it strictly as an address, not a flag.
    bsd = ["ndp", "-n", ip] if is_v6 else ["arp", "-n", ip]
    for cmd in (["ip", "neigh", "show", ip], bsd):
        exe = cmd[0]
        if not shutil.which(exe):
            continue
        try:
            out = subprocess.run(
                cmd, capture_output=True, text=True, timeout=3,
            ).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        for line in out.splitlines():
            nb = parse_neighbor_line(line, want_ip=ip)
            if nb is not None:
                return nb
    return None


def read_arp_table() -> dict[str, str]:
    """Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).

    Retained for callers that want a whole-pass view. NOTE: this is a CACHE
    snapshot with NO freshness guarantee — the per-target read_neighbor() is
    preferred for liveness decisions. Never raises.
    """
    table: dict[str, str] = {}
    for cmd in ("ip neigh", "arp -an"):
        exe = cmd.split()[0]
        if not shutil.which(exe):
            continue
        try:
            out = subprocess.run(
                cmd.split(), capture_output=True, text=True, timeout=5,
            ).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        for line in out.splitlines():
            ip_m = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", line)
            if not ip_m:
                continue
            nb = parse_neighbor_line(line, want_ip=ip_m.group(1))
            if nb and nb.mac:
                table[ip_m.group(1)] = nb.mac
        if table:
            break
    return table


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _state_for_confidence(conf: float) -> str:
    if conf >= 0.90:
        return STATE_CONFIRMED
    if conf >= 0.70:
        return STATE_PROBABLE
    if conf >= 0.30:
        return STATE_RECENT
    return STATE_INCONCLUSIVE


def fuse_liveness(
    evidence_ports: list[tuple[int, str]],
    neighbor: Neighbor | None,
) -> dict:
    """Combine TCP + neighbor signals into a confidence-scored verdict.

    Returns a dict with: alive(bool), state(str), confidence(float),
    method(legacy str), reason(str), and signals(list of structured evidence).
    Pure/deterministic given its inputs — easy to unit-test.
    """
    signals: list[dict] = []
    positives: list[float] = []
    ts = _now()

    # --- TCP endpoint evidence (strongest an unprivileged scanner can get) ---
    tcp_alive = False
    for port, state in evidence_ports:
        key = "tcp_open" if state == "open" else "tcp_refused"
        conf = _SIG_CONF[key]
        positives.append(conf)
        tcp_alive = True
        signals.append({
            "method": "tcp_connect", "port": port,
            "result": "syn_ack" if state == "open" else "rst",
            "confidence": conf, "observed_at": ts,
        })

    # --- Neighbor / ARP freshness evidence -----------------------------------
    arp_positive = False
    if neighbor is not None:
        if neighbor.fresh == FRESH_FAILED:
            signals.append({
                "method": "arp_neighbor", "result": "unresolved",
                "nud": neighbor.raw_state, "confidence": 0.04,
                "observed_at": ts,
            })
        elif neighbor.mac:
            conf = _SIG_CONF.get(neighbor.fresh, 0.5)
            positives.append(conf)
            arp_positive = True
            signals.append({
                "method": "arp_neighbor", "result": neighbor.fresh,
                "nud": neighbor.raw_state, "mac": neighbor.mac,
                "confidence": conf, "observed_at": ts,
            })

    # --- Fuse ----------------------------------------------------------------
    if positives:
        headline = max(positives)
        # Corroboration: each ADDITIONAL independent positive nudges up a little,
        # never past 0.99 (we never claim certainty from indirect evidence).
        headline = min(0.99, headline + 0.02 * (len(positives) - 1))
        state = _state_for_confidence(headline)
        reason = signals[0]["result"]  # strongest signal is emitted first (TCP)
        alive = True
    elif neighbor is not None and neighbor.fresh == FRESH_FAILED:
        # We asked the LAN and got a definitive "not resolvable" — the closest an
        # unprivileged on-LAN probe gets to "down". Still not certain (host may
        # be off-LAN / just booted), so keep confidence low.
        headline, state, reason, alive = 0.10, STATE_UNREACHABLE, "arp_unresolved", False
    else:
        # Silence with no neighbor entry: genuinely inconclusive, NOT "dead".
        headline, state, reason, alive = 0.10, STATE_INCONCLUSIVE, "silent", False

    # Legacy `method` string (kept stable for any downstream that branches on it).
    if tcp_alive and arp_positive:
        method = "tcp+arp"
    elif arp_positive:
        method = "arp"
    elif tcp_alive:
        method = "tcp"
    else:
        method = None

    return {
        "alive": alive,
        "state": state,
        "confidence": round(headline, 3),
        "method": method,
        "reason": reason,
        "signals": signals,
    }


class HostDiscoveryScanner(BaseScanner):
    name = "host_discovery"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = list(PROBE_PORTS if ports is None else ports)

    async def _probe(self, target: str, port: int) -> str | None:
        """Return 'open', 'refused', or None (no response)."""
        await self.limiter.wait()
        async with self.sem:
            try:
                fut = asyncio.open_connection(target, port)
                reader, writer = await asyncio.wait_for(fut, timeout=self.timeout)
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
                return "open"
            except ConnectionRefusedError:
                return "refused"        # host is alive, port just closed
            except (asyncio.TimeoutError, OSError):
                return None

    async def scan_target(self, target: str) -> list[ScanResult]:
        # --- TCP probes with early-exit on first proof of life ---------------
        tasks = {asyncio.ensure_future(self._probe(target, p)): p
                 for p in self.ports}
        evidence_ports: list[tuple[int, str]] = []
        pending = set(tasks)
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED)
            for d in done:
                state = d.result()
                if state in ("open", "refused"):
                    evidence_ports.append((tasks[d], state))
            if evidence_ports and pending:
                # Proof of life already; stop probing this host's other ports.
                for p in pending:
                    p.cancel()
                await asyncio.gather(*pending, return_exceptions=True)
                pending = set()
        evidence_ports.sort()
        ports_open = {p for p, s in evidence_ports if s == "open"}

        # --- Neighbor freshness fusion ---------------------------------------
        # Read AFTER the probes so a Linux entry reflects the reachability our
        # connect() just elicited (silent on-LAN hosts still ARP -> REACHABLE).
        # Off the event loop so the subprocess never blocks other targets.
        neighbor = await asyncio.to_thread(read_neighbor, target)
        mac = neighbor.mac if neighbor else None
        vendor = vendor_for_mac(mac) if mac else None

        verdict = fuse_liveness(evidence_ports, neighbor)
        alive = verdict["alive"]
        hint = device_hint(mac, vendor, ports_open) if alive else None

        data: dict = {
            "alive": alive,                       # legacy boolean (kept)
            "state": verdict["state"],            # NEW confidence-scored state
            "confidence": verdict["confidence"],  # NEW 0-1
            "responding_ports": [
                {"port": p, "state": s} for p, s in evidence_ports
            ],
            "method": verdict["method"],          # legacy headline method (kept)
            "reason": verdict["reason"],          # NEW strongest-signal reason
            "vantage": self.name,                 # exposure is path-dependent
            "evidence": verdict["signals"],       # NEW structured per-signal list
        }
        if mac:
            data["mac"] = mac
            data["randomized_mac"] = is_locally_administered(mac)
            data["arp_state"] = neighbor.fresh    # NEW freshness bucket
        if vendor:
            data["vendor"] = vendor
        if hint:
            data["device_hint"] = hint

        # Human-readable proof-of-life line.
        bits: list[str] = []
        if evidence_ports:
            bits.append("tcp " + ", ".join(f"{p}/{s}" for p, s in evidence_ports))
        if mac:
            bits.append(
                f"arp {mac} [{neighbor.fresh}]" + (f" ({vendor})" if vendor else ""))
        if hint:
            bits.append(hint)
        evidence = "; ".join(bits) if alive else (
            "no response on any probe port, no fresh neighbor entry")

        return [ScanResult(
            scanner=self.name,
            target=target,
            # UNCHANGED mapping: alive -> "open", silent -> "filtered". The
            # nuance lives in data.state/confidence; downstream stage gating
            # (agent/engine.py) still keys off "filtered" for re-probe.
            status="open" if alive else "filtered",
            data=data,
            evidence=evidence,
        )]


def main() -> None:
    parser = base_argparser("Host discovery (liveness) scanner")
    args = parser.parse_args()
    setup_logging(args.verbose)
    main_entrypoint(lambda: run_cli(HostDiscoveryScanner, args))


if __name__ == "__main__":
    main()
