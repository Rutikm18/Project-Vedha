# 03 — External Web Triage (Core-Level Playbook)

> **Goal:** Rapidly map and risk-rank an organization's **externally reachable web attack
> surface** — domains, subdomains, virtual hosts, TLS posture, technologies, and obviously
> exposed/dangerous endpoints — *before* deep app testing (`10_web_app_triage.md`). Triage =
> breadth + prioritization, not exhaustive exploitation.

---

## 1. Core theory: the web surface is bigger than the IPs

A single IP can host **hundreds of sites** (name-based virtual hosting via HTTP `Host:` header /
TLS SNI). Conversely one hostname can resolve to **many IPs** (CDN, load balancers, GeoDNS). So
web triage is fundamentally about **the name→IP→service graph**, not a port list:

- **HTTP/1.1 `Host` header + TLS SNI** decide *which site* answers on a shared IP. Scanning the IP
  with no `Host` gives you the default vhost — often not the real target.
- **CDN/WAF fronting** (Cloudflare, Akamai, CloudFront) means the IP you hit is the edge, not
  origin. Finding the **origin IP** (via cert transparency, DNS history, SSRF, misconfig) is a
  recurring triage objective.
- **TLS certificates are an intelligence goldmine:** SANs enumerate sibling hostnames; issuer,
  validity, and cipher suites reveal posture. Certificate Transparency (CT) logs let you
  enumerate subdomains *passively* with zero packets to the target.

---

## 2. The triage pipeline (breadth-first)

### 2.1 Passive asset discovery (no packets to target)
- **CT logs:** `crt.sh`, `censys`, `certspotter` → subdomains from every cert ever issued.
- **Passive DNS / OSINT:** `amass enum -passive`, `subfinder`, `assetfinder`.
- **Search/attack-surface engines:** Shodan, Censys, FOFA — already-scanned banners, techs, CVEs.
- **DNS records:** A/AAAA/CNAME/MX/TXT/NS; SPF/DMARC (email spoofability); wildcard detection.

### 2.2 Active resolution & liveness
- Resolve all candidate names (`dnsx`/`massdns`) → dedupe to IPs.
- **HTTP probing:** `httpx -status-code -title -tech-detect -tls-grab -follow-redirects` across
  ports 80/443/8080/8443/etc. This is the core triage sweep — it tells you which names actually
  serve HTTP, their titles, status, redirect chains, and detected tech.

### 2.3 Fingerprinting (what is it?)
- **Server/tech stack:** `Server` header, `X-Powered-By`, cookies (`JSESSIONID`=Java,
  `PHPSESSID`=PHP, `.AspNet`=IIS), favicon hash (mmh3 → Shodan pivot), JS frameworks, `Wappalyzer`
  fingerprints. Same principle as Nmap version detection (`fresh_implement.md §8`) but at L7.
- **TLS posture:** `sslscan`/`testssl.sh`/`tls-scan` → protocol versions (SSLv3/TLS1.0 = finding),
  weak ciphers, cert expiry, self-signed, weak keys, Heartbleed/ROBOT class issues.
- **WAF/CDN detection:** `wafw00f`; timing/behavior differences; edge headers (`cf-ray`,
  `x-amz-cf-id`, `x-akamai-*`).

### 2.4 Exposure hunting (the actual triage findings)
- **Dangerous defaults & panels:** `/admin`, `/actuator` (Spring), `/.git/`, `/.env`, `/server-status`,
  phpMyAdmin, Jenkins, GitLab, Grafana, Kibana, Swagger/`/openapi.json`, `/wp-login.php`.
- **Cloud metadata / SSRF indicators, open redirects, directory listing, backup files**
  (`.bak`,`.old`,`.zip`), source leaks.
- **Automated template scan:** `nuclei -t exposures,misconfiguration,cves,default-logins` — this
  is the workhorse; templates encode behavioral checks (not just banners) → low false positives.

---

## 3. Approach from a single system (commands)

