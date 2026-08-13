"""
mass_scan.py — fast large-scale TCP port discovery.

WHY THIS EXISTS (modern context): connect-scanning a /16 takes hours. Companies
need to sweep huge ranges in minutes to answer "what is open across our whole
network right now / what changed since yesterday". That is impossible with the
per-port connect model. masscan is stateless (state encoded in the SYN sequence
number) and scans enormous ranges fast. The standard architecture is two-stage:

    mass_scan (find open ports FAST)  ->  service/version/tls/etc. (deep, only on opens)

This module wraps the `masscan` binary when present and normalizes its JSON into
the SAME ScanResult schema as every other scanner, so the deep scanners can
consume its output directly.

FALLBACK: if masscan is not installed, it falls back to a high-concurrency async
connect sweep (pure stdlib). The fallback is slower than masscan but lets the
module run anywhere; for true internet/large-LAN scale, install masscan.

COLLECTION ONLY: this finds open ports. It does not fingerprint, exploit, or
modify anything. masscan requires root/CAP_NET_RAW for its raw-socket mode.

LICENSING NOTE: masscan is AGPL-3.0. Invoking an installed binary (as here) is
generally fine; bundling/redistributing it in a commercial product triggers AGPL
obligations — review before shipping it inside an appliance.
"""

from __future__ import annotations

import argparse
import asyncio
import ipaddress
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, LOG, RateLimiter,
    main_entrypoint,
)


# --------------------------------------------------------------------------- #
# masscan path (preferred for scale).
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class MasscanRun:
    records: list[dict]
    outcome: str
    error_code: str | None = None
    error: str | None = None
    returncode: int | None = None
    parse_error_count: int = 0


def _have_masscan() -> bool:
    return shutil.which("masscan") is not None


def _run_masscan(target_specs: list[str], ports: str, rate: int,
                 timeout: int, extra: list[str]) -> MasscanRun:
    """
    Run masscan over the given target specs and return its parsed JSON records.
    masscan accepts CIDRs/ranges directly, so we pass scope-validated specs
    rather than expanding to individual hosts (that's the whole point of speed).
    """
    out_fd, out_path = tempfile.mkstemp(suffix=".json")
    os.close(out_fd)  # masscan opens/writes the path itself; we only need the name
    cmd = ["masscan", *target_specs, "-p", ports,
           "--rate", str(rate), "-oJ", out_path, *extra]
    LOG.info("running: %s", " ".join(cmd))
    error_code = None
    error = None
    returncode = None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        returncode = proc.returncode
        if proc.returncode != 0:
            error_code = "nonzero_exit"
            error = f"masscan rc={proc.returncode}: {(proc.stderr or '')[-1000:]}"
    except subprocess.TimeoutExpired as exc:
        error_code = "timeout"
        error = (
            f"masscan exceeded the {timeout}s job timeout; reduce scope/rate "
            "or raise the bounded timeout"
        )
        if isinstance(exc.stderr, str) and exc.stderr:
            error += f": {exc.stderr[-500:]}"
    except FileNotFoundError:
        error_code = "dependency_missing"
        error = "masscan was not found on PATH"
    except PermissionError as exc:
        error_code = "permission_denied"
        error = f"masscan could not start with the current privileges: {exc}"
    except OSError as exc:
        error_code = "launch_failed"
        error = f"masscan could not start: {exc}"

    records: list[dict] = []
    parse_error_count = 0
    output_text = ""
    try:
        with open(out_path, "r", encoding="utf-8") as fh:
            output_text = fh.read()
        records, parse_error_count = _parse_masscan_json_detailed(output_text)
    except OSError as exc:
        if error is None:
            error_code = "output_read_failed"
            error = f"masscan output artifact could not be read: {exc}"
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass

    if parse_error_count:
        parse_message = (
            f"masscan output contained {parse_error_count} malformed record(s)"
        )
        if error:
            error = f"{error}; {parse_message}"
        else:
            error_code = "parse_error"
            error = parse_message
    if error:
        LOG.warning("%s", error)
        return MasscanRun(
            records=records,
            outcome="degraded" if records else "failed",
            error_code=error_code,
            error=error,
            returncode=returncode,
            parse_error_count=parse_error_count,
        )
    return MasscanRun(
        records=records,
        outcome="completed",
        returncode=returncode,
        parse_error_count=parse_error_count,
    )


