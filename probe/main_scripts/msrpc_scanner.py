"""
msrpc_scanner.py — MSRPC endpoint-mapper (EPM) enumeration over port 135
(VA checklist: Windows RPC service-surface disclosure).

METHOD (collection, read-only): bind to the Windows endpoint mapper (EPM,
ncacn_ip_tcp:<host>[135]) and call ept_lookup — the same "rpcinfo for Windows"
that `rpcdump` performs. This returns every registered RPC interface (UUID +
version), its string binding (dynamic TCP port or named pipe), and an annotation.
No interface is invoked and no credentials are sent — we only read the public
service map the endpoint mapper hands to anonymous callers.

The endpoint map is recon-grade information: it reveals which services run (task
scheduler, DCOM, spoolss, DRSUAPI, etc.) and the high dynamic ports they listen
on — narrowing an attacker's next move. On an enterprise perimeter, 135/EPM should
be firewalled from untrusted zones.

LIBRARY: reimplemented natively with the impacket the probe already ships (this
is genuine MSRPC, which impacket speaks). Lazy import + graceful degrade; the
blocking impacket call runs in a worker thread; the endpoint list is bounded.
"""

from __future__ import annotations

import asyncio

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_MSRPC_PORTS = [135]
MAX_ENTRIES = 2000


def _summarize(endpoints: list[dict]) -> dict:
    """Reduce the raw endpoint list to distinct interfaces and dynamic ports."""
    interfaces = sorted({e.get("uuid", "").split(" ")[0] for e in endpoints if e.get("uuid")})
    named = sorted({e.get("exe") for e in endpoints if e.get("exe")})
    return {"interface_count": len(interfaces), "interfaces": interfaces,
            "named_services": named}


class MSRPCScanner(BaseScanner):
    name = "msrpc_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_MSRPC_PORTS

    def _enumerate(self, target: str, port: int) -> dict:
        """Blocking: EPM ept_lookup via impacket. Monkeypatchable for tests."""
        try:
            from impacket.dcerpc.v5 import transport, epm
            from impacket import uuid as iuuid
        except ImportError:
            return {"msrpc": None, "error": "impacket_not_installed"}

        stringbinding = r"ncacn_ip_tcp:%s[%d]" % (target, port)
        try:
            rpctransport = transport.DCERPCTransportFactory(stringbinding)
            if hasattr(rpctransport, "set_connect_timeout"):
                rpctransport.set_connect_timeout(int(self.timeout) or 5)
            dce = rpctransport.get_dce_rpc()
            dce.connect()
            try:
                resp = epm.hept_lookup(None, dce=dce)
            finally:
                try:
                    dce.disconnect()
                except Exception:
                    pass
        except Exception as exc:
            return {"msrpc": None, "reason": "no_msrpc", "detail": str(exc)[:160]}

        endpoints: list[dict] = []
        for entry in (resp or []):
            if len(endpoints) >= MAX_ENTRIES:
                break
            try:
                floors = entry["tower"]["Floors"]
                iface = str(floors[0])
                binding = epm.PrintStringBinding(floors)
                annotation = ""
                try:
                    ann = entry["annotation"]
                    if ann:
                        annotation = bytes(ann).split(b"\x00")[0].decode("utf-8", "replace")
                except Exception:
                    annotation = ""
                exe = ""
                try:
                    key = iuuid.uuidtup_to_bin(iuuid.string_to_uuidtup(iface))[:18]
                    exe = epm.KNOWN_UUIDS.get(key, "")
                except Exception:
                    exe = ""
                endpoints.append({"uuid": iface, "binding": binding,
                                  "annotation": annotation, "exe": exe})
            except Exception:
                continue

        data = {"msrpc": True, "endpoint_count": len(endpoints), "endpoints": endpoints}
        data.update(_summarize(endpoints))
        return data

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._enumerate, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if data.get("error") == "impacket_not_installed":
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="error", error="impacket not installed")
        if not data.get("msrpc"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_msrpc"),
                              data=data)
        evidence = (f"endpoints={data.get('endpoint_count', 0)} "
                    f"interfaces={data.get('interface_count', 0)}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("MSRPC endpoint-mapper (EPM) enumeration")
    parser.add_argument("-p", "--ports", default=None, help="MSRPC ports (default: 135)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_MSRPC_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = MSRPCScanner(scope, rate=args.rate, concurrency=args.concurrency,
                               timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
