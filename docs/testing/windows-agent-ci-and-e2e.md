# Windows agent - CI, the real-install test, and what each failure taught us

Workflow: `.github/workflows/agent-windows-build.yml` (name `vedha-agent-windows-build`).
Related: [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) · [reference](../probe/WINDOWS_AGENT_REFERENCE.md) ·
[ADR-0005](../adr/0005-windows-agent-delivery.md) · [bring-up report](../reports/2026-10-07-windows-agent-bringup-report.md).

## 1. What the workflow proves

It runs on a real `windows-latest` runner, on a manual run ("Run workflow", input `manager_url`,
default `https://api.vedhasec.com`) and on pull requests that touch the agent, scanner, workflow,
Windows scripts, the closure tool or the runtime requirements. A pull request run has no
`manager_url`, so its package carries the placeholder `https://api.example.invalid`, which the
installer refuses: **never send a package from a pull request run.**

| # | Step | What a pass means |
|---|---|---|
| 1 | Closure check (`tools/agent_closure.py --check`) | only the agent's own 77 modules are compiled; no blocked module or dynamic import |
| 2 | PowerShell scripts parse | all installer, packaging and test scripts are valid PowerShell |
| 3 | Installer logic tests, PowerShell 7 **and** Windows PowerShell 5.1 | the installer's helper functions (settings text, token and scope checks, integrity check, permission check, hashing, folder removal) behave; 5.1 is what customers run |
| 3b | **Hosted one-command download tests** (PowerShell 7 and 5.1): `windows/hosting/tests/Test-Get.ps1` | `hosting/get.ps1`'s checks and its whole download, hash check and unpack against a web server on the runner (51 assertions) |
| 4 | Restore Nuitka cache | warm compile |
| 5 | **Build the compiled agent (Nuitka)** | the agent compiles with MinGW gcc, then `runtime-check` runs on the compiled exe |
| 6 | Save Nuitka cache | kept even if a later step fails |
| 7 | Smoke test | `version`, `hostid`, `runtime-check`, `manifest` (22 capabilities) work in the compiled exe |
| 8 | Troubleshooting commands work in the compiled agent | `help` lists doctor/status/support-bundle; an unknown command exits 2; `doctor --preinstall` against an unreachable manager exits 1 and names the cause |
| 9 | No source or bytecode of ours in the output | no `.py`/`.pyc` from our packages, no `findings` module |
| 10 | Package | `package-zip.ps1` builds the zip with the manager address, checksums and allow-list |
| 11 | **Install the customer package for real (end to end)** | section 3 |
| 12 | Upload artifact `vedha-agent-windows` | the zip, its `.sha256` and `vedha-agent-win.release.json` (read by `publish-to-s3.sh`) |

Typical time: a warm build about 5 minutes of compiling plus about 2 minutes of tests; a cold build
28-38 minutes; the first run after adding new modules (for example the `websockets` package) compiles
them once and is slower. The job timeout is 120 minutes.

## 2. The compiled build

`probe/windows/build-agent-exe.ps1` runs Nuitka in `--standalone` folder mode:

- from an **export of the agent's import closure only** (`agent_closure.py --export`), so nothing
  outside the agent's own code is compiled;
- `--mingw64` (MinGW-w64 gcc, downloaded by Nuitka);
- `--include-package` for `agent`, `scanner`, `workflow`, `ldap3`, `dns` and `websockets`;
- impacket **not** whole: only the modules the scanners import, with `impacket.examples` and
  `impacket.dcerpc.v5.tsts` excluded; `paramiko` and `winrm` excluded on purpose;
- `--python-flag=no_docstrings,no_asserts`, `--windows-console-mode=force`, and company, product, file
  and product version taken from the repo's `VERSION`.

`vedha-agent.exe runtime-check` then imports every module and library **and exercises the real entry
points**: a WebSocket connect to a closed local port, an HTTPS request, the identity keys. A library
that loads parts of itself lazily by name (`websockets` does) is invisible to a compiler, and
importing only the top-level package passes while the compiled agent is broken; the gate exists
because that happened once (finding F-3 in the ADR).

## 3. The real-install test (`probe/windows/tests/Test-InstallE2E.ps1`)

It unzips the package exactly as a customer would, runs `install.cmd` (so the real Windows PowerShell
5.1, the real scheduled task, the real permissions and the real compiled agent are exercised) against
a manager address where nothing listens (`https://127.0.0.1:9`), and then removes everything. It
**installs and removes the agent on the machine it runs on**, so it refuses to run anywhere except
GitHub Actions unless `-Force` is given, and refuses if an agent is already installed.

The 25 checks:

| Group | Check |
|---|---|
| The package | has everything a customer needs · bundles its own Python and Visual C++ runtime · manager address and version are baked in |
| Stops before installing | a damaged file is refused and named · a missing agent program (antivirus quarantine) is explained · a non-token is refused · a non-https address is refused · an unreachable manager stops the install with the cause and the fix and changes nothing |
| Install | `install.cmd -Token ...` installs and exits 0 · the program is in Program Files and runs · the task runs the agent directly, as SYSTEM, at startup · the data folder is SYSTEM and Administrators only · `agent.env` is right, has no BOM and carries the token · the install log exists and has no token |
| The running agent | starts and reports "cannot reach the manager" with why and the fix · writes a readable log file |
| Troubleshooting | `doctor` explains and exits non-zero · `status` prints a summary · `support-bundle` has the diagnosis and no secret |
| Repair and removal | `-Repair` keeps the settings and removes the leftover token · `-Uninstall` removes the program and task, keeps identity and logs · `-Uninstall -Purge` deletes everything |
| One command from a hosted location | a hosted download whose hash does not match the command is refused and nothing is installed · one command downloads, verifies and installs the hosted package (run under Windows PowerShell 5.1 against a web server on the runner, as `get.ps1` would be run against S3) and leaves no downloaded files · the hosted install can be removed again |

