# Probe — Use Cases (what a probe run performs)

The probe drives a per-host **gated funnel** (`workflow/workflow_engine.py`):
every in-scope host walks the stages below in order, each gated on preconditions
(`gates.py`) + the fact cache (`cache.py`), with results merged into the per-host
`Asset` (`asset.py`). This document defines the use cases the probe performs.

---

## 1. Per-host scan pipeline (each stage = a use case)

| # | Use case | Gate | Scanner | Asset output |
|---|----------|------|---------|--------------|
| 1 | **Host discovery** — alive? + MAC / vendor / device-class | 2 | `host_discovery` | `last_seen_alive`, `open_ports` (hints) |
| 2 | **Port scan** — open TCP ports (connect; SYN for wide sweeps) | 3 | `port_scanner` / `syn_scanner` | `open_ports` |
| 3 | **Service banner** — service + version per open port | 4 | `service_banner` | `services[port]` |
| 4 | **OS fingerprint** 🆕 — OS family from TTL/TCP + banners | 4b | `os_fingerprint` | `os_fact` |
| 5 | **Deep service enumeration** 🆕 — services, roles, mgmt/auth surfaces, weak/legacy protocols, hostnames | 5a | `service_enum` | `enrichment` |
| 6 | **TLS assessment** — versions, ciphers, cert, posture grade | 5 | `tls_scanner` | `tls_facts[port]` |
| 7 | **Web assessment** — headers, title, methods | 5 | `web_scanner` | `web_facts[port]` |
| 8 | **SMB assessment** — dialect, signing, SMBv1 | 5 | `smb_scanner` | `smb_state` |
| 9 | **Database fingerprint** — type/version (non-std ports routed by banner) | 5 | `db_scanner` | `db_facts[port]` |
| 10 | **AI/MCP endpoint detection** — exposed AI/MCP servers | 5 | `mcp_ai_scanner` | `ai_facts[port]` |
| 11 | **SNMP assessment** — communities / exposure | 5 | `snmp_scanner` | `snmp_state[port]` |
| 12 | **UDP scan** — UDP services + amplification exposure | 5 | `udp_scanner` | UDP `open_ports` / `services` |
| 13 | **Credentialed collection** — authenticated Linux (SSH) + Windows facts | 6 | `ssh_collector`, `windows_collector` | `credential_inventory` |
| 14 | **Passive collection** — OT-safe listen-only, no active probes | 0 | `passive_collector` | `passive_facts` |

🆕 = wired into the probe on 2026-08-18 (`os_fingerprint`, `service_enum`). Both
are host-level, cached `deterministic`, merged via `Asset._merge_os_fingerprint`
/ `_merge_service_enum`, and traced.

### `os_fact` (os_fingerprint) shape
`{alive, icmp_reply, observed_ttl, os_guess, confidence, signals{…}}`

### `enrichment` (service_enum) shape
`{open_ports, hostnames, services{port:…}, os_guess, os_confidence, ttl, roles,
management_surfaces, auth_surfaces, weak_legacy, vantage}`

---

## 2. Scan profiles (modes)

| Profile | Ports | Deep branches | Liveness recheck | Intent |
|---------|-------|---------------|------------------|--------|
| **`it`** | IT catalog | `tls, web, smb, db, mcp_ai, snmp` | 1 hour | corporate / IT assets |
| **`iot`** | IoT catalog | `tls, web` | 5 min | consumer / IoT (churny) |
| **`ot`** | — (none) | — (none) | — | operational technology: **passive-only hard stop** (Gate 0) — listens, never actively probes fragile PLCs / industrial gear |

---

## 3. Depth control (stage ceiling)

A job can stop at any depth along:

```
host_discovery → port_scan → service_banner → deep_scan
```

- **discovery only** → asset inventory / liveness map
- **stop after banner** → quick service map
- **deep_scan** → full assessment (OS fingerprint, service enum, TLS/web/smb/db/ai/snmp/udp branches)

---

## 4. Cross-cutting use cases

- **Re-scan / delta / change detection** — cache-backed: deterministic facts are
  collected once per engagement; a re-run only re-probes stale facts and surfaces
  what changed. `os_fingerprint` + `service_enum` are registered `deterministic`
  in `cache.py` so they cache correctly across gate passes.
- **Dynamic routing** (`router.py`) — a service on a non-standard port (e.g. a DB
  on an odd port) is routed to the right deep scanner by banner signature.
- **Hard scope enforcement** — allowlist + exclusions are enforced at the single
  engine entry point (`run_engagement`); out-of-scope hosts are never scanned.
- **Intensity knob** — rate / timeout / port-breadth tuning (light / normal /
  thorough) without changing which branches run.

---

## 5. Where this lives in code

| Concern | File |
|---------|------|
| Pipeline / gate executor | `workflow/workflow_engine.py` (`run_engagement`) |
| Per-host fact model + result merge | `workflow/asset.py` |
| Fact cache + certainty | `workflow/cache.py` |
| Gate preconditions + profile catalogs | `workflow/gates.py` |
| Dynamic Gate-5 routing | `workflow/router.py` |
| Stage ceilings | `workflow/modes.py` |
| The scanners themselves | `scanner/*.py` (`main_scripts/*.py` is a manual-run copy) |

> Note: `service_enum`'s `os_guess` is unprivileged-heuristic and can be `None`;
> `os_fingerprint` (TTL/TCP) is the authoritative OS signal in the pipeline.
