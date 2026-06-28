# How the probe works — flow, gates & commands

The probe is a **gated, cache-aware funnel**: scope → profile → discovery →
ports → banners → behaviour-routed deep scans. Everything lives in
`workflow/run_engagement()`; each stage has a *precondition* (a gate) and is
skipped when the gate is false. Every result merges into one `Asset` per host
("what do we know so far?"), which drives the next decision.

```
scope.txt ──(hard allowlist; nothing runs outside it)
   │
[profile?] ──ot──> passive_collector ONLY ──> stop
   │ it/iot
host_discovery ──(live hosts only)──> port_scan ──(open ports only)──> service_banner
   │                                                                        │
   │                                         [router: banner reveals what it actually is]
   │                                              ├─ HTTP/1.x  → web_scan
   │                                              ├─ silent TLS → tls_scan   (catches HTTPS on odd ports)
   │                                              ├─ DB greeting → db_scan
   │                                              └─ 445/161/AI → smb / snmp / mcp_ai
   └─ udp_scan (uncertain results: no-reply is ambiguous)
        │
   [cache: deterministic facts reused on re-runs; uncertain ones re-probed]
```

---

## 0. Run it (the normal way)

```bash
cd probe
echo "192.168.0.34/32" > scope.txt          # the allowlist — one IP/CIDR per line

python3 -m workflow.cli -t 192.168.0.34 -s scope.txt --mode assessment -o result.json
#   --mode  triage | assessment | service-specific | re-scan
#   --profile it | iot | ot        (default it)
#   --services web,db,tls,...       (service-specific mode only)

python3 -m json.tool result.json | head -40       # inspect the per-host facts
```

| mode | what runs |
|---|---|
| `triage` | discovery + ports + banners only (fast snapshot) |
| `assessment` | the full funnel, every deep branch |
| `service-specific` | only the branches in `--services` |
| `re-scan` | reuse a prior run's cache, re-probe only stale/uncertain facts |

---

## 1. Scope gate — nothing runs outside `scope.txt`

`ScopeGuard` is a hard allowlist; `run_engagement` filters targets at the entry,
before any packet.

```bash
python3 -c "
import sys; sys.path.insert(0,'.')
from scanner.scanner_base import ScopeGuard
s = ScopeGuard.from_list(['192.168.0.34/32'])
print('in scope  192.168.0.34 ->', s.in_scope('192.168.0.34'))
print('out scope 8.8.8.8      ->', s.in_scope('8.8.8.8'))
"
# in scope  192.168.0.34 -> True
# out scope 8.8.8.8      -> False
```

---

## 2. Profile gate — `ot` is passive-only (hard stop)

```bash
python3 -c "
import sys; sys.path.insert(0,'.')
from workflow.gates import gate_0_is_passive_profile, PROFILE_PORTS
print('ot passive-only? ', gate_0_is_passive_profile('ot'))   # True -> listen only, no probes
print('it ports scanned:', len(PROFILE_PORTS['it']), 'ports')
print('iot ports scanned:', len(PROFILE_PORTS['iot']), 'ports')
"
```
`ot` → runs `passive_collector` only and returns. `it`/`iot` continue and set
the port list + rate/timeout.

---

## 3. Host discovery — only live hosts proceed

```bash
python3 -c "
import asyncio, sys; sys.path.insert(0,'.')
from scanner.scanner_base import ScopeGuard
from scanner.host_discovery import HostDiscoveryScanner
async def main():
    scope = ScopeGuard.from_list(['192.168.0.34/32'])
    for r in await HostDiscoveryScanner(scope, timeout=2.0).scan_target('192.168.0.34'):
        print('alive:', r.data.get('alive'), '| responding:', r.data.get('responding_ports'))
asyncio.run(main())
"
```
`asset.last_seen_alive` gets set on a response; `gate_3` then skips any host
where it's still `None`. (Your `.35` came back `alive=False` → dropped here.)

---

## 4. Port scan — on live hosts, then banners on open ports

