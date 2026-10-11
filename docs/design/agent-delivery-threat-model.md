# Agent delivery: what can fail, and what a breach would look like

Date: 2026-10-11 · Scope: building, signing, publishing and installing the Windows agent, the one-command install, and the
first step of automatic update. Written from the code in this repository, not from a test against a live system.
Related: [version management](agent-version-management.md) · [ONE_COMMAND_INSTALL](../operations/ONE_COMMAND_INSTALL.md) ·
[competitor memo](../research/2026-10-07-windows-agent-friction-and-competitors.md).

## The one sentence to remember

**Whoever can sign a release, or change what your manager serves, can run code as SYSTEM on every machine that installs or
updates from it.** Everything below is about making that hard, and about limiting the damage when it is not hard enough.

## 1. Where the trust sits today

```
 your Windows PC            your manager server                      customer machine
 (source, build, keys)  --> (agent-releases/, .env, api)  --TLS-->   (install.ps1, then the agent as SYSTEM)
   private signing keys       public keys in .env                       trusts: the pasted command, TLS to the
   compiled agent             serves install.ps1 + signed manifest      manager, then the manifest signature
```

* The **private keys** (Ed25519 for Linux, P-256 for Windows) sign the manifest. They live as plain PEM files in
  `%USERPROFILE%\.vedha`. They never go to the server.
* The installer script is **served by the manager and is not itself signed**. It carries the release public key, which
  then verifies the manifest and so the package. The root of trust for the script is TLS to the manager and the command the
  person pasted.
* An enrolled agent updates by fetching that same installer (first step of auto-update, off by default).

## 2. Failure and breach points, most serious first

