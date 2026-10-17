# Vedha Agent — Windows (simple, git-based)

> Starting, running, updating and troubleshooting an installed agent: [docs/operations/WINDOWS_AGENT_MANAGEMENT.md](../../docs/operations/WINDOWS_AGENT_MANAGEMENT.md).

Run the probe on a **Windows** machine straight from the repo — no Docker, no exe
build, no zip. The customer clones/pulls from GitHub and runs one script that
sets up a venv, installs dependencies, and starts the agent.

> Native (not Docker) on purpose: Docker on Windows runs Linux containers behind
> WSL2 NAT and would scan the *virtual* network, not the real LAN. See
> `../../probe_docker_customer_env.md` Part 4.

---

## One command (recommended): signed release from your manager

In the Vedha portal open **Fleet → Add agent**, pick **Windows**, and copy the command. It carries
your manager address and a single-use install token.

PowerShell, from an **elevated** prompt (Run as administrator):
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm 'https://manager.example.com/agent/install.ps1'))) -Manager 'https://manager.example.com' -Token 'vet_...'"
```
or from cmd.exe (asks for administrator rights itself):
```bat
curl.exe --proto =https --tlsv1.2 -fsSL "https://manager.example.com/agent/install.cmd" -o "%TEMP%\vedha-install.cmd" && "%TEMP%\vedha-install.cmd" "https://manager.example.com" "vet_..."
```

The installer (`install-remote.ps1`, served as `/agent/install.ps1`) first verifies the release
manifest's ECDSA P-256 signature against the key baked into the script, then downloads the package
with your token and checks its size and SHA-256 against that signed manifest, checks the Authenticode
signature when the release pins a certificate, unpacks it (refusing any path that escapes the target
folder) and runs the packaged `install.ps1` (the same installer as in the hand-delivered ZIP: package
checksums, connection check, locked data folder, Scheduled Task, wait-for-connect, diagnostics). It stops at
the first mismatch and installs nothing. The token goes only into the agent's settings file inside the
locked data folder and is removed once the agent is online. The manager must be an `https://` address.

`C:\ProgramData\vedha-agent` is restricted to SYSTEM and Administrators (it holds the agent's
identity key). The installer and uninstaller stay in `C:\ProgramData\vedha-agent\tools`.

Update: run the same command again with a fresh token. Remove: `C:\ProgramData\vedha-agent\tools\uninstall.cmd`
(add `-Purge` to also delete the identity and logs). Audit a release without installing it: add `-VerifyOnly`
to the PowerShell command (no administrator rights needed).

---

## The git-based customer commands (on the target Windows machine)

