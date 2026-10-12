# Windows agent: secure, easy to install, easy to connect - research and design

Date: 2026-10-11 · Status: **proposal for the owner's decision. Nothing in sections 5 to 9 is built.**
Builds on: [ADR-0005](../adr/0005-windows-agent-delivery.md) · [threat model](agent-delivery-threat-model.md) ·
[version management](agent-version-management.md) · [Windows pipeline](../planning/2026-10-07-windows-agent-pipeline.md) ·
[competitor memo](../research/2026-10-07-windows-agent-friction-and-competitors.md) · [ONE_COMMAND_INSTALL](../operations/ONE_COMMAND_INSTALL.md).

## 0. The design in one page

**Target experience.** A customer's IT person does *one* of these, and nothing else:

| Who | What they do | Customer actions |
|---|---|---|
| One machine, by hand | Paste the line from Fleet into any window, click **Yes** on the Windows permission prompt | 2 |
| Many machines (Intune, GPO, RMM) | Deploy one signed `VedhaAgent.msi` with the command Fleet prints | 0 on the machine |
| A machine with no token to hand | Run the MSI (or the line without a token); approve the pairing code in Fleet | 1 on the machine, 1 in Fleet |

**What makes it safe**, in eight rules:

1. **Two independent signatures on everything shipped.** Authenticode (so Windows and endpoint products trust it, and the prompt names a verified publisher) *and* our own release signature (so an agent trusts only us, even if the manager is compromised).
2. **The release trust root is pinned on the machine at install time**, inside the signed MSI. The manager can no longer change who is trusted.
3. **Keys have jobs and live in the right place.** An offline root, a signing key in a KMS or HSM that CI can use but nobody can copy, and a separate code-signing certificate. No private key sits on a laptop.
4. **Updates are verified by the agent, can only move forward, expire if stale, and roll back by themselves** if the new agent does not come up.
5. **Rollout is staged and pausable.** An update never reaches every agent at once.
6. **A real Windows service with least privilege**, not a Scheduled Task as SYSTEM, once a spike proves the scanners run without it.
7. **The device identity is hardware-protected** (TPM) where there is one, and file-protected where there is not.
8. **The enrolment secret never lands on a command line, in a log, or in a file that outlives the install.**

**What is new versus today:** an MSI as the main artifact, a pinned and rotatable trust root, a KMS-held signing key, Authenticode, a service
instead of a task, an update with rollback and rings, and Fleet-generated deployment commands for Intune, GPO and RMM. What stays: the one-time
engagement-bound token, the pairing-code fallback, the device key with a signed challenge, 10-minute access tokens, `doctor`/`status`/`support-bundle`.

