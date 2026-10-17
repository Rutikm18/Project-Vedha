# Go-live runbook — zero-knowledge one-command Windows install (approach #2)

**Goal:** a client pastes ONE line and nothing else — no manager IP, key, token or name,
only the generic facade address `get.vedhasec.com` and an opaque single-use code — and the
agent installs and enrols by itself.

```powershell
& ([scriptblock]::Create((irm 'https://get.vedhasec.com/agent/install.ps1'))) -Manager 'https://get.vedhasec.com' -Code 'vac_...'
```

This runbook makes that live on the server you already run. It does **not** create a new
server. Each step is tagged **[MAC]**, **[SERVER]** (your Linux manager host) or
**[WINDOWS-ONCE]** (any Windows box / throwaway VM / CI — needed only to compile the agent).

Built on branch `feat/windows-zero-knowledge-install` and merged into `main` on 17 Oct
(`500bff5a`): install codes, `/agent/redeem`, `-Code` installer, `get.$DOMAIN` facade, Fleet card.
Everything below uses `main`. See the
[plan](../planning/2026-10-13-windows-agent-zero-knowledge-install.md).

---

## Before you start — four things to have

| Need | Value |
|---|---|
| Your domain | `vedhasec.com` (owned) |
| Facade subdomain | `get.vedhasec.com` (or `agent.`/`install.` — your pick, must match everywhere) |
| Manager server | its public IP and SSH login (e.g. `ubuntu@16.4.75.44`) |
| One Windows box, once | to compile `vedha-agent.exe` (Nuitka can't cross-compile from macOS) |

### Footguns (read once — each has bitten a real install)
1. **The server must run `main` from 17 Oct or later.** Nothing works until it pulls that code.
2. **DNS must resolve before Caddy runs**, or the TLS certificate (ACME) fails.
3. **`MANAGER_PUBLIC_URL` must be the facade** (`https://get.vedhasec.com`) in both `install.sh`
   and the publish step — whichever runs last wins, so keep them equal.
4. **Signing keys must be consistent.** Generate them in ONE place and reuse them forever; the
   manager pins the public key, so a second set from a different machine breaks verification.

---

## Step 0 — nothing to push · **[MAC]**

The work is on `main` (merged 17 Oct, `500bff5a`), so there is no branch to push. The server
pulls `main` in Step 2.

---

## Step 1 — add the DNS record · **[your DNS provider]**

One A record at your registrar / DNS host:
```
get.vedhasec.com   A   <your manager's public IP>
```
Wait until it resolves (`dig +short get.vedhasec.com` returns the IP) before Step 3.

---

## Step 2 — redeploy the manager with the new code · **[SERVER]**

SSH to the server and update the checkout the manager runs from, then rebuild + migrate:
```bash
cd /opt/Project-Vedha            # wherever the manager checkout lives
git fetch origin
git checkout main && git pull origin main
make full                        # rebuilds the stack AND runs migrations (gets /agent/redeem + migration 0065)
```
`make full` runs `alembic upgrade head`, so migration **0065** (the `agent_install_codes`
table) is applied automatically. `main` also carries migrations 0066 to 0068, and 0067 locks
`audit_logs` for about 1.5 minutes per million entries. On a server with a large audit log, apply
those first, one at a time, with [migrations-0066-0068-rollout.md](migrations-0066-0068-rollout.md).
Confirm the API is healthy before moving on:
```bash
curl -fsS http://127.0.0.1:8000/health && echo OK
```

---

## Step 3 — bring up the facade (Caddy + TLS) · **[SERVER]**

```bash
cd /opt/Project-Vedha
DOMAIN=vedhasec.com ./deploy/aws/install.sh
```
This writes the `get.vedhasec.com` Caddy block (serving only `/agent/*`, `/agents/*`,
`/probe-enrollment/*`, `/health`), gets a free Let's Encrypt certificate, and sets
`MANAGER_PUBLIC_URL=https://get.vedhasec.com` in `.env`. Verify the cert and route:
```bash
curl -fsS https://get.vedhasec.com/health && echo "facade OK"
```
If this fails with a TLS error, DNS hasn't propagated yet (Step 1) — wait and re-run.

---

## Step 4 — build + sign + publish the release

The agent **binary** is unchanged by this feature, so you compile on Windows **once**; every
later installer change re-publishes from the Mac with the same zip.

### 4a — compile the agent, once · **[WINDOWS-ONCE]**
On any Windows 10/11 box (a throwaway AWS Windows EC2 you terminate afterward is ideal):
```powershell
git clone https://github.com/Rutikm18/Project-Vedha.git
cd Project-Vedha
powershell -ExecutionPolicy Bypass -File probe\windows\build-agent-exe.ps1
powershell -ExecutionPolicy Bypass -File probe\windows\package-zip.ps1 -Release
# → produces probe\windows\dist\vedha-agent-win.zip  (copy this one file to the Mac)
```

> **Simplest alternative (all on Windows):** skip 4b/4c and run the all-in-one publisher,
> which builds, signs, uploads AND configures the server over SSH:
> ```powershell
> powershell -ExecutionPolicy Bypass -File probe\windows\publish-release.ps1 `
>     -Server ubuntu@16.4.75.44 -ManagerUrl https://get.vedhasec.com -ConfigureManager
> ```
> Its signing keys land in `%USERPROFILE%\.vedha` — **back them up**; reuse them for every
> future publish. If you ever publish from the Mac instead, copy those two `.pem` files to
> `~/.vedha` on the Mac first (footgun #4).

### 4b — sign the release (reuses the zip) · **[MAC]**
Generate signing keys **once** and keep them on the Mac (back up `~/.vedha`):
```bash
make agent-keygen
make agent-keygen-p256
```
Then sign a Windows-only release from the zip you copied over:
```bash
make agent-release WINDOWS_ZIP=/path/to/vedha-agent-win.zip AGENT_ARCH=
```
(`AGENT_ARCH=` empty = Windows-only, no Linux Docker images.)

### 4c — publish to the manager + set the keys · **[MAC → SERVER]**
```bash
make agent-publish TO=ubuntu@16.4.75.44:/opt/Project-Vedha/manager/agent-releases
```
Then put the two **public** keys on the server so it will serve the signed release. Print them:
```bash
scripts/agent_release.py pubkey --key ~/.vedha/agent-release-key.pem --p256-key ~/.vedha/agent-release-p256-key.pem
```
SSH to the server, add those two lines to `.env`, keep `MANAGER_PUBLIC_URL` as the facade, and restart the API:
```bash
# on the SERVER, in the compose dir (e.g. /opt/Project-Vedha)
#   AGENT_RELEASE_PUBLIC_KEY=<ed25519 public>
#   AGENT_RELEASE_P256_PUBLIC_KEY=<p256 public>
#   AGENT_RELEASE_REQUIRE_SIGNATURE=true
#   MANAGER_PUBLIC_URL=https://get.vedhasec.com
docker compose up -d api
```

---

## Step 5 — verify the host serves it · **[MAC or anywhere]**

Over the facade (these are the exact paths a client uses):
```bash
curl -fsS https://get.vedhasec.com/agent/manifest.json | head -c 400 ; echo
# expect: a JSON manifest whose "packages" includes an os:"windows" entry
```
In the console: **Fleet → Add agent** should show the agent version and a
**“Windows — one command, nothing to share”** card.

---

## Step 6 — hand a client the one command · **[console]**

1. **Fleet → Add agent → pick the engagement →** the **“Windows — one command, nothing to
   share”** card → **Generate Windows install command**.
2. Copy the single line it shows and send it to the client (chat/email is fine — it holds no
   secret beyond a single-use code).
3. The client runs it in any PowerShell window; Windows asks for administrator itself; the
   agent enrols and appears under **Connected vedha-agents**. The card shows **agent enrolled**
   (and the redeemer IP, so you can sanity-check it was the right machine).

That's the whole flow. No key, no user id, no login — the client only ever has the facade name
and an opaque code.

---

## When you change the installer again (not the agent code)

Just redo **4b + 4c** on the Mac with the same `vedha-agent-win.zip` — no Windows box needed,
because the compiled binary is unchanged. Only if the agent's own Python changes do you rebuild
on Windows (4a).

## Still worth doing (not required to go live)
- **Code signing** (OV cert, cloud HSM) — removes the SmartScreen warning and most EDR blocks;
  the single highest-value hardening. See the code-signing research in the chat / pipeline X1.
- **Authenticode thumbprint in the release** — the installer already enforces it when the
  manifest pins one; it is a no-op until you sign.
## Approach #1 — the air-gapped / download-averse zip (built)

For a client that cannot, or will not, run the download one-liner, hand them a
self-contained zip instead. It's built once on Windows (the compiled agent) and
**repackaged on the Mac in one command** — no Windows box needed to repackage:

```bash
# reuse the vedha-agent-win.zip from the one-time Windows build (step 4a)
make agent-airgap AGENT=/path/to/vedha-agent-win.zip MANAGER=https://get.vedhasec.com
# → dist/vedha-agent-airgap.zip  (+ .sha256 and .release.json)
```

Send the client the zip + its SHA-256, and a one-time `vet_` token (created in
Fleet → Add agent) on a **different** channel. They run, offline-of-download:

```
install.cmd -Token vet_XXXXXXXX
```

The facade URL is baked in, so the client is still never given a manager IP, key
or internal name — only the generic facade and a single-use token. This uses the
`-Token` flow (not the zero-knowledge `-Code`), because a self-contained zip skips
the redeem step. The package is byte-compatible with the Windows `package-zip.ps1`
output and the installer verifies every file against `SHA256SUMS.txt` before it
installs. Builder + tests: `scripts/airgap_package.py`, `probe/tests/test_airgap_package.py`.

---

## Deploying to a NEW server — the short version (most of the pain is now automated)

The first field deploy (14-16 Oct) surfaced a string of gotchas. **They are now baked
into the scripts**, so a fresh server is far fewer steps. On a new box:

1. **DNS:** one A record `get.$DOMAIN -> <server IP>` (+ `app.`/`api.` as usual).
2. **Deploy the manager:**
   ```bash
   sudo RELEASE_REF=<signed-tag-or-sha> DOMAIN=yourdomain.com ./deploy/aws/install.sh
   ```
   (`REQUIRE_SIGNED_RELEASE=0` only if you deploy an *unsigned* branch, as during development.)
3. **Publish the agent** (one-time Windows compile → Mac/Windows publish), then **activate**:
   ```bash
   sudo ./deploy/aws/set-release-keys.sh --ed25519 '<pub>' --p256 '<pub>'
   ```
4. **Add agent** in Fleet → generate a code → install on clients.

### What is now automatic (was manual in the first deploy)
| Field problem | Now handled by |
|---|---|
| Console dropped connections (`ECONNRESET`/`UND_ERR_SOCKET`) on a small box | `install.sh` sizes `API_WORKERS` by **RAM as well as CPU** — a <2 GB box auto-runs 1 worker |
| Facade 503 for ~15 s after every API restart | the `get.$DOMAIN` block has **no active health check** (single upstream, passive health) |
| New facade vhost not served until a manual `docker restart caddy` | `install.sh` **restarts Caddy** after the stack is up |
| Windows build died on **Python 3.13** | `build-agent-exe.ps1` checks the venv Python up front and fails with the 3.12 fix |
| Windows build died on **Nuitka 4.3** ("'agent' is not a package") | `build-agent-exe.ps1` pins `nuitka<4.3` |
| `package-zip.ps1` crashed after writing the zip | `$release`/`[switch]$Release` collision fixed |
| `publish-release.ps1` died on the Python version check | parses `python --version` (no PS 5.1 quote-stripping) |
| `/agent/redeem` returned 401 | added to the auth middleware public-path allowlist |

### What is still manual on a new server (and the one-command fix for each)
- **Signing keys → `.env`.** The build prints two public keys; run
  `sudo ./deploy/aws/set-release-keys.sh --ed25519 '<pub>' --p256 '<pub>'` (writes them, recreates the API, verifies).
- **Windows build box: Defender quarantines impacket.** Before the build, in an **admin** PowerShell:
  `Add-MpPreference -ExclusionPath "<repo path>"`. (impacket is a pentest lib Defender flags; without the
  exclusion the build fails with `[Errno 22]` on `impacket\__init__.py`.)
- **SSH from the build box to the server.** Put the key in `~/.ssh/config` with `User ubuntu` + `IdentityFile`,
  and `icacls <key> /inheritance:r /grant:r "$env:USERNAME:R"` so Windows SSH accepts it.
- **`MANAGER_PUBLIC_URL`** must be the facade — `install.sh` sets it from `DOMAIN` automatically now; only
  override if you front the manager differently.
- **Server size:** 1 GB RAM is below comfortable for the full console; **2 GB+** (e.g. t3.small) is recommended.
