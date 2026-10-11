# Manager backend security review — 2026-10-11

Method: `.claude/skills/secure-dev` (threat model, then evidence, then plan, then step-by-step fixes, then verification) against OWASP Top 10:2025, OWASP API Top 10:2023 and CWE Top 25:2025.
Scope: `manager/backend/app` (280 files, ~59k lines). This was a targeted review of the paths most exposed to attack, not a line-by-line audit:

- the auth middleware and JWT/PAT handling
- tenant scoping of every lookup by ID in `app/routers` (54 candidates, each read in context)
- the probe enrollment, agent and exploit routers
- outbound HTTP (SSRF)
- subprocess, deserialization and XML handling
- uploads and exports

## Fixed in this change

| # | Sev | Finding | Ref | Fix | Proof |
|---|---|---|---|---|---|
| 1 | Critical | `extra_options` was merged *after* `RHOSTS`, so `{"RHOSTS": "<any host>"}` aimed a Metasploit module at a target outside the engagement after the scope check had passed on `target_ip`. | A01, A06, CWE-284 | `validate_extra_options` rejects the engine-owned keys (target, payload, command, callback/proxy hosts), case-insensitively. Engine values are now applied last. | Reproduced on the old code: the module ran with `RHOSTS=8.8.8.8` and `CMD=rm -rf /`. `tests/test_exploit_safety_bypass.py` |
| 2 | High | `cmd/unix/generic` and `cmd/windows/generic` are allowlisted, but only `windows/x64/exec` had its CMD checked, so any command could run on the target. | A05, CWE-77/78 | Every payload that executes a command is held to the read-only command list. | Same test file |
| 3 | High | The exploit approval gate trusted the `target_hostname` and default criticality from the request. Leaving the hostname out skipped approval for a DC or a critical asset. | A01, CWE-863 | `_target_risk_context` reads the hostname and criticality from the engagement's own asset rows for that IP and uses the riskiest one. The request's hostname is only a fallback. | Same test file |
| 4 | High | Legacy agent JWTs (1-year, from `/agents/register`) skipped the agent lookup. A probe whose access had expired in Fleet, or whose agent row was gone or not active, kept polling for jobs. | A01, A07, CWE-613 | The middleware checks every `role=agent` token against the live agent row (exists in tenant, active, not expired; in-flight result upload still allowed). | 4 of 7 tests fail on the old code. `tests/test_legacy_agent_token_revocation.py` |
| 5 | High | The gzip request middleware runs before authentication and called `gzip.decompress` on the full body *before* the 128 MB check. A 254 KB request reached a 557 MB memory peak, so the 32 MB compressed cap allowed roughly 70 GB. | A10, CWE-409/770 | `bounded_gunzip` inflates with a hard output limit and handles multi-member bodies. | `tests/test_gzip_request_bomb.py` (peak memory stays under 16 MB for a 256 MB bomb) |

Verification: the backend suite gave **3194 passed, 9 skipped** (baseline 3155 + 39 new tests). `ruff` reports no new findings in the changed app files. bandit, semgrep and pip-audit were not run because they aren't installed here.

## Open — needs a decision or a follow-up

| # | Sev | Finding | Ref | Proposed fix |
|---|---|---|---|---|
| 6 | High (multi-tenant) | `GET /probe-enrollment/requests` lists unclaimed requests (`tenant_id IS NULL`) to **every** tenant's admins and managers. `POST /requests/{id}/approve` claims one into the caller's tenant without the user code, with the default auto-enroll scope. Tenant A can take over a probe installed in tenant B's network. Anyone unauthenticated can also plant requests that show up in every tenant's list. The architecture docs describe the manager as cloud multi-tenant. | A01, CWE-639 | Show unclaimed requests and allow one-click approval only when the manager has a single active tenant (or behind an explicit setting). Otherwise require the user code (device flow) or a site-bound enroll token. **This is a product decision.** |
| 7 | Medium | `/exploits/run` accepts `msf_host`, `msf_port` and `msf_password` from any tester. The manager connects there and returns the connection error text, which works as an internal network/port oracle (SSRF). | A01 (SSRF), CWE-918 | Move the MSF RPC endpoint and credentials to settings and drop them from the request body. |
| 8 | Medium | The Metasploit client defaults to the password `"msf"`, the approved-run path hard-codes `127.0.0.1:55553`/`"msf"`, and both use `verify_ssl=False`. | A04, A07, CWE-798/295 | Read from settings or secrets, fail closed when unset, and pin or verify the msfrpcd certificate. |
| 9 | Medium | The exploit routes never consult the engagement's rules of engagement. Active validation does (`active_validation_allowed`), and `agent_policy` has an exploit tier, but `/exploits/run` does not. | A06 | Apply an RoE gate (e.g. `exploitation_allowed`) on run and on approve. |
| 10 | Medium | SIEM/EDR `siem_config` and `edr_config` (API tokens) are stored as plaintext JSONB, whereas integrations encrypt their secrets. | A04, CWE-312 | Encrypt the secret fields with `credential_crypto`, as integrations do. |
| 11 | Medium | Tenant admins and managers set arbitrary outbound URLs: SIEM/EDR `base_url`, Jira/ServiceNow URLs, Slack webhook, SMTP host:port. The manager calls them with no egress guard. This is mostly blind (results are logged, not returned), but it can still reach metadata and internal services. | A01 (SSRF), CWE-918 | Shared outbound-URL guard: https only, resolve the host and block loopback, private, link-local and metadata ranges unless an operator allowlist permits them, and don't follow redirects to blocked targets. |
| 12 | Low | Approved exploits against a DC-named host re-enter the approval gate (`_run_approved_exploit` passes the same hostname), so they never run. This is a functional bug, not a security one. | — | Pass an "approved" flag or the approval id so the gate is satisfied. |
| 13 | Low | `bloodhound-python` receives the AD password via `-p` on the command line, where `ps` in the container can read it. | CWE-214 | Pass it via an environment variable or stdin if the tool supports it. |
| 14 | Low | `decode_token` returns `Invalid token: {e}` (library error detail) to the client. | CWE-209 | Return a generic message and log the detail. |
| 15 | Info | `app/discovery/worker.py` (`DiscoveryWorker`) has no references. It passes targets to nmap positionally with no `--` and no timeout. | CWE-88 | Delete it, or validate targets with `ipaddress` and add `--` and a timeout before anything wires it up. |

## Checked and found sound (evidence, not exhaustive)

- JWT: algorithm pinned, secret checked at startup and fatal in production (`auth/startup.py`); MFA challenge has its own audience; portal-audience tokens are confined to `/portal` and `/auth`; agent tokens are route-allowlisted.
- PATs: stored hashed, with scope, expiry and revocation checked in the middleware.
- Tenant scoping: all 54 lookups by ID without an inline tenant filter are follow-up reads after a tenant-checked parent (engagement or job), or background tasks fed server-side IDs. The one exception is the enrollment approval in #6.
- Rate limiting: X-Forwarded-For is trusted only from trusted proxies (`ratelimit.py`); login, MFA and enrollment are rate-limited; the enrollment refresh path rejects replayed nonces via Redis and fails closed.
- `/metrics` is internal-network only, and API docs are off in production.
- No `shell=True`, `eval`, `pickle` or unsafe `yaml.load`. Subprocess calls use argument lists. The only raw SQL `text()` uses a constant.
- Exports neutralize spreadsheet formulas (CSV and XLSX). Intel bundles are signature-verified and size-capped. Uploads are read with a size cap.
