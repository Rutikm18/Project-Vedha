# Sharing the agent with a client: security review and checklist

Internal. 3 October 2026. Answers "is it safe to send the agent to a client, what do I send, and does any code leak?". The answers come from building the real release image and inspecting it, and from running the real installer end to end against a test manager.

## Short answers

| Question | Answer |
|---|---|
| Is it secure to send? | **Yes, if you send the client kit and follow the checklist below.** The client downloads the agent from your manager with a single-use token. The installer refuses anything that is not signed by your release key or that does not match its checksum. The agent runs non-root, read-only, with no Linux capabilities, and only connects outward. |
| What do I send? | **The client kit** (`make agent-client-kit`): `vedha-agent-install.sh` + `INSTALL.md` + `SHA256SUMS`, as one zip. **Separately**, by phone or Signal, send the install token (`vet_…`) and the installer checksum. Never send the image, the repository, `.env`, keys or a PAT. |
| Does code leak? | **The agent's own code, yes; the valuable code, no.** See "Code exposure" below. |

## Code exposure

What a client can read is exactly what is in the image. They can run `docker save` and unpack it, or `docker run --entrypoint sh`.

| Ships to the client (readable) | Stays on your servers (never ships) |
|---|---|
| 73 Python files, about 25,000 lines: the scanners (TCP connect, banners, TLS, SSH, SMB/LDAP/DNS checks), the scan workflow engine, and the agent's connection code | Vulnerability judgement (`scanner/findings.py`), the detection engine and CVE matching, risk scoring, intelligence snapshots, AI prompts, reports, the campaign runner, `main_scripts/`, tests, the manager |

Verified on 3 October:
- The build exports only the import closure.
- The image contains no secrets, private keys, internal host names, customer data or `TODO` notes.
- The image history shows no build arguments.
- The vendored `ssh-audit` data keeps its MIT notice.

**What the readable code reveals.** It shows how the scans are done. It does not show which findings you conclude from them. That conclusion is the valuable part, and it runs on the manager. Comparable logic exists in open-source tools such as nmap and ssh-audit, so this exposure is modest.

**Reducing it further** is possible with a compiled build: `probe/Dockerfile.sealed` (Nuitka) ships no source. It is **not a drop-in switch** today:
- A sealed build always requires a per-host licence, which the token flow does not issue.
- The installer runs `python` inside the image for setup steps, and the sealed image has no Python.
- Free Nuitka still leaves string constants readable.

Making it the default is a planned piece of work:
1. Installer helpers become agent subcommands.
2. Choose a licence policy for sealed token installs.
3. CI builds and seal-parity runs for amd64 and arm64.
4. A full end-to-end test.

Until then, use the contract protections below.

## What is protected, and how

| Risk | Control | Verified |
|---|---|---|
| A tampered or substituted agent | The release manifest is signed with Ed25519, and the installer has your public key embedded. The image's SHA-256 must match the signed manifest. The installer refuses on a mismatch, and **cannot be told to skip the check** (`PROBE_REQUIRE_SIGNATURE=false` is ignored by a signed installer) | End to end: a tampered manifest and a wrong token are both refused |
| A host that cannot verify (old OpenSSL) | Falls back to `python3-cryptography`. Otherwise it **stops** (previously it continued with a warning) | Tested with a fake OpenSSL 1.1.1 |
| A stolen install token | Single-use, bound to one engagement, expires (1 h, 24 h or 7 d), stored only as a hash, revocable in Fleet. `--token-file` keeps it out of shell history and the process list | Token-file path tested |
| The installer swapped in transit | The kit's `SHA256SUMS`, plus the checksum given by phone. The installer prints the signing key ID, which the guide tells the client to compare | Kit checksums tested |
| The agent scanning outside the engagement | The scope comes from the engagement and is enforced by both the manager and the agent | Existing tests |
| An agent left behind after the engagement | Access expiry in Fleet; the manager refuses an expired agent. Uninstall and purge steps are in the guide | Existing tests |
| Upgrades | Re-running a newer installer now **replaces the container and keeps the identity**. Previously it silently kept the old version running | End to end, 1.0.371 to 1.0.372 |

## Before you send anything (once per environment)

- [ ] **Manager in production mode over HTTPS.** Check that
  `curl -s -o /dev/null -w '%{http_code}' https://<app-domain>/api/auth/dev-hint` prints `404`, and that `.env` has `APP_ENV=production`. `make tls` and `make full` now set this. If the hint was ever served, rotate the admin password.
- [ ] **Release signing key.** Run `make agent-keygen` on your build machine, never on the server. Back up the private key offline. Put `AGENT_RELEASE_PUBLIC_KEY` in the manager's `.env`. In production the manager refuses unsigned releases.
- [ ] **A signed release published:**
  ```bash
  make agent-release
  make agent-verify PUB=<key>
  make agent-publish TO=<server>
  ```
  Fleet → Add agent should show "signed (`<key id>`)".
- [ ] **Plain-HTTP API closed** (`make tls … TLS_ARGS=--no-legacy-http`) once no existing probe uses `http://<ip>`.
- [ ] **`PROBE_AUTO_ENROLL=false`** in `.env`. The token flow does not need it.
- [ ] **Your domain categorised** by the main web filters. New domains are often blocked by corporate proxies (see STATUS → *Needs you*).
- [ ] **Paperwork template** ready: a scan authorisation (rules of engagement), and your terms (no reverse engineering or redistribution of the agent, data processing, retention).

## For each client

1. **Agreement first:** signed scan authorisation with scope, time window and contacts. Terms that cover the agent software.
2. In Vedha, create the engagement and set its **scope**. Set an **access expiry** for the agent (the end of the engagement).
3. Build the kit:
   ```bash
   make agent-client-kit CUSTOMER="ACME Bank" MANAGER=https://api.vedhasec.com \
        PUB=<AGENT_RELEASE_PUBLIC_KEY> CONTACT="Name, phone, email"
   ```
   It writes `dist/client-kit/vedha-agent-kit-acme-bank-<version>.zip` and prints the installer checksum. The builder verifies the release against `PUB` and refuses a development installer or an `http://` manager.
4. Send the **zip** by email or file share.
5. In Fleet → Add agent, generate an install command with the **shortest lifetime that works**. Read the **token** (`vet_…`) and the **installer checksum** to the client by phone or Signal. Never put them in the same email as the zip.
6. Stay on the call while they install: Fleet should flip to *agent enrolled*. If it doesn't, revoke the token.
7. Before the first scan, confirm the client has told their SOC and allow-listed the agent's IP in IPS/NAC.
8. **At the end:** let access expire (or remove the agent in Fleet), ask the client to run the "remove completely" step, and record it.

## Known limits and next steps

| Item | Effect | Next step |
|---|---|---|
| Agent source is readable | Scanner technique visible to the client | Sealed build as the default (see above). Until then, rely on contract terms |
| Token stays in the container's environment after use | Visible to anyone with `docker inspect` on the client host; already spent, so it cannot be reused | Remove it from the env file after the first enrolment |
| Base image is a floating tag (`python:3.12-slim`) | Two builds of the same version can differ (it already moved to Debian 13) | Pin by digest. Scan with Trivy or Grype and attach an SBOM to each release |
| Linux with Docker only | Windows clients need a Linux VM | The Windows build (`probe/windows`) has not been run yet |
| Bridge network | The agent scans from behind Docker NAT: TCP scans work, layer-2 discovery does not | As designed |
