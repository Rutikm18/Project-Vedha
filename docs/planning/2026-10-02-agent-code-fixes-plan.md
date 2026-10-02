# Agent code fixes and Windows quick wins — task plan

Date: 2026-10-02 · Branch: `feat/agent-install` · Approach: [windows-agent-quick-wins](2026-10-02-windows-agent-quick-wins.md)

## Status (2 Oct 2026)

**Quick wins done** (committed on `feat/agent-install`): T1, T2, T3, T4 (agent ships only its closure,
`runtime-check`), T9 (Windows instance lock), T10 (Windows MAC lookup), T16 (install-command lifetime
1 h / 24 h / 7 d), T17 (manager-enforced access expiry, migration 0053), T18 (Fleet expiry controls,
portal read-only), T20 (retire risky Windows defaults), T21 (this doc, STATUS, memory).

**Also done (3 Oct):** T5–T8, the compiled build, with one gap. The closure-only compile is proven for
the Linux sealed image (`scripts/seal_parity.sh`: compiled `runtime-check` loads 73 modules + 6 libraries, no
source/bytecode/`findings` in the image, manifest parity). The Windows build script and its CI job
(`agent-windows-build.yml`) are written and statically tested but have **not been run**: no Windows machine
here, and the workflow only runs once pushed. Live expiry test also done (see STATUS).

**In the pipeline, not started:** T12, T13, T14, T15 (Windows release artifact, token-gated download route,
PowerShell installer, Fleet OS switch) and T19 (a real install on a Windows VM). They need the Windows build
artifact from CI and a Windows VM, and the owner's answers on the CI runner and the VM.

Rules for every task:

- One small change, with a test that would fail without it, committed on its own.
- `scanner/` and `main_scripts/` are byte-identical mirrors (`test_two_tree_parity.py`): edit
  `main_scripts/` first, then copy to `scanner/`.
- Nothing here needs a Windows machine except the tasks marked **[Windows]**. Those are written
  and syntax-checked here, and proved on the Windows CI runner and the owner's Windows VM.

Owner answers still open (defaults used until answered):

- Build the Windows agent on a GitHub Actions Windows runner: **assumed yes** (workflow is
  written; it runs only when pushed).
- Agent expiry defaults to the POC plan end: **not automatic**. Fleet pre-fills the POC end date
  and the operator confirms it.
- Windows VM for a real install: **needed for T19**.

## Phase A — ship only the agent's code (C1, C2)

| Task | Change | Done when |
|---|---|---|
| T1 | `probe/tools/agent_closure.py`: the static import closure from `agent/agent.py` (AST, including imports inside functions); `--list`, `--check`, `--export DIR` | Prints the 71 runtime modules; `--check` fails on a blocked module or an `import_module` / `__import__` call |
| T2 | Blocklist: `scanner.findings`, `scanner.run_all`, `scanner.va_campaign`, `scanner.accuracy*`, `scanner.delta_scanner`, `main_scripts.*`, `cve.*`, `tests.*`, `agent.setup` / `deps` / `cli` / `bootstrap` | Unit tests: closure excludes them; a planted forbidden import or dynamic import fails `--check` |
| T3 | Linux image: a select stage runs `--export`; the runtime stage copies only the closure | `docker build` passes; the image contains no `findings.py`; every closure module imports inside the image |
| T4 | `vedha-agent selftest`: imports every scanner the workflow can dispatch, builds a plan for 127.0.0.1, runs one local TCP connect; exits 0 or 1 | Unit test; it runs in the Linux image (T3) and in the compiled build (T6) |

## Phase B — compiled build (C1, C2)

