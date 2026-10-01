# Installing the Vedha agent in your network

The Vedha agent is a small container that runs inside your network, scans the
systems in your engagement's scope, and sends the results to Vedha. It only
makes **outbound HTTPS connections to your Vedha manager** — nothing connects
in to it, and you open no inbound ports.

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

The token in it works **once** and **expires after 24 hours**. Anyone holding it
can add an agent to your engagement until then, so share it only with the
person doing the install. You can revoke it in the same panel.

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
