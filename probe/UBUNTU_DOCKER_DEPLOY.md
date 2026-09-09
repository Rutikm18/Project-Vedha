# Running vedha-agent on an Ubuntu server (Docker)

A focused runbook for deploying the Vedha **probe** (a.k.a. **vedha-agent**) on an
Ubuntu server using Docker, connecting it to a Manager that is already running.

For the broader split-deployment picture (Manager + probe), see
[`DEPLOYMENT.md`](DEPLOYMENT.md). If it connects but gets no jobs, see
[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

---

## What vedha-agent is (mental model)

A **thin, dial-out scanner**. It does not analyze or store anything long-term. It:

1. Opens **one outbound connection** to your Manager (HTTPS + WebSocket on the same port),
2. Receives scan jobs the Manager pushes to it,
3. Scans the local network **within the scope the Manager enforces**,
4. Streams raw facts back over that same connection.

**No inbound listener. No exploitation.** The only firewall rule you need on the
Ubuntu box is **outbound** to the Manager — nothing inbound.

> The agent normally needs a **running Manager** to be useful. On its own it just
> retries the connection. (Code/dir is `probe/`; the daemon is `agent.agent`.)

---

## Prerequisites

- Ubuntu server with **Docker Engine + compose plugin**:
  ```bash
  sudo apt update && sudo apt install -y docker.io docker-compose-plugin
  sudo usermod -aG docker $USER   # log out/in so `docker` works without sudo
  ```
- The `probe/` folder present on the server.
- **No nmap/masscan needed** — the scanners are pure-Python/stdlib TCP.
- Outbound network access from the server to the Manager (443 for a TLS Manager,
  or `:18080` for a bare-IP http Manager).

---

## Step 1 — Get the probe onto the server

From your machine:
```bash
rsync -av probe/ user@ubuntu-server:~/vedha-probe/
```
On the Ubuntu server:
```bash
cd ~/vedha-probe
```

## Step 2 — Configure `probe.env`

```bash
cp probe.env.example probe.env
nano probe.env
```

Two values are **required**:

```ini
PLATFORM_URL=https://manager.your-domain.com   # your Manager (use https:// for prod)
PROBE_NETWORK_SEGMENTS=192.168.1.0/24          # CIDR(s) this agent may scan; empty = refuse every job
PROBE_NAME=ubuntu-probe-01                      # display name in the Fleet UI
VERIFY_TLS=true
```

**Authentication** — pick the one matching your Manager:

| Manager setup | What to do |
|---|---|
| Auto-enroll on (`PROBE_AUTO_ENROLL=true`) | Nothing else — the agent self-registers and the Manager auto-approves. |
| Personal Access Token | Set `PROBE_PAT=vpat_xxx` in `probe.env` (issue it in the Manager UI). |
| Approval-gated pairing / enroll-token | Leave the token blank and use the installer flow in Step 4. |

**Private/self-signed Manager cert:** put `ca.pem` in this folder, set
`PROBE_CA_BUNDLE=/etc/vedha/ca.pem`, and uncomment the `./ca.pem` volume in
`docker-compose.yml`. **Never** set `VERIFY_TLS=false` in production.

## Step 3 — Prepare the result-archive dir (Linux-specific)

The container runs as uid **10001** and is read-only, so make the bind-mount
writable first (otherwise archiving just logs one warning and carries on):

```bash
mkdir -p result && sudo chown 10001:10001 result
```

## Step 4 — Bring it up

**Option A — manual compose (most transparent):**
```bash
docker compose up -d --build
docker compose logs -f vedha-agent      # watch: register → heartbeat → polling
```

**Option B — installer (handles pairing / enroll-token):**
```bash
sudo sh install.sh --docker --manager https://manager.your-domain.com --enroll
```
This prints a short pairing code:
```
1) Open : https://manager.your-domain.com/fleet/enroll
2) Enter code : A7BQ-9KFP
```
Approve it in the Manager and the agent activates itself.

## Step 5 — Verify

- Logs show register → heartbeat → polling.
- **Manager UI → Fleet**: the agent appears **online**.
- If pairing-gated, approve the code and it starts scanning.

---

## Networking: bridge vs host (matters for LAN scanning)

- **Default bridge mode** (compose as-is): the agent does **L3 connect scans** via
  the host's routing. Correct results, most locked-down — a good default.
- **Raw SYN / ARP / scanning the host's own L2 segment**: edit `docker-compose.yml`:
  ```yaml
  network_mode: host
  cap_add: [NET_RAW, NET_ADMIN]
  # and remove:  cap_drop: [ALL]
  ```
  Off-privileged, the SYN scanner auto-falls back to connect scans, so this is
  optional unless you specifically need L2/raw capability.

## Firewall (customer egress)

| Direction | Port | Proto | Destination | Why |
|---|---|---|---|---|
| **Outbound** | **443** | TCP | Manager host | REST **and** WebSocket (the whole control + result channel) |
| Outbound | 53 | UDP/TCP | DNS resolver | Resolve the Manager domain |
| Outbound (LAN) | scan ports | TCP/UDP | `PROBE_NETWORK_SEGMENTS` | The agent scanning your own assets |
| **Inbound** | — | — | — | **NONE.** The agent never listens. |

Behind an egress proxy? Set `HTTPS_PROXY` in `probe.env`. If the proxy can't carry
WebSockets, set `PROBE_WS_ENABLED=false` and the agent long-polls over HTTPS.

---

## Common operations

```bash
docker compose logs -f vedha-agent      # follow logs
docker compose restart vedha-agent      # restart
docker compose pull && docker compose up -d   # update to a newer published image
docker compose down                     # stop (keeps the state volume)
docker compose down -v                  # stop AND wipe identity → forces fresh enrollment
```

- Identity + spool live in the `probestate` named volume (`/var/lib/vedha-agent`).
  Keeping it means a restart reuses the same agent registration; deleting it
  (`down -v`) creates a new probe row on the Manager on next start.
- `restart: unless-stopped` is set, so the container comes back after a reboot.

## When it won't connect / gets no jobs

Work through [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) — a stage-by-stage runbook
(reachability → credential → enrollment → WebSocket → jobs) that maps each error
line to its cause, exit code, and fix.

---

## Quick reference — minimal `probe.env`

```ini
PLATFORM_URL=https://manager.your-domain.com
PROBE_NETWORK_SEGMENTS=192.168.1.0/24
PROBE_NAME=ubuntu-probe-01
VERIFY_TLS=true
# PROBE_PAT=vpat_xxx        # only if not using auto-enroll / pairing
```
