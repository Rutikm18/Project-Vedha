You are working inside the Vedha repository as a senior platform, security, DevOps, and Bash automation engineer.

## Required top skills

Apply these skills throughout the implementation:

1. **Advanced Bash scripting**

   * Strict mode: `set -Eeuo pipefail`
   * Functions, arrays, traps, exit codes, argument parsing
   * Interactive menus and non-interactive execution
   * Idempotent and reusable shell automation
   * Safe quoting and input validation

2. **Docker and container lifecycle management**

   * Docker image build, pull, inspect, and run
   * Container networking
   * Container-to-host communication on macOS and Linux
   * Existing-container detection
   * Container logs, health checks, restart, and cleanup
   * Volume and environment-variable management

3. **FastAPI and REST API integration**

   * Inspect FastAPI routes and Pydantic schemas
   * Authenticate with `/auth/login`
   * Create Personal Access Tokens
   * Register probes
   * Poll agent status and heartbeat endpoints
   * Handle HTTP status codes and structured API errors

4. **Security engineering**

   * Secure handling of JWTs, PATs, passwords, and licenses
   * Least-privilege PAT scopes
   * Secret masking
   * Temporary-file permissions
   * Avoid leaking secrets through logs, command history, or Git
   * TLS enforcement for remote manager communication

5. **Authentication and authorization design**

   * Access-token authentication
   * Personal Access Token lifecycle
   * Token reuse, expiration, and revocation awareness
   * Probe registration authorization
   * Scope-based permissions

6. **Python CLI integration**

   * Safely invoke `probe/tools/issue_license.py`
   * Parse JSON without requiring `jq`
   * Parse Host ID and license output robustly
   * Validate output before using it

7. **Cross-platform automation**

   * Support macOS and Linux
   * Correctly handle:

     * `localhost`
     * `host.docker.internal`
     * remote HTTPS manager URLs
   * Detect operating system and platform-specific behavior

8. **Production-grade error handling**

   * Clear `[INFO]`, `[OK]`, `[WARN]`, and `[ERROR]` messages
   * Actionable failure messages
   * Cleanup traps
   * Retry and timeout handling
   * Sanitized diagnostic output
   * Preserve useful exit codes

9. **Secure DevOps**

   * `.gitignore` protection
   * Configuration-state separation
   * No hardcoded credentials
   * Reproducible setup
   * Dry-run support
   * ShellCheck-compatible scripts

10. **Repository-first engineering**

    * Inspect the existing code before implementing
    * Reuse current installer, Dockerfile, API schemas, and naming conventions
    * Avoid assumptions that conflict with the repository
    * Make minimal and surgical changes
    * Do not modify unrelated application code

---

## Objective

Build a production-quality interactive Bash CLI that automates the complete Vedha probe bootstrap, authentication, licensing, startup, registration, and verification workflow.

The operator should be able to run:

```bash
./scripts/run-probe.sh
```

The script should guide the operator through a small interactive menu and automatically complete the required setup.

Create:

```text
scripts/run-probe.sh
scripts/lib/common.sh
scripts/lib/manager.sh
scripts/lib/auth.sh
scripts/lib/license.sh
scripts/lib/probe.sh
scripts/lib/verify.sh
scripts/README-probe-bootstrap.md
```

## Supported commands

```bash
./scripts/run-probe.sh
./scripts/run-probe.sh install
./scripts/run-probe.sh status
./scripts/run-probe.sh logs
./scripts/run-probe.sh restart
./scripts/run-probe.sh register
./scripts/run-probe.sh uninstall
./scripts/run-probe.sh doctor
```

The default invocation must open an interactive menu.

## Interactive menu

```text
Vedha Probe Manager

1. Install and register a local probe
2. Install and register a remote probe
3. Re-register an existing probe
4. Check probe status
5. View probe logs
6. Restart probe
7. Run diagnostics
8. Remove probe
9. Exit
```

## Required installation workflow

The `install` workflow must:

1. Detect the repository root using the script location, not the current working directory.

2. Validate required tools:

```text
bash
docker
curl
python3
```

3. Verify that the Docker daemon is running.

4. Inspect the repository and identify the exact:

```text
FastAPI login route
PAT creation route
agent registration route
agent-list route
probe image build path
probe Dockerfile
probe Host ID output format
license-tool output format
probe installer
probe container name
required probe environment variables
```

5. Verify that this file exists:

```text
probe/tools/issue_license.py
```

6. Ask the operator to choose the probe image source:

```text
1. Use an existing local image
2. Build the image from the repository
3. Pull the image from a registry
```

7. Ask for or infer:

```text
Manager API URL
Platform URL visible from the probe container
Admin email
Admin password
Existing PAT or new PAT choice
Probe image
Probe container name
Customer name
License validity
Registration timeout
Polling interval
```

