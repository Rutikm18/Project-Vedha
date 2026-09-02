"""
ipv6_discovery.py — link-local IPv6 host discovery via Neighbor Discovery (RFC 4861).

An IPv6 /64 has 2**64 addresses, so brute-force sweeping is not viable — and it's
not needed. RFC 4861 defines ff02::1, the link-local ALL-NODES multicast address:
every live IPv6 host on the segment is already subscribed. One ICMPv6 echo to
ff02::1 makes them all reply, which populates the kernel's Neighbor Cache; reading
that cache (Linux `ip -6 neigh`, macOS/BSD `ndp -an`) yields the live IPv6 addresses
without enumerating anything. Those addresses then feed the EXISTING dual-stack
connect scanner (resolve()/port_scanner already handle AF_INET6) — this module only
supplies the targets that were previously never discovered.

Read-only and unprivileged: one multicast ping + a neighbor-cache read. No sweep,
never a /64 enumeration (a guardrail, not just an optimization).
"""
from __future__ import annotations

import ipaddress
import socket
import subprocess
import sys

ALL_NODES = "ff02::1"                       # RFC 4861 link-local all-nodes multicast

# Neighbor states worth scanning: the entry corresponds to a host that answered or
# recently did. INCOMPLETE/FAILED/NOSTATE mean no working L2 mapping — skip them.
_USABLE_STATES = {"REACHABLE", "STALE", "DELAY", "PROBE", "PERMANENT", "NOARP"}

# macOS/BSD `ndp` single-letter state column → the Linux-style name.
_NDP_STATE = {"R": "REACHABLE", "S": "STALE", "D": "DELAY", "P": "PROBE",
              "I": "INCOMPLETE", "N": "NOSTATE"}


def _is_ipv6(addr: str) -> bool:
    try:
        ipaddress.IPv6Address(addr.split("%", 1)[0])
        return True
    except ValueError:
        return False


def parse_ip_neigh6(text: str) -> list[tuple[str, str | None]]:
    """Parse Linux `ip -6 neigh show` into [(address, state)]. Lines look like:
        fe80::1 dev eth0 lladdr aa:bb:.. router REACHABLE
        2001:db8::5 dev eth0 lladdr .. STALE
        fe80::9 dev eth0  FAILED
    """
    out: list[tuple[str, str | None]] = []
    for line in text.splitlines():
        parts = line.split()
        if not parts or not _is_ipv6(parts[0]):
            continue
        state = next((p for p in parts[1:]
                      if p in _USABLE_STATES or p in ("FAILED", "INCOMPLETE")), None)
        out.append((parts[0], state))
    return out


def parse_ndp(text: str) -> list[tuple[str, str | None]]:
    """Parse macOS/BSD `ndp -an` into [(address, state)]. Columns:
        Neighbor  Linklayer-Address  Netif  Expire  St  Flags
        fe80::1%en0  aa:bb:cc:dd:ee:ff  en0  permanent  R
    """
    out: list[tuple[str, str | None]] = []
    for line in text.splitlines():
        if line.startswith("Neighbor") or not line.strip():
            continue
        parts = line.split()
        if not parts or not _is_ipv6(parts[0]):
            continue
        state = None
        for p in parts[1:]:
            if p in _NDP_STATE:                # single-letter state column
                state = _NDP_STATE[p]
                break
        out.append((parts[0], state))
    return out


def _own_ipv6_addresses() -> set[str]:
    """Best-effort set of this host's own IPv6 addresses, to exclude from results
    (the neighbor cache lists neighbors, but be defensive)."""
    own: set[str] = set()
    try:
        for _f, _t, _p, _c, sockaddr in socket.getaddrinfo(
                socket.gethostname(), None, socket.AF_INET6):
            own.add(sockaddr[0].split("%", 1)[0])
    except OSError:
        pass
    own.add("::1")
    return own


def _run(cmd: list[str], timeout: float) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def _ping_all_nodes(iface: str | None, pings: int, timeout: float) -> None:
    """Fire an ICMPv6 echo at ff02::1 (scoped to `iface`) to make live hosts reply,
    populating the neighbor cache. Best-effort — failures are non-fatal."""
    target = f"{ALL_NODES}%{iface}" if iface else ALL_NODES
    if sys.platform == "darwin":
        _run(["ping6", "-c", str(pings), target], timeout)
    else:  # linux / other
        _run(["ping", "-6", "-c", str(pings), target], timeout)


def _read_neighbor_cache() -> list[tuple[str, str | None]]:
    if sys.platform == "darwin":
        return parse_ndp(_run(["ndp", "-an"], 5.0))
    return parse_ip_neigh6(_run(["ip", "-6", "neigh", "show"], 5.0))


def discover_ipv6_hosts(iface: str | None = None, *, pings: int = 3,
                        timeout: float = 3.0,
                        include_link_local: bool = True) -> list[str]:
    """Discover live IPv6 neighbors on the segment via ND multicast + neighbor
    cache. Returns scannable address strings (link-local carry the %iface scope so
    the connect scanner can reach them). Excludes own addresses and dead states.
    Best-effort: returns [] on any platform/permission problem, never raises.

    `iface` scopes BOTH halves of the operation. It always scoped the multicast
    ping; it now also filters the harvest, because the neighbor cache is
    system-wide. Without that filter a scan of the wired LAN also returned every
    neighbor on every VPN tunnel (utun*) and Apple's peer-to-peer AWDL link —
    hosts on entirely different segments that the engagement never authorized.
    Addresses with no %scope (globals) are kept: they are not interface-bound.
    """
    _ping_all_nodes(iface, pings, timeout)
    own = _own_ipv6_addresses()
    seen: set[str] = set()
    hosts: list[str] = []
    for addr, state in _read_neighbor_cache():
        bare, _, zone = addr.partition("%")
        if iface and zone and zone != iface:
            continue                            # a neighbor on a different segment
        if bare in own or bare in seen:
            continue
        if state is not None and state not in _USABLE_STATES:
            continue                            # INCOMPLETE / FAILED / NOSTATE
        is_ll = ipaddress.IPv6Address(bare).is_link_local
        if is_ll and not include_link_local:
            continue
        # Link-local addresses MUST keep their %scope to be routable by connect().
        scoped = addr if is_ll else bare
        seen.add(bare)
        hosts.append(scoped)
    return hosts


def main() -> None:
    import argparse
    import json
    ap = argparse.ArgumentParser(description="IPv6 neighbor discovery (ND multicast)")
    ap.add_argument("-i", "--iface", default=None, help="scanning interface (e.g. en0)")
    ap.add_argument("--pings", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    hosts = discover_ipv6_hosts(args.iface, pings=args.pings)
    if args.json:
        print(json.dumps({"ipv6_hosts": hosts, "count": len(hosts)}))
    else:
        for h in hosts:
            print(h)


if __name__ == "__main__":
    main()
