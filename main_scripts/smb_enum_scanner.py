"""
smb_enum_scanner.py — SMB null-session enumeration (VA checklist: anonymous
information disclosure over SMB/445).

METHOD (collection, read-only): open an SMB session with EMPTY credentials
(a "null session"), and — only if the server accepts it — read what it
volunteers: the OS/domain identity, the share list, and the local/domain user
list (SAMR enumeration, with LSAT RID-cycling as a fallback). Everything here is
information the server chooses to disclose to an unauthenticated peer.

POLICY BOUNDARY (important, read before shipping): a null session sends EMPTY
credentials — it is NOT credential guessing, spraying, or brute force, so it
stays inside the probe's "no guessed credentials" invariant. But it IS an
(anonymous) authentication and it is visible to an IDS. It is therefore a
DELIBERATE, DOCUMENTED capability that only runs against in-scope hosts with SMB
open. If a null session is refused, that is the secure result and we simply
record it.

TECHNIQUE PROVENANCE: the enumeration technique (null session → shares, SAMR
users, RID cycling 500-550/1000-1050) mirrors enum4linux-ng, which is GPL — so we
reimplement it NATIVELY with the impacket library the probe already ships
(never copying GPL code, never shelling out to Samba). The exact impacket call
sequences follow impacket's own MIT/Apache example scripts (lookupsid.py,
samrdump.py) verified against the installed impacket version.

SAFETY: every enumeration phase is independently guarded (one failure never
aborts the rest) and bounded (user/share caps, RID range cap, socket timeout) so
a hostile or huge directory cannot hang or flood the probe. impacket is imported
lazily and its blocking calls run in a thread (never in the event loop).
"""

from __future__ import annotations

import asyncio

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_SMB_PORTS = [445]

# Bounds — a null session against a huge or hostile directory must never hang or
# flood the probe. RID cycling stays deliberately small (local + first domain
# accounts), matching enum4linux-ng's defaults rather than a 0..4000 sweep.
DEFAULT_RID_RANGES = "500-550,1000-1050"
MAX_USERS = 2000
MAX_SHARES = 256
MAX_RIDS = 4096


def parse_rid_ranges(spec: str) -> list[int]:
    """Parse 'a-b,c-d,e' into a sorted, de-duplicated, bounded list of RIDs.

    Bounded to MAX_RIDS so a pasted '0-1000000' can't turn into a brute sweep.
    Invalid tokens are skipped rather than raising — this feeds a network cap,
    not a security decision.
    """
    out: set[int] = set()
    for tok in str(spec or "").split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            if "-" in tok:
                lo, hi = tok.split("-", 1)
                lo_i, hi_i = int(lo), int(hi)
                if lo_i > hi_i:
                    lo_i, hi_i = hi_i, lo_i
                # Expand incrementally and stop at the cap — a single huge token
                # (e.g. "0-100000000") must never balloon memory/CPU before the
                # length check that a per-range update() would skip.
                for i in range(lo_i, hi_i + 1):
                    out.add(i)
                    if len(out) >= MAX_RIDS:
                        break
            else:
                out.add(int(tok))
        except ValueError:
            continue
        if len(out) >= MAX_RIDS:
            break
    return sorted(out)[:MAX_RIDS]


# ── impacket enumeration (blocking; runs in a worker thread) ──────────────────
def _enum_shares(smb) -> list[dict]:
    """List SMB shares over the null session. Read-only (share listing, no file
    access). Bounded to MAX_SHARES."""
    shares: list[dict] = []
    try:
        for s in smb.listShares()[:MAX_SHARES]:
            name = _decode(s["shi1_netname"])
            remark = _decode(s.get("shi1_remark", ""))
            shares.append({"name": name, "remark": remark,
                           "type": int(s.get("shi1_type", 0))})
    except Exception:
        pass
    return shares


