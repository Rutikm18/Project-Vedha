# Attack playbook — think like the attacker

Use in Phase 0. Find the feature type(s) below and write the attacks that
apply as abuse cases; each one needs a mitigation and (ideally) a test.
Map to MITRE ATT&CK / CAPEC where it helps communication, but focus on the
concrete request an attacker would send.

## Attacker profiles to consider for Vedha
1. **Anonymous internet user** hitting the manager UI/API.
2. **Low-privilege tenant user** (viewer/analyst) trying to escalate or read other tenants.
3. **Malicious/compromised tenant admin** attacking the platform or other tenants.
4. **Compromised or spoofed probe** sending forged results or pulling other tenants' jobs.
5. **Hostile scanned network** — targets return crafted banners, HTTP bodies, TLS certs,
   SMB/LDAP responses, hostnames designed to exploit our parsers, UI, or LLM (reverse attack).
6. **Supply-chain attacker** — malicious dependency, poisoned CI, tampered agent update.
7. **Insider with DB/log access** — what can they read that they shouldn't?

## By feature type

### New API endpoint / router
- Call without token; with expired token; with token signed `alg=none` / HS↔RS confusion.
- Call as each lower role (function-level authz).
- Swap IDs to another tenant's object (BOLA/IDOR) — via path, query, body, nested objects, bulk endpoints.
- Add extra fields (`tenant_id`, `role`, `is_verified`) to body (mass assignment).
- Huge page size / deep nesting / giant body / unicode edge cases / negative numbers.
- Sort/filter param with SQL fragments; JSON operators.
- Change HTTP method (GET vs POST vs PATCH) to dodge checks; trailing slash/case variants.

### Authentication, sessions, MFA, PATs
- Credential stuffing / brute force (rate limit, lockout, generic errors).
- User enumeration via timing or different messages on login/reset/invite.
- MFA bypass: skip step, reuse TOTP, use PAT/refresh path that doesn't require MFA.
- Refresh token reuse after rotation; logout not revoking; token in URL/logs/Referer.
- Password reset token predictability, lifetime, single use, host-header poisoning in reset links.

### Probe ↔ manager channel
- Enrol a rogue probe with a leaked/replayed enrolment token.
- Probe A requests jobs/configs/credentials for tenant B.
- Forged scan results: inject findings, XSS payloads in hostnames/banners, oversized payloads.
- Replay old manager commands; MITM without cert pinning; downgrade TLS.
- Manager → probe command channel abused to run arbitrary commands (RCE inside customer network!).
- Agent update path: unsigned/unauthenticated update, version rollback.

### Scanner / parser of network data (hostile target)
- Banners/certs/HTTP titles containing `<script>`, ANSI escapes, CRLF, null bytes, very long strings.
- XML from tools (nmap -oX) → XXE / billion laughs → use `defusedxml`.
- Hostnames/targets beginning with `-` → argument injection into nmap/etc.
- Decompression bombs, zip-slip in archives, infinite redirects, slowloris responses (timeouts!).
- Regex on attacker data → ReDoS.

### File upload / import / export / reports
- Upload `.html`/`.svg` with script; polyglots; wrong MIME; oversized; zip bomb.
- Path traversal in filename (`../../`), absolute paths, Windows `..\\`, unicode normalisation.
- CSV/formula injection in XLSX/CSV exports (`=HYPERLINK(...)`) — prefix `'` for cells starting with `= + - @`.
- Download endpoint fetching another tenant's report by guessing the key.

### Outbound integrations / webhooks / URL fetch
- SSRF to `169.254.169.254`, `localhost:5432`, Redis, internal docker service names, IPv6, DNS rebinding, decimal/octal IP encodings, redirects.
- Webhook receiver: unsigned payloads, replay, timing-unsafe signature compare.
- Leaking secrets in outbound URLs/headers to attacker-controlled endpoints.

### AI / LLM features
- Indirect prompt injection through scan data, CVE descriptions, uploaded docs.
- Model asked to reveal system prompt / other tenants' data / API keys.
- Model output rendered as HTML or fed to tools/SQL/shell.
- Cost exhaustion via huge inputs or loops.

### Frontend (Next.js)
- XSS sinks: `dangerouslySetInnerHTML`, `href` with `javascript:`, markdown renderers, chart labels.
- Open redirect via `?next=` / `returnTo` params.
- Tokens in `localStorage` (XSS-stealable) vs HttpOnly cookies; secrets exposed via `NEXT_PUBLIC_*`.
- Server actions / route handlers missing auth; middleware (`proxy.ts`) matcher gaps.
- Clickjacking (frame-ancestors), CSP weakened with `unsafe-inline`/`unsafe-eval`.

### Infra / CI / Docker
- Running as root, writable root FS, docker socket mounted, privileged containers.
- Secrets in image layers, compose files, build args, logs.
- Workflow injection via `${{ github.event.* }}` in `run:`; `pull_request_target` with checkout of PR code; over-broad `permissions`.
- Unpinned actions/base images; `latest` tags.

### Background jobs / workers / WebSockets
- Job payloads trusted without re-checking tenant/authz at execution time.
- WebSocket: auth on connect only, no per-message authz; subscribing to another tenant's channel.
- Unbounded queues/fan-out → DoS.
