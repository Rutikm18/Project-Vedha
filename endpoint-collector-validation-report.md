# Endpoint Collector Validation & Detection-Engineering Report
 
**CONFIDENTIAL · INTERNAL DETECTION-ENGINEERING**
 
Field validation of the macOS agent's 42 telemetry collectors (25 core + 17 deep-mesh), each assessed as a security telemetry source: data-quality defect, the detection logic it should implement, ATT&CK mapping, and adversary evasion / edge cases. Section 7 gives per-collector engineering enhancement depth for every flagged source. Findings grounded in current (2025–2026) threat research.
 
| Field | Value |
|---|---|
| Lab host | Rutiks-MacBook-Air · Apple M4 · macOS 26 (25E253) |
| Agent | com.attacklens.agent (PID 52497) + watchdog |
| Method | synthetic create → verify (local) → dashboard → cleanup |
| Test IPs | RFC-5737 TEST-NET (198.51.100.0/24) |
| Date | 2026-09-23 · rev 2 |
| Scope | 42 collectors, positive + negative control each |
 
---
 
## 1 · Executive summary
 
The collection layer is broadly sound — port, network, sysctl, user, security-posture, and most deep-mesh (MCP, extensions, native-messaging) collectors captured injected lab artifacts and reflected real state accurately. Validation surfaced **one high-severity code defect that recurs across the package collectors** and a broad class of **detection-logic gaps** where data is collected but the security signal is never evaluated (marked RETEST / NOT AS EXPECTED and expanded in §7).
 
**Scorecard:** 15 pass · 8 not-as-expected · 1 bug (P1) · 10 retest · 8 pending = 42
 
> **Most significant finding (P1).** The Node package collector reports `available:true, ok:false, error:"ValueError", package_count:0`. The manager is installed and found, but the output parser throws and the result is silently coerced to an empty set — a parse failure presented as "clean host." This produces **false-negative supply-chain coverage** exactly where 2025–2026's most active threats live (Shai-Hulud npm worm⁶, @antv "Mini Shai-Hulud"⁷).
 
---
 
## 2 · Top findings, ranked
 
| # | Sev | Finding | Evidence | Impact |
|---|---|---|---|---|
| 1 | P1 | npm/bun parser crash masked as empty inventory | `ok:false ValueError`, `count:0`, `root:null` | False-negative on the most active supply-chain surface |
| 2 | P1 | Plaintext secret in shell startup not flagged | `API_KEY="30a9e044…"` in `~/.zshrc`, `suspicious:false` | Credential exposure (T1552.001) undetected |
| 3 | P2 | `/etc/hosts` redirect not flagged | `3.108.231.92 app.harmonic-bartos.test`, `suspicious:false` | Traffic redirection / spoofing (T1565.001) |
| 4 | P2 | Scheduled-task execution history absent | all tasks `last_run/next_run: null` | Cannot distinguish dormant vs active persistence |
| 5 | P2 | "Error" indistinguishable from "empty" on dashboard | `count:0` on parse failure | Violates NOT_EVALUATED-vs-found-nothing principle |
| 6 | P3 | AI Applications keys only on known binaries | 0.0.0.0:11434 seen as port, not classified | Generic exposed inference server missed⁴ |
| 7 | P3 | Homebrew / Python package data empty | same swallow-to-empty pattern | Incomplete SBOM basis |
| 8 | P3 | Cron update not reflected; Weekday/WeekDay key case | parser inconsistency | Minor drift-detection gaps |
 
---
 
## 3 · Core collectors (25)
 
Legend: **PASS** captured + correct · **NOT AS EXP.** collected but wrong/missing signal · **RETEST** partial / needs cycle / logic unverified · **BUG** code defect · **PENDING** not yet exercised
 