def _enum_users_samr(smb, target: str, port: int) -> list[dict]:
    """Enumerate domain/local users via the SAMR named pipe, reusing the null
    session. Mirrors impacket's samrdump.py. Bounded to MAX_USERS."""
    from impacket.dcerpc.v5 import transport, samr
    from impacket.dcerpc.v5.rpcrt import DCERPCException

    users: list[dict] = []
    rpc = transport.SMBTransport(target, port, r"\samr", smb_connection=smb)
    dce = rpc.get_dce_rpc()
    try:
        dce.connect()
        dce.bind(samr.MSRPC_UUID_SAMR)
        server = samr.hSamrConnect(dce)["ServerHandle"]
        domains = samr.hSamrEnumerateDomainsInSamServer(dce, server)["Buffer"]["Buffer"]
        for dom in domains:
            dom_name = _decode(dom["Name"])
            if dom_name.lower() == "builtin":
                continue  # BUILTIN groups aren't the interesting account set
            sid = samr.hSamrLookupDomainInSamServer(dce, server, dom["Name"])["DomainId"]
            dh = samr.hSamrOpenDomain(dce, serverHandle=server, domainId=sid)["DomainHandle"]
            status = 0x105  # STATUS_MORE_ENTRIES
            ctx = 0
            while status == 0x105 and len(users) < MAX_USERS:
                try:
                    resp = samr.hSamrEnumerateUsersInDomain(dce, dh, enumerationContext=ctx)
                except DCERPCException as e:
                    if "STATUS_MORE_ENTRIES" not in str(e):
                        break
                    resp = e.get_packet()
                for u in resp["Buffer"]["Buffer"]:
                    users.append({"name": _decode(u["Name"]), "rid": int(u["RelativeId"]),
                                  "domain": dom_name, "source": "samr"})
                    if len(users) >= MAX_USERS:
                        break
                ctx = resp["EnumerationContext"]
                status = resp["ErrorCode"]
    except Exception:
        pass
    finally:
        try:
            dce.disconnect()
        except Exception:
            pass
    return users


def _enum_users_ridcycle(smb, target: str, port: int, rids: list[int]) -> list[dict]:
    """RID-cycling fallback via LSAT: resolve <DomainSID>-<rid> for each rid to a
    name. Catches accounts even when SAMR enumeration is restricted. Mirrors
    impacket's lookupsid.py. Bounded by the (already capped) rid list."""
    from impacket.dcerpc.v5 import transport, lsat, lsad
    from impacket.dcerpc.v5.samr import SID_NAME_USE
    from impacket.dcerpc.v5.dtypes import MAXIMUM_ALLOWED
    from impacket.dcerpc.v5.rpcrt import DCERPCException

    found: list[dict] = []
    if not rids:
        return found
    rpc = transport.SMBTransport(target, port, r"\lsarpc", smb_connection=smb)
    dce = rpc.get_dce_rpc()
    try:
        dce.connect()
        dce.bind(lsat.MSRPC_UUID_LSAT)
        policy = lsad.hLsarOpenPolicy2(
            dce, MAXIMUM_ALLOWED | lsat.POLICY_LOOKUP_NAMES)["PolicyHandle"]
        info = lsad.hLsarQueryInformationPolicy2(
            dce, policy, lsad.POLICY_INFORMATION_CLASS.PolicyAccountDomainInformation)
        domain_sid = info["PolicyInformation"]["PolicyAccountDomainInfo"]["DomainSid"].formatCanonical()
        sids = [f"{domain_sid}-{r}" for r in rids]
        try:
            resp = lsat.hLsarLookupSids(dce, policy, sids, lsat.LSAP_LOOKUP_LEVEL.LsapLookupWksta)
        except DCERPCException as e:
            if "STATUS_SOME_NOT_MAPPED" in str(e):
                resp = e.get_packet()
            elif "STATUS_NONE_MAPPED" in str(e):
                return found
            else:
                raise
        for n, item in enumerate(resp["TranslatedNames"]["Names"]):
            if item["Use"] == SID_NAME_USE.SidTypeUnknown:
                continue
            dom_idx = item["DomainIndex"]
            dom = ""
            if dom_idx >= 0:
                dom = _decode(resp["ReferencedDomains"]["Domains"][dom_idx]["Name"])
            found.append({"name": _decode(item["Name"]), "rid": rids[n],
                          "domain": dom, "source": "rid_cycle",
                          "sid_type": SID_NAME_USE.enumItems(item["Use"]).name})
    except Exception:
        pass
    finally:
        try:
            dce.disconnect()
        except Exception:
            pass
    return found


