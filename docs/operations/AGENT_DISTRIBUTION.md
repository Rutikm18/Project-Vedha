# Agent distribution — operator runbook

How the Vedha agent reaches a customer's network, and how platform images reach
an on-prem customer. Design and reasoning:
[`planning/2026-10-01-agent-install-approach.md`](../planning/2026-10-01-agent-install-approach.md) §10.

## The model in one paragraph

Vedha is centrally hosted at `api.vedhasec.com`. Customers get **only the
agent**, and they get it **from the manager**, never from a public registry. You
build and sign a release (CI does this on a tag, see below); the manager serves
it; a customer clicks **Fleet → Add agent**, copies one command containing a
single-use install token, and runs it on a Linux host (`curl … | sh`) or a
Windows host (one PowerShell or cmd command). The installer verifies the
release signature and the package checksum before running anything, and the
agent enrols itself into that engagement with the engagement's scope. Customers
who must run the whole platform on their own premises get an **encrypted,
signed bundle made for them alone**, on request.

```
build machine                         manager (api.vedhasec.com)            customer Linux host
─────────────                         ──────────────────────────            ───────────────────
make agent-release ──signed──▶  agent-releases/ (read-only mount)
   (private key stays here)        GET /agent/install.sh     (public) ◀── curl … | sh -s -- --token vet_…
make agent-publish TO=…            GET /agent/manifest.json(.sig)     ◀── verify signature (OpenSSL 3)
                                   GET /agent/image/{arch}  (token)   ◀── verify SHA-256, docker load
                                   POST /probe-enrollment/requests    ◀── agent enrols with the token
```

## Two signing keys, why

| Key | Used by | Manager setting |
|---|---|---|
| Ed25519 | `install.sh` (Linux) verifies it with OpenSSL | `AGENT_RELEASE_PUBLIC_KEY` |
| ECDSA P-256 | `install.ps1` (Windows) verifies it with the built-in .NET/CNG crypto | `AGENT_RELEASE_P256_PUBLIC_KEY` |

Windows PowerShell 5.1 / .NET Framework cannot verify Ed25519, so a release that
ships a Windows package carries a **second signature over the same
`manifest.json`**. Linux installs are unaffected: a release without Windows is
byte-for-byte the schema-1 format older managers and installers expect. Each
installer has its key baked in when the release is built, so a swapped
manifest, package or signature is caught before anything runs.

## One-time setup

1. **Create the release signing keys** (build machine — never the server):
   ```bash
   make agent-keygen          # Ed25519, for Linux  -> AGENT_RELEASE_PUBLIC_KEY=…
   make agent-keygen-p256     # P-256, for Windows  -> AGENT_RELEASE_P256_PUBLIC_KEY=…
   ```
   They write `~/.vedha/agent-release-key.pem` and `~/.vedha/agent-release-p256-key.pem`
   (mode 600) and print the public halves. Back the private keys up offline; anyone
   holding one can sign agents your customers will trust. Neither command overwrites
   an existing key.
2. **On the manager**, add to `.env` and restart the API (`make full`):
   ```
   AGENT_RELEASE_PUBLIC_KEY=<printed value>
   AGENT_RELEASE_P256_PUBLIC_KEY=<printed value>
   MANAGER_PUBLIC_URL=https://api.vedhasec.com        # make tls already sets this
   ```
   In production the manager refuses to serve a release that is unsigned or
   doesn't verify against these keys. Without the P-256 key it serves Linux only
   and withholds the Windows package (Fleet shows the reason to operators).
3. **Migration 0052** (engagement-bound tokens) runs with the normal deploy.

## Releasing with CI (recommended)

`.github/workflows/agent-release.yml` builds, signs, verifies and publishes a release so
nobody signs from a laptop and no SSH key to the manager exists in CI.

**One-time GitHub setup**

| Where | Name | Value |
|---|---|---|
| Settings → Environments → new `agent-release` (add required reviewers if you want an approval gate) | secret `AGENT_RELEASE_SIGNING_KEY` | contents of `agent-release-key.pem` |
| same environment | secret `AGENT_RELEASE_P256_KEY` | contents of `agent-release-p256-key.pem` |
| Settings → Variables (public values) | `AGENT_RELEASE_PUBLIC_KEY`, `AGENT_RELEASE_P256_PUBLIC_KEY` | the printed public keys — the pipeline verifies its own output against **these**, so a wrong or rotated key fails in CI, not in the field |
| optional, environment secrets | `WINDOWS_CODESIGN_PFX_BASE64`, `WINDOWS_CODESIGN_PFX_PASSWORD` | Authenticode certificate (see below) |
| optional, variable | `AGENT_REQUIRE_AUTHENTICODE=true` | fail the release if the Windows exe could not be signed |