def _parse_masscan_json(text: str) -> list[dict]:
    """Parse masscan -oJ output robustly: handles trailing comma, 'finished'
    sentinel line, and a missing closing bracket."""
    records, _ = _parse_masscan_json_detailed(text)
    return records


def _parse_masscan_json_detailed(text: str) -> tuple[list[dict], int]:
    text = text.strip()
    if not text:
        return [], 0
    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            records = [item for item in obj if isinstance(item, dict)]
            return records, len(obj) - len(records)
        if isinstance(obj, dict):
            return [obj], 0
    except json.JSONDecodeError:
        pass
    records: list[dict] = []
    parse_errors = 0
    for line in text.splitlines():
        line = line.strip().rstrip(",")
        if not line or line in ("[", "]"):
            continue
        try:
            o = json.loads(line)
            if isinstance(o, dict):
                records.append(o)
            else:
                parse_errors += 1
        except json.JSONDecodeError:
            parse_errors += 1
    return records, parse_errors


def _masscan_records_to_results(records: list[dict],
                                scope: ScopeGuard) -> list[ScanResult]:
    results: list[ScanResult] = []
    for rec in records:
        ip = rec.get("ip")
        if not ip or not scope.in_scope(ip):
            continue
        for p in rec.get("ports", []):
            if p.get("status") != "open":
                continue
            results.append(ScanResult(
                "mass_scan", ip, port=p.get("port"),
                proto=p.get("proto", "tcp"), status="open",
                data={"ttl": p.get("ttl"), "reason": p.get("reason")},
                evidence=f"masscan open ({p.get('reason')})",
            ))
    return results


# --------------------------------------------------------------------------- #
# Fallback: async connect sweep (no masscan, pure stdlib).
# --------------------------------------------------------------------------- #
class _ConnectSweep(BaseScanner):
    name = "mass_scan"

    def __init__(self, *args, ports: list[int], **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports

    async def _probe(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        async with self.sem:
            try:
                fut = asyncio.open_connection(target, port)
                _r, w = await asyncio.wait_for(fut, timeout=self.timeout)
                w.close()
                try:
                    await w.wait_closed()
                except Exception:
                    pass
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="open", evidence="connect open (fallback)")
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
                return None

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._probe(target, p) for p in self.ports]
        return [r for r in await asyncio.gather(*tasks) if r is not None]


