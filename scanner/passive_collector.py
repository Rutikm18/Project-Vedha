"""
passive_collector.py — LISTEN-ONLY host discovery for fragile networks (OT/ICS).

WHY THIS EXISTS (deep version):
  Every other scanner in this package is ACTIVE — it opens a TCP connection or
  sends a UDP probe to the target. On an IT or even an IoT network that is fine.
  On an OPERATIONAL TECHNOLOGY network (ICS/SCADA: PLCs, RTUs, HMIs, drives,
  safety controllers) it is NOT. Industrial controllers run real-time stacks
  with tiny resource budgets; an unsolicited connection, a malformed probe, or
  even a burst of well-formed SYNs has — repeatedly, in the real world — hung or
  rebooted a PLC and tripped a physical process. The cardinal rule of OT
  assessment is therefore: on the control network you LISTEN, you do not probe.

WHAT THIS MODULE DOES:
  It transmits NOTHING to any target. It binds broadcast / industrial
  announcement UDP ports in RECEIVE-ONLY mode, then records whatever hosts
  voluntarily announce themselves on the local segment. This UDP backend only
  sees traffic delivered by the host network stack; a SPAN/TAP deployment
  requires a separately approved receive-only packet-capture backend.
  Zero packets leave this tool toward a target.

  Important: the UDP backend does NOT join multicast groups. IP_ADD_MEMBERSHIP
  can emit IGMP membership reports, which violates strict passive operation.
  mDNS, SSDP, and LLMNR are therefore reported as unavailable coverage until a
  receive-only packet-capture backend is configured. The built-in backend only
  binds broadcast announcement ports and never calls send, sendto, or connect.

  Multicast sources intentionally disabled in this backend:
    * mDNS        224.0.0.251:5353
    * SSDP/UPnP   239.255.255.250:1900
    * LLMNR       224.0.0.252:5355

  Broadcast sources it listens to (all recv-only):
    * NetBIOS     broadcast :137     — Windows host announcements
    * BACnet/IP   broadcast :47808   — building-automation controllers (OT)
    * EtherNet/IP broadcast :2222    — Allen-Bradley / industrial I/O (OT)

  Because it only ever reports hosts that are also inside the authorization
  scope, it is safe to leave running on a sensitive segment: out-of-scope
  chatter is observed but dropped, never recorded.

PRIVILEGE: platform-dependent. The NetBIOS listener uses UDP/137 and may require
  bind permission. If a port is already in use or cannot be bound, the failed
  source is reported in coverage; the collector never falls back to anything
  active.
"""

from __future__ import annotations

import argparse
import asyncio
import errno
import socket
import time

from .scanner_base import (
    ScanResult, ScopeGuard, ResultWriter, setup_logging, base_argparser,
    LOG, main_entrypoint,
)

# (multicast_group | None, port, label). Multicast entries are reported as
# unavailable; only group=None broadcast ports are bound by this backend.
PASSIVE_SOURCES: list[tuple[str | None, int, str]] = [
    ("224.0.0.251", 5353, "mdns"),
    ("239.255.255.250", 1900, "ssdp"),
    ("224.0.0.252", 5355, "llmnr"),
    (None, 137, "netbios"),
    (None, 47808, "bacnet"),     # OT: building automation (BACnet/IP)
    (None, 2222, "ethernet-ip"), # OT: EtherNet/IP implicit I/O
]


def _printable_strings(data: bytes, min_len: int = 4, limit: int = 6) -> list[str]:
    """Pull short printable ASCII runs from a payload, for human-readable evidence."""
    out, cur = [], []
    for b in data:
        if 32 <= b < 127:
            cur.append(chr(b))
        else:
            if len(cur) >= min_len:
                out.append("".join(cur))
            cur = []
        if len(out) >= limit:
            break
    if len(cur) >= min_len and len(out) < limit:
        out.append("".join(cur))
    return out