8. Use these local macOS defaults:

```text
Host-side manager API:
http://localhost:18080

Manager URL visible from a Docker container:
http://host.docker.internal:18080
```

9. For Linux local Docker, detect an appropriate host-gateway approach instead of assuming `host.docker.internal` is already available.

10. For remote environments, require an HTTPS platform URL unless the operator explicitly selects local development mode.

## Authentication

Authenticate with the repository-confirmed login endpoint, expected to be:

```http
POST /auth/login
```

Send:

```json
{
  "email": "<admin-email>",
  "password": "<admin-password>"
}
```

Parse the access token using Python.

Do not require `jq`.

Never print:

```text
complete access token
refresh token
admin password
PAT
license token
```

Display only masked values such as:

```text
vpat_abcd1234...
```

## Personal Access Token

Allow the operator to choose:

```text
1. Create a new PAT
2. Enter an existing PAT
3. Reuse a PAT from secure storage when supported
```

For a new PAT, use the repository-confirmed PAT endpoint, expected to be:

```http
POST /auth/personal-access-tokens
```

Use:

```json
{
  "name": "Vedha Probe CLI",
  "scopes": [
    "probe:read",
    "probe:write",
    "probe:register",
    "engagement:read",
    "engagement:write"
  ],
  "expires_in_days": 90
}
```

Avoid creating duplicate PATs unnecessarily.

When possible, inspect existing PAT metadata before creating another token.

Store only the PAT ID and masked prefix in operational state. Do not store the complete PAT in a normal plaintext state file.

## Probe image management

Support:

```bash
docker image inspect
docker build
docker pull
```

Before building, inspect the repository to determine the correct Docker build context and Dockerfile.

Do not assume `./probe` is the correct build context unless confirmed.

## Probe Host ID

Run the repository-supported Host ID command, expected to resemble:

```bash
docker run --rm "$PROBE_IMAGE" hostid
```

Parse the Host ID using the exact output format implemented by the probe.

Do not use a fragile unconditional `tail -n 1`.

Validate:

```text
Host ID is present
Host ID matches the expected format
Host ID is not an error message
Host ID belongs to the current probe host
```

## Probe license

Issue the license using:

```bash
python3 probe/tools/issue_license.py issue \
  --hostid "$PROBE_HOST_ID" \
  --customer "$CUSTOMER_NAME" \
  --days "$LICENSE_DAYS"
```

Parse the license token according to the actual tool output.

Fail clearly when:

```text
the tool does not exist
the command fails
the Host ID is invalid
the license token cannot be parsed
the license has already expired
```

Do not print the complete license token.

## Probe installation

Prefer the repository’s existing supported installer when available.

Inspect the repository for:

```text
install.sh
probe installer scripts
Docker Compose definitions
Makefile probe targets
documented docker run commands
```

The installer must receive the repository-confirmed equivalents of:

```bash
PROBE_IMAGE
PLATFORM_URL
OPERATOR_TOKEN
PROBE_LICENSE
```

If an existing container is detected, present:

```text
1. Restart the existing container
2. Recreate the container
3. Re-register the existing probe
4. Cancel
```

Do not silently delete or replace a running probe.

## Probe verification

After startup:

1. Verify the container exists.

2. Verify the container is running.

3. Inspect the last probe logs using sanitized output.

4. Poll the manager’s agent endpoint.

5. Match the expected probe using the strongest available identifier:

```text
probe ID
Host ID
registration ID
container-provided identity
```

6. Confirm:

```text
probe is registered
status is online
heartbeat is recent
manager can communicate with the probe
probe is polling for jobs
```

Use configurable values:

```text
registration timeout
polling interval
heartbeat freshness
```

On timeout, show:

```text
failed stage
HTTP status
sanitized API response
last 50 probe log lines
manager connectivity result
recommended correction
```

## Doctor command

Implement:

```bash
./scripts/run-probe.sh doctor
```

It must check:

```text
Operating system
Bash version
Docker CLI
Docker daemon
curl
Python
repository root
license tool
probe Dockerfile
probe image
manager API reachability
login endpoint reachability
container-to-manager connectivity
existing probe container
probe container health
probe logs
current probe registration
heartbeat freshness
platform URL configuration
TLS usage for remote manager
state-file permissions
Git ignore protection
```

## State management

Save only non-sensitive operational state in:

```text
scripts/state/probe.env
```

Allowed values include:

```env
MANAGER_API_URL=
PLATFORM_URL=
PROBE_IMAGE=
PROBE_CONTAINER=
PROBE_HOST_ID=
PAT_ID=
PAT_PREFIX=
CUSTOMER_NAME=
LICENSE_DAYS=
```

