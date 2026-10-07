# ADR-0005 — Windows agent delivery: a zip, one command, self-diagnosing

Status: accepted and implemented on `claude/fervent-brahmagupta-o0g44u` (not merged, no pull request open)
Date: 2026-10-07
Related: [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) · [reference](../probe/WINDOWS_AGENT_REFERENCE.md) · [CI and end-to-end test](../testing/windows-agent-ci-and-e2e.md) · [version management](../design/agent-version-management.md) · [bring-up report](../reports/2026-10-07-windows-agent-bringup-report.md) · [pipeline](../planning/2026-10-07-windows-agent-pipeline.md)

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
| D1 | **Deliver a zip you send, plus one command**: `install.cmd -Token vet_…`. The zip's SHA-256 and the token travel by a different channel from the zip. | The owner's choice. A manager-hosted `irm \| iex` needs a signed Windows download route and an agent-authenticated download, neither of which exists; both are in the [pipeline](../planning/2026-10-07-windows-agent-pipeline.md). |
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

## 3. Alternatives considered and rejected

| Option | Why not |
|---|---|
| PyInstaller | Decompiles easily; its bootloader is a common antivirus false-positive signature. |
| Nuitka `--onefile` | Unpacks to `%TEMP%` at every start. |
| MSVC for the Nuitka compile | Out of heap on impacket's generated modules (C1002), even after trimming. |
| `irm \| iex` hosted by the manager now | Needs a signed download route, an authenticated download for an already-enrolled agent, and Authenticode signing first. |
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
- **The manager does not host the Windows package**, and Fleet → Add agent cannot mint a token until a *Linux* release is published (the button is gated on it). Until then a token is minted through the API (see the operator guide).
- The install token is passed on a command line, so a local administrator can see it briefly. It is single-use; `-TokenFile` avoids it.

## 5. Open findings

- **F-1 — scan results are archived in a readable place.** By default the agent writes every submitted scan payload, indefinitely ("never deleted by the probe", `task_runner.py`), to a `result` folder next to its code. On Windows that is `C:\Program Files\Vedha Agent\result`, readable by standard users, and it grows without limit. The installer should relocate it to the locked data folder (`PROBE_RESULT_DIR`), turn it off, or add retention. **A privacy and security decision for the owner; fix before the first customer.**
- **F-2 — local `status` can say ONLINE while the agent is not connected.** The agent records `online` when it registers and when a connection is made (`agent.py`: after registration, on the WebSocket "live connection", on the first HTTP poll). Nothing records it going back down when the WebSocket closes or heartbeats and polls fail later; `status` only checks that the process is alive. So `status` is the *last recorded state*, not a live check. Until fixed, trust the agent log (`WebSocket connected` / `reconnecting`) and the manager's own view (`GET /agents` → `online`, `last_heartbeat`). The fix: record `retrying` on a closed connection or failed heartbeat, and stamp the time of the last successful contact so `status` can say "last heard from the manager N minutes ago". Found while troubleshooting the first field install.
- The `Get-FileHash` failure in the first real install was worked around (the installer hashes with .NET) but its exact cause was not isolated.
- Everything in the guide's *not yet verified* list (clean machine, real enrolment, reboot, UAC, a customer EDR, the `ALLOWLIST.txt` claims).