| # | What goes wrong | Effect | What exists | Open / what to do |
|---|---|---|---|---|
| 1 | **The signing key is stolen** from the build PC (malware as that user, a backup, a lost USB stick). It is an unencrypted PEM; Windows does not enforce the `600` mode the tool asks for | Anyone can publish an agent every customer accepts: **fleet-wide code execution as SYSTEM** | The key is never on the server; the script reminds you to back it up (which creates more copies) | Encrypt it or keep it in hardware (a token, an HSM, a cloud KMS: pipeline item "release key in a KMS"); sign only on a dedicated, clean machine; keep at most one offline backup; write a rotation and revocation procedure (none exists: installed machines have the old key baked in) |
| 2 | **The build is poisoned** before it is signed: unpinned `pip install nuitka cryptography` and the runtime requirements, and Nuitka downloads a C compiler (`--assume-yes-for-downloads`) | A backdoored agent that carries your valid signature | The closure check keeps source and secrets out; an SBOM is produced | Hash-locked requirements (pipeline X3), a pinned compiler, build in a clean VM, reproducible-build check, review the SBOM |
| 3 | **The manager server is compromised** (the API, the `agent-releases` folder, `.env`) | An attacker with write access can replace the release **and** the public keys in `.env`, and the next install or update takes their code: this is the same fleet-wide outcome as #1, without stealing any key | The release folder is mounted read-only into the API; with `AGENT_RELEASE_REQUIRE_SIGNATURE=true` the manager refuses an unsigned release | The installer an agent re-fetches comes from the manager, so a compromised manager defeats the signature. **Pin the release key on the machine at install time** and have the agent refuse updates not signed by it; sign the installer script itself; staged rollout and a pause switch (none built) |
| 4 | **The pasted command is swapped** (clipboard malware, a poisoned chat message, a look-alike domain) | The victim runs an attacker's installer, which carries the attacker's key and passes its own checks | Fleet prints the release key id; the script header says to compare it | Tell customers to compare the key id out of band; show a short fingerprint in Fleet next to the command; send the command by a different channel from the engagement details |
| 5 | **A bad release bricks the fleet.** No automatic rollback; every agent with auto-update on moves at once | Loss of coverage, or of the agents' ability to reconnect | Off by default; idle-only; once per version per 24 h; the installer keeps the old folder as `.old` | Rollback when the new agent is not `online` in time, staged rollout, a pause switch, canary group (all unbuilt). Do not enable fleet-wide |
| 6 | **`.env` edited over ssh** by `-ConfigureManager` | The manager's `.env` holds every secret (database, JWT secret, API keys). **A first version of my script created its backup and temporary copy with a default umask, so they could have been world-readable. Fixed today** (`umask 077`, `cp -p`; tested) | Opt-in switch; refuses unexpected lines; only the four settings it owns are touched | Old `.env.bak.*` files accumulate on the server: delete them after checking. The ssh account must be able to run `docker compose`, which is close to root: use a dedicated deploy user with a key and a passphrase, never a shared or password login |
| 7 | **ssh to the server**: first connection trusts whatever key it is shown (trust on first use); password logins can be phished | A fake server receives your release, or a harvested login pushes a release | The script validates `-Server`, so it cannot be turned into an option injection | Check the host key fingerprint on first use, use key-based login, keep a separate account for publishing |
| 8 | **The install token leaks** (chat history, a screenshot, the command line, PowerShell script-block logging, a process list) | A stranger enrols an agent into your engagement before you do | Single-use, engagement-bound, 1 h / 24 h / 7 d; in the new self-elevation the token goes in the environment, not on a command line | The pasted one-liner still carries it on the first window's command line for the length of the install. Use short lifetimes, send by a different channel, revoke unused tokens in Fleet. A different admin account supplying the UAC password may not receive the token (it says so) |
| 9 | **The UAC prompt is a habit.** The one-liner now asks the user to approve an elevated `powershell.exe` | A person trained to click Yes on that prompt will click Yes on a hostile one | The prompt only appears after the token, manager and scope pass strict patterns | Awareness; code-sign so the prompt shows a verified publisher (Authenticode, pipeline P0-3c) |
| 10 | **Update ticket abuse** (`vet_upd-…`) | A stolen agent credential can fetch the public package; a replay inside 15 minutes if Redis is flushed | HMAC under a key derived from the manager secret; 15 minutes; single use in Redis; the agent must exist, be active, be in the same tenant, and be older than the release; a failed check does not spend it; Redis down fails closed (503) | Its key is derived from `jwt_secret`: if that is left at the default the tickets are forgeable. The startup check already rejects a default secret in production: keep it that way. Rotating `jwt_secret` invalidates outstanding tickets (harmless) |
| 11 | **Unsigned build, unsigned installer** | SmartScreen warnings train customers to click through; some endpoint products block it | `ALLOWLIST.txt`, hashes, signed manifest, folder install | Authenticode signing (blocked: needs an account and certificate); sign the `.ps1` files |
| 12 | **Scan data and identity on the machine** | A local user reads results or the agent identity | The data folder is limited to SYSTEM and Administrators; results moved there (F-1) | A retention limit on the results archive is still open |
| 13 | **Compromised agent as a foothold.** The agent scans the customer's network as SYSTEM | An attacker who controls the manager can aim the agent at the network | The manager decides scope; the agent re-validates it against its local scope; job signing exists but is off by default and the manager does not sign jobs | Job signing end to end (pipeline); least-privilege service account instead of SYSTEM |

## 3. What would reduce the most risk, in order

1. **Keep the signing key out of reach**: a hardware token or KMS, a dedicated signing machine, one offline backup, a written
   rotation procedure (#1).
2. **Pin the release key on each machine** and make updates verify against it, so a compromised manager cannot push code (#3, #4).
3. **Build in a clean, pinned environment** and review the SBOM (#2).
4. **Rollback, staged rollout and a pause switch** before anyone turns on auto-update widely (#5).
5. **Authenticode-sign** the executable and the scripts (#9, #11).
6. Operational hygiene on the manager host: a dedicated deploy account, no leftover `.env.bak.*`, `REQUIRE_SIGNATURE=true` in
   production (#6, #7).

## 4. What this note is not

It is a reading of the code and the design, not a penetration test. Nothing here was exploited on a running system, and the
Windows-only steps (the UAC hand-over, the one-shot update task, the real build) have never run on a Windows machine.
