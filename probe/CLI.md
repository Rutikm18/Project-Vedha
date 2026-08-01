# Probe CLI

The probe CLI is the production control surface for a deployed scanner. It uses a
manager-issued Personal Access Token (PAT), stores it locally with `0600`
permissions, and then performs only the actions allowed by the PAT role and
scopes.

## Scope Of Work

After authentication the CLI can:

- show the authenticated user and token scopes;
- run pre-scan diagnostics against the manager, token, use-cases, scope, and online probes;
- list registered probes and available use-cases;
- create engagements when the PAT role is `admin` or `manager`;
- show authoritative engagement scope;
- enqueue on-demand probe scan jobs;
- wait for job completion and print status/results metadata;
- start the long-running probe daemon with the stored PAT.

The CLI does not bypass manager RBAC. A PAT with `tester` role can dispatch
permitted jobs, but it cannot create engagements because the manager route is
admin/manager-only.

## Token Model

The manager creates `vpat_...` personal access tokens under
`/auth/personal-access-tokens`.

Security properties:

- the full token is returned once;
- only a SHA-256 hash is stored server-side;
- tokens have expiry, revocation, last-used tracking, role, and scopes;
- PATs cannot create more PATs;
- PAT middleware enforces coarse scopes before route RBAC runs.

Residual risk: the CLI profile and registered probe identity contain bearer
tokens as plaintext JSON on the probe host. The writers use private directories,
`0600` files, and atomic replacement, but this is permission protection rather
than encryption at rest. Production probe hosts must use full-disk encryption,
least-privilege service accounts, short-lived narrowly scoped PATs, and prompt
revocation after an engagement. OS keychain or hardware-backed secret storage is
deferred because the probe must run unattended and portably across Linux,
Windows, containers, Python, and Go; adding it without a cross-runtime key
provider would create inconsistent recovery and deployment behavior.

Default probe CLI scopes:

```text
probe:read
probe:write
probe:register
engagement:read
engagement:write
```

## Create A PAT

From an interactive manager login, create a PAT. This example uses curl because
the dashboard token-creation UI may not exist yet.

```bash
BASE="https://manager.example.com"

ACCESS_TOKEN=$(curl -fsS -X POST "$BASE/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"manager@example.com","password":"REDACTED"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')

curl -fsS -X POST "$BASE/auth/personal-access-tokens" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "client-dmz-probe-cli",
    "expires_in_days": 90,
    "scopes": [
      "probe:read",
      "probe:write",
      "probe:register",
      "engagement:read",
      "engagement:write"
    ]
  }'
```

Save the returned `token` value. It is shown once.

## Authenticate The CLI

```bash
cd probe
./probe auth login --manager https://manager.example.com --pat "vpat_xxx"
./probe auth status
```

For automation, avoid putting the token in shell history:

```bash
export PROBE_PAT="vpat_xxx"
export PROBE_MANAGER_URL="https://manager.example.com"
./probe auth login
```

The config is stored at:

```text
~/.config/vedha/probe-cli.json
```

Use profiles when operating against multiple managers:

```bash
./probe --profile client-a auth login --manager https://a.example.com
./probe --profile client-b auth login --manager https://b.example.com
```

## Run The Probe Daemon

The daemon registers with the manager using the PAT, opens the outbound control
channel, receives on-demand jobs, enforces scope locally, and uploads results.

```bash
./probe daemon run \
  --name client-dmz-probe-01 \
  --location "Client DMZ" \
  --segment 10.20.30.0/24
```

For private PKI:

```bash
./probe --ca-bundle /etc/vedha/ca.pem daemon run \
  --name client-dmz-probe-01 \
  --segment 10.20.30.0/24
```

Use `--insecure` only for local development.

## Operator Commands

Run a pre-scan health check:

```bash
./probe doctor
./probe doctor --engagement-id "<engagement-id>" --json
```

List use-cases:

```bash
./probe use-cases
```

List online probes:

```bash
./probe agents list
```

Create an engagement:

```bash
./probe engagements create \
  --name "Client DMZ July Assessment" \
  --scope 10.20.30.0/24 \
  --exclude 10.20.30.10 \
  --scan-profile it
```

Run a safe first scan:

```bash
./probe scan run \
  --engagement-id "<engagement-id>" \
  --use-case uc_discovery_only \
  --target 10.20.30.20 \
  --wait
```

Run a web triage scan:

```bash
./probe scan run \
  --engagement-id "<engagement-id>" \
  --use-case uc_web_app_triage \
  --target 10.20.30.20 \
  --wait \
  --json
```

Check a job later:

```bash
./probe scan status "<job-id>"
```

Show manager-side authoritative scope:

```bash
./probe engagements scope "<engagement-id>"
```

## Capability And Accuracy Validation

The `validate` command performs preflight checks, enforces the authoritative
scope locally, checks that an online Probe advertises every selected capability,
runs bounded jobs sequentially, and saves private JSON evidence. It refuses to
send traffic until `--confirm-authorized` is supplied. Review the plan first:

```bash
export PROBE_MANAGER_URL="https://manager.example.com"
read -rsp "Validation PAT: " PROBE_PAT; export PROBE_PAT; printf '\n'

./probe validate \
  --scope 10.20.30.20/32 \
  --target 10.20.30.20 \
  --suite baseline \
  --ports 22,80,443 \
  --repeat 3 \
  --dry-run
```

Execute the reviewed plan:

```bash
./probe validate \
  --scope 10.20.30.20/32 \
  --target 10.20.30.20 \
  --suite baseline \
  --ports 22,80,443 \
  --repeat 3 \
  --confirm-authorized
```

Suites are `baseline`, `web`, `infrastructure`, `inventory`, `exposure`,
`full`, and `ot-passive`. Combine suites by repeating `--suite`, or add exact
manager use-cases with `--use-case`. `exposure` includes UDP and read-only SNMP
checks; `full` runs the full assessment; `ot-passive` is the only suite allowed
for an OT-profile engagement.

For accuracy scoring, supply ground truth collected independently from the
target:

```json
{
  "hosts": [
    {
      "ip": "10.20.30.20",
      "ports": [
        {"port": 22, "protocol": "tcp", "service": "ssh"},
        {"port": 443, "protocol": "tcp"}
      ],
      "cves": ["CVE-2026-0001"]
    }
  ]
}
```

```bash
./probe validate \
  --scope 10.20.30.20/32 \
  --target 10.20.30.20 \
  --suite full \
  --ground-truth ground-truth.json \
  --strict-ground-truth \
  --confirm-authorized
```

Omit a host's `ports`, port `service`, or `cves` field when that dimension is
unknown; the command reports it as not scored rather than treating missing
truth as an empty expected set. Results are stored under
`validation-results/<UTC timestamp>/` with directory mode `0700` and file mode
`0600`.

The manager cannot currently pin a job to a specific Probe. Validation
therefore requires exactly one online Probe by default. Use
`--allow-multiple-agents` only when mixed-Probe attribution is acceptable.

## Production Run Order

1. Confirm written authorization and approved CIDRs.
2. Create a manager/admin PAT with only required scopes.
3. Authenticate CLI on the probe host.
4. Start the daemon with the PAT.
5. Confirm readiness with `./probe doctor`.
6. Create or select an engagement with exact `scope_cidrs` and exclusions.
7. Run `uc_discovery_only` on one non-critical host.
8. Review manager assets/services/findings.
9. Expand to a small range, then the full approved range.
10. Revoke the PAT after the engagement if it is no longer needed.