**What it costs the owner:** a code-signing route (section 5.1 explains why Azure's service may not be available in India), a cloud KMS or HSM account,
and a Windows machine or VM for testing. Everything else is engineering.

## 1. Goals, non-goals, and how we will know it worked

**Goals.** (a) Installing on one machine takes one command and one click. (b) Installing on a thousand takes zero clicks on the machines. (c) A stolen
laptop, a stolen build machine, or a compromised manager cannot push code to customers. (d) A bad update cannot take the fleet offline.
(e) Connecting to the manager needs no firewall or proxy knowledge in the normal case, and explains itself when it does.

**Non-goals now.** macOS and Linux packaging (see [that pipeline](../planning/2026-10-11-macos-linux-agent-pipeline.md)), Npcap, a sealed per-host licence,
Windows on ARM.

**Measures** (each is testable): time from "command pasted" to "agent online in Fleet" (target under 3 minutes on a clean VM with a fast link); number of
customer actions per tier (table above); percentage of installs that need a support bundle (target under 5% in the first ten customers); an update
drill in which a deliberately broken release is refused or rolled back on 100% of test agents; a key-compromise drill that ends with all agents trusting
the new key and none trusting the old one.

## 2. What the research says, and how far to trust it

I searched the web on 11 Oct 2026 (about a dozen queries). Several official pages could not be fetched from this environment, so most points rest on
search-result summaries, not full reads. Each claim below is marked **[S]** (a source I saw), **[K]** (my general knowledge, not checked today: confirm
before relying on it) or **[R]** (from this repository's code).

**Code signing**
* **[S]** Microsoft's guide recommends *Artifact Signing* (the renamed *Trusted Signing*) for apps distributed outside the Store. **Organizations** in the
  USA, Canada, EU and UK can use it; **individual developers** only in the USA and Canada. Pricing is consumption-based: Basic about 9.99 USD a month for
  5,000 signatures, Premium about 99.99 USD for 100,000. **India is not on the list.**
* **[S]** Signing gives a *base* reputation with SmartScreen; reputation still builds over time. EV certificates **no longer give an instant SmartScreen
  bypass since 2024**. OV certificates cost roughly 150 to 300 USD a year. So signing is necessary but not a magic wand.
* **[S]** Always add an RFC 3161 timestamp (`signtool /tr … /td sha256`): without it the signature stops being trusted the day the certificate expires.
* **[S]** Nuitka *standalone* (folder) builds draw fewer antivirus false positives than *onefile*, which unpacks itself like a dropper. Signing plus
  submitting each release to Microsoft and the AV vendors is what actually works, and it has to be repeated every release.
* **[K]** For a company without access to Artifact Signing, the usual route is an OV or EV certificate whose private key lives in a cloud signing service
  or hardware module (the CA bundles one) so it can be used from CI. This was not researched today.

**Packaging and deployment**
* **[S]** Intune and SCCM work natively with MSI; **keep the MSI upgrade code constant forever** or Windows treats a new version as a different product.
  Intune needs a **detection rule** or it can never confirm an install; a product-code rule breaks across upgrades, so a **registry version key** is
  more robust; supersedence plus an in-place MSI major upgrade is how updates are delivered; failures are diagnosed in `IntuneManagementExtension.log`.
* **[S]** Every competitor in our memo ships a signed MSI with the enrolment secret as an install property (Tenable, Rapid7, Wazuh, Qualys, Datadog).
* **[K]** A WiX-built MSI can install and configure a Windows service (`ServiceInstall`), set failure actions, and run a custom action. MSI properties
  that hold secrets can be listed in `MsiHiddenProperties` so they are not written to verbose logs.

**Updates**
* **[S]** The Update Framework (TUF) defends against *rollback* (offering an old version), *freeze* (withholding updates) and key compromise, using
  versioned, **expiring** metadata and separate roles and keys. It cannot stop denial of service, but a stalled update becomes **detectable**. A 2022
  go-tuf advisory (CVE-2022-29173) shows the client's *verification code* matters as much as the design: persist the last trusted metadata and check it.
* **[S]** Elastic Agent upgrades **retry with growing waits** (1, 5, 10, 15, 30 minutes, then hourly), offer a **manual rollback** to the previous version for a
  limited time, and have had Windows-specific stuck-upgrade bugs. I could not confirm an *automatic* rollback watcher from the results.
* **[R]** Our own installer already restores the previous folder if the *install* fails; nothing restores it if the new agent installs but cannot connect.

**Service hardening**
* **[S]** Windows Service Hardening gives each service its own **service SID**, **least-privilege tokens** (`RequiredPrivileges`), and **write-restricted
  tokens** (the service can read broadly but write only where its service SID is granted). The same sources show privilege-escalation research against
  services, so a service running as SYSTEM with no need is a liability. **[K]** a *virtual account* (`NT SERVICE\<name>`) is the usual low-privilege identity.

**Device identity and enrolment**
* **[S]** A TPM-held key is non-exportable and can be *attested* (an attestation key signs the key's properties so a server can verify it is hardware-bound).
  Older Microsoft pages say this needs the *Microsoft Platform Crypto Provider* and RSA keys; **check the current rules**, we use Ed25519 today.
* **[S]** SPIRE's *join token* is one-time, short-lived and bound to an identity; after enrolment the agent holds a **short-lived certificate** it keeps
  renewing, and a re-attestation by join token cannot repeat (one-time), so the lifetime must tolerate downtime or an operator issues a new token. Our
  design already behaves the same way (single-use token, 10-minute access tokens, a refresh secret).
* **[S]** RFC 8628 (*device authorization grant*) is made for headless devices: show a short code, a human approves elsewhere, the device polls as a
  state machine and backs off on `slow_down`. Separate *first enrolment* from *routine renewal*. This is our pairing-code flow, and it is the right shape.
* **[S]** Wazuh passes the registration password to its MSI as a property and writes it to a file; I did not find its hardening advice.

**What I could not establish** (so the design avoids depending on it): current Microsoft guidance on TPM-backed Ed25519; Azure Artifact Signing
eligibility for India after 2025 (sources disagree, and Microsoft's page governs); Nuitka build reproducibility; whether Elastic's watcher rolls back
automatically; python-tuf's current API.

## 3. Where we are today ([R], read from the code)

* **Delivery.** A zip or a manager-served `install-remote.ps1` (one command; now self-elevating) that verifies a P-256-signed manifest and the package
  SHA-256, then runs the packaged `install.ps1`. No Authenticode on the exe, scripts or zip. No MSI.
* **Run.** A Scheduled Task `VedhaAgent` as SYSTEM at boot, restarting every minute; program in `Program Files`, data in `ProgramData\vedha-agent` locked by
  `icacls` to SYSTEM and Administrators.
* **Identity.** An Ed25519 device key and a refresh secret in `state.json` (plain file; the folder ACL is the protection; `chmod` does nothing on Windows).
  Enrolment: single-use engagement-bound token → request → challenge signed by the device key → activation. Access tokens last 10 minutes and are refreshed
  with a nonce and generation counter. The manager's signed site policy is trusted on first use and pinned.
* **Trust anchors.** The release public key is baked into the installer **served by the manager**. The installer script itself is unsigned.
* **Updates.** A first step exists (update ticket, one-shot task running the manager-served installer; off by default; no rollback; no staging).
* **Diagnostics.** `doctor` (DNS, proxy, TCP, TLS, HTTP), `status`, `support-bundle`, a status file, a rotating log.
* **Keys and build.** Signing keys are PEM files in a user profile on a PC; the build installs unpinned packages and Nuitka downloads its compiler.

## 4. From threats to controls

| Threat ([threat model](agent-delivery-threat-model.md) #) | Control in this design | Section |
|---|---|---|
| 1 signing key stolen | Offline root + online signing key in a KMS/HSM used by CI through short-lived credentials; no private key on a laptop; rotation drill | 5.1 |
| 2 poisoned build | Hash-locked requirements, pinned compiler, clean ephemeral build VM, SBOM and provenance attached to each release | 5.2 |
| 3 compromised manager | Trust root pinned in the signed MSI; agent verifies releases itself; manager can propose but not authorize | 5.1, 5.5 |
| 4 swapped command | Fleet shows a key fingerprint and puts the expected publisher in the command; the bootstrap refuses a mismatch | 5.3 |
| 5 bad release bricks fleet | Watchdog rollback, rings, pause, maintenance windows | 5.5 |
| 8 token leak | Token off the command line, hidden MSI property, short lifetime, optional machine binding, pairing alternative | 5.4 |
| 9 UAC habit | Authenticode publisher on the prompt; MSI does its own elevation | 5.1, 5.3 |
| 11 unsigned build | Authenticode + timestamp on exe, MSI, scripts | 5.1 |
| 13 agent as a foothold | Least-privilege service, signed jobs, scope enforced twice | 5.6, 5.4 |
| service as SYSTEM / local abuse | Virtual account, restricted token, narrow ACLs | 5.6 |

## 5. The design

### 5.1 Trust architecture: who may sign what

Four kinds of key, kept apart so losing one does not lose everything:

| Key | Purpose | Where it lives | Who can use it | If it leaks |
|---|---|---|---|---|
| **Release root** | Authorizes the signing keys and the trust list; signs rarely | Offline: a hardware token in a safe, two people | Ceremony only, a few times a year | Rotate by an out-of-band reinstall (the worst case; hence offline) |
| **Release signing key** | Signs each release manifest | A cloud KMS or HSM key that cannot be exported; CI uses it through short-lived federated credentials (no stored secret) | The release workflow, after an approval | Root revokes it and authorizes a new one; agents accept the change because the root signed it |
| **Authenticode certificate** | Makes Windows, SmartScreen and endpoint products trust `vedha-agent.exe`, the MSI and the scripts | The CA's cloud signing service or a hardware module; never a file | The same workflow | Revoke at the CA; reissue; agents do not depend on it for trust (rule 1) |
| **Device key** (per agent) | Proves *this* machine on every call | TPM where present, else a protected file | The agent service only | One machine is revoked in Fleet; nothing else is affected |

How an agent decides to trust a release (a deliberately small subset of TUF, which fits our size):

1. The MSI carries a **trust list**: the root public key(s) and the first signing key, inside the Authenticode-signed package. This is the pin.
2. A release manifest is signed by a signing key **and** names `version`, `expires`, `min_agent_version` and the hash of every file.
3. The agent accepts it only if: signature valid under a key the root has authorized, `version` is greater than the last accepted one (stored by the agent),
   it has not expired, and the package hash matches. A manager that withholds new manifests until the old one expires makes the agent say so (a freeze
   becomes visible in Fleet and in `status`).
4. **Key rotation** is a root-signed statement in the next release ("from version N, key B is authorized, key A is not"). Root rotation uses an overlap
   release signed by both roots. A rotation drill is part of the acceptance tests.

**Code-signing route (a decision for the owner, section 9).** Microsoft's own service is the cheapest and best fit **if** the company is in an eligible
place; the sources say that excludes India. Then the realistic route is an OV or EV certificate from a CA that offers a cloud signing service (so the
key is never a file), plus a timestamp. EV no longer buys instant reputation, so OV is probably enough. **[K]** Costs and terms need a quote.

### 5.2 Build and release pipeline

* Runs in CI on an **ephemeral Windows VM**, from a tagged commit, by a workflow that needs a second person's approval to reach the signing step.
* **Hash-locked dependencies** (`pip install --require-hashes`), a pinned Nuitka version, and a **pinned, checksummed C compiler** supplied from an artifact store
  rather than downloaded at build time. The build fails on any unpinned download.
* Output: `vedha-agent` folder → **Authenticode-signed exe and DLLs** → **MSI** (WiX) signed and timestamped → manifest signed by the KMS key → SBOM and a
  build-provenance statement attached. Nothing is published until a verification job re-downloads the artifacts and checks every signature and hash.
* **Today's blocker:** GitHub Actions is stopped by billing, so the first version of this pipeline is the one-command PC script
  (`publish-release.ps1`) running on a *dedicated, clean* machine, with the key still a file. That is acceptable for pilots and not for customers.
* Each release is also submitted to Microsoft and the main AV vendors for false-positive review (**[S]** this must be repeated every release).

### 5.3 Install experience

**One signed MSI is the product.** Everything else is a thin way to get it to a machine and run `msiexec` correctly.

```
Tier A  one machine, by hand      paste the Fleet line  ->  bootstrap verifies  ->  msiexec (UAC)  ->  service starts  ->  online
Tier B  many machines, managed    Intune / GPO / RMM runs: msiexec /i VedhaAgent.msi /qn MANAGER=... ENROLL=...    ->  online
Tier C  no token available        run the MSI / the line without a token  ->  pairing code (RFC 8628 shape)  ->  approve in Fleet  ->  online
```

* **Tier A bootstrap** (`install.ps1`, Authenticode-signed, tiny): fetches the manifest, verifies it against the *pinned* key id carried **in the command**
  (so a swapped command needs a swapped pin, and a person can compare the pin out of band), downloads the MSI with the token, checks its Authenticode
  publisher and SHA-256, then runs `msiexec`. **Windows Installer performs the elevation**, so the self-elevating PowerShell pattern
  [ADR-0005 D14](../adr/0005-windows-agent-delivery.md) was wary of goes away.
* **Tier B** gets commands Fleet generates and a copy-ready **detection rule** (a registry value `HKLM\SOFTWARE\Vedha\Agent\Version`), plus the uninstall command and
  an Intune supersedence note. The **upgrade code is fixed forever**; each release is a major upgrade. A reusable group token is an option here only (section 9).
* **Tier C** is the safest for a person who cannot get a token safely: nothing secret is typed; a human approves in Fleet with the code shown on the machine
  *and* the machine's name, IP and key fingerprint, so the approver can tell it is the right box.
* **Properties** map to configuration: `MANAGER`, `ENROLL` (hidden from logs, deleted after use), `SCOPE`, `PROXY`, `CABUNDLE`, `NAME`, `AUTOUPDATE`. Nothing else is required.
* **Configuration after install** is one file (`agent.json`, replacing `agent.env`) and one command (`vedha-agent configure --scope … --proxy …`) that validates
  before saving. Defaults are chosen so most sites need nothing: scope auto-detected (exists), **proxy auto-detected from WinHTTP**, **corporate root read from the
  certificate store**, both of which are open items today (pipeline X6).
* **Uninstall** is *Apps and features* or `msiexec /x`; it saves the scan archive first (exists today) and removes the task/service, files and, with a flag, data.

### 5.4 Enrolment and connection to the manager

Keep what works; harden around it.

1. **Token:** single-use, engagement-bound, 1 h by default. Delivered as a **hidden MSI property** or a file the bootstrap deletes; never in a log or on a child
   command line. A token may optionally be **bound to a machine** the operator names or a hardware hash pre-registered in Fleet (high-assurance sites).
2. **Key:** the agent creates its device key **in the TPM** when available (a non-exportable key with attestation, so the manager can record "hardware-bound"
   in Fleet); otherwise a key protected by the machine's data-protection API and the locked folder. **A spike must confirm** which algorithm the TPM provider
   accepts (we use Ed25519; many TPM paths are RSA or P-256) and may move the device key to P-256, which the installer already uses for verification.
3. **Enrol:** token → request → challenge signed by the device key → activation, unchanged. The manager records the key fingerprint and, if present, the
   attestation. Re-enrolment of a known device is refused unless an operator revokes the old one (exists).
4. **Connect:** a live WebSocket with an HTTP polling fallback (exists, now retries push mode). TLS 1.2+ to the manager; the manager's signed policy key is pinned. **mTLS**
   with a short-lived client certificate is an optional later hardening, not needed for the first release.
5. **Failure explains itself**: the five-step `doctor` chain, plus the installer's pre-flight, plus Fleet showing *why* an agent is not online (last error, last
   heartbeat, version, whether the clock is wrong, whether the key is hardware-bound).

### 5.5 Updates: verified, forward-only, reversible, staged

```
manager: release R signed, put in ring "canary" (5%)   ->  agent sees offer  ->  verify against pinned root (5.1)
    agent updater (a separate tiny signed service): download -> verify -> stop agent -> swap into slot B -> start -> wait for "online" + one heartbeat
        ok  -> mark slot B good, keep slot A for 7 days, report to Fleet           fail/timeout (5 min) -> restore slot A, report "update failed, rolled back"
    Fleet: ring health (success rate, time to online); promote canary -> 25% -> 100% automatically only if the previous ring is healthy; a PAUSE switch halts all
```

* **Two slots (A/B)** so rollback is a rename, not a reinstall. The installer keeps the old folder as `.old` today; this makes restoring automatic.
* **Updater is separate** from the agent and is itself updated rarely, through the same verification, so a broken agent cannot stop its own repair.
* **Rings and a pause** are manager-side (a ring per site or group; a global kill switch). **Maintenance windows** and "not while a scan runs" (exists).
* **No update to an unreachable or unsigned target; no downgrade; expired metadata means "do nothing and raise an alert", never "guess".**
* **MSI managed estates** can ignore all of this: their tool deploys the next MSI, and the agent's own updater is off by policy (`AUTOUPDATE=0`).

### 5.6 Run with least privilege

* **A Windows service**, not a Scheduled Task, installed by the MSI with failure actions (restart after 5, 30, 60 seconds), delayed automatic start, a description, and
  a dependency on the network stack. It removes the 1-minute restart loop of the task.
* **Account:** start from the **virtual account `NT SERVICE\VedhaAgent`** with a service SID, a **write-restricted token**, `RequiredPrivileges` reduced to the few we
  need, write access only to its data folder and read-only access to its program folder. **A spike is required first**: the connect scans, TLS, SMB, LDAP and the
  Windows checks must all work without SYSTEM. Anything that needs more is listed and either removed or granted by name. Until that spike passes, SYSTEM stays.
* **Data folder:** ACL to the service SID and Administrators only; the identity key and refresh secret in the TPM or protected; scan results with a retention limit.
* **Jobs:** the manager signs each job, the agent verifies the signature and the engagement scope against its **local** allowed networks before scanning
  (verification exists but is off and nothing signs: pipeline X7). **No credentials are stored** (already a rule).
* **The agent does not change the customer's security settings** (ADR D6 stays): no firewall, Defender, proxy or policy changes.

### 5.7 Being trusted by the customer's security stack

Authenticode on every binary and script, with timestamps; a stable publisher name so customers can write a **publisher-based allow rule** in their application-control
policy ([K], confirm the rule levels) instead of hash rules that break each release; `ALLOWLIST.txt` with hashes, the publisher and the network footprint; folder
install, no `%TEMP%` unpacking; honest documentation that the agent looks like a scanner. Evasion is out of scope.

## 6. End to end, with the failure each step can have

**Tier A (one machine).** Fleet shows a line with the manager, a token and the release key id → paste into any window → the bootstrap checks the manifest signature
against the pinned id → downloads the MSI → verifies the Authenticode publisher and SHA-256 → `msiexec` shows the Windows prompt (publisher: Vedha) → the service starts →
the agent enrols and the window prints `ONLINE`. Failures and what the person sees: wrong or used token ("ask for a new one", with the manager's reason);
no route to the manager (the pre-flight names the failing hop and the proxy fix); a security product blocks the file (names the file and the publisher to allow);
a mismatched pin (a clear "this installer is not from the release you were told about, stop").

**Tier B (managed).** An admin pastes the Fleet-generated command and rule into Intune, assigns a group, and watches the agents appear in Fleet. The MSI logs to the
standard location with the token masked. An uninstall and a supersede path are provided.

**Tier C (pairing).** Run the MSI; the console window and a status page show a code, the machine name and the key fingerprint; an operator approves in Fleet; the agent
is online. No secret was typed.

## 7. How this compares

| | Today | Competitors (memo) | This design |
|---|---|---|---|
| Signed installer | no | yes (MSI/EXE) | yes (MSI + scripts + exe, timestamped) |
| Enrolment secret | one-time token on a command line / file | property, reusable group key | hidden property or file; one-time; or no secret (pairing) |
| Mass deployment | not supported | Intune, GPO, SCCM, RMM | supported (Tier B) |
| Who the agent trusts | whatever the manager serves | vendor-controlled channels | a root pinned in the signed MSI, with rotation |
| Update safety | none | staged, some rollback | verified, forward-only, A/B rollback, rings, pause |
| Privilege | SYSTEM task | usually SYSTEM service | least-privilege service (after a spike) |
| Device key | file | varies | TPM where present |

## 8. Build order

Sized S under a day, M a few days, L a week or more. "Needs you" is an owner decision or an account.

**Phase 0 - close the cheap, high-impact gaps (no money, no certificate).**
| # | Item | Size | Needs you |
|---|---|---|---|
| 0.1 | **BUILT 12 Oct, agent 2.2.9 (untested on real Windows).** **Pin the release key on the machine**: install it from the *first* trusted copy, store it, and make `update_check`/`auto_update` verify against the stored key, not the one in a freshly fetched script | M | no |
| 0.2 | **Hash-locked, pinned build** (`requirements.lock` with hashes, pinned Nuitka, compiler from a checksummed artifact) | M | no |
| 0.3 | **Encrypt the signing keys at rest** and move signing to one clean machine; write the rotation and compromise procedures; run a rotation drill on a test key | S-M | no |
| 0.4 | **BUILT 12 Oct, agent 2.2.9 (untested on real Windows).** **Rollback**: if the new agent is not `online` in 5 minutes, restore the previous folder and report it | M | no |
| 0.5 | **Rings and a pause switch** in the manager, a Fleet "update available / rolled back" column | M | no |
| 0.6 | **BUILT 12 Oct, agent 2.2.9 (untested on real Windows); expiry is optional and off by default.** Manager signs a **release expiry and monotonic version**; the agent stores the last accepted version | S | no |

**Phase 1 - trust and the MSI.**
| # | Item | Size | Needs you |
|---|---|---|---|
| 1.1 | **Code-signing route**: decide the CA/service, buy, wire CI to sign with a key that is never a file; timestamp | M | **Yes** |
| 1.2 | **WiX MSI**: per-machine, fixed upgrade code, properties (hidden token), registry version key, silent install, uninstall saving data, logs; first as a *task* host, then the service | L | no |
| 1.3 | Sign the exe, DLLs, scripts and MSI; update the bootstrap to verify publisher and pin; Fleet shows the key id and a fingerprint | M | after 1.1 |
| 1.4 | **Fleet deployment page**: Tier A/B commands, Intune detection rule and uninstall, copy buttons, the pinned id | M | no |
| 1.5 | **Microsoft/AV false-positive submissions** as part of each release | S per release | no |

**Phase 2 - hardening.**
| # | Item | Size | Needs you |
|---|---|---|---|
| 2.1 | **Least-privilege spike**: run the whole scanner suite as `NT SERVICE\VedhaAgent` with a restricted token; list what fails | M | a Windows test VM |
| 2.2 | The Windows service + updater (A/B slots) replacing the Scheduled Task | L | after 2.1 |
| 2.3 | **TPM device key** with attestation (after the algorithm spike); fallback to a protected file | M-L | a TPM-equipped test machine |
| 2.4 | **Job signing end to end**, on by default | M | no |
| 2.5 | Scan-result **retention limit** | S | decide the number |

**Phase 3 - scale and polish.**
| # | Item | Size | Needs you |
|---|---|---|---|
| 3.1 | **KMS-held signing key and the release workflow** with two-person approval (when Actions billing is fixed or another CI is chosen) | M | **Yes: KMS/HSM account** |
| 3.2 | Machine-bound tokens; reusable group tokens for managed estates (with expiry and a use cap) | M | decide (section 9) |
| 3.3 | WinHTTP proxy auto-detect and certificate-store roots (X6) | S-M | no |
| 3.4 | Optional mTLS with short-lived client certificates | M | no |
| 3.5 | winget / Chocolatey listing, GPO ADMX template, air-gapped bundle and relay | M each | no |

**Acceptance tests to write alongside each item** (so none depends on trust): a release signed by the wrong key is refused; an expired one is refused; an older
version is refused; a manager serving a different installer cannot change the pinned key; a tampered MSI fails the publisher check; a broken update rolls back; a paused
ring does not update; a revoked agent cannot enrol again; the token appears nowhere in the MSI log, the event log or the process list.

## 9. Decisions for the owner (with my recommendation)

1. **Code-signing route.** Is the company eligible for Microsoft's service? If not, buy an OV certificate with a cloud signing service. *Recommend: OV with cloud-held key; do not buy EV.*
2. **Signing key home.** A cloud KMS or HSM (which cloud?), or a hardware token run by two people. *Recommend: the KMS of the cloud you already use for the manager, plus an offline root on a hardware token.*
3. **MSI first, service second?** Ship the MSI hosting the existing task (fast), then move to the least-privilege service after the spike. *Recommend: yes.*
4. **Reusable group tokens for managed estates**, with an expiry and a use cap, or keep single-use only? *Recommend: single-use for hand installs, capped group tokens for Intune/GPO only, per customer.*
5. **Machine-bound tokens** for high-assurance customers: worth building in the first release? *Recommend: later (3.2).*
6. **Update default.** Off until rings and rollback exist, then on for new installs with a `canary` ring you control? *Recommend: yes.*
7. **Retention** for scan results (days or count)? *Recommend: 30 days.*
8. **Test hardware.** A Windows 10/11 VM with and without TPM, a domain-joined one, and one behind a proxy with TLS inspection. *Needed for Phases 1 to 2.*

## 10. Risks in this design and unknowns to resolve on a real machine

* **Least-privilege may not be enough** for every scanner (some Windows checks need local rights). The spike decides; the fallback is SYSTEM with a narrower ACL.
* **TPM support varies** by algorithm and by Windows build; attestation needs a verifying component on the manager.
* **An A/B updater is real engineering** (locked files, antivirus holding handles, reboot cases). Budget for field bugs.
* **MSI custom actions are a common source of failed installs**; keep them to a minimum and test uninstall and repair paths.
* **Code signing does not remove false positives**; the submission process is ongoing work.
* **Everything Windows-specific here is untested**: nothing in this repository has yet been run on a real Windows machine against a real manager.

## Sources (search results unless noted; see section 2 for how far to trust each)

* Microsoft Learn, *Code signing options* (Artifact Signing, OV/EV, SmartScreen): https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options
* Azure Artifact Signing product page: https://azure.microsoft.com/en-us/products/artifact-signing
* The Update Framework specification and overview (rollback, freeze, expiring metadata): https://theupdateframework.io · CVE-2022-29173 (go-tuf): https://api.osv.dev/v1/vulns/CVE-2022-29173
* Elastic Fleet, upgrade Elastic Agent (retries, manual rollback): https://www.elastic.co/guide/en/fleet/current/upgrade-elastic-agent.html
* SPIRE server reference (join tokens, agent TTL): https://spiffe.io/docs/latest/deploying/spire_server/
* RFC 8628, OAuth 2.0 Device Authorization Grant: https://rfc-editor.org/info/rfc8628
* Microsoft, TPM Key Attestation: https://learn.microsoft.com/fr-fr/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn581921(v=ws.11)
* Windows Service Hardening overviews: https://itprotoday.com/it-security/understanding-windows-service-hardening and https://learn.microsoft.com/vi-vn/archive/blogs/voy/write-restricted-token
* Intune Win32 and MSI deployment, supersedence and detection: https://www.sikich.com/insight/intune-supersedence-with-win32-apps/ and https://www.mobile-mentor.com/insights/how-to-manage-the-application-update-process-in-intune/
* Wazuh Windows deployment variables: https://documentation.wazuh.com/4.8/user-manual/agent/deployment-variables/deployment-variables-windows.html
* Authenticode timestamping: https://www.encryptionconsulting.com/significance-of-time-stamping-for-code-signing-certificates/ and https://www.sectigo.com/faqs/detail/Time-Stamp-Server-Stamping-Protocols-for-Digital-Signatures-Code-Signing
* Nuitka and antivirus false positives (blog-level): https://pydevtools.com/handbook/reference/nuitka.md
