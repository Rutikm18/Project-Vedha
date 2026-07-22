# Probe Runbook — step by step

Two audiences: the **vendor** (you — build & license the probe once) and the
**client** (deploy it inside their network). Plus a **dev** path for local testing.

---

## A. Vendor — one-time setup (you, on a trusted machine)

```bash
cd probe

# 1. Make the signing keypair (ONCE). Keep the private key secret forever.
python3 tools/issue_license.py keygen
#   → prints VENDOR_PUBLIC_KEY_HEX  +  writes tools/vendor_private.key (gitignored)

# 2. Build the SEALED probe image (native binary, no source) with your public key baked in.
docker build -f Dockerfile.sealed -t registry.example.com/vedha-probe:1.0 \
  --build-arg PROBE_LICENSE_PUBKEY=<hex from step 1> .

# 3. Push to your registry (clients pull from here).
docker push registry.example.com/vedha-probe:1.0
```

You now have: a sealed image clients can run but not read, and a private key only you hold.

---

## B. Client — deploy the probe (inside their network)

```bash
# 1. Get this machine's Host ID (no install needed):
docker run --rm registry.example.com/vedha-probe:1.0 hostid
#   → e.g.  6106788dc177      (client sends YOU this id)
```

```bash
# 2. You (vendor) issue a license bound to that host:
python3 tools/issue_license.py issue --hostid 6106788dc177 --customer "Acme" --days 365
#   → a license token; send it to the client
```

```bash
# 3. Client installs — one command (the installer pulls the image, configures, runs):
curl -fsSL https://YOUR_HOST/install.sh | \
  PROBE_IMAGE=registry.example.com/vedha-probe:1.0 \
  PLATFORM_URL=https://manager.example.com \
  OPERATOR_EMAIL=ops@acme.com OPERATOR_PASSWORD=*** \
  PROBE_LICENSE=<token from step 2> \
  sh

#   …or inspect-first (recommended for security teams):
curl -fsSL https://YOUR_HOST/install.sh -o install.sh
less install.sh            # read it
sh install.sh              # interactive — prompts for the values above
```

The probe now: verifies its license → registers with the manager → polls for jobs →
scans (scope enforced) → ships raw facts back. It dials **out only**, no inbound ports.

```bash
# Operate:
docker logs -f vedha-probe          # watch it
docker rm -f vedha-probe            # stop/remove
```

---

## C. Run a scan (operator, from the manager)

```bash
# 1. Log in, get a token:
TOKEN=$(curl -s -X POST https://manager.example.com/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"ops@acme.com","password":"***"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

# 2. Create an engagement (the authorization boundary = scope):
EID=$(curl -s -X POST https://manager.example.com/engagements \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"Acme Q3","scope_cidrs":["10.0.0.0/24"]}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

# 3. Enqueue a scan (the probe inside Acme's network picks it up):
curl -s -X POST https://manager.example.com/agents/jobs \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"engagement_id\":\"$EID\",\"job_type\":\"discovery\",
       \"params\":{\"scan_type\":\"assessment\",\"targets\":[\"10.0.0.0/24\"],
       \"scope_cidrs\":[\"10.0.0.0/24\"]}}"

# 4. Findings appear in the dashboard (https://manager.example.com → :3000) and via API:
curl -s "https://manager.example.com/findings?engagement_id=$EID" -H "Authorization: Bearer $TOKEN"
```

Scan modes (in `params.scan_type`): `assessment` (full), `discovery`/triage (fast),
or service-specific (`tls_scan`, `web_scan`, `db_fingerprint`, …). `ot` profile is passive-only.

---

## D. Dev / standalone (local testing, no manager, no license)

```bash
cd probe

./dev.sh check 192.168.0.34            # quick reachability first
./dev.sh scan  192.168.0.34            # full assessment (auto-scope), saves /tmp/probe_result.json
./dev.sh facts 192.168.0.34            # scan + pretty fact table
./dev.sh web   192.168.0.34            # only the web branch

# or the raw CLI:
echo "192.168.0.34/32" > scope.txt
python3 -m workflow.cli -t 192.168.0.34 -s scope.txt --mode assessment -o result.json
```

See `probe/HOW_IT_WORKS.md` for the gate-by-gate flow.

---

## The end-to-end picture

```
VENDOR                          CLIENT NETWORK                 MANAGER (cloud)
keygen ───────────────────────────────────────────────────────────────────
build sealed image ──push──► registry
                            client: docker run … hostid ──► (sends id to vendor)
issue license(hostid) ──────► client: curl install.sh ──► probe registers ──► manager
                            probe: scope-checked scan ──raw facts──► detection → findings → dashboard
```
