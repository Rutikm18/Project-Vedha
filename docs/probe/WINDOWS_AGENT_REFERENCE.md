# Windows agent - reference

What is installed where, every setting, every command, every state and exit code. For the
how-to see the [operator guide](WINDOWS_AGENT_INSTALL.md); for why it is built this way see
[ADR-0005](../adr/0005-windows-agent-delivery.md). Source of truth is the code; the files
named below are the ones to read when this page and the code disagree.

## 1. What is in the package

Built by `probe/windows/package-zip.ps1`, which also writes two files beside the zip that are **not** inside it:
`vedha-agent-win.zip.sha256` and `vedha-agent-win.release.json` (version, hashes, size; read by the
[S3 publish script](../operations/WINDOWS_AGENT_HOSTING.md)).

`vedha-agent-win.zip`, built by `probe/windows/package-zip.ps1`:

| Item | What it is |
|---|---|
| `vedha-agent\` | the compiled agent (`vedha-agent.exe` and the libraries and runtime beside it). No Python or other software is needed on the customer's machine |
| `install.cmd` | the one command; starts `install.ps1` under Windows PowerShell with the execution policy bypassed for that script only, passing every argument through |
| `install.ps1` | the installer (the manager address and package version are written into it when the zip is built) |
| `uninstall.cmd`, `uninstall.ps1` | removal (a wrapper over `install.ps1 -Uninstall`) |
| `run.cmd` | run the agent in a window without installing (no administrator rights; close the window to stop) |
| `README.txt` | what the customer does (source `probe/windows/README-CUSTOMER.txt`) |
| `ALLOWLIST.txt` | what the customer's security team should allow, with this build's `vedha-agent.exe` SHA-256 and the manager host (source `ALLOWLIST.template.txt`) |
| `SHA256SUMS.txt` | a checksum of every other file; the installer re-checks all of them |

## 2. What the installer puts where

| Path | Holds | Access |
|---|---|---|
| `C:\Program Files\Vedha Agent\` | the compiled agent | Windows default for Program Files (standard users can read and run, not write) |
| `C:\Program Files\Vedha Agent.old\` | the previous install, only while an upgrade is in progress; removed on success, restored on failure | |
| `C:\ProgramData\vedha-agent\` | everything below | **SYSTEM and Administrators only** (`icacls`, set by SID `*S-1-5-18` and `*S-1-5-32-544`, inheritance removed) |
| `...\agent.env` | the agent's settings (section 3). UTF-8, no byte-order mark | |
| `...\state.json` | the agent's identity (agent id, tokens, keys). **Never shared**; never in a support bundle | |
| `...\status.json` | what the agent is doing now (section 5) | |
| `...\spool\` | results waiting to be delivered to the manager | |
| `...\results\` | the archive of every submitted scan payload (never pruned; see the note below) | |
| `...\logs\agent.log` | the agent's log; rotates at 10 MB, 5 old files kept | |
| `...\logs\install-YYYYMMDD-HHMMSS.log` | one log per installer run, with the install token masked | |
| `...\ca-bundle.pem` | the company root certificate, only if `-CaBundle` was used | |
| Scheduled task `VedhaAgent` | see section 6 | |

> **Scan results (finding F-1, fixed in agent package 2.2.2):** the agent keeps a copy of every scan
> payload it submits, for offline review. The installer now points `PROBE_RESULT_DIR` at
> `C:\ProgramData\vedha-agent\results` (inside the locked data folder), and the real-install test fails if a
> `result` folder appears under Program Files. Still true: the archive is **never pruned by the agent**, so
> it grows with every scan; a retention limit is a [pipeline item](../planning/2026-10-07-windows-agent-pipeline.md).
> Setting `PROBE_RESULT_DIR=` (empty) turns the archive off. An older install left a `result` folder under
> Program Files; upgrading with `-Repair` removes it with the old program folder.

## 3. `agent.env` - settings

One `KEY=VALUE` per line. The agent loads it on every start; **an environment variable that is
already set wins over the file**. Written by the installer (do not edit while the agent runs;
`install.cmd -Repair` rewrites it from the existing values plus any options you pass).

| Key | Default written | Meaning |
|---|---|---|
| `PLATFORM_URL` | the address baked into the zip | the manager (https only) |
| `VERIFY_TLS` | `true` | verify the manager's certificate |
| `LICENSE_ENFORCED` | `false` | the compiled build is unsealed; control is on the manager (single-use token, revocation, access expiry) |
| `PROBE_KEEP_RETRYING` | `true` | wait for an unreachable manager instead of exiting (pause grows to 5 minutes) |
| `PROBE_NAME` | `<computername>-probe` (or `-Name`) | the name shown in Fleet |
| `PROBE_NETWORK_SEGMENTS` | the machine's own /24 (or `-Scope`) | the networks this agent may scan, a local ceiling in addition to the engagement's scope |
| `STATE_FILE` | `...\state.json` | identity file |
| `RESULT_SPOOL_DIR` | `...\spool` | delivery queue |
| `PROBE_RESULT_DIR` | `...\results` | archive of submitted scan payloads, inside the locked data folder |
| `PROBE_LOG_FILE` | `...\logs\agent.log` | log file |
| `PROBE_STATUS_FILE` | `...\status.json` | status file |
| `PROBE_INSTALLER_VERSION` | the package version | reported to the manager at enrolment |
| `PROBE_BUILD_DIGEST` | SHA-256 of the installed `vedha-agent.exe` | reported to the manager at enrolment |
| `HTTPS_PROXY` | only with `-Proxy` | web proxy for the agent |
| `PROBE_CA_BUNDLE` | only with `-CaBundle` | company root certificate (.pem) for HTTPS inspection |
| `PROBE_ENROLL_TOKEN` | only with `-Token` | the one-time install token; **removed by the installer once the agent is online** |

Other settings the agent honours (not written by the installer; add a line to use one):

| Key | Effect |
|---|---|
| `PROBE_WS_ENABLED=false` | skip the live (WebSocket) connection and use HTTPS polling only |
| `PROBE_UPDATE_CHECK=off` | do not ask the manager whether a newer agent exists |
| `PROBE_UPDATE_CHECK_INTERVAL_HOURS` | how often (1-168, default 6) |
| `HEARTBEAT_INTERVAL`, `POLL_INTERVAL` | seconds (5-300 and 1-300; defaults 30 and 10) |
| `PROBE_EXPIRED_RETRY_SECS` | how often an access-expired agent re-checks (30-3600, default 300) |
| `LOG_LEVEL`, `PROBE_DEBUG=1` | more logging |
| `NO_PROXY` | hosts that bypass the proxy |
| `VEDHA_AGENT_ENV=<path>` | read this file instead of `%ProgramData%\vedha-agent\agent.env` |

After changing the file: `Stop-ScheduledTask -TaskName VedhaAgent` then `Start-ScheduledTask -TaskName VedhaAgent`.

## 4. Commands

`"C:\Program Files\Vedha Agent\vedha-agent.exe" <command>`

| Command | What it does | Exit code |
|---|---|---|
| `run` | start the agent (what the task runs; also the default with no command) | 0 normal stop; 1 setup error or unexpected crash (recorded in the log and status); 2 gave up on the manager (only when `PROBE_KEEP_RETRYING` is off) |
| `help` | list the commands | 0 |
| `doctor` | check this computer's path to the manager (DNS, proxy, TCP, TLS, HTTP), the data folder, the agent's state and scope; explain each problem and its fix | 0 no check failed; 1 at least one check failed (a warning alone does not fail it) |
| `doctor --preinstall` | only the checks that make sense before installing (what the installer runs) | same |
| `status [--json]` | what the agent is doing now (section 5) | 0 |
| `support-bundle [--out FILE] [--mask-ips]` | write a redacted zip for Vedha support. Holds `doctor.txt`, `status.json`, `system.txt`, `configuration.txt` (settings with secrets masked), `README.txt` and the log. **Never** the identity file, keys, tokens or the result queue | 0 |
| `version` | print the agent version | 0 |
| `hostid` | print this host's identifier | 0 |
| `runtime-check` | the build gate: load every module and library, and exercise the WebSocket, HTTPS and key entry points | 0 / 1 |
| `manifest` | print the agent's capabilities as JSON | 0 |
| any other word | prints the help and exits | 2 |

## 5. `status` and `status.json`

The agent writes `status.json` (atomically, never failing the agent) and `status` reads it.

| State | Meaning |
|---|---|
| `starting` | loading configuration |
| `enrolling` | the install token was accepted; registering with the manager |
| `awaiting-approval` | a person must approve it in Fleet (the pairing code and address are shown) |
| `online` | registered, and the live connection or polling is working |
| `retrying` | cannot reach the manager (or lost the live connection); still trying. `reason` and `remediation` say why and what to do |
| `failed` | the agent stopped (`reason` and `remediation` say why) |
| `not-running` | not a recorded state: `status` shows it when the recorded process no longer exists |

`status` is **the last state the agent recorded**, plus a check that the process is alive. It does
not probe the network. For ground truth use the log and the manager's `GET /agents` (`online`
means a heartbeat in the last 90 seconds).

## 6. The scheduled task

| Setting | Value |
|---|---|
| Name | `VedhaAgent` |
| Action | `"C:\Program Files\Vedha Agent\vedha-agent.exe" run`, working folder the install folder |
| Trigger | at system startup |
| Account | `SYSTEM`, service-account logon, highest privileges |
| On failure | restart every 1 minute, up to 999 times |
| Other | no time limit; start when available; allowed on battery; a second instance is ignored (and the agent also holds a single-instance lock on its identity file) |

`LastTaskResult` in Task Scheduler is the agent's exit code (section 4).

## 7. The installer

`install.cmd [options]` (equivalent to `powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1 [options]`).

| Option | Meaning |
|---|---|
| `-Token vet_...` | the one-time install token |
| `-TokenFile <path>` | read the token from a file (keeps it off the command line) |
| `-Manager <https url>` | override the baked-in manager address |
| `-Scope <cidr[,cidr]>` | networks the agent may scan (default: this machine's own /24) |
| `-Proxy <url>` | web proxy for the agent |
| `-CaBundle <file.pem>` | company root certificate for HTTPS inspection |
| `-Name <text>` | name shown in Fleet |
| `-Repair` | re-apply the installation from this package and re-check it; keeps the agent's identity; needs no token |
| `-Uninstall [-Purge]` | remove the agent; `-Purge` also deletes `C:\ProgramData\vedha-agent` (identity, settings, logs) |
| `-NoWait` | register and start, but do not wait to see it connect |
| `-SkipPreflight` | skip the pre-install connection check (not recommended) |
| `-NoPause` | do not wait for Enter at the end |

Steps (printed as `[1/6]` ... `[6/6]`): check the computer and the package; work out the
settings; check the connection to the manager (`doctor --preinstall`, stops here if it fails,
before anything is changed); install; start; wait up to 2 minutes for `online` or
`awaiting-approval`, then remove the used token from `agent.env`.

| Exit code | Meaning |
|---|---|
| 0 | success, or installed and waiting for approval in Fleet |
| 1 | stopped: a check failed, administrator rights were declined, or an error (nothing was changed, or the previous install was put back) |
| 2 | not Windows |
| 3 | installed, but the agent did not connect yet (the doctor's findings are printed; the agent keeps trying) |

It never changes the customer's firewall, Defender, proxy, certificate store or PowerShell
execution policy (enforced by `probe/tests/test_windows_scripts.py`).

## 8. Source files

| Area | Files |
|---|---|
| Installer, packaging | `probe/windows/install.ps1`, `install.cmd`, `uninstall.*`, `package-zip.ps1`, `run.cmd`, `README-CUSTOMER.txt`, `ALLOWLIST.template.txt` |
| Build | `probe/windows/build-agent-exe.ps1`, `probe/tools/agent_closure.py`, `probe/agent/_closure.py` |
| Agent commands and status | `probe/agent/agent.py`, `diagnostics.py`, `runtime_status.py` |
| Version management | `probe/agent/version.py`, `update_check.py` (see [the design](../design/agent-version-management.md)) |
| Tests | `probe/windows/tests/Test-Install.ps1`, `Test-InstallE2E.ps1`, `probe/tests/test_diagnostics.py`, `test_runtime_gate.py`, `test_windows_scripts.py` (see [the test doc](../testing/windows-agent-ci-and-e2e.md)) |