| Collector | Status | Defect / observation | Detection logic it should implement | ATT&CK |
|---|---|---|---|---|
| Packages | NOT AS EXP. | Under-counts; parse failures upstream (§7.1) | KEV/EPSS CVEs on reachable components; malware-named pkgs | T1195.002 |
| Processes | NOT AS EXP. | New proc + lineage slow to dashboard (§7.7) | Office→shell lineage, interpreter spawn, unsigned exec | T1059 / T1106 |
| Connections | NOT AS EXP. | Short-lived egress capture inconsistent (§7.8) | Beaconing periodicity + egress to IOC/rare dest | T1071 / T1041 |
| Open Files | NOT AS EXP. | Read-burst capture inconsistent (§7.9) | ≥4 sensitive reads / 120s = credential staging² | T1552 / T1074.001 |
| Binaries | RETEST | Confirm hash + signing captured (§7.10) | sha256→intel; unsigned/xattr-cleared; fleet-rarity | T1204 / T1553 |
| Configs | RETEST | Reads fully; misses `/etc/hosts` redirect (§7.5) | hosts redirects, weak sshd/sudoers, self-source | T1565.001 |
| SBOM | RETEST | Dependent on package layer (§7.3) | Component drift w/o build event; reachability join | T1195 / T1554 |
| Services | RETEST | Lab service appeared only after reload (§7.11) | Unsigned/non-Apple daemon; new-service fleet drift | T1543.001 |
| Tasks | RETEST | `last_run/next_run` null; key-case bug (§7.12) | Jobs w/ network-fetch/encoded/reverse-shell cmd | T1053.003 |
| Dev Security | RETEST | Repo-secret test staged (§7.15) | Committed secrets, .env in git, insecure git cfg | T1552.001 |
| Ports | PASS | Port 9999 LISTEN captured | Unexpected listener on non-standard port + owner | T1571 |
| Users | PASS | `labf` surfaced on add, gone on delete | New admin/hidden account; UID<500 anomalies | T1136.001 |
| Sysctl | PASS | `ip.forwarding=1` drift captured; IPv6=0 held | Drift of hardening keys (forwarding, redirect, AMFI) | T1562.001 |
| sca | PASS | CIS scan present | Failed controls scored; unknown≠fail | — |
| Security | PASS | Firewall off/on reflected | Gatekeeper/SIP/FileVault posture drift | T1562.001 |
| Network | PASS | `lo0` alias 127.0.0.55 + full iface detail | New iface/route, promiscuous mode, rogue DNS | T1016 |
| ARP | PASS | Neighbor entries populate | ARP-spoof (dup MAC/IP), gateway MAC change | T1557.002 |
| Containers | PASS | Baseline captured | Privileged/root containers; vulnerable base image | T1610 |
| Agent Health | PASS | Agent + watchdog running | Dead-man: silence >3× interval while powered² | T1562.001 |
| Storage / Mounts | PENDING | DMG test staged (`LABVOL`) | New external/removable mount; exfil-staging volume | T1052.001 |
| Hardware | PENDING | USB insert = manual | New USB mass-storage / HID-injection device | T1200 |
| Apps | PENDING | Count looked low (2) | Unsigned/quarantine-cleared app in /Applications | T1204.002 |
| Metrics / Battery | PENDING | Passive — confirm live update | Baseline for cryptomining CPU / anomaly | T1496 |
 
---
 
## 4 · Deep-mesh / dev-security collectors (17)
 