```bash
# Passive breadth
subfinder -d target.com -all -silent | anew subs.txt
amass enum -passive -d target.com | anew subs.txt
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | anew subs.txt

# Resolve + probe
dnsx -l subs.txt -a -resp -silent | anew resolved.txt
httpx -l subs.txt -sc -title -tech-detect -tls-grab -favicon -follow-redirects -o web.txt

# TLS posture (per host)
testssl.sh --quiet --color 0 https://app.target.com

# Templated triage
cat web.txt | nuclei -severity low,medium,high,critical \
   -t exposures/ -t misconfiguration/ -t default-logins/ -t cves/
```

Prioritize outputs by: **internet-facing + auth-less + known-CVE/default-cred + sensitive-data**.

---

## 4. Vulnerability logic (what turns triage into findings)

- **Version/tech + public CVE** (e.g., exposed Confluence/Exchange/Citrix version → RCE CVE).
- **Exposed management/telemetry** (`/actuator/env` leaking secrets; open Kibana; Jenkins script
  console) → often direct RCE or credential disclosure.
- **TLS weaknesses** → downgrade/MITM potential; expired/mismatched cert → phishing/trust issues.
- **Missing security headers** (HSTS, CSP, X-Frame-Options) → informational-to-medium.
- **Subdomain takeover** — a CNAME pointing to a de-provisioned cloud resource (S3/Azure/GitHub
  Pages) you can claim. Detected by dangling-CNAME + service-specific error fingerprints.
- **Origin IP exposure behind CDN** → bypass WAF entirely.

---

## 5. Challenges & how to tackle them

| Challenge | Root cause | Tackle |
|-----------|-----------|--------|
| CDN/WAF hides origin | Edge fronts real server | CT logs, DNS history (SecurityTrails), SSRF, `Host`-header origin probing, favicon/JARM pivot on Shodan |
| Wildcard DNS pollutes results | `*.target.com` resolves everything | Detect wildcard (resolve random sub); filter by response fingerprint/content hash |
| Rate limiting / WAF blocks bulk probing | Bursty httpx/nuclei | Throttle (`-rl`), rotate source IPs, respect robots-less scope, spread over time |
| Virtual hosts hidden | Default vhost != target | Fuzz `Host:` header with candidate names; use SNI variations; vhost brute with wordlists |
| Scope ambiguity (shared hosting/CDN IP) | One IP, many orgs | Confirm ownership by hostname, not IP; never attack a shared IP indiscriminately |
| Banner/version spoofing | Server headers stripped/faked | Behavioral fingerprints (error pages, timing, favicon hash, JARM TLS fingerprint) |
| Huge subdomain list, mostly dead | Passive sources include stale records | `httpx` liveness filter first; cluster by response similarity |
| JS-heavy SPAs hide endpoints | Client-side routing | Parse JS for routes/APIs (`linkfinder`, `katana`); handoff to `10_web_app_triage.md` |
| HTTP/2 / HTTP/3 differences | Old tools assume HTTP/1.1 | Use h2/h3-aware clients; check for request-smuggling surface |

---

## 6. Considerations & guardrails

- **Only test hostnames/IPs you can prove the client owns.** Shared IPs and CDNs make it easy to
  hit third parties — verify ownership per asset.
- **Passive-first** minimizes footprint and legal risk; escalate to active probing within scope.
- Triage **prioritizes**, it does not fully exploit — deep testing is `10_web_app_triage.md`.
- Record request/response evidence for each finding.

---

## 7. References

- RFC 9110/9112 (HTTP semantics/1.1), RFC 6066 (TLS SNI), RFC 6962 (Certificate Transparency).
- OWASP Web Security Testing Guide (WSTG) — Information Gathering chapters.
- OWASP Amass, ProjectDiscovery suite (subfinder/dnsx/httpx/nuclei/katana), testssl.sh.
- JARM (Salesforce) active TLS fingerprinting; mmh3 favicon-hash pivoting (Shodan).
- Nmap version-detection analogy: `../fresh_implement.md §8`.
