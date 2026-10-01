# P0-3 · Installing the Vedha agent in a client environment — approach

Date: 2026-10-01 · Status: **approach for review — nothing implemented yet**
Roadmap item: P0-3 in [`2026-09-29-next-8-workstreams-plan.md`](2026-09-29-next-8-workstreams-plan.md)

## 1. Summary

The agent itself is mature: outbound-only, device identity, enrolment with approval, scope
enforcement, proxy support, `doctor` checks, Docker / systemd / launchd / Windows paths. **What is
broken is getting it onto a customer's machine.** The Fleet page tells customers to download from
`https://downloads.vedha.example/…`, a placeholder that doesn't exist, and nothing serves the agent
image. A customer following the product's own instructions cannot install the agent today.

Recommended approach, in one line: **the manager (`api.vedhasec.com`) distributes a signed agent
image and installer; the customer clicks "Add agent" in the portal, copies one command containing a
single-use enrolment token, runs it on a Linux VM, and watches the agent come online.** A
pre-built virtual appliance follows for customers who can't run Docker.

## 2. What exists today (verified on `origin/main` b6a3b60)

| Piece | State | Where |
|---|---|---|
| Docker installer (`--docker --manager … [--enroll-token vet_…]`) with self-heal, non-root container, state volume, uninstall | Works, **if the image is already on the host** | `probe/install.sh` |
| Native paths: systemd, launchd, Windows scheduled task, foreground | Work (Python on the host) | `probe/install.sh connect`, `probe/windows/` |
| Device-code enrolment, approve/activate, pre-authorised enrol tokens (`vet_…`), portal approval | Backend done; portal can approve a code | `routers/probe_enrollment.py`, `portal.py` `/workspace/fleet/enrollment/approve` |
| Sealed (native-binary) agent + licence + host binding | Builds, passes parity + bypass checks | `probe/Dockerfile.sealed`, `seal-probe.sh` |
| `doctor` (DNS → TCP → TLS → cert chain, clock), `self_scan`, `explain_plan` | Works | `agent.setup` |
| Proxy (`HTTPS_PROXY`), private CA (`PROBE_CA_BUNDLE`), WebSocket → long-poll fallback | Works | agent transport |
| Docs: install guide (3 OSes), client prerequisites, network requirements, troubleshooting | Thorough but operator-oriented and scattered | `docs/probe/`, `docs/deployment/`, `probe/*.md` |

## 3. Gaps found (the reasons customers can't install today)

| # | Gap | Evidence | Impact |
|---|---|---|---|
| G1 | **No image distribution.** Installer defaults to `vedha-agent:local`, which only exists where it was built. No registry, no CI publishing, no hosted tar. | `install.sh:206`; no publish step in `.github/workflows/` | **Blocker** |
| G2 | **Fleet install command points at a fake domain** (`downloads.vedha.example`). Manager doesn't serve `install.sh`. | `fleet/page.tsx:169` | **Blocker** |
| G3 | **No UI to mint enrol tokens** (`vet_…`); only an API. Without one, every install needs a code read out and approved by hand. | no frontend references to `enroll-tokens` | High friction |
| G4 | **Sealed image can't use the installer:** it computes the hardware ID with `--entrypoint python`, and the sealed image has no Python. | `install.sh` hw-id block | Blocks shipping sealed agents |
| G5 | **Hardware binding needs `--mac-address`**, which rootless Docker, Docker Desktop and Podman reject. | `install.sh` error path | Fails on common hosts (RHEL ships Podman) |
| G6 | **Single architecture**: images built on whatever machine runs `make`; ARM hosts (Graviton, Raspberry Pi, Apple) get emulation or failure. | no buildx/multi-arch | Medium |
| G7 | **No integrity check by default**: `PROBE_IMAGE_SHA256` is optional; no signature. A tampered image would run with scan rights inside the customer network. | `install.sh` load path | Security |
| G8 | **No customer-facing package**: docs assume repo access, `make probe-pat`, and operator knowledge. | `docs/probe/AGENT_INSTALL_GUIDE.md` §2 | Support load |
| G9 | **No support bundle / version visibility / upgrade path** for remote troubleshooting. | — | Support load |

## 4. How comparable products do it (research)

