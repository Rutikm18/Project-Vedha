# Probe ⇄ Manager Connection Troubleshooting

A backend engineer's runbook for "the probe won't connect / won't get jobs."
Work **top-down**: the connection is a pipeline, and a later stage can only be
debugged once the earlier ones are green.

> TL;DR triage — run these three first:
> ```sh
> curl -fsS http://<manager>:18080/health            # is the manager up & answering?
> PROBE_DEBUG=1 ./install.sh <manager>                # verbose handshake trace
> python3 -c 'import json,os;print(json.dumps(json.load(open(os.path.expanduser("~/vedha-agent/state.json"))),indent=2,default=str))' | grep -vi secret
> ```

---

## 1. Mental model — the connection pipeline

The probe reaches "waiting for jobs" by passing through **five stages, in order**.
Every failure below is bucketed by the stage it breaks in.

```
0. REACHABILITY   GET /health              → "✓ Manager reachable"
1. IDENTITY       load/generate keys       → state file readable & writable
2. CREDENTIAL     who am I to the manager?  ┐ PAT / operator login / bootstrap /
                                            ┘ cached device credential
3. ENROLL/REGISTER POST /agents/register    → "Registered as '<name>'"
      or device flow  POST /probe-enrollment/requests → poll → activate
4. TRANSPORT      WS /agents/ws             → "WebSocket connected. Push mode active"
5. JOBS           receive → run → submit    → scope ceiling must allow the target
```

Credential precedence (first one present wins), resolved in `agent.py:_obtain_identity`:

1. **`PROBE_PAT` / `OPERATOR_TOKEN` / `VEDHA_PAT`** — a `vpat_…` token → `POST /agents/register`.
2. **`PROBE_BOOTSTRAP_KEY`** — shared bootstrap key → `POST /agents/bootstrap`.
3. **`OPERATOR_EMAIL` + `OPERATOR_PASSWORD`** — `POST /auth/login` → register.
4. **Device enrollment** (no human credential) — `POST /probe-enrollment/requests` → poll → activate.
5. **Cached device credential** in the state file — refreshed before any of the above is retried.

`probe.env` is auto-loaded (`agent.py:_load_env`) with **`os.environ.setdefault`** —
so a variable already exported in your shell **wins over** `probe.env`. This is the
#1 source of "but my config says X": something stale in `probe.env` is being loaded
because you didn't export an override.

---

## 2. Stage 0 — Manager unreachable

Symptom lines come from `agent.py:_classify_connection_error`.

| Log says | Meaning | Fix |
|---|---|---|
| `connection refused` | Nothing is listening on that host:port | Manager down, or wrong port. Manager API is on **18080** (host) → `curl http://<mgr>:18080/health`. Port 80 is the edge proxy; `/health` works there too but enrollment/agent paths are under `/`. |
| `connection timed out` | Packets dropped | Firewall / AWS security group not open to this host on 18080. Open it, or fix `PLATFORM_URL`. |
| `cannot resolve host` | DNS failure | `PLATFORM_URL` host doesn't resolve. Common trap: using the Docker service name `http://api:8000` **from the host** — that only resolves *inside* the compose network. From the host use `http://localhost:18080`. |
| `TLS handshake failed` | Cert not trusted | Private CA → `PROBE_CA_BUNDLE=/path/ca.pem`. Testing only → use an `http://` URL. |
| `manager returned HTTP <code>` | **Manager answered and rejected** | This is a **server/API fault, not the network** — read the manager logs, not the firewall. (Before the fix this was mislabeled "connection error".) |

Diagnose:
```sh
curl -v -m 8 http://<manager>:18080/health          # 200 {"status":"healthy",...}
curl -s http://<manager>:18080/health | jq .version # confirm manager version
```

---

## 3. Stage 2 — Credential rejected

### 3a. `Manager rejected the configured PROBE_PAT/OPERATOR_TOKEN`
The PAT was **expired, revoked, or minted against a different manager** (a PAT is
bound to the manager/DB that issued it; if that DB was recreated, the PAT is dead).

```sh
# Prove it: a live PAT registers, a dead one 401s.
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://<mgr>:18080/agents/register \
  -H "Authorization: Bearer $PROBE_PAT" -H 'Content-Type: application/json' \
  -d '{"name":"pat-test","capabilities":["discovery"],"network_segments":["10.0.0.0/24"]}'
# 201 = good ·  401 = dead PAT
```
Fix — mint a fresh PAT **against the manager you're targeting**:
```sh
scripts/issue_pat.sh --url http://<manager>:18080 --name my-probe --days 365
# then put it in probe.env:  PROBE_PAT=vpat_…
```
If `OPERATOR_EMAIL`/`OPERATOR_PASSWORD` are also set, the probe now **auto-falls-back
to operator login** when a configured PAT is rejected (self-heal). Clearing a dead
`PROBE_PAT` from `probe.env` also forces the login path.