**Cut a release**

```bash
# VERSION is bumped by the commit hook; the tag must equal it
git tag agent-v$(cat VERSION) && git push origin agent-v$(cat VERSION)
```

The run builds the Linux images (amd64 + arm64), the SBOM and the Windows package
**without ever seeing a key**, then the `sign` job (the only one with the keys) assembles
and signs the release and verifies it against the pinned public keys. `windows-verify`
then runs the signed release's real `install.ps1` on Windows PowerShell 5.1 against a
stub manager: it must verify the release and **refuse** a tampered manifest, signature,
package, truncated or oversize download and a redirect, plus a bad token; it also
exercises the Authenticode pin with a throwaway certificate and a real
install/uninstall. Only then does `publish` attach the files to an immutable GitHub
Release (plus a build-provenance attestation on public repositories). A tag that does
not match `VERSION` is rejected. You can also run the workflow by hand (Actions → agent-release →
Run workflow) to get the signed files as a run artifact without publishing.

**Put it on the manager** (on the manager host, no CI access needed):

```bash
make agent-pull REPO=<owner>/<repo> TO=/opt/Project-Vedha/manager/agent-releases
# private repository: export GITHUB_TOKEN=<token that can read the repository's contents> first
# a specific version / rollback:  … TAG=agent-v1.0.371
```

`pull` downloads the newest published agent release, **re-verifies both signatures against
the keys in the manager's `.env`**, checks every file against its signed SHA-256 and that
the manifest's version equals the tag, and only then installs it and makes it current.
Nothing reaches the store if anything fails. It takes only files the signed manifest
lists, refuses to overwrite an existing version, and announces a rollback. The manager
notices the new `CURRENT` on its next request; Fleet → Add agent shows the new version.

**Rotating a key.** Generate the new key, update the GitHub secret and variable, publish a
new release signed by it, then in ONE maintenance step update the manager's `.env` and run
`make agent-pull` for that release (until both are done the manager fails closed:
installs are refused, nothing unsigned is served). Customers who already installed are
unaffected; the key only gates new installs and upgrades.

## Publishing a release by hand

The path CI replaces; still valid for a build machine without CI.

```bash
make agent-release                       # amd64 + arm64, version from VERSION
make agent-verify PUB=<AGENT_RELEASE_PUBLIC_KEY>
make agent-publish TO=ubuntu@<server>:/opt/Project-Vedha/manager/agent-releases
```

A release with Windows needs a built Windows package (made on Windows, see the Windows
section): `make agent-release WINDOWS_ZIP=path/to/vedha-probe-win.zip` and
`make agent-verify PUB=… P256_PUB=…`.

- Cross-architecture builds use `docker buildx` (Docker Desktop ships the
  emulation). `AGENT_ARCH=amd64` builds one.
- Publishing copies the version directory first and switches `CURRENT` last,
  so the manager never serves a half-copied release. Old versions stay for
  rollback.
- Releases are immutable: a version directory is never overwritten. Commit (the
  VERSION hook bumps it) before building again.
- Check Fleet: the Add agent panel shows `Agent <version> · amd64, arm64 ·
  signed (<key id>)`.

**Roll back:** on the server, `echo 1.0.338 > /opt/Project-Vedha/manager/agent-releases/CURRENT`.
The manager notices on the next request.

**Local development:** `make agent-publish TO=manager/agent-releases`; leave
`AGENT_RELEASE_PUBLIC_KEY` empty to serve unsigned releases outside production.

## What the customer gets

Fleet → **Add agent** (operator: pick the engagement; portal: the customer's own
engagement) → **Generate install command**:

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://api.vedhasec.com/agent/install.sh \
  | sudo sh -s -- --manager https://api.vedhasec.com --token vet_…
