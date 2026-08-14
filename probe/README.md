# Vedha Probe — collection layer

The probe is the **thin, deployable scanner** that runs inside a client network. It
**collects only** — open ports, banners, TLS/SMB/SNMP posture, web + MCP/AI
fingerprints, device roles, reachability — and ships **raw facts** to the Manager.
It never correlates, matches CVEs, scores risk, or exploits anything. All analysis
(CVE matching, correlation, attack-paths, reporting) lives on the Manager.

- **No exploitation** — no brute-force, credential spraying, payloads, or target modification.
- **Dial-out only** — one outbound HTTPS/WSS connection to the Manager; no inbound listener.
- **Scope-guarded** — every target passes `ScopeGuard` before a packet leaves the host.

## Run it

The Manager owns auth, scope, and which scans run — give the probe only its address.

```bash
# zero-touch pairing (recommended — no token to copy):
./install.sh <manager-ip> --enroll     # prints a pairing code; approve it in the dashboard

# or with a saved PAT in probe.env:
./install.sh <manager-ip>
```

The Manager dispatches a scan by a compact numeric protocol — `{ "uc": 80,
"intensity": 3, targets }` — which the probe maps to exactly one scan pipeline
(`uc` = use-case code, `intensity` = 1 light / 2 standard / 3 deep). See
**[DEPLOYMENT.md](DEPLOYMENT.md)** for the full flow, the use-case code table, and
the firewall/ports the client must open.

## Ship it (protect the IP)

Compile the probe to a sealed native binary (no source, no bytecode), gated by a
vendor-signed, host-locked license:

```bash
./seal-probe.sh                 # → vedha-probe:sealed
```

See **[SEALING.md](SEALING.md)** for the flow, key management, and the honest
threat model.

## Layout

```
probe/
├── scanner/       collectors (ScanResult schema, ScopeGuard, BaseScanner)   ← ≡ main_scripts/
├── main_scripts/  authoritative source for scanner/ (edit here; drift-guarded)
├── workflow/      bounded, fail-isolated per-target sequencing + gates + intensity
├── agent/         manager transport: register/enroll → poll/WS → scan → submit
├── tools/         issue_license.py (vendor licensing), gen_mtls_certs.sh
├── tests/         pytest suite
├── probe          CLI entrypoint (→ agent.cli)
├── install.sh     ← run the probe: LOCAL python, or `--docker` for a hardened container
├── seal-probe.sh  · Dockerfile · Dockerfile.sealed · docker-compose.yml
└── DEPLOYMENT.md · SEALING.md
```

## Develop & test

```bash
python -m venv .venv && ./.venv/bin/pip install -r requirements-runtime.txt
./.venv/bin/python -m pytest tests/ -q          # unit + logic suite
```

`main_scripts/` is the source of truth for the scanners; `scanner/` is kept
byte-identical to it (`tests/test_scanner_parity.py` enforces the drift guard).
Edit in `main_scripts/`, then `./seal-probe.sh` re-syncs and compiles.

For the full platform architecture (probe ↔ manager), see the repo-root
**[ARCHITECTURE.md](../ARCHITECTURE.md)**.
