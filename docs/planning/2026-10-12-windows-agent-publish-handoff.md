# Windows agent: build, sign, publish - hand-off (12 Oct 2026)

Written at the end of a long session so a new chat can continue without the history. Read section 1 and 3 first.
Everything described as "built" was unit-tested here; **nothing has been run end to end on a real Windows PC against the
real manager.** The one real run (the owner's PC, section 2) got as far as logging in to the server and was refused.

## 1. The state in one page

* **On `main` (PR #19, merged 12 Oct):** agent 2.2.9 (pinned release key, installer verified against the signed manifest,
  automatic rollback, optional signed expiry), one-line Windows install that elevates itself, auto-update (off by default),
  **opt-in tokenless install** (`AGENT_ALLOW_TOKENLESS_INSTALL`, off by default: a machine installs, shows a pairing code,
  an operator approves it in Fleet with that code), `publish-release.ps1`, the threat model and the secure-delivery design.
* **On branch `claude/serene-bardeen-1uqxzq`, pushed, NOT merged (8 commits ahead of `main`):**
  1. `agent-release-sync` - an opt-in compose service that makes the manager fetch new SIGNED releases from GitHub by itself
     (`agent_release.py watch`, `pull --only-if-newer`; copy in `manager/backend/scripts/`; compose files updated; the
     production compose file now passes `AGENT_ALLOW_TOKENLESS_INSTALL`).
  2. The **build kit** (`scripts/make_agent_build_kit.py`): a 0.5 MB zip with only the agent code and build scripts, one
     `install.cmd` at the root (`probe/windows/kit-install.ps1`): settings screen with defaults, checks the PC and the server,
     then runs `publish-release.ps1`. Also a one-line cloud bootstrap command (`--url`).
  3. `publish-release.ps1 -SshKey`, `-PythonExe`; the release tool honours `VEDHA_SSH_IDENTITY`; **every ssh/scp call now uses
     `StrictHostKeyChecking=accept-new`** (see 3.1); the kit asks for the `.pem` when the login is refused.
* **Do not merge the branch until the owner has decided section 4.** The owner called the ssh-from-a-PC approach a security
  problem (their words: "totally breaches the security"). I did not ask which part; section 3 lists every candidate.
* **Not done / blocked:** no signed release has ever been published to the manager, so Fleet -> Add agent still says "The agent
  installer is not available yet" (correct). GitHub Actions fails in 2-3 seconds with no steps and no logs on every run
  (consistent with the account's billing block, which the owner knew about; the banner text was not read).

## 2. The owner's environment (as stated, not independently verified)

| Fact | Source | Status |
|---|---|---|
| Manager at `16.4.75.44`, Ubuntu on AWS | Fleet showed the address; `ubuntu` assumed | host key accepted, login **refused** (`Permission denied (publickey)`) |
| Public API address `https://api.vedhasec.com` | STATUS.md says production is `api.vedhasec.com` | **never checked** that it resolves to this server with a valid certificate |
| No `.pem` key file found on the PC (Downloads, .ssh, Desktop, Documents, kit folder) | kit output | owner has not said whether the key exists |
| Windows PowerShell 5.1.26100, Python 3.12.10 beside 3.13.14 | kit output | PC checks all passed in the second real run |
| Production compose host holds only `manager/` and `deploy/` (sparse clone) | `deploy/aws/install.sh` | so `make agent-pull` and the repo `scripts/` do not exist on the server |
| GitHub Actions blocked | every run fails in 2-3 s | billing assumed, not confirmed |

## 3. Security review of what was built (candid)

Ranked by how much each matters. "Owner flagged" is unknown: ask.

1. **A build PC with a shell on the production manager.** `publish-release.ps1 -ConfigureManager` uses ssh to (a) copy the release,
   (b) edit the manager's `.env` (every secret) and (c) run `docker compose up -d api`. The login needs docker rights, which is
   effectively root. A long-lived key on a general-purpose Windows PC is the weakest link in the whole chain. The threat model
   (`docs/design/agent-delivery-threat-model.md`, points 1, 6, 7) already listed this; the kit made it easier to do, not safer.
2. **Trust-on-first-use for the server's host key (`accept-new`), added because the "continue connecting?" question confused the
   owner.** A first connection to an impostor is accepted silently; only a later change is refused. Defensible only if the
   fingerprint is checked once by a person. Options in 4.4.
3. **Signing keys are plain PEM files in `%USERPROFILE%\.vedha`** on that PC (threat model #1). Anyone with that file can
   publish an agent that every machine trusts and that runs as SYSTEM.
4. **The cloud bootstrap command trusts its own channel.** The SHA-256 is inside the same command as the link, so if the
   command is replaced the check protects nothing. The kit also holds the agent's source, behind a link that is secret
   only until it expires.
5. **Tokenless install** (on `main`, off by default) lets anyone who can reach the manager download the signed agent and file
   pairing requests. Mitigations exist (code required at approval, caps, rate limits) but in a manager shared by several
   customers the unbound requests are listed to every tenant's admins. Keep it off there.
6. **`install.cmd` runs with `-ExecutionPolicy Bypass`, installs Python through winget, and downloads build tools** (Nuitka fetches
   a C compiler; dependencies are unpinned: threat model #2). Normal for a build machine, but it is exactly the code that
   gets signed.
7. **The release-sync token** (optional, private repo) lives in the manager's `.env`. Read-only "Contents" on one repo limits it.

What is sound and worth keeping: the **manager verifies both signatures and every file against pinned public keys before it
serves anything** (`agent_release.py pull/watch`, `app/agent_release.py`), agents pin the release key and verify the installer
against the signed manifest, rollback exists, and the sync service sees only public keys.

## 4. Better alternatives (recommended direction first)

The principle: **make the signature the only trust anchor and treat every transport as untrusted**, so no person or PC
needs a shell on the manager and the manager needs no inbound access from a build machine. Verification already exists on the
manager; what is missing is a way to get a release to it without ssh.

### 4.1 Recommended: pull-based, no ssh, no GitHub billing needed

```
build + sign (controlled place)  ->  private bucket / URL  ->  manager `agent-release-sync` pulls, verifies, serves
```
* The build/sign step outputs `dist/agent-release/<version>/` (this already exists: `publish-release.ps1` without `-Server`
  stops after step 5 and verifies what it made).
* The folder goes to a **private S3 bucket** (general AWS knowledge, unverified here): the build PC gets a role or presigned
  PUT limited to one prefix and write-only; the manager's instance role gets read-only on that prefix. No ssh key, no `.env`
  edit, no docker rights for the builder.
* **Build:** extend `agent_release.py watch` so its source can be an HTTPS/S3 prefix as well as a GitHub repo. The
  verification code path is unchanged: both signatures against the keys in `.env`, every file against its signed SHA-256,
  version equals the folder name, nothing overwritten, never a rollback. This is a small change (the GitHub downloader is
  the only part that is source-specific) and keeps all current tests meaningful.
* **One-time server step** (done once, by the owner, in the AWS console terminal): put the two PUBLIC keys and the source in
  `.env`, then start the sync service. After that nobody touches the server per release.
* Acceptance tests to write: a release placed in the bucket by someone without the signing key is refused; a tampered file is
  refused; an older version is ignored; a paused store (`PAUSE`) is not touched; the manager role cannot write the bucket.

### 4.2 Move signing keys out of files (do this before real customers)
* Keep the signing keys in **AWS KMS** (asymmetric ECDSA P-256 sign-only keys do exist; whether Ed25519 is available in KMS
  was **not verified**: check, the Linux path uses Ed25519). The key never exists as a file; signing is an API call by a
  tightly scoped role; every use is logged. The Windows installer needs P-256, which is the supported case.
* If KMS is not possible yet: at minimum encrypt the PEM with a passphrase and sign on a dedicated machine that does nothing else
  (threat-model item 1), plus a written rotation and revocation procedure (none exists).

### 4.3 Server access without long-lived keys
* Use **AWS Systems Manager Session Manager** or EC2 Instance Connect (IAM-controlled, audited, no inbound port 22) for the
  occasional human task. Close port 22 to the world. A script should not need a human's key at all once 4.1 exists.

### 4.4 If ssh stays for now (interim, safer than today)
* Make the host-key check **explicit again**: show the fingerprint the owner can compare with the AWS console's instance output,
  or pin it in `kit-defaults.json`; drop `accept-new` as the default.
* Use a **dedicated deploy user** with a passphrase-protected key (or SSH certificates), docker access only, IP-restricted in the
  security group; never a shared admin login.
* Keep `.env` changes out of the script: print the three lines and have the owner paste them once.

### 4.5 Comparison

| | 4.1 pull from bucket | GitHub Actions + sync (built) | ssh from a PC (current kit) |
|---|---|---|---|
| Shell on the manager needed | none | none | yes (docker = root-equivalent) |
| Key files on a PC | signing key only (until 4.2) | none (keys in GitHub environment) | signing key + server key |
| Works while GitHub billing is blocked | yes | **no** | yes |
| Built today | **no** (small change) | yes (needs billing + secrets) | yes |
| Attack if the build PC is compromised | can publish a signed release (fix with 4.2) | n/a | same, plus a shell on the server |

## 5. What to build next, in order

1. **Release source = HTTPS/S3** for `agent_release.py watch` (+ the vendored copy, tests, docs). Smallest step that removes ssh.
2. **Kit default = build only.** `install.cmd` builds, signs and verifies, then prints the one place to put the folder (or uploads
   it with a presigned PUT the owner provides). Server steps and `-ConfigureManager` become an explicit advanced option.
3. **Decide the host-key behaviour** (4.4): revert `accept-new` or pin a fingerprint.
4. **KMS signing spike** (4.2): check Ed25519 support, design the role, add a `sign` step that calls KMS.
5. Fleet "not published" message: lead with the pull-based route once it exists.
6. Retire or harden the cloud bootstrap command (4.4 point 4): sign the bootstrap script or drop it.

## 6. Questions for the owner (do not assume)

1. Which part felt like the security problem: the long-lived key on a PC, the auto-accepted host key, the kit being downloadable,
   tokenless install, or all of it?
2. Is there an AWS account the manager runs in that can hold a private bucket and an instance role? (Decides 4.1.)
3. Does `https://api.vedhasec.com` reach this server with a valid certificate? (Decides the manager address; never checked.)
4. Is the `.pem` for this server lost, or only misplaced? (Only matters if ssh stays.)
5. Can the GitHub billing block be cleared at all? (Decides whether the existing CI route comes back.)

## 7. How to resume

* Repo state: `git fetch && git log --oneline origin/main..origin/claude/serene-bardeen-1uqxzq`. The branch is **not merged**; if a PR
  for it is merged later, restart the branch from `main` (`git checkout -B claude/serene-bardeen-1uqxzq origin/main`).
* Rebuild the kit with the owner's defaults:
  `python scripts/make_agent_build_kit.py --out dist --default-server ubuntu@16.4.75.44 --default-manager-url https://api.vedhasec.com --default-tokenless`
  (the defaults are the owner's values, passed on the command line, not stored in code).
* Tests that cover this work (all passed on the last run): `manager/backend/tests/test_agent_release_pull.py`, `test_agent_release_tool.py`,
  `test_release_sync_compose.py`, `test_tokenless_install.py`; `probe/tests/test_agent_build_kit.py`, `test_kit_install.py`,
  `test_release_trust_integration.py`, `test_auto_update.py`, `test_windows_installer_pwsh.py` (needs PowerShell 7 on PATH);
  `probe/windows/tests/Test-KitInstall.ps1`, `Test-PublishRelease.ps1`, `Test-Install.ps1`; frontend `tests/fleet-install.test.ts`.
* Known unrelated failure: `probe/tests/test_feasibility.py::test_run_scan_logs_a_runtime_estimate` hangs in the sandbox, also on
  code from before this work. Also unrelated and older: backend `test_capability_map.py` and `test_crown_jewels.py` do not
  collect; probe `test_main_scripts_ja4x`, `test_result_archive`, `test_risk_port_coverage`, `test_probe_next_features`.
* Pitfalls met while working: never use `pkill -f` or `pgrep -f` with a pattern that appears in the same command (it kills the shell);
  `next dev` regenerates `manager/frontend/AGENTS.md` (restore it, do not commit it); dev-server pages must be opened as
  `localhost`, not `127.0.0.1`.

## 8. What was not verified

Anything on real Windows (the folder swap, Scheduled Task, UAC, the build, `winget`), a real S3 bucket, a real GitHub release,
the owner's server layout (`/opt/Project-Vedha/manager` with `docker-compose.yml` and `.env` is an assumption), the research
claims in `windows-agent-secure-delivery-design.md` beyond what each cites, and whether `openssh` on the owner's PC is new
enough for `StrictHostKeyChecking=accept-new` (needs OpenSSH 7.6 or later; the PC passed the ssh check but the version was not read).