def _device_hint(label: str, data: bytes) -> str | None:
    """Best-effort device label from an announcement payload (recv-only parsing)."""
    text = data.decode("latin-1", "replace")
    if label == "ssdp":
        for line in text.splitlines():
            low = line.lower()
            if low.startswith("server:") or low.startswith("usn:"):
                return line.strip()[:200]
    if label == "mdns":
        names = [s for s in _printable_strings(data, 4, 8) if "." in s or "_" in s]
        if names:
            return ", ".join(names[:3])[:200]
    hints = _printable_strings(data)
    return ", ".join(hints[:3])[:200] if hints else None


class PassiveListenerError(RuntimeError):
    """All passive sources failed before the listen window could start."""

    def __init__(self, error_code: str, coverage: dict):
        self.error_code = error_code
        self.retryable = bool(coverage["retryable"])
        self.remediation = coverage["remediation"]
        self.details = {"coverage": coverage}
        super().__init__(
            f"no passive listeners available ({coverage['failed_count']} failed)"
        )


def _open_listener(group: str | None, port: int) -> socket.socket:
    """Open one recv-only UDP listener or raise the socket error.

    Multicast groups are rejected because joining can emit IGMP. Broadcast
    listeners only bind; SO_REUSEADDR/REUSEPORT let them coexist with services.
    """
    if group is not None:
        raise OSError(
            errno.EOPNOTSUPP,
            "multicast joins disabled for strict passive operation",
        )
    sock: socket.socket | None = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except (AttributeError, OSError):
            pass
        sock.bind(("", port))
        sock.setblocking(False)
        return sock
    except OSError:
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass
        raise


def _listener_error_code(exc: OSError) -> str:
    return (
        "permission_denied"
        if isinstance(exc, PermissionError) or exc.errno in {errno.EACCES, errno.EPERM}
        else "listener_unavailable"
    )


def _coverage(
    active_sources: list[dict],
    failed_sources: list[dict],
) -> dict:
    bind_failures = [
        item
        for item in failed_sources
        if item.get("reason") != "multicast_join_disabled"
    ]
    if bind_failures and all(
        item["error_code"] == "permission_denied"
        for item in bind_failures
    ):
        error_code = "permission_denied"
    else:
        error_code = "listener_unavailable"
    multicast_disabled = any(
        item.get("reason") == "multicast_join_disabled"
        for item in failed_sources
    )
    if error_code == "permission_denied":
        remediation = (
            "Grant the probe service account permission to bind the configured "
            "UDP listeners, then restart the probe."
        )
    elif multicast_disabled and not bind_failures:
        remediation = (
            "Configure an approved receive-only packet-capture backend to cover "
            "multicast announcements; UDP membership remains disabled for OT safety."
        )
    else:
        remediation = (
            "Check for conflicting UDP listeners and bind configuration. Use an "
            "approved receive-only capture backend for multicast coverage."
        )
    return {
        "requested_count": len(PASSIVE_SOURCES),
        "active_count": len(active_sources),
        "failed_count": len(failed_sources),
        "active_sources": active_sources,
        "failed_sources": failed_sources,
        "degraded": bool(failed_sources),
        "error_code": error_code if failed_sources else None,
        "retryable": (
            error_code == "listener_unavailable" and bool(bind_failures)
            if failed_sources
            else False
        ),
        "remediation": remediation if failed_sources else None,
    }


