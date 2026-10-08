# Debugging & Troubleshooting the Vedha Agent (Probe)

> How to raise the agent's log verbosity, where its logs and state are stored on
> each platform, the built-in diagnostic subcommands, how to attach a debugger,
> a symptom→cause→action troubleshooting table, and a dedicated **Windows agent**
> section (install, logs, gotchas).
>
> Companion docs: [`operations/TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) (scanner
> error codes), [`probe/RUNBOOK.md`](../probe/RUNBOOK.md),
> [`probe/step-by-step-run.md`](../probe/step-by-step-run.md),
> [`testing/probe-testing.md`](../testing/probe-testing.md) (two-machine lab).

---

## 1. Turn up log verbosity

The daemon logs to **stderr** (`agent.agent.configure_logging`). Two env knobs:

| Env var | Values | Effect |
|---|---|---|
| `LOG_LEVEL` | `CRITICAL` / `ERROR` / `WARNING` / `INFO` / `DEBUG` | Log level. **Default `INFO`.** An unknown value warns and falls back to `INFO`. |
| `PROBE_DEBUG` | `1` / `true` / `yes` / `on` | Forces `DEBUG`, **un-mutes transport chatter** (`httpx`, `httpcore`, `websockets`, `asyncio`, `urllib3`), and prints `[debug] …` traces. |

- At `INFO` the probe narrates the useful events: *job claimed, use-case resolved,
  scope-guard decisions, "done — N hosts, M open ports", result archived*.
- Routine HTTP polling (every ~10 s) + heartbeat (30 s) is **`DEBUG`-only** so an
  idle probe doesn't look busy and the lines that matter aren't buried.
- `WARNING`/`ERROR` about reaching the manager always surface, even at `INFO`.

```bash
# Docker (compose already wires LOG_LEVEL: ${LOG_LEVEL:-INFO})
LOG_LEVEL=DEBUG docker compose up -d probe      # or: PROBE_DEBUG=1 ...
# Native / from source
PROBE_DEBUG=1 .venv/bin/python -m agent.agent   # foreground, full tracing
```

---

## 2. Where logs are stored (by deployment mode)

The agent does **not** write a log file itself — persistence depends on the
supervisor that runs it:

| Deployment mode | Installed by | Log destination | How to read it | Persisted? |
|---|---|---|---|---|
| **Docker** (default Linux install) | `probe/install.sh` | Container stdout/stderr → Docker logging driver | `docker compose logs -f probe` / `docker logs -f <ctr>` | Until the container/volume is removed (json-file driver) |
| **Native systemd** (Linux) | `agent.service` (`service.py` → `/etc/systemd/system/vedha-agent.service`) | stderr → **journald** | `journalctl -u vedha-agent -f` | Yes (journald retention) |
| **Native launchd** (macOS) | `~/Library/LaunchAgents/com.vedha.agent.plist` | **file:** `~/vedha-agent/logs/agent.log` (via plist `StandardOutPath`/`StandardErrorPath`) | `tail -f ~/vedha-agent/logs/agent.log` | ✅ **Yes — a real file** |
| **Windows scheduled task** | `probe/windows/setup.ps1` | Wrapper redirects `>> agent.log 2>&1` | Open / `Get-Content -Wait` the file | ✅ **Yes — a real file** (appended) |
| **Foreground** (any OS) | `-Foreground` / running `agent.agent` by hand | Console (stderr) | Watch the terminal | No (unless you redirect) |

**Log file paths:** Windows → `C:\ProgramData\vedha-agent\logs\agent.log`;
macOS → `~/vedha-agent/logs/agent.log` (or `<dirname of STATE_FILE>/logs/agent.log`).

> **macOS logging** is written by the launchd plist's `StandardOutPath` /
> `StandardErrorPath` (both point at `agent.log`), and `install()` creates the
> `logs/` dir up front — launchd refuses to spawn a job whose log parent is
> missing. To relocate, set `STATE_FILE` before `connect --service`; the log
> follows the state dir.

### State & result-spool locations (where results/identity persist)

Results are **spooled to disk before upload** (`result_spool.py`), so a crash mid-upload
doesn't lose a finished host — inspect the spool when a scan "finished but no findings arrived."

| Mode | State file (`STATE_FILE`) | Spool dir (`RESULT_SPOOL_DIR`) |
|---|---|---|
| Docker | `/var/lib/vedha-agent/state.json` (state volume) | `/var/lib/vedha-agent/spool` |
| Linux source | `$HOME/vedha-agent/state.json` | `$HOME/vedha-agent/spool` |
| macOS | `~/vedha-agent/state.json` | `~/vedha-agent/spool` (logs → `~/vedha-agent/logs/agent.log`) |
| Windows | `C:\ProgramData\vedha-agent\state.json` | `C:\ProgramData\vedha-agent\spool` |

---

## 3. Built-in diagnostic subcommands (no manager needed)

All under `probe/agent/`. From source use `.venv/bin/python -m agent.<module>`;
a packaged install exposes the operator CLI as `./vedha-agent <cmd>`.

| Command | What it answers | Invocation |
|---|---|---|
| **`doctor`** | Is the host healthy & the manager reachable? Pass/warn/**fail** + remediation per check (DNS, TCP, TLS/cert, clock skew, disk, interfaces, manager auth). | `./vedha-agent doctor` · `python -m agent.setup doctor` |
| **`explain-plan --dry-run`** ⭐ | *Why did/didn't the probe scan port X?* Prints the gate + router **decision table** (which deep scanners run and why). `--dry-run` = **zero packets**. | `python -m agent.explain_plan <target> --profile it --dry-run` |
| **`local-run`** ⭐ | Reproduce the **real pipeline** on one host without the manager, one use-case at a time. | `python -m agent.agent local-run <target> it deep_scan tls,smb` |
| **`self-scan`** | Safe smoke test — scans only this host's own IP (refuses in a container/WSL2). | `python -m agent.self_scan` |
| **`whoami` / `auth status`** | Which identity/PAT is active? | `./vedha-agent whoami` |
| **`scan status`** | State of a dispatched job. | `./vedha-agent scan status <job-id>` |
| **`engagements scope`** | The authoritative allow/exclude scope in force. | `./vedha-agent engagements scope <id>` |

`local-run` port control: `PROBE_LOCAL_PORTS="full"` (whole catalog) or `"445,161"` / `"1-65535"`.

---

## 4. Attaching a real debugger (dev)

**Anti-debug is informational only — it does NOT block startup** (`agent.py:_check_anti_debug`;
comment: *"legitimate operators may run under a profiler"*). So `pdb`, `debugpy`,
`py-spy`, `strace` all work.

```bash
cd probe && .venv/bin/python -m pdb -m agent.agent local-run <target>
# VS Code / remote:
.venv/bin/python -m debugpy --listen 5678 --wait-for-client -m agent.agent local-run <target>
# tests:
.venv/bin/python -m pytest tests/test_task_runner.py -k mytest -s --pdb
```

⚠️ Two startup gates **do** hard-exit (`SystemExit 2`) — but only for the **sealed
binary**: **hardware binding** and **license** (`_startup_gauntlet`). Debug from
**source**, where `LICENSE_ENFORCED=false`, to avoid that friction.

---

## 5. Troubleshooting — symptom → cause → action

| Symptom | Likely cause | Action |
|---|---|---|
| Probe connects but **gets no jobs** | Empty/narrow scope (`PROBE_NETWORK_SEGMENTS`) or not assigned to the engagement | Set a scope CIDR; check `engagements scope`; confirm the probe is assigned in the manager |
| **"Stuck scanning, no results"** | Manager 422-rejects the whole facts payload (run-scoped fact 422) | Check `job.result_scope_rejected`; inspect `DetectionRun.stats["ingest"]` on the manager |
| Scan **"finished but no findings"** | Facts emitted but dropped at the manager ingest gate (silent), OR genuinely clean | Agent emits facts; **manager detects** → check ingest stats first, then `explain-plan` on the probe |
| Endless **WS 403** / auth loops | A **second probe process** sharing `state.json` rotated the token | Ensure one process per state dir (`instance_lock.py`); check for a stray container/task |
| **"Credential revoked"** unexpectedly | Re-pointed to a different manager, or a 5xx misread | Confirm `PLATFORM_URL`; credentials now record their issuer |
| Component `failed` / `degraded` / `partial` | A coverage gap, **not** a clean scan | Read the job `outcome`, `issues`, `scanner_runs`, `error_code` — see [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) |
| Throughput collapses on long scans | AIMD ratchet reading RST-suppression as congestion | Fixed via delivery-rate signal; if seen, capture `PROBE_DEBUG=1` transport logs |
| Silent probe, nothing in logs | Log level too low / logs not persisted for this mode | See §1 (raise level) + §2 (log location for your mode) |

**Probe error codes** (`error_code` on a failed component) — full list with operator
actions is in [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md): `scope_empty`,
`no_authorized_targets`, `targets_missing`, `target_expansion_limit`,
`dependency_missing`, `permission_denied`, `scanner_timeout`,
`dns_resolution_failed`, `connection_failed`, `resource_exhausted`,
`scanner_internal_error`.

**First-response checklist**
1. `doctor` — is the host + manager path healthy?
2. Raise verbosity (`PROBE_DEBUG=1`) and re-read logs for your mode (§2).
3. `explain-plan --dry-run <target>` — is the probe even planning to touch it?
4. `local-run <target>` — does the pipeline reproduce the behavior off the manager?
5. Inspect the **spool dir** for finished-but-unsent results.
6. If facts left the probe but nothing showed up: check the **manager** ingest gate.

---

## 6. Windows agent — install, logs, and debugging

The Windows agent is a **supported, CI-tested target** — `agent-ci.yml` runs the
hardened-agent unit suite on `windows-latest` alongside Linux and macOS.

### 6.1 Install modes

| Mode | Script | Admin? | Use for |
|---|---|---|---|
| **Foreground (source)** | `probe\windows\setup.ps1 -Foreground` | No | Quick test / live console debugging |
| **Persistent task (source)** | `probe\windows\setup.ps1` | **Yes** | Real deployment (survives reboot) |
| **Packaged .exe (customers)** | the zip from CI: `install.cmd -Token vet_...` ([guide](../probe/WINDOWS_AGENT_INSTALL.md)) | Yes | Customer distribution (no Python on host). Diagnose with `vedha-agent.exe status` / `doctor` / `support-bundle` ([reference](../probe/WINDOWS_AGENT_REFERENCE.md)) |
| **Bootstrap one-liner** | `probe\install.ps1` | — | Download-then-run bootstrap |

```powershell
# Test now (no admin): auto-installs Python, venv, deps; runs in the console
powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground -Manager http://<manager> -Scope 192.168.1.0/24

# Install as a reboot-surviving background task (elevated)
powershell -ExecutionPolicy Bypass -File setup.ps1 -Manager http://<manager> -Scope 192.168.1.0/24
```

What `setup.ps1` does automatically: finds or **silently installs Python 3.12**
(winget → official installer), creates `.venv-win`, installs
`requirements-runtime.txt`, **auto-detects the host's /24** as scope, creates the
state/spool/logs dirs, and (elevated) registers scheduled task **`VedhaAgent`**
(runs as `SYSTEM` at startup, auto-restart up to 999×, restart interval 1 min).

### 6.2 Windows logs & state

| Item | Path |
|---|---|
| **Log file** (scheduled-task mode) | `C:\ProgramData\vedha-agent\logs\agent.log` |
| State file | `C:\ProgramData\vedha-agent\state.json` |
| Result spool | `C:\ProgramData\vedha-agent\spool` |
| Task wrapper | `C:\ProgramData\vedha-agent\agent-service.cmd` |

```powershell
Get-Content -Wait 'C:\ProgramData\vedha-agent\logs\agent.log'   # live tail
Get-ScheduledTask -TaskName VedhaAgent | Get-ScheduledTaskInfo  # last run result / next run
Stop-ScheduledTask  -TaskName VedhaAgent                        # stop
Start-ScheduledTask -TaskName VedhaAgent                        # start
```
For verbose Windows logs, set `PROBE_DEBUG=1` before launch (edit the wrapper
`.cmd`, or run `-Foreground` with `$env:PROBE_DEBUG=1`).

### 6.3 Windows gotchas (check these first)

| Gotcha | Symptom | Fix |
|---|---|---|
| **Windows Defender vs impacket** ⭐ | `pip` dies with `[Errno 22] Invalid argument: …DumpNTLMInfo.py`, or the agent is blocked at runtime | Run **elevated** (`setup.cmd` elevates) — it adds `Add-MpPreference` exclusions for the venv, `C:\ProgramData\vedha-agent`, and `python.exe`. Without admin, add the exclusion manually. |
| Persistent task needs **admin** | *"Installing the background task needs Administrator"* | Use `setup.cmd` (elevates) or `-Foreground` for a non-admin test |
| **Empty scope** | Connects, receives **no jobs** | Pass `-Scope <CIDR>` (auto-detect only finds the /24 with a default gateway) |
| **Default manager is a hardcoded IP** (`http://13.127.147.205`) | Talks to the wrong/old manager | Always pass `-Manager <url>` (the Caddy edge on :80) |
| Windows Store Python stub | `python -c` returns nothing / fails | `setup.ps1` skips the stub and installs real Python; ensure real Python 3.10+ |
| Raw sockets / SYN scan | Needs packet capability | The `SYSTEM` scheduled task has it; a non-admin foreground run falls back to connect-based scans |

### 6.4 Will it work? — assessment

**Yes, it should work**, and **yes, it has logs for debugging** — the scheduled-task
mode writes a real, appended `agent.log`, and foreground mode streams to the
console. Windows is exercised in CI on every probe-path PR. The realistic failure
modes are all environmental and covered above — chiefly **Defender/impacket** (run
elevated) and **scope/manager not set**. Source mode runs with
`LICENSE_ENFORCED=false`, so license/HW-bind gates won't get in the way while debugging.

> This assessment is from the install/service code and CI coverage, not a live
> Windows run in this session. Before relying on it in the field, do a
> `setup.ps1 -Foreground` smoke test on a real Windows host and confirm:
> (1) Python auto-installs, (2) the probe registers with the manager (`doctor`),
> (3) a `self-scan` produces a result, (4) `agent.log` fills.

---

## 7. Quick reference

```bash
# Verbosity
PROBE_DEBUG=1 ...            # full DEBUG + transport tracing
LOG_LEVEL=DEBUG ...          # DEBUG without the transport firehose

# Read logs
docker compose logs -f probe                 # Docker
journalctl -u vedha-agent -f                  # Linux systemd
tail -f ~/vedha-agent/logs/agent.log          # macOS launchd
Get-Content -Wait C:\ProgramData\vedha-agent\logs\agent.log   # Windows

# Diagnose (from source: .venv/bin/python -m agent.<module>)
./vedha-agent doctor
python -m agent.explain_plan <target> --dry-run
python -m agent.agent local-run <target> it deep_scan
python -m agent.self_scan
```

> Reminder: always invoke via the **explicit venv python** (`.venv/bin/python -m …`),
> never a bare `pytest`/`python3` — a shell hook can intercept it.
