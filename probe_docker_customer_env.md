# Vedha Probe — Customer-Environment Distribution Design Dossier

> **What this is.** An expert design thread on turning the Vedha probe into a
> hosted, one-command install for customer environments
> (`curl … | sudo sh -s -- --manager …`). Captured as three parts:
> **(1)** the hosting/serving architecture, **(2)** the failure-mode &
> improvement analysis, **(3)** the non-disruptive implementation approach +
> step-by-step plan.
>
> **Repo state when written:** `main` branch, working tree dirty (graphify
> output + in-flight `manager/` and `probe/` code changes). All file:line
> references below point at the probe/manager code as read during this analysis.
> **No code was changed** producing this dossier — it is analysis + plan only.

---

## Part 1 — How to host / serve the probe as a one-command install

**Prompt:**
> help me to understand how i can host vedha-agent or serve to client so that
> only one command with them can [download], install dependencies automatically
> and start vedha-agent like —
> `curl --proto '=https' --tlsv1.2 -fsS https://downloads.vedha.example/probe/install.sh | sudo sh -s -- --manager http://13.127.147.205`
> …just think deeper as expert and help me with that first. Don't implement in code.

### Bottom line up front

`probe/install.sh` today is an **in-repo installer**, not a **remote bootstrap
installer**. It assumes the probe source tree (or a Docker image) is already on
disk next to it. The `curl … | sudo sh` one-liner needs three things it doesn't
have yet:

1. **A hosting origin** (`downloads.vedha.example`) that serves the script *and*
   a payload over TLS.
2. **A self-contained payload** the script can fetch — because when piped through
   `sh`, there is no source tree, no `probe.env`, no `requirements-runtime.txt`,
   no `agent/` package on the client.
3. **A bootstrap layer** that detects OS/arch, downloads + verifies the payload,
   and installs it as a *service* that survives reboots.

The biggest question isn't the shell plumbing — it's **what you serve**.
`probe/SEALING.md` already answers it: ship the **sealed native binary**, never
raw `.py`. That constraint drives everything.

### Why the exact command fails today

- `curl … | sudo sh -s -- --manager http://13.127.147.205` → piped via stdin, so
  `$0` is `sh`, and the first arg `--manager` matches `--*` → the script picks
  **DOCKER mode** (`install.sh:34`).
- DOCKER mode needs Docker (clear preflight failure if absent, `install.sh:266`)
  **and an image**. Default is `IMAGE=vedha-agent:local` (`install.sh:182`) — a
  *local* tag that can't be pulled. It dies at `docker pull vedha-agent:local`
  (`install.sh:322`), or earlier deriving `PROBE_HW_ID`, which itself runs the
  image (`install.sh:361`).
- LOCAL mode wouldn't help either: it does `cd "$(dirname "$0")"` and reads
  `requirements-runtime.txt` + `agent.agent` from disk — none of which exist on a
  freshly-curled client.

**Nothing in the script downloads a payload.** That's the missing half.

### What to serve — three shapes

| Shape | IP-protected? | Client needs | Reuses existing code | Verdict |
|---|---|---|---|---|
| **A. Sealed Docker image** (hosted tar + SHA256) | ✅ Nuitka native, license-gated | Docker | ~all of DOCKER mode already supports `PROBE_IMAGE_TAR_URL` + `PROBE_IMAGE_SHA256` (`install.sh:288–332`) | **Ship this now** |
| **B. Sealed native binary + systemd** | ✅ same seal, no container | nothing (single file) | needs a new Nuitka `--onefile` export + a systemd unit | **Roadmap — best client UX** |
| **C. Python source + venv** (LOCAL mode) | ❌ leaks scanner source | Python 3.8+ | LOCAL mode as-is | PoC / trusted fleets only |

Shape **A** is the fast path: DOCKER mode already knows how to fetch an image tar
from a URL, verify its checksum, hardened-run it with a restart policy, and do
device enrollment. The gap is a thin bootstrap that (a) points
`PROBE_IMAGE_TAR_URL` at your host and (b) optionally installs Docker.

Shape **B** is the cleanest long-term client experience (no Docker dependency,
one file, `systemctl enable --now`) — the rustup/Tailscale/k3s model — but needs
a per-OS/arch build matrix `seal-probe.sh` doesn't emit yet (it only builds the
Docker image today).