| Collector | Status | Defect / observation | Detection logic it should implement | ATT&CK |
|---|---|---|---|---|
| Node Packages | **BUG** | **ValueError parser crash → empty (§7.2)** | Typosquats, install-scripts, preinstall exfil, Bun evasion⁶ | T1195.002 |
| AI Applications | NOT AS EXP. | Keys on binaries; generic listener missed (§7.16) | Any `0.0.0.0` model-server bind, auth=false⁴ | T1190 / T1133 |
| Cron Jobs | NOT AS EXP. | Updated job not reflected (§7.13) | curl\|base64\|/dev/tcp in schedule commands | T1053.003 |
| Python Packages | NOT AS EXP. | Same swallow-to-empty (§7.2) | `.pth`/sitecustomize exec; malicious PyPI advisory | T1546 / T1195.002 |
| Homebrew | NOT AS EXP. | No valid data — scan-path/prefix (§7.2) | Unofficial taps; trojanized formula⁵ | T1195.002 |
| AI / Agent CLI | RETEST | Scan limited to known dev roots (§7.16) | Injection in `CLAUDE.md/.cursorrules`; sandbox-off run³ | T1059 / T1204 |
| Shell Startup | RETEST | **Misses plaintext API_KEY**; self-source (§7.6) | Secret patterns + `eval $(curl)` in startup files | T1546.004 / T1552.001 |
| Git | RETEST | Hook-poison test staged (§7.14) | Hook exec primitives; `core.hooksPath` redirect | T1546 / T1195.002 |
| Credential Locations | RETEST | Staging-burst correlation to confirm (§7.9) | Cluster reads .ssh/.aws/Keychain/Cookies → exfil² | T1552 / T1555 |
| MCP Servers | PASS | Shell-exec config surfaced | Rug-pull: L2 drift on `hash(name+desc+schema)`; injection; unpinned¹ | T1195.002 / T1204 |
| Editor Extensions | PASS | Sideloaded `evil-ext` flagged | Non-marketplace install; obfuscation + `child_process.exec` | T1176.002 |
| Native Messaging | PASS | `com.test.evil`→user-writable script flagged | Manifest path user-writable + wildcard origin | T1176 / T1059 |
| Listening Ports | PASS | 11434 bind captured | 0.0.0.0 binds on inference/dev-tool ports | T1571 |
| Processes (mesh) | PASS | Captured | Coding-agent → curl/ssh/aws within 60s = exfil¹ | T1552 / T1041 |
| LaunchDaemons | PASS | `com.test.evil` plist flagged | Script/curl-pipe ProgramArguments; vendor impersonation | T1543.001 |
| Browser Extensions | PENDING | Needs load in Chrome to register | `<all_urls>`+cookies+debugger infostealer combo | T1539 / T1185 |
| Docker | PENDING | Daemon not fully up (socket stopped) | Privileged containers; vulnerable images; exposed API | T1610 / T1611 |
 
---
 
## 5 · Detailed findings — root cause & remediation
 
### F-1 · Package-manager parser crash reported as empty inventory — P1
*T1195.002 Supply chain*
- **Evidence:** `"npm":{"available":true,"ok":false,"error":"ValueError","packages":[],"package_count":0,"root":null}`; identical for `bun`.
- **Root cause:** Command runs (available:true) but output parsing throws — most likely `npm ls -g --json` emitting non-JSON warnings on stderr, or an `undefined`/empty field coerced to int. The exception is caught and coerced to an empty array; `npm root -g` never runs, hence `root:null`.
- **Why it matters:** `npm install` is now an RCE primitive: Shai-Hulud (Sep + Nov 2025, 700–800+ pkgs, 20M weekly downloads) executes in **preinstall** and installs Bun to evade Node monitoring.⁶ Empty-on-failure = zero coverage precisely here.
- **Fix:** (1) Never coerce a parse failure to `[]` — emit `ok:false` with raw stderr + failing command. (2) Resolve `root` independently. (3) Surface `ok:false` as a distinct dashboard error state, not `count:0`. (4) Audit Python/Homebrew for the same swallow.
### F-2 · Plaintext credential in shell-startup not flagged — P1
*T1552.001 Credentials in files*
- **Evidence:** `export API_KEY="30a9e044…"` in `~/.zshrc`, `suspicious:false`; a self-referential `source ~/.zshrc` on the same line also unflagged.
- **Why it matters:** Startup files are a primary infostealer target (AMOS/Poseidon harvest these + Keychain/browser stores).²
- **Fix:** Content-scan for entropy + key formats (`AKIA`, `ghp_`, `sk-`, generic `API_KEY=`); flag `eval $(curl…)` / self-source. Redact value in evidence. **Action:** rotate this key — it has been on disk in plaintext.
### F-3 · /etc/hosts redirect not flagged — P2
*T1565.001*
- **Evidence:** `3.108.231.92  app.harmonic-bartos.test`, `suspicious:false`.
- **Fix:** Flag non-default hosts entries mapping names to public IPs / suspicious TLDs; diff vs known-good baseline.
### F-4 · Scheduled-task execution history absent — P2
*T1053*
- **Evidence:** all 18 tasks `last_run/next_run:null`; `Weekday` vs `WeekDay` key-case mismatch (`gkreport` vs `csrutil.report`). Three third-party updaters run as **root** on interval.
- **Fix:** Populate last/next run from `launchctl print`; normalize schedule-key parsing.
### F-5 · Exposed-inference detection too narrow — P3
*T1190 / T1133*
- **Evidence:** `0.0.0.0:11434` captured as a port but not classified as exposed AI app (classifier keys on known inference binaries).
- **Why it matters:** 175,000 internet-reachable Ollama hosts (~23k persistent); ~20% of a Cisco/Shodan sample served models with no auth.⁴ The signal is bind + auth state, not binary name.
- **Fix:** Flag any listener on inference/dev ports bound to `0.0.0.0` with auth=false, independent of process identity.
---
 
