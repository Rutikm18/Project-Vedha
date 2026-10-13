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

Built in: branch `feat/windows-zero-knowledge-install` (install codes, `/agent/redeem`,
`-Code` installer, `get.$DOMAIN` facade, Fleet card). See the
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
1. **The branch isn't pushed yet.** Nothing works until you push it and the server pulls it.
2. **DNS must resolve before Caddy runs**, or the TLS certificate (ACME) fails.
3. **`MANAGER_PUBLIC_URL` must be the facade** (`https://get.vedhasec.com`) in both `install.sh`
   and the publish step — whichever runs last wins, so keep them equal.
4. **Signing keys must be consistent.** Generate them in ONE place and reuse them forever; the
   manager pins the public key, so a second set from a different machine breaks verification.

---

## Step 0 — push the branch · **[MAC]**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
git push -u origin feat/windows-zero-knowledge-install
```
(Or merge it to `main` first if you prefer; then the server pulls `main`.)

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
git checkout feat/windows-zero-knowledge-install   # or: git pull origin main (if merged)
make full                        # rebuilds the stack AND runs migrations (gets /agent/redeem + migration 0063)
```
`make full` runs `alembic upgrade head`, so migration **0063** (the `agent_install_codes`
table) is applied automatically. Confirm the API is healthy before moving on:
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
git checkout feat/windows-zero-knowledge-install
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
- **Approach #1 (air-gapped zip)** — one script that emits a self-contained zip for clients
  that can't reach the manager. Deferred by choice; the `-Token` flow, not `-Code`.
