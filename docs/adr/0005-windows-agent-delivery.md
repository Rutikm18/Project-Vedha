# ADR-0005 — Windows agent delivery: a zip, one command, self-diagnosing

Status: accepted and implemented on `claude/fervent-brahmagupta-o0g44u` ([PR #10](https://github.com/Rutikm18/Project-Vedha/pull/10), open, not merged)
Date: 2026-10-07
Related: [S3 hosting](../operations/WINDOWS_AGENT_HOSTING.md) · [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) · [reference](../probe/WINDOWS_AGENT_REFERENCE.md) · [CI and end-to-end test](../testing/windows-agent-ci-and-e2e.md) · [version management](../design/agent-version-management.md) · [bring-up report](../reports/2026-10-07-windows-agent-bringup-report.md) · [pipeline](../planning/2026-10-07-windows-agent-pipeline.md)

## 1. Context

Most first customers run Windows. The owner's first achievable goal (7 Oct 2026):

> Send the final Windows agent to a client with **one command to install**, **all
> dependencies included**, and an **auto-troubleshooting mechanism**. Everything else
> stays in the pipeline.

Behind that, four requirements the owner set: (1) one command only; (2) endpoint-security
products should not flag it; (3) the main code stays secure; (4) enrolment and management
are automatic and easy.

Before this work the Windows path was a source install (`setup.ps1`: installs Python,
readable source, Defender exclusions) and an unrun compiled-build script. The Linux path
(Fleet → Add agent → signed Docker image) already existed and was left alone.

## 2. Decisions

| # | Decision | Why |
|---|---|---|
| D1 | **Deliver a zip you send, plus one command**: `install.cmd -Token vet_…`. The zip's SHA-256 and the token travel by a different channel from the zip. | The owner's choice. A manager-hosted `irm \| iex` needs a signed Windows download route and an agent-authenticated download, neither of which exists; both are in the [pipeline](../planning/2026-10-07-windows-agent-pipeline.md). **Extended by D14**: the same package can also be installed with one command from an S3-hosted address. |
| D2 | **Build with Nuitka in `--standalone` folder mode**, closure-only (the 77 modules the agent imports), compiled with **MinGW-w64 gcc**, in GitHub Actions on `windows-latest`. Not `--onefile`. | A one-file exe unpacks to `%TEMP%` on every start, which endpoint tools treat as a dropper. MSVC ran out of heap (error C1002) compiling impacket's generated RPC modules; MinGW did not. The build ships no source, bytecode or docstrings and CI fails if any appear. |
| D3 | **Run as a Scheduled Task**: account SYSTEM, trigger at startup, restart every 1 minute up to 999 times, one instance. Not a Windows service. | No service wrapper to write or sign. A real service / MSI is a pipeline item. |
| D4 | **Layout and permissions**: program in `C:\Program Files\Vedha Agent`; settings, identity, spool and logs in `C:\ProgramData\vedha-agent`, restricted by `icacls` to SYSTEM and Administrators (by SID, so it works on any language of Windows). | Standard users must not read the agent's identity or settings. See open finding F-1 for one folder this does not yet cover. |
| D5 | **The installer checks before it changes anything** and cleans up after: it re-launches itself as administrator, verifies every file against `SHA256SUMS.txt`, runs the agent's own `doctor --preinstall` against the manager, backs up and restores a previous install on failure, waits until the agent reports `online` or shows the pairing code, then removes the used token from disk. It is ASCII-only and runs on Windows PowerShell 5.1. | A failed install must say what is wrong and leave the machine as it was. |
| D6 | **The installer and agent never change the customer's firewall, Defender, proxy, certificate store or PowerShell execution policy.** A unit test enforces it. | The owner chose "diagnose, explain and safe self-heal only". Changing security settings on a customer's machine is not ours to do. |
| D7 | **Auto-troubleshooting is three commands plus a status file**: `doctor` (DNS → proxy → TCP → TLS → HTTP to the manager, names a TLS-inspection issuer), `status` (what it is doing now), `support-bundle` (a redacted zip). The agent writes `status.json` (`starting`, `enrolling`, `awaiting-approval`, `online`, `retrying`, `failed`), a rotating log (10 MB × 5), and records any crash. | A Scheduled Task has no console, so without these a client has nothing to read or send. |
| D8 | **The support bundle is emailed by the client**; nothing is uploaded automatically. It never contains the identity file, keys, tokens or the result queue. | The owner's choice for this phase. |
| D9 | **On Windows the agent keeps retrying an unreachable manager** (`PROBE_KEEP_RETRYING=true`, written by the installer; pause grows to 5 minutes). Linux/Docker keep the old behaviour (exit with a diagnosis; the container restart policy supervises). | A reboot or a network blip must not leave a Windows agent stopped. Found by the first real install. Opt-in so the Linux behaviour did not change without the owner's say. |
| D10 | **The agent has its own version number** (`probe/agent/version.py`, bumped by hand, checked by CI), separate from the platform release in `VERSION`. See [version management](../design/agent-version-management.md). | A manager release that does not touch the agent must not look like an agent update. |
| D11 | **The manager is not changed to serve Windows.** The install token is the existing single-use, engagement-bound `vet_…` token from Fleet. | Keeps this phase to one repo area. Consequence: see D13. |
| D12 | **Licence**: the compiled build is unsealed with `LICENSE_ENFORCED=false`, written by the installer. Control is on the manager side (single-use token, revocation, access expiry). | As decided in the [quick-wins note](../planning/2026-10-02-windows-agent-quick-wins.md). A sealed, per-host licence is in the pipeline. |
| D13 | **Stance on endpoint-security products: be trusted, not invisible.** No evasion. The means: a folder build in Program Files (no `%TEMP%` unpacking), an `ALLOWLIST.txt` in the zip with this build's hash and the network it uses, no Defender exclusions, honest documentation that scans look like a scanner. Code signing is the real fix and is in the pipeline. | The owner's second requirement, reframed from "must not be detected" to "must not be falsely blocked". Evading detection by security tools is something we do not build. |
| D14 | **One command from an S3 + CloudFront address** (added 8 Oct 2026): `get.ps1` downloads the package, **requires the package version and SHA-256 to be part of the command** (so the bucket is not trusted), unpacks into an administrator-only folder, runs the installer and deletes the files. It must be run from an Administrator PowerShell and never raises its own rights. A publish script uploads versions immutably and prints the customer's command; a CloudFormation template creates a private bucket read only through CloudFront. See [the hosting guide](../operations/WINDOWS_AGENT_HOSTING.md). | The owner asked for a single pasted command, hosted on S3. Pinning the hash in the command makes the download trustworthy without trusting AWS or the network; refusing to self-elevate avoids the privilege-escalation pattern of an installer that re-launches itself as administrator from a writable folder. Caveat: a "download and run" command is a pattern some endpoint products flag, so the zip route stays supported and a "read it first" form is documented. |

## 3. Alternatives considered and rejected

| Option | Why not |
|---|---|
| PyInstaller | Decompiles easily; its bootloader is a common antivirus false-positive signature. |
| Nuitka `--onefile` | Unpacks to `%TEMP%` at every start. |
| MSVC for the Nuitka compile | Out of heap on impacket's generated modules (C1002), even after trimming. |
| `irm \| iex` hosted **by the manager** | Needs a signed download route and an authenticated download for an already-enrolled agent. (Hosting on S3 with a pinned hash, D14, was built instead.) |
| Windows service / MSI now | More moving parts than the first goal needs. |
| Automatic fixing of firewall, proxy or certificates | Out of bounds (D6). |
| Uploading the support bundle automatically | The owner chose email for now (D8). |
| Auto-update in this phase | Version management only; the download and apply path is a pipeline item. |

## 4. Consequences

**Good**
- A customer gets one command, no dependencies, and a message that names the problem and the fix.
- The whole thing is tested on a real Windows runner on every change (22 install checks; see the [CI doc](../testing/windows-agent-ci-and-e2e.md)).
- The agent no longer fails silently under a headless host.

**Costs and limits**
- The build is **unsigned**: SmartScreen and some endpoint products warn or block until it is signed.
- Windows scans are **TCP-connect scans** (no raw sockets without Npcap): no SYN scan, OS fingerprinting or ARP discovery.
- **No automatic update**: a new version means sending a new zip and re-running `install.cmd`.
- **The manager does not host the Windows package** (S3 does, D14), and Fleet → Add agent cannot mint a token until a *Linux* release is published (the button is gated on it). Until then a token is minted through the API (see the operator guide).
- The install token is passed on a command line, so a local administrator can see it briefly. It is single-use; `-TokenFile` avoids it.

## 5. Open findings

- **F-1 - scan results were archived in a user-readable place. Fixed in agent package 2.2.2.** By default the agent writes every submitted scan payload, indefinitely ("never deleted by the probe", `task_runner.py`), to a `result` folder next to its code, which on Windows was `C:\Program Files\Vedha Agent\result`, readable by standard users. The installer now sets `PROBE_RESULT_DIR` to the locked data folder (`...\vedha-agent\results`) and the real-install test fails if a result folder appears under Program Files. **Still open:** the archive has no retention limit, so it grows with every scan ([pipeline](../planning/2026-10-07-windows-agent-pipeline.md)).
- **F-2 - local `status` could say ONLINE while the agent was not connected. Fixed in `e854f03` (agent 2.2.1).** The agent recorded `online` when it registered or connected and nothing recorded it going back down, so `status` was the last recorded state, not a live check. A closed or unavailable live connection, or an unreachable manager during polling, is now recorded as `retrying` (with a reason and a fix) and back to `online` when contact returns. Still true: `status` shows what the agent last recorded, not a probe of the network; the log and the manager's `GET /agents` (`online`, `last_heartbeat`) are the ground truth. Found while troubleshooting the first field install, together with F-3.
- **F-3 - the compiled agent could not open its live connection. Fixed in `e854f03` (agent 2.2.1).** `websockets` loads `websockets.asyncio.client` lazily by name, which Nuitka cannot follow, so the agent registered and then logged `No module named 'websockets.asyncio'` forever, never heartbeating; and the old `runtime-check` only imported the top-level package. Now: the build includes the whole `websockets` package, `runtime-check` exercises the real entry points (a WebSocket connect to a closed local port, an HTTPS request, the identity keys) and a test proves it fails a broken build, and the agent falls back to HTTP polling when the WebSocket library cannot load. Version 2.2.0 reached a real machine with this defect, which is why the version moved to 2.2.1.
- **F-4 - `os.kill(pid, 0)` is not an existence check on Windows. Fixed in agent 2.2.3.** On Windows, signal 0 is `CTRL_C_EVENT`, so `instance_lock._holder_hint` (called when a second agent finds the lock taken) would send Ctrl+C to the running agent's console group. Found because the `test (windows-latest)` job ended with `KeyboardInterrupt` after all 398 tests passed (it had done so on every earlier run, hidden behind two other failures). `_holder_hint` now uses `runtime_status.process_alive`, which has a Windows branch, and a test fails if any agent module calls `os.kill(pid, 0)`.
- **F-5 - `python -m agent.setup doctor` crashed on a cp1252 Windows console. Fixed in agent 2.2.4.** The report contains an arrow (`→`) that a cp1252 console cannot encode, so the command died with `UnicodeEncodeError`. `agent.agent` already forced UTF-8 output; `agent.setup` (`doctor`, `connect`) did not. It surfaced only when the Windows unit-test step stopped failing early and the `doctor smoke` step ran on Windows for the first time. `agent.setup` now makes its output encoding-proof, and a test runs `doctor` with a cp1252 console encoding.
- The `Get-FileHash` failure in the first real install was worked around (the installer hashes with .NET) but its exact cause was not isolated.
- Everything in the guide's *not yet verified* list (clean machine, real enrolment, reboot, UAC, a customer EDR, the `ALLOWLIST.txt` claims).
