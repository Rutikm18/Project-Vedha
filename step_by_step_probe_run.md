# Probe — Run & Test Guide

How to run the Vedha probe and test a scan end-to-end, plus the network/firewall
policies you need. Manager lives in the cloud; the probe runs on the network you
want to scan.

---

## 1. The one rule that decides everything

> **The probe must sit on the same network as the targets you want to scan.**

The probe scans its *own* local network. A probe running in the cloud has **no
route** to private LANs (`192.168.x.x`, `10.x.x.x`, `172.16.x.x`), so it cannot
see home/office hosts. Test targets like `192.168.1.254` must be scanned by a
probe **on that LAN** → run the probe **local**.

---

## 2. Architecture — manager and probe do NOT share a network

```
   YOUR LAN (192.168.1.x)                 CLOUD
 ┌────────────────────────┐        ┌──────────────────┐
 │                        │        │                  │
 │   [ Probe ] ───────────┼────────►   [ Manager ]    │
 │      │   outbound HTTPS/WS       │  13.127.147.205  │
 │      │   (probe dials OUT)       │                  │
 │      ▼                 │        └──────────────────┘
 │  scans targets         │
 │  192.168.1.74/.84/.254 │
 └────────────────────────┘
```

Two separate connections — only one crosses networks:

| Connection | Direction | Where |
|-----------|-----------|-------|
| **Probe → Manager** (get jobs, send results) | **Outbound** from probe | Across the internet |
| **Probe → Targets** (the actual scan) | Local | Same network only |

**Manager in the cloud + probe on your LAN = correct, intended design.** The
probe dials *out* to the manager, so the manager never has to reach into your
network.

---

## 3. Network policies — what to allow

**Manager side (EC2 security group) — the only real config**

| Rule | Port | Allow from | Why |
|------|------|-----------|-----|
| Inbound | **TCP 18080** | probe's public IP (or `0.0.0.0/0` for testing) | So the probe can connect in |
| Inbound | TCP 22 (SSH) | **your admin IP only** | Manage the box |
| Outbound | all (default) | — | Manager reaches its DB + Claude API |

> For testing, `0.0.0.0/0` on 18080 is fine. For production, whitelist the
> probe/customer egress IP.

**Probe side (your home LAN)**

- **Outbound TCP 18080 → manager IP** — home routers already allow all outbound,
  so usually **nothing to do**.
- **No inbound rules, no port-forwarding** — the manager never connects back to
  you. (This is the security win.)
- Local access to scan targets — already have it (same network).

**Target machines (what you're scanning)**

- Their **host firewall** decides what the probe can see. A blocked port is
  correctly reported closed/filtered. To test *full* accuracy, allow the probe's
  IP on the target (or lower its firewall temporarily).

**Scan privileges**

- Scans use **TCP-connect** by default — **no root needed**, works as-is.
- For faster **SYN/ICMP** scans, run the probe with `sudo` (optional, not
  required for testing).

---

## 4. Cloud-hosted probe — restrictions (for reference)

If you ever run the probe *in* a cloud env instead of on the target LAN:

| # | Restriction | Effect |
|---|-------------|--------|
| 1 | No route to private LANs | Can't scan `192.168.x.x` / `10.x.x.x`; only public IPs or same-VPC hosts |
| 2 | Security-group / egress firewall | Outbound scan ports get blocked |
| 3 | Cloud provider anti-abuse (AWS AUP) | Outbound port-scanning needs prior authorization; instance can be flagged |
| 4 | Hardened container = no raw sockets | No SYN/ICMP; slower connect-scan; ICMP host-discovery may fail |
| 5 | NAT'd source IP | Target sees the cloud IP, not your real vantage |

**Rule of thumb:**
- Targets on **your LAN** → probe **local** (or Docker on that LAN).
- Targets on **public internet / same cloud VPC** → cloud probe is fine.

---

## 5. Step-by-step: run & test

**Step 1 — Confirm the manager is reachable** (from your machine)

```bash
nc -vz 13.127.147.205 18080
```

Expect `succeeded` / `open`. If it hangs → the EC2 security group isn't allowing
18080.

**Step 2 — Start the probe** (keep this terminal open)

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe"
PROBE_NAME=scanner-probe-01 sh install.sh http://13.127.147.205:18080 --local
```

Wait for the `▶ probe → …` line and WebSocket-connected logs. The probe is
already enrolled (`~/vedha-probe/state.json`), so it just **connects** — no
re-enrollment.

**Keep it alive after closing the terminal** (optional):

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe"
PROBE_NAME=scanner-probe-01 nohup sh install.sh http://13.127.147.205:18080 --local \
  > ~/vedha-probe/probe.log 2>&1 < /dev/null & disown
tail -f ~/vedha-probe/probe.log
```

**Step 3 — Verify it's online**

Dashboard → **Fleet** → `scanner-probe-01` shows **green / online**.

**Step 4 — Pick a target that's actually UP** (important)

```bash
nc -vz 192.168.1.254 80
```

`succeeded` = host is up and scannable. (`.254` is the router and is up; a down
host returns `0 hosts / Port Scan skipped`.)

**Step 5 — Launch a scan from the dashboard**

Dashboard → **Scanner** → choose **Network Discovery** → probe
`scanner-probe-01` → target `192.168.1.254` → **Launch**.

**Step 6 — Watch it complete**

Job goes Queued → Scanning → **Complete**, and you'll see the host + open ports
(e.g. 22/80/443).

---

## 6. Probe status & control

**Is the probe running?**

```bash
ps aux | grep -E "agent\.agent" | grep -v grep
```

**Restart it:** stop the old one first (same identity can't run twice), then
start again with the Step 2 command.

```bash
pkill -f agent.agent
```

**Logs (if launched detached):**

```bash
tail -f ~/vedha-probe/probe.log
```

---

## 7. Known issue — Full Assessment currently stalls

- **Use "Network Discovery" for a clean end-to-end test** — it completes.
- **"Full Assessment" gets stuck** on a manager **HTTP 500**: the SSH/HTTP banner
  can contain **NUL (`\x00`) bytes**, and PostgreSQL JSONB can't store the NUL
  character, so the result insert crashes. The scan itself runs fine — only the
  *result submission* fails, and the result is spooled locally under
  `~/vedha-probe/spool/`.
- **Fix:** strip NUL bytes from `facts` before they're persisted (probe result
  builder or manager ingest). Pending.
