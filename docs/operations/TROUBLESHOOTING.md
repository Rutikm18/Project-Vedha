# Scanner Troubleshooting

This runbook covers the production Vedha probe workflow and the optional
third-party validation engines. A scan with no observations is a valid clean
result only when its component state is `completed` or `cached`. `failed`,
`degraded`, and `partial` runs are coverage gaps, not clean scans.

## Start Here

1. Open the completed job and inspect `outcome`, `issues`, and `scanner_runs`.
2. Confirm the expected component was `completed` or `cached`, not `skipped`.
3. Check the component's `error_code`, target, retryability, and remediation.
4. Confirm the effective allow/exclude scope and authorized target count in
   `run_stats.scope_enforced`.
5. Retry only transient failures. Fix configuration, dependency, privilege,
   template, feed, and parser failures before retrying.

The result's `engine_manifest` distinguishes:

- `scanner_module`: the production Vedha workflow orchestrator.
- Native components such as Host Discovery, TLS Inspector, and Web Fingerprint.
- Nmap and Masscan: optional standalone cross-validation tools. Availability
  does not mean they executed in the job.

The Next.js manager-local scanner routes are disabled by default. Production
scans should use the scope-bound manager-to-probe path. Set
`ENABLE_LEGACY_LOCAL_SCANNERS=true` only on an isolated validation worker; the
routes still require a FastAPI-validated `admin`, `manager`, or `tester` session.

## Probe Error Codes

| Code | Meaning | Operator action |
|---|---|---|
| `targets_missing` / `invalid_targets` | The job has no usable target list. | Supply IP, CIDR, hostname, or IP-range strings. |
| `scope_empty` | The manager supplied an empty authoritative scope. | Define engagement scope; do not retry a target-only manager job. |
| `no_authorized_targets` | Scope or exclusions removed every requested target. | Correct the job subset or engagement policy. |
| `target_expansion_limit` | A CIDR/range exceeds the 200,000-host materialization cap. | Split the job. Use separately governed Masscan validation for a genuine large sweep. |
| `dependency_missing` | A required binary or Python dependency is absent. | Install and pin the dependency, then restart the probe. |
| `permission_denied` | The service account lacks a required socket/file capability. | Grant the narrow capability needed; do not run the whole probe privileged by default. |
| `scanner_timeout` | A bounded component operation expired. | Verify reachability, lower concurrency, or raise the bounded timeout. |
| `dns_resolution_failed` | The probe could not resolve a hostname. | Verify the probe's DNS view or use an authorized IP. |
| `connection_failed` | Routing, firewall, or target state prevented a connection. | Test from the same probe network segment before retrying. |
| `resource_exhausted` | File descriptors, buffers, or memory were exhausted. | Lower concurrency and inspect service limits. |
| `scanner_internal_error` | A component raised an unexpected exception. | Preserve partial facts, inspect probe logs, and fix before retrying. |

## Nmap

The wrapper owns targets, XML output, and scripts. `--extra-args` accepts only
bounded tuning flags; target/input/output/script flags are rejected so they
cannot bypass `ScopeGuard`.

| Symptom | Meaning and action |
|---|---|
| `dependency_missing` | Run `nmap --version`; install Nmap on the probe host if absent. |
| `permission_denied` or an OS-profile failure | OS/SYN features require elevated packet access. Use a connect-based profile or grant only the required capability. |
| `timeout` | Narrow scope, tune `--host-timeout`/`--max-retries`, or raise `--nmap-timeout`. Aggressive retry limits can omit filtered hosts. |
| `parse_error` | Treat the run as failed. Verify the binary and data files belong to the same installed Nmap version. |
| Nonzero exit with XML facts | Facts are partial; the run remains degraded and must not be treated as complete coverage. |

