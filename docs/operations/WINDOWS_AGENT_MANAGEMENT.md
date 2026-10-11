# Windows agent: start it, run it, manage it

For the person who has the downloaded agent on a Windows machine and wants it running and under
control. Every command here was read out of the installer and agent source (`probe/windows/*.ps1`,
`probe/agent/*.py`, `manager/backend/app/routers/*.py`) on 11 Oct 2026. **The commands were not run on a
Windows machine while writing this page**, so section 12 lists what still needs one real run.

Related, and not repeated here: [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) (building and
sending the package) · [reference](../probe/WINDOWS_AGENT_REFERENCE.md) (every file, setting, state, exit
code) · [hosting on S3](WINDOWS_AGENT_HOSTING.md) · [debugging](DEBUGGING_THE_AGENT.md).

---

## 1. Pick the route

| You have | Use | Needs | Section |
|---|---|---|---|
| A command from **Fleet → Add agent → Windows** | the one-liner | admin PowerShell or cmd, internet to the manager | 2.1 |
| **`vedha-agent-win.zip`** (built by the pipeline, sent to you) | `install.cmd -Token vet_...` | admin rights, the install token | 2.2 |
| An S3 one-liner (`get.ps1 ... -Version ... -Sha256 ...`) | paste it | admin PowerShell | 2.3 |
| Just want to **watch it connect once**, no install | `run.cmd` | nothing (see the catch in 2.4) | 2.4 |
| The **git repo** on a lab PC | `setup.cmd` | Python (auto-installed) | 2.5 |

All routes except 2.4 and 2.5 install the **same compiled agent**. It needs no Python, runs as a
Scheduled Task called `VedhaAgent` (SYSTEM, starts at boot, restarts itself) and only makes
**outbound** connections to the manager (TCP 443). It opens no inbound port.

Requirements: 64-bit Windows 10 / Server 2016 or newer, administrator rights, about 500 MB free on the
system drive, outbound HTTPS to the manager.

---

## 2. Start it

### 2.1 One command from the manager (Fleet → Add agent → Windows)

The **Windows** tab appears only when the manager has a published release that includes a Windows
package. If it is missing, use 2.2.

Run it in an **elevated** prompt. PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm 'https://MANAGER/agent/install.ps1'))) -Manager 'https://MANAGER' -Token 'vet_...'"
```

or cmd.exe (it asks for administrator rights itself):

```bat
curl.exe --proto =https --tlsv1.2 -fsSL "https://MANAGER/agent/install.cmd" -o "%TEMP%\vedha-install.cmd" && "%TEMP%\vedha-install.cmd" "https://MANAGER" "vet_..."
```

Before installing anything the script checks the release's ECDSA signature, then the package's size and
SHA-256, then (when the release pins one) the Authenticode signature, and stops at the first mismatch.
Add `-VerifyOnly` to do those checks and nothing else (no admin needed).

### 2.2 The downloaded zip (`install.cmd` / `install.ps1`)

1. **Check the file.** `Get-FileHash .\vedha-agent-win.zip -Algorithm SHA256` must equal the value you
   were given through a *different* channel.
2. **Unzip** to a normal folder, for example `C:\vedha-install`. Do not run it from inside the zip.
3. **Open a prompt in that folder** and run:

   ```bat
   install.cmd -Token vet_XXXXXXXX
   ```

   Windows shows one administrator prompt; the install continues in a new window that stays open.

**`install.cmd` or `install.ps1`?** `install.cmd` is only a launcher for `install.ps1` that bypasses the
PowerShell execution policy for that one run. Calling the script directly works too, but a default policy
may refuse it, so use this form:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Token vet_XXXXXXXX
```

