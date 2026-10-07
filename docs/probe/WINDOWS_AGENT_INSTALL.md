# Sending the Windows agent to a customer

**Goal:** the customer runs **one command** on a Windows machine and the agent is
installed, connected to your manager and able to explain what is wrong if it is
not. This page is for **you** (the operator). The customer's own instructions are
`README.txt` inside the zip (source: `probe/windows/README-CUSTOMER.txt`).

What the customer needs: Windows 10 / Server 2016 or newer (64-bit), administrator
rights, outbound HTTPS (TCP 443) to your manager. No Python, no downloads.

## 1. Build the package (once per release)

1. GitHub → **Actions** → **vedha-agent-windows-build** → **Run workflow**.
2. Pick the branch, and set **Manager address baked into the customer package**
   (default `https://api.vedhasec.com`). The address is written into the installer,
   so the customer never types it.
3. Wait for a green run. A re-run with the compile cache takes about 7 minutes; a
   cold build about 35.
4. Open the run → **Artifacts** → download `vedha-agent-windows`. It holds:
   - `vedha-agent-win.zip` — what you send
   - `vedha-agent-win.zip.sha256` — the zip's SHA-256

A run that is green has already, on a real Windows runner: compiled the agent,
checked it contains none of our source, started it, run the troubleshooting
commands, installed the package, checked the folder permissions and the scheduled
task, run `-Repair`, `doctor` and `support-bundle`, and uninstalled it
(`windows/tests/Test-InstallE2E.ps1`). A pull request run (no `manager_url`) bakes
in the placeholder `https://api.example.invalid`; **never send that one** — the
installer refuses to use it.

## 2. Create the customer's install token

In the portal: **Fleet → Add agent → Generate install command**. The command
contains `--token vet_…`; copy **only the `vet_…` value**. It works once and
expires after the lifetime you choose (shortest that works: 1 hour to 7 days). You
can revoke it in the same panel.

Set the engagement scope in the portal as usual. The Windows installer also sets
what the agent *may* scan on the machine itself (default: the machine's own
network; `-Scope 10.0.5.0/24` changes it).

## 3. Send it

| What | Channel |
|---|---|
| `vedha-agent-win.zip` | email, link, shared drive — anything |
| the zip's **SHA-256** (from the `.sha256` file) | **a different channel** (phone, chat) |
| the **install token** | **a different channel** (phone, chat) |

Splitting the channels is what makes the hash check mean something: someone who
swaps the zip cannot also change the hash you phoned through.

## 4. What the customer does

```
Get-FileHash .\vedha-agent-win.zip -Algorithm SHA256     # must match what you told them
# unzip, open a prompt in that folder, then:
install.cmd -Token vet_XXXXXXXX
```

Windows asks them to confirm administrator access once. The installer then:

1. checks Windows version, 64-bit, disk space and the package's own checksums;
2. runs `doctor --preinstall` — DNS, proxy, TCP, TLS, HTTP to your manager — and
   **stops before changing anything** if the manager cannot be reached, saying
   what to ask IT for;
3. installs to `C:\Program Files\Vedha Agent`, data in `C:\ProgramData\vedha-agent`
   (readable only by SYSTEM and Administrators);
4. registers a scheduled task `VedhaAgent` (SYSTEM, starts at boot, restarts itself);
5. waits until the agent reports **online** (or shows the pairing code if your
   manager needs a person to approve it), then removes the used token from disk;
6. prints `SUCCESS`, or `INSTALLED, BUT NOT CONNECTED YET` followed by the doctor's
   findings. A failed install puts the previous version back.

Variants: `-Proxy http://proxy:3128`, `-CaBundle C:\certs\root.pem` (HTTPS
inspection), `-Scope 10.0.5.0/24`, `-TokenFile C:\path\token.txt` (keeps the token
off the command line), `-Repair`, `-Uninstall [-Purge]`, `-NoWait`.
`run.cmd` runs the agent in a window without installing (no admin needed) — handy
for a first look on a restricted machine.

## 5. When something is wrong

The agent diagnoses itself; the customer never has to read a log first.