**Do not** use Shape C for real clients — `SEALING.md` is explicit that shipping
decryptable `.py` is strictly weaker than what you already have.

### Where to host it

- **Manager-served behind Caddy (recommended to start).** Every probe already
  reaches the manager over 443, and you already run Caddy + Let's Encrypt there.
  Serve `/install.sh` and `/downloads/probe-<ver>-<arch>.tar` from the same
  origin. The one-liner collapses to a single trust anchor:
  ```
  curl --proto '=https' --tlsv1.2 -fsS https://manager.example.com/install.sh \
    | sudo sh -s -- --manager https://manager.example.com --enroll-token vet_…
  ```
  Zero new infra; download host == enrollment host.
- **S3 + CloudFront (`downloads.vedha.example`).** The classic static-CDN pattern
  — decouples downloads from the manager, scales to many tenants, gives the
  vanity domain in the example. Graduate here once you have multiple
  managers/customers.

Start manager-served; migrating to a CDN is just changing a base URL later.

### What the bootstrap actually has to do (8 responsibilities; yours does 3–4)

1. **Detect OS + arch** (`uname -s`/`-m`) → select amd64 **or** arm64 payload.
   (Today the script only *warns* on arch mismatch, `install.sh:342`.)
2. **Fetch over pinned TLS** — `--proto '=https' --tlsv1.2 -fsS` is exactly right.
3. **Verify the payload** against a SHA256 (and ideally an Ed25519/minisign
   signature) **embedded in install.sh itself**. `PROBE_IMAGE_SHA256` exists —
   the hosted script just needs to carry the digest for the version it ships.
4. **Install the runtime** — require Docker with a clear message (current) *or*
   auto-run `get.docker.com` when absent. A real fork (see decisions).
5. **Enroll without a human secret** — pass a site-bound `--enroll-token` so it's
   safe on untrusted client networks, not just single-owner fleets.
6. **Install as a service** — Docker `--restart unless-stopped` (already set,
   `install.sh:577`) survives reboot *if* dockerd is enabled. Shape B needs a
   systemd unit. The LOCAL-mode `while` self-heal loop (`install.sh:144`) is a
   *foreground* supervisor — wrong for an unattended client.
7. **Be idempotent + upgradeable** — re-run fetches a newer tar, `docker load`,
   recreate container preserving the state volume (identity/license live in the
   named volume; the "refuse to move an enrolled identity" guard at
   `install.sh:593` protects this).
8. **Uninstall cleanly** — `--uninstall` / `PROBE_PURGE` already exist
   (`install.sh:220`).

### The enrollment UX that makes it "one command"

The magic in Tailscale/k3s isn't the script — it's that **the dashboard
generates the exact copy-paste line, pre-filled with a freshly-minted,
site-bound enroll token**. The `--enroll-token` path already auto-approves;
what's missing is the **Fleet → Add Probe** screen that mints the token and
renders the one-liner. One line, no secret the customer must understand, safe on
an untrusted LAN because the token is scope-bound and consumed on first boot.

### Decisions needed before building

1. **Payload shape** — sealed Docker image now (fast, reuses code, needs Docker)
   vs. sealed native binary + systemd (best UX, new per-arch pipeline).
   *Recommendation: Docker image now, native binary on the roadmap.*
2. **Hosting origin** — manager-served behind Caddy (recommended) vs. S3+CloudFront now.
3. **Docker on the client** — auto-install via `get.docker.com` when missing
   (hands-off but invasive) vs. require it as a prereq (safer, current behavior).
4. **Enrollment mode** — always mint a site-bound `--enroll-token` from the
   dashboard (safe on untrusted nets) vs. rely on `PROBE_AUTO_ENROLL`
   (single-owner only).

---

## Part 2 — Areas of improvement & failure (all edge factors)

**Prompt:**
> still find the area of improvement and help me understand, considering all edge
> factors and area of failure. Don't change code.

Confirmed facts from the code: the enroll-token mint endpoint **exists**
backend-side (`manager/backend/app/routers/probe_enrollment.py:769` `POST
/enroll-tokens`, plus list/revoke `:817`/`:842`); the sealed image is a side
artifact — production compose builds the *plain* `Dockerfile` (`vedha-agent:local`,
`probe/docker-compose.yml:19`), and `Dockerfile.sealed` is referenced only by
`seal-probe.sh:75`. No manager route serves `/install.sh` or any payload
(`FileResponse`/`StaticFiles`/`downloads` grep → empty).

