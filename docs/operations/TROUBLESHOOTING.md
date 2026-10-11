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

## Console: "Manager API …" errors (was "fetch failed")

The console's server (Next.js) calls the Manager API (`BACKEND_INTERNAL_URL`, `http://api:8000` in compose). When that call gets no HTTP answer, the console used to show only `fetch failed` with HTTP 500. It now names the cause, returns the matching status with `Retry-After: 5`, and writes one JSON line per failure to the frontend log (`"event":"backend.unreachable"`, with `code`, `path` and `status`). A read (GET) whose connection was dropped is retried once; a write never is.

| Message | Status | Cause | Check |
|---|---|---|---|
| `Manager API refused the connection (ECONNREFUSED)` | 503 | The API is down or restarting. | `docker compose ps api`; `docker compose logs --since 1h api` |
| `Manager API dropped the connection mid-request (ECONNRESET / UND_ERR_SOCKET)` | 502 | An API worker died during the request. The usual reason is the memory limit (`API_MEM_LIMIT`, 768M by default for 2 to 4 workers). | `docker stats --no-stream`; `sudo dmesg -T \| grep -iE "oom\|killed process"`; `docker compose logs api \| grep -Ei "died\|Waiting for child\|Started server process"` |
| `Manager API did not answer within 60 s` | 504 | The API accepted the request but never answered: overloaded, or a database query is blocked (no `statement_timeout` is set). | `docker compose exec postgres psql -U vapt -d vapt_db -c "select pid, now()-query_start as age, state, wait_event_type, left(query,80) from pg_stat_activity where state <> 'idle' order by age desc;"` |
| `Manager API address could not be resolved (ENOTFOUND)` | 503 | `BACKEND_INTERNAL_URL` names a host the console container cannot resolve. | `docker compose exec frontend printenv BACKEND_INTERNAL_URL` |

Reads wait at most `BACKEND_READ_TIMEOUT_MS` (default 60000; `0` turns the bound off) for the API to start answering; a download that has started is never cut. Writes and the two streaming proxies (operator exports, customer portal) keep Node's own limit.

One command shows the raw cause from inside the console container:

```bash
docker compose exec frontend node -e "fetch('http://api:8000/health').then(r=>console.log('HTTP',r.status)).catch(e=>console.log(e.message,e.cause&&(e.cause.code||e.cause.message)))"
```

A page where only some panels fail (for example *Scan catalog* loads but *Probe inventory* and *Engagement scope* fail) points at the API's database path, not at the network: the catalog is a fixed list and never touches Postgres.
