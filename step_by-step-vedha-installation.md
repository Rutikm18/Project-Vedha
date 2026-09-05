# Vedha Agent — Step-by-Step Installation Guide

Install the **Vedha probe (agent)** on a machine inside the customer network so it
connects to the Vedha **Manager** (cloud) and runs scan jobs. This is the
**git-based, source-mode** install we ship today — no Docker, no exe build, no zip.

- **Manager (already running):** `http://13.127.147.205:18080`
- **Agent (what you install here):** dials **out** to the manager over one
  connection, scans the local LAN, and **never opens an inbound port**.
- **Primary platform:** Windows. Linux/macOS steps are in Part F.

> Repo: `https://github.com/Rutikm18/Project-Vedha.git` · scripts live in `probe/windows/`.

---

## 0. Prerequisites (target machine)

| Requirement | Why | Get it |
|---|---|---|
| **Python 3.10+** | the agent runs on it | **auto-installed by `setup.ps1` if missing** (via winget or the official installer). Manual: https://www.python.org/downloads/windows/ |
| **Git** *(optional)* | to `clone`/`pull` the agent | https://git-scm.com/download/win — **or skip Git and download the repo ZIP** (see Step 1) |
| **Administrator** | for the permanent (background service) install, and to install Python all-users | one-time UAC prompt |
| **Outbound network + internet** | reach the manager + fetch Python/deps on first run | allow this PC → `13.127.147.205:18080` (TCP, outbound). **No inbound rule needed.** |

> **Fresh machine with nothing installed?** You don't need to pre-install Python —
> `setup.ps1` installs it for you. You only need a way to get the files: either
> Git (`git clone`) or the **Download ZIP** option in Step 1.

Optional — check what's already there (a new **PowerShell** window):
```powershell
python --version   # ok if this says "not found" — setup will install it
git --version      # only needed if you clone instead of downloading the ZIP
```

---

## 1. Windows — permanent install (recommended)

Runs the agent as a background task (`VedhaAgent`) that starts on boot and
restarts on failure.

**Step 1 — Get the code**

With Git:
```bat
git clone https://github.com/Rutikm18/Project-Vedha.git
cd Project-Vedha\probe\windows
```

Without Git (nothing installed) — download the ZIP in PowerShell, then enter the folder:
```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri https://github.com/Rutikm18/Project-Vedha/archive/refs/heads/main.zip -OutFile vedha.zip -UseBasicParsing
Expand-Archive vedha.zip -DestinationPath . -Force
cd Project-Vedha-main\probe\windows
```
(Or use the green **Code → Download ZIP** button on GitHub and extract it.)

**Step 2 — Install + start**

In **PowerShell**, opened **as Administrator** (right-click → *Run as administrator*):
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

Or, from a normal (non-admin) window — this one line self-elevates (UAC prompt) and installs:
```powershell
Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PWD\setup.ps1`""
```

Or simply run the batch wrapper (double-click or type it), which auto-elevates:
```bat
setup.cmd
```

- Accept the **UAC (admin) prompt**.
- The script automatically: creates a Python venv → installs dependencies →
  detects this host's `/24` as the scan scope → registers the `VedhaAgent`
  background task → starts it.

**Step 3 — Confirm it connected** (see Part D).

That's it. The agent is now running and will survive reboots.

---

## 2. Windows — quick test (no admin)

To watch it connect in a console window without installing the background task:
```bat
cd Project-Vedha\probe\windows
powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground
```
You'll see it enroll and reach **"WebSocket connected. Push mode active — waiting
for jobs"**. Close the window to stop. (Use Part 1 to make it permanent.)

---

## 3. Point at a different manager or scope

By default the manager is `http://13.127.147.205:18080` and the scope
auto-detects. To override:
```bat
powershell -ExecutionPolicy Bypass -File setup.ps1 -Manager https://manager.example.com -Scope 10.0.0.0/24
```
- `-Manager` — full URL (use `https://…` in production; plain `http://` sends the
  token in clear text).
- `-Scope` — the CIDR the probe is allowed to scan (empty ⇒ the manager sends **no
  jobs**).

---

## 4. Update to the latest version
```bat
cd Project-Vedha\probe\windows
git pull
setup.cmd
```
Or in one step: `powershell -ExecutionPolicy Bypass -File setup.ps1 -Update`.
Re-running is safe — it reuses the existing identity and just refreshes the task.

---

## 5. Uninstall
```bat
cd Project-Vedha\probe\windows
uninstall.cmd
```
Run as administrator. The agent's identity/logs under
`C:\ProgramData\vedha-agent` are **kept** by default. To delete them too:
```bat
powershell -ExecutionPolicy Bypass -File uninstall.ps1 -Purge
```

