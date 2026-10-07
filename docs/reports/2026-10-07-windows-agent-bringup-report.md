# Windows agent bring-up report - 7 October 2026

Branch: `claude/fervent-brahmagupta-o0g44u` (16 commits ahead of `origin/main`, **not merged, no pull request open**).
Related: [ADR-0005](../adr/0005-windows-agent-delivery.md) · [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) ·
[CI and real-install test](../testing/windows-agent-ci-and-e2e.md) · [pipeline](../planning/2026-10-07-windows-agent-pipeline.md).

## 1. Summary

Goal: send a Windows agent to a client with **one command**, **all dependencies included**, and **auto-troubleshooting**;
everything else stays in the pipeline.

| | |
|---|---|
| Delivered | a compiled Windows agent built in CI; a one-command installer with checks before it changes anything; `doctor`, `status` and `support-bundle`; a status file, rotating log and crash recording; agent version management (the agent reports its version and asks the manager about updates); an operator guide and a decision record |
| Proven on a real Windows runner | the build, the package, and a real install, repair and removal: **22 of 22 checks** (run 18) |
| First field install | on 7 Oct the owner installed it on a real Windows PC. It **registered and was auto-approved**, but never connected: the compiled build was missing part of the `websockets` library (F-3). Fixed in `e854f03` (agent 2.2.1); the rebuild is the next thing to confirm |
| Not yet proven | a live connection to the manager from the installed agent; a reboot; the UAC prompt; a clean machine; a customer's endpoint product |
| Open decisions | F-1 (scan results archived in a user-readable folder); how to mint tokens while Fleet's button is blocked by the missing Linux release; a signing identity |

## 2. What was built

| Area | What | Main files |
|---|---|---|
| Compiled build | Nuitka standalone folder, MinGW gcc, closure-only (77 modules), whole `websockets` package, impacket trimmed; "no source" check | `probe/windows/build-agent-exe.ps1`, `probe/tools/agent_closure.py` |
| Installer | one command; self-elevation; integrity check; `doctor --preinstall`; install, backup and restore; wait for online; token removed; `-Repair`, `-Uninstall [-Purge]`, `-Proxy`, `-CaBundle`, `-Scope`, `-TokenFile` | `probe/windows/install.ps1`, `install.cmd`, `package-zip.ps1` |
| Self-help | `doctor`, `status`, `support-bundle`; status file; rotating log; crash recorded; keep retrying an unreachable manager; fall back to polling if push mode cannot load | `probe/agent/diagnostics.py`, `runtime_status.py`, `agent.py` |
| Version management | `AGENT_VERSION`, CI gate, manifest field, heartbeat version, `POST /agents/update-check`, startup and 6-hourly check | `probe/agent/version.py`, `update_check.py`, `manager/backend/app/agent_release.py`, `routers/agents.py` |
| CI | build, tests under PowerShell 7 and 5.1, smoke, the real-install test, artifact | `.github/workflows/agent-windows-build.yml`, `agent-version-gate.yml` |
| Docs | operator guide, reference, decision record, design, test doc, research memo, pipeline | this folder tree |

## 3. Timeline