## 6 · Prioritised remediation roadmap
 
| Pri | Action | Collector(s) | Principle |
|---|---|---|---|
| P1 | Never coerce a parse failure to empty; surface an explicit error state | Node/Python/Homebrew pkgs | Error ≠ empty |
| P1 | Add secret + malicious-content scanning to shell-startup and config files | Shell Startup, Configs, Dev Security | Content, not inventory |
| P2 | Populate task execution history; normalize schedule keys | Tasks, Cron | Timing enables correlation |
| P2 | Move event-window rules to an EndpointSecurity event stream | Processes, Open Files, Connections, Credential Locations | Events over snapshots |
| P2 | Classify exposed inference by bind+auth, not binary name | AI Applications | Signal over signature |
| P3 | Reachability join + KEV/EPSS on package/SBOM findings; lockfile parse | SBOM, Packages, Binaries | Exploitability-first⁸ |
 
---
 
## 7 · Technical enhancement deep-dive (flagged collectors)
 
For each collector: **Gap → Root cause → Enhancement (data-model / engineering) → Detection (concrete rules & thresholds) → Evasion / edge cases.**
 
### 7A · Package & supply-chain family
 
**7.1 Packages — NOT AS EXP.**
- **Gap:** Aggregate under-counts; the top-level count is derived from per-manager parsers that fail independently, with no cross-check against OS receipts.
- **Root cause:** Single aggregate field hides per-source health; no reconciliation with `pkgutil --pkgs` / `system_profiler SPApplicationsDataType`.
- **Enhancement:** Model each manager as an independent source with its own `{available, ok, error, count, root}`. Build a unified component graph = union(npm, pip, brew, pkgutil) with per-component `source` + `collection_status`. Parse **lockfiles** (package-lock.json, poetry.lock, Podfile.lock) for the full transitive tree, not just top-level. Join each component to running processes / open ports for a `reachable` boolean.
- **Detection:** component→version → NVD/OSV lookup; `composite = w1·CVSS + w2·EPSS + w3·KEV + w4·reachable + w5·asset_tier`; KEV∩reachable ⇒ "same-day". Name-match against typosquat / known-malicious lists; flag any package declaring `preinstall/postinstall` lifecycle scripts (Shai-Hulud vector⁶).
- **Evasion:** install via `curl|bash` (no manifest) → covered by Binaries/Processes; vendored deps with no manifest → file-hash match against a component-hash DB; malicious transitive dep under a benign top-level → requires lockfile parse.
**7.2 Node / Python / Homebrew package collectors — BUG / NOT AS EXP.**
- **Gap:** npm+bun `ok:false ValueError` → empty; Python same swallow; Homebrew returns no data.
- **Root cause:** (npm/bun) exception during output parse, caught and coerced to `[]`. (Homebrew) prefix/arch mismatch — Apple-silicon prefix is `/opt/homebrew`, collector likely assumes `/usr/local` or calls `brew` without the user's PATH/HOME.
- **Enhancement:** Wrap every parser in try/except that preserves raw output + exit code and sets `ok:false` with a message — never empty-coerce. Invoke with explicit env (`HOME`, `PATH`). Resolve brew via `brew --prefix` / `HOMEBREW_PREFIX`. Prefer machine-readable modes (`npm ls -g --json`, `pip list --format=json`, `brew info --json=v2 --installed`) and separate stderr from stdout.
- **Detection:** npm/pip typosquats + install-scripts + Bun-runtime spawned by npm (evasion signal⁶); Python `.pth`/`sitecustomize.py` with `import os/subprocess`; Homebrew unofficial taps, non-standard bottle URLs.
- **Evasion:** parser DoS via crafted package name; a manager legitimately having 0 packages must be distinguishable from a parse error (the core fix).
**7.3 SBOM — RETEST**
- **Gap:** Built on the broken package inventory → incomplete; no build-event correlation.
- **Enhancement:** Assemble from lockfiles + installed set, hash each component, record provenance and first-seen. Correlate a component's appearance with a build/CI event (±1h window).
- **Detection:** component in the running artifact with no correlating build event ⇒ **SBOM drift** (T1195/T1554); dependency-confusion (internal package name resolving to a public registry version).
- **Evasion:** vendored/copied source with no manifest → file-hash matching; post-build tamper that also forges a build event.
**7.10 Binaries — RETEST**
- **Gap:** Confirm hash + signing captured, not just path.
- **Enhancement:** For each Mach-O in exec paths: `sha256`, codesign status + Team ID (`codesign -dv`), notarization (`spctl -a -vv`), quarantine xattr, and fleet-rarity of the path/hash.
- **Detection:** unsigned / ad-hoc-signed binary in `/usr/local/bin` or `~`; quarantine xattr cleared (`xattr -c`) post-download; sha256 ∈ threat-intel (MalwareBazaar / VT≥5); same rare hash on N hosts ⇒ supply-chain lead (fleet correlator).
- **Evasion:** stolen valid Developer ID; LOLBins (signed Apple binaries used maliciously) → needs behavioral, not signing alone.
### 7B · Content-scanning collectors
 