Every option works with either (`-Proxy`, `-CaBundle`, `-Scope`, `-Name`, `-TokenFile`, `-Repair`,
`-Uninstall`, `-NoWait`; full table in the [reference](../probe/WINDOWS_AGENT_REFERENCE.md#7-the-installer)).
No token yet? Run it without one: it asks for the token and also accepts Enter, which makes the agent show a
**pairing code** that someone approves in Fleet (2.6).

**What you will see** (six numbered steps, and nothing is changed if step 1 or 3 fails):

| Step | Does | If it fails |
|---|---|---|
| 1/6 | Windows version, 64-bit, package checksums (`SHA256SUMS.txt`), 500 MB free, the agent program starts | Antivirus removed or blocked the program → give `ALLOWLIST.txt` to the security team, unzip again |
| 2/6 | Works out manager, name (`<computer>-probe`), scan scope (this computer's own network; one larger than a /22 is narrowed to its /24) | Bad `-Scope` / `-Manager` → the message names it |
| 3/6 | `doctor --preinstall`: DNS, proxy, TCP, TLS, HTTP to the manager | Nothing is installed; the message says what IT must allow. `-SkipPreflight` overrides |
| 4/6 | Copies the program to `C:\Program Files\Vedha Agent`, locks `C:\ProgramData\vedha-agent`, writes `agent.env`, registers the task. A failure puts the previous version back | |
| 5/6 | Starts the task and waits up to 2 minutes | |
| 6/6 | Prints the result | |

| Result | Meaning | Exit code |
|---|---|---|
| `SUCCESS: the Vedha agent is installed and connected.` | online; the one-time token has been removed from `agent.env` | 0 |
| `INSTALLED. One step left: approve this agent in Fleet.` | prints a URL and a code; approve it (2.6) and it connects by itself | 0 |
| `INSTALLED, BUT NOT CONNECTED YET.` | installed, cannot reach the manager yet; the doctor findings follow and the agent keeps retrying | 3 |
| `STOPPED: ...` | a check failed; nothing further changed; log path printed | 1 |

Each run writes `C:\ProgramData\vedha-agent\logs\install-<date>.log` with the token masked.

### 2.3 The S3 one-liner

Generated for you by `publish-to-s3.sh`; you only add the token. See the
[hosting guide](WINDOWS_AGENT_HOSTING.md).

### 2.4 Watch it without installing (`run.cmd`)

Double-click `run.cmd` (or run it in a prompt). It runs `vedha-agent.exe run` in that window until you
close it. It needs a manager address baked into the package (otherwise it stops and says so) and uses the
**same** `C:\ProgramData\vedha-agent` identity as the installed agent.

The catch: once the agent is installed, that folder is readable only by SYSTEM and Administrators, so a
normal user cannot use `run.cmd`; and an administrator who runs it while the task is running gets
*"another Vedha probe is already using this state file"*, because the agent allows one process per
identity (two would double the scan traffic and corrupt each other's results). To debug in a window:

```powershell
Stop-ScheduledTask -TaskName VedhaAgent
# ... run.cmd in an Administrator prompt, watch it, Ctrl+C ...
Start-ScheduledTask -TaskName VedhaAgent
```

### 2.5 From the git repo (lab only)

```bat
git clone https://github.com/Rutikm18/Project-Vedha.git
cd Project-Vedha\probe\windows
setup.cmd
```

`setup.cmd` elevates, then `setup.ps1` finds or installs Python 3.12, builds a private venv, installs the
dependencies and registers the **same task name** `VedhaAgent`, running the readable Python source through
`C:\ProgramData\vedha-agent\agent-service.cmd`. `-Manager <https url>` is required (it prompts if you give
none). Add `-Foreground` to run in the window with no admin and no task.

This is the lab path: it ships readable source, may add Windows Defender exclusions for its own venv and
data folder, has no install-token option, and takes its settings from `agent-service.cmd` instead of
`agent.env`. **Do not mix it with route 2.1-2.3 on one machine**; they share the task name and the data
folder, and each replaces the other's task.

### 2.6 Approving an agent that shows a pairing code

In Fleet, **Pending requests** lists agents waiting for approval; enter the code the installer printed and
approve. The agent connects on its own within seconds. A name is optional.

---

## 3. Is it running? Three checks, in this order

**Which window are you in?** If the prompt looks like `C:\Users\you>` you are in **Command Prompt**
(cmd.exe), where PowerShell commands such as `Select-String` or `Stop-ScheduledTask` fail with *"is not
recognized as an internal or external command"*. Either type `powershell` first (the prompt then starts
with `PS`), or use the cmd forms in the table in section 4. Open it as Administrator: right-click → *Run as
administrator*.

**On the machine** (Administrator prompt). The program is
`"C:\Program Files\Vedha Agent\vedha-agent.exe"`; below it is written `vedha-agent`.

```powershell
vedha-agent status          # what the agent last recorded; exit code 0 only when online
vedha-agent doctor          # checks the path to the manager, the data folder, the scope; explains each problem
vedha-agent version         # "Vedha Probe 2.2.x"
Get-ScheduledTask -TaskName VedhaAgent | Select-Object TaskName, State
Get-Process vedha-agent
```

`status` is the *last state the agent wrote* plus a check that the process is alive; it does not probe the
network. States: `starting`, `enrolling`, `awaiting-approval`, `online`, `retrying` (cannot reach the
manager; `reason` and `remediation` say why), `failed`, and `not-running`.

**In the log** `C:\ProgramData\vedha-agent\logs\agent.log`:

```powershell
Get-Content 'C:\ProgramData\vedha-agent\logs\agent.log' -Tail 80 -Wait
```

| Line | Meaning |
|---|---|
| `Registered as '<name>'` / `Resumed as '<name>'` | the manager accepted it |
| `WebSocket connected. Push mode active` | healthy: jobs are pushed to it |
| `WebSocket ... falling back to HTTP poll`, `Waiting for scan jobs (HTTP polling)` | live connection blocked by a firewall or proxy; polling works, just slower to start jobs |
| `WebSocket auth rejected` | the manager refuses its credential |
| `Device credential was revoked, expired, or disabled` / `This agent's access has expired` | see 6.3 |
| `Manager not reachable [n/6]` | network: run `doctor` |
| `Port scans: closed ports report in N ms (Windows SYN retry off ...)` | good (2.2.6 and later) |
| `Port scans: Windows still retries refused connections (~2 s per closed port)` | full-port scans from this agent will be slow; see 8 |

**In Fleet** (or `GET /agents`): the agent should be listed with `online: true`. The manager calls an agent
online when its last heartbeat is under **90 seconds** old *and* its status is `online` or `busy`.

---

## 4. Everyday operations

All from an **Administrator** prompt, because the task runs as SYSTEM.

| I want to | Do |
|---|---|
| Stop the agent | `Stop-ScheduledTask -TaskName VedhaAgent` |
| Start it | `Start-ScheduledTask -TaskName VedhaAgent` |
| Restart it | stop, then start (do this after every `agent.env` change) |
| Stop it starting at boot | `Disable-ScheduledTask -TaskName VedhaAgent` (and `Enable-ScheduledTask` to undo) |
| Why did it last stop? | `Get-ScheduledTaskInfo -TaskName VedhaAgent` → `LastTaskResult` is the agent's exit code: `0` normal, `1` setup error or crash (in the log), `2` gave up on the manager (only if `PROBE_KEEP_RETRYING` is off) |
| See more detail | add `PROBE_DEBUG=1` to `agent.env`, restart |
| Send a problem to support | `vedha-agent support-bundle --mask-ips` writes a zip with the diagnosis, redacted settings and the log tail. It never holds the identity file, keys, tokens or queued results. Nothing is sent automatically |
| Change the manager, name, scope, proxy or CA | `install.cmd -Repair -Scope 10.0.5.0/24` (any of `-Manager -Name -Scope -Proxy -CaBundle`). Needs no token and **keeps the agent's identity** |
| Change one setting by hand | edit `C:\ProgramData\vedha-agent\agent.env` as Administrator, then restart. Settings you can add are in the [reference](../probe/WINDOWS_AGENT_REFERENCE.md#3-agentenv---settings) |

**In Command Prompt (cmd.exe) instead of PowerShell** (run as Administrator):

| I want to | cmd.exe form |
|---|---|
| Stop / start the agent | `schtasks /End /TN VedhaAgent` / `schtasks /Run /TN VedhaAgent` |
| Task state and last result | `schtasks /Query /TN VedhaAgent /V /FO LIST` (look at *Status* and *Last Result*) |
| Last 60 log lines | `powershell -NoProfile -Command "Get-Content 'C:\ProgramData\vedha-agent\logs\agent.log' -Tail 60"` |
| Log lines about the live connection | `findstr /i "websocket websockets" "C:\ProgramData\vedha-agent\logs\agent.log"` |
| Is the process running | `tasklist /FI "IMAGENAME eq vedha-agent.exe"` |
| Disable / enable start at boot | `schtasks /Change /TN VedhaAgent /DISABLE` / `schtasks /Change /TN VedhaAgent /ENABLE` |

> **`-Repair` re-installs the package you run it from.** Running it from the same 2.2.0 folder re-installs
> 2.2.0 and fixes nothing. To get a newer agent, run it from a folder unzipped from a **newer** package
> (section 5); check the result with `vedha-agent version`.

> **Gotcha: `-Repair` (and an update) rewrites `agent.env` from a fixed list of keys.** The installer keeps
> `PLATFORM_URL`, `PROBE_NAME`, `PROBE_NETWORK_SEGMENTS`, `HTTPS_PROXY` and `PROBE_CA_BUNDLE`, but **drops any
> setting you added by hand** (for example `PROBE_DEBUG`, `PROBE_MAX_FULL_SCAN_SECONDS`, `HEARTBEAT_INTERVAL`).
> Write your extra settings down and re-add them after every repair or update, then restart.

> **Stopping while a scan runs abandons it.** The manager notices when the agent stops renewing the job's
> 300-second lease, then puts the job back to `pending` for another attempt; once its attempt limit is used
> the job is marked `failed`, and whatever per-host evidence had already arrived is kept as its result.

**Scope has two layers and both must cover a target.** The engagement's scope (set in Fleet) and the
agent's own ceiling (`PROBE_NETWORK_SEGMENTS`, default: this machine's own /24). A job outside either is not
dispatched or is rejected. If the machine's network could not be detected, the agent connects and receives
**no jobs** until you run `install.cmd -Repair -Scope <your network>`. After changing it, confirm the
manager sees the new value (`network_segments` in `GET /agents`); that is read from the manager, not
assumed.

---

## 5. Update to a newer agent

The agent does **not** download or apply updates. It reports its version on every heartbeat and, at start,
asks the manager whether a newer one exists; the manager answers and sends nothing.

1. Get the new package: a new zip, or run the Fleet / S3 command again with a **fresh token**.
2. For a zip: unzip it somewhere new, then in an Administrator prompt there:

   ```bat
   install.cmd -Repair
   ```

   `-Repair` copies the new program in (the old one is kept as `Vedha Agent.old` while the new files are
   copied and the task is registered, and put back if either step fails), keeps the identity and settings, and re-checks the connection.
3. Check: `vedha-agent version`, and `agent_version` in Fleet.

> **`-Repair` and `install.cmd -Token` install the package they are run from, even an OLDER one.** Nothing
> compares versions. Running them from a forgotten download folder replaces a working agent with an old one
> (seen in the field: a working agent was replaced by a 2.2.0 package that cannot open its live
> connection). Before installing, run `<that folder>\vedha-agent\vedha-agent.exe version`; to find every
> copy on the PC: `dir /s /b C:\Users\*vedha-agent.exe`. The log keeps the history of what ran:
> `findstr /i "starting (log level" "C:\ProgramData\vedha-agent\logs\agent.log"`.
4. Re-add any hand-added settings (the gotcha in section 4).

**Which version should you be on?** `main` is at **2.2.7**. 2.2.6 added the Windows closed-port fix and the
removal of the Deep Port Sweep host cap. 2.2.7 makes `vedha-agent doctor` show the closed-port check that
the 2.2.6 startup message tells you to run. Build a new package for either; an agent still on 2.2.5 has none
of these changes.

**Building the package.** Normally GitHub → Actions → *vedha-agent-windows-build*. While Actions is blocked
by the account's billing, build on any Windows machine with Python 3.10-3.12 and internet:

```powershell
cd Project-Vedha\probe\windows
powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1                       # compiles the agent (Nuitka)
powershell -ExecutionPolicy Bypass -File package-zip.ps1 -Manager https://MANAGER  # makes dist\vedha-agent-win.zip
```

`-Manager` bakes one manager address into the zip; `-Release` builds the address-less package the manager
itself serves. The zip's SHA-256 is printed beside it; send that by a different channel than the zip.

---

## 6. What you can do about an agent in Fleet

| Task | Where | Notes |
|---|---|---|
| See agents, status, last heartbeat, version, networks | Fleet | `online` is the 90-second rule in section 3 |
| Make an install token | Fleet → Add agent | single use; an engagement allows at most 5 unused tokens; an engagement that already has an agent assigned, or no scope, is refused |
| Cancel an unused token | Fleet → Add agent → Revoke | |
| Approve a waiting agent | Fleet → Pending requests | section 2.6 |
| Stop a running job | the **Cancel** button on the campaign page (console `POST /api/fleet/jobs/{id}/cancel`, manager `POST /agents/jobs/{job_id}/cancel`). A queued job just becomes `cancelled`; a running one has its lease superseded, which is what makes the agent abandon the scan | the agent sees it as a lease revoked (`409` on its next heartbeat) and stops |
| Limit how long an agent may work | Fleet → access expiry (`+Nd`, or clear) | the agent then logs `This agent's access has expired` and re-checks every `PROBE_EXPIRED_RETRY_SECS` (default 300 s) |
| **Cut an agent off now** | set its access expiry to a time in the past (`PATCH /agents/{id}/access-expiry`) | "A past instant expires the agent immediately." |

**What does not exist.** There is no *revoke*, *disable* or *delete* agent button or endpoint. The database
has `lifecycle_status` and credential `revoked_at` fields and the manager refuses an agent that is not
`active` or whose credential is revoked, but nothing in the current code sets them. So: to cut an agent
off, use the expiry above; to remove it from the list, there is no way yet. (The older operator guide says
you can "revoke the agent from Fleet"; that is not true today, and its text is corrected.)

---

## 7. Why a job does not start (connected, but nothing scans)

The manager offers a job only to an agent that is all of these:

1. **online**: status `online`, heartbeat under 90 s old;
2. **idle**: it runs **one job at a time**, so a `busy` agent gets nothing new until it finishes;
3. **capable**: its advertised capabilities include what the job needs;
4. **in scope**: the job's targets lie inside the agent's `network_segments` *and* the engagement's scope.

When no online agent qualifies, the manager API log records one line per job with the reason for each
agent:

```bash
docker compose logs --since 1h api | grep agent.job.no_eligible_probe
```

(`reasons` reads like `missing capability 'x' (probe advertises [...])`, `engagement has no scope_cidrs`, or a
network that does not cover the targets.) The common causes, in order:

| Symptom | Cause | Fix |
|---|---|---|
| Agent `online`, job `pending` forever | scope: the agent's /24 does not contain the targets | `install.cmd -Repair -Scope <network>` (and check the engagement scope) |
| Job `pending`, agent `busy` | it is running another job | wait, or cancel that job |
| Agent `offline` after a long scan | its connection dropped; the job lease (300 s) lapses and the job is re-queued | `status`, `doctor`, the log; see section 3 |
| Console shows `Manager API ... (ECONNREFUSED / ECONNRESET / did not answer)` | the console cannot reach the API | [TROUBLESHOOTING](TROUBLESHOOTING.md#console-manager-api--errors-was-fetch-failed) |
| Log shows `409` on heartbeat and the job stops | the job was cancelled in the console, or its lease expired | expected after a cancel |

---

## 8. Deep and all-port scans from Windows

* **Use cases.** *Deep Port Sweep (all 65,535 ports)* sweeps every TCP port on each host; the lighter
  *aggressive* mode scans a fixed set of about 2,400 ports. The customer portal limits Deep to one asset by
  policy.
* **No host cap and a longer ceiling (2.2.6+).** `PROBE_DEEP_PORT_SWEEP_MAX_HOSTS` defaults to 0 (no cap).
  A job normally has `PROBE_MAX_JOB_SECONDS` (7200 s); a full 65,535-port sweep raises its own ceiling to
  cover the estimated sweep time, up to `PROBE_MAX_FULL_SCAN_SECONDS` (86400 s). The log line
  `full coverage: ...` says what was chosen and, if the rate is too low to finish, the rate that would.
* **Windows scans by TCP connect, not SYN.** Raw SYN scanning is Linux-only. Windows used to wait about
  2.2 s per closed port (it re-sends the SYN after a reset); 2.2.6 turns that off per socket
  (`SIO_TCP_INITIAL_RTO`). Check it took effect: the startup log line above, and from 2.2.7
  `vedha-agent doctor` shows `connect_fast_fail` as `pass` or `warn`. **This has been proven on a Linux
  loopback in tests but not yet on a real Windows machine; the first Windows run is the real test.**
  After it, the scan's `cleanup pass resolved ...` line should no longer re-check every port.
* **Advice.** Run full-port sweeps from a **Linux** agent where you can: it uses SYN scanning, which takes
  minutes per host. A Windows agent is the fallback.

---

## 9. Remove it

```bat
install.cmd -Uninstall            :: stops and removes the task and the program; keeps identity and logs
install.cmd -Uninstall -Purge     :: also deletes C:\ProgramData\vedha-agent (identity, settings, logs)
```

`uninstall.cmd` does the same. After `-Purge` the agent is a stranger to the manager: a new install makes a
new agent. Tell your Vedha contact so the old record is dealt with (section 6: there is no delete button).
To move an agent to a **different manager**, purge and install fresh with a token from the new one; whether
`-Repair -Manager` re-enrols an existing identity is not verified.

---

## 10. Where things are

| What | Path |
|---|---|
| Program | `C:\Program Files\Vedha Agent\` (anyone may run it; only Administrators change it) |
| Data (SYSTEM and Administrators only) | `C:\ProgramData\vedha-agent\` |
| Settings | `...\agent.env` |
| Identity (never share it) | `...\state.json` |
| Log | `...\logs\agent.log` (rotates at 10 MB, 5 kept); `...\logs\install-*.log` |
| Results waiting to upload / archive of submitted scans | `...\spool\` / `...\results\` (the archive is never pruned) |
| Live state | `...\status.json` |
| Scheduled task | `VedhaAgent` (SYSTEM, at boot, restart every minute up to 999 times, no time limit) |

The installer and agent never change the firewall, Defender, proxy, certificate store or PowerShell
execution policy (a test enforces this). If antivirus blocks the agent, give `ALLOWLIST.txt` (in the zip,
with the build's hash) to the customer's security team; do not try to evade their controls.

---

## 11. Quick troubleshooting card

| You see | Do |
|---|---|
| `Administrator rights were not granted` | run again, choose **Yes**, or open PowerShell as Administrator first |
| `The package failed its integrity check` | the download is damaged or antivirus removed a file: download again, compare the SHA-256 |
| `The agent program does not run on this computer` | antivirus / EDR: allow the folder (`ALLOWLIST.txt`) |
| `The manager is not reachable from this computer` | the doctor output says which of DNS / proxy / TCP / TLS; fix it, run the same command again |
| `TLS certificate is not trusted ... signed by: <name>` | HTTPS inspection: exempt the manager, or `-CaBundle <root.pem>` |
| `WARN clock` | fix time sync (TLS and tokens depend on it) |
| `That does not look like an install token` | it must start with `vet_`; copy it again from Fleet |
| `another Vedha probe is already using this state file` | a second copy is running; stop the task or the other window |
| `INSTALLED, BUT NOT CONNECTED YET` | the agent keeps retrying; fix what `doctor` lists and it connects without reinstalling |
| Online here, absent in Fleet | `status` → compare the manager address; read the log; ask the manager (`GET /agents`) |
| `irm : The remote name could not be resolved: 'manager'` | you pasted the example command with the placeholder `MANAGER` still in it (it appears twice: in the URL and in `-Manager`). Copy the command from Fleet → Add agent → Windows; do not retype it. The URL must be your real manager, e.g. `https://api.example.com/agent/install.ps1` |
| `is not recognized as an internal or external command` for `Select-String`, `Stop-ScheduledTask`, `Get-...` | you are in Command Prompt, not PowerShell: type `powershell` first, or use the cmd forms in section 4 |
| `status` says ONLINE but the agent is not in Fleet, and `vedha-agent version` says **2.2.0** | the known 2.2.0 bug: the compiled build lacked part of the `websockets` library, so it registered but never connected, and `status` kept saying ONLINE. Read the log (cmd: `findstr /i websockets "C:\ProgramData\vedha-agent\logs\agent.log"`); `No module named 'websockets.asyncio'` confirms it. Install a package built from 2.2.1 or later with `install.cmd -Repair` |
| `vedha-agent stop` / `restart` says `Unknown command` | the program has no such commands; use `Stop-ScheduledTask` / `Start-ScheduledTask -TaskName VedhaAgent` (section 4) |
| Lots of `WinError 10054` lines | normal peer resets from scanned hosts; 2.2.6 hides them below DEBUG |

---

## 12. Not yet verified on a real machine

1. Every command above on a clean Windows 10/11 or Server VM (written from source, not run).
2. A full enrolment with a real token, a job running end to end, and a reboot bringing the task back.
3. 2.2.6 / 2.2.7 on Windows: the closed-port timing, `connect_fast_fail` in `doctor`, and a full 65,535-port
   Deep Port Sweep of one host (record the time it takes).
4. Whether editing the name or scope in `agent.env` is reflected in Fleet without re-enrolling.
5. The Windows tab in Fleet (needs a published release that includes the Windows package).
