# HTTPS for a deployed manager — one command

**Easiest:** on the server, in the repo directory (stack already running via `make full`):

```bash
./setup-https.sh
```

It asks for your domain and an email, shows the exact DNS records, can create them
(Route 53) and open ports 80/443 itself, checks everything, waits for DNS, then
enables HTTPS. `./setup-https.sh --status` · `./setup-https.sh --rollback`.

Non-interactive (automation / CI):

```bash
make tls DOMAIN=vedha.example.com EMAIL=you@example.com
```

Result:

| URL | Serves |
|---|---|
| `https://vedha.example.com` | dashboard + customer portal |
| `https://api.vedha.example.com` | API + probes (REST and WSS) |

Certificates come from Let's Encrypt (ZeroSSL fallback), HTTP redirects to HTTPS,
and Caddy renews automatically. Check any time with `make tls-status`.

## Before you run it

1. **DNS** — two A records to the server's public IP (use an Elastic IP so it never changes):

   ```
   vedha.example.com       A   <server public IP>
   api.vedha.example.com   A   <server public IP>
   ```

   On Route 53 the script can create them: `TLS_ARGS=--route53`.
   On Cloudflare set both to **DNS only** (grey cloud).
2. **Security group** — inbound TCP **80** and **443** from `0.0.0.0/0`
   (Let's Encrypt validates on port 80). Or let the script open them: `TLS_ARGS=--open-ports`.

Not sure? Diagnose first — changes nothing:

```bash
make tls-check DOMAIN=vedha.example.com
```

## Options (`TLS_ARGS="…"`)

| Flag | Effect |
|---|---|
| `--route53` | create/update both A records in Route 53 (AWS CLI + IAM) |
| `--open-ports` | open 80/443 in the instance's security group |
| `--staging` | Let's Encrypt staging (no rate limits, untrusted) — for a dry run |
| `--api-host HOST` | a different API host name than `api.DOMAIN` |
| `--no-legacy-http` | stop serving the API on `http://<ip>` (after probes are re-pointed) |
| `--wait-dns N` | wait up to N minutes for DNS to propagate (default 10) |
| `--yes` | skip the confirmation prompt |

## Troubleshooting (automatic)

If a certificate isn't issued within 4 minutes the script reads Caddy's log and names the cause:

| Symptom in the log | Cause | Fix |
|---|---|---|
| timeout / connection refused on `/.well-known` | port 80 blocked | open TCP 80 to `0.0.0.0/0` (SG and NACL) |
| NXDOMAIN / DNS problem | no A record yet | create the records, wait for propagation |
| unauthorized / invalid response | DNS points elsewhere, or a CDN proxy | point straight at the server; Cloudflare → DNS only |
| rateLimited | too many recent attempts | wait; test with `--staging` |
| CAA | CAA record forbids the CA | allow `letsencrypt.org` / `sectigo.com` |
| address already in use | nginx/httpd on 80/443 | stop it |

Caddy keeps retrying by itself; after fixing, `make tls-status`.

## After switching

- Re-point probes: `./install.sh https://api.vedha.example.com` (or `PLATFORM_URL=` in `probe.env`).
  Until then they keep working through `http://<ip>`; close that with `TLS_ARGS=--no-legacy-http`.
- `make full` / `make gen-env` keep HTTPS on (they read `TLS_DOMAIN` from `.env`).
- Undo everything: `make tls-rollback` (restores the backed-up `.env` and the port-80 proxy).
