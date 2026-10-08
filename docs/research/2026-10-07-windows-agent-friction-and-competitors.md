# Windows agent: where customers get stuck, and what other vendors teach

Date: 2026-10-07 · Type: research memo (informs the [pipeline](../planning/2026-10-07-windows-agent-pipeline.md))
Related: [ADR-0005](../adr/0005-windows-agent-delivery.md) · [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) ·
[earlier Windows quick-wins note](../planning/2026-10-02-windows-agent-quick-wins.md) (failure points W1-W11, C1-C8).

> **How much to trust section 3.** The vendor and incident points come from web *search results*
> (14 searches on 7 Oct 2026), not from reading each source in full. The sources are listed in section 4.
> Re-check any point before quoting it outside the company. Sections 1, 2 and 5 are from this
> repository's code and the real installs.

## 1. The owner's four requirements, and how they were read

| Requirement | Reading | Built |
|---|---|---|
| 1. One command to install | `install.cmd -Token vet_...` from a zip; everything included | yes |
| 2. Security products should not detect it | **"Be trusted, not falsely blocked."** We do not build evasion of security tools. The honest means are: a signed build, a folder install in Program Files (no `%TEMP%` unpacking), published hashes, an allow-list note for the customer's security team, and a network footprint that is documented. A network scanner will look like a scanner, because it is one | partly (signing is not done: [pipeline](../planning/2026-10-07-windows-agent-pipeline.md)) |
| 3. Security implemented, the main code protected | the detection rules, AI and reporting stay on the manager; the agent holds only its collection code, compiled, with no source; identity and settings are access-restricted; every shipped file is checksummed | yes, with findings F-1 and the gaps in section 3 |
| 4. Automatic enrolment, easy management | single-use engagement-bound token, auto-approve, status and diagnostics on the machine, version reported to the manager | yes for enrolment; update and remote management are pipeline |

## 2. Where a customer gets stuck (in the order they meet it)

| # | Step | What goes wrong | Handled now | Still open |
|---|---|---|---|---|
| 1 | Receive the zip | tampering or a damaged download | zip SHA-256 sent by another channel (or, with the S3 route, carried in the command itself); every file re-checked by the installer | the zip is not signed |
| 2 | Unzip | Windows marks downloaded files; SmartScreen may warn on first run | README says "More info -> Run anyway" | needs Authenticode signing |
| 3 | Run `install.cmd` | not an administrator; execution policy | the installer asks for administrator rights itself and bypasses the execution policy for that script only | UAC path not yet tried by hand |
| 4 | Endpoint protection | quarantines or blocks the agent or a file in the package | the installer detects a missing or non-running program and names the folder to allow; `ALLOWLIST.txt` carries the hash | real behaviour with a customer's product is untested |
| 5 | Reach the manager | DNS, firewall that drops or rejects, proxy needing login or blocking the host, **TLS inspection** | `doctor --preinstall` before anything is changed; each failure has its own fix; `-Proxy`, `-CaBundle` | proxy auto-detection from WinHTTP; reading the corporate root from the certificate store |
| 6 | Clock | a wrong clock breaks TLS and tokens | `doctor` checks the clock against the manager's reply | none |
| 7 | Token | expired, already used, mistyped, engagement full | the manager's message is shown; the installer rejects a malformed token | a token typed on a command line is visible to local admins briefly (`-TokenFile` avoids it) |
| 8 | Approval | agent waits for a person | the installer shows the pairing code and address | none |
| 9 | Scope | the agent's own /24 and the engagement's scope disagree, so jobs are rejected | the installer prints the scope and warns about a very large network | the two scopes are not shown together in one place |
| 10 | After reboot / sleep | a laptop sleeps or changes network | a Scheduled Task at startup, restarting every minute; the agent keeps retrying an unreachable manager | not tried on a rebooted machine yet |
| 11 | Silent half-working | registered but not connected | the log, `status`, `doctor`, the manager's `GET /agents` (see the operator guide's checklist); a build gate that now exercises the connection | the first real install hit exactly this (F-3) |
| 12 | Update | a new version needs a new zip and a re-run | `-Repair` keeps the identity | no automatic update |
| 13 | Remove | leftovers | `-Uninstall [-Purge]`, tested | none |