**7.5 Configs — RETEST**
- **Gap:** Reads files fully but evaluates none — missed the `/etc/hosts` redirect.
- **Enhancement:** Ship a per-file known-good baseline (default macOS content); diff every cycle; parse security-relevant directives rather than storing blobs. Resolve include directives (`Include /etc/ssh/sshd_config.d/*`) before evaluating.
- **Detection:** hosts entries → public IPs / suspicious TLDs; sshd `PermitRootLogin yes`, `PasswordAuthentication yes`; sudoers `NOPASSWD` / `!log_allowed`; PAM edits; a config that sources itself.
- **Evasion:** payload hidden behind an `Include`/drop-in dir; comment-obfuscation; trailing-whitespace / homoglyph hostnames.
**7.6 Shell Startup — RETEST**
- **Gap:** Inventoried the file, missed the plaintext `API_KEY` and the self-source line.
- **Enhancement:** Content-scan the full set — `~/.zshrc .zprofile .bashrc .bash_profile .profile` and system-wide `/etc/zshrc /etc/profile`. Follow `source`/`.` targets one hop to catch payload-by-indirection.
- **Detection:** secret regexes (`AKIA[0-9A-Z]{16}`, `ghp_[A-Za-z0-9]{36}`, `sk-[A-Za-z0-9]{20,}`, generic `(API_KEY|TOKEN|SECRET)=` with Shannon-entropy > threshold); `eval $(curl…)`, `base64 -d|sh`; sudo/ssh function-hijack; hidden-below-the-fold payload (≥N blank lines then code). Redact matched secret in evidence.
- **Evasion:** payload sourced from a non-startup file; secret assembled from concatenated vars; unicode/zero-width obfuscation.
**7.15 Dev Security — RETEST**
- **Gap:** Repo-secret path unverified; likely inventories repos without scanning content.
- **Enhancement:** For each git repo under `$HOME` (bounded depth): scan tracked + untracked files for secrets, detect `.env` that is git-tracked, and read insecure git config (`http.sslVerify=false`, credential.helper storing plaintext). Share the secret-regex engine with Shell-Startup (7.6).
- **Detection:** committed secret (AKIA/ghp_/sk-…); tracked `.env`; `sslVerify=false`; unencrypted private key inside a project.
- **Evasion:** secret only in git history (not HEAD) → needs a shallow history scan; secret in an ignored file read at runtime.
### 7C · Persistence & scheduling
 
