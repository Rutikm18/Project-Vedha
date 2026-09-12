# vedha-agent — SOC / EDR deployment guide

**Pre-empt the conversation:** vedha-agent is a legitimate, authorized network
scanner. It scans the LAN and beacons out to a Manager — behaviour your own EDR
*should* flag. Tell your SOC before rollout; this page is what they need.

## What the agent does that looks suspicious (and why it's fine)

| Observed behaviour | Why | Not malware because |
|---|---|---|
| Periodic outbound TLS beacon to one host | Receives scan jobs / returns results | One fixed destination, one port, no DGA, no domain fronting |
| Scans the local subnet | That's the product | Only within the operator-confirmed typed scope; denylist enforced locally |
| Restarts if killed | Service supervision | **Bounded** restart cap (`StartLimitBurst`) — respects a deliberate stop |
| Reads network interfaces | Scope detection | No raw-socket send on Windows; connect-scan fallback unprivileged |

## Exclusions to add (per EDR)

Add process + path allowlist entries for the agent's interpreter running
`agent.agent` / `agent.setup` under the install dir:

- **Process:** `python`/`python3`/`python.exe` invoked with `-m agent.agent`.
- **Paths:** the probe dir's `.venv`, the state dir (`/var/lib/vedha-agent`,
  `%ProgramData%\vedha-agent`, or `~/vedha-agent`), and the result queue therein.
- **Network:** outbound 443 (or the Manager's port) to the single Manager host.

CrowdStrike / Defender for Endpoint / SentinelOne / Carbon Black: add the above
as an allowlist/exclusion; submit the signed binary to the vendor's
false-positive / allowlist program before fleet rollout.

## Identify the agent

- Version + artifact hash: `python -m agent.setup collect-diagnostics` (redacted bundle).
- Service name: `vedha-agent` (systemd) · `com.vedha.agent` (launchd) · `VedhaAgent` (Scheduled Task).
- Network: one destination (your Manager), TLS, no inbound listener.

## Remove it

`python -m agent.setup uninstall` (removes the OS service). Add `down -v`-style
purge of the state dir to wipe identity + the result queue.

## Roadmap (before GA)
Code signing on all three OSes (Authenticode EV / notarized+hardened-runtime /
signed pkg+GPG) and vendor allowlist submissions — the single biggest reduction
in false-positive friction.