### Tier 0 — Foundational: the one-liner can't actually ship yet

1. **The IP-protected payload is self-flagged as non-shippable.**
   `Dockerfile.sealed:1-3`: *"non-shipping research artifact… do not treat this
   as a deployment alternative until it passes the same release pipeline and
   runtime-parity tests."* The `SEALING.md` "ship it" story rests on an artifact
   its own author marked unready. Production compose builds the **plain**
   `Dockerfile` instead.

2. **Even if shipped, the sealed image is functionally crippled.**
   `Dockerfile.sealed:29` installs `nuitka httpx cryptography websockets` —
   **missing `impacket`, `ldap3`, `dnspython`**, and `--include-package` (`:75-77`)
   omits them too. `requirements-runtime.txt:9-19` says these are *"NOT optional
   in practice"* — their absence forces `outcome=partial`/`degraded=true` on
   **every** assessment and makes three manager posture rules unreachable
   (SMB-NULL-SESSION, LDAP-ANONYMOUS-BIND, DNS-ZONE-TRANSFER). Sealed and plain
   are **not at runtime parity**.

3. **No hosting origin and no download logic.** Manager serves no `/install.sh`,
   no payload route. `install.sh` never *fetches* the payload except via
   `PROBE_IMAGE_TAR_URL` (set out-of-band), with **no OS/arch detection** to pick
   amd64 vs arm64 — only a post-hoc arch *warning* at `:342`.

### Tier 1 — The two design tensions that will generate outages & tickets

4. **Host-binding is brittle and fights the one-command model.**
   `hw_bind.py:30`: fingerprint = `uuid.getnode() | platform.node() | platform.machine()`.

   | Component | Fails when | Consequence |
   |---|---|---|
   | `uuid.getnode()` (MAC) | can't read a real MAC → Python returns a **random** value; multi-NIC → arbitrary pick; NIC swap / Wi-Fi↔Ethernet / dock / VM migration | fingerprint changes |
   | `platform.node()` (hostname) | DHCP rename, `hostnamectl`, container recreate | fingerprint changes |

   Any change → `check_hw_bind()` raises → **binary refuses to start**: a silent
   outage after routine infra changes. Docker mode stabilizes it by pinning
   `--hostname` + a deterministic `--mac-address` (`install.sh:353-373`) — but
   **only in Docker mode**. A bare native binary (Shape B) is the *most* fragile.

5. **Host-binding breaks the install on the two commonest SMB/dev environments.**
   `install.sh:366-372`: Docker Desktop and rootless Docker **reject
   `--mac-address`**, so HW-ID derivation fails and the install aborts unless the
   user hand-sets `PROBE_MAC_ADDRESS` + `PROBE_HW_ID`. A piped `curl|sh` can't
   prompt for those → hard failure on exactly those machines.

