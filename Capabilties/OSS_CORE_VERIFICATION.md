# OSS Core-Level Verification — cloned, read, verified firsthand

> Companion to `OSS_CORE_STUDY.md`. That doc was the first-pass study; this one is
> the **firsthand verification**: every repo below was re-cloned (shallow) and its
> named core files were opened and measured, not recalled. Purpose: confirm we have
> the core-level logic to reimplement each in-scope capability **in the current
> probe architecture, with zero copyleft/binary embedding**.
>
> Clones live in the session scratchpad (`oss-study/`), nothing committed.
> Verified: 2026-08-24.

## Correction to `OSS_CORE_STUDY.md`
- **onesixtyone is GPL-2.0, NOT BSD.** File header + LICENSE both say GPL v2
  (`Copyright (C) 2002,2003 solareclipse@phreedom.org`). It moves from
  *Tier 1 (copy/vendor)* to *Tier 2 (reference the technique only)*. The async
  fire-and-forget UDP technique is still reimplementable (techniques aren't
  copyrightable); we simply must not copy the C source.

## Master table — core logic · binary status · reimplementability

| Tool | License | Lang | Core logic (verified) | Ships as binary? | Intelligence (data) | Reimplement in our arch? |
|---|---|---|---|---|---|---|
| **ssh-audit** | MIT | Python | `ssh_socket.py` (452L transport) → `ssh2_kex.py` (147L KEXINIT parser) → `ssh2_kexdb.py` (**500L DB**: `FAIL_/WARN_/INFO_` consts + `name→[ver,fails,warns,infos]`) → `algorithms.py` (203L eval); `banner.py`+`software.py` (250L) banner→sw→EOL | **No** — pure Python | `ssh2_kexdb` ~37KB | ✅ VENDOR DB + ~200L engine (in progress) |
| **dnsx** | MIT | Go | AXFR one-liner `d.dnsClient.AXFR()` via `retryabledns`→`miekg/dns`; DNSSEC/trace | Yes (Go static) | — | ✅ reimplement w/ `dnspython` |
| **cdncheck** | MIT | Go | IP-range matcher over `sources_data.json` (**2.6M**; `cdn/waf/cloud/common`→provider→ranges) | Yes (Go static)+data | 2.6M ranges | ✅ VENDOR the JSON data |
| **nuclei** | MIT | Go | Template→Compile→Executer; matcher DSL (`Status/Words/Regex/DSL/Binary/Size`+`and\|or`+extractors); pluggable exporters | Yes (Go static) | ~10k YAML | ✅ adopt DESIGN for content/engine split |
| **naabu** | MIT | Go | Stateless SYN via SYN-cookies (`syncookie.go` 70L — target encoded in TCP seq, no per-port state) | Yes (Go static) | — | ✅ adopt technique for `syn_scanner` |
| **httpx** | MIT | Go | HTTP probe: status/title/tech/body-hash/JARM/CDN | Yes (Go static) | — | ◐ reference for `web_scanner` |
| **tlsx** | MIT | Go | `ztls`/`ctls` — ZMap `zcrypto` pure-Go TLS speaking SSLv3/TLS1.0 without OpenSSL; JARM/JA3 | Yes (Go static) | — | ◐ license-clean legacy-TLS path (wrap or raw ClientHello) |
| **mapcidr** | MIT | Go | CIDR split/aggregate/dedupe | Yes (Go) | — | ◐ reference for `expand_targets` |
| **subfinder/uncover/asnmap/alterx/katana** | MIT | Go | Concurrent aggregators over external APIs (Shodan/Censys/whois/crawl) | Yes (Go static) | provider lists | △ manager-side (egress+API keys) |
| **cvemap** | MIT | Go | API client to hosted `cloud.projectdiscovery.io` (not a local DB) | Yes (Go static) | hosted | △ manager-side enrichment |
| **sslyze** | **AGPL-3.0** | Python | Depends on `nassl>=5.4,<6` = compiled C-ext bundling modified OpenSSL; `robot` plugin, cert_info, Mozilla-profile grader | Yes (nassl C-ext) | Mozilla profiles | ⛔ REFERENCE ONLY (copyleft); take technique+Mozilla data |
| **testssl.sh** | **GPL-2.0** | bash | bash + **committed openssl binaries** in `bin/` (`openssl.Linux.x86_64` 4.3M, Darwin, FreeBSD) + cipher tables + raw `/dev/tcp` | Yes (committed openssl) | cipher tables | ⛔ REFERENCE ONLY (copyleft) |
| **enum4linux-ng** | **GPL-3.0** | Python | Orchestrates Samba CLI + RID cycling (`RID_RANGES="500-550,1000-1050"`), share enum, NetBIOS, LDAP, pw-policy | No (shells to Samba) | — | ⛔ REFERENCE technique; reimplement via impacket |
| **onesixtyone** | **GPL-2.0** ⚠ | C | Decoupled async send/recv (963L) — fire-and-forget SNMP GET over UDP, non-blocking collect | No committed binary | community list | ⛔ REFERENCE technique only (GPL) |
| **nmap** | **NPSL** (restricted) | C+Lua | Engines `ultra_scan/service_scan/osscan2`/NSE over DATA: `nmap-service-probes` (17,154L/2.5M), `nmap-os-db` (116,271L/5.1M), 611 NSE | Yes (compiled C)+data | the DBs are the value | ⛔ can't copy DBs; keep as optional external binary (`nmap_wrapper.py`)+reference design |
| **aircrack-ng** | GPL-2.0 | C | PTW WEP / WPA-PSK from captured 802.11 frames | Yes (compile) | — | 🚫 OUT OF SCOPE (monitor-mode NIC) |
| **kismet** | GPL-2.0 | C++ | Passive RF capture + device tracking across radios/SDR | Yes (compile) | — | 🚫 OUT OF SCOPE (SDR hardware) |

