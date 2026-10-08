# Vedha Agent: Installation Guide

**Prepared for:** {{CUSTOMER}} · **Agent release:** {{VERSION}} · **Manager:** `{{MANAGER}}` · **Date:** {{DATE}}

This guide explains how to install the Vedha agent in your network. You need about 15 minutes and root access to one Linux host.

---

## 1. What the agent is

The Vedha agent is a small, locked-down Docker container. It runs on one host in your network and checks the systems you have authorised.

| It does | It does not |
|---|---|
| Connect **out** to your Vedha manager over HTTPS (port 443) | Open any inbound port, or accept connections |
| Scan **only** the addresses in your engagement's scope; the manager and the agent both enforce this | Install anything on the systems it scans |
| Send scan facts (open ports, service versions, configuration observations) | Collect files, documents, credentials or user data |
| Run as a non-root user, with a read-only file system and no Linux capabilities | Hold any human password or long-lived API key: its identity is a key pair created on your host |

Your Vedha team can pause the agent at any time. It stops receiving work as soon as its access date passes.

## 2. What you receive, and how

You receive two things through **different channels**, so that interception of one alone is useless.

| Item | Channel | Contents |
|---|---|---|
| This kit | Email or file share | `vedha-agent-install.sh`, this guide, `SHA256SUMS` |
| Install token and checksum | Phone, Signal, or your password manager (**not** the same email) | A single-use token starting `vet_`, and the installer checksum below |

Installer SHA-256 (your Vedha contact will read it to you separately):

```
{{INSTALLER_SHA256}}  vedha-agent-install.sh
```

Release signing key ID: **`{{KEY_ID}}`**

The install token works **once** and **expires** (usually after 24 hours). Anyone holding it could add an agent to your engagement until then, so keep it private and use it promptly. If it expires, ask for a new one.

## 3. Before you start

### Host

