# 04 — Database Exposure Check (Core-Level Playbook)

> **Goal:** Find databases reachable from your foothold that should not be, and determine whether
> they are **unauthenticated, weakly authenticated, or leaking data**. Exposed databases are among
> the highest-impact, most common findings (ransomware/extortion frequently start here).

---

## 1. Core theory: databases speak binary wire protocols with a handshake

Unlike HTTP, most DB protocols begin with a **server-initiated greeting** or a strict
**client-startup** exchange. That handshake is a fingerprinting oracle — you learn the product,
version, auth method, and often whether auth is required at all *before* logging in. This is the
same "banner/handshake reveals identity" idea as Nmap's `-sV` NULL probe
(`fresh_implement.md §8`), applied to DB ports.

Key default ports and their wire behavior:

| DB | Port | Wire-protocol core fact |
|----|------|-------------------------|
| MySQL/MariaDB | 3306 | Server sends **Initial Handshake Packet** first: version string, thread id, capability flags, auth-plugin, salt |
| PostgreSQL | 5432 | Client sends **StartupMessage**; server replies with AuthenticationRequest (trust/md5/scram/…) — `trust` = no password |
| MSSQL (TDS) | 1433 (+1434/UDP browser) | **Pre-Login** packet negotiates encryption; UDP 1434 SQL Browser leaks instance names/ports |
| Oracle TNS | 1521 | TNS listener; `tnscmd`/version query; historically leaks SID/service names |
| MongoDB | 27017 | Wire protocol (OP_MSG); `isMaster`/`buildInfo` often answer **without auth** if misconfigured |
| Redis | 6379 | RESP protocol; plaintext; `PING`/`INFO` with no auth on default installs = full access |
| Elasticsearch | 9200 | HTTP+JSON; `GET /` and `/_cat/indices` unauth on old/default configs |
| Memcached | 11211 | Text/binary; `stats`/`version` unauth; UDP variant = amplification (`11`) |
| CouchDB | 5984 | HTTP; "Admin Party" (no admin) historically world-writable |
| Cassandra | 9042 | CQL binary; auth optional by default |

---

## 2. Why exposed DBs are so dangerous (the vuln logic)

1. **Default = no/weak auth.** Redis, Mongo (pre-3.6 bind-all era), Elasticsearch, memcached,
   CouchDB have all shipped with *no authentication by default* and `bind 0.0.0.0`. If reachable,
   they are often fully readable/writable with zero credentials.
2. **Auth methods leak.** Postgres `trust`, MySQL old-password/`mysql_native_password`, MSSQL
   mixed-mode `sa` with blank/weak password.
3. **RCE pivots.** Redis → write SSH keys / cron / module load → RCE. MSSQL `xp_cmdshell`.
   Postgres `COPY ... PROGRAM` / untrusted PL languages. Mongo/JS injection. These turn "read a
   DB" into "own the host."
4. **Data at rest = the crown jewels.** PII, credentials (password hashes → cracking → lateral
   movement), tokens, business data.

---

## 3. Approach from a single system (methodology + commands)

**Step 1 — find the ports:**
```bash
nmap -sS -p 1433,1521,3306,5432,5984,6379,7000,7001,9042,9200,11211,27017,27018,50000 \
     -sV --script "banner" -iL live.txt -oX db_ports.xml
# UDP for MSSQL browser / memcached
nmap -sU -p 1434,11211 <hosts>
```

**Step 2 — handshake fingerprint (unauth, low-risk):**
```bash
# MySQL greeting → version + auth plugin
nmap -p3306 --script mysql-info <host>
# Postgres
nmap -p5432 --script pgsql-brute --script-args ...    # or just capture startup reply
# MSSQL instances via UDP browser
nmap -sU -p1434 --script ms-sql-info <host>
# Mongo without auth
mongosh "mongodb://<host>:27017" --eval 'db.adminCommand({buildInfo:1})'
# Redis no-auth check
redis-cli -h <host> PING ; redis-cli -h <host> INFO server
# Elasticsearch
curl -s http://<host>:9200/ ; curl -s http://<host>:9200/_cat/indices?v
# memcached
printf 'version\r\nstats\r\n' | nc <host> 11211
```

**Step 3 — auth posture & safe validation:**
- Confirm *whether* auth is required (a successful unauth `INFO`/`buildInfo`/`_cat` is the finding).
- Test **default/blank credentials** only if in scope: `sa`/blank (MSSQL), `root`/blank (MySQL),
  `postgres`/`postgres`, no-auth Redis/Mongo.
- Nmap NSE: `mysql-empty-password`, `ms-sql-empty-password`, `mongodb-databases`,
  `redis-info`, `*-brute` (rate-limited, in scope only).

**Step 4 — scope the exposure, do NOT exfiltrate:**
- Enumerate database/table/index *names and row counts* as proof — avoid pulling actual PII.
- Note network reachability (who else can reach this port?), bind address, and TLS on/off.

---

## 4. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| Port open but protocol unknown | Non-standard port, custom build | `-sV --version-all`; grab raw handshake with `ncat`; match bytes to protocol |
| TLS-wrapped DB | Encrypted MSSQL/Postgres/Mongo | Use TLS-aware clients (`--tls`), inspect cert; Nmap tunnels probes through SSL (`fresh_implement.md §8`) |
| Auth required, brute risky | Lockout/DoS, logging | Prefer default-cred *single* attempts; small curated lists; respect lockout policy; note "auth present" as partial finding |
| Read-only reconnaissance mandate | Don't want to alter data | Use metadata/admin commands only (`buildInfo`, `INFO`, `_cat`, `SELECT version()`); never write |
| Handshake crashes fragile DB | Old/embedded engines | Gentle single connections, no aggressive NSE brute, `-sT` on delicate hosts |
| MSSQL dynamic ports | Named instances on random ports | Query UDP 1434 SQL Browser first to learn the real TCP port |
| Mongo/Redis behind app only | Bound to localhost, reachable via SSRF/app | Note as reachable-via-pivot; test from the app tier if in scope |
| False "exposed" (honeypot) | Deceptive service | Corroborate with version consistency, latency, data plausibility |
| Cloud managed DBs (RDS/Atlas) | IAM/network-based auth | Check security-group/IP-allowlist exposure, not just port; TLS + IAM posture |

---

## 5. Considerations & guardrails

- **Never exfiltrate real data.** Prove access with schema/metadata/counts. Data theft can breach
  law and engagement scope even when authorized to "test."
- **Writes can corrupt production** (Redis `CONFIG SET`, Mongo writes). Read-only unless explicitly
  authorized to modify a test instance.
- **Brute force = DoS + lockout risk.** Bounded, in-scope, logged.
- **Password hashes found = handle as secrets;** do not crack out of scope.

---

## 6. References

- Protocol docs: MySQL Client/Server Protocol, PostgreSQL Frontend/Backend Protocol,
  MS-TDS (Microsoft), MongoDB Wire Protocol, Redis RESP spec, Elasticsearch REST API.
- CIS Benchmarks for MySQL/PostgreSQL/MSSQL/MongoDB (secure-config baselines to test against).
- Nmap NSE db categories: `mysql-*`, `ms-sql-*`, `mongodb-*`, `redis-*`, `pgsql-*`.
- Historical exposure research: Shodan/Censys reports on open MongoDB/Elasticsearch/Redis;
  MITRE ATT&CK T1210 (Exploitation of Remote Services), T1078 (Valid Accounts).
- Handshake-fingerprint analogy: `../fresh_implement.md §8`.