| Task | Change | Done when |
|---|---|---|
| T5 | `probe/tools/check_build_report.py`: reads Nuitka's `--report` XML and fails if a compiled module is outside closure ∪ allowed third-party, or is blocked | Unit tests with sample report XML |
| T6 | Prove the compile recipe on Linux (container): Nuitka `--standalone` from `agent/agent.py` with `--nofollow-import-to` for the blocklist, paramiko and winrm; strip docstrings and asserts; report check; `selftest` passes; no `.py` / `.pyc` in the output | Works in a Linux build container (same flags the Windows build uses) |
| T7 **[Windows]** | `probe/windows/build-agent-exe.ps1`: same recipe; folder build into `dist\vedha-agent\`; PyInstaller removed | Script reviewed; proved by T8 on CI |
| T8 **[Windows]** | `.github/workflows/agent-windows-build.yml`: `windows-latest` runs build, report check, `selftest`, a no-source check, then zips and uploads the artifact | YAML valid; runs when pushed |

## Phase C — Windows runtime fixes (C3, C4, C6)

| Task | Change | Done when |
|---|---|---|
| T9 | Single-instance lock on Windows (`msvcrt.locking`) so two agents can't share `state.json` | Unit test with a fake `msvcrt`; POSIX behaviour unchanged |
| T10 | Neighbour / MAC lookup on Windows: run `arp -a <ip>` and parse `aa-bb-cc-dd-ee-ff` (`main_scripts` then `scanner`) | Parser test with real Windows `arp -a` output; parity test green |
| T11 | Licence off for the unsealed compiled build is set by the installer (T14); the agent says clearly why it stopped if it is missing | Covered by T14 tests |

## Phase D — Windows delivery (QW2, QW3)

| Task | Change | Done when |
|---|---|---|
| T12 | Release tool: optional `--windows-zip PATH` adds a `windows-amd64` artifact (zip, SHA-256) to the signed manifest | Cross-test: the manager loader accepts a release with and without it |
| T13 | Manager: `GET /agent/download/{platform}` (token-gated, `windows-amd64`); `GET /agent/install.ps1` (public) | Route tests: no token → 401; dead token → 401; wrong platform → 404 |
| T14 **[Windows]** | `probe/windows/install-agent.ps1` (published as `install.ps1`) does the following: <ul><li>preflight: OS / 64-bit / admin / TLS 1.2 / Constrained Language Mode / manager health / clock / battery</li><li>token download, checked against the manifest SHA-256</li><li>unpack to Program Files, ACL'd ProgramData</li><li>SYSTEM boot task, restart cap 10, rotating log, settings file</li><li>`-Proxy`, `-CaBundle`, `-Uninstall`, `-Purge`</li><li>licence off</li></ul> | Static checks here; proved on CI (T8 smoke) and the VM (T19) |
| T15 | Fleet → Add agent gets an OS switch (Linux / Windows); the backend returns Windows commands too | Route and frontend tests; browser check |

## Phase E — expiry from Fleet (QW4)

| Task | Change | Done when |
|---|---|---|
| T16 | Install-command lifetime choice: 1 h, 24 h, 7 days (operator and portal) | Tests: the BFF and portal accept only the allowed values |
| T17 | `agents.access_expires_at` (migration 0053) enforced by the manager. <ul><li>The heartbeat, job poll, result upload and device-token refresh routes refuse an expired agent with "agent access expired".</li><li>Running jobs may finish uploading.</li></ul> | Tests for every gated path; extending the date restores access |
| T18 | Fleet shows expiry and status (expired / expires in N days). <ul><li>The operator sets or extends the date; the POC end date is pre-filled.</li><li>The portal shows it read-only.</li></ul> | Frontend test; browser check |

## Phase F — clean-up and proof

| Task | Change | Done when |
|---|---|---|
| T19 **[Windows VM]** | One real install from Fleet on Windows 10/11 or Server | Agent enrols, scans one in-scope host, expiry blocks it |
| T20 | Retire risky paths for customers: banner on `setup.ps1`; remove the old IP and HTTP defaults; Defender `python.exe` exclusion becomes opt-in | Grep test: no `13.127.147.205` in `probe/windows` |
| T21 | Docs, STATUS, memory | Updated |

Order: T1–T4, then T5–T6, then T9–T10, then T12–T13, then T16–T18, then T7–T8, T14–T15,
then T20–T21. T19 runs when a VM is available.