### 3b. `Device credential was revoked, expired, or disabled by <manager>`
A **cached device credential** in the state file is no longer valid on that manager
(operator removed the probe in Fleet, credential superseded, or the manager DB was
reset). By design the probe **stops for administrator review** rather than silently
re-enrolling — clearing a real revocation would hide it.

Fix — the "administrator" action is to reset the local identity, then re-enroll:
```sh
mv ~/vedha-agent/state.json ~/vedha-agent/state.json.bak   # keep a backup
./install.sh <manager> --enroll                            # fresh device enrollment
```

### 3c. `These credentials were issued by <A>, but this probe is pointed at <B>`
You re-pointed the probe at a **different manager**. This is not a revocation — the
probe re-enrolls with the new manager and leaves the old credential intact. Nothing
to fix; if it loops, clear the state file (3b).

---

## 4. Stage 3 — Enrollment (device flow)

### 4a. `Stored enrollment request no longer exists on the manager — starting a fresh enrollment`
A stored `enrollment_request_id` was **spent, expired, or purged** (or the manager's
enrollment store/Redis was reset). The probe now **discards it and re-creates**
automatically (bounded, `_recreate_budget=3`).

> This replaced a real bug: a `404` on poll used to be mislabeled a transient
> "connection error" and retried 12× before a false "Manager unreachable". If you
> still see the old behavior, your `agent/` is out of date — the fix lives in
> `poll_enrollment` (raises `EnrollmentRequestNotFound`) and the poll loop.

### 4b. `ENROLLMENT FAILED — manager keeps losing the request`
The manager accepted requests then 404'd them **3 times running**. This is
**manager-side**: enrollment store/Redis reset mid-flight, requests evicted before
approval, or a load balancer fronting instances with a non-shared store. Check the
manager's `probe-enrollment` service and Redis; confirm it isn't multi-instance
without shared state.

### 4c. `Already enrolled, no reusable credential — self-healing` (exit 4)
`POST /probe-enrollment/requests` → **409**: this device's **signing key** is already
a registered agent, but this install has no reusable credential (never activated, or
state was wiped). The probe **wipes the stale local identity and exits 4** so the
next start generates a **fresh key** and enrolls clean.

- **Docker**: the restart policy makes this automatic — it self-heals to online.
- **Local (`install.sh`)**: there's no auto-restart — **just run `./install.sh <manager>` again.** The orphaned agent can be pruned later in Fleet.

### 4d. `PROBE PAIRING REQUIRED — approve to start scanning`
No auto-approve, so the manager issued a **pairing code**. Approve it:
open `http://<manager>:18080/fleet/enroll`, enter the code. The probe activates
automatically. To skip this in future: set `PROBE_AUTO_ENROLL=true` **on the
manager**, or pass a pre-authorized enroll token: `./install.sh <manager> <vet_…>`.

### 4e. `ENROLLMENT NOT APPROVED — stopping` (exit 3)
Nobody approved within the window (default 30 min, `PROBE_ENROLL_WAIT_SECS`).
Approve in Fleet, or enable `PROBE_AUTO_ENROLL` / use an enroll token, then re-run.

---

## 5. Stage 5 — Connected but no / rejected jobs

The probe says **"Push mode active — waiting for jobs"** but scans never run.

- **Scope ceiling mismatch.** `PROBE_NETWORK_SEGMENTS` is a hard local authorization
  ceiling — the probe **rejects any job whose targets fall outside it**, regardless
  of what the manager dispatches. If your probe advertises `192.168.1.0/24` but this
  host is on `10.44.221.0/24`, a job for the real LAN is refused.
  ```sh
  ip -4 route get 1.1.1.1        # what network am I actually on?
  ```
  Fix: set `PROBE_NETWORK_SEGMENTS` in `probe.env` to the range you intend to scan,
  then restart the probe.
- **Capability mismatch.** The manager only routes jobs whose required capability is
  in the probe's advertised set (printed on connect). A newly added capability needs
  a metadata refresh — restart the probe.
- **Probe not actually running.** Jobs only execute while the process is up. Run it
  under a supervisor (`nohup … &`, `systemd`, or the Docker restart policy).

---

## 6. Reference

### Exit codes (`SystemExit`)
| Code | Meaning |
|---|---|
| 0 | Clean exit (e.g. a one-shot subcommand) |
| 1 | Setup error or **authoritative credential rejection** (bad creds, revoked device, invalid config) — needs a human |
| 2 | **Manager unreachable / connection exhausted** or enrollment infra failure — retriable once the manager/network is fixed |
| 3 | Enrollment **not approved** in time |
| 4 | **Already-enrolled self-heal** — identity wiped, restart to re-enroll |