Capability limits to state to customers: on Windows the agent does **connect scans** (no raw
sockets without Npcap), so no SYN scan, TCP-stack OS fingerprinting or ARP discovery. Banner, TLS,
SMB, LDAP, DNS and SNMP checks are unaffected. Npcap can be redistributed inside a commercial product
only with its paid OEM licence (nmap.org/oem), so it is a deliberate later decision, not a bundled
download. For full-depth scanning a Linux agent on a VM remains the answer. The agent's own startup
line reports `SYN scan: no` on Windows.

## 3. Security gaps found by reading the code (before and during this work)

Verified by reading the repository; none reproduced on a running system unless stated.

| Gap | Where | Status |
|---|---|---|
| Job-signature verification exists in the agent but is **off by default**, and the manager does not sign jobs | agent job handling, manager scheduling | open; pipeline "job signing end to end" |
| File-permission hardening of the identity file is done only on POSIX | `probe/agent` identity code | Windows relies on the folder's access list set by the installer (tested) |
| The release-signing key is a file on a build machine | `scripts/agent_release.py`, `make agent-keygen` | open; pipeline "release key in a KMS" |
| The Fleet install command carries the token on the command line | `install_commands` | single-use and short-lived; `-TokenFile` on Windows |
| The customer PDF guide documents `--token-file` and a `SHA256SUMS` check that the Linux `install.sh` does not implement | the vendor PDF vs `probe/install.sh` | the **Windows** installer implements both; the Linux gap is open |
| **F-1** scan results archived indefinitely in a user-readable folder | `task_runner.py` | **fixed 8 Oct** (archive moved into the locked data folder); no retention limit yet |
| Manager "Add agent" cannot mint a token until a Linux release is published | `AddAgent.tsx` | open; workaround via the API (operator guide) |

## 4. What other vendors and incidents suggest (from search results)