**7.11 Services — RETEST**
- **Gap:** Lab agent surfaced only after an explicit `launchctl load` + cycle; no signing / drift baseline.
- **Enhancement:** Per service capture label, program path, code-signature + Team ID, scope (system vs user LaunchAgents), `RunAtLoad/KeepAlive`; diff vs a fleet baseline; shorten the service-collector cadence or hook `launchd` state changes.
- **Detection:** unsigned / non-Apple daemon in system scope; service seen on <X% of fleet (rarity); label impersonating `com.apple.*` with a wrong/absent Team ID.
- **Evasion:** install under user LaunchAgents (lower scrutiny); benign-looking vendor label with a valid third-party signature.
**7.12 Tasks — RETEST**
- **Gap:** `last_run/next_run` null on all 18; `Weekday`/`WeekDay` key-case parsing bug.
- **Enhancement:** Pull execution metadata from `launchctl print system/<label>` (last exit, next fire); parse schedule keys case-insensitively; unify calendar vs `StartInterval` schedules into one normalized model.
- **Detection:** schedule command containing `curl|base64|/dev/tcp|osascript`; job that writes into LaunchAgents; inventory of root-run third-party updaters for context.
- **Evasion:** benign command that later fetches; very long `StartInterval`; task delegating to a helper script.
**7.13 Cron Jobs — NOT AS EXP.**
- **Gap:** Updated crontab not reflected on the dashboard.
- **Root cause:** Snapshot cadence/caching, or only root's crontab read (not per-user or `/etc/cron.d`).
- **Enhancement:** Enumerate per-user crontabs (`crontab -l -u <user>`), `/etc/crontab`, `/etc/cron.d`, periodic dirs; hash + diff each cycle; attribute the writing process via file-write on the crontab.
- **Detection:** network-fetch / encoded / reverse-shell command patterns; new job absent from baseline.
- **Evasion:** use `at` or a launchd timer instead of cron; obfuscated command body.
**7.14 Git — RETEST**
- **Gap:** Hook-poison detection unverified.
- **Enhancement:** Enumerate `.git/hooks/*` across known repos plus global `core.hooksPath` and `init.templateDir`; hash hook bodies; allowlist husky/lefthook managed dirs so only the poisoned hook fires.
- **Detection:** hook body with exec primitives / `curl|sh`; `core.hooksPath` redirected to a user-writable dir (fires on next pull/commit).
- **Evasion:** payload placed inside an allowlisted husky path; hook that shells out to a benign-named script.
### 7D · Behavioral / event-window collectors
 
**7.7 Processes — NOT AS EXP.**
- **Gap:** New process + exact parent lineage slow / inconsistent to reach dashboard.
- **Root cause:** Snapshot cadence with no event stream — short-lived procs and precise exec ordering are missed.
- **Enhancement:** Interim: reconstruct lineage from PPID + macOS `responsible pid` at snapshot. Target: subscribe to EndpointSecurity `ES_EVENT_TYPE_NOTIFY_EXEC` for exact parent→child, argv, cwd, and signing at exec time.
- **Detection:** office/browser → shell/interpreter lineage; interpreter spawning a network tool within N s; unsigned exec from a world-writable path.
- **Evasion:** argv[0] renaming / process hollowing; fork without exec; procs that live entirely between snapshots (the reason to move to ES).
**7.8 Connections — NOT AS EXP.**
- **Gap:** Short-lived egress capture inconsistent (verified: a fast `SYN_SENT` to TEST-NET was only visible mid-loop).
- **Enhancement:** NetworkExtension / ES flow events or higher-frequency `nettop` sampling with aggregation; retain per-flow 5-tuple + owning PID + bytes + duration + first/last seen.
- **Detection:** beaconing = regular interval + low jitter + small payload (periodicity/entropy scoring); egress to IOC / newly-registered-domain / fleet-rare destination; DNS to DGA-like domains.
- **Evasion:** low-and-slow beacons under the sampling window; domain fronting; egress via an allowlisted CDN → needs JA3/SNI (roadmap).
**7.9 Open Files & Credential Locations — NOT AS EXP. / RETEST**
- **Gap:** Fast open→read→close bursts (the exact infostealer pattern) inconsistently captured; staging→exfil correlation unconfirmed.
- **Enhancement:** Subscribe to ES `ES_EVENT_TYPE_NOTIFY_OPEN` filtered to a sensitive-path watchlist (`~/.ssh`, `~/.aws`, Keychain DBs, browser Cookies/Login Data, gcloud, VPN profiles); count per-PID in a sliding 120s window; then correlate with Connections for the upload leg.
- **Detection:** ≥4 sensitive files by one PID / 120s = staging (OF-0002); L4 chain `burst read → archive(zip/tar) → egress` = AMOS/Poseidon infostealer kill-chain.²
- **Evasion:** staggered reads beyond the window; access via a signed helper / legitimate browser process; `mmap` instead of `read()`; direct Keychain API vs file read.
### 7E · AI / agentic surface
 