---

## D. Verify it's working

**On the agent machine:**
```powershell
# the background task exists and is running
Get-ScheduledTask -TaskName VedhaAgent
# tail the log
Get-Content C:\ProgramData\vedha-agent\logs\agent.log -Tail 20 -Wait
```
Healthy log ends with lines like:
```
Registered as '<name>' … WebSocket connected. Push mode active — waiting for jobs
```

**Where things live:**
| Path | Contents |
|---|---|
| `C:\ProgramData\vedha-agent\state.json` | device identity (do **not** copy to another machine) |
| `C:\ProgramData\vedha-agent\logs\agent.log` | runtime log |
| `C:\ProgramData\vedha-agent\spool\` | results awaiting upload |

**On the Manager:** open **Fleet / Probes** — the new probe appears (approve it
if pairing is required; see Troubleshooting).

---

## E. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `python is not recognized` | Python not on PATH | reinstall Python, tick **Add to PATH**, open a new terminal |
| `git is not recognized` | Git not installed | install Git for Windows |
| Log: `connection refused` / `timed out` | manager down or firewall | confirm outbound to `13.127.147.205:18080`; check the manager is up: `curl http://13.127.147.205:18080/health` |
| Connected but **no jobs run** | scope empty or wrong | re-run with `-Scope <your-LAN-CIDR>` (e.g. `192.168.1.0/24`) |
| Log: **PROBE PAIRING REQUIRED** + a code | manager requires approval | open the manager Fleet page, enter/approve the code |
| Log: `enrollment not approved` | nobody approved in time | approve in Fleet, then re-run `setup.cmd` |
| AV/EDR blocked `python.exe` / the agent | scanner behavior looks like recon | allowlist it (Part G) |
| Task runs but nothing in the log | wrong working dir / venv | re-run `setup.cmd`; check `C:\ProgramData\vedha-agent\logs\agent.log` |

Clean identity reset (start enrollment over):
```bat
powershell -ExecutionPolicy Bypass -File uninstall.ps1 -Purge
setup.cmd
```

---

## F. Linux / macOS install (secondary)

The existing installer handles these directly:
```bash
git clone https://github.com/Rutikm18/Project-Vedha.git
cd Project-Vedha/probe
./install.sh 13.127.147.205
```
`install.sh` normalizes the bare IP to `http://13.127.147.205:18080`, builds a
venv, auto-detects the local scope, and runs the agent. Run persistently with
`nohup ./install.sh 13.127.147.205 >~/vedha-probe.log 2>&1 &` or a systemd unit.
(Docker mode: `sudo sh install.sh --docker --manager <url>` — Linux only.)

---

## G. Antivirus / EDR allowlisting

A network scanner can trip AV/EDR. This is expected for authorized scanning tools
(Nessus/Qualys behave the same). **Coordinate with the customer's security team —
do not evade their controls.**

- **On a machine you own** (testing), exclude it (admin PowerShell):
  ```powershell
  Add-MpPreference -ExclusionPath "C:\ProgramData\vedha-agent"
  Add-MpPreference -ExclusionProcess "python.exe"
  ```
- **On a customer machine**, give their team: the install path
  (`C:\ProgramData\vedha-agent`), expected behavior (outbound to the manager +
  authorized LAN scanning), and the scope, so they allowlist it.

---

## H. What `setup.ps1` does (reference)

1. Finds Python; creates a private venv in `probe\windows\.venv-win`.
2. Installs runtime deps: `httpx websockets cryptography impacket ldap3 dnspython`.
3. Auto-detects this host's IPv4 `/24` as `PROBE_NETWORK_SEGMENTS` (the scan ceiling).
4. Sets `PLATFORM_URL`, `PROBE_NAME`, `STATE_FILE`, `RESULT_SPOOL_DIR` under
   `C:\ProgramData\vedha-agent`.
5. Either runs `python -m agent.agent run` in the foreground (`-Foreground`) or
   registers the SYSTEM scheduled task **VedhaAgent** (default) and starts it.

The agent generates its own device identity (its keypair is its ID). On the AWS
testing manager (auto-enroll) it connects with nothing but the manager URL; on a
locked-down manager it prints a pairing code to approve in Fleet.

---

## Quick reference

```bat
:: install (permanent)
git clone https://github.com/Rutikm18/Project-Vedha.git
cd Project-Vedha\probe\windows
setup.cmd

:: test (no admin)
powershell -ExecutionPolicy Bypass -File setup.ps1 -Foreground

:: update
git pull && setup.cmd

:: uninstall
uninstall.cmd
```