```bash
python3 -c "
import asyncio, sys; sys.path.insert(0,'.')
from scanner.scanner_base import ScopeGuard
from scanner.port_scanner import PortScanner
from scanner.service_banner import ServiceBannerScanner
async def main():
    scope = ScopeGuard.from_list(['192.168.0.34/32'])
    open_ports = []
    for r in await PortScanner(scope, ports=[80,443,3306,8080,8443], timeout=2.0).scan_target('192.168.0.34'):
        if r.status == 'open': open_ports.append(r.port)
    print('open ports:', open_ports)
    for r in await ServiceBannerScanner(scope, ports=open_ports, timeout=3.0).scan_target('192.168.0.34'):
        print(' ', r.port, '->', (r.data.get('first_line') or r.data.get('banner') or 'no banner')[:50])
asyncio.run(main())
"
```
Only `status == open` ports flow on (`asset.open_ports_for_deep_scan()`).

---

## 5. The router — routes by **observed behaviour**, not port number

This is what catches HTTPS on a non-standard port: a silent open port (raw TLS
answers our probe with nothing) gets routed to `tls_scan` even if it's not in
the static TLS port table.

```bash
python3 -c "
import sys; sys.path.insert(0,'.')
from workflow.router import looks_like_http, looks_like_tls
print('HTTP banner -> web? ', looks_like_http({'first_line':'HTTP/1.1 200 OK'}))   # True
print('silent :9443 -> tls?', looks_like_tls(9443, {'banner': None}))              # True
print('silent :8443 -> tls?', looks_like_tls(8443, {'banner': None}))             # False (client-first port)
"
```
Final per-branch decision = `gate_5_branch_eligible`: runs if **router flagged it
OR an open port is in the branch's static table**, *and* the profile/`--services`
filter allow it.

---

## 6. Deep scans — the conditional forest

```bash
python3 -c "
import asyncio, sys, json; sys.path.insert(0,'.')
from scanner.scanner_base import ScopeGuard
from scanner.web_scanner import WebScanner
from scanner.db_scanner import DBScanner, DEFAULT_DB_PORTS
from scanner.tls_scanner import TLSScanner
async def main():
    scope = ScopeGuard.from_list(['192.168.0.34/32'])
    for r in await WebScanner(scope, ports=[80,8080], timeout=4.0).scan_target('192.168.0.34'):
        print('web ', r.port, json.dumps(r.data)[:90])
    for r in await DBScanner(scope, port_map={3306:DEFAULT_DB_PORTS[3306]}, timeout=4.0).scan_target('192.168.0.34'):
        print('db  ', r.port, json.dumps(r.data)[:90])
    for r in await TLSScanner(scope, ports=[8443], timeout=4.0).scan_target('192.168.0.34'):
        print('tls ', r.port, json.dumps(r.data)[:90])
asyncio.run(main())
"
```
`smb_scan` (445), `snmp_scan` (161), `mcp_ai_scan` (AI ports), `udp_scan`
(53/123/137/161) run only when the relevant port-state suggests it. UDP results
are tagged **uncertain** (no-reply = closed | filtered | dropped — ambiguous).

---

## 7. Caching — settled facts are free on re-runs

`WorkflowCache`, keyed `(host, port, scanner)`. `should_recheck()` decides reuse
vs re-probe from each fact's certainty:

```bash
python3 -c "
import sys; sys.path.insert(0,'.')
from workflow.cache import FACT_CERTAINTY
for k,v in FACT_CERTAINTY.items(): print(f'  {k:18} {v}')
"
```
- **deterministic** (banner/tls/web/db/smb/snmp) → reused within the engagement.
- **uncertain** (host_discovery, udp, anything that errored/timed out) → always re-probed.

A `re-scan` reuses deterministic facts and only re-checks volatile ones → far
fewer packets, and a delta report of what changed.

---

## The whole run in one call (what the manager triggers)

```bash
python3 -c "
import sys, json; sys.path.insert(0,'.')
from agent.engine import run_scan
r = run_scan('assessment', {'targets':['192.168.0.34'], 'scope_cidrs':['192.168.0.34/32']})
print(json.dumps({k:(f'<{len(v)} facts>' if k=='facts' else v) for k,v in r.items()}, indent=2))
"
```
Output is the **raw facts** the probe ships to the manager — `finding_count` is
always `0`: the probe never produces CVEs. Detection (version → CVE) runs on the
manager against the pinned vuln DB, which never enters the client network.

> **Model:** scope filters *who* → profile sets *how hard* → discovery finds *who's
> alive* → ports find *what's open* → banners reveal *what each port is* → router
> sends each to the *right* deep scanner by behaviour → cache makes settled facts
> free next time.
