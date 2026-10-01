# Vedha Agent (Probe) — Install & Run Guide (Linux · macOS · Windows)

> **Customer installs now go through Fleet → Add agent**, which prints one
> command with a single-use install token; the manager serves the signed agent
> itself. See [CUSTOMER_AGENT_INSTALL.md](CUSTOMER_AGENT_INSTALL.md) and the
> operator runbook [AGENT_DISTRIBUTION.md](../operations/AGENT_DISTRIBUTION.md).
> The paths below remain for development, labs and native installs.

> Expert, step-by-step installation for the Vedha probe on every supported OS, with
> the exact commands for each path. The probe is a **thin agent**: it dials *out* to
> the manager, pulls scope-bound jobs, scans the **local** network, and returns
> facts — the manager does detection.
>
> **Companion docs:**
> - [`probe/step-by-step-run.md`](./step-by-step-run.md) — network/firewall model + first scan
> - [`operations/DEBUGGING_THE_AGENT.md`](../operations/DEBUGGING_THE_AGENT.md) — logs, verbosity, troubleshooting
> - [`operations/TROUBLESHOOTING.md`](../operations/TROUBLESHOOTING.md) — scanner error codes
> - [`deployment/aws-deployment.md`](../deployment/aws-deployment.md) — the manager side

---

## 0. Before you start — the one rule + the mental model

> **The probe must run on the same network as the targets you want to scan.**
> It cannot reach a private LAN (`192.168.x.x`, `10.x.x.x`, `172.16.x.x`) from the cloud.

```
   YOUR LAN / DATA CENTER                       CLOUD (or on-prem manager)
 ┌──────────────────────────┐   outbound     ┌───────────────────────┐
 │  [ Vedha Agent ] ────────┼── HTTPS/WS ───►│      [ Manager ]      │
 │        │                 │  (dials OUT)   │  https://<manager>    │
 │        ▼ scans           │                └───────────────────────┘
 │  192.168.x.x targets     │   No inbound to the probe. Ever.
 └──────────────────────────┘
```

- **Probe → Manager**: outbound only (jobs + results). No inbound/port-forward on the probe.
- **Probe → Targets**: local, same network.

---

## 1. Prerequisites (all OS)

| Requirement | Linux | macOS | Windows |
|---|---|---|---|
| **Runtime** | Python 3.8+ **or** Docker | Python 3.10+ (`brew`) | Python 3.10+ (auto-installed by the script) |
| **Egress to manager** | TCP `443` (edge/TLS) or `18080` (direct API) | same | same |
| **Privilege for install** | root for Docker/systemd | admin for launchd | Administrator for the scheduled task |
| **Privilege for scanning** | connect-scan = none; SYN/ICMP = root/`CAP_NET_RAW` | same | SYSTEM task has it; foreground non-admin = connect-scan only |
| **Manager credential** | a probe **PAT** (`vpat_…`) or **enroll-token** (`vet_…`) — see §2 | same | same |

> **Manager URL forms.** Production uses the Caddy **edge**: `https://<manager>` (or `http://<manager>` on port 80). Direct/dev uses the API port: `http://<ip>:18080`. Prefer the edge URL in the field.

---

## 2. Step 0 (do once, on the MANAGER) — mint an enrollment credential

The probe never carries a human credential. On the **manager host** (where the repo/stack runs), mint a probe-scoped token:

```bash
# A probe PAT (vpat_…) — used by the native CLI / local installs
make probe-pat ARGS="--days 90"
# → prints: vpat_XXXXXXXXXXXXXXXXXXXX   (copy it)
```

- **`vpat_…` (PAT)** → for the **native** (`connect`) and **local** install paths.
- **`vet_…` (enroll-token)** → Site-bound, pre-authorized, for **Docker** zero-touch enrollment (mint via the Fleet UI or enrollment API).

Keep the token secret; it enrolls a device. After first enrollment the probe's **Ed25519 keypair is its identity** and the manager issues its device token — the PAT isn't needed again.

---

## 3. Pick your install path

| Path | Best for | Runs as | OS |
|---|---|---|---|
| **Docker** | Production Linux hosts | Hardened container, auto-restart | Linux |
| **Native service** | Bare-metal / VM, no Docker | systemd / launchd / scheduled task | Linux · macOS · Windows |
| **Foreground** | Testing, first scan, debugging | Terminal (Ctrl+C to stop) | all |

---

## 4. Linux

### 4A. Docker (production) — recommended

```bash
# 1. Get the installer (inspect-first is encouraged)
curl -fsSL https://<manager>/probe/install.sh -o install.sh
less install.sh

# 2. Install as a hardened container with zero-touch enrollment
sudo sh install.sh --docker \
  --manager https://<manager> \
  --enroll-token vet_XXXXXXXX
```

