# Universal cross-OS vedha-agent installer + self-scan — design

**Date:** 2026-09-09
**Branch:** `cross-os-agent-installer`
**Status:** Approved design — ready for implementation planning

## Problem

Running `vedha-agent` (the probe) today takes **two separate installer families**:
`probe/install.sh` (POSIX sh, macOS/Linux) and `probe/windows/` (PowerShell/CMD).
They duplicate the same logic (Python/venv setup, scope auto-detect, enrollment,
run loop, service install) in two languages that drift apart. We want **one
installer experience for any OS** (macOS, Linux, Windows), plus a first-class
option to **scan the host's own IP** without a Manager.

## Goals

- One orchestrator, one source of truth, for macOS + Linux + Windows.
- A single obtain-and-run command per OS (`curl … | sh` on unix, `irm … | iex` on
  Windows), plus a literal single-file path (`python vedha-setup.py`) where Python
  already exists.
- A `self-scan` mode: auto-detect this machine's own IP and scan **only** it, via
  the existing manager-less local engine.
- Optional reboot-surviving service install per OS.
- Correct behavior for the real per-OS edge factors (below) — never silently wrong.

## Non-goals

- No new scanning capability — reuses `agent.agent` (daemon + `local-run`) as-is.
- No Docker path in this installer (native venv only — see Edge factor #3). The
  existing `probe/docker-compose.yml` remains available for Linux users who want it.
- No sealed-binary packaging here (the existing `seal-probe.sh` /
  `build-agent-exe.ps1` remain the IP-protection path).
- No change to the Manager, enrollment protocol, or scope enforcement.

## Decision record (locked during brainstorming)

1. **Packaging:** native venv on every OS (native = correct LAN scanning on all three).
2. **Distribution:** a single hosted download-and-run command (curl on unix; `irm`
   on Windows, since Windows cannot pipe to `sh`).
3. **Self-scan:** the host's **own IP only**, manager-less; no `/24`, no auth gate needed.
4. **Persistence:** default one-shot/foreground; opt-in `--service` per OS.

## The real per-OS edge factors (verified in the repo, not assumed)

| # | Factor | Consequence for the design |
|---|--------|----------------------------|
| 1 | **No shell spans all three OSes** (`sh` vs PowerShell); **Python is the only common runtime** | One Python "brain" + two ~30-line bootstrap shims |
| 2 | **Python may be absent** (Win especially) | Shim auto-installs Python (apt/dnf/brew/winget); fail-closed with a clear message otherwise |
| 3 | **Docker ≠ LAN scanning on Windows/macOS** — Docker Desktop runs Linux containers in a VM/WSL2 behind NAT, scanning the *virtual* net (stated in `probe/windows/README.md`) | Installer is **native-venv only**; no Docker path |
| 4 | **Raw sockets/privilege differ** — unix SYN/ICMP need root; **Windows blocks raw TCP send since XP SP2** → connect-scan only; macOS needs root + BPF; scanner degrades gracefully | **Never require root**; detect + warn; document connect-scan fallback |
| 5 | **Persistence differs** — systemd / launchd / Scheduled-Task-as-SYSTEM | `--service` renders the correct unit per OS |
| 6 | **Paths & elevation differ** — `%ProgramData%` vs `/var/lib`/`$HOME`; UAC vs sudo | Per-OS state dir; elevation only requested for `--service` |
| 7 | **Scanning the host's own /24 touches other machines** | `self-scan` is own-IP-only — nothing else on the LAN is contacted |

## Architecture

```
  mac/linux:  curl -fsSL <base>/install.sh | sh -s -- <args>
  windows:    irm <base>/install.ps1 -OutFile install.ps1 ;  .\install.ps1 <args>
                     │                         │
             install.sh (POSIX sh)     install.ps1 (PowerShell)
             ── ensure Python 3.8+, then exec the brain ──
                     └────────────┬────────────┘
                                  ▼
                    agent/setup.py  ── THE BRAIN ──
       OS/priv detect · venv+deps · scope auto-detect · connect|self-scan · service
                                  ▼
                    agent.agent  (daemon: run  |  local-run)   ← reused unchanged
```

Everywhere Python already exists, the brain is directly runnable:
`python vedha-setup.py <args>` (a thin repo-root shim re-exporting `agent.setup`).

## Components (each: one responsibility, testable in isolation)

### `agent/setup.py` — the orchestrator (new)
Pure-logic where possible; side effects (subprocess, filesystem) isolated behind
small functions so the pure parts are unit-testable. Subcommands:

- `connect --manager <url> [--enroll | --pat <t> | --token <t>] [--scope <cidr>] [--service] [--name <n>]`
  1. ensure `.venv` + `requirements-runtime.txt` (idempotent via a requirements-hash stamp, mirroring current `install.sh`);
  2. resolve scope (CLI `--scope`, else auto-detect `/24`, see below);
  3. write/merge `probe.env` (`PLATFORM_URL`, `PROBE_NETWORK_SEGMENTS`, `PROBE_NAME`, `VERIFY_TLS`);
  4. either install the service (`--service`) or run the daemon in the foreground with a **cross-OS self-heal supervisor** (ports the sh restart loop: exit 4 → re-enroll fresh key; exit 2 → backed-off retry).
- `self-scan [--profile it|iot|ot] [--stage <stage>] [--service off]`
  → detect the host's own primary IPv4, set scope to **that single IP**, and run
  `python -m agent.agent local-run <own-ip> <profile> <stage>` — no Manager, no
  enrollment. Writes results to the standard local result archive.
- `doctor`
  → print OS, arch, privilege (root/admin?), Python version, venv/deps status,
  and (if a Manager is configured) reachability — so a user can self-diagnose.

### `install.sh` (refactor of the existing) — unix bootstrap
Detect `python3` ≥ 3.8; if absent, attempt install (`apt`/`dnf`/`brew`) or print
exact instructions; then `exec python3 -m agent.setup "$@"`. The bootstrap carries
no Docker logic (Linux users who want Docker use `docker-compose.yml` directly, per
Non-goals).

### `install.ps1` (refactor of `windows/setup.ps1`) — Windows bootstrap
Detect `py`/`python`; if absent, `winget install Python` (fallback: official
installer); then `python -m agent.setup @args`. Elevation (UAC) requested only
when `--service` is passed.

### Service templates (new, emitted only under `--service`)
- **Linux:** systemd unit → `systemctl enable --now vedha-agent` (user or system scope).
- **macOS:** launchd plist in `~/Library/LaunchAgents` → `launchctl load`.
- **Windows:** Scheduled Task `VedhaAgent` as SYSTEM (reuse the current pattern).

## Cross-OS scope auto-detection (no root, one implementation)
Replace the three OS-specific shell snippets with one stdlib routine in the brain:
open a UDP socket, `connect(("1.1.1.1", 80))` (no packets sent), read
`getsockname()[0]` → the host's primary source IPv4 → derive `<a.b.c>.0/24`.
Works unprivileged on macOS, Linux, and Windows. `self-scan` uses the bare IP;
`connect` uses the `/24` ceiling.

## CLI / UX surface (the "one command")

`<base>` is the repo's raw GitHub path, e.g.
`https://raw.githubusercontent.com/Rutikm18/Project-Vedha/main/probe`
(configurable at deploy time; any static host works).

```bash
# connect to a Manager (mac/linux) — pipe args through sh -s --:
curl -fsSL <base>/install.sh | sh -s -- connect --manager https://mgr.example.com --enroll

# connect to a Manager (Windows) — download then run (can't pipe to sh):
irm <base>/install.ps1 -OutFile install.ps1
.\install.ps1 connect --manager https://mgr.example.com --enroll

# scan only THIS machine, no Manager (any OS, once Python + repo are present):
python -m agent.setup self-scan

# diagnose:
python -m agent.setup doctor
```

## Error handling

- Python missing/too old → shim exits non-zero with the exact install command for
  the detected OS. Never proceeds half-configured.
- venv/deps failure → surface pip output, exit; the requirements-hash stamp is not
  written, so re-run heals it.
- Not privileged + `--service` → explain how to elevate (sudo / Run-as-Admin) and exit.
- Not privileged + scan → **proceed** (connect-scan fallback), print a one-line notice.
- Empty scope → refuse to run `connect` (fail-closed, mirrors current behavior);
  `self-scan` always has the own-IP scope so it never hits this.

## Testing

- **Unit (Python, no root/network):** OS/arch/privilege detection, scope derivation,
  arg parsing, `probe.env` merge, service-file rendering per OS (golden strings).
- **CI matrix (GitHub Actions ubuntu/macos/windows):** bootstrap → venv → deps →
  `doctor` exits 0 on all three.
- **Manual:** `self-scan` against localhost on each OS; `connect --enroll` against a
  test Manager; `--service` install/uninstall round-trip per OS.

## Build order (phasing)

1. **Brain core** — `agent/setup.py` with `doctor`, scope auto-detect, venv/deps,
   arg parsing + unit tests.
2. **`self-scan`** — own-IP detect → `agent.agent local-run` (delivers standalone
   value with no Manager).
3. **`connect`** — enrollment env + cross-OS supervisor loop.
4. **Bootstraps** — refactor `install.sh` + `install.ps1` to thin shims; repo-root
   `vedha-setup.py`.
5. **`--service`** — systemd / launchd / Scheduled Task templates.
6. **CI matrix** — the three-OS `doctor` smoke test.

Each phase is independently testable; phase 2 alone already gives "scan my own
machine on any OS."
