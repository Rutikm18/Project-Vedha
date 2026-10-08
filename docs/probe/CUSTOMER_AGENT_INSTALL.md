# Installing the Vedha agent in your network

The Vedha agent is a small container that runs inside your network, scans the
systems in your engagement's scope, and sends the results to Vedha. It only
makes **outbound HTTPS connections to your Vedha manager** — nothing connects
in to it, and you open no inbound ports.

> **Windows host?** Skip to [Installing on Windows](#installing-on-windows) below. The portal's
> **Add agent** panel shows a **Linux / Windows** switch when your Vedha team has published
> the Windows agent.

## 1. Prepare a host

| Need | Details |
|---|---|
| Machine | A Linux VM or server: Ubuntu 22.04+, Debian 12, RHEL 9 or Amazon Linux 2023; amd64 or arm64; 2 vCPU, 4 GB RAM, 20 GB disk |
| Software | Docker Engine (rootful), `curl`, OpenSSL 3 (default on all of the above) |
| Placement | On the same network segment as the systems to be assessed, with a fixed IP or DHCP reservation |
| Network | Outbound HTTPS (443) to your manager address (shown in the portal); DNS that resolves it; time sync (NTP) |

Before the first scan, tell your SOC, and allow-list the agent's IP in any
IPS / NAC so scans aren't blocked half-way through.

## 2. Get your install command

In the Vedha portal open **Fleet → Add agent → Generate install command**. You
get one command like:

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://api.vedhasec.com/agent/install.sh \
  | sudo sh -s -- --manager https://api.vedhasec.com --token vet_…
```

The token in it works **once** and expires after the time you pick under
**Command valid for** (1 hour, 24 hours or 7 days). Anyone holding it can add an
agent to your engagement until then, so share it only with the person doing the
install, and choose the shortest lifetime that works. You can revoke it in the
same panel.

Prefer to read the installer first? Use **"Prefer to read the installer
first?"** in the panel: download `vedha-install.sh`, read it, then run it.

## 3. Run it on the host

Run the command as root. The installer:

1. checks Docker, the network path to the manager and the clock;
2. downloads the agent release from your manager and **verifies its Ed25519
   signature** against the key built into the installer;
3. downloads the agent image and **refuses to load it unless its SHA-256
   matches** the signed release;
4. starts the agent as a locked-down container (non-root, read-only file
   system, no Linux capabilities, log size capped) that restarts with the host;
5. enrols it with the token — no approval step.

Within a minute the panel shows **agent enrolled** and the agent appears under
**Connected vedha-agents**. Its scan range is exactly your engagement's scope.

### Behind a proxy

```bash
… | sudo sh -s -- --manager https://api.vedhasec.com --token vet_… \
      --proxy http://proxy.example.local:3128
```

If the proxy inspects TLS, either exempt the manager address from inspection
(preferred) or add `--ca-bundle /path/to/your-inspection-ca.pem`. Proxy
settings are written into the agent's own configuration too; scan traffic to
your local network never goes through the proxy.

### Other options

| Option | Use |
|---|---|
| `--name NAME` | Name shown in the portal (default: the host name) |
| `--no-proxy LIST` | Extra hosts that bypass the proxy |
| `--require-signature` | Fail if the signature can't be checked on this host (no OpenSSL 3) |

## 4. Operate

| Task | Command |
|---|---|
| Logs | `docker logs -f vedha-agent` |
| Status | the portal's Fleet page (heartbeat, current job) |
| Remove | `sudo sh vedha-install.sh --uninstall` (add `PROBE_PURGE=true` to delete its identity) |

## Access dates

Your Vedha team can give an installed agent an **access expiry** (for example the
end of a proof of concept). Fleet shows it as "expires <date>", or "access expired"
once it has passed.

- A scan already running at that moment finishes; no new scan starts.
- The agent does not remove itself or lose its identity. It waits, and **resumes by
  itself within about 5 minutes after your Vedha team extends the date**.
- You do not need to reinstall anything.

## What the agent sends, and what it doesn't

- It sends **scan facts** about the in-scope systems (open ports, service
  banners, configuration findings) to your Vedha manager over TLS.
- It holds **no human credentials**: its identity is a key pair created on the
  host, and its access tokens are short-lived.
- It **refuses jobs outside your engagement's scope**, which is enforced on
  the agent as well as on the manager.

## If something goes wrong

| Message | What to do |
|---|---|
| "the install token was refused" | It expired, was used, or was revoked — generate a new command |
| "could not reach …" | Check outbound 443, DNS and any proxy (`--proxy`) |
| "unable to get local issuer certificate" | A TLS-inspecting proxy — exempt the manager or use `--ca-bundle` |
| "release signature does NOT verify" | Stop and contact Vedha; do not work around it |
| The agent shows a pairing code | Enter it in Fleet → "Or approve with an installer code" |
| Fleet shows "access expired" | The access date passed. Ask your Vedha team to extend it; no reinstall |

## Installing on Windows

**The host.** 64-bit Windows 10 / 11 or Windows Server 2016 or later, Windows PowerShell 5.1 or
later, and an account that can run PowerShell as administrator. Same network rules as Linux:
outbound HTTPS (443) to your manager, working time sync, no inbound ports.

**The command.** In **Fleet → Add agent**, choose **Windows**, generate the command and run it in
PowerShell opened with **Run as administrator** (or paste the Command Prompt form into `cmd`, which
asks for administrator rights itself). It looks like this:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm 'https://api.vedhasec.com/agent/install.ps1'))) -Manager 'https://api.vedhasec.com' -Token 'vet_…'"
```

The token works once and expires like the Linux one. Before it installs anything the installer
verifies the signature on the release, checks the downloaded package against the checksum in that
signed release, and — when the release is Authenticode-signed — checks the signature on
`vedha-agent.exe`. If any check fails it stops and installs nothing. To check a release without
installing it, add `-VerifyOnly` to the command (no administrator rights needed).

**What gets installed.** A background task named **VedhaAgent** that runs as SYSTEM and starts at boot,
under `C:\ProgramData\vedha-agent` (identity key, logs). That folder is readable only by SYSTEM and
Administrators. The agent appears under **Connected vedha-agents** within a minute; its scan range
is exactly your engagement's scope.

**Security software.** A network scanner can look like malware to antivirus / EDR. Ask your security
team to allow `vedha-agent.exe` (and the folder above) before installing. If a file goes missing during
install, security software removed it: allow it and run the command again.

**Upgrade:** run a fresh command from the portal. **Remove:** from an administrator prompt run
`powershell -ExecutionPolicy Bypass -File C:\ProgramData\vedha-agent\uninstall.ps1 -Purge`
(without `-Purge` the identity and logs are kept).