6. **A host-locked *binary* and a generic *one-command image* are mutually
   exclusive.** `Dockerfile.sealed` bakes `HW_BIND_FINGERPRINT` at **build time**,
   per machine; a generic `curl|sh` pulls **one** image for everyone. The only
   coherent model is **floating binary + host-locked license.token** (which
   `SEALING.md`'s run example uses) — which leads to #7.

7. **License delivery is chicken-and-egg — it defeats "one command and it's
   running."** With `LICENSE_ENFORCED=true`, `store_license()`
   (`install.sh:488-510`) **exits** if no license is present. Only you can mint a
   license (vendor private key), host-locked to a HW ID unknown until the probe
   runs once. There is **no "phone home → auto-issue license" path**. So enforced
   install is inherently: *install → read `hostid` → you mint → deliver → start.*
   One `curl|sh` cannot complete it. Choose: ship **unenforced** (no IP gate —
   defeats the point) or accept a **two-step, human-in-the-loop** handshake. The
   deepest unresolved tension.

8. **License expiry has no renewal path.** `issue_license.py … --days 365` → the
   probe silently dies when the license lapses (binary refuses to start), no
   auto-renew or grace. Across a fleet, expiries become a recurring fire drill.

### Tier 2 — Supply-chain & root-execution risk (piping to `sudo sh`)

9. **Payload verification is optional, hash-only, same-channel.**
   `PROBE_IMAGE_SHA256` is checked *only if set* (`install.sh:301`), it's a
   **hash not a signature**, delivered over the same origin as the script — a
   compromised origin rewrites both. Want an out-of-band **signature**
   (cosign/minisign/GPG) with the public key pinned *inside* the installer.

10. **Truncated-download execution hazard.** The classic `curl|sh` footgun: a
    mid-pipe truncation executes a *partial* script. `--proto '=https' --tlsv1.2
    -fsS` authenticates the **transport, not the content or completeness**.
    `install.sh` runs top-to-bottom and is **not** wrapped in a `main() { … };
    main "$@"` guard, so a partial read can execute half an installer.

11. **Cleartext token leak via the copy-paste pattern.** The example targets
    `--manager http://13.127.147.205` — plain HTTP to an IP. `install.sh:485`
    only *warns*; the agent token + results go over the wire in clear text. A
    client installer should **hard-refuse** non-local `http://`, not warn.

### Tier 3 — "Runs, then dies later" — lifecycle-over-time failures

12. **Reboot survival isn't guaranteed.** LOCAL mode's supervisor is a
    **foreground `while` loop** (`install.sh:144`) — dies on SSH disconnect,
    terminal close, or reboot (`TROUBLESHOOTING.md:176` even says "run under a
    supervisor"). Docker's `--restart unless-stopped` (`install.sh:577`) survives
    reboot **only if dockerd auto-starts** — not guaranteed on rootless / Docker
    Desktop. No systemd unit is installed to guarantee either.

13. **Unbounded disk growth — a silent time-bomb.** Result archive:
    `probe.env.example:66` — *"Nothing here is ever deleted by the probe — prune
    it yourself."* Result spool: retried until 2xx, so a prolonged manager outage
    grows it without a stated cap. Both fill the disk over months on an
    unattended client.

14. **Manager-redeploy self-heal is bounded — a long outage strands the probe.**
    `TROUBLESHOOTING.md:4c/4d`: a manager DB reset orphans the device credential
    (409 on re-enroll) → self-heal exit 4, bounded by `PROBE_SELFHEAL_MAX=6`. If
    the redeploy window outlasts the budget, the probe **gives up and needs a
    manual re-run** — hard on a remote client.

15. **Clock skew fails enrollment cryptically.** `TROUBLESHOOTING.md:8` — signed
    enrollment challenges + JWTs are time-sensitive; a fresh client VM with no NTP
    fails enrollment with an opaque error. The installer never checks/warns.

16. **`sudo` env-stripping meets `setdefault` config.** `probe.env` loads with
    `os.environ.setdefault` (`TROUBLESHOOTING.md:40`); under `sudo sh` the env is
    sudo's reset env, so a needed `HTTPS_PROXY`/`PROBE_CA_BUNDLE` silently isn't
    carried. Behind a corporate proxy or TLS-intercepting MITM the probe can't
    reach the manager. None of proxy / private-CA / mTLS is expressible in a
    single `curl|sh` without pre-work.

### Cross-cutting: doc drift on the identity model

17. **Two competing identity stories.** `probe.env.example:7-10` still says
    *"production should use a manager-issued PAT"*; `DEPLOYMENT.md` +
    `TROUBLESHOOTING.md` push device-enrollment / enroll-token; PATs die on
    manager DB reset (`TROUBLESHOOTING.md:3a`) and have **no dashboard UI**. Pick
    one canonical client identity model (device-enroll + `vet_` token) and make
    the docs agree.

### The cheap win

The enroll-token backend is **already built** (`probe_enrollment.py:769-842`).
What's missing is the **Fleet → Add Probe** UI that mints a `vet_` token and
renders the exact one-liner. Frontend-only; highest-leverage step toward the UX.

### If prioritizing

1. **Decide the licensing posture** (#7) — dictates whether "one command" is even
   achievable or is inherently two steps.
2. **Make one payload production-real** (#1, #2).
3. **Build the origin + a hardened bootstrap** (#3, #9, #10).
4. **Guarantee lifecycle** (#12, #13, #14).
5. **Ship the Add-Probe one-liner UI** and **fix host-binding fragility** (#4, #5).

---

## Part 3 — Non-disruptive implementation approach + step-by-step plan

**Prompt:**
> How do you implement in the current project without disrupting or impacting
> current work? What's your approach, and how do you go with it? Define a
> step-by-step plan.

### Approach — blast-radius control (governing principles)

The project is **live and dirty** (300+ uncommitted files, in-flight `manager/`
and `probe/` code, and possibly probes already enrolled against the AWS testing
manager). Any change to the install path, the manager, or the probe image risks
breaking in-repo dev workflows, stranding enrolled probes, destabilizing the
manager, or colliding with the uncommitted diff. So:

1. **Isolate in a git worktree + feature branch.** Build the distribution work in
   a separate worktree checkout so the messy main tree is never touched or risked.
   First preserve the current changes on their own branch (commit or stash) so
   nothing is lost or entangled.

2. **Additive only — no rewrites of load-bearing files.** New bootstrap script,
   new manager route, new UI page, new build script. The working `install.sh` /
   `Dockerfile` / enrollment flow stay **byte-for-byte unchanged**, so their tests
   stay green and in-repo devs are unaffected.

3. **Flag-gated, default-off manager route.** The distribution endpoints ship
   **disabled**; existing manager deployments see zero behavior change until an
   operator opts in. Safe to merge before the payload exists.

4. **Reuse the existing enrollment backend.** The `vet_` mint endpoint already
   exists; the UI just calls it. No new auth/identity surface = smallest blast
   radius.

5. **Parity enforced by a test (mirror the existing drift-guard).** A CI test
   fails if the sealed image's deps diverge from `requirements-runtime.txt` — so
   the "crippled sealed image" (#2) can't regress. Guard rails, not vigilance.

6. **Opt-in payload switch.** The sealed image becomes a new **versioned tag**
   selected by the bootstrap; the plain `Dockerfile` stays the dev default.
   Nobody is force-migrated.

7. **Staged rollout + kill switch.** dev → AWS testing manager → one throwaway
   canary VM → real client. The flag (or DNS) is the instant rollback.

8. **Each phase independently mergeable, revertible, and valuable on its own.**
   Order the work so stopping after any phase still leaves something shippable.

### Step-by-step plan (phased)

#### Phase 0 — Isolate & decide (no product change)
- **Preserve current work:** commit or stash the dirty tree on its **own** branch
  (don't mix distribution work into the existing diff).
- **Isolate:** `git worktree add ../vedha-probe-dist feature/probe-distribution`
  off a clean base — an isolated checkout; the main tree is untouched.
- **Baseline green:** run the probe pytest suite (~1651 tests, ~105 s) + manager
  tests; record pass-before so any regression is attributable.
- **Make the one gating decision:** **enforced-license vs floating** (failure #7).
  Document it. Everything IP-related (Phases 4–5) branches on this; Phases 1–3 do
  not, so work can start immediately regardless.

#### Phase 1 — Hosted origin + truncation-safe bootstrap, on the EXISTING image *(decision-independent, high value)*
- **New** `bootstrap`/`get.sh` (the hosted `/install.sh` entrypoint): function-
  guarded (`main() { … }; main "$@"` — safe on truncation), detects OS/arch,
  TLS-fetches a **pinned + signed** payload, verifies the signature, then delegates
  to the existing install logic. **Does not replace** `install.sh`.
- **New** manager static route: `GET /install.sh` + `GET /downloads/<ver>/…`,
  behind Caddy, **flag-gated default-off**.
- **Publish** the current **plain** image as a versioned, checksummed, signed tar
  (floating). No sealed dependency yet.
- **Verify end-to-end:** AWS testing manager + a throwaway VM → one command →
  probe online.
- **Stop-value:** a working `curl | sh --manager … --enroll-token …` one-command
  install for the floating case.

#### Phase 2 — Add-Probe one-liner UI *(frontend-only cheap win)*
- **New** Fleet → Add Probe page → calls the existing `POST /enroll-tokens` →
  renders the exact copy-paste command with a fresh `vet_` token. Additive UI +
  a thin BFF proxy. **No backend identity change.**
- **Stop-value:** Tailscale-style add-device UX for operators/customers.

#### Phase 3 — Lifecycle hardening *(decision-independent; prevents silent outages)*
- Optional **systemd unit** for reboot survival; **rotation/quota** on the result
  spool + result archive; **longer/backoff self-heal** for remote probes. All new
  knobs; defaults unchanged for existing installs.

#### Phase 4 — Sealed image → production parity *(IP track; needs the Phase 0 decision if enforced)*
- Fix sealed **dep parity** (add `impacket`/`ldap3`/`dnspython` to build +
  `--include-package`).
- Add a **parity test** (mirrors the drift-guard): sealed deps must equal
  `requirements-runtime.txt`.
- Run the sealed image through the **same release pipeline + runtime-parity
  tests** as the plain image; only then drop the "non-shipping" caveat.
- Switch the published payload to **sealed behind the flag / a new tag** — no
  forced migration.

#### Phase 5 — Licensing handshake *(only if enforced-license chosen)*
- Implement **install → hostid → mint → deliver** (two-step) **or**
  floating-license-gated; add expiry **renewal/grace**. Deliberately last —
  everything above works without it.

#### Phase 6 — Supply-chain + client-env hardening
- **Signature pinning** in the bootstrap; **hard-refuse non-local `http://`**;
  **proxy / CA / mTLS pass-through** flags; **clock-skew preflight**.

### Rollback discipline (throughout)
- Flag **default-off** is the master switch.
- Each phase merges + reverts **independently**.
- **Canary** on a throwaway VM before any real client.
- **Never test on prod**; always the AWS testing manager first.

### The gating fork, restated
Phases 1–3 (and the Phase 2 cheap win) deliver a working hosted one-command
install **without** touching the licensing question. Phases 4–5 are the IP-
protection track and depend on the **enforced vs floating** decision from
Phase 0. Resolve that decision when ready; it changes what "one command" can mean
(single-shot vs. an inherent two-step license handshake).

---

## Part 4 — Offline ZIP delivery & Windows-primary packaging

**Prompt:**
> I want to send them as a Docker image that does the required work — only need
> to send a **zip file**; in that file they only run `install.sh`, and that
> script itself identifies the OS and installs the required dependencies **and
> Docker** as well. **Mostly runs on Windows machines.** Design the architecture
> like that — is that the right approach? Don't start working; first find the
> areas of failure and the best enhancement approach, and document it here.

### Verdict — right *delivery* instinct, wrong *Windows packaging primitive*

Split the idea in two:

- **The delivery model** — a **self-contained ZIP**, one OS-detecting entry
  script, auto-installed dependencies, air-gap-friendly and inspectable — is a
  **sound pattern**. Keep it.
- **"Ship the Linux Docker image and auto-install Docker Desktop on a Windows
  host"** — for a **network scanner** whose whole job is LAN visibility, this is
  the **wrong primitive**. On Windows, Docker runs Linux containers inside a
  **WSL2 VM behind NAT**, so the probe scans the *virtual* network, not the
  customer LAN. Combined with Docker Desktop's licensing/admin/reboot weight and
  the fact that **Windows cannot execute a `.sh` at all**, "mostly Windows +
  Docker image + only run install.sh" does not hold together as stated.

This is how the market actually ships Windows scan agents (Nessus, Qualys,
Rapid7, CrowdStrike): a **native Windows agent + Windows Service**, delivered as a
**signed MSI** — *not* a Linux container. For a Windows-primary product, build on
the native path; keep Docker for your Linux customers.

### Grounded findings (from the probe code)

| Finding | Evidence | Impact on the proposed model |
|---|---|---|
| No Windows installer/service exists | only `tools/verify_windows_ground_truth.ps1` (a QA helper) | "run install.sh on Windows" has nothing to run |
| SYN / OS-fingerprint scanners use **raw sockets** | `syn_scanner.py:285,398-402` (`SOCK_RAW`,`IPPROTO_RAW`); `os_fingerprint.py:327` | native Windows needs **Npcap + admin**; in a container they bind the WSL2 NIC (wrong network) |
| Crash-safe durability is **POSIX-only** | `result_spool.py:60,81,120`; `transport.py:132,145,164,170,277` (`os.name=="posix"`) | on native Windows, atomic/fsync result durability silently degrades |
| Auto scope-ceiling detection is **Unix-only** | `install.sh:80-91` (`ip route`/`ipconfig`/`route`) | can't derive scope on Windows; inside WSL2 derives the **virtual** subnet |
| Container networking assumes LAN adjacency | `DEPLOYMENT.md` (probe scans its host's segment) | WSL2 NAT means "its segment" ≠ the corporate LAN |

### Areas of failure

**A. Windows cannot run `install.sh`.** `.sh` needs Git Bash/WSL/MSYS — not
present by default. The real Windows entry must be `install.cmd`/`install.ps1`.
PowerShell also blocks unsigned `.ps1` by default (execution policy) and tags
downloaded files with **Mark-of-the-Web**.

**B. WSL2 NAT — the scanner scans the wrong network (the killer).** A Linux
container on Docker Desktop sits behind a WSL2 virtual switch. Host discovery
(ARP/broadcast), SYN, UDP, and OS-fingerprinting see the **172.x virtual net**,
not the customer LAN. Auto-scope (`install.sh:80`) would even set the ceiling to
that virtual /24, so real-LAN jobs are **refused** (scope mismatch,
`TROUBLESHOOTING.md §5`). Worst kind of failure: enrolls green, scans nothing
real. `--network host` on Docker Desktop maps to the WSL2 VM, **not** the Windows
host NIC — it does not fix this.

**C. Docker Desktop is heavy, licensed, admin-gated, reboot-prone.** Requires
WSL2/Hyper-V (BIOS virtualization + Windows features + **reboot**), Administrator,
a commercial **license** for larger orgs, and is a multi-hundred-MB install.
Silent install exists (`Docker Desktop Installer.exe install --quiet`) but still
needs admin + reboot + the WSL2 kernel.

**D. Raw-socket scanners break on Windows.** Native: Windows blocks crafted raw
TCP/ICMP since XP SP2 → **no Npcap = no SYN/OS-fingerprint** (connect-scan still
works). Container: raw sockets work in the Linux kernel but on the wrong NIC (B).

**E. POSIX-only durability degrades natively.** The `os.name=="posix"` guards mean
crash-safe spooling/atomic result writes are skipped on Windows — a reliability
regression to close before a native Windows agent is trustworthy.

**F. Single script can't finish through reboots.** Enabling WSL2/Hyper-V or
installing Docker Desktop needs 1–2 reboots; a one-shot `install.sh` can't resume
across them without a RunOnce/Scheduled-Task handoff.

**G. SmartScreen / AV / EDR quarantine.** A script that installs software and
runs a **network scanner** is textbook-suspicious. Unsigned artifacts trip
SmartScreen; enterprise EDR quarantines scanner binaries. Needs **code-signing**
+ documentation for the customer's security team to allowlist — a go-to-market
gate, not just a technical one.

**H. Admin/UAC everywhere.** Installing Docker/Npcap/a service and using raw
sockets all require Administrator. The entry must elevate (UAC); a `.sh` can't.

**I. ZIP integrity & credential-in-ZIP risk.** An emailed ZIP is spoofable and
often size-blocked (image tar 200–500 MB). If a `vet_` enroll-token is baked in
for zero-touch, the ZIP now carries a **credential** — interception = a rogue
probe. Mitigate with signed artifacts + short-TTL/single-use/site-scoped tokens
(or keep pairing-code approval for ZIP delivery).

**J. No auto-update.** A ZIP is point-in-time; upgrades mean re-sending. Needs a
version stamp + a manager-driven update channel.

### Recommended architecture (best enhancement)

**One ZIP, OS-detecting entry, two native payloads — Windows-first.**

```
vedha-probe-<ver>.zip
├── install.cmd          ← Windows entry (double-click): elevates (UAC) → install.ps1
├── install.ps1          ← Windows: detect arch, install Npcap (optional), register service
├── install.sh           ← Linux/macOS entry: existing DOCKER-mode path
├── README.txt           ← quickstart + security-team allowlisting notes
└── payloads/
    ├── windows/  vedha-agent.exe  (sealed Nuitka build)  [+ npcap-*.exe]
    └── linux/    vedha-agent-<ver>.tar  (sealed Docker image)  + .sig
```

1. **Windows = native sealed agent + Windows Service, packaged as a *signed MSI*.**
   Build the **same agent** to `vedha-agent.exe` with Nuitka-on-Windows (same IP
   seal), register it as a **Windows Service** (WinSW/NSSM or `sc.exe`) so it runs
   on the **host network** — sees the real LAN, no WSL2 NAT, survives reboot
   natively, no Docker license. Prefer a **WiX-built MSI** over raw ZIP+scripts:
   MSI handles elevation, service install, Npcap as a bundled prerequisite, clean
   uninstall, upgrade codes (versioning), and passes SCCM/Intune + AV far better.
   *(Ship the MSI inside the ZIP if you want inspectability, or ship the MSI
   directly.)*

2. **Windows MVP = connect-scan mode (no Npcap, no admin for basic).** TCP
   connect + UDP + banner + TLS scanners use normal sockets and work on the
   Windows host network today. Ship that first (huge friction drop); add
   **Npcap-backed SYN/OS-fingerprint as an optional, admin-gated upgrade.** Before
   this is production-real, close the `os.name=="posix"` durability gaps (E).

3. **Linux = the Docker image you already have.** `install.sh` DOCKER mode + the
   sealed image; host networking on Linux actually sees the LAN.

4. **Docker-on-Windows only as an explicit, documented fallback** (customers who
   insist): force **manual `PROBE_NETWORK_SEGMENTS`** (never auto-detect on
   WSL2), warn loudly about virtual-network scope, and set expectations that
   discovery/SYN are degraded. Not the default.

5. **Sign everything; short-TTL enroll tokens; manager-driven auto-update.**
   Authenticode-sign the `.exe`/MSI + a detached signature/SHA256 for the ZIP;
   mint site-scoped, short-lived `vet_` tokens per delivery; let the probe (which
   already dials the manager) receive "newer version available" and self-update.

### The decision this forces

| Track | Effort | LAN scanning on Windows | Docker Desktop needed | Recommendation |
|---|---|---|---|---|
| **Native Windows agent (MSI + service)** | higher (Win build + Npcap + signing + durability fixes) | **correct** (host network) | no | **Recommended for a Windows-primary product** |
| **Docker image + auto-Docker-Desktop** | lower (reuse install.sh) | **broken/partial** (WSL2 NAT) | yes (license/admin/reboot) | fallback only, documented caveats |

### Non-disruption note

This is **additive**: a new `windows/` build target, a `.ps1`/MSI installer, and
guarded Windows durability code paths. It does **not** touch the Linux Docker
path, the agent's Linux behavior, or the enrollment backend. Same worktree +
flag-gated + parity-test discipline as Part 3. The native-Windows track slots in
as a **Phase 1.5 / 4-parallel** stream — independently valuable, independently
revertible.

---

## Part 5 — Implementation delivered: `probe/windows/` (native Windows agent)

**Prompt:**
> Can you create it? First make sure it doesn't disrupt current operations,
> find the areas of failure, divide it into small tasks, do it, and give me the
> files and the commands to run.

Delivered as a **purely additive** folder — no existing probe/manager code
changed, artifacts gitignored, nothing committed. The agent binary is
`agent/agent.py` compiled to one file (`agent.py:1789` defaults argv to `run`, so
the exe *is* the daemon). Full guide: `probe/windows/README.md`.

**Files (each a small task):**

| # | File | Role | Runs on |
|---|---|---|---|
| T1 | `run.cmd` | attended run; auto-detects the `/24` scope | customer |
| T2 | `install.ps1` + `install.cmd` | SYSTEM scheduled task (reboot-surviving), UAC-elevated | customer |
| T3 | `uninstall.ps1` + `uninstall.cmd` | remove task; `-Purge` wipes identity | customer |
| T4 | `build-agent-exe.ps1` | compile `agent/agent.py` → `vedha-agent.exe` (PyInstaller/Nuitka) | you (Windows) |
| T5 | `package-zip.ps1` | assemble `vedha-probe-win.zip` | you (Windows) |
| T6 | `README-CUSTOMER.txt`, `probe.env.template` | in-zip instructions + config | ship |
| T7 | `README.md`, `.gitignore` | operator guide; keep artifacts out of git | repo |

**Build + package (on a Windows box):**
```powershell
cd probe\windows
powershell -ExecutionPolicy Bypass -File build-agent-exe.ps1     # -> dist\vedha-agent.exe
.\dist\vedha-agent.exe hostid                                    # smoke test
powershell -ExecutionPolicy Bypass -File package-zip.ps1         # -> dist\vedha-probe-win.zip
```

**Customer runs (from the ZIP):** `run.cmd` to test → `install.cmd` (Run as
administrator) to make it permanent → `uninstall.cmd` to remove.

**Failure modes handled in-script:** execution-policy bypass, UAC elevation,
empty-scope auto-detect (+warn), console-less logging, reboot survival, idempotent
reinstall, shared identity under `C:\ProgramData\vedha-agent`.
**Documented (need signing/Npcap, not blockers):** SmartScreen/AV, raw-socket
SYN/OS-fingerprint needing Npcap, POSIX-only durability, clock skew, plain-HTTP
token exposure. Roadmap: code-sign → bundle Npcap → WiX MSI → Windows durability →
manager-driven auto-update.