Do not save:

```text
admin password
access token
refresh token
complete PAT
complete probe license
```

Set restrictive permissions:

```bash
chmod 600 scripts/state/probe.env
```

Update `.gitignore` when necessary:

```gitignore
scripts/state/
*.probe.env
```

## Secret handling

Apply the following controls:

* Use `read -s` for passwords and tokens.
* Use `mktemp` for temporary files.
* Set temporary files to mode `600`.
* Remove temporary files through traps.
* Do not enable `set -x` when secrets are present.
* Do not pass secrets as command-line arguments when stdin, environment variables, or protected files are safer.
* Never print complete API responses containing secrets.
* Sanitize logs before displaying them.
* Warn the operator when using HTTP outside local development.

## Bash engineering requirements

Use:

```bash
set -Eeuo pipefail
```

Add traps for:

```text
ERR
EXIT
INT
TERM
```

Use well-named functions.

Avoid deeply nested logic.

Keep modules focused:

```text
common.sh   → logging, prompts, validation and cleanup
manager.sh  → reachability and manager configuration
auth.sh     → login and PAT management
license.sh  → Host ID and license generation
probe.sh    → image and container lifecycle
verify.sh   → registration and health verification
```

Use explicit return codes.

All destructive actions must require confirmation unless `--force` is supplied.

## CLI options

Support:

```text
--manager-url
--platform-url
--admin-email
--pat
--probe-image
--probe-container
--customer
--license-days
--timeout
--poll-interval
--non-interactive
--dry-run
--force
--verbose
--help
```

Do not accept the admin password directly as a normal CLI argument.

Allow it through:

```text
secure prompt
environment variable
protected file descriptor
```

## Dry-run mode

Implement:

```bash
./scripts/run-probe.sh install --dry-run
```

It must show sanitized planned actions without:

```text
creating a PAT
issuing a license
building or pulling an image
creating or deleting containers
registering a probe
modifying persistent state
```

## Non-interactive mode

Implement:

```bash
./scripts/run-probe.sh install \
  --non-interactive \
  --manager-url http://localhost:18080 \
  --platform-url http://host.docker.internal:18080 \
  --admin-email admin@vedha.io \
  --probe-image vedha-probe:latest \
  --customer "Vedha Local Lab"
```

In non-interactive mode:

* Never prompt.
* Fail clearly when required information is missing.
* Do not silently use insecure defaults.
* Read secrets only from approved environment variables or secure input sources.

## Idempotency requirements

Re-running the script must not silently create:

```text
duplicate containers
duplicate registrations
unnecessary PATs
unnecessary licenses
conflicting state files
```

Detect existing state and present the correct action.

## Documentation

Create:

```text
scripts/README-probe-bootstrap.md
```

Include:

```text
architecture
interactive usage
non-interactive usage
local macOS setup
local Linux setup
remote manager setup
PAT workflow
Host ID workflow
license workflow
probe registration
status and logs
doctor command
credential security
state-file behavior
troubleshooting
uninstall procedure
examples
```

## Implementation process

Before coding:

1. Inspect the existing repository.
2. Locate all relevant API routes and schemas.
3. Locate the probe entry point.
4. Locate the Host ID implementation.
5. Locate the licensing implementation.
6. Locate the installer and Docker definitions.
7. Identify the exact agent registration flow.
8. Identify the exact agent-list response schema.
9. State assumptions.
10. Present a concise implementation plan.

While coding:

* Make minimal changes.
* Follow existing repository conventions.
* Do not duplicate existing functionality.
* Do not modify unrelated application logic.
* Do not weaken authentication, licensing, or scope controls.

## Required validation

After implementation, run:

```bash
bash -n scripts/run-probe.sh
bash -n scripts/lib/*.sh
```

Run ShellCheck when available:

```bash
shellcheck scripts/run-probe.sh scripts/lib/*.sh
```

Test:

```text
--help
doctor
--dry-run
manager connectivity
login
PAT creation
existing-PAT use
probe image detection
Host ID generation
license generation
probe startup
existing-container handling
registration polling
online status
logs
restart
uninstall cancellation
non-interactive missing-input behavior
```

Do not claim that a test passed unless it was actually executed.

## Final report

After implementation, report:

```text
Files created
Files modified
Repository behavior discovered
Differences from initial assumptions
Validation commands executed
Passed checks
Failed checks
Untested checks
Security controls added
Exact command the operator should run next
```

The expected final operator experience is:

```bash
./scripts/run-probe.sh
```

The operator selects an installation mode, supplies only necessary information, and the script automatically handles:

```text
preflight
manager connectivity
authentication
PAT selection or creation
probe image preparation
Host ID generation
license issuance
probe startup
registration
online verification
sanitized diagnostics
```
