# Agent distribution — operator runbook

How the Vedha agent reaches a customer's network, and how platform images reach
an on-prem customer. Design and reasoning:
[`planning/2026-10-01-agent-install-approach.md`](../planning/2026-10-01-agent-install-approach.md) §10.

## The model in one paragraph

Vedha is centrally hosted at `api.vedhasec.com`. Customers get **only the
agent**, and they get it **from the manager**, never from a public registry. You
build and sign a release on your build machine; the manager serves it; a
customer clicks **Fleet → Add agent**, copies one command containing a
single-use install token, and runs it on a Linux host. The installer verifies
the release signature and the image checksum before running anything, and the
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

## One-time setup

1. **Create the release signing key** (build machine — never the server):
   ```bash
   make agent-keygen
   ```
   It writes `~/.vedha/agent-release-key.pem` (mode 600) and prints
   `AGENT_RELEASE_PUBLIC_KEY=…`. Back the private key up offline; anyone holding
   it can sign agents your customers will trust.
2. **On the manager**, add to `.env` and restart the API (`make full`):
   ```
   AGENT_RELEASE_PUBLIC_KEY=<printed value>
   MANAGER_PUBLIC_URL=https://api.vedhasec.com        # make tls already sets this
   ```
   In production the manager refuses to serve a release that is unsigned or
   doesn't verify against this key.
3. **Migration 0052** (engagement-bound tokens) runs with the normal deploy.

## Publishing a release

```bash
make agent-release                       # amd64 + arm64, version from VERSION
make agent-verify PUB=<AGENT_RELEASE_PUBLIC_KEY>
make agent-publish TO=ubuntu@<server>:/opt/Project-Vedha/manager/agent-releases
```

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
- Sending the agent to a client (what to send, code exposure, checklist, `make agent-client-kit`):
  [`SHARING_THE_AGENT.md`](SHARING_THE_AGENT.md).

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
- The Windows compiled build (`probe/windows/build-agent-exe.ps1`, CI job
  `agent-windows-build.yml`) uses the same closure-only recipe. **It has not been
  run yet** — it runs on a Windows runner once the branch is pushed.

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
| Fleet shows "access expired" | The date set in Fleet passed | Extend it in Fleet; the agent resumes within 5 minutes |
| Agent log: "access has expired … Waiting" | Same | Same. Nothing to reinstall |
| Agent shows pairing code although a token was used | The engagement already had an agent or lost its scope when the agent enrolled (fallback by design) | Approve the code in Fleet, or fix the engagement and reinstall |
