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

Verification: after the first five fixes the backend suite gave **3194 passed, 9 skipped** (baseline 3155 + 39 new tests); after the follow-up it gives **3309 passed, 9 skipped**. `ruff` reports no new findings in the changed app files. bandit, semgrep and pip-audit were not run because they aren't installed here.

## Fixed in the follow-up change

| # | Sev | Finding | Fix | Tests |
|---|---|---|---|---|
| 6 | High (multi-tenant) | Unclaimed probe enrollment requests were listed to every tenant's admins and claimable by id without the device's user code. | The list and one-click approval include unclaimed requests only when the Manager serves exactly one active tenant (`_single_tenant_mode`). Otherwise the operator must enter the code the device displays (`POST /approve`) or use an enroll token. Both approval routes also refuse another tenant's claimed request (404). | `test_enrollment_tenant_claim.py` (5 of 7 fail on the old code) |
| 7 | Medium | `msf_host`/`msf_port`/`msf_password` came from the request: SSRF plus a network oracle through the error text. | Removed from the request. Host, port, password and TLS policy come from settings (`MSF_RPC_*`). Connection errors are logged, never returned. | `test_exploit_msf_and_roe.py` |
| 8 | Medium | Stock password `msf` as default and `verify_ssl=False` hard-coded. | No default password; unset, `msf`, `password` and `metasploit` are refused (503). TLS is verified by default, with `MSF_RPC_CA_BUNDLE` or an explicit `MSF_RPC_TLS_VERIFY=false` (logged) for msfrpcd's self-signed certificate. | same |
| 9 | Medium | Exploit routes ignored the engagement's rules of engagement. | `rules_of_engagement.exploitation_allowed: false` blocks `/exploits/run` and approval, and is re-checked when the approved job runs. See "Decision for you" below on the default. | same |
| 12 | Low | An approved run re-entered the approval gate, so a DC-named host never ran. | The runner re-reads the approval and runs only if it is `approved` for the same engagement, target, module and payload, then calls the orchestrator with `pre_approved=True` (scope, safety and blast radius still run). | same |
| 10 | Medium | SIEM/EDR API tokens stored in plaintext JSONB. | Secret keys (`token`, `api_key`, ...) are Fernet-encrypted on save and decrypted only to build the engine. Old plaintext rows keep working and are encrypted on next save. | `test_outbound_guard.py` |
| 11 | Medium | Tenant-supplied outbound URLs (SIEM/EDR, Jira, ServiceNow, Slack, SMTP) were called as given. | `services/outbound_guard.py`: https only, no credentials, every resolved address checked; loopback, link-local/metadata and other special ranges always refused; private ranges refused unless `OUTBOUND_ALLOW_PRIVATE_NETWORKS` or `OUTBOUND_HOST_ALLOWLIST`; SMTP limited to mail ports; no redirects; ServiceNow table name validated. Checked at save time and again on every call. | same |
| 13 | Low | AD password passed to `bloodhound-python` as `-p` (visible in `/proc/*/cmdline`). | Sent over stdin; option values use the `-x=VALUE` form so a leading `-` cannot become a flag. | `test_ad_and_token_hardening.py` |
| 14 | Low | JWT library error text returned to clients. | Fixed `"Invalid token"`; the reason class is logged. | same |
| 15 | Info | Unused `DiscoveryWorker` passed targets to nmap with no `--` or timeout. | Deleted (nothing enqueued to it; history keeps it). | n/a |
| 16 | High (new) | `POST /ad/assess` accepted any string as `dc_ip` and never checked the engagement scope, so a tester could make the Manager run LDAP/SMB/Kerberos and BloodHound against any reachable host. | `dc_ip` must be an IP literal inside the engagement scope and not excluded, and never loopback/link-local; `domain` and `username` are validated. | same |
| 17 | Medium (new) | The AD request could name the Neo4j URI and credentials the Manager connects to. | The request's `neo4j` block is ignored; the import uses `NEO4J_URI`/`NEO4J_USER`/`NEO4J_PASSWORD` when `NEO4J_ENABLED`. | same |

## Behaviour changes operators will notice

- **Private integration targets are blocked by default.** An on-prem Jira, ServiceNow, SIEM or SMTP server on a private address stops working after upgrade (it is logged as `notify.delivery_failed` or `siem.request_failed`; saving the integration returns 422). Set `OUTBOUND_ALLOW_PRIVATE_NETWORKS=true`, or list the hosts in `OUTBOUND_HOST_ALLOWLIST`.
- **Exploit routes answer 503 until `MSF_RPC_PASSWORD` is set** to a non-default value, and msfrpcd's self-signed certificate needs `MSF_RPC_CA_BUNDLE` or `MSF_RPC_TLS_VERIFY=false`.
- **Multi-tenant Managers can no longer one-click approve a probe from the fleet list.** Use the device's code or an enroll token.
- `ADAssessRequest.neo4j` is accepted but ignored.

## Decision for you

- `exploitation_allowed` defaults to **true** (opt-out), matching `active_validation_allowed`, so existing engagements keep working. A stricter posture is default-deny, where each engagement must set it to `true` before any exploit can run. That is a one-line change in `_roe_allows_exploitation`.
- `extra_options` is still accepted (target, payload, command and callback keys are blocked). Nothing in the repo sends it; removing the field is the smallest attack surface.

## Residual risks

- The SSRF guard resolves the name, and the HTTP client resolves it again when it connects, so a DNS-rebinding host can change its answer in between. Loopback/metadata are the backstop together with an egress firewall; pinning the resolved IP into the connection would close it fully.
- `verify_ssl` for SIEM/EDR remains tenant-controlled.
- Not run (not installed here): bandit, semgrep, pip-audit.

## Checked and found sound (evidence, not exhaustive)

- JWT: algorithm pinned, secret checked at startup and fatal in production (`auth/startup.py`); MFA challenge has its own audience; portal-audience tokens are confined to `/portal` and `/auth`; agent tokens are route-allowlisted.
- PATs: stored hashed, with scope, expiry and revocation checked in the middleware.
- Tenant scoping: all 54 lookups by ID without an inline tenant filter are follow-up reads after a tenant-checked parent (engagement or job), or background tasks fed server-side IDs. The one exception is the enrollment approval in #6.
- Rate limiting: X-Forwarded-For is trusted only from trusted proxies (`ratelimit.py`); login, MFA and enrollment are rate-limited; the enrollment refresh path rejects replayed nonces via Redis and fails closed.
- `/metrics` is internal-network only, and API docs are off in production.
- No `shell=True`, `eval`, `pickle` or unsafe `yaml.load`. Subprocess calls use argument lists. The only raw SQL `text()` uses a constant.
- Exports neutralize spreadsheet formulas (CSV and XLSX). Intel bundles are signature-verified and size-capped. Uploads are read with a size cap.
