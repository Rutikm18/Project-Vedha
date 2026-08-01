# Vedha Probe Manager

`scripts/run-probe.sh` is the supported repository-local workflow for preparing,
registering, verifying, and operating a Docker probe.

## Architecture

The entrypoint detects the repository from its own location and loads five
focused modules:

- `common.sh`: logging, input validation, protected temporary files, and state
- `manager.sh`: host/container manager connectivity and TLS policy
- `auth.sh`: JWT login and least-privilege PAT creation/validation
- `license.sh`: deterministic container identity and signed license handling
- `probe.sh`: image and container lifecycle
- `verify.sh`: agent registration, heartbeat polling, and diagnostics

The host calls the manager through `MANAGER_API_URL`. The probe container calls
the same manager through `PLATFORM_URL`. Registration uses a five-scope PAT.
After registration succeeds, the container is recreated without the PAT and
resumes using its agent identity in the persistent Docker volume. The manager
does not consider bootstrap complete until the runtime logs show a job-receive
loop and the volume contains the persisted agent identity.

## Interactive usage

```bash
./scripts/run-probe.sh
```

The menu supports local/remote installation, re-registration, status, sanitized
logs, restart, diagnostics, and removal.

Direct commands:

```bash
./scripts/run-probe.sh install
./scripts/run-probe.sh status
./scripts/run-probe.sh logs
./scripts/run-probe.sh restart
./scripts/run-probe.sh register
./scripts/run-probe.sh doctor
./scripts/run-probe.sh uninstall
```

Use `--help` for all options.

## Local macOS

Defaults:

```text
Host manager:      http://localhost:18080
Container manager: http://host.docker.internal:18080
Image:             vedha-probe:local
Container:         vedha-probe
```

Start the manager first, then run the interactive installer. HTTP and disabled
licensing are accepted only for an explicitly local development target.

## Local Linux

Use the same URLs when Docker supports `host-gateway`. The manager automatically
adds:

```text
host.docker.internal:host-gateway
```

If the manager is on another host, provide its reachable HTTPS URL instead.

## Remote manager

Remote probe communication requires HTTPS:

```bash
VEDHA_PAT='vpat_...' \
VEDHA_PROBE_LICENSE='signed-license' \
VEDHA_PROBE_LICENSE_PUBKEY='vendor-public-key-hex' \
./scripts/run-probe.sh install \
  --manager-url https://manager.example.com \
  --platform-url https://manager.example.com \
  --probe-image registry.example.com/vedha/probe:1.0 \
  --network-segments 10.20.0.0/16
```

Configure the host/container trust store for private certificate authorities.
Do not disable TLS verification for production.

## Non-interactive installation

```bash
VEDHA_ADMIN_PASSWORD='read-from-a-secret-manager' \
./scripts/run-probe.sh install \
  --non-interactive \
  --manager-url http://localhost:18080 \
  --platform-url http://host.docker.internal:18080 \
  --admin-email admin@vedha.io \
  --probe-image vedha-probe:local \
  --network-segments 192.168.10.0/24 \
  --max-targets 4096 \
  --max-job-seconds 7200 \
  --customer "Vedha Local Lab"
```

If an active `Vedha Probe CLI` PAT already exists, the script refuses to create
a duplicate. Supply the existing value through `VEDHA_PAT`.

Do not place passwords or PATs directly in shell history. `--pat` exists for
automation compatibility, but `VEDHA_PAT` or a secure interactive prompt is
preferred.

`--network-segments` is a mandatory probe-local authorization ceiling, not a
discovery hint. Every manager-assigned target must be inside both its engagement
scope and this local ceiling. CIDRs are validated and normalized before launch;
an empty or malformed ceiling stops installation. `--max-targets` and
`--max-job-seconds` bound expansion and wall-clock execution for every job.

## Dry run

```bash
./scripts/run-probe.sh install --dry-run
```

Dry run validates configuration and prints a sanitized plan. It does not log in,
create a PAT, issue a license, build/pull an image, create/delete a container,
register a probe, or write state.

## PAT workflow

The manager uses:

```text
POST /auth/login
GET  /auth/personal-access-tokens
POST /auth/personal-access-tokens
GET  /auth/me
```

New PATs receive only:

```text
probe:read
probe:write
probe:register
engagement:read
engagement:write
```