def _merge_users(*lists: list[dict]) -> list[dict]:
    """Merge user lists, de-duplicated by (name, rid); SAMR entries win over RID
    cycling for the same account."""
    by_key: dict[tuple, dict] = {}
    for lst in lists:
        for u in lst:
            key = (u.get("name", "").lower(), u.get("rid"))
            if key not in by_key or u.get("source") == "samr":
                by_key[key] = u
    return sorted(by_key.values(), key=lambda u: (u.get("rid") or 0, u.get("name", "")))


def _decode(val) -> str:
    if isinstance(val, bytes):
        val = val.decode("utf-8", "replace")
    return str(val).rstrip("\x00").strip()


class SMBEnumScanner(BaseScanner):
    name = "smb_enum_scan"

    def __init__(self, *args, ports: list[int] | None = None,
                 rid_ranges: str = DEFAULT_RID_RANGES, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_SMB_PORTS
        self.rids = parse_rid_ranges(rid_ranges)

    def _enumerate(self, target: str, port: int) -> dict:
        """Blocking: attempt a null session and enumerate what the server
        volunteers. Returns a fact dict; raises only for 'impacket missing'."""
        try:
            from impacket.smbconnection import SMBConnection
        except ImportError:
            return {"smb": None, "error": "impacket_not_installed"}

        try:
            smb = SMBConnection(target, target, sess_port=port, timeout=self.timeout)
        except Exception as exc:
            return {"smb": False, "reason": "no_smb", "detail": str(exc)}

        try:
            try:
                smb.login("", "")  # null session: EMPTY credentials, no guessing
            except Exception as exc:
                # SMB is present but refuses the null session — the secure result.
                return {"smb": True, "null_session": False, "reason": "null_refused",
                        "detail": str(exc)[:200]}

            guest = bool(smb.isGuestSession()) if hasattr(smb, "isGuestSession") else False
            data: dict = {
                "smb": True,
                "null_session": True,
                "guest_session": guest,
                "server_os": _safe(smb.getServerOS),
                "server_name": _safe(smb.getServerName),
                "server_domain": _safe(smb.getServerDomain),
            }
            shares = _enum_shares(smb)
            samr_users = _enum_users_samr(smb, target, port)
            rid_users = _enum_users_ridcycle(smb, target, port, self.rids)
            users = _merge_users(samr_users, rid_users)
            data.update({
                "shares": shares, "share_count": len(shares),
                "users": users, "user_count": len(users),
                "user_enum_method": ("samr" if samr_users else "")
                                    + ("+rid_cycle" if rid_users else ""),
            })
            return data
        finally:
            try:
                smb.close()
            except Exception:
                pass

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
        if not data.get("smb"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_smb"),
                              data=data)
        evidence = (f"null_session={data.get('null_session')} "
                    f"shares={data.get('share_count', 0)} users={data.get('user_count', 0)}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def _safe(fn) -> str:
    try:
        return _decode(fn())
    except Exception:
        return ""


def main() -> None:
    parser = base_argparser("SMB null-session enumeration (shares / users)")
    parser.add_argument("-p", "--ports", default=None, help="SMB ports (default: 445)")
    parser.add_argument("--rid-ranges", default=DEFAULT_RID_RANGES,
                        help=f"RID ranges to cycle (default: {DEFAULT_RID_RANGES})")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_SMB_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SMBEnumScanner(scope, rate=args.rate, concurrency=args.concurrency,
                                 timeout=args.timeout, ports=ports,
                                 rid_ranges=args.rid_ranges)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