| Step | Result |
|---|---|
| Runs 1-13: get the compiled build to work | failed on missing Nuitka version fields, then on MSVC running out of heap (twice), then a `$PSScriptRoot` bug, then green at run 13 with MinGW, a trimmed impacket and a compile cache |
| Version management, diagnostics, installer written and unit-tested locally | 11 commits (see section 6) |
| Run 14 | first run with the installer: logic tests passed under PowerShell 7 and 5.1; the troubleshooting step failed on a runner quirk (section 4, #1) |
| Run 15 | first real install on Windows: **7 of 22** checks passed; the installer stopped at `Get-FileHash` (#2) |
| Run 16 | 19 of 22 |
| Run 17 | 21 of 22; the last failure showed the agent giving up after six manager checks (#6) |
| Run 18 | **22 of 22**; artifact uploaded |
| Field install by the owner (agent 2.2.0) | registered, never connected (#7, #8) |
| Run 19 (agent 2.2.1, commit `e854f03`) | **green**: build (a 16-minute first compile of the whole `websockets` package), smoke test with the new `runtime-check`, troubleshooting, packaging, **22 of 22** install checks; artifact 31.9 MB. **Not yet confirmed on the owner's machine** (a repair install from this build) |

## 4. Defects found, and what each taught

| # | Found by | Symptom | Cause | Fix | Caught by CI now? |
|---|---|---|---|---|---|
| 1 | run 14 | the "troubleshooting commands" step failed with a correct result | the runner ends a `pwsh` step with the last native command's exit code, and `doctor`'s expected 1 came last | reset `$global:LASTEXITCODE` after the checks | yes |
| 2 | run 15 | the installer stopped: `Get-FileHash` not recognized | **not isolated** (a child Windows PowerShell can find it on its own) | the installer hashes with .NET and starts from Windows PowerShell's own module folders | yes (the real-install test) |
| 3 | run 15 | `-Uninstall -Purge` said "Deleted" and the folder remained | the installer's own log was open inside the folder | delete after the log closes, with retries; report the truth | yes |
| 4 | run 16 | the test failed calling an installer helper | the test depended on the code it tests, and dot-sourcing would overwrite its variables | the test parses `agent.env` itself | yes |
| 5 | run 16 | the installed agent reported "starting" then "not running" with no reason | a Scheduled Task has no console; a traceback is lost | any crash is written to the log and status; the test dumps evidence at the moment of failure | yes |
| 6 | run 17 | the agent gave up after six manager checks and exited with code 2; the status stayed at "starting" | the Linux behaviour (exit, let the container restart it) is wrong for a Windows task, and the message told Windows users to re-run a Linux script | `PROBE_KEEP_RETRYING` (set by the Windows installer); the status updates after the first failed check | yes |
| 7 | **field install** | registered, but Fleet never showed the agent; the log repeated `No module named 'websockets.asyncio'` | `websockets` loads a submodule lazily by name; Nuitka cannot see that; `runtime-check` imported only the top-level package | include the package; `runtime-check` exercises the real connection, HTTPS and key paths (a test proves it fails a broken build); **agent falls back to HTTP polling if push mode cannot load** | **yes (the gate), but only for a missing library; a protocol fault still needs X2 in the pipeline** |
| 8 | field install | local `status` said ONLINE while the agent was not connected | the status was only ever set to "online", never back | a lost connection or an unreachable manager is recorded as "retrying" | yes (unit tests) |
| 9 | reading the real-install log | scan payloads are archived in `C:\Program Files\Vedha Agent\result`, indefinitely, readable by standard users | the archive default is a folder next to the code | **open (F-1)** | no |
| 10 | the owner asking for a token | the Fleet button is gated on a published Linux release | `AddAgent.tsx` uses `info.available` | **open**; the API route is documented | no |

Two lessons that shaped the work:

- **A green build gate is only as good as what it exercises.** Importing a package is not using it. The
  `runtime-check` now does real work with each critical library, and a test breaks the build on purpose
  to prove the gate notices.
- **CI cannot stand in for the first real install.** A real-install test with an unreachable manager
  proves the installer; it cannot prove the connection. A protocol-level fake manager in that test is
  the next investment ([pipeline X2](../planning/2026-10-07-windows-agent-pipeline.md)).

## 5. First field install (7 Oct 2026, agent 2.2.0, real Windows PC)

What the agent's own log showed (host details left out): the manager was reachable; a new identity was
generated; **"Probe pre-authorized via enrollment token - auto-approving, no code needed"**; **"Registered as
'<computer>-probe'"**; the scan ceiling covered the host's /24; and then, every minute with a growing pause,
`WebSocket error: ModuleNotFoundError: No module named 'websockets.asyncio' - reconnecting`. So the token,
the enrolment, auto-approval, the scope check and the HTTPS path to the manager all **worked on a real
machine**; only the live connection was broken, which is why the agent never heartbeated.

The install itself (installer, task, permissions, log) behaved as the real-install test predicted.

## 6. Commits on the branch

| Commit | Change |
|---|---|
| `214632f` `8fb81e9` `75eaa56` `a51ebda` | make the Nuitka build work: version fields, trim impacket, MinGW, output folder, cache |
| `6f41f80` `7f0a22f` | version management and its docs |
| `a4e8054` | `doctor`, `status`, `support-bundle`, status file, rotating log |
| `2bea0cc` | the one-command installer, packaging, tests |
| `7fc7abe` | runner exit-code quirk; refused vs dropped connections in `doctor` |
| `2e33ee6` `72363e0` | operator guide |
| `735f063` | installer independent of `Get-FileHash`; purge fixed |
| `558d1e7` | crash recording; evidence capture in the real-install test |
| `96160d9` | keep retrying an unreachable manager |
| `e854f03` | `websockets` shipped; polling fallback; status tells the truth; agent 2.2.1 |
| `13b3dbb` and later | documentation |

## 7. Honest limits of this report

- Everything marked "proven" ran on a GitHub-hosted `windows-latest` runner or, for one install, on the
  owner's machine. Nothing was run against a customer's environment or a customer's endpoint product.
- The token commands in the operator guide were written from the code and had not been run by me
  against the live manager (my sandbox cannot reach it); they were run by the owner.
- Competitor and incident points in the research memo come from search results, not full reads.
- The cause of the `Get-FileHash` failure was not found.