| Requirement | Details |
|---|---|
| Operating system | Linux, amd64 or arm64: Ubuntu 22.04 or later, Debian 12, RHEL 9 / Rocky 9 / Alma 9, or Amazon Linux 2023 |
| Size | 2 vCPU, 4 GB RAM, 20 GB free disk. A small VM is fine |
| Software | Docker Engine, run by root ([install guide](https://docs.docker.com/engine/install/)), `curl`, and OpenSSL 3 (included in the systems above) |
| Placement | On the same network segment as the systems to assess, with no client isolation in between. Use a fixed IP or a DHCP reservation |
| Time | NTP time sync enabled |

On older systems such as RHEL 8, Ubuntu 20.04 or Amazon Linux 2, the installer needs the `python3-cryptography` package to check the release signature. Without it, the installer stops.

### Network

| From | To | Port | Why |
|---|---|---|---|
| Agent host | `{{MANAGER_HOST}}` | TCP 443 (HTTPS) | Download the agent; send results. Nothing else outbound is needed |
| Agent host | Systems in scope | The ports in your scope | The scans themselves |

- **Proxy:** if outbound traffic goes through a proxy, allow `CONNECT` to `{{MANAGER_HOST}}:443`. If the proxy inspects TLS, exempt this host from inspection (preferred) or have your proxy's CA certificate ready.
- **Security tools:** tell your SOC before the first scan, and allow-list the agent host's IP in IPS, NAC and EDR network policies for the engagement period. Otherwise scans may be blocked half-way through.

### Approvals

- A signed scan authorisation (rules of engagement) that lists the scope and time window.
- A change ticket, if your process requires one.

## 4. Check the kit

In the folder where you saved the kit:

```bash
sha256sum -c SHA256SUMS
```

Every line must say `OK`. Then compare the `vedha-agent-install.sh` value with the checksum your Vedha contact read to you. **If anything differs, stop and call your Vedha contact.**

You are welcome to read the installer first (`less vedha-agent-install.sh`). It is a plain shell script.

## 5. Install

**Step 1.** Copy the kit folder to the agent host.

**Step 2.** Save the install token to a file that only root can read. This keeps it out of your shell history:

```bash
sudo install -m 600 /dev/null /root/vedha-token
sudo nano /root/vedha-token        # paste the vet_… token, save
```

**Step 3.** Run the installer:

```bash
sudo sh vedha-agent-install.sh --manager {{MANAGER}} --token-file /root/vedha-token
```

| If you need to | Add |
|---|---|
| Go through a proxy | `--proxy http://proxy.example.local:3128` |
| Trust a TLS-inspection CA | `--ca-bundle /path/to/your-ca.pem` |
| Name the agent | `--name vedha-agent-dc1` |

**Step 4.** Check the output. You should see these lines:

```
Release signature verified (signing key {{KEY_ID}}).
Checksum verified. Loading the agent image ...
OK: agent '<name>' is installed with no PAT or human credential.
```

The signing key ID must be **`{{KEY_ID}}`**. If it is different, or you see "signature does NOT verify", stop and call your Vedha contact. Never work around these checks.

**Step 5.** Delete the token file. It cannot be used again anyway:

```bash
sudo rm -f /root/vedha-token
```

Within about a minute, your Vedha contact sees the agent as **connected**.

## 6. Check it is running

```bash
sudo docker ps --filter name=vedha-agent      # STATUS should be "Up"
sudo docker logs --tail 30 vedha-agent        # recent activity
```

## 7. Keep the agent host secure

- Membership of the `docker` group is equivalent to root. Only administrators who need it should have it.
- The agent's identity (its key pair) is stored in the Docker volume `vedha-agent-state`. Do not copy or share this volume.
- Keep the host patched. The agent restarts by itself after a reboot.
- If you believe the host has been compromised, stop the agent (`sudo docker stop vedha-agent`) and tell your Vedha contact. They can revoke it at once.

## 8. Day to day

| Task | How |
|---|---|
| See logs | `sudo docker logs -f vedha-agent` |
| Stop / start | `sudo docker stop vedha-agent` / `sudo docker start vedha-agent` |
| Upgrade | Run a newer `vedha-agent-install.sh` with a new token, using the same command as in section 5. The agent is replaced and **keeps its identity**, so nothing changes in Vedha |
| Remove | `sudo sh vedha-agent-install.sh --uninstall` |
| Remove completely (also deletes its identity) | `sudo PROBE_PURGE=true sh vedha-agent-install.sh --uninstall`, then `sudo docker image rm $(sudo docker images -q 'vedha-agent')` |

At the end of the engagement, remove the agent completely and tell your Vedha contact, who revokes it on their side.

## 9. If something goes wrong

| Message or symptom | What to do |
|---|---|
| `the install token was refused` | It has expired, was already used, or was revoked. Ask for a new token |
| `could not reach …` | Check outbound 443 to `{{MANAGER_HOST}}`, DNS, and the proxy (`--proxy`) |
| `unable to get local issuer certificate` | A TLS-inspecting proxy is in the way. Exempt `{{MANAGER_HOST}}`, or use `--ca-bundle` |
| `this host cannot check the release signature` | Use a supported OS, or install `python3-cryptography` |
| `signature does NOT verify` / `does not match the release checksum` | **Stop.** Call your Vedha contact. Do not retry with other options |
| The agent shows a pairing code instead of connecting | Read the code to your Vedha contact, who approves it |
| Scans stop part-way through | An IPS or firewall is blocking the agent's IP. Allow-list it |

When asking for help, send the output of `sudo docker logs --tail 100 vedha-agent`. It contains no passwords or tokens.

## 10. Your data

- Results go only to `{{MANAGER_HOST}}` over TLS, and are visible only to your organisation and your Vedha team.
- The agent sends facts about the systems it scans: addresses, open ports, service names and versions, configuration observations. It does not read file contents or capture traffic.
- When the engagement ends and the agent is removed, nothing of Vedha's remains on your host (after the "remove completely" step).

**Vedha contact:** {{CONTACT}}
