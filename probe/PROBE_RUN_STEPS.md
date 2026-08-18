# Running the Probe — Step by Step (perform use cases one by one)

Two ways to run the probe:

- **Path A — Local engine** (works now, no manager): drives `workflow.run_engagement`
  directly via `tools/probe_local_run.py`. Same engine the production probe runs;
  best for LAN validation.
- **Path B — Production** (through the manager): `./probe validate …` dispatches
  each use case to an online probe daemon and scores accuracy. Needs a PAT + an
  enrolled daemon.

Validated 2026-08-18 against `192.168.1.254` on `192.168.1.0/24`.

See `PROBE_USECASES.md` for what each use case does.

---

## Path A — local engine (runs now)

### Step 0 — setup (once per shell)
```bash
cd "…/Vedha/probe"
export PYTHONPATH="$PWD"
PY=.venv/bin/python3
echo "192.168.1.0/24" > /tmp/s.txt          # scope allowlist (must contain the target)
T=192.168.1.254                              # your target
```

The driver is `tools/probe_local_run.py`:
```
tools/probe_local_run.py <target> [profile] [stage] [service_filter]
  profile        : it | iot | ot                       (default it)
  stage          : host_discovery | port_scan | service_banner | deep_scan  ('-' = full)
  service_filter : tls | web | smb | snmp | db | mcp_ai | udp   (isolate one branch)
```
> To scan the full profile port catalog instead of just 22/80/443, set
> `PORT_OVERRIDE = None` at the top of the driver.

### Step 1–4 — the depth ladder (stage ceiling)
```bash
$PY tools/probe_local_run.py $T it host_discovery    # UC1  liveness + MAC/vendor/device
$PY tools/probe_local_run.py $T it port_scan         # UC2  + open TCP ports
$PY tools/probe_local_run.py $T it service_banner    # UC3  + service/version + os_fingerprint
$PY tools/probe_local_run.py $T it deep_scan         # UC4  + service_enum + TLS/web/smb/db/snmp/udp
```
Expected progression (from the validated run):
- UC1 → `alive: true`
- UC3 → `os_fact: {os_guess: "Linux/Unix/macOS", observed_ttl: 64, confidence: 0.5}`
- UC4 → `enrichment: {roles: ["web"], services: [...]}`, `tls_ports: [443]`, `snmp_ports: [161]`, UDP ports discovered

### Step 5 — scan profiles (modes)
```bash
$PY tools/probe_local_run.py $T iot deep_scan        # UC5  IoT profile (tls/web branches, 5-min liveness)
$PY tools/probe_local_run.py $T ot -                 # UC6  OT profile = PASSIVE-ONLY (listens ~60s, no active probes)
```

### Step 6 — isolate ONE deep branch (service filter)
```bash
$PY tools/probe_local_run.py $T it deep_scan tls     # only TLS assessment      (:443/8443…)
$PY tools/probe_local_run.py $T it deep_scan web     # only HTTP assessment     (:80/443/8080…)
$PY tools/probe_local_run.py $T it deep_scan smb     # only SMB assessment      (:445)
$PY tools/probe_local_run.py $T it deep_scan snmp    # only SNMP assessment     (:161)
$PY tools/probe_local_run.py $T it deep_scan db      # only DB fingerprint      (3306/5432/1433/6379…)
$PY tools/probe_local_run.py $T it deep_scan mcp_ai  # only AI/MCP endpoints
$PY tools/probe_local_run.py $T it deep_scan udp     # only UDP scan
```

### Step 7 — credentialed collection (UC13)
Needs real creds — pass them to `run_engagement` (edit the driver's `kw`):
```python
kw["ssh_creds"] = {"user": "U", "key": "~/.ssh/id_rsa"}          # Linux inventory
kw["win_creds"] = {"user": "U"}   # + env WIN_SCAN_PASSWORD       # Windows inventory
```

### Verify accuracy (attacker-side + target-side)
Cross-check any run with the ground-truth commands in
`../main_scripts_probe_actual_function_run.md` (nmap / openssl / `ss -tlnp`).

---

## Path B — production (through the manager)

The "real probe" flow: each use case is dispatched to an **online probe daemon**
and scored for accuracy. Prerequisites (check with `./probe doctor`): a valid
**PAT** and at least one **online agent**.

```bash
export PROBE_MANAGER=http://13.127.147.205:18080

./probe auth login --pat <YOUR_PAT>                # 1. authenticate to the manager
./probe daemon run                                  # 2. (on the probe host) enroll + go online
./probe doctor                                      # 3. verify: auth OK, online_agents >= 1
./probe use-cases                                   # 4. list the manager's use-case IDs

# 5. run the use cases with accuracy validation:
./probe validate --target 192.168.1.254 --scan-profile it --suite full --confirm-authorized
./probe validate --target 192.168.1.254 --suite baseline --dry-run           # preview plan only
./probe validate --target 192.168.1.254 --use-case <ID> --repeat 3 \
                 --ground-truth truth.json --strict-ground-truth              # scored accuracy
```

`--scan-profile`: `it | iot | ot`
`--suite`: `baseline | web | infrastructure | inventory | exposure | full | ot-passive`
`--use-case <ID>`: a specific manager use-case (IDs from `./probe use-cases`)
`--dry-run`: validate + print the plan without scanning
`--repeat N`, `--ground-truth FILE`, `--strict-ground-truth`: repeatability + accuracy scoring

---

## Notes
- **Run from `probe/`** with `PYTHONPATH="$PWD"` and the **venv Python** (`.venv/bin/python3`).
- **Scope is enforced** — the target must be inside `/tmp/s.txt`; out-of-scope hosts are never scanned.
- **A branch that finds nothing** on a host lacking that service is correct (e.g. `smb` on a host without :445).
- Path A limits ports to `22,80,443` for speed — set `PORT_OVERRIDE = None` in the driver for a full-catalog scan.
- Privileged paths (raw SYN, raw ICMP OS-fingerprint) need `sudo`/Linux; unprivileged runs degrade gracefully.
