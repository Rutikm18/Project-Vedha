# Accuracy lab — TLS, end-of-life OS, databases, Terrapin

A reproducible lab that proves (or disproves) the checks clients see most often on a real
network, end to end: the **probe's real scanners** scan pinned Docker targets, the
**manager's detection engine** turns the facts into findings, and the result is graded
against `ground_truth.json`. Every check has a positive target and a clean control, so a
pass means "fires when it should *and* stays quiet when it should".

```sh
python scripts/lab/accuracy/run_lab.py \
    --probe-python <python with probe/requirements.txt> \
    --engine-python <python with manager/backend/requirements.txt>
python scripts/lab/accuracy/run_lab.py --only tls-weak tls-strong --keep   # a subset, leave it up
```

Needs Docker with compose v2. Images come from Docker Hub only (pinned tags); no
package mirrors are used, so it also runs where those are blocked. Output goes to
`results/<stamp>/`: each target's raw scanner JSONL, `findings.json`, and `report.md`.
The exit code is 1 when any expectation fails.

**Safety.** The targets are deliberately vulnerable. They sit on an `internal` bridge
(`172.31.250.0/24`) with no published ports and no route out. Never attach it to a LAN.

## Targets

| Target | Role | What it is |
|---|---|---|
| `ssh-terrapin` | positive | OpenSSH 9.3p2 built before the Terrapin fix: chacha20 without strict kex |
| `ssh-current` | clean | OpenSSH 10.3: strict kex; banner omits the portable `p1` suffix |
| `eol-ubuntu1604` | positive | Ubuntu 16.04 (EOL), named by its SSH banner |
| `supported-debian12` | clean | Debian 12: banner carries the package revision |
| `tls-weak` | positive | TLS 1.0/1.1, 1024-bit RSA, expired, self-signed (3DES offered but not preferred) |
| `tls-anon` | positive | TLS 1.2 whose only suite is anonymous ECDH (weak cipher) |
| `tls-strong` | clean | TLS 1.2/1.3, ECDHE + AEAD, 2048-bit, in date |
| `redis-noauth` / `redis-auth` | positive / clean | Redis 7.2 without / with a password |
| `mongo-noauth` | positive | MongoDB 7.0 without `--auth` |
| `mariadb`, `postgres` | exposure positive, auth clean | password-protected, reachable databases |

## Ground-truth fields

`expect` (must be reported), `absent` (must not be), `absent_prefixes`, `cve_max` (cap on
customer-facing CVE findings: a clean control's guard against version-match noise),
`severity`, and `known_gaps`: a real weakness the pipeline is known to miss, with who owns
the fix. A known gap is printed in the report, never counted as a pass, and flagged if it
starts being reported (move it to `expect` then).

## What the first runs found (17 Oct 2026)

Fixed in the manager (matcher revisions 3 and 4):

- OpenSSH builds that omit the portable suffix (`OpenSSH_10.3` on Alpine, macOS,
  Windows) were read as older than `10.3p1`: five false CVEs on a current server.
- MariaDB's wire version `5.5.5-10.11.19-MariaDB` was read as **5.5.5**: every MariaDB
  CVE since 2012.
- Multi-branch products (Redis 7.2.16) were flagged for CVEs fixed only on a newer line
  (8.0). A fix on another release line is now product presence, not a finding.
- `DEBIAN-CVE-…` records duplicated their `CVE-…` twin.
- Debian `+debNuM` / `~debNuM` (M>1) revisions were mistaken for first packagings.

Known gaps, agent side (see `known_gaps`):

- The TLS scanner records only the server's preferred cipher per version, so a weak
  suite offered beside a stronger preferred one (3DES on `tls-weak`) is never seen.
- The probe's `top1000` profile does not include 6379 (Redis), 27017 (MongoDB) or 2222
  (SSH alt): a standard run never reaches those services. The lab scans `full`.
- OpenSSH on Alpine (musl) is not exploitable by regreSSHion (CVE-2024-6387, glibc only),
  but its banner does not say Alpine, so the CVE is reported as suspected.
