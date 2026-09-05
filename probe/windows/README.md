# Vedha Agent — Windows (simple, git-based)

Run the probe on a **Windows** machine straight from the repo — no Docker, no exe
build, no zip. The customer clones/pulls from GitHub and runs one script that
sets up a venv, installs dependencies, and starts the agent.

> Native (not Docker) on purpose: Docker on Windows runs Linux containers behind
> WSL2 NAT and would scan the *virtual* network, not the real LAN. See
> `../../probe_docker_customer_env.md` Part 4.

---

## The customer commands (on the target Windows machine)

**Prerequisites:** [Git](https://git-scm.com/download/win) and
[Python 3.10+](https://www.python.org/downloads/windows/) (tick *Add to PATH*).

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
| Firewall | outbound only | allow this PC → `13.127.147.205:18080` (no inbound) |

State/identity/logs live under `C:\ProgramData\vedha-agent\`.

**Per-machine:** each machine enrolls its own identity — do **not** copy
`state.json` between hosts. Scope auto-detects that host's `/24`.

---

## Files

| File | Role |
|---|---|
| `setup.ps1` / `setup.cmd` | **the automated installer** (venv + deps + run/register) |
| `uninstall.ps1` / `uninstall.cmd` | remove the background task |
| `probe.env.template` | documents the config the script sets |
| `README-CUSTOMER.txt` | short in-repo customer note |

**Advanced (optional, for sealed distribution to untrusted customers):**
`build-agent-exe.ps1` + `package-zip.ps1` build a single `vedha-agent.exe` and a
ZIP (see the exe launchers `run.cmd` / `install.ps1`). Not needed for the git flow
above.

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