### Environment variables
| Var | Purpose |
|---|---|
| `PLATFORM_URL` | Manager base URL (required). `http://host:18080` or `https://…` |
| `PROBE_PAT` / `OPERATOR_TOKEN` / `VEDHA_PAT` | `vpat_…` token credential |
| `OPERATOR_EMAIL` / `OPERATOR_PASSWORD` | Operator login (dev) |
| `PROBE_BOOTSTRAP_KEY` | Shared bootstrap key |
| `PROBE_ENROLL_TOKEN` | Pre-authorized site enroll token (`vet_…`) — auto-approves device enrollment |
| `PROBE_NETWORK_SEGMENTS` | CIDR scope **ceiling** (comma-separated). Empty denies all jobs |
| `STATE_FILE` | Identity/state path. Local default `~/vedha-agent/state.json`; container `/var/lib/vedha-agent/state.json` |
| `RESULT_SPOOL_DIR` | Crash-safe result spool |
| `VERIFY_TLS` | `true` (default). Set `PROBE_CA_BUNDLE` for private CAs instead of disabling |
| `PROBE_CA_BUNDLE` / `PROBE_CLIENT_CERT` / `PROBE_CLIENT_KEY` | Private-PKI trust / mTLS |
| `PROBE_DEBUG=1` | Verbose handshake + HTTP trace |
| `LOG_LEVEL` | `INFO` (default) … `DEBUG` |
| `PROBE_AUTO_ENROLL` | **Manager-side** — auto-approve device enrollment |
| `PROBE_ENROLL_WAIT_SECS`, `PROBE_*_NET_FAIL_LIMIT`, `PROBE_CREDENTIAL_RETRY_LIMIT` | Bounded retry / approval budgets |

### Manager endpoints the probe uses
```
GET  /health
POST /auth/login
POST /agents/register            POST /agents/bootstrap
POST /agents/heartbeat           GET  /agents/{id}/jobs
POST /probe-enrollment/requests
POST /probe-enrollment/requests/{id}/poll
POST /probe-enrollment/requests/{id}/activate
WS   /agents/ws                  (push mode)
```

### State file anatomy (`~/vedha-agent/state.json`, mode 0600)
| Key | Meaning |
|---|---|
| `agent_id`, `token` | Active agent identity + access token |
| `device_refresh_secret`, `credential_generation` | Device credential for short-lived token refresh |
| `signing_identity_sk/pk` | Ed25519 **device signing key** = the device's identity to the manager |
| `identity_sk/pk` | X25519 key for scope encryption |
| `manager_fingerprint` | Which manager issued the credential (scheme+host+port) — powers wrong-manager detection |
| `enrollment_request_id`, `enrollment_device_secret` | In-flight enrollment; **cleared on activate**. A lingering pair = an interrupted enrollment |

A **half-enrolled zombie** — `agent_id: null` but `enrollment_request_id` present —
means enrollment was interrupted after create, before activate. The probe now
self-heals from this; to force it, delete the state file.

---

## 7. Recipes

**Clean identity reset (start over):**
```sh
mv ~/vedha-agent/state.json ~/vedha-agent/state.json.bak-$(date +%s)
./install.sh <manager>            # or --enroll for pure device enrollment
```

**Switch which manager a probe targets:** edit `PLATFORM_URL` in `probe.env`, then
reset identity (above) — a device credential is meaningless to a different manager.

**Mint a fresh PAT:** `scripts/issue_pat.sh --url http://<manager>:18080 --days 365`

**Run persistently:** `nohup ./install.sh <manager> >~/vedha-probe.log 2>&1 &`
(or Docker `make probe-run`, or a systemd unit — see `DEPLOYMENT.md`).

**Verify a job end-to-end:** start the probe, dispatch a scan from the manager whose
target is **inside** `PROBE_NETWORK_SEGMENTS`, and watch the probe log:
`WebSocket connected` → job received → `scan results will be archived to …`.

---

## 8. Manager-side checks (when the probe is innocent)

The probe can only be as healthy as the manager. Verify:
```sh
curl -s http://<manager>:18080/health | jq        # postgres/redis "ok", version
```
- **Version parity** — the probe and manager should be compatible builds. A missing
  enrollment endpoint (`404` on a path that *should* exist) means version skew.
- **Redis / enrollment store** — device enrollment requests live here; if Redis is
  flushed or the API is multi-instance without shared state, requests vanish (see 4b).
- **Fleet approval** — an unapproved probe stays pending until an operator approves
  it (or `PROBE_AUTO_ENROLL=true`).
- **Clock skew** — signed enrollment challenges and JWTs are time-sensitive; keep the
  probe host's clock in sync (NTP).
