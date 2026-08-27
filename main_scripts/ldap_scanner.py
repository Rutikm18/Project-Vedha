"""
ldap_scanner.py — LDAP anonymous-bind enumeration (VA checklist: anonymous
directory exposure over LDAP/389 and LDAPS/636).

METHOD (collection, read-only): perform an ANONYMOUS LDAP bind (no username, no
password) and, only if the server accepts it, read what it volunteers — the
RootDSE (naming contexts, functional levels, vendor, DNS host name) and, as a
bounded probe, whether the directory tree itself is readable without
authentication.

POLICY BOUNDARY: an anonymous bind sends EMPTY credentials — it is not credential
guessing/spraying, so it stays inside the probe's "no guessed credentials"
invariant. It is a deliberate, documented capability that only runs against
in-scope hosts with LDAP open. Most directories permit an anonymous RootDSE read
(low risk); the security-relevant escalation is when the directory *tree* is also
anonymously readable — which this scanner tests with a strict size/time cap.

LIBRARY: uses ldap3 (pure-Python, no C extension → sealed-build friendly),
imported lazily so the module loads even where ldap3 is absent (graceful degrade).
Blocking calls run in a worker thread, never in the event loop. Every phase is
guarded and bounded (connect/receive timeouts, a small search size limit) so a
huge or hostile directory cannot hang or flood the probe.
"""

from __future__ import annotations

import asyncio

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_LDAP_PORTS = [389, 636]
LDAPS_PORT = 636
SEARCH_LIMIT = 20   # cap on the bounded "is the tree anonymously readable?" probe


def _first(other: dict, key: str) -> str:
    v = other.get(key)
    if isinstance(v, (list, tuple)):
        return str(v[0]) if v else ""
    return str(v) if v is not None else ""


class LDAPScanner(BaseScanner):
    name = "ldap_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_LDAP_PORTS

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: anonymous bind + RootDSE read + bounded tree-read probe.
        Returns a fact dict; only 'ldap3 missing' is surfaced as an error."""
        try:
            from ldap3 import Server, Connection, ANONYMOUS, ALL, SUBTREE
            from ldap3.core.exceptions import (
                LDAPException, LDAPSocketOpenError, LDAPBindError)
        except ImportError:
            return {"ldap": None, "error": "ldap3_not_installed"}

        use_ssl = (port == LDAPS_PORT)
        try:
            server = Server(target, port=port, use_ssl=use_ssl, get_info=ALL,
                            connect_timeout=self.timeout)
            conn = Connection(server, authentication=ANONYMOUS, auto_bind=True,
                              receive_timeout=self.timeout)
        except LDAPSocketOpenError as exc:
            return {"ldap": False, "reason": "no_ldap", "detail": str(exc)[:200]}
        except LDAPBindError as exc:
            # Server reachable but anonymous bind refused — the secure result.
            return {"ldap": True, "anonymous_bind": False,
                    "reason": "anon_bind_refused", "detail": str(exc)[:200]}
        except LDAPException as exc:
            return {"ldap": False, "reason": "ldap_error", "detail": str(exc)[:200]}

        try:
            info = server.info
            other = {}
            try:
                other = dict(getattr(info, "other", {}) or {})
            except Exception:
                other = {}
            naming = [str(x) for x in (getattr(info, "naming_contexts", None) or [])]
            data: dict = {
                "ldap": True,
                "ssl": use_ssl,
                "anonymous_bind": True,
                "naming_contexts": naming,
                "default_naming_context": _first(other, "defaultNamingContext"),
                "dns_host_name": _first(other, "dnsHostName"),
                "domain_functional_level": _first(other, "domainFunctionality"),
                "forest_functional_level": _first(other, "forestFunctionality"),
                "supported_ldap_versions": [
                    str(x) for x in (getattr(info, "supported_ldap_versions", None) or [])],
                "vendor": (str(getattr(info, "vendor_name", "") or "") + " "
                           + str(getattr(info, "vendor_version", "") or "")).strip(),
            }

            # Bounded probe: is the directory TREE readable anonymously (not just
            # the RootDSE)? Strict size + time caps — never a full dump.
            base = data["default_naming_context"] or (naming[0] if naming else "")
            anon_search = False
            sample = 0
            if base:
                try:
                    from ldap3.core.exceptions import LDAPException as _LE
                    conn.search(base, "(objectClass=*)", search_scope=SUBTREE,
                                attributes=["objectClass"], size_limit=SEARCH_LIMIT,
                                time_limit=int(self.timeout) + 1)
                    sample = len(conn.entries)
                    anon_search = sample > 0
                except _LE:
                    pass
                except Exception:
                    pass
            data["anonymous_search_allowed"] = anon_search
            data["sample_entry_count"] = sample
            return data
        finally:
            try:
                conn.unbind()
            except Exception:
                pass

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if data.get("error") == "ldap3_not_installed":
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="error", error="ldap3 not installed")
        if not data.get("ldap"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_ldap"),
                              data=data)
        evidence = (f"anon_bind={data.get('anonymous_bind')} "
                    f"anon_search={data.get('anonymous_search_allowed')} "
                    f"naming_contexts={len(data.get('naming_contexts', []))}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("LDAP anonymous-bind enumeration (RootDSE / directory)")
    parser.add_argument("-p", "--ports", default=None,
                        help="LDAP ports (default: 389,636)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_LDAP_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = LDAPScanner(scope, rate=args.rate, concurrency=args.concurrency,
                              timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
