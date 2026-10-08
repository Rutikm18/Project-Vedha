# Windows agent - what is parked in the pipeline

Date: 2026-10-07 · Status: backlog, ordered, with the decisions it needs from the owner
First goal (done on the branch): send a Windows agent with one command, all dependencies included, and
self-diagnosis. Everything below was deliberately left out of that goal.
Related: [ADR-0005](../adr/0005-windows-agent-delivery.md) · [research memo](../research/2026-10-07-windows-agent-friction-and-competitors.md) ·
[version management](../design/agent-version-management.md) · [earlier quick-wins note](2026-10-02-windows-agent-quick-wins.md) ·
[STATUS.md](../STATUS.md).

Size: S under a day, M a few days, L a week or more. "Needs you" marks an owner decision or an account only the owner has.

## Now - before the first customer

| # | Item | Why | Size | Needs you |
|---|---|---|---|---|
| N1 | ~~Decide and fix F-1~~ **Done (8 Oct): the installer archives scan results in the locked data folder** (`PROBE_RESULT_DIR`). Remaining: a **retention limit**, because the archive is never pruned and grows with every scan | the archive is customer scan data at rest | S | Yes: how long to keep results (or turn the archive off) |
| N2 | **Fleet's "Generate install command" is blocked until a Linux release is published** | you cannot mint a token from the UI today. Either publish a Linux release (`make agent-release`, `make agent-publish`, `AGENT_RELEASE_PUBLIC_KEY`), or let the panel mint tokens without one (backend already allows it) and add a Windows card | S-M | **Yes: which route** |
| N3 | Manual field checks that CI cannot do: clean machine, **real enrolment**, reboot, UAC prompt, one customer endpoint product, `ALLOWLIST.txt` claims | the first real install already found two bugs CI could not | S | **Yes: you run them** |
| N4 | Remove the stray `probe copy` entry (`git rm --cached "probe copy"`) | every run warns exit code 128 | XS | no |
| N5 | **Deploy the S3 hosting once and try it** ([hosting guide](../operations/WINDOWS_AGENT_HOSTING.md)): the template has never run in AWS, and a real download from a clean Windows machine has not been tried | the whole hosted route is verified except the AWS side | S | **Yes: you run the AWS steps** |

## Next - make it trustworthy and testable

| # | Item | Why | Size | Needs you |
|---|---|---|---|---|
| X1 | **Code signing**: Authenticode for `vedha-agent.exe`, the installer scripts and later the MSI; submit the build to Microsoft for false-positive review | removes the SmartScreen warning and is the base of being trusted by endpoint products | M | **Yes: a signing identity and its cost** (EV certificate or Azure Trusted Signing; identity validation takes days) |
| X2 | **A protocol-level fake manager in the real-install test** (register, heartbeat, WebSocket hello) | `runtime-check` catches a missing library; only a connection test catches a broken protocol path. The real-install test could not have found the first field bug because its manager is unreachable on purpose | M | no |
| X3 | Pin the runtime dependencies (a hash-locked file) instead of `websockets>=12.0` etc. | builds float to whatever is newest; the `websockets` problem was version-dependent | S | no |
| X4 | A live `status` (`status --live`: probe the manager now) and a "last heard from the manager" time in `status.json` | `status` is the last recorded state, not a live check | S | no |
| X5 | Linux `install.sh` parity: `--token-file` and a `SHA256SUMS` check (the Windows installer has both; the PDF guide promises them) | closes a documented-but-missing gap | S | no |
| X6 | Proxy auto-detection from WinHTTP; read the company root from the Windows certificate store | fewer customer steps behind proxies and TLS inspection | S-M | no |
| X7 | Job signing end to end: the manager signs jobs, the agent verifies, on by default | verification exists in the agent but is off and nothing signs | M | no |

## Later - distribution and updates

| # | Item | Why | Size | Needs you |
|---|---|---|---|---|
| L1 | **Manager-hosted Windows package** (`windows-amd64` in the signed release manifest) and a Fleet OS switch. **Partly done differently (8 Oct): an S3 + CloudFront route with a one-line install exists** ([hosting guide](../operations/WINDOWS_AGENT_HOSTING.md)); what is left is serving it from the manager with the signed manifest and an OS switch in Fleet | the customer downloads from the manager, with Fleet generating the command | M | depends on X1 |
| L2 | **Update download and apply**: agent-authenticated route, signature and hash checked inside the agent, anti-rollback, restore on failure ([design](../design/agent-version-management.md#7-not-built-download-and-apply-the-design-to-follow)) | automatic updates | L | depends on L1 |
| L3 | **Channels, a staged rollout and a pause**, and a Fleet "update available" badge | an update must never reach every agent at once | M | depends on L2 |
| L4 | A real Windows service / MSI (Intune, group policy) | managed deployment | M-L | depends on X1 |
| L5 | Release pipeline: release built in CI, the release key held in a KMS instead of a file on one machine | the signing key is a single point of failure | M | **Yes: KMS account** |
| L6 | Air-gapped bundle for Windows (a signed offline package, and a relay) | sites with no direct internet | M | no |
| L7 | Sealed Windows build with the licence issued at enrolment | per-host licence control | M | no |
| L8 | Native Linux binary and Podman/RHEL support (STATUS P0-3b) | Linux customers without Docker | L | no |
| L9 | **Npcap** under its OEM licence: SYN scan, OS fingerprinting, ARP discovery on Windows | full-depth scanning on Windows | M | **Yes: the licence and its cost** |
| L10 | Windows on ARM; a virtual appliance (Hyper-V / VMware) | other customer environments | L | no |

## Suggested order

N1, N2 and N3 in parallel with X1's paperwork (it has a lead time); then X2 and X3; then X4-X7; then
L1 -> L2 -> L3 once the build is signed. Each item above that changes shipped agent code needs an
`AGENT_VERSION` bump (the CI version gate enforces it).

## Decisions needed from the owner

1. **Retention for the scan-result archive** (F-1 is fixed; the archive still grows without limit): how many days or scans to keep, or off? (N1)
2. **Fleet token button:** publish a Linux release, or change the panel? (N2)
3. **Signing identity and budget** for Authenticode / Azure Trusted Signing. (X1)
4. **Npcap OEM licence:** worth buying for Windows SYN scans, or recommend a Linux VM for depth? (L9)
