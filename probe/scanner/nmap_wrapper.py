"""
nmap_wrapper.py — orchestrate nmap and normalize its XML into ScanResult.

WHY: nmap is 25+ years of battle-tested scanning. For discovery, SYN scanning
(root), service/version detection (-sV), OS detection (-O), and protocol checks
(NSE), wrapping it is the right call — do not reimplement it. This module runs
nmap as a subprocess and parses its XML so its findings land in the SAME schema
as the pure-Python scanners, letting you compare accuracy/FP between engines.

LICENSING NOTE: nmap is distributed under the Nmap Public Source License
(GPLv2-derived). Redistributing nmap inside a commercial product can trigger
licensing obligations — review before bundling. Here we INVOKE an nmap that is
already installed on the system rather than shipping it.

COLLECTION ONLY: we run discovery/version/OS/safe NSE categories. We do NOT run
exploit/intrusive NSE scripts.
"""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import xml.etree.ElementTree as ET

from .scanner_base import (
    ScanResult, ScopeGuard, ResultWriter, expand_targets,
    setup_logging, base_argparser, LOG, main_entrypoint, parse_ports,
)

# Scan profiles. Note: -sS (SYN) and -O (OS) require root; -sT/-sV do not.
PROFILES = {
    "discovery": ["-sn", "-PR", "-PE", "-PS80,443", "-PA80"],
    "version":   ["-sT", "-sV", "--version-intensity", "5"],
    "os":        ["-sT", "-O"],
    "smb":       ["-p", "139,445", "--script", "smb-protocols,smb2-security-mode"],
    "fast":      ["-sT", "-F"],
}