| Vendor | Form factor in the customer network | How it links | Network |
|---|---|---|---|
| **Qualys** Virtual Scanner Appliance | OVA / VHDX / cloud image; power on, enter a **14-digit personalization code** in the template or console | Code from the Qualys UI → appliance activates and appears as "Connected" | Outbound 443 only; HTTP proxy configurable at deploy time |
| **Tenable** Agent / sensor | Native `.deb` / `.rpm` / `.msi` | `nessuscli agent link --key=<linking key> --host --port [--groups]`; retries hourly if offline | Outbound 443 to `sensor.cloud.tenable.com` |
| **Rapid7** InsightVM Scan Engine | Installer on Linux/Windows | **Pairing** engine ↔ console with a shared secret; engine-to-console or console-to-engine direction | Engine → console; updates from `updates.rapid7.com:443` |

Sources: [Qualys VMware deploy](https://success.qualys.com/discussions/s/article/000006011) ·
[Qualys Hyper-V](https://docs.qualys.com/en/scanner/hyper-v/microsoft/get_started.htm) ·
[Tenable Linux agent](https://docs.tenable.com/agent/Content/InstallNessusAgentLinux.htm) ·
[Rapid7 distributed engines](https://docs.rapid7.com/insightvm/configuring-distributed-scan-engines/) ·
[Cosign keyless signing in GitHub Actions](https://www.qcecuring.com/blog/sigstore-cosign-keyless-github-actions) ·
[Signing multi-arch images](https://some-natalie.dev/blog/sigstore-multiarch/)

**Patterns every one of them uses — and what Vedha should copy:**
1. **One short secret pasted once** (linking key / personalization code / pairing secret). Vedha has
   this already (`vet_` tokens, device codes) but no UI to create them.
2. **Outbound 443 to one vendor host.** Vedha matches this. Pulling images from a third-party registry
   (ghcr.io, Docker Hub) would add more egress rules, so **the manager should serve the image itself**.
3. **Two form factors:** a package for teams with Linux skills and a **virtual appliance** for teams
   without (Qualys's main path). Docker is the package equivalent for Vedha; the appliance comes next.
4. **Proxy set at install time**, not discovered later.
5. **Retry forever on link failure**, then show "Connected" in the console. Vedha self-heals, but the
   customer currently can't see install progress in the portal.

## 5. Points of failure (what goes wrong in real client networks) and the mitigation

| # | Failure | How it shows up | Mitigation in this plan |
|---|---|---|---|
| F1 | Egress only through a proxy | install can't download / agent can't connect | `--proxy` flag at install, written into the agent config; `doctor` tests through it |
| F2 | **TLS inspection** (Zscaler, Palo Alto, Fortinet) re-signs HTTPS | `unable to get local issuer certificate` | `doctor` detects a non-Let's-Encrypt issuer and says so; `--ca-bundle` flag; docs ask IT to exempt `api.vedhasec.com` from inspection (preferred) |
| F3 | Proxy doesn't carry WebSockets | connects, then drops / slow jobs | automatic fallback to HTTPS long-poll (exists); surface "degraded: long-poll" in Fleet |
| F4 | Image pulled from a registry blocked by egress policy | `docker pull` fails | manager serves the image: no second egress rule |
| F5 | **Docker not allowed / not installed / Podman** (RHEL 8/9 default) | installer stops | preflight names it; Podman support; virtual appliance for no-Docker sites |
| F6 | Rootless Docker / Docker Desktop / Podman reject `--mac-address` | hardware-ID error | MAC-independent identity (device key already is the identity; licence binds to the state volume + host fingerprint without a forced MAC) |
| F7 | ARM host | emulation or crash | multi-arch image (amd64 + arm64) |
| F8 | Wrong placement: VLAN, client isolation, NAT, Docker bridge | agent online but targets "down" | Fleet "reachability test" against one in-scope IP before the first scan; docs: same segment as targets |
| F9 | Clock skew | TLS / token errors | `doctor` clock check (exists); install refuses if skew > 5 min, with the fix |
| F10 | Internal DNS can't resolve `api.vedhasec.com` / split horizon | DNS failure | preflight resolves and prints which resolver answered |
| F11 | EDR / IDS / IPS block or alert on scan traffic | scans incomplete, SOC tickets | client checklist: allow-list probe IP; Stealth preset for monitored segments; advance notice template for the SOC |
| F12 | VM cloned or migrated | duplicate agents / WebSocket 403 loop | one-identity-per-host check; Fleet shows duplicates; documented re-enrol |
| F13 | Enrol token leaks via shell history / screenshots | someone else enrols an agent | token is single-use, expires in 24 h, bound to one engagement and its scope; enrolment audited; revocable |
| F14 | Tampered installer or image (`curl … | sh`) | malicious code with scan rights | HTTPS from the manager, versioned installer, SHA-256 + signature verified before load; inspect-first command offered |
| F15 | Agent version drift after manager upgrades | features missing / incompatible | agent reports its version; manager shows "update available" and the one update command |
| F16 | "It's online but no jobs" (empty scope) | idle agent | scope comes from the engagement automatically when enrolled via its token (no `PROBE_NETWORK_SEGMENTS` needed) |
| F17 | Hard to debug remotely | long email threads | `support-bundle` command: redacted logs + doctor output, uploaded to the manager with one consent prompt |

## 6. Recommended approach

### 6.1 Primary path — Docker on a customer Linux VM (Phase 1)

**Customer experience (target: under 10 minutes, no Vedha engineer needed):**

1. Portal → **Fleet → Add agent**. A short wizard shows the requirements (Linux VM, 2 vCPU / 4 GB /
   20 GB, Docker or Podman, outbound 443 to `api.vedhasec.com`), asks for an optional agent name and
   proxy, and generates:
   ```bash
   curl -fsSL https://api.vedhasec.com/agent/install.sh | sudo sh -s -- --token vet_XXXX
   ```
   plus an inspect-first variant (download, view, run).
2. Customer runs it. The installer:
   - **Preflight** (each failure prints the exact fix): OS/arch, Docker/Podman, disk/RAM, clock, DNS,
     TCP 443, TLS chain (detects inspection), proxy.
   - Downloads the image for the host's architecture **from the manager**, verifies SHA-256 and the
     vendor signature, loads it.
   - Starts the hardened container (non-root, read-only, no inbound ports) and enrols with the token.
3. The portal wizard **updates live**: Waiting → Connected → Scope received → Reachability test
   passed → Ready. If nothing arrives in 5 minutes it shows the likely causes from §5.

**Building blocks:**

| Block | Description |
|---|---|
| Release pipeline | GitHub Actions on tag: build **multi-arch** (amd64, arm64) agent image, run seal-parity, sign, publish artifacts to the manager's distribution store (S3 or the manager volume) with a manifest: version, digest per arch, SHA-256, signature |
| Distribution endpoints on the manager | `GET /agent/install.sh` (public, versioned) · `GET /agent/manifest.json` · `GET /agent/image/{version}/{arch}` — **image downloads require a valid enrol token or agent credential** (keeps the agent binary away from the public internet) |
| Signing | Reuse the existing vendor Ed25519 key (already used for licences): sign the manifest; the installer embeds the public key. (Alternative: cosign keyless via GitHub OIDC — better if images move to a registry later.) |
| Enrol tokens in the UI | Operator Fleet and portal Fleet can mint **single-use, 24 h, engagement-bound** tokens; list, revoke, audit |
| Installer changes | default image source = manager; mandatory checksum + signature; `--token`, `--proxy`, `--ca-bundle`, `--name`; Podman support; MAC-independent identity; sealed-image-compatible hardware ID (`vedha-agent hwid` subcommand instead of `--entrypoint python`) |
| Fleet onboarding status | per-token state machine shown in the wizard; reachability test against one in-scope IP |

### 6.2 Secondary path — virtual appliance (Phase 3)

For customers who won't run Docker or don't have Linux skills, the Qualys model:

- OVA (VMware), VHDX (Hyper-V), AMI / Azure image: minimal hardened Ubuntu + Docker + agent.
- First boot: console wizard asks for the **enrol token**, proxy and (optional) static IP — same token
  as §6.1, so the portal flow is identical.
- Read-only root, automatic security updates, no SSH by default (console only).

### 6.3 Kept as supported, not primary

- Native systemd / launchd: for hosts where containers are forbidden; same token, same manifest.
- Windows: connect-scan only, Defender exclusions needed. Recommend the appliance on Hyper-V instead.

## 7. Phases, priority and effort

| Phase | Scope | Unblocks | Effort |
|---|---|---|---|
| **1 — Installable** | release pipeline (multi-arch, signed) · manager distribution endpoints · installer: manager source, verification, preflight, `--token/--proxy/--ca-bundle`, Podman, MAC-independent identity, sealed-compatible hw-id · enrol-token UI (operator + portal) · real install command in Fleet · onboarding status in the wizard | **Every new customer** | ~5–7 days |
| **2 — Supportable** | client package: 1-page requirements, install guide with screenshots, security FAQ, SOC notice template · `support-bundle` · agent version + "update available" + upgrade command · uninstall/offboard (revoke + purge) · duplicate-agent detection | Lower support load, enterprise security reviews | ~4–5 days |
| **3 — No-Docker sites** | virtual appliance (OVA/VHDX/AMI) with first-boot wizard · optional signed auto-update | Customers without Linux/Docker | ~5–8 days |

Testing for each phase: installer runs in CI on Ubuntu 22.04/24.04, Debian 12, RHEL 9 (Podman),
Amazon Linux 2023, on amd64 and arm64; network fault injection (proxy, blocked 443, TLS
interception with a test CA, clock skew); one real end-to-end install against `api.vedhasec.com`.

## 8. Decisions needed from you before implementation

1. **Image hosting:** served by the manager, gated by token (recommended: one egress rule, agent not
   public) — or a container registry (GHCR / ECR: simpler pipeline, but extra egress rules and a
   public or per-customer-authenticated image)?
2. **Image type for customers:** sealed native binary (recommended, protects the code; passes parity)
   or plaintext Python image for now?
3. **Default enrolment:** single-use token in the command (recommended: one step, like Tenable) or
   device-code approval (customer reads a code and approves it in the portal; more steps, nothing
   secret in the command)? Both stay supported; this picks the default in the wizard.
4. **Podman support in Phase 1** (needed for RHEL customers), or Docker-only first?
5. **Virtual appliance:** Phase 3 as proposed, or sooner if your first customers are Windows/VMware shops?
6. **Signing method:** existing Ed25519 vendor key (recommended now) or cosign keyless?

## 9. Deeper research (2026-10-02): 19 more field failure points and 5 privacy ones

Method: vendor knowledge bases (Palo Alto, Cisco, Tenable, AWS, Docker), field reports, then each
point checked against Vedha's code. **Verified** = confirmed in the code or by a lookup;
**research** = documented elsewhere, not yet reproduced with Vedha; **to confirm** = the source
lookup was rate-limited, so treat it as likely rather than certain.

### 9.1 New field failure points

| # | Failure | Basis | Symptom | Mitigation |
|---|---|---|---|---|
| F18 | **`vedhasec.com` is a newly registered domain** (created 2026-09-28). Palo Alto blocks "Newly Registered Domains" (< 32 days) by recommended default; Umbrella, Zscaler and Fortinet have similar categories | **Verified** (whois) + [Palo Alto URL categories](https://docs.paloaltonetworks.com/advanced-url-filtering/administration/url-filtering-basics/url-categories) | Agent can't reach the manager even with 443 open; installer download blocked | **Now:** submit `vedhasec.com` for categorisation (Palo Alto Test-A-Site, Zscaler, Fortinet, Cisco Talos, Broadcom, Check Point). Client checklist: allow-list `api.vedhasec.com`. Pre-flight recognises a filter block page or proxy-issued certificate |
| F19 | **Proxy settings don't reach the agent container**: the installer's env file has no `HTTPS_PROXY` / `NO_PROXY` | **Verified** (`install.sh` `write_env_file`) | Host curl works, agent can't connect | Pass proxy variables into the env file; `--proxy` flag |
| F20 | **Authenticating proxies** (NTLM / Kerberos) | to confirm (httpx supports Basic proxy auth only) | 407 Proxy Authentication Required | IP-based proxy exemption for the agent VM; Basic credentials; state it in the requirements |
| F21 | **Agent container logs unbounded** (no `--log-opt`) | **Verified** (`docker run` flags) | Customer VM disk fills over months | `--log-opt max-size=10m --log-opt max-file=5` |
| F22 | **Docker not enabled at boot** | **Verified** (no `systemctl enable docker`) | Agent offline after the VM reboots | Installer enables Docker; pre-flight warns |
| F23 | **No ICMP host discovery**: the container has no `NET_RAW` | **Verified** (`--cap-drop ALL`) | Hosts that only answer ping look "down" | Optional `NET_RAW`; explain it in the reachability test |
| F24 | **Container DNS differs from the host** (split DNS, VPN-only resolvers, systemd-resolved stub) | research | Name resolution fails inside the container only | Pre-flight resolves from inside the container; `--dns` passthrough |
| F25 | **MTU black hole** on VPN / IPsec / GRE paths | research ([Server Fault](https://serverfault.com/questions/1170054/why-does-an-ssl-handshake-fail-due-to-small-mtu)) | TLS handshake hangs with no error | Timed handshake in pre-flight; document MSS clamping |
| F26 | **End-of-life host OS** (CentOS 7, RHEL 7): old Docker, old CA store | research | Installer download or Docker features fail | Supported-OS list; pre-flight refuses EOL with the reason |
| F27 | **SELinux enforcing** with bind mounts (e.g. a CA bundle) | research ([GitHub](https://github.com/letsencrypt/boulder/issues/4165)) | Permission denied inside the container | `:z` on bind mounts; named volumes for state (already) |
| F28 | **firewalld reload removes Docker's rules** (RHEL family) | research | Agent loses network after a firewall change | Document; pre-flight detects firewalld; recommend Docker's firewalld zone |
| F29 | **Docker Desktop** on customer machines: paid licence for companies > 250 staff or > $10M revenue, and its NAT hides the LAN | research ([Docker licence](https://docs.docker.com/subscription-billing/desktop-license/)) | Licence exposure; scans can't see targets | Supported only: Docker Engine / Podman on Linux, or the appliance |
| F30 | **IPS / NAC reacts to the scan**: port-scan detection shuns the agent IP; NAC (e.g. Cisco ISE) quarantines its switch port | research ([Cisco port scan detection](https://secure.cisco.com/secure-firewall/docs/port-scan-detection)) | Mid-scan, everything turns "filtered"; agent goes offline | Allow-list the agent IP in IPS/NAC; detect a sudden all-filtered pattern, stop and alert |
| F31 | **Fragile devices and stateful firewalls**: printers, OT/PLCs and old embedded devices crash; scanning *through* a firewall exhausts its session table | research ([Tenable fragile devices](https://docs.tenable.com/cyber-exposure-studies/ransomware/Content/AvoidScanningFragileDevices.htm)) | Device or network outage blamed on Vedha | Fragile-asset guard (exists); agent on the same segment as targets; Stealth for sensitive segments; OT passive only |
| F32 | **Agent VM changes IP** (DHCP) | research | IPS/NAC allow-lists stop matching, which leads to F30 | Require a static IP or DHCP reservation |
| F33 | **EDR / antivirus flags the agent**: scanners and Nuitka-packed binaries are often flagged heuristically | research | Agent quarantined or blocked | Code-sign releases; publish hashes for allow-listing; submit to AV vendors |
| F34 | **Change windows and time zones**: scans run outside an approved window | research | Change-ticket violations, SOC escalations | Scan windows per engagement, in the customer's time zone |
| F35 | **NTP blocked** (UDP 123), the usual root cause of clock skew (F9) | research | TLS and token errors after days of drift | Pre-flight checks time sync; document NTP egress |
| F36 | Idle timeouts on long-lived connections (AWS NAT / NLB: fixed 350 s) | research ([AWS](https://aws.amazon.com/blogs/networking-and-content-delivery/implementing-long-running-tcp-connections-within-vpc-networking/)) | Silent disconnects | **Already handled**: WebSocket ping every 30 s (`transport.py`) |

### 9.2 New privacy failure points

| # | Failure | Basis | Mitigation |
|---|---|---|---|
| P11 | **Certificate Transparency leaks customer names** if each customer gets its own subdomain (`<slug>.portal.vedhasec.com` is planned) | **Verified** plan in `customer_access.py`; [CT subdomain discovery](https://inventivehq.com/blog/subdomain-discovery-using-certificate-transparency-logs) | Wildcard certificate (DNS challenge) or path-based tenancy; never put customer names in public certificates |
| P12 | **AI providers keep prompts for a period** (abuse monitoring) unless zero-data-retention terms apply | to confirm | Record each provider's retention in the sub-processor list; seek zero-retention terms; masked identifiers by default |
| P13 | **Support bundles and logs** sent to Vedha contain IPs and hostnames | research | Redaction (exists) plus explicit consent; store in India; delete after the ticket closes |
| P14 | **The agent is a pivot** if the manager is compromised: it can be tasked inside the customer network | research | Agent-side scope enforcement (exists); signed job policy (key exists); a customer-visible switch to stop the agent; alert on scope changes |
| P15 | **Prompt injection through scan data**: banners and hostnames are attacker-controlled and flow into AI prompts | research | Treat scan data as untrusted in prompts; masking; label AI output as unverified (already in the portal) |