# --------------------------------------------------------------------------- #
# Public driver used by both CLI and the orchestrator.
# --------------------------------------------------------------------------- #
async def run_mass_scan(target_specs: list[str], scope: ScopeGuard, *,
                        ports: str = "1-1000", rate: int = 10000,
                        timeout: int = 1800, concurrency: int = 500,
                        per_op_timeout: float = 2.0,
                        force_fallback: bool = False,
                        writer: ResultWriter) -> None:
    """
    target_specs: raw CIDRs/ranges/hosts (NOT pre-expanded) — masscan wants them.
    For the fallback path we expand and connect-sweep.
    """
    # Scope check the specs: every network/host in a spec must be allowed.
    allowed_specs = [s for s in target_specs if _spec_in_scope(s, scope)]
    dropped = set(target_specs) - set(allowed_specs)
    for d in dropped:
        LOG.warning("dropping out-of-scope spec: %s", d)
    if not allowed_specs:
        LOG.error("no in-scope target specs")
        return
    if not 1 <= rate <= 100_000:
        raise ValueError("masscan rate must be between 1 and 100000 packets/second")
    if timeout <= 0:
        raise ValueError("masscan timeout must be greater than zero")

    if _have_masscan() and not force_fallback:
        LOG.info("using masscan (fast path)")
        extra: list[str] = []
        excl = _masscan_excludes(scope)
        if excl:
            extra += ["--exclude", ",".join(excl)]
            LOG.info("masscan: excluding %d out-of-scope network(s) at the "
                     "packet level", len(excl))
        loop = asyncio.get_running_loop()
        run = await loop.run_in_executor(
            None, _run_masscan, allowed_specs, ports, rate, timeout, extra)
        for r in _masscan_records_to_results(run.records, scope):
            writer.write(r)
        if run.outcome != "completed":
            writer.write(ScanResult(
                scanner="mass_scan",
                target="<masscan-run>",
                status="error",
                data={
                    "error_code": run.error_code,
                    "retryable": run.error_code in {
                        "timeout", "resource_exhausted", "output_read_failed",
                    },
                    "remediation": (
                        "Verify CAP_NET_RAW/root access and adapter selection, "
                        "then retry at a lower rate or narrower scope."
                    ),
                    "outcome": run.outcome,
                    "returncode": run.returncode,
                    "parse_error_count": run.parse_error_count,
                    "partial_result_count": len(run.records),
                },
                error=run.error,
            ))
    else:
        if force_fallback:
            LOG.info("masscan fallback forced")
        else:
            LOG.warning("masscan not installed — using slower connect-sweep "
                        "fallback. Install masscan for true large-scale speed.")
        port_list = parse_ports(ports)
        targets = expand_targets(allowed_specs)
        sweeper = _ConnectSweep(scope, ports=port_list, rate=float(rate),
                                concurrency=concurrency, timeout=per_op_timeout)
        await sweeper.run(targets, writer)


def _masscan_excludes(scope: ScopeGuard) -> list[str]:
    """Excluded networks -> masscan --exclude specs, so they get ZERO packets."""
    return [str(net) for net in scope.excludes]


def _spec_in_scope(spec: str, scope: ScopeGuard) -> bool:
    """
    A CIDR spec is in scope only if it is fully contained in an allowed network.
    Single IPs / hostnames use the normal check.
    """
    spec = spec.strip()
    if "-" in spec and "/" not in spec:
        try:
            targets = expand_targets([spec])
        except ValueError:
            return False
        if targets != [spec]:
            return all(scope.in_scope(target) for target in targets)
    try:
        net = ipaddress.ip_network(spec, strict=False)
    except ValueError:
        return scope.in_scope(spec)  # hostname / single
    if net.num_addresses == 1:
        return scope.in_scope(str(net.network_address))
    # require every allowed network to contain it, or it to sit within one
    for allowed in scope.networks:
        try:
            if net.subnet_of(allowed):
                return True
        except TypeError:
            continue
    return False


def main() -> None:
    parser = base_argparser("Mass port scanner (masscan wrapper + fallback)")
    parser.add_argument("-p", "--ports", default="1-1000",
                        help="ports e.g. '1-1000' or '22,80,443' (default 1-1000)")
    parser.add_argument("--masscan-rate", type=int, default=10000,
                        help="masscan packets/sec (default 10000; tune to network)")
    parser.add_argument("--masscan-timeout", type=int, default=1800,
                        help="overall masscan subprocess timeout sec")
    parser.add_argument("--fallback", action="store_true",
                        help="force the pure-Python connect sweep")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        # Keep raw specs for masscan; do not expand here.
        specs = list(args.targets)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await run_mass_scan(
                specs, scope, ports=args.ports, rate=args.masscan_rate,
                timeout=args.masscan_timeout, concurrency=args.concurrency,
                per_op_timeout=args.timeout, force_fallback=args.fallback,
                writer=writer)
        finally:
            writer.close()
            LOG.info("mass_scan done — %d open port(s)", writer.count)

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