**Prerequisites:** none pre-installed is required — `setup.ps1` **auto-installs
Python** if it's missing (winget or the official installer). Use
[Git](https://git-scm.com/download/win) to clone, or just download the repo ZIP.
Needs internet on first run (to fetch Python + Python deps).

**First time:**
```bat
git clone https://github.com/Rutikm18/Project-Vedha.git
cd Project-Vedha\probe\windows
setup.cmd
```
`setup.cmd` asks for admin (UAC), then installs a background task **VedhaAgent**
that connects to the manager and survives reboot.

**Just test it (no admin, runs in a window):**
```bat
powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground
```

**Update later:**
```bat
git pull
setup.cmd
```
(or one step: `powershell -ExecutionPolicy Bypass -File setup.ps1 -Update`)

**Remove:** `uninstall.cmd` (Run as administrator; add `-Purge` to wipe identity).

Point at a different manager or scope:
```bat
powershell -ExecutionPolicy Bypass -File setup.ps1 -Manager https://manager.example.com -Scope 10.0.0.0/24
```

---

## What the target machine needs

| Need | What | Notes |
|---|---|---|
| Git | git-scm.com | for `clone` / `pull` |
| Python | 3.10+ | `setup.ps1` builds a private venv from it |
| Deps | auto-installed | `httpx websockets cryptography impacket ldap3 dnspython` (from `requirements-runtime.txt`) |
| Env | auto-set by the script | `PLATFORM_URL`, `PROBE_NAME`, `PROBE_NETWORK_SEGMENTS`, `STATE_FILE`, `RESULT_SPOOL_DIR` |
| Firewall | outbound only | allow this PC → your Vedha manager over HTTPS (443, outbound only; no inbound) |

State/identity/logs live under `C:\ProgramData\vedha-agent\`.

**Per-machine:** each machine enrolls its own identity — do **not** copy
`state.json` between hosts. Scope auto-detects that host's `/24`.

---

## Files

| File | Role |
|---|---|
| `setup.ps1` / `setup.cmd` | **the automated installer** (venv + deps + run/register) |
| `install-remote.ps1` / `install-remote.cmd` | **one-command signed install** (stamped with the release key and served by the manager as `/agent/install.ps1` and `/agent/install.cmd`) |
| `install.ps1` / `install.cmd` | install from an unpacked package (what the one-command installer runs after verifying it) |
| `uninstall.ps1` / `uninstall.cmd` | remove the background task |
| `probe.env.template` | documents the config the script sets |
| `python-env.ps1` | which Python the build may use (3.10-3.12); shared by `build-agent-exe.ps1` and `publish-release.ps1` |
| `README-CUSTOMER.txt` | short in-repo customer note |

**Advanced (optional, for sealed distribution to untrusted customers):**
`build-agent-exe.ps1` (Nuitka, agent code only, no readable source) + `package-zip.ps1` build a `vedha-agent\` folder with `vedha-agent.exe` and a
ZIP (see the exe launchers `run.cmd` / `install.ps1`). Not needed for the git flow
above.

---

## When the build stops

`publish-release.ps1` and `build-agent-exe.ps1` run on **your** Windows PC. Two failures account for
most stops. Both are checked or explained by the scripts now, but the fix is on your machine.

**`FATAL: Error, cannot use '--mingw64' on Python version 3.13 or higher.`**
The build environment (`probe\windows\.venv-win`) was made with Python 3.13 or newer. Nuitka cannot
use MinGW there, and MinGW is what compiles impacket's large generated modules (MSVC runs out of heap
space on them). The build needs Python 3.10, 3.11 or 3.12; 3.12 is what CI uses. The scripts now stop
before the long step with this message, also for an environment that already exists. To fix it:

```powershell
py -0p                                       # which Pythons are installed
winget install --id Python.Python.3.12 -e    # only if there is no 3.12
Remove-Item -Recurse -Force probe\windows\.venv-win
```

Then run the script again; it picks `py -3.12` by itself, even when `python` on the PATH is newer.

**`Could not install packages due to an OSError: [Errno 22] Invalid argument: '...\.venv-win\Scripts\DumpNTLMInfo.py'`**
(or another impacket script, or "Access is denied"). Installing impacket copies about 70 of its example
scripts (`secretsdump.py`, `ntlmrelayx.py`, ...) into `.venv-win\Scripts`. Antivirus tends to flag
those as hacking tools and block the write. The agent never uses them. To check, without waiting for a
20-minute build:

```powershell
.\probe\windows\.venv-win\Scripts\python.exe -m pip install impacket
Get-MpThreatDetection | Sort-Object InitialDetectionTime -Descending |
    Select-Object -First 5 InitialDetectionTime, Resources
```

If the detections name files in `.venv-win\Scripts`, exclude that one folder (elevated PowerShell; this
is a decision for whoever owns the PC, and on a company-managed PC it is IT's), delete the folder, run
the script again, and remove the exclusion once you are done building:

```powershell
Add-MpPreference -ExclusionPath "$PWD\probe\windows\.venv-win"
Remove-MpPreference -ExclusionPath "$PWD\probe\windows\.venv-win"
```

If nothing is detected, the cause is something else: send the full pip output.

---

## Known limits (not blockers for connect-scan)

- **AV/EDR** may flag a network scanner. On machines you own:
  `Add-MpPreference -ExclusionPath "C:\ProgramData\vedha-agent"`. On customer
  machines, their security team allowlists it (hash + path + expected behavior).
  Coordinate — never evade their controls.
- **Raw-socket SYN / OS-fingerprint** need Npcap + admin; without it the agent
  still does connect / UDP / banner / TLS / SMB / LDAP / DNS scans.
- **Crash-safe result durability** is POSIX-only today (results still upload).
- **Plain-HTTP manager** sends the token in clear text — fine for the testing
  box; use `https://` for production.