class NmapExecutionError(OSError):
    """Actionable subprocess failure; never reinterpret it as zero findings."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        returncode: int | None = None,
        stderr: str = "",
    ):
        super().__init__(message)
        self.code = code
        self.returncode = returncode
        self.stderr = stderr


_EXTRA_FLAGS = {"-Pn", "-6", "--open", "--reason"}
_EXTRA_VALUE_FLAGS = {
    "--host-timeout",
    "--script-timeout",
    "--max-retries",
    "--version-intensity",
    "--top-ports",
}


def _validated_extra_args(raw: str) -> list[str]:
    """Allow tuning only; target, script, and output controls stay owned here."""
    tokens = shlex.split(raw)
    validated: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in _EXTRA_FLAGS or (
            len(token) == 3
            and token.startswith("-T")
            and token[2] in "012345"
        ):
            validated.append(token)
            index += 1
            continue
        if token in _EXTRA_VALUE_FLAGS:
            if index + 1 >= len(tokens):
                raise ValueError(f"{token} requires a value")
            value = tokens[index + 1]
            if token in {"--max-retries", "--version-intensity", "--top-ports"}:
                try:
                    number = int(value)
                except ValueError:
                    raise ValueError(f"{token} requires an integer") from None
                lower = 0 if token in {"--max-retries", "--version-intensity"} else 1
                upper = 9 if token == "--version-intensity" else 65535
                if not lower <= number <= upper:
                    raise ValueError(
                        f"{token} value must be between {lower} and {upper}"
                    )
            elif not value or value.startswith("-"):
                raise ValueError(f"{token} requires a duration")
            validated.extend((token, value))
            index += 2
            continue
        raise ValueError(
            f"unsupported --extra-args token {token!r}; target, output, "
            "script, and input-file options are intentionally blocked"
        )
    return validated


def _have_nmap() -> bool:
    return shutil.which("nmap") is not None


def _run_nmap(targets: list[str], extra: list[str], timeout: int) -> str:
    cmd = ["nmap", "-oX", "-", "-n", *extra, *targets]
    LOG.info("running: %s", " ".join(cmd))
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise NmapExecutionError(
            "timeout",
            f"nmap exceeded the {timeout}s job timeout; narrow the scope or "
            "increase --nmap-timeout",
            stderr=(exc.stderr or "")[-1000:] if isinstance(exc.stderr, str) else "",
        ) from exc
    except FileNotFoundError as exc:
        raise NmapExecutionError(
            "dependency_missing",
            "nmap was not found on PATH; install it or use the native collectors",
        ) from exc

    stderr = (proc.stderr or "")[-1000:]
    if not proc.stdout.strip():
        code = "nonzero_exit" if proc.returncode else "empty_output"
        raise NmapExecutionError(
            code,
            f"nmap returned no XML output (rc={proc.returncode}): {stderr}",
            returncode=proc.returncode,
            stderr=stderr,
        )
    if proc.returncode != 0:
        # Nmap can flush complete XML before an abnormal exit. Preserve that
        # evidence, but make the degraded state visible in operator logs.
        LOG.warning(
            "nmap produced potentially partial XML (rc=%d): %s",
            proc.returncode,
            stderr,
        )
    return proc.stdout


def _parse_nmap_xml(xml_text: str, profile: str) -> list[ScanResult]:
    results: list[ScanResult] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise NmapExecutionError(
            "parse_error",
            f"nmap XML was incomplete or incompatible: {exc}",
        ) from exc

    finished = root.find("./runstats/finished")
    if finished is not None and finished.get("exit") not in {None, "success"}:
        message = finished.get("errormsg") or "nmap reported an abnormal scan exit"
        results.append(ScanResult(
            scanner="nmap_" + profile,
            target="<nmap-run>",
            status="error",
            data={
                "error_code": "nonzero_exit",
                "retryable": False,
                "remediation": (
                    "Check target reachability, selected profile privileges, and "
                    "the installed Nmap data-file version."
                ),
            },
            error=message[:300],
        ))

    for host in root.findall("host"):
        # NOTE: `Element.find(...) or Element.find(...)` is a classic ElementTree
        # trap — an Element with no children is falsy even when found (it tests
        # len(), not identity), so the first match would be silently discarded.
        # Explicit `is not None` checks avoid that.
        addr_el = host.find("address[@addrtype='ipv4']")
        if addr_el is None:
            addr_el = host.find("address")
        addr = addr_el.get("addr") if addr_el is not None else "?"

        status_el = host.find("status")
        host_state = status_el.get("state") if status_el is not None else "unknown"

        # Host-level (discovery / OS) result.
        if profile in ("discovery", "os"):
            data = {"host_state": host_state}
            os_el = host.find("os")
            if os_el is not None:
                matches = [{"name": m.get("name"), "accuracy": m.get("accuracy")}
                           for m in os_el.findall("osmatch")]
                if matches:
                    data["os_matches"] = matches[:3]
            results.append(ScanResult(
                "nmap_" + profile, addr,
                status="open" if host_state == "up" else "filtered",
                data=data, evidence=f"host {host_state}"))

        # Port-level results.
        for port in host.findall(".//port"):
            portid = int(port.get("portid"))
            proto = port.get("protocol")
            st = port.find("state")
            state = st.get("state") if st is not None else "unknown"
            svc = port.find("service")
            data = {}
            evidence = state
            if svc is not None:
                data = {
                    "service": svc.get("name"),
                    "product": svc.get("product"),
                    "version": svc.get("version"),
                    "extrainfo": svc.get("extrainfo"),
                    "cpe": [c.text for c in svc.findall("cpe")],
                }
                evidence = " ".join(filter(None, [
                    svc.get("name"), svc.get("product"), svc.get("version")]))
            # NSE script output (e.g. smb-protocols).
            scripts = {s.get("id"): s.get("output") for s in port.findall("script")}
            if scripts:
                data["scripts"] = scripts
            if state == "open" or profile == "smb":
                results.append(ScanResult(
                    "nmap_" + profile, addr, port=portid, proto=proto,
                    status=state, data=data, evidence=evidence))
    return results


def main() -> None:
    parser = base_argparser("nmap orchestrator (discovery/version/os/smb)")
    parser.add_argument("--profile", choices=list(PROFILES.keys()),
                        default="version", help="nmap scan profile")
    parser.add_argument("--nmap-timeout", type=int, default=900,
                        help="overall nmap subprocess timeout (s)")
    parser.add_argument("-p", "--ports",
                        help="ports for profiles that perform a port scan")
    parser.add_argument("--extra-args", default="",
                        help="allowlisted nmap tuning args (advanced)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    def _run() -> None:
        if not _have_nmap():
            LOG.error("nmap is not installed. Install nmap or use the pure-Python "
                      "scanners (port_scanner.py, service_banner.py, ...).")
            return

        scope = ScopeGuard.from_file(args.scope)
        targets = [t for t in expand_targets(args.targets) if scope.in_scope(t)]
        if not targets:
            LOG.error("no in-scope targets")
            return

        extra = list(PROFILES[args.profile])
        if args.ports:
            ports = parse_ports(args.ports)
            extra += ["-p", ",".join(str(port) for port in ports)]
        if args.rate <= 0:
            raise ValueError("--rate must be greater than zero")
        extra += ["--max-rate", str(max(1, min(int(args.rate), 2000)))]
        if args.extra_args:
            extra += _validated_extra_args(args.extra_args)

        xml_text = _run_nmap(targets, extra, args.nmap_timeout)
        results = _parse_nmap_xml(xml_text, args.profile)

        writer = ResultWriter(args.output, also_stdout=True)
        try:
            for r in results:
                writer.write(r)
        finally:
            writer.close()
        LOG.info("nmap_%s done — %d result(s)", args.profile, writer.count)

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