The complete PAT is held only during bootstrap. Persistent state contains its
database ID and masked prefix. After registration, the PAT is removed from the
probe container configuration.

The runtime container has a read-only root filesystem, a bounded temporary
filesystem, all Linux capabilities dropped, `no-new-privileges`, a PID limit,
and an init process. It runs as UID/GID 10001. The bootstrap migrates older
root-owned state volumes in a network-isolated helper and verifies write access
before launch; existing identity, license, and result-spool files are preserved.

The current web Settings page does not expose PAT management, and the generated
API documentation does not currently provide an authenticated PAT form. Normal
probe installation does not require manual PAT access because `run-probe.sh`
creates and consumes the scoped PAT without printing it. If another client
requires the complete value, run `make probe-pat`; it displays the PAT once so
it can be copied directly into a secret manager.

## Host ID and licensing

The Docker image must be built from `probe/Dockerfile` with context `probe/`.
The manager invokes the probe’s Python identity implementation directly; it
does not call the operating system’s unrelated `hostid` utility.

A deterministic hostname and locally administered MAC address keep the
container fingerprint stable across recreation. A vendor key can issue a
host-locked license:

```bash
python3 probe/tools/issue_license.py keygen
./scripts/run-probe.sh install
```

Keep `probe/tools/vendor_private.key` on an authorized vendor workstation only.
The license is validated before use and written via stdin to the protected probe
Docker volume, not to `scripts/state/probe.env`.

## Registration and verification

The probe registers through `POST /agents/register`. Verification polls
`GET /agents`, preferring a saved agent ID and otherwise matching the exact
probe name. Success requires:

- a running container
- an online manager record
- a recent heartbeat
- successful manager/probe communication

Timeouts include sanitized logs and actionable connectivity guidance.

## State and credentials

Non-sensitive state is saved to:

```text
scripts/state/probe.env
```

The directory is Git-ignored and mode `0700`; the file is mode `0600`. It never
contains the admin password, JWT, refresh token, complete PAT, or license.
For isolated automation or tests, set `VEDHA_STATE_DIR` (and optionally
`VEDHA_STATE_FILE`) to a protected alternate location.

The probe’s long-lived agent JWT and X25519 private identity are necessarily
stored in its named Docker volume so it can restart without retaining the
bootstrap PAT. The probe writes that state atomically with mode `0600`, but a
host administrator or anyone controlling the Docker daemon can still read the
volume. Production hosts should therefore use encrypted disks, restrict Docker
socket/root access, and apply host backup controls. Hardware-backed key wrapping
or an external secret store is the remaining hardening path when that host trust
boundary is insufficient.

For non-interactive secrets, prefer a secret manager that injects:

```text
VEDHA_ADMIN_PASSWORD
VEDHA_PAT
VEDHA_PROBE_LICENSE
VEDHA_PROBE_LICENSE_PUBKEY
```

## Status, logs, and doctor

```bash
VEDHA_PAT='vpat_...' ./scripts/run-probe.sh status
./scripts/run-probe.sh logs
./scripts/run-probe.sh doctor
```

Logs mask PAT, bearer-token, generic token, and license-shaped values. Doctor
checks tools, Docker, repository paths, manager endpoints, container networking,
image/container state, registration evidence, heartbeat freshness, TLS policy,
state permissions, and Git ignore protection.

## Restart, re-registration, and uninstall

```bash
./scripts/run-probe.sh restart
VEDHA_PAT='vpat_...' ./scripts/run-probe.sh register
./scripts/run-probe.sh uninstall
```

Re-registration clears the cached agent identity only after confirmation.
Uninstall removes the container but preserves its state volume by default.
Deleting the volume is a separate interactive confirmation. In non-interactive
automation, destructive actions require `--force`.

## Troubleshooting

- Manager health failure: verify `MANAGER_API_URL/health`.
- Container connectivity failure: verify `PLATFORM_URL`, Docker DNS, firewall,
  and Linux `host-gateway`.
- PAT rejection: verify expiry, revocation, and the five probe scopes.
- License failure: verify Host ID, expiry, signature, and embedded public key.
- Registration timeout: inspect `./scripts/run-probe.sh logs` and ensure the
  probe name is unique within the tenant.
- Stale heartbeat: restart the probe and inspect manager/probe clocks.