What it does: pulls/uses the `vedha-agent` image, creates the state volume
`vedha-agent-state` (identity + license persist here), sets `VERIFY_TLS=true`, and
**self-heals** enrollment (re-enrolls with a fresh key if the manager reports an
orphaned credential).

Useful env knobs (prefix the command): `PROBE_NAME`, `PROBE_NETWORK_SEGMENTS=<CIDR>`
(the scan ceiling — **empty = no jobs**), `PROBE_IMAGE`, `PROBE_CONTAINER`,
`PROBE_MAX_TARGETS` (4096), `PROBE_MAX_JOB_SECONDS` (7200).

```bash
# Manage
docker ps --filter name=vedha-agent
docker logs -f vedha-agent
docker restart vedha-agent
```

> From the repo checkout you can also use the Make targets: `make probe-build` then `make probe-run`.

### 4B. Native systemd (no Docker)

```bash
cd probe
# ensures Python 3.8+ via apt/dnf/pacman, enrolls, installs a systemd unit
sudo sh install.sh connect \
  --manager https://<manager> \
  --pat vpat_XXXXXXXX \
  --service
```

Creates `/etc/systemd/system/vedha-agent.service` (auto-restart with a start-limit
cap so a crash loop isn't read as malware). Manage:

```bash
sudo systemctl status vedha-agent
sudo systemctl restart vedha-agent
journalctl -u vedha-agent -f          # logs
```

Set the scan scope with the env var before install, or in the unit:
`PROBE_NETWORK_SEGMENTS=192.168.1.0/24`.

### 4C. Foreground (dev / first scan)

```bash
cd probe
# bare host:port ⇒ LOCAL mode, runs directly with Python (Ctrl+C to stop)
PROBE_NAME=probe-01 sh install.sh http://<ip>:18080 --local
# or via the brain CLI without installing a service:
sh install.sh connect --manager https://<manager> --pat vpat_XXXXXXXX
```

---

## 5. macOS

macOS runs the **native** agent under launchd. (Docker Desktop works but its NAT
makes scanning the host LAN awkward — prefer native on a Mac that sits on the target LAN.)

```bash
# 1. Python (if missing)
brew install python

# 2. Enroll + install a launchd service (asks for the login keychain/admin as needed)
cd probe
sh install.sh connect \
  --manager https://<manager> \
  --pat vpat_XXXXXXXX \
  --service
```

Creates `~/Library/LaunchAgents/com.vedha.agent.plist` (RunAtLoad, restart on
failure, throttled). **Logs are persisted to a file** (fixed in `service.py`):

```bash
tail -f ~/vedha-agent/logs/agent.log     # live logs
launchctl list | grep com.vedha.agent    # is it loaded?
launchctl unload ~/Library/LaunchAgents/com.vedha.agent.plist   # stop
launchctl load  -w ~/Library/LaunchAgents/com.vedha.agent.plist  # start
```

**Foreground (test) on macOS:**

```bash
cd probe
PROBE_NETWORK_SEGMENTS=192.168.1.0/24 \
  sh install.sh connect --manager https://<manager> --pat vpat_XXXXXXXX
```

> Set the scan scope via `PROBE_NETWORK_SEGMENTS` before install, or the probe
> connects but receives no jobs.

---

## 6. Windows

The Windows agent auto-installs Python and registers a scheduled task. Two source
sub-modes (foreground test vs. persistent), plus a sealed-exe mode.

### 6A. Source install (recommended)

```powershell
cd probe\windows

# Test now — no admin. Auto-installs Python, venv, deps; runs in this console.
powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground `
  -Manager http://<manager> -Scope 192.168.1.0/24

# Install a reboot-surviving background task (run elevated — needed for the task + Defender exclusions)
powershell -ExecutionPolicy Bypass -File setup.ps1 `
  -Manager http://<manager> -Scope 192.168.1.0/24
```

Registers scheduled task **`VedhaAgent`** (runs as `SYSTEM` at startup, auto-restart).
**Logs to a file:** `C:\ProgramData\vedha-agent\logs\agent.log`.

```powershell
Get-Content -Wait 'C:\ProgramData\vedha-agent\logs\agent.log'   # live logs
Get-ScheduledTask -TaskName VedhaAgent | Get-ScheduledTaskInfo  # last/next run
Stop-ScheduledTask  -TaskName VedhaAgent
Start-ScheduledTask -TaskName VedhaAgent
```

> ⚠️ **Windows Defender vs impacket** — if `pip` dies with `[Errno 22] …DumpNTLMInfo.py`
> or the agent is blocked, run **elevated**; `setup.ps1` then auto-adds Defender
> exclusions for the venv, `C:\ProgramData\vedha-agent`, and `python.exe`.
> Also: pass a real `-Manager` (the default is a baked-in IP) and a `-Scope`.

### 6B. Sealed-exe mode (no Python on the host)

```powershell
cd probe\windows
powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1   # build the .exe (on a build box)
powershell -ExecutionPolicy Bypass -File install.ps1           # install the packaged agent
```

---

## 7. Verify the install (all OS)

Run these after install — in order — to confirm health before trusting a scan:

```bash
# 1. Host + manager reachability, TLS, clock, disk, auth  → pass/warn/FAIL + fix
sh install.sh doctor --manager https://<manager>          # Linux/macOS
#   Windows:  .venv-win\Scripts\python -m agent.setup doctor

# 2. Safe smoke scan of THIS host only (no manager needed)
cd probe && .venv/bin/python -m agent.self_scan           # Linux/macOS

# 3. See what the probe WOULD scan against a target, zero packets
python -m agent.explain_plan <target> --dry-run
```

Then, in the **dashboard → Fleet**, the probe shows **green / online**, and a
**Network Discovery** scan against a known-up target (`nc -vz <host> 80`) completes
Queued → Scanning → **Complete** with open ports. (Full walk-through:
[`step-by-step-run.md`](./step-by-step-run.md).)

---

## 8. Autostart / run-as-service — recap

| OS | Mechanism | Name | Log file / command |
|---|---|---|---|
| Linux (Docker) | container restart policy | `vedha-agent` | `docker logs -f vedha-agent` |
| Linux (native) | systemd | `vedha-agent.service` | `journalctl -u vedha-agent -f` |
| macOS | launchd | `com.vedha.agent` | `~/vedha-agent/logs/agent.log` |
| Windows | Scheduled Task | `VedhaAgent` | `C:\ProgramData\vedha-agent\logs\agent.log` |

---

## 9. Logs & debugging (quick reference)

Raise verbosity anywhere with `PROBE_DEBUG=1` (full DEBUG + transport tracing) or
`LOG_LEVEL=DEBUG`. Where logs live:

```bash
docker compose logs -f probe                                   # Docker
journalctl -u vedha-agent -f                                    # Linux systemd
tail -f ~/vedha-agent/logs/agent.log                           # macOS launchd
Get-Content -Wait C:\ProgramData\vedha-agent\logs\agent.log    # Windows
```

Full guide (diagnostic subcommands, attaching a debugger, symptom→fix table):
[`operations/DEBUGGING_THE_AGENT.md`](../operations/DEBUGGING_THE_AGENT.md).

---

## 10. Update / upgrade

| OS / mode | Update command |
|---|---|
| Linux Docker | `sudo sh install.sh --docker --manager https://<manager>` (re-pulls the image) |
| Linux/macOS native | `git pull` in the checkout, then `sudo systemctl restart vedha-agent` / reload launchd |
| Windows source | `powershell -File setup.ps1 -Update -Manager http://<manager> -Scope <CIDR>` (git-pulls first) |

---

## 11. Uninstall

```bash
# Linux Docker (add PROBE_PURGE=true to also delete identity/license volume)
sudo sh install.sh --docker --uninstall
sudo PROBE_PURGE=true sh install.sh --docker --uninstall

# Linux/macOS native
python -m agent.setup uninstall          # removes systemd unit / launchd plist

# Windows
schtasks /Delete /TN VedhaAgent /F
#   or: powershell -File probe\windows\uninstall.ps1
```

---

## 12. Install-time troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `python3 not found` (Linux) | No interpreter | Script auto-installs via apt/dnf/pacman; or `sudo apt-get install -y python3 python3-venv` |
| `pip [Errno 22] …DumpNTLMInfo.py` (Windows) | Defender quarantines impacket | Re-run `setup.ps1` **elevated** (auto-adds exclusions) |
| Probe online but **no jobs** | Empty scope | Set `PROBE_NETWORK_SEGMENTS=<CIDR>` (Linux/macOS) / `-Scope <CIDR>` (Windows) |
| Enrollment loops / rejected | Stale/duplicate identity | Remove the stale probe in **Fleet**, then re-enroll (Docker self-heals up to 6×) |
| `connection refused` to manager | Egress blocked / wrong URL | Open TCP 443 (or 18080); verify `--manager`; `nc -vz <manager> 443` |
| Endless WebSocket **403** | Two processes share one `state.json` | Run **one** probe per state dir |
| Scan runs but SYN/ICMP fails | No raw-socket privilege | Run with root / `CAP_NET_RAW`, or accept connect-scan |

> More scanner-side codes (`scope_empty`, `dependency_missing`, `permission_denied`,
> `scanner_timeout`, …) with operator actions:
> [`operations/TROUBLESHOOTING.md`](../operations/TROUBLESHOOTING.md).