class PassiveCollector:
    """
    Listen-only discovery. No active probing. Reports in-scope hosts that
    announce themselves within the listen window.
    """

    name = "passive_collect"

    def __init__(self, scope: ScopeGuard, *, listen_seconds: float = 60.0):
        self.scope = scope
        self.listen_seconds = listen_seconds

    async def run(self, writer: ResultWriter) -> dict:
        loop = asyncio.get_running_loop()
        socks: dict[int, tuple[socket.socket, str]] = {}
        active_sources: list[dict] = []
        failed_sources: list[dict] = []
        for group, port, label in PASSIVE_SOURCES:
            if group is not None:
                failed_sources.append({
                    "source": label,
                    "group": group,
                    "port": port,
                    "error_code": "listener_unavailable",
                    "reason": "multicast_join_disabled",
                    "message": (
                        "UDP multicast membership is disabled because it can "
                        "transmit IGMP; use an approved receive-only capture backend"
                    ),
                })
                continue
            try:
                sock = _open_listener(group, port)
            except OSError as exc:
                error_code = _listener_error_code(exc)
                failed_sources.append({
                    "source": label,
                    "group": group or "broadcast",
                    "port": port,
                    "error_code": error_code,
                    "message": str(exc)[:200],
                })
                LOG.warning(
                    "passive: could not open %s:%d (%s) — skipping this source",
                    group or "broadcast",
                    port,
                    exc,
                )
                continue
            socks[sock.fileno()] = (sock, label)
            active_sources.append({
                "source": label,
                "group": group or "broadcast",
                "port": port,
            })

        coverage = _coverage(active_sources, failed_sources)
        if not socks:
            LOG.error("passive: no listeners could be opened")
            raise PassiveListenerError(coverage["error_code"], coverage)

        LOG.info("passive: listening (recv-only, sending NOTHING) on %d source(s) "
                 "for %.0fs", len(socks), self.listen_seconds)

        # host -> {"labels": set, "hints": set, "first_seen": ts, "packets": int}
        seen: dict[str, dict] = {}
        deadline = loop.time() + self.listen_seconds

        fd_to_sock = {fd: s for fd, (s, _l) in socks.items()}
        fd_to_label = {fd: l for fd, (_s, l) in socks.items()}

        try:
            while True:
                remaining = deadline - loop.time()
                if remaining <= 0:
                    break
                try:
                    ready = await asyncio.wait_for(
                        self._select(loop, list(fd_to_sock.values())),
                        timeout=remaining)
                except asyncio.TimeoutError:
                    break
                for sock in ready:
                    try:
                        data, addr = sock.recvfrom(4096)
                    except OSError:
                        continue
                    src = addr[0]
                    if not self.scope.in_scope(src):
                        continue  # out-of-scope chatter is observed but never recorded
                    label = fd_to_label[sock.fileno()]
                    rec = seen.setdefault(src, {
                        "labels": set(), "hints": set(),
                        "first_seen": time.time(), "packets": 0})
                    rec["labels"].add(label)
                    rec["packets"] += 1
                    hint = _device_hint(label, data)
                    if hint:
                        rec["hints"].add(hint)
        finally:
            for sock, _label in socks.values():
                try:
                    sock.close()
                except OSError:
                    pass

        for host, rec in sorted(seen.items(), key=lambda kv: kv[0]):
            writer.write(ScanResult(
                self.name, host, status="observed",
                data={
                    "method": "passive_listen",
                    "announced_via": sorted(rec["labels"]),
                    "device_hints": sorted(rec["hints"])[:5],
                    "packets_observed": rec["packets"],
                },
                evidence="announced via " + ", ".join(sorted(rec["labels"])),
            ))
        LOG.info("passive: %d in-scope host(s) observed (0 packets sent)", len(seen))
        return coverage

    @staticmethod
    async def _select(loop, socks: list[socket.socket]) -> list[socket.socket]:
        """Await readability on any listener without blocking the event loop."""
        fut: asyncio.Future = loop.create_future()
        registered: list[socket.socket] = []

        def _ready(s):
            if not fut.done():
                fut.set_result(None)

        for s in socks:
            loop.add_reader(s.fileno(), _ready, s)
            registered.append(s)
        try:
            await fut
        finally:
            for s in registered:
                loop.remove_reader(s.fileno())
        return [s for s in socks if _is_readable(s)]


def _is_readable(sock: socket.socket) -> bool:
    import select
    r, _, _ = select.select([sock], [], [], 0)
    return bool(r)


def main() -> None:
    parser = base_argparser("Passive listen-only discovery (OT/ICS-safe)")
    # -t is accepted for interface symmetry but NOT used to send anything; scope
    # is what filters which observed hosts get recorded.
    parser.add_argument("--listen-seconds", type=float, default=60.0,
                        help="how long to listen (default 60s)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            collector = PassiveCollector(scope, listen_seconds=args.listen_seconds)
            await collector.run(writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
