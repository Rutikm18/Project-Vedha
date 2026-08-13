# 10 — Web Application Triage (Core-Level Playbook)

> **Goal:** Go beyond external surface mapping (`03`) into **application-level** assessment of a
> specific web app: map its routes and inputs, understand its auth and session model, and
> systematically test the input/logic surface for the OWASP-class vulnerabilities. Triage here =
> find and prioritize the exploitable classes efficiently, not perform a full manual audit of every
> parameter.

---

## 1. Core theory: a web app is a state machine reachable only through its inputs

At the core, every web vuln reduces to one pattern: **untrusted input crosses a trust boundary
into an interpreter or a security decision without correct handling.** The interpreters/boundaries:

- **SQL/NoSQL** → injection (SQLi/NoSQLi).
- **OS shell** → command injection.
- **HTML/JS in browser** → XSS.
- **HTTP request parsing (front-end vs back-end disagreement)** → request smuggling.
- **Server-side URL fetch** → SSRF.
- **Object/graph references** → IDOR / broken access control.
- **Template engines** → SSTI.
- **Deserializers** → insecure deserialization → RCE.
- **Auth/session logic** → broken authentication, JWT flaws, session fixation.
- **File path/name** → path traversal, unrestricted upload.

So the method is: **(1) enumerate every input and trust boundary, (2) reason about which
interpreter each input reaches, (3) test the corresponding vuln class.** Enumeration completeness
is what separates good testing from lucky testing.

---

## 2. The triage pipeline

### 2.1 Map the app (attack-surface enumeration)
- **Crawl** both static and JS-rendered routes: `katana`, `hakrawler`, Burp Suite spider; parse JS
  bundles for hidden API paths (`linkfinder`).
- **Content/endpoint discovery** (brute force known paths): `ffuf`/`feroxbuster` with curated
  wordlists (raft, SecLists). Find `/api`, `/admin`, backups, `.git`, swagger.
- **Parameter discovery:** `arjun`/`x8` to find unlinked query/body params (hidden input = hidden
  surface).
- **API spec harvest:** `/openapi.json`, `/swagger.json`, GraphQL introspection (`__schema`).
- Build a **route × method × parameter** matrix — this is your test plan.

### 2.2 Understand auth & session
- Authentication mechanism (form/JWT/OAuth/SAML/API-key), session token location (cookie/header),
  flags (`HttpOnly`, `Secure`, `SameSite`), CSRF protections, token entropy/structure.
- **JWT:** decode header/claims; test `alg:none`, weak HMAC secret (crack with `hashcat`), `kid`
  injection, algorithm confusion (RS256→HS256).
- Map **roles** (anon / user / admin) → drives access-control testing.

### 2.3 Test the vuln classes (behavioral, evidence-based)
- **Injection (SQLi/NoSQLi/cmd/SSTI):** `sqlmap` for SQLi; template markers (`${7*7}`,`{{7*7}}`)
  for SSTI; time-based/OOB for blind.
- **XSS:** reflected/stored/DOM; context-aware payloads; use OOB (Burp Collaborator) for blind.
- **Access control / IDOR:** replay requests as lower-priv user / swap object IDs → the most
  common and highest-impact web class (OWASP A01).
- **SSRF:** any URL/host/webhook parameter → point at internal metadata (`169.254.169.254`),
  internal services, `file://`.
- **Request smuggling:** front-end/back-end parsing mismatch (CL.TE/TE.CL); `smuggler`/Burp.
- **Insecure deserialization, file upload, path traversal, open redirect, CORS misconfig,
  security-header gaps.**
- **Automated first pass:** `nuclei` (cves, exposures, misconfig, default-logins) across the mapped
  routes for known-CVE/quick wins.

---

## 3. Approach from a single system (commands)

```bash
# Map
katana -u https://app.target/ -jc -d 5 -o urls.txt
ffuf -u https://app.target/FUZZ -w raft-medium-directories.txt -mc 200,301,401,403
arjun -u https://app.target/api/item -m GET,POST          # hidden params

# Auth
# (decode JWT, inspect cookies, map roles manually / with Burp)

# Test classes
sqlmap -u "https://app.target/item?id=1" --batch --level 3 --risk 2
nuclei -l urls.txt -t cves/ -t exposures/ -t misconfiguration/ -severity medium,high,critical
# SSRF/XSS/IDOR — driven through Burp Suite with OOB (Collaborator/interactsh)
interactsh-client            # OOB callback listener for blind SSRF/XSS/RCE
```

Prioritize by **impact × reachability**: pre-auth RCE/SQLi/SSRF on internet-facing >> post-auth
self-XSS.

---

## 4. Vulnerability logic (what turns a probe into a finding)

- **Deterministic proof:** SQLi confirmed by boolean/time/OOB oracle; SSRF confirmed by OOB
  callback from the target's IP; XSS confirmed by JS execution.
- **Access control:** identical request, different identity, still succeeds → broken access control.
- **Chain thinking:** low-sev primitives combine (open redirect + OAuth = token theft; SSRF +
  cloud metadata = credential theft + full compromise).
- **Business logic:** race conditions, price/quantity tampering, workflow bypass — not
  tool-detectable; require understanding the app's intended state machine.

---

## 5. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| SPA hides routes/APIs | Client-side rendering | JS-aware crawler (`katana -jc`), parse bundles, harvest API specs, watch XHR in browser |
| WAF blocks payloads | Signature filtering | Encoding/case/comment obfuscation, OOB techniques, timing; note WAF as a control, find bypass within scope |
| Auth required for most surface | Deep app behind login | Obtain test accounts per role; automate session handling in Burp/`ffuf` with cookies |
| Blind/no-feedback vulns | No reflected output | Out-of-band (interactsh/Collaborator) + time-based oracles |
| State/CSRF tokens break automation | Anti-automation | Macro/session-handling rules; extract tokens per request |
| False positives from scanners | Naive pattern matching | Manually verify every scanner hit with a reproducible PoC |
| Rate limiting / lockout | Anti-abuse | Throttle; avoid credential brute; single well-formed proofs |
| Destructive test risk | Payloads that write/delete/spend | Read-only proofs; use safe markers; test on staging where possible |
| Complex auth (OAuth/SAML/JWT) | Multi-party flows | Model the full flow; test each hop (redirect_uri, token validation, alg confusion) |
| Business-logic flaws invisible to tools | Semantics, not syntax | Manual analysis of the intended workflow; abuse-case thinking |

---

## 6. Considerations & guardrails

- **Web tests can mutate data or take real actions** (create orders, send emails, delete records).
  Prefer staging; on production use non-destructive proofs and safe markers.
- **Every finding needs a reproducible PoC** (request/response, steps) — scanner output alone isn't
  a finding.
- **Stay in scope:** don't pivot through SSRF into out-of-scope internal systems without
  authorization; don't exfiltrate real user data.
- **Chain conservatively** — demonstrate impact enough to prove severity, then stop.

---

## 7. References

- **OWASP Top 10 (2021)** and **OWASP Web Security Testing Guide (WSTG)** — the definitive method.
- OWASP API Security Top 10; OWASP ASVS (verification standard / test depth).
- PortSwigger Web Security Academy (authoritative technique references for each class).
- RFC 9110/9112 (HTTP), RFC 7519 (JWT), RFC 6749 (OAuth 2.0), RFC 7235 (HTTP auth).
- Tooling: Burp Suite, katana/ffuf/feroxbuster/arjun, sqlmap, nuclei, interactsh, jwt_tool.