```

- The token is **single-use, bound to one engagement**, and valid for the lifetime
  chosen in the panel: **1 hour, 24 hours (default) or 7 days**. At most 5 unused
  ones can exist per engagement. It is stored only as a hash.
- It downloads the image (`/agent/image/{arch}` refuses anything without a live
  token) and auto-approves enrolment; the agent's Site is built from the
  engagement's scope **at enrolment time** and the agent is assigned to the
  engagement. If the engagement can no longer take an agent, enrolment falls
  back to manual code approval — it never widens scope.
- The panel flips from "waiting for install" to "agent enrolled" by itself.
  Revoke an unused command there.
- Customer-facing instructions: [`probe/CUSTOMER_AGENT_INSTALL.md`](../probe/CUSTOMER_AGENT_INSTALL.md).

## The Windows agent

Fleet → Add agent shows a **Linux / Windows** switch once the published release has a Windows
package. The Windows commands carry the same single-use token:

```powershell
# PowerShell opened with "Run as administrator"
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm 'https://api.vedhasec.com/agent/install.ps1'))) -Manager 'https://api.vedhasec.com' -Token 'vet_…'"
```
```bat
:: cmd.exe (asks for administrator rights itself)
curl.exe --proto =https --tlsv1.2 -fsSL "https://api.vedhasec.com/agent/install.cmd" -o "%TEMP%\vedha-install.cmd" && "%TEMP%\vedha-install.cmd" "https://api.vedhasec.com" "vet_…"
```

What `install.ps1` does, in order, stopping at the first thing that does not check out:

1. fetch `manifest.json` and `manifest.json.p256.sig`, verify the signature with the key baked into the
   script — **before** any package is downloaded or the token is sent anywhere;
2. download `/agent/package/windows` with the token (redirects refused), check size and SHA-256
   against the signed manifest;
3. if the release pins an Authenticode certificate, require `vedha-agent.exe` to carry a valid
   signature from exactly that certificate;
4. unpack (refusing `..`, absolute, drive and `:stream` paths and oversize archives) and run the
   packaged `install.ps1`, which registers the Scheduled Task **VedhaAgent** (SYSTEM, starts at boot).

The token lives only in `C:\ProgramData\vedha-agent\enroll.token`, readable by SYSTEM and
Administrators, and is deleted as soon as the agent has enrolled. The same folder holds the
agent's identity key, so it is locked to SYSTEM and Administrators too (consequence: `run.cmd`,
the attended mode, needs an administrator prompt after a permanent install).
`install.ps1 … -VerifyOnly` does steps 1–3 and the unpack without installing or needing
administrator rights — the way to audit a release. Re-running the command with a fresh token
upgrades; `uninstall.ps1 -Purge` removes everything.

**Trust model, plainly.** The installer script itself arrives over TLS from the manager, so
TLS to the manager is the root of trust for the script. The signatures then protect everything
the script downloads: a swapped or tampered package, a replayed older manifest (the version must
match the script's), a changed mirror. They do not protect against a manager that serves a
different script. Compare the key id shown in Fleet with the one you generated if that matters.

**Authenticode (no certificate yet).** Until `WINDOWS_CODESIGN_PFX_BASE64` is configured the
release ships `vedha-agent.exe` **unsigned** and the pipeline says so with a warning; Windows
installs are then protected by TLS + the SHA-256 pin + the signed manifest, and SmartScreen /
EDR will treat the exe as unsigned. Once you buy a code-signing certificate, add the secret
(a `.pfx`, base64-encoded) and the next release signs the exe, proves the signature, and pins
the certificate's thumbprint into the signed manifest so the installer insists on it. Since 2023
most certificate authorities issue code-signing keys on hardware or in a cloud HSM and will not
give you an exportable `.pfx`; in that case use the signing service's own CI integration in place
of the PFX step in `windows-package` (the rest — thumbprint pinning and the installer check —
is unchanged). Signing improves reputation and tamper evidence; it does not by itself make AV/EDR
allow-list a network scanner, so tell the customer's security team to allow `vedha-agent.exe`.

## Agent access expiry (set from Fleet)

Every connected agent in Fleet shows **no expiry / expires `<date>` / access expired**.
Operators set it with **Extend +7 / +30 / +90 days** or **Clear** (API:
`PATCH /agents/{id}/access-expiry`, audited as `agent.access_expiry.set`). The
customer sees the date read-only in the portal.

- **Enforced only on the manager**, so a changed host clock or a patched binary
  cannot get around it. Past the date the manager refuses the agent's heartbeats,
  job polls, token refreshes and WebSocket connection, and hands it no new jobs.
- A scan **already running** at expiry finishes and may still upload its results;
  the agent is then disconnected on its next idle heartbeat.
- The agent does **not** stop or re-enrol. It keeps its identity, logs "access has
  expired", and re-checks every 5 minutes (`PROBE_EXPIRED_RETRY_SECS`, 30–3600).
  **Extend the date and it resumes by itself** within that window; no reinstall.
- Expiry is separate from the install command's lifetime: the command lifetime
  limits how long a *new install* can start; access expiry limits how long an
  *installed agent* may work.

## What ships to the customer (code boundary)

The agent contains **only its own code**: the 73 modules in its import closure
(`probe/tools/agent_closure.py`). The vulnerability judgement rules
(`scanner/findings.py`), the campaign runner, accuracy gates, `main_scripts/`,
`cve/` and tests never leave the repository, and detection stays on the manager.

- CI and every image build run `agent_closure.py --check`: a blocked module or a
  dynamic import (which a compiler cannot follow) fails the build.
- `vedha-agent runtime-check` imports every module and library the agent can load
  at run time. The standard image build runs it; the **sealed** (compiled) build
  is checked by `make seal-parity`, which also fails if any Python source,
  bytecode or `findings` module is in the image.
- Compiled agents carry no source, bytecode or docstrings. String constants (port
  lists, banner patterns) are still readable with tools; hiding those needs
  Nuitka's commercial tier (pipeline).
- The Windows compiled build (`probe/windows/build-agent-exe.ps1`) uses the same
  closure-only recipe; it is built and smoke-tested on a Windows runner by
  `agent-windows-build.yml` (every change) and `agent-release.yml` (every release).

## On-prem customers (on request only)

1. The customer creates an age key pair and sends you **only the public key**:
   `age-keygen -o vedha-age-key.txt` → `Public key: age1…`.
2. Build their bundle (includes the current agent release if one is built):
   ```bash
   make onprem-bundle CUSTOMER="ACME Bank" RECIPIENT=age1…
   ```
   Output in `dist/onprem/`: `vedha-onprem-acme-bank-<v>.tar.age` (encrypted to
   them only), `vedha-onprem-load.sh` (your public key embedded), the `.sha256`,
   and `ledger.jsonl` (one line per bundle: id, customer, checksum).
3. Deliver the `.tar.age` + loader through a **time-limited link** (e.g.
   `aws s3 presign … --expires-in 259200`). Give the **SHA-256 over a different
   channel** (phone, Signal). The link alone is useless: only their private key
   decrypts it.
4. They run:
   ```bash
   sh vedha-onprem-load.sh vedha-onprem-acme-bank-<v>.tar.age \
      --identity vedha-age-key.txt --sha256 <value you told them> --dir /opt/vedha
   ```
   The loader refuses on a checksum mismatch, a wrong key, a bad signature, a
   file that doesn't match, an unlisted file or an unsafe path.

Keep `ledger.jsonl`: if a bundle turns up somewhere else, its `bundle_id` (in
`bundle-manifest.json` on their side) tells you whose copy it was.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Fleet: "agent installer is not available" | No `CURRENT`, bad signature, missing `AGENT_RELEASE_PUBLIC_KEY`, or a file changed after signing | The panel shows the exact reason to operators; republish, or fix the key |
| Installer: "release signature does NOT verify" | Release signed with another key than the installer trusts | Never bypass. Republish with the right key |
| Installer: "install token was refused" | Expired (24 h), used, or revoked | Generate a new command |
| Installer: "could not reach" / TLS errors | Egress, DNS, proxy, TLS inspection | `--proxy http://proxy:3128`, `--ca-bundle corp-ca.pem`, or exempt the manager from inspection |
| Agent online but scans blocked mid-way | Customer IPS/NAC | Allow-list the agent IP; see the checklist in the panel |
| Windows installer: "manifest signature does not verify" | The release was signed with a different P-256 key than the one baked into the script, or a mirror altered the manifest | Never bypass. Check `AGENT_RELEASE_P256_PUBLIC_KEY` on the manager equals the key CI signs with; republish |
| Windows installer: "has no Windows agent release to offer" | The published release has no Windows package, or the manager has no P-256 key (production withholds it) | Fleet shows the reason to operators; set the key / publish a release built with Windows |
| Windows installer: "install token was refused" | Expired, used or revoked | Generate a new command |
| Windows installer: "PowerShell policy blocked the packaged installer" | Group Policy enforces an execution policy | Run the command exactly as shown (it starts PowerShell with `-ExecutionPolicy Bypass` for that process); if GPO still blocks it, have IT allow it |
| Windows installer: "Refusing an http:// manager" | Lab manager without TLS | Use https; for a lab only, add `-AllowInsecureHttp` (the token then crosses the network in clear text) |
| Windows installer: package incomplete / file missing | Antivirus quarantined `vedha-agent.exe` while unpacking | Allow-list it and run the command again |
| `make agent-pull` fails "does not verify" | The manager's `.env` keys differ from the ones CI signs with, or the GitHub release was altered | Never bypass. Fix the key or republish |
| Fleet shows "access expired" | The date set in Fleet passed | Extend it in Fleet; the agent resumes within 5 minutes |
| Agent log: "access has expired … Waiting" | Same | Same. Nothing to reinstall |
| Agent shows pairing code although a token was used | The engagement already had an agent or lost its scope when the agent enrolled (fallback by design) | Approve the code in Fleet, or fix the engagement and reinstall |