| Topic | The point | What we did or plan |
|---|---|---|
| **CrowdStrike, July 2024 outage** (Channel File 291 root-cause analysis) | A content update reached every sensor at once, and a validation gap turned a bad file into a crash on every machine. The response was staged deployment with customer control over timing | Version management reports what each agent runs; **channels, a staged rollout and a "pause" are pipeline requirements** before any auto-update |
| **Tenable Nessus Agent, Qualys Cloud Agent** (update settings; release notes) | Updates are managed by an *update plan* / channel the vendor controls, with documented exclusions for endpoint protection and a trusted-root update that customers had to apply | an `ALLOWLIST.txt` ships in the zip; update policy is a manager-side decision (pipeline) |
| **Notepad++ update hijack (reported 2025-2026)** | An update channel that is only "served over HTTPS" can be hijacked; the client must verify a signature of what it downloads | the planned agent-side download verifies the manifest signature and the file hash itself, with a key built into the agent ([design](../design/agent-version-management.md#7-not-built-download-and-apply-the-design-to-follow)) |
| **The Update Framework (TUF)** | Self-updaters face rollback (an old version re-offered) and freeze (updates withheld) attacks; separate keys for roles help | the agent already ignores any version not strictly newer; key roles and a freshness check are pipeline |
| **Elastic Agent upgrades** | An upgrade has a watcher that rolls back if the new agent does not come up; stuck upgrades are a known failure class | the planned apply step restores the previous folder if the new agent is not `online` by a deadline (the installer already restores on a failed install) |
| **Rapid7 Insight Agent / collector** | The updater and the collector are separate; offline sites use a collector as a relay; proxy and offline installs are documented paths | an air-gapped bundle and a relay are pipeline items; Linux on-prem bundles already exist |
| **Npcap / nmap licensing** | Free for personal use; redistribution inside a commercial product needs the paid OEM licence | no Npcap bundled |
| **Nuitka vs PyInstaller and antivirus** (blog-level evidence only) | Compiled-to-C builds draw fewer antivirus false positives than PyInstaller's bootloader, but no compiler removes the need for signing | Nuitka folder build chosen; signing is the real fix |
| **Claude Code's installer** (docs) | Release channels (`stable`, `latest`) and a switch to disable auto-update | the channel idea is in the pipeline |

Sources consulted (search results; not all read in full):
CrowdStrike "Channel File 291 RCA" and coverage (crowdstrike.com, scworld.com, bitsight.com, oodaloop.com);
Tenable docs on agent update settings (docs.tenable.com); Qualys Cloud Agent release notes and FAQ
(docs.qualys.com, success.qualys.com); Notepad++ supply-chain reporting (helpnetsecurity.com, orca.security,
esecurityplanet.com, privacyguides.org); The Update Framework (theupdateframework.io); Elastic Fleet upgrade
docs and known issues (elastic.co); Rapid7 Insight Agent docs and forum (docs.rapid7.com, discuss.rapid7.com);
Npcap and nmap OEM licensing (npcap.com, nmap.org/oem); Nuitka vs PyInstaller write-ups; Claude Code install docs
(code.claude.com); Microsoft Defender false-positive submission guidance (learn.microsoft.com).

## 4b. How other vendors install on Windows (8 Oct 2026, search results, not full page reads)

| Vendor | Install pattern | Token / key | Notes |
|---|---|---|---|
| Datadog | A one-line PowerShell command **generated in their app** (Fleet Automation > Install Agents > Windows). It downloads their signed MSI from their own download host and installs silently | API key inside the generated command | Closest to our S3 one-liner. Needs an elevated shell, PowerShell 5.1+ |
| Tenable Nessus Agent | Signed MSI, `msiexec /i ... NESSUS_KEY=... NESSUS_GROUPS=... /qn`; pushed by AD / SCCM / Intune / RMM | Linking key as an install property | Retries linking by itself (hourly if the manager is unreachable, every 24 h if the link fails); offline-install and custom-CA properties |
| Rapid7 Insight Agent | Signed MSI, `msiexec /i agentInstaller-x86_64.msi /quiet CUSTOMTOKEN=<region>:<token>` | Token as an install property | Community threads show Intune quoting and filename pitfalls: test the exact command in the tool you deploy with |
| Wazuh | `msiexec.exe /i wazuh-agent-<version>.msi /q WAZUH_MANAGER="<manager>"`, then start the service | Manager address (and optional registration password) as properties | Open source, MSI |
| Qualys Cloud Agent | `QualysCloudAgent.exe CustomerId=... ActivationId=... WebServiceUri=...`; also an MSI for Intune / GPO / SCCM | Customer ID + activation ID | Proxy argument supported |

What they share: a **signed installer** (MSI or EXE), the **enrolment secret passed as an install property**, a **silent switch**, and
**delivery through the customer's own software-distribution tool** (Intune, GPO, SCCM, RMM) for anything beyond a handful of machines. Only Datadog-style
vendors also offer a pasted one-liner, and they generate it per customer inside their product. Their keys are reusable group keys; ours is single-use per engagement, which is safer and less convenient for mass rollout.

Where we differ: unsigned build (all of them sign); a zip and scripts instead of an MSI (L4 in the pipeline); the command is made by hand through the API
(N2 in the pipeline), not generated in Fleet.

**Azure Trusted / Artifact Signing eligibility (sources disagree):** Microsoft's Artifact Signing quickstart lists organizations in the US, Canada, the EU, the UK, Australia,
New Zealand, Japan, South Korea, Singapore, Switzerland, Norway and Israel, and individual developers only in the US and Canada; an older page and a June 2026 answer name only the US, Canada, the EU and the UK.
India is on none of these lists. An organization outside the listed places should expect to use an EV/OV certificate with a cloud signing service instead. Check the live Microsoft Learn page before buying anything.

## 5. Recommendation (order of work)

1. **Sign the build** (Authenticode / Azure Trusted Signing). It removes the SmartScreen warning and is the foundation of
   being trusted by endpoint products.
2. ~~Fix F-1~~ (done: scan results now stay in the locked data folder; add a retention limit) and **unblock Fleet's token button** from the Linux release.
3. **Try it on a clean machine with a real enrolment and a reboot**, then with one customer's endpoint product.
4. **Then, and only then, auto-update**: agent-authenticated download, client-side signature and hash check,
   anti-rollback, restore on failure, channels with a pause, and a Fleet badge.
5. A real Windows service / MSI for managed deployment (Intune, group policy).