References: [Nmap performance options](https://nmap.org/book/man-performance.html),
[XML output](https://nmap.org/book/output-formats-xml-output.html), and
[binary/data-file version mismatch issue](https://github.com/nmap/nmap/issues/1501).

## Masscan

Masscan is an optional large-scope discovery validator, not a hidden production
engine. The wrapper enforces scope before launch and exclusions again at the
packet layer.

| Symptom | Meaning and action |
|---|---|
| `permission_denied` | Verify root/CAP_NET_RAW and interface access. |
| `timeout` | Partial JSON is retained and marked degraded. Narrow scope or lower the rate. |
| `nonzero_exit` | Inspect the bounded error tail, interface selection, and source-IP configuration. |
| `parse_error` | Partial valid records are retained; malformed record count is reported. |
| Unexpectedly few ports | Re-run at a lower rate and verify candidates with TCP connect/Nmap before concluding they are closed. |

The wrapper caps the configured rate at 100,000 packets/second. Upstream warns
that transmit rate and packet loss directly affect coverage; see the
[Masscan README](https://github.com/robertdavidgraham/masscan) and
[false-negative discussion](https://github.com/robertdavidgraham/masscan/issues/450).

## Nuclei

The manager adapter streams `-jsonl`, separates per-request timeout from the
whole-job deadline, bounds stderr, terminates and awaits the process, and
retains findings emitted before timeout, parse error, or nonzero exit.

| Symptom | Meaning and action |
|---|---|
| `not_installed` | Install the pinned Nuclei binary and verify `nuclei -version`. |
| Template-related empty/failure | Verify templates are installed and compatible before accepting a zero result. |
| `timeout` with findings | Findings are partial. Reduce target/template volume or increase the job deadline. |
| `parse_error` | Check Nuclei/schema version drift; valid earlier JSONL lines remain partial evidence. |

References: [Nuclei running documentation](https://docs.projectdiscovery.io/opensource/nuclei/running),
[JSON export issue](https://github.com/projectdiscovery/nuclei/issues/4371), and
[timeout behavior issue](https://github.com/projectdiscovery/nuclei/issues/4607).

## OpenVAS / Greenbone

The adapter checks the GMP transform, scan config, port list, scanner, and feed
resources before launch. Polling has a deadline; `Stopped` is a failure, not
`Done`, and temporary scripts/output are permission-restricted and removed.

| Symptom | Meaning and action |
|---|---|
| Missing config/port list/scanner | Complete feed import and verify resource ownership for the GMP user. |
| Authentication or TLS failure | Verify GMP credentials, certificate trust, host, and port. |
| Feed not ready | Wait for feed synchronization/import; do not retry scans in a tight loop. |
| `Stopped`, abnormal helper exit, or deadline | Inspect Greenbone service logs and task status; do not publish zero findings. |

References: [python-gvm usage](https://greenbone.github.io/python-gvm/usage.html),
[Greenbone troubleshooting](https://greenbone.github.io/docs/latest/troubleshooting.html),
and [feed synchronization](https://greenbone.github.io/docs/latest/22.4/source-build/feed-sync.html).

## NetExec and WhatWeb

- NetExec output must use flags supported by the installed `nxc` version.
  Prefer its documented logging/database output and never interpret a usage
  error as zero hosts. See [NetExec CLI source](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/cli.py),
  [logging documentation](https://www.netexec.wiki/getting-started/log-your-results),
  and [JSON-output issue](https://github.com/Pennyw0rth/NetExec/issues/621).
- WhatWeb JSON stdout uses `--log-json=-` and is an array. A malformed,
  non-array, or nonzero result is an engine failure. See the
  [WhatWeb README](https://github.com/urbanadventurer/WhatWeb) and
  [JSON output issue](https://github.com/urbanadventurer/WhatWeb/issues/258).

## Result Delivery

The Go probe writes a result to its spool before WebSocket delivery and deletes
it only after the matching `result_ack` or successful HTTP upload. If results
remain queued:

1. Verify manager URL and strict TLS trust.
2. Confirm WebSocket authentication and the `/agents/ws` endpoint.
3. Check spool permissions and available disk space.
4. Look for an acknowledgment with the same job ID.
5. Do not manually delete unacknowledged spool entries.
