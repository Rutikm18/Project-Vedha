# OSS Core-Level Study — cloned, read, understood

> Sequence followed: cloned → read core files → extracted core logic → noted
> binaries → collected research papers. **No implementation yet** — this is the
> pre-build checkpoint. Clones live in the session scratchpad (`oss-study/`), not
> committed to the repo.

Tools cloned (shallow): ssh-audit, sslyze, testssl.sh, tlsx, dnsx, nuclei.

---

## 1. Core logic per tool (what actually makes each one work)

### ssh-audit — MIT — pure Python — **fully portable**
- **Core files:** `ssh_socket.py` (SSH transport), `ssh2_kex.py` (KEXINIT parser),
  `ssh2_kexdb.py` (**the database — the crown jewel**), `algorithms.py` (evaluator),
  `banner.py` + `software.py` (banner→software+version+lifecycle), `hostkeytest.py`,
  `gextest.py`/`kexdh.py`/`dheat.py` (GEX modulus + DHEat DoS test),
  `policy.py`/`builtin_policies.py` (compliance policies).
- **Core algorithm:** TCP connect → exchange version banners → read
  `SSH_MSG_KEXINIT` → parse the offered name-lists (per RFC 4253: `cookie(16) +
  kex + hostkey + enc×2 + mac×2 + compression×2 + languages×2 + follows + reserved`)
  → for each offered algorithm, look up `MASTER_DB[category][name]` → aggregate
  failures/warnings/infos. Optional: fetch host key, probe GEX modulus size.
- **DB format (`ssh2_kexdb.py:93`):**
  `'algo_name': [[version_first_appeared], [FAIL...], [WARN...], [INFO...]]`,
  categories `kex / key / enc / mac`. Severity strings are constants
  (`FAIL_SHA1`, `WARN_2048BIT_MODULUS`, `INFO_...`), and it already tags the
  **Terrapin** counter-measure (`INFO_STRICT_KEX`, CVE-2023-48795).
- **Binaries:** NONE. **Action:** vendor `MASTER_DB` + constants verbatim (with the
  MIT notice), reimplement the ~200-line socket/KEXINIT engine in `BaseScanner` style.

### nuclei — MIT — Go — **adopt the architecture, not the binary**
- **Core (`DESIGN.md`):** `Template` (YAML: requests + matchers + extractors) →
  `Parse`/`Compile` → `Executer` → results via callback. A `Request` interface is
  implemented per protocol (http / dns / network / headless / file) with
  `Compile / Match / Extract / ExecuteWithResults / GetCompiledOperators`.
- **Matcher DSL (the whole detection language):** 6 matcher types —
  `status, size, word, regex, binary, dsl` — combined by `matchers-condition:
  and|or`, plus `extractors`. Detections are **data files**, engine is fixed.
- **Reporting:** pluggable `Exporter` (Elasticsearch / markdown / SARIF) + `Tracker`
  (Jira / GitHub / GitLab) + dedup.
- **Maps onto our probe:** Request ≈ `BaseScanner`, Executer ≈ `scan_funnel`,
  operators/matchers ≈ `findings.py _RULES` (make them declarative), exporters ≈
  the manager integrations. **This is the reference design for the content/engine split.**
- **Binaries:** distributed as one compiled Go static binary; source fully readable;
  none committed in the repo (built by goreleaser).

### sslyze — **AGPL-3.0 — DO NOT EMBED** — but it teaches the crypto reality
- **Core depends on `nassl>=5.4,<6`** = a **compiled C-extension wrapping a
  *modified* OpenSSL** that re-enables SSLv2/SSLv3/weak/EXPORT ciphers stock OpenSSL
  removed. This is the "bring-your-own-crypto" truth.
- **Plugins (ScanCommands):** `openssl_cipher_suites` (per-version cipher
  enumeration), `certificate_info`, `robot` (ROBOT/Bleichenbacher oracle —
  `_robot_tester.py`), `session_resumption`, `openssl_ccs_injection`,
  `ems_extension`, fallback SCSV, compression (CRIME), early-data, heartbleed.
- `mozilla_tls_profile/` grades a config against Mozilla's modern/intermediate/old
  JSON baselines.
- **Binaries:** nassl (a binary), separately installed. **Action:** reference the
  *technique* + Mozilla profile; never copy AGPL code into the sealed binary.

### testssl.sh — **GPL-2.0 — DO NOT COPY** — note the shipped binaries
- **Core:** bash + **committed compiled OpenSSL binaries** in `bin/`
  (`openssl.Darwin.x86_64`, `openssl.Linux.x86_64`, `openssl.FreeBSD.amd64`,
  ~3–4 MB each) with legacy support, + data tables (`etc/cipher-mapping.txt`,
  `tls_data.txt`) + raw `/dev/tcp` handshakes for what openssl can't do.
- **Action:** reference conceptually only; GPL blocks copying into the product.

### tlsx — MIT — Go — **the license-clean answer to legacy TLS**
- **Core:** `pkg/tlsx/ztls/ztls.go` uses `github.com/zmap/zcrypto/tls` — ZMap's
  **pure-Go TLS stack that speaks SSLv3/TLS1.0**, no OpenSSL. Plus `auto` (try
  `crypto/tls`, fall back to `ztls`), `jarm/` (JARM active fingerprint), `ja3/`.
- **Why it matters:** this is how you test legacy TLS *without* OpenSSL and *without*
  a copyleft dependency. Python has no zcrypto equivalent → either wrap the tlsx
  binary (MIT) or craft raw ClientHellos ourselves.
- **Binaries:** one compiled Go static binary; MIT.

### dnsx — MIT — Go — DNS
- **Core:** `libs/dnsx/dnsx.go` wraps `projectdiscovery/retryabledns` → `miekg/dns`
  (BSD). AXFR is a one-liner: `d.dnsClient.AXFR(hostname)`; DNSSEC + trace supported.
- **Python equivalent:** `dnspython` — `dns.query.xfr` (AXFR), `dns.dnssec`
  (validation), ISC-licensed, embeddable. **Action:** reimplement in Python with dnspython.
- **Binaries:** one compiled Go static binary; MIT.

---

## 2. Binaries — direct answer to "if there are binaries of main files, let me know"

| Tool | Is the core a binary? | Detail |
|---|---|---|
| **ssh-audit** | ❌ No | Pure Python, 100% readable + portable |
| **nuclei / tlsx / dnsx** (+ naabu/httpx) | ⚠️ Distributed as a binary | Go → single compiled static binary; **source fully readable**; no binary committed in repo (goreleaser builds it) |
| **sslyze** | ✅ Yes (dependency) | Core crypto = **nassl**, a compiled C-extension bundling a modified OpenSSL (AGPL); pip-installed, not in repo |
| **testssl.sh** | ✅ Yes (committed) | Ships prebuilt **openssl binaries in `bin/`** (Darwin/Linux/FreeBSD, 3–4 MB each), GPL |

**Takeaway:** the only tool whose *core logic* is locked behind a binary is sslyze
(nassl) and testssl (bundled openssl) — and both are exactly the copyleft ones we
can't use anyway. Everything we *can* legally absorb (ssh-audit, and the design of
nuclei/tlsx/dnsx) is readable source.

---

## 3. Research papers (foundations behind the techniques)

- **Internet-wide scanning:** Durumeric, Wustrow, Halderman — *ZMap: Fast
  Internet-wide Scanning*, USENIX Security 2013.
  https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_durumeric.pdf
  (10-yr retrospective: https://arxiv.org/pdf/2406.15585)
- **UDP amplification / reflection (your NTP-monlist, DNS open-resolver findings):**
  Rossow — *Amplification Hell: Revisiting Network Protocols for DDoS Abuse*, NDSS 2014.
- **SSH integrity (the modern SSH check):** Bäumer, Brinkmann, Schwenk — *Terrapin
  Attack*, USENIX Security 2024 (CVE-2023-48795). https://terrapin-attack.com/
- **TLS RSA oracle (sslyze robot plugin):** Böck, Somorovsky, Young — *Return Of
  Bleichenbacher's Oracle Threat (ROBOT)*, USENIX Security 2018.
- **Vulnerability prioritization (our risk-scoring core):** Jacobs, Romanosky,
  Edwards, Roytman, Adjerid — *Exploit Prediction Scoring System (EPSS)*, Digital
  Threats: Research & Practice, 2021. https://arxiv.org/abs/1908.04856
- **Passive OS fingerprinting:** Zalewski — *p0f v3* methodology.
- **TLS fingerprinting (you already do ja4s/ja4x):** JA3/JA4 (FoxIO specs), JARM
  (Salesforce).
- **TLS config baseline (grading):** Mozilla Server Side TLS guidelines.

---

## 4. Core-level approaches to follow (derived from what these tools do at their core)

1. **Two-layer engine/content architecture (from nuclei).** A stable executor +
   declarative, versioned, signed detection content. `Request(protocol)` +
   `Executer` + `Operators(matchers/extractors)` mapped onto
   `BaseScanner`/`scan_funnel`/`findings`. **This is the foundational move.**
2. **Data-table-driven protocol audits (from ssh-audit).** Each audit = thin engine
   + a versioned table `name → [versions, fails, warns, infos]`. Vendor ssh-audit's
   `MASTER_DB`; build the same shape for TLS ciphers (from Mozilla profile), SMB, etc.
3. **Bring-your-own-crypto for legacy testing (from sslyze/testssl/tlsx).** Legacy
   TLS/SSH needs crypto the platform withholds. Pick the license-clean path: raw
   handshake crafting (pure-Python, bounded) or wrap `tlsx` (MIT). Never sslyze/testssl.
4. **Fact → finding separation with confidence + provenance + evidence.** Already our
   model; formalize it as the single schema every content module targets.
5. **Declarative compliance-policy layer (from ssh-audit `policy.py` + sslyze Mozilla
   profile).** Grade an observation against a named baseline (Mozilla/CIS/vendor) as
   data, not code.
6. **Pluggable exporter/tracker layer (from nuclei reporting).** Findings flow out to
   SIEM / Jira / SARIF / markdown via one interface.
7. **Version→software→lifecycle intelligence (from ssh-audit `software.py`).** Map
   banners to software + version + EOL/"removed in X" as data — feeds prioritization
   with no CVE DB on the probe.
8. **Prioritization by exploitability, not raw severity (from EPSS).** Core score =
   KEV + EPSS + exposure (vantage data we already have) + asset criticality.

### Recommended first build (on your go-ahead)
- **`ssh_scanner.py`** — vendor `MASTER_DB` (MIT + attribution) behind a thin
  `BaseScanner` KEXINIT engine. Highest value, lowest risk, pure-Python, sealed-safe.
- In parallel, sketch the **engine/content skeleton** (approach #1) so `ssh_scanner`
  is the first module authored *as content*, not hardcoded.

---

# PART 2 — Full arsenal study (ProjectDiscovery + nmap + specialists + wireless)

Cloned this round: naabu, httpx, subfinder, katana, cdncheck, asnmap, mapcidr,
cvemap, uncover, alterx, enum4linux-ng, onesixtyone, aircrack-ng, kismet, nmap.

## THE unifying core-level insight (read this first)

**Every mature tool here is the same architecture: a small generic ENGINE + a
large, versioned, independently-updated DATA FILE. The intelligence is never in the
code — it is in the data.**

| Tool | Engine (code) | Intelligence (data) | Data size |
|---|---|---|---|
| nmap | ultra_scan / service_scan / osscan2 / NSE | `nmap-service-probes` + `nmap-os-db` + NSE | **17,154 + 116,271 lines**, 611 scripts |
| nuclei | protocol executor + matchers | templates | ~10k YAML |
| ssh-audit | KEXINIT parser | `MASTER_DB` | ~37 KB |
| testssl.sh | bash checks | `cipher-mapping.txt` + bundled openssl | — |
| cdncheck | IP-range matcher | `sources_data.json` | **2.6 MB of ranges** |
| subfinder / uncover | concurrent aggregator | source/provider list | ~30+ sources |
| onesixtyone | async send/recv loop | community list | tiny |

There are two data shapes; your engine should support both:
1. **Match-rule data** (regex → verdict): nmap-service-probes, nuclei templates,
   your `service_banner`. For *identify/detect*.
2. **Lookup-table data** (name → properties): ssh-audit `MASTER_DB`, cipher maps,
   cdncheck ranges. For *grade/classify*.

**Lesson:** tools that hardcoded detections died; tools that separated a stable
engine from versioned content (nmap, nuclei) dominate. Our value and our moat will
be the **content**, so the architecture MUST separate engine from content (approach #1).

## Extended inventory — license · core logic · binary · fit

### ProjectDiscovery (ALL MIT, Go — copy design/data freely, with attribution)
- **naabu** — port scanner. Core `pkg/scan/scan_raw.go` (39 KB): stateless SYN via
  gopacket with **SYN cookies** (`syncookie.go` — encodes the target into the TCP
  seq so replies match with no per-port state, the ZMap/masscan trick), `connect.go`
  fallback, `icmp/arp/ndp` discovery. *Fit:* you have `syn_scanner.py`; **adopt the
  SYN-cookie stateless technique** for scale. Binary (Go static).
- **httpx** — HTTP prober. Core `common/httpx/httpx.go`: status/title/tech/response-
  hash/CDN/JARM. *Fit:* overlaps `web_scanner.py`; reference for tech-detect + body
  hashing. Binary.
- **subfinder** — passive subdomain aggregation. Core `pkg/subscraping/sources/*`
  (~30+ API source integrations) + concurrent dedupe agent. *Fit:* **manager-side**
  recon (needs internet + API keys). Binary.
- **katana** — crawler. Core `pkg/engine/{standard,headless,hybrid}` + `parser`
  (standard=HTTP, headless=chromedp browser). *Fit:* manager-side web-app pre-flight.
  Binary.
- **cdncheck** — CDN/WAF/cloud detection. Core: `sources_data.json` (**2.6 MB of
  provider IP ranges**) + range match in `cdncheck.go`. *Fit:* **HIGH** — enrich your
  exposure/vantage findings ("port open but behind Cloudflare"); the DATA is the
  value and it's MIT. Binary + data.
- **asnmap** — ASN→CIDR via PD whois/BGP API. *Fit:* scope expansion, manager-side. Binary.
- **mapcidr** — pure CIDR arithmetic (split/aggregate/dedupe). *Fit:* reference for
  target expansion (you have `expand_targets`). Lib/binary.
- **cvemap** — CVE navigation. Core: **API client to `cloud.projectdiscovery.io`**
  (hosted CVE library, NOT a local DB). *Fit:* manager-side enrichment; note it's a
  hosted service, not embeddable data. Binary.
- **uncover** — search-engine host discovery. Core `pkg/agent/provider.go` aggregates
  Shodan/Censys/Fofa/Quake/Hunter/ZoomEye/Netlas. *Fit:* manager-side external recon
  (API keys). Binary.
- **alterx** — subdomain permutation DSL. *Fit:* manager-side recon. Binary.

### Specialists
- **ssh-audit** — MIT, Python. [Part 1] engine + `MASTER_DB`. **COPY/VENDOR.** No binary.
- **onesixtyone** — **GPL-2.0** (⚠ corrected 2026-08: this draft first said BSD, but
  the `onesixtyone.c` header + LICENSE are GPL v2 — `Copyright (C) 2002,2003
  solareclipse@phreedom.org`), C. Core `onesixtyone.c`: **decoupled async send/recv**
  — blast SNMP GET (community list; defaults public/private) fire-and-forget over UDP
  to many hosts, collect replies in a non-blocking loop → huge scale. *Fit:* GPL =
  **reference the technique only**; reimplement the async fire-and-forget pattern
  natively to scale `snmp_scanner` community discovery. Tiny C, no shipped binary.
- **enum4linux-ng** — **GPLv3**, Python. Core `enum4linux-ng.py`: orchestrates Samba
  CLI (`net`,`nmblookup`,`smbclient`,`rpcclient`) + **RID cycling** (500-550,1000-1050
  via `rpcclient lookupsids`), share enum, NetBIOS, LDAP, password policy. *Fit:*
  **reimplement the techniques natively with the `impacket` you already ship** (SAMR/
  LSAT RID cycling, share enum) — do NOT copy GPL code, do NOT shell to Samba. Depends
  on external Samba binaries.
- **testssl.sh** — GPL-2.0, bash + **committed openssl binaries in `bin/`** + cipher
  data. **REFERENCE ONLY.**
- **sslyze** — AGPL-3.0, Python + **nassl** (compiled modified OpenSSL). **REFERENCE ONLY.**

### Wireless — need monitor-mode / SDR hardware → OUT OF SCOPE for a network probe
- **aircrack-ng** — GPL-2.0, C. Core `lib/ptw/aircrack-ptw-lib.c` (PTW WEP recovery),
  `lib/cowpatty` + `lib/ce-wpa/wpapsk.c` (WPA-PSK dict/PMK). Requires captured 802.11
  frames from a monitor-mode NIC. *Fit:* **OUT OF SCOPE** (hardware) unless you ship a
  dedicated wireless sensor appliance.
- **kismet** — GPL-2.0, C++. Core `capture_linux_wifi` + `datasourcetracker`: passive
  RF capture across many radios (wifi/BT/zigbee/SDR) + device tracking/IDS. Requires
  monitor-mode/SDR hardware. *Fit:* **OUT OF SCOPE** (hardware) — same caveat.

### nmap — NPSL 0.95 (GPLv2-derived, commercial-restricted)
- The core "logic" is **DATA**: `nmap-service-probes` (17,154 lines / 5.1 MB —
  `Probe`/`match`/`softmatch` regex→product rules) and `nmap-os-db` (116,271 lines /
  2.5 MB — TCP/IP stack `SEQ(SP=…GCD=…)` fingerprints→OS) + **611 NSE Lua scripts**.
  Engines: `ultra_scan` (scan), `service_scan` (version-match engine), `osscan2` (OS
  match), NSE (Lua). *Fit:* **can't copy the DBs into a commercial product** (NPSL);
  keep as optional external engine (you already have `nmap_wrapper.py`), and reference
  the `Probe/match` data-file *design* for building your own service-detection table.

## License-tiered adoption plan (the actionable list)

- **Tier 1 — COPY / VENDOR (MIT/BSD, embeddable):** ssh-audit (`MASTER_DB`),
  cdncheck (`sources_data.json`), all PD Go tools'
  design + data, dnsx/mapcidr logic. → straight into the probe / content packs.
- **Tier 2 — REFERENCE ONLY (GPL/AGPL/NPSL — technique, never code):** testssl,
  sslyze, enum4linux-ng, onesixtyone, aircrack-ng, kismet, nmap data files. Reimplement natively.
- **Tier 3 — WRAP AS OPTIONAL EXTERNAL BINARY (separate distribution):** nmap
  (already), tlsx, nuclei, katana — power-user / "fat image" / manager path.
- **Tier 4 — MANAGER-SIDE / internet-facing (need egress + API keys):** subfinder,
  uncover, asnmap, cvemap, live cdncheck.
- **OUT OF SCOPE — wireless (aircrack, kismet):** monitor-mode hardware; only if a
  dedicated wireless sensor product is on the roadmap.
