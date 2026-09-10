# vedha-agent — interface contracts (versioned)

**Date:** 2026-09-10 · **Branch:** `cross-os-vedha-agent-install` · **Phase:** 0b/0c (design, no product code)
**Parent:** `2026-09-10-hardened-vedha-agent-architecture.md` · **Model source:** `…-threat-model.md`

Two boundaries become **versioned, contract-tested artifacts** instead of implicit
couplings: the in-host **brain↔daemon** boundary (0b) and the network
**agent↔Manager** boundary (0c). This removes the "verify the enrollment env-var
names by archaeology" risk the installer plan flagged.

**Versioning:** `CONTRACT_VERSION = "1.0.0"` (semver). Both sides assert
`major` compatibility on startup/connect; a mismatch is a `fatal-config` exit
(class 20) with the specific version pair in the message.

---

## 0b. Brain ↔ daemon (in-host)

### Config object (single validated shape, one loader)

| Field | Type | Source precedence | Notes |
|---|---|---|---|
| `manager_url` | str (https/http\:ip\:18080) | CLI > env `PLATFORM_URL` > probe.env > default | normalized by `agent.cli.normalize_manager_url` |
| `scope` | `list[Segment]` | Manager-pushed (confirmed) > CLI `--scope` > probe.env | **typed**, see below; empty ⇒ fatal-config |
| `name` | str | CLI `--name` > env `PROBE_NAME` > `<hostname>-probe` | |
| `verify_tls` | bool | env `VERIFY_TLS` > default `true` | never `false` in prod |
| `ca_bundle` | path\|null | env `PROBE_CA_BUNDLE` | private-CA trust |
| `mtls_cert`/`mtls_key` | path\|null | env | present together or neither |
| `heartbeat_interval`/`poll_interval` | int s | env > default 30/10 | |
| `job_limit`/`max_targets`/`max_job_seconds` | int | env > appliance ceilings | per-job may reduce, never exceed |
| `state_dir` | path | env `STATE_FILE` dir / OS default | queue + identity live here |

**Precedence (single documented chain):** `CLI flag > process env > probe.env >
Manager-pushed > built-in default`. `config show --effective` prints each value
**with its winning source**.

```
Segment = {
  cidr: str,            # IPv4 CIDR
  type: "IT"|"IoT"|"OT"|"NEVER",
  profile: "it"|"iot"|null,   # null for NEVER/OT-passive
  active: bool = true,        # OT defaults false
  rate_ceiling_pps: int|null, # engine-enforced; CLI cannot raise
  site: str,                  # tenant/site key (see 0c)
  authorized_by: str|null
}
```

### Exit-state protocol (wide channel — replaces 4 overloaded codes)

Exit code = **broad class only**; detail rides a state file
`<state_dir>/exit-state.json` and a structured stderr line
`VEDHA-EXIT {class} {reason} :: {remediation}`.

| Class | Code | `reason` values (examples) | Supervisor policy |
|---|---|---|---|
| success | 0 | `clean-shutdown` | stop |
| retryable | 10 | `manager-503`, `dns-failed`, `no-interface-up`, `tls-transient`, `manager-unreachable` | **monotonic** backoff, capped by `StartLimitBurst` |
| fatal-config | 20 | `empty-scope`, `bad-manager-url`, `clock-skew-exceeds-ttl`, `contract-version-mismatch` | stop, print remediation |
| fatal-identity | 30 | `cert-expired`, `identity-revoked`, `orphaned-identity` | bounded re-enroll flow |
| awaiting-approval | 40 | `pairing-pending` | poll, not an error |

`exit-state.json = { contract_version, class, code, reason, remediation, at_monotonic }`.
The supervisor parses this — it never infers policy from the bare code.

### Enrollment env contract (the flagged coupling — now specified)

The brain sets exactly these; the daemon reads exactly these (add a contract test
asserting the mapping on both sides):

| Mode | Brain sets | Daemon behavior |
|---|---|---|
| pairing | `VEDHA_ENROLL_MODE=pairing` | fresh device enrollment; print pairing code; exit 40 until approved |
| pat | `VEDHA_ENROLL_MODE=pat`, `VEDHA_PAT=<t>` | authenticate with the PAT |
| token | `VEDHA_ENROLL_MODE=token`, `VEDHA_ENROLL_TOKEN=<t>` | pre-authorized, site-bound token |

> Migration note: today's daemon reads `PROBE_PAT`/saved `probe.env`. Phase 0b
> pins the new names above; Phase 6 wires the daemon to read them and keeps a
> back-compat shim for `PROBE_PAT` for one release.

---

## 0c. Agent ↔ Manager (network)

### Signed job envelope (agent enforces its own ceiling)

```
Job = {
  contract_version: "1.0.0",
  job_id: uuid,                 # idempotency key (also the result key)
  uc: int, intensity: 1|2|3,
  scope_cidrs: [str],           # authoritative scope for THIS job
  targets: [str],
  site: str,
  not_before: iso8601, expires: iso8601,
  sig: base64                   # Ed25519 over canonical(Job \ sig)
}
```
Agent MUST: (1) verify `sig` against the **pinned** job-signing pubkey; (2) check
`contract_version` major; (3) check `not_before ≤ now ≤ expires` (clock-aware,
A6); (4) verify `targets ⊆ local typed scope` and the segment's `type` permits
`uc` (e.g. no active `uc` on an `OT`/`NEVER` segment); reject with a specific
`reason` otherwise. **A signed job can only request a subset — never widen scope.**

### Result envelope (at-least-once, idempotent, site-keyed)

```
Result = { contract_version, job_id, agent_id, site, produced_at, payload }
```
- `job_id` is the **idempotency key**; the Manager dedups replays.
- `site` is assigned at enrollment and included on **every** result (solves
  overlapping RFC1918 / NAT — §4 of the review).
- Delivery is at-least-once from the durable queue; a crash between "sent" and
  "acked" replays safely.

### Enrollment
Device X25519 keypair = identity. Flows: pairing (approval-gated) / auto (if
Manager allows) / site-bound token (TTL). **Clock-skew guard:** reject with
`clock-skew-exceeds-ttl` and the measured offset when skew > token TTL.

### mTLS profile
TLS 1.2+; verify Manager cert (public CA or pinned private CA via `ca_bundle`);
optional client cert (`mtls_cert`/`mtls_key`) so the Manager authenticates the
agent at the TLS layer. Short-lived certs (clock-sensitive).

### Kill switch
- **Local:** a stop file `<state_dir>/STOP` or an OS service stop halts scanning
  even if the Manager is unreachable.
- **Remote:** a Manager `revoke` obeyed on next contact; agent ceases and exits
  `fatal-identity`.

---

## Contract-test plan (both sides import the artifact)

| Test | Asserts |
|---|---|
| config round-trip + precedence | `config show --effective` source resolution matches the chain |
| version mismatch | major mismatch → `fatal-config` `contract-version-mismatch` |
| exit-state parse | supervisor maps each `reason` to the right class/policy |
| enrollment env mapping | brain-set vars == daemon-read vars for all 3 modes |
| job signature | valid verifies; tampered/expired/wrong-key rejected |
| scope re-check | out-of-scope / wrong-segment-type target rejected with reason |
| result idempotency | duplicate `job_id` deduped by the Manager stub |
| kill switch | `STOP` file halts an in-flight scan; revoke → `fatal-identity` |

## What this unblocks
Phase 1 (scope model) implements `Segment`; Phase 3 implements the exit-state
emitter/parser; Phase 6 implements enrollment + job verification against these
exact shapes — no archaeology, no guessing.