Legend: ✅ take & build · ◐ take design/technique · △ manager-side · ⛔ reference-only · 🚫 out of scope.

## Binary answer, distilled
- **Go tools** (tlsx, dnsx, nuclei, naabu, httpx, subfinder, katana, cdncheck, asnmap, mapcidr, cvemap, uncover, alterx): all compile to **one static Go binary via goreleaser**; **source fully readable, no binary committed**. We copy design+data, never a binary.
- **Only two are genuinely binary-locked at the core** — and they're the copyleft ones we reference-only anyway: **sslyze** (nassl) and **testssl.sh** (committed openssl).
- **ssh-audit** (our #1 target) is **100% pure-Python, no binary** — cleanest possible port.

## Capability → source → build plan

| Capability | Source (verified) | We take | We build | Binary dep? | Ready |
|---|---|---|---|---|---|
| SSH algo/config audit | ssh-audit (MIT) | vendor `MASTER_DB`+constants | ~200L KEXINIT engine, `BaseScanner` style | No | ✅ in progress |
| DNS AXFR/DNSSEC/version.bind | dnsx (MIT) | technique | `dnspython` scanner (TCP/53, size cap) | No | ✅ |
| SNMP community scale | onesixtyone (GPL) | async pattern (technique) | native async send/recv | No | ✅ |
| SMB null-session/LDAP anon/RID cycle | enum4linux-ng (GPL) | technique | native via impacket (already shipped) | No | ✅ (policy call first) |
| CDN/WAF/cloud exposure enrichment | cdncheck (MIT) | vendor `sources_data.json` (2.6M) | range-match enrich layer | No | ✅ |
| Content/engine split (detection packs) | nuclei (MIT) | matcher-DSL design | declarative rules over facts | No | ✅ design ready |

## The only two decisions (not missing logic — both already in `IMPLEMENTATION_RISKS`)
1. **Legacy TLS crypto substrate.** stdlib `ssl` can't *offer* protocols system OpenSSL
   removed (SSLv2/3, EXPORT, RC4) → can't test them with it. Build-vs-buy: (a) craft
   raw ClientHellos in pure Python (bounded, sealed-safe), or (b) wrap MIT **tlsx**.
   Never sslyze/testssl.
2. **CVE correlation + vantage problem.** cvemap is a hosted service, not embeddable;
   NVD/KEV/EPSS need a feed pipeline; probe-inside-network vs manager-in-cloud
   reachability is unresolved. Manager-side architecture, not probe logic.