**7.16 AI / Agent CLI & AI Applications — RETEST / NOT AS EXP.**
- **Gap:** CLI-tool scan limited to known dev roots (a repo in `~/hostilerepo` may not be scanned); AI-Applications keys on named inference binaries, so a generic `0.0.0.0:11434` listener is missed.
- **Enhancement:** (CLI) broaden to any git repo under `$HOME` (bounded depth) and watch the full instruction-file set: `CLAUDE.md, AGENTS.md, .cursorrules, .clinerules, .github/copilot-instructions.md`, skill `SKILL.md`; normalize unicode + strip zero-width before matching. (Apps) classify by **bind + auth state** on inference/dev ports, independent of binary name; add a pickle-opcode scan (`GLOBAL os/subprocess`, `REDUCE`) for model artifacts.
- **Detection:** "ignore previous instructions", read `~/.aws|.ssh|.env` + exfil URL, hidden `<IMPORTANT>`/zero-width; coding agent launched with `--dangerously-skip-permissions`/`--yolo`; agent → credential/egress tool within 60s;¹,³ any model server on `0.0.0.0` with auth=false;⁴ pickle model outside allowlisted registries.⁹
- **Evasion:** homoglyph / zero-width injection; instruction split across files; base64-encoded directive; inference server behind a reverse proxy on a non-default port.
---
 
## 8 · Cross-cutting principle
 
The dominant theme is **"collected" ≠ "evaluated."** Most flagged collectors read the right data (sysctl, hosts, startup files, tasks, repos) but return `suspicious:false` or a bare count without applying detection logic — and the package layer additionally **hides failures as empty**. Two engineering thrusts resolve the majority of findings: (1) make failure states honest — never a silent zero; (2) push content-level and event-stream detection into collectors that currently only inventory. Both align with the platform's own principle of separating "couldn't evaluate" from "found nothing."
 
---
 
## References
 
1. Invariant Labs, "MCP Security Notification: Tool Poisoning Attacks" (2025); CSA Research Note, "MCP Tool Poisoning" — rug-pull / post-approval mutation, >60% success across 45+ servers; CVE-2025-54136 (CVSS 8.8).
2. Sophos, "Why AMOS matters" (2026); Microsoft, "Infostealers without borders: macOS…" (Feb 2026) — Keychain/browser/credential staging, T1555/T1560/T1041.
3. Trend Micro / TrendAI, "Malicious skills used to distribute Atomic macOS Stealer" (2026) — injection hidden in agent skill/instruction files.
4. SentinelLABS + Censys (Jan 2026) — 175,000 exposed Ollama hosts, ~23k persistent; Cisco Talos / Shodan (Sep 2025) — 1,100+ exposed, ~20% unauthenticated on port 11434.
5. Homebrew trojanized-formula distribution noted in AMOS campaign analyses (2025).
6. Zscaler / Datadog / Wiz / CISA (Sep–Nov 2025) — Shai-Hulud & 2.0 npm worm: 700–800+ packages, preinstall execution, Bun-runtime evasion, dead-man switch.
7. Microsoft, "Mini Shai-Hulud: compromised @antv npm packages enable CI/CD credential theft" (May 2026).
8. Jacobs, Romanosky, Edwards, Roytman, Adjerid, "Exploit Prediction Scoring System (EPSS)," DTRAP 2(3), 2021 (ROC-AUC 0.838); FIRST EPSS.
9. JFrog (2024) — ~100 malicious pickle-format models on Hugging Face; `__reduce__` RCE at `torch.load()`; mitigation = safetensors + `weights_only=True`.
---
 
*AttackLens · Collector Validation & Detection-Engineering Report · rev 2 · 2026-09-23 · claims limited to observed lab behavior; threat context cited from public 2025–2026 research.*