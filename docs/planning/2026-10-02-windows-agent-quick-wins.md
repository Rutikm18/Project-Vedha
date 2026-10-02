# Windows-first agent: quick wins now, everything else in the pipeline

Date: 2026-10-02 · Status: **approach for review — not implemented**
Builds on: [agent install approach §10](2026-10-01-agent-install-approach.md#10-decisions-2-oct-2026-and-what-phase-1-built) (Linux/Docker path, built on `feat/agent-install`)

## Why this note

Most first customers will install the agent on **Windows**. The owner's goals:

- what we hand over contains **only the code the agent needs, compiled** (no readable source);
- **one install command**;
- the agent **registers and enrols itself** in Fleet;
- **expiry is set from Fleet**.

This note picks the smallest set of changes that gets there on Windows, and parks the rest.

## What exists today (Windows)

| Piece | State | Problem |
|---|---|---|
| `probe/windows/setup.ps1` (source mode) | Works; the owner has run it | Ships **readable Python source**; auto-installs Python; adds a Defender exclusion for **every** `python.exe`; licence off; defaults to the old `http://13.127.147.205` |
| `build-agent-exe.ps1` + `install.ps1` + `package-zip.ps1` (exe mode) | Builds an exe with PyInstaller (decompiles easily) or Nuitka | `install.ps1` never sets `LICENSE_ENFORCED=false`, and the unsealed default is **true**, so the exe stops with "licence required". Defaults to the old HTTP IP. No token, so manual code approval |
| Delivery | A zip sent by hand | No link from Fleet, no integrity check |

## Quick wins (proposed for now, in order)

### QW1: compiled, minimal Windows agent

- **Build with Nuitka in `--standalone` folder mode, not `--onefile`.** A one-file exe unpacks itself to `%TEMP%` on every start, which endpoint tools treat as a dropper. A folder installed under `C:\Program Files\Vedha Agent\` is quieter and starts faster.
- **Include only `agent/`, `scanner/` and `workflow/`** (about 1.7 MB of source) plus `httpx`, `websockets`, `cryptography`, `impacket`, `ldap3` and `dnspython`. Never `tests/`, `main_scripts/`, `Capabilties/`, `cve/`, `tools/`, docs or `.env` files.
  - Strip docstrings and asserts (as the sealed Linux build already does).
  - A build-time check fails if any `.py` or `.pyc` file ends up in the output.
- **Build in CI on a GitHub `windows-latest` runner** (Nuitka needs MSVC; it can't build Windows binaries from a Mac). The CI build is reproducible and never needs a developer laptop.
- **Licence:** compiled but unsealed, with `LICENSE_ENFORCED=false` set by the installer. Control comes from the manager: the single-use token, revocation, and expiry (QW4). The sealed per-host licence moves to the pipeline ("licence issued at enrolment").

### QW2: same signed release, one PowerShell command from Fleet

- `scripts/agent_release.py` adds a `windows-amd64` artifact (the zipped folder) to the existing signed manifest. The manager serves it at `GET /agent/download/windows-amd64`, which needs a live install token, the same rule as the Linux image.
- Fleet → Add agent gets an OS switch. For Windows it prints one command to run in an **elevated** PowerShell:
  ```powershell
  & ([scriptblock]::Create((irm https://api.vedhasec.com/agent/install.ps1))) -Manager https://api.vedhasec.com -Token vet_…
  ```
  It also offers "download, read, run" and a "run this in PowerShell (Admin)" hint.

### QW3: `install.ps1` that checks, never installs

1. **Preflight, each failure with its fix:**
   - Windows 10/11 or Server 2016+, 64-bit, running as admin;
   - TLS 1.2 forced, because PowerShell 5.1 defaults lower;
   - the manager's `/health` is reachable;
   - the clock is within 5 minutes.
2. **Download** the zip with the token sent in a header. Check its **SHA-256 against the manifest** fetched from the manager over HTTPS.
   - Windows PowerShell can't verify Ed25519 signatures, so for now integrity rests on the checksum plus the manager's HTTPS certificate.
   - Authenticode signing comes in the pipeline; then `Get-AuthenticodeSignature` is checked as well.
3. **Unpack** to `C:\Program Files\Vedha Agent\`. State, logs and spool go under `C:\ProgramData\vedha-agent\`, with an access list limited to SYSTEM and Administrators.
4. **Run as SYSTEM** through a scheduled task that starts at boot, as today, but:
   - the restart cap is 10 instead of 999;
   - the log file rotates (10 MB × 5);
   - settings go in a file the task's launcher reads, never on a command line other users can see.
5. **No auto-installs:** no Python, no Npcap, no Defender exclusion for `python.exe`. If the customer's endpoint tool quarantines the agent, the installer says exactly which path to allow-list, as a step for their security team.
6. **`--proxy` and `--ca-bundle`**, like Linux. PowerShell uses the system proxy, but the agent needs `HTTPS_PROXY` set explicitly.
7. `install.ps1 -Uninstall`, with `-Purge` to also delete the agent's identity.

### QW4: expiry set from Fleet (enforced by the manager)

- **Install command lifetime:** pick 1 h, 24 h or 7 days when generating, instead of the fixed 24 h.
- **Agent access expiry:** a new optional `agents.access_expires_at` column (migration), set and changed from the agent row in Fleet. Its default is the POC plan's end date when the engagement is on a POC plan.
- After expiry the manager:
  - refuses heartbeats, jobs and token refreshes with "agent access expired";
  - shows **expired** in Fleet and the portal.

  Extending the date restores the agent with no reinstall. Running scans finish; no new ones start.
- Expiry is enforced only on the server, so changing the customer's clock or patching the binary doesn't get around it.

### QW5: retire the risky Windows paths for customers

- **`setup.ps1`** (source mode): kept for the lab only. It gets a banner saying "not for customer sites", and its Defender exclusion for every `python.exe` becomes opt-in.
- **Defaults:** remove the old `http://13.127.147.205` from all Windows scripts and docs.

## Failure points of this quick path and how each is handled

| # | Failure | Handling now | Later (pipeline) |
|---|---|---|---|
| W1 | Defender / endpoint tools flag an **unsigned** network scanner; impacket's code is a known detection signature | Folder build (no `%TEMP%` unpacking); installed in Program Files; installer names the exact path to allow-list | Authenticode signing (EV certificate); submit the build to Microsoft as a false positive; optionally a Windows build without impacket |
| W2 | **SmartScreen** | Avoided: PowerShell downloads don't carry the "downloaded from the internet" mark, so SmartScreen doesn't apply | Signed MSI |
| W3 | Execution policy / Constrained Language Mode / AppLocker or WDAC blocks the script or the program | The one-line command doesn't depend on execution policy; preflight detects Constrained Language Mode and says so | Signed MSI for Intune / GPO deployment |
| W4 | No raw sockets without Npcap, so no SYN or OS fingerprinting | Connect scans (already how Windows runs); Fleet shows "connect-scan only" | Npcap only with its paid OEM licence, or a Linux VM for full capability |
| W5 | Laptop or workstation sleeps or changes networks | Requirements say a server or VM; preflight warns on battery power | Hyper-V / VMware virtual appliance |
| W6 | System proxy not used by the agent | `-Proxy` is written into the agent's config; the system proxy is detected and offered | Read the proxy from WinHTTP automatically |
| W7 | TLS inspection | `-CaBundle` (the WebSocket fix is already on the branch) | Read the corporate root from the Windows certificate store |
| W8 | Compiled code can still be studied by a determined admin | Accepted: compiling removes source, bytecode and docstrings; the valuable detection logic runs on the manager | Sealed build + licence at enrolment; Nuitka commercial constant protection |
| W9 | No Ed25519 in Windows PowerShell | Checksum over the manager's HTTPS | Authenticode signature checked by the installer |
| W10 | Old Windows (7, 2012 R2) or 32-bit | Preflight refuses with the reason | — |
| W11 | Hardware binding breaks on VM migration or NIC change | Not used (no host binding on the unsealed build) | Bind the licence to the enrolled identity, not the MAC |

## Pipeline (not now)

1. Authenticode-signed builds + signed **MSI** (Intune / GPO).
2. Real **Windows service** instead of a scheduled task.
3. **Sealed** build with the licence issued at enrolment.
4. **Linux native binary** (systemd), next to Docker.
5. **macOS**: notarized `.pkg`, system service (LaunchDaemon).
6. **Signed auto-update**; version shown in Fleet; support bundle.
7. Npcap OEM licence for SYN scans on Windows.
8. Windows on ARM.
9. Virtual appliance.

## Effort (quick wins)

| QW | Effort |
|---|---|
| QW1 compiled minimal build + CI job + "no source" check | ~1 day |
| QW2 Windows artifact in the release + download route + Fleet OS switch | ~0.5 day |
| QW3 `install.ps1` | ~1 day |
| QW4 expiry (migration, manager enforcement, Fleet controls) | ~1 day |
| QW5 retire risky defaults | ~0.5 hour |

Testing:
- Unit tests for the routes and for expiry.
- `install.ps1` run with Pester on the Windows CI runner.
- One real install on a Windows 10/11 or Server VM, which needs the owner or a Windows CI runner. The Mac can't run Windows.