| They see | Meaning | What to do |
|---|---|---|
| `FAIL manager … cannot look up … in DNS` | name does not resolve | their DNS / VPN split-DNS; the message says what to try |
| `FAIL manager … cannot connect … refused` | address wrong, or a firewall rejects | check the baked address; ask IT to allow TCP 443 |
| `FAIL manager … cannot connect … timed out` | firewall silently drops | ask IT to allow it, or install with `-Proxy` |
| `… proxy requires a login (HTTP 407)` / `403` | proxy blocks the manager | IT exempts the machine / allows the host |
| `FAIL … TLS certificate is not trusted … signed by: <name>` | HTTPS is being inspected | IT exempts the manager from inspection (preferred), or `-CaBundle <their root .pem>` |
| `WARN clock` | machine clock is off | fix time sync; tokens and TLS depend on it |
| `The package failed its integrity check` | damaged download, edited file, or antivirus quarantined a file | download again; compare the SHA-256 |
| `The agent program does not run` / disappears after copy | antivirus / EDR blocked it | give them `ALLOWLIST.txt` (in the zip, holds this build's hash) |
| `awaiting-approval` + pairing code | manager needs a person to approve | approve in Fleet; the agent connects by itself |
| Windows prompt declined | nothing was changed | run again and choose **Yes** |

On the machine (Administrator prompt), `"C:\Program Files\Vedha Agent\vedha-agent.exe"`:

- `status` — what it is doing now (`--json` for tools)
- `doctor` — re-run the connection checks and explain
- `support-bundle [--mask-ips]` — writes a zip for you. It contains version, status,
  doctor result, redacted settings and the last log lines. It never contains the
  identity file, keys, tokens or queued results. **The customer emails it to you;
  nothing is uploaded automatically.**

The agent keeps retrying by itself, so once the customer fixes the cause (firewall,
proxy, CA) it connects without reinstalling.

Self-help is **diagnose, explain and safe self-heal only**. The installer and the
agent never change the customer's firewall, antivirus, proxy, certificate store or
PowerShell execution policy (a unit test enforces this).

## 6. Updating and removing

- **Update:** send a new zip and have them run `install.cmd -Token …` again (or
  `-Repair`). The agent keeps its identity. The agent reports the version it runs
  to the manager on every heartbeat (stored on the agent record; a Fleet "update
  available" badge is not built yet) and, when started, asks the manager whether a
  newer one exists. It does **not** download or apply updates yet (pipeline item).
- **Remove:** `install.cmd -Uninstall` (add `-Purge` to delete identity and logs).
  You can also revoke the agent from Fleet at any time.

## 7. Honest limits today

| Limit | Consequence |
|---|---|
| **Not code-signed** | SmartScreen / some EDR may warn or block on first run. The `ALLOWLIST.txt` carries the hash for their security team. Signing (Authenticode / Azure Trusted Signing) is the first pipeline item. |
| Runs as a scheduled task, not a Windows service | Fine for operation; it does not appear in `services.msc`. |
| Scan = TCP connect scan | Windows has no raw sockets without Npcap, so no SYN scan, OS fingerprinting or ARP discovery. Findings from banners, DNS, LDAP, SMB, SNMP are unaffected. |
| Updates are manual | See section 6. |
| The install token is passed on the command line | Visible briefly to local administrators. It is single-use; use `-TokenFile` if that matters. |
| Package is not encrypted | The zip holds only the compiled agent and scripts — no secrets. Identity is created on the customer's machine. |

## 8. Verified vs. not yet verified

**Verified** - on a GitHub `windows-latest` runner, in the run that built the zip you
download (all 22 install checks and every build step green):

- Build: closure-only compile (77 modules, MinGW gcc), no Python source or bytecode in
  the output, `version` / `hostid` / `manifest` / `runtime-check`, and `help`, an unknown
  command and `doctor` against an unreachable manager on the compiled exe.
- Installer logic under PowerShell 7 **and** Windows PowerShell 5.1.
- A real install from the unzipped package via `install.cmd`, then:
  - a damaged package, a missing agent program, a malformed token, an `http://` manager
    and an unreachable manager each stop **before** anything is installed, with the cause
    and the fix, and leave no task or folder behind; the token is never echoed or logged;
  - the program lands in `Program Files`, runs, and has its own Python and Visual C++
    runtime in the folder; the scheduled task runs as SYSTEM at startup;
  - the data folder is readable only by SYSTEM and Administrators; `agent.env` has no BOM
    and holds the settings; the install log holds no token;
  - the agent, started by the task as SYSTEM, writes its log and reports `retrying`
    with the reason and the fix when the manager is unreachable (it does not exit);
  - `doctor`, `status` and `support-bundle` work on the installed agent, and the bundle
    holds the diagnosis but no token or key;
  - `-Repair` keeps the settings and removes the leftover token; `-Uninstall` removes the
    program and task but keeps the identity and logs; `-Uninstall -Purge` deletes
    everything.

Two things the runs taught us, so you do not rediscover them:

- An unreachable manager used to make the agent give up after six checks. On Windows
  it now keeps retrying (`PROBE_KEEP_RETRYING=true`, written by the installer; the pause
  grows to 5 minutes). Linux/Docker keep the old exit-with-diagnosis behaviour.
- A first run of the installer stopped at `Get-FileHash` ("not recognized") on the
  runner. The exact cause was **not isolated**; a child Windows PowerShell can find that
  cmdlet when run on its own. The installer now hashes with .NET and starts from
  Windows PowerShell's own module folders, which got it through. If a customer
  machine ever reports a "not recognized" cmdlet, send the install log.

**Not verified yet - do these once before the first customer:**

1. Install on a **clean** Windows 10/11 or Server VM (not a CI runner): that the folder
   runs on a machine that never had Visual C++ or Python installed. (The folder carries
   the runtime DLLs; only a clean machine proves nothing else is missing.)
2. A **real enrolment**: a Fleet token, the baked manager address, the agent shows
   online, and a job runs end to end. CI only proves the unreachable-manager path.
3. **Reboot**: that the task starts the agent at boot and it connects after a restart.
4. The **UAC prompt path** (double-click `install.cmd`, not an elevated prompt). CI
   runs already elevated.
5. A machine **with your customer's EDR** (or Windows Defender with cloud protection) -
   expect a warning until the build is signed.
6. `ALLOWLIST.txt` says the agent "does not read files ... or capture traffic":
   confirm that is true of this build before you send it. The text was adapted from
   another vendor's guide, not derived from our code.
