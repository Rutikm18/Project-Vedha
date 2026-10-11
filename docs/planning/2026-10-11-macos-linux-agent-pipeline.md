# Agent on macOS and Linux - what exists, and what is parked in the pipeline

Date: 2026-10-11 · Status: backlog, nothing here is started
Asked for by the owner (11 Oct): the agent should be runnable on macOS and Linux as well as Windows, with the Windows
one-command experience. Facts below are from the code (`probe/install.sh`, `probe/Dockerfile`, `scripts/agent_release.py`,
`probe/agent/kernel_limits.py`); nothing was run on a Mac.
Related: [ONE_COMMAND_INSTALL](../operations/ONE_COMMAND_INSTALL.md) · [Windows pipeline](2026-10-07-windows-agent-pipeline.md) · [STATUS.md](../STATUS.md).

## What exists today

| | One command from Fleet | What actually runs | Gaps |
|---|---|---|---|
| **Windows 10 / Server 2016+, x64** | yes, once a signed release with the Windows package is published | compiled agent, Scheduled Task as SYSTEM | not Authenticode-signed; not run on a real manager (see STATUS P0-3b, P0-3c) |
| **Linux x86-64 / ARM64** | yes, **only if the release was built with the Docker images** (`make agent-release` with the default `AGENT_ARCH`; a Windows-only release has none) | one Docker container, non-root, read-only, `--cap-drop ALL` | needs Docker on the host; **cannot SYN scan** (no `NET_RAW`), no ARP/Layer-2 discovery, scans from behind Docker's network |
| **Linux, native** | no | `sh install.sh connect --manager … --token …` from a copy of the `probe/` folder: installs Python 3.8+ (apt, dnf or pacman) and runs `python3 -m agent.setup` | no packaged build, no service unit, strict verification is off by default ("initial phase" in the script); as root it is the only way to get SYN scan |
| **macOS** | no | the same `install.sh connect …` path (it calls `brew install python` when Python is missing), or the Docker path under Docker Desktop | **not tried on a Mac**; `install.sh` has no macOS-specific handling; no launchd service; raw sockets on macOS cannot receive TCP, so connect scan only; Docker Desktop scans from inside a VM behind NAT |
| **Windows on ARM64** | no | the installer's checks would accept it; the x64 program under emulation was never tried | unknown |

## Pipeline (ordered)

| # | Item | Why | Size | Needs you |
|---|---|---|---|---|
| L1 | **Prove the Linux one-command end to end**: build a release with images, publish it, install on a clean Ubuntu host with Docker, confirm the agent appears in Fleet | the Linux path has never been run against a real manager; only its pieces are tested | S | a Linux host and Docker on the build machine |
| L2 | **Native Linux package**: a `.deb`/`.rpm` or a self-contained tarball with a systemd unit, running as a service, with `CAP_NET_RAW` (or root) so SYN scan and ARP work; signed release like Windows | the Docker agent cannot do the fast, accurate scans the Windows story promises to match; this is what makes "Linux agent" mean full capability | M-L | which distros first (Ubuntu/Debian, RHEL/Alma); whether customers accept a root service |
| L3 | **`install.sh` parity with the Windows installer**: `--token-file`, `SHA256SUMS` check, update-in-place and a downgrade guard, `-Repair`/uninstall equivalents | Windows has all of these; Linux has none (also in the Windows pipeline as X5) | S-M | no |
| L4 | **Fleet shows "Linux (Docker)" and "Linux (native)" as separate options** with the capability difference stated | operators must know which agent can SYN scan before choosing | S | no |
| M1 | **Run the native path on a real Mac** (Intel and Apple silicon) and fix what breaks | nothing macOS-specific has been exercised | S-M | a Mac |
| M2 | **Packaged macOS agent**: compiled build (Nuitka, as on Windows), launchd daemon, `.pkg` installer, **signed with a Developer ID and notarized** | without notarization Gatekeeper blocks the download; this is the macOS equivalent of the Windows signing problem (P0-3c) | L | an Apple Developer account and certificate |
| M3 | **macOS one command** in Fleet (`curl … \| sudo sh`) once M2 exists | parity with Windows and Linux | S | after M2 |
| W1 | Try the x64 Windows agent on Windows ARM64 (emulation), or build an ARM64 package | currently "unknown" | S | an ARM64 Windows machine |

## Decisions needed from the owner

1. Which comes first: **native Linux (L2)** or **macOS (M1-M3)**? My recommendation is L1, then L2, then macOS, because Linux is where most
   scan targets and most customer servers are, and L2 is what gives SYN scanning.
2. Is a root-level agent acceptable to customers on Linux? Without it SYN scan and ARP discovery are not possible.
3. Do you have, or will you buy, an Apple Developer account? M2 cannot ship without it.