**What it cannot prove**, and the manual checks that remain: a real enrolment and a live connection to a
manager (the test's manager is unreachable on purpose), a reboot, the UAC prompt (the runner is
already elevated), a clean machine, and a customer's endpoint-security product. They are the
"not yet verified" list in the [operator guide](../probe/WINDOWS_AGENT_INSTALL.md#8-verified-vs-not-yet-verified).

When a check fails the test prints the evidence **at that moment** (agent log, install logs, status,
the data folder's permissions, the task's last result, and a 20-second foreground run of the agent),
because by the end of the run everything has been uninstalled.

## 4. Running things yourself

| What | Command |
|---|---|
| Build and test on GitHub | Actions -> vedha-agent-windows-build -> Run workflow (set `manager_url`) |
| Installer logic tests (any machine with PowerShell 7) | `pwsh -NoProfile -File probe/windows/tests/Test-Install.ps1` |
| Agent tests | `cd probe && python -m pytest tests/test_diagnostics.py tests/test_runtime_gate.py tests/test_update_check.py tests/test_check_agent_version.py tests/test_windows_scripts.py tests/test_agent_closure.py` |
| Closure check | `python probe/tools/agent_closure.py --check` |
| The hosted-download tests (any machine with PowerShell and Python) | `pwsh -NoProfile -File probe/windows/hosting/tests/Test-Get.ps1` |
| The publish script and the CloudFormation template | `cd probe && python -m pytest tests/test_hosting.py` |
| The real-install test on a throwaway Windows machine | `pwsh -NoProfile -File probe\windows\tests\Test-InstallE2E.ps1 -ZipPath <zip> -Force` (it installs and removes the agent there) |
| Agent version gate | `python probe/tools/check_agent_version.py --base origin/main` |

The Linux CI job `agent-ci.yml` runs the same agent test files (plus the rest of the probe suite) on
Linux, macOS and Windows.

## 5. Gotchas found while bringing it up (so nobody repeats them)

| Symptom | Cause | Rule |
|---|---|---|
| Nuitka aborts: file and product version required | a company name was set without a version | pass `--file-version` and `--product-version` |
| `cl.exe` C1002 "out of heap space", then again after trimming | impacket's generated RPC modules overflow MSVC | compile with `--mingw64`; include only the impacket modules the scanners use |
| `Rename-Item '\dist\agent.dist'` fails | `$PSScriptRoot` is empty inside a `param()` default under Windows PowerShell | resolve paths in the script body |
| A step with a correct result fails with "exit code 1" | the runner ends a `pwsh` step with the last native command's exit code, and `doctor`'s expected 1 was last | set `$global:LASTEXITCODE = 0` after the checks |
| The installer stopped at `Get-FileHash` "not recognized" on the first real install | **not isolated**; a child Windows PowerShell can find the cmdlet on its own | the installer hashes with .NET and starts from Windows PowerShell's own module folders |
| `-Purge` printed "Deleted" and the folder remained | the installer's own transcript log was open inside it | delete the folder after the log closes, with retries, and report the truth |
| The test crashed calling an installer helper | dot-sourcing `install.ps1` into the test would overwrite the test's own `$Token` and `$Manager` | a test parses `agent.env` with its own function |
| Agent "starting" then gone, nothing in the log | the agent gave up after six manager checks (exit 2) and a Scheduled Task has no console | `PROBE_KEEP_RETRYING`, crash recording, and evidence capture in the test |
| Registered, never in Fleet, `status` ONLINE | `websockets.asyncio` missing from the compiled build; `status` never went back down | include the package, exercise entry points in `runtime-check`, fall back to polling, record lost connections |
| `gitleaks` fails on a pull request with "GITHUB_TOKEN is now required" | the action needs the token on `pull_request` events | pass `GITHUB_TOKEN` and `pull-requests: read` in `secret-scan.yml` |
| `test_stage_fanout_policy` fails on a small runner | the scanner defaulted to 8 hosts at once, more than the default thread pool (`min(32, cpu + 4)` = 6 on 2 CPUs) can serve | the default follows the pool when it is smaller (fails the same way on a clean `main` with 2 CPUs) |
| `test_service` fails only on Windows | `macos_log_path()` joined a macOS path with `os.path` | use `posixpath` for a macOS path |
| Every run warns `git ... exit code 128` | a stray `probe copy` entry in the repo with no `.gitmodules`; harmless | `git rm --cached "probe copy"` removes it |

## 6. Test counts (7 Oct 2026, local, before the last rebuild)

Installer logic 85 assertions · agent tests (diagnostics, runtime gate, update check, version gate,
Windows scripts, closure, transport, enrolment, manifest, result chunks) 299 passed · real-install
test 22 of 22 on the Windows runner (run 18; the run after the `websockets` fix is in the
[bring-up report](../reports/2026-10-07-windows-agent-bringup-report.md)). A handful of probe tests
that perform real network sweeps (`test_probe_core`, `test_probe_next_features`) hang in the cloud
sandbox used for development; they hang the same way on a clean `main` and do not touch this work.
