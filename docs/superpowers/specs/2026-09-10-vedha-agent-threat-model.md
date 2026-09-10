# vedha-agent — threat model (STRIDE)

**Date:** 2026-09-10 · **Branch:** `cross-os-vedha-agent-install` · **Phase:** 0a (design, no product code)
**Parent:** `2026-09-10-hardened-vedha-agent-architecture.md`

This is the artifact enterprise security review asks for, and the source of the
control roadmap: every uncontrolled entry below is future work. It fixes the
identity, authorization, scope, and data-classification models **before** code.

## Assets (what an attacker wants)

| Asset | Why it matters |
|---|---|
| Agent device identity (X25519 key) | Impersonating an agent lets a rogue host receive/return jobs |
| Job-signing trust anchor (pinned pubkey on agent) | The one thing that lets the agent trust a job; forging it = fleet-wide scan control |
| Scan results (topology, service+version inventory, banners) | A ready-made target map of the customer's network |
| Host root/Administrator privilege | The agent runs privileged; a bug is remote root on thousands of hosts |
| The Manager control plane | Compromise = arbitrary jobs on the whole estate + the full network map |
| Result-queue encryption key (host-sealed) | Unseals confidential results at rest |

## Trust boundaries

1. **Internet:** agent ⇄ Manager (dial-out 443, REST+WSS).
2. **Host process:** bootstrap → brain → engine → queue → uplink (same host, different responsibilities/privilege).
3. **Local disk:** the durable result queue + config + identity (at rest).
4. **LAN:** scanner ⇄ targets (the packets that can brick a fragile device).

## Attacker profiles

- **Network MITM** on the agent→Manager path.
- **Rogue Manager** (or a compromised one) issuing malicious jobs.
- **Rogue agent** trying to enroll into a fleet.
- **Malicious/curious local user** on the host (edit scope/config, read the queue).
- **Compromised Manager operator** (insider).
- **The customer's own SOC/EDR** treating the agent as a threat (§EDR in the arch doc).

## STRIDE

| Category | Scenario | Boundary | Control | Residual / roadmap |
|---|---|---|---|---|
| **S**poofing | Rogue host enrolls as an agent | Internet | Approval-gated enrollment (pairing/token) + enrollment CA; device key = identity | Auto-enroll must be off on untrusted networks (policy) |
| Spoofing | Rogue/again spoofed Manager issues jobs | Internet | **Jobs are Ed25519-signed; agent verifies against a *pinned* job-signing key**; TLS cert pinning / mTLS | Key rotation procedure (Phase 6) |
| **T**ampering | Local user edits scope/config to widen the ceiling | Disk | Config integrity check + signed effective-scope from Manager; local scope only ever *narrows* the Manager ceiling; audit event | Tamper-evident config store (roadmap) |
| Tampering | Job mutated in transit | Internet | Signature over canonical job bytes; reject on mismatch | — |
| Tampering | Result queue altered on disk | Disk | Encrypt-at-rest (host-sealed key) + per-record integrity | — |
| **R**epudiation | "Who authorized this scan?" unanswerable | Manager | **Signed job + immutable audit at scan time** (Manager); agent logs correlation-id per job | Manager-side audit store (dependency track) |
| **I**nfo disclosure | Result queue read at rest | Disk | Host-sealed encryption; StateDirectory perms | Key stored in OS keystore (roadmap) |
| Info disclosure | Diagnostics bundle leaks topology/creds | Disk/email | **Redaction** + data minimization; secrets stripped from config dump | Redaction unit tests (Phase 8) |
| Info disclosure | Logs contain targets/secrets | Disk | No secrets/full-results/target-lists at info level; structured redaction | — |
| Info disclosure | Results intercepted in transit | Internet | TLS 1.2+; results are confidential customer data (not telemetry) | FIPS mode (roadmap) |
| **D**oS | Agent floods the Manager | Internet | Monotonic backoff + capped retries + heartbeat rate | Server-side per-agent rate limit (Manager) |
| DoS | Scanner bricks a fragile device (OT/medical) | LAN | **OT deferred from v1**; engine-enforced rate caps; abort-on-anomaly; connect-only | Full OT safety track before OT ships |
| DoS | Queue fills the disk during a Manager outage | Disk | Bounded queue (size+age) + backpressure stops new scans | Disk-space `doctor` check (Phase 2) |
| **E**oP | Network-facing parser bug in a root process | Host | Strict input validation on **everything** the agent accepts from the Manager; least privilege; drop caps where possible | Fuzzing the job parser in CI (Phase 10) |
| EoP | Tampered `curl\|sh` / unsigned artifact runs as root | Supply chain | **Signed artifacts** + checksums + package-manager distribution | Reproducible builds (roadmap) |
| EoP | Agent retains more privilege than needed | Host | Request root only for `--service`; scan degrades to connect-scan unprivileged | Capability-scoped runtime (roadmap) |

## Model decisions locked here (feed Phase 0b/0c + Phase 1)

- **Identity:** device X25519 keypair = identity; **enrollment CA ≠ job-signing key**.
- **Authorization:** the agent enforces its **own** typed-scope ceiling; a signed
  job can only ever request a *subset* — never widen scope. Local scope narrows,
  never widens, the Manager ceiling.
- **Scope:** typed segments (IT/IoT/OT/NEVER) with a permanent denylist; confirmed
  by a human at enrollment; never auto-adopted.
- **Data class:** scan output is **confidential customer data**, encrypted at
  rest and in transit, minimized, redacted in diagnostics.

## Uncontrolled entries = roadmap
Manager-side audit store, tamper-evident config, OS-keystore key sealing, job-parser
fuzzing, reproducible builds, FIPS mode. Tracked in the architecture doc's Part C.
