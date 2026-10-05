# Connecting AI on an AWS instance — step by step

> **Scope:** make Vedha's AI features (AI Brain chat, security briefs, remediation
> guidance, engagement reports, the advisor agent) answer on an EC2 host: which keys to
> create, **exactly where each key goes**, which settings matter, what the instance must be
> able to reach, and how to prove it works. It picks up where
> [AWS Deployment](aws-deployment.md) ends — the stack is up, but AI is not answering.
>
> Design background: [ADR-0004](../adr/0004-ai-fallback-chain.md) (automatic provider chain)
> and [ADR-0003](../adr/0003-bfsi-deployment-and-ai-gateway.md) (deployment profiles,
> pseudonymisation).

**Contents:** [0 Short version](#0-the-short-version) · [1 How it works](#1-how-the-ai-connection-works) ·
[Step 0 Which install](#step-0--which-install-do-you-have) · [Step 1 Create keys](#step-1--create-the-api-keys) ·
[Step 2 Put keys on the host](#step-2--put-the-keys-on-the-instance) · [Step 3 Settings](#step-3--routing-and-privacy-settings-optional) ·
[Step 4 Network](#step-4--let-the-instance-reach-the-providers) · [Step 5 Apply](#step-5--apply-the-change) ·
[Step 6 Verify](#step-6--verify-in-four-levels) · [Troubleshooting](#troubleshooting) ·
[Day-2](#day-2-cost-caps-key-rotation-logs) · [Optional SDK features](#optional-sdk-features-install_extras) ·
[Not supported](#not-supported-today)

---

## 0. The short version

1. **Keys live in one place** — the `.env` file on the EC2 host (or SSM Parameter Store when
   you deploy with `deploy/aws/install.sh`). There is **no key field in the UI**, and the
   browser never sees a key.
2. **Only the backend uses them.** `api` and `worker` (and the one-shot `migrate`) receive
   the keys. The `frontend` container deliberately receives none.
3. **You need a pay-as-you-go API key.** A Claude Pro/Max or ChatGPT Plus subscription has no
   API access and will not work.
4. **Editing `.env` changes nothing until the containers are re-created.**
   `docker compose restart` does not re-read it — use `up -d --force-recreate api worker`
   ([Step 5](#step-5--apply-the-change)).
5. **The instance must reach the provider on TCP 443** — route, security group, NACL, DNS
   ([Step 4](#step-4--let-the-instance-reach-the-providers)).
6. **"configured" is not "working".** `/ai/status` reports `configured: true` for any
   non-empty key, including a placeholder. Prove the connection with the live check in
   [Step 6](#step-6--verify-in-four-levels).

---

## 1. How the AI connection works

```
Browser ──► Next.js frontend ──► FastAPI api ──► AI gateway ──► provider API (HTTPS 443)
            (a proxy: holds no keys,  ▲           │
            makes no model calls)     │           ├─ profile: cloud | hybrid | sovereign
                                      │           └─ chain: anthropic → openai → gemini → groq → openrouter
                                      │                     (a provider with no key is skipped)
.env ─ compose environment ───────────┴──► worker (same code and keys: background jobs)

Redis, shared by every worker, remembers provider health (ai:cool:*), daily spend
(ai:spend:*) and reusable answers (ai:ans:*)
```

- **Automatic chain.** Every key you set joins one chain, premium first. A request goes to the
  first provider that is healthy; one that is out of credit, rate limited, over its daily cap
  or unreachable is skipped and the next answers (the reply is flagged as a *fallback*).
  Nobody picks a provider, so `LLM_PROVIDER` stays empty.
- **Tiers.** Anthropic and OpenAI are *premium*; a billed Gemini key is *budget*; free Gemini,
  Groq and OpenRouter are *free* and are always pseudonymised before they leave the host.
  Customer-facing reports and compliance briefs try premium first; chat accepts any tier.
- **Egress profile (`DEPLOYMENT_PROFILE`).** `cloud` (default) sends raw context to the
  provider, `hybrid` pseudonymises IPs, hostnames, e-mails and accounts first, `sovereign`
  allows a local model only and **ignores every cloud key**.
- **Failure memory.** When a provider fails, every worker is told. Key rejected or out of
  credit: skipped for 1 hour. Provider-side monthly spend limit: skipped until the 1st.
  Rate limit: the provider's `Retry-After` (60 s if absent). Network error or overload: 30 s,
  doubling up to 10 min. Redis persists this across restarts, so **a fixed key can still look
  blocked** until you clear it ([Troubleshooting](#troubleshooting)).

---

## Step 0 — Which install do you have?

Two AWS paths exist in this repo and they keep `.env` in different places. Editing the wrong
one is the most common reason "I added the key and nothing changed".

| | **A. Production installer** | **B. `make full` / `make aws-up`** |
|---|---|---|
| Deployed with | `sudo bash deploy/aws/install.sh` | `make full` (or `make aws-up`) |
| App directory | `/opt/vedha` (sparse clone: `manager/` + `deploy/` only) | your full clone, e.g. `/opt/Project-Vedha` |
| `.env` | `/opt/vedha/.env` | `<clone>/.env` |
| `.env` created by | the installer (chmod 600, plus a managed block) | `scripts/gen-env.sh`, from `.env.docker.example` |
| Secrets from SSM | yes (`/vedha/<NAME>`) | no |
| TLS | Caddy overlay generated by the installer | `make tls`, or the plain-HTTP edge on port 80 |

Not sure which you have?

```bash
ls -d /opt/vedha /opt/Project-Vedha 2>/dev/null
docker inspect vedha-api-1 --format '{{json .Config.Labels}}' \
  | jq -r 'to_entries[] | select(.key|test("compose.project")) | "\(.key)=\(.value)"'
```

### The `vc` helper (used by every command below)

Compose looks for `.env` next to the first `-f` file (`manager/`), **not** in the repo root, so
a bare `docker compose -f manager/docker-compose.yml …` fails with
`required variable POSTGRES_PASSWORD is missing a value`. This helper always passes the right
`--env-file` and picks the same overlay the Makefile would. **Become root first (`sudo -i`)** —
`.env` is `chmod 600` and Docker normally needs root too — then paste this. (`jq` is needed for a
few checks: `dnf install -y jq` or `apt-get install -y jq`.)

```bash
export VEDHA_DIR=/opt/vedha        # Path A.   Path B: export VEDHA_DIR=/opt/Project-Vedha

vc() {
  local root="${VEDHA_DIR:-/opt/vedha}" o
  local f=(-f "$root/manager/docker-compose.yml")
  for o in deploy/tls/docker-compose.tls.yml deploy/aws/docker-compose.prod.yml; do   # Makefile priority
    [ -f "$root/$o" ] && { f+=(-f "$root/$o"); break; }
  done
  docker compose --env-file "$root/.env" "${f[@]}" --profile ui "$@"
}

vc ps        # postgres, redis, api, worker, frontend (and caddy on Path A) should be Up
```

---

## Step 1 — Create the API key(s)

You need **at least one**. Recommended: one premium key (Anthropic) plus one free fallback
(Gemini or Groq), so AI keeps answering when the paid account runs dry.

| Provider | Create it at | Key looks like | Billing | Variable |
|---|---|---|---|---|
| **Anthropic** (Claude) — tried first | console.anthropic.com | `sk-ant-…` | **Required.** Add credit in the Console. Claude Pro/Max is not API access | `ANTHROPIC_API_KEY` |
| **OpenAI** | platform.openai.com | `sk-…` / `sk-proj-…` | **Required.** A key without credit returns HTTP 429 `insufficient_quota` | `OPENAI_API_KEY` |
| **Google Gemini** | aistudio.google.com/apikey | `AIza…` | Free key works. Set `GEMINI_PAID=true` only if the key's Google Cloud project has billing | `GEMINI_API_KEY` |
| **Groq** | console.groq.com | `gsk_…` | Free tier | `GROQ_API_KEY` |
| **OpenRouter** | openrouter.ai/keys | `sk-or-…` | Free via `:free` models | `OPENROUTER_API_KEY` (+ `OPENROUTER_MODEL`, see Step 3) |

Copy the **whole** key the moment it is shown — most consoles show it once. An OpenAI key that
appeared to be missing its `sk-` prefix was one of the causes of the 28 Sep outage
([STATUS.md](../STATUS.md)).

---

## Step 2 — Put the keys on the instance

Pick **one** of 2A, 2B or 2C. 2A works on both paths.

### 2A. In `.env` (both paths)

```bash
cd "$VEDHA_DIR"
cp -p .env ".env.bak-$(date +%F)"      # a copy of what worked; it contains secrets, keep chmod 600
nano .env                               # or vi
```

Set one line per key — no spaces around `=`, no quotes needed, the full value. Replace the
`<…>` placeholders; leave the other lines as shown:

```
ANTHROPIC_API_KEY=<full key starting sk-ant->
# optional free fallback
GEMINI_API_KEY=<full key starting AIza>
# empty = automatic chain
LLM_PROVIDER=
DEPLOYMENT_PROFILE=cloud
```

Keep comments on their own lines — the installer reads key lines with `cut -d= -f2-`, so a
trailing `# …` on a key line would be folded into the saved value.

Check what you actually saved. This prints only the first 7 characters of each key and shows
**every** duplicate — if a key appears twice, the **last** line wins:

```bash
grep -nE '^(ANTHROPIC|OPENAI|GEMINI|GROQ|OPENROUTER)_API_KEY=|^(LLM_PROVIDER|LLM_CHAIN|DEPLOYMENT_PROFILE)=' .env \
  | sed -E 's/(API_KEY=.{7}).*/\1…/'
stat -c '%a %U' .env                    # expect: 600 root
```

If the file was edited on Windows, strip carriage returns: `sed -i 's/\r$//' .env`.

**Path A only — the managed block.** The five key lines sit inside
`# >>> vedha-aws-installer >>>` … `# <<< vedha-aws-installer <<<`. Editing them there is fine: on
every run the installer reads the last value back before rewriting the block, so keys survive.
Everything else in that block is regenerated each run:

- **Do not set `LLM_PROVIDER` by hand.** The installer rewrites it from your *shell* environment
  (empty by default), so a hand edit is silently reverted. To control the order use
  `LLM_CHAIN` instead — it is outside the block and survives re-runs.
- Settings outside the block (`DEPLOYMENT_PROFILE`, `LLM_CHAIN`, `AI_DAILY_CAP_USD`,
  `GEMINI_PAID`, `OPENROUTER_MODEL`, `INSTALL_EXTRAS`, …) persist.

### 2B. In SSM Parameter Store (Path A only)

```bash
read -rsp 'Anthropic key: ' K; echo
aws ssm put-parameter --name /vedha/ANTHROPIC_API_KEY --type SecureString --overwrite --value "$K"
unset K
# same pattern for /vedha/OPENAI_API_KEY, /vedha/GEMINI_API_KEY, /vedha/GROQ_API_KEY, /vedha/OPENROUTER_API_KEY
```

The instance role needs `ssm:GetParameter` + `kms:Decrypt` on `/vedha/*` (policy JSON in
[AWS Deployment §3](aws-deployment.md#option-b--aws-ssm-parameter-store-optional-best-for-fleets--no-secrets-on-disk)).
Know how the installer uses it:

- It reads SSM **once, at install time, on the host**. Containers never call SSM. After you
  change a parameter, re-run the installer (or copy the value into `.env` and re-create the
  containers).
- Precedence: **exported shell variable → SSM → existing `.env`**. An empty SSM value never
  blanks a key already in `.env`.
- **It hides SSM errors.** A missing role, wrong region or wrong parameter name simply yields an
  empty key, and the only trace is the warning `no cloud AI key — AI features inert`. Test by
  hand first — it should print `sk-ant-`:

  ```bash
  aws ssm get-parameter --name /vedha/ANTHROPIC_API_KEY --with-decryption \
    --query Parameter.Value --output text | cut -c1-7
  ```

  If it errors, fix the role, or set the region: `export AWS_DEFAULT_REGION=<your-region>`.

Then run the installer ([Step 5](#step-5--apply-the-change)).

### 2C. Exported variable for one installer run (Path A)

```bash
read -rsp 'Anthropic key: ' ANTHROPIC_API_KEY; echo; export ANTHROPIC_API_KEY
sudo -E RELEASE_REF=<tag-or-sha> bash /opt/vedha/deploy/aws/install.sh   # lab: ALLOW_UNPINNED_RELEASE=1
```

`-E` is required, otherwise `sudo` drops the variable. The installer then writes the value into
`.env`, so it persists. EC2 **user-data**: fetch the key from SSM inside the script — never paste a
literal key there (user-data is readable by anyone who can describe the instance or reach the
metadata service).

### Where **not** to put keys

| Not here | Why |
|---|---|
| Git / the compose files / the Dockerfile | Gitleaks (`secret-scan` workflow) fails the push, and a committed key stays in history and image layers |
| `manager/frontend/.env.local` | That file feeds the operator-local Node CLI only; the deployed stack never reads it |
| `NEXT_PUBLIC_*` or any browser-visible setting | Would ship the key to every user |
| `docker run -e …` / shell history | Leaks to history and `docker inspect` |

---

## Step 3 — Routing and privacy settings (optional)

Defaults are right for a first run: just set a key and skip this step. Put these in `.env`
(outside the Path A managed block).

| Variable | Default | Change it when |
|---|---|---|
| `LLM_PROVIDER` | empty | **Leave empty.** A value is tried first; `ollama` on a host with no Ollama makes the default runtime show "Ollama not reachable" and flags every answer as a fallback |
| `LLM_CHAIN` | empty → `anthropic,openai,gemini,groq,openrouter` | You want another order or fewer providers, e.g. `anthropic,gemini` |
| `DEPLOYMENT_PROFILE` | `cloud` | `hybrid` = pseudonymise before sending. `sovereign` = local model only; **cloud keys are ignored** |
| `AI_PSEUDONYMIZE` | `false` | `true` pseudonymises under `cloud` too |
| `LLM_MODEL` | `claude-sonnet-4-6` | Your Anthropic account cannot use that model id. Must be a valid id for your account; requests naming any other model are refused |
| `OPENAI_MODEL` / `GROQ_MODEL` / `GEMINI_MODEL` | `gpt-4o-mini` / `openai/gpt-oss-120b` / `gemini-flash-latest` | You want a different model on that provider |
| `GEMINI_PAID` | `false` | `true` only when the key's Google Cloud project has billing |
| `OPENROUTER_MODEL` | compose: `openrouter/free` | **Set it explicitly** to a live `:free` id from openrouter.ai/models?max_price=0. `.env.docker.example` says the literal `openrouter/free` is rejected (HTTP 400) |
| `AI_DAILY_CAP_USD` / `AI_MODEL_PRICES` | empty | Cost control — read [Day-2](#day-2-cost-caps-key-rotation-logs); a cap does nothing for an unpriced model |
| `AI_ANSWER_CACHE_TTL_SECONDS` | `604800` | `0` stops identical briefs and report sections being reused |
| `LLM_REQUEST_TIMEOUT_SECONDS` | `180` | A slow egress path |
| `OPENAI_BASE_URL` / `GEMINI_BASE_URL` / `GROQ_BASE_URL` / `OPENROUTER_BASE_URL` | the public URLs | You route through an in-VPC gateway |

**Settings that look configurable but are not forwarded.** `manager/docker-compose.yml` only
passes the variables listed under `x-backend-env` into the containers. These exist in
`app/config.py` but are *not* forwarded, so putting them in `.env` is a silent no-op:
`LLM_EFFORT`, `LLM_MAX_TOKENS`, `LLM_MAX_RETRIES`, `AI_STRICT_QUALITY_FLOOR`, `HTTPS_PROXY`,
`HTTP_PROXY`, `NO_PROXY`. To use one, add it to `x-backend-env` **in the repo** (a PR) —
`install.sh` refuses to deploy a host with locally modified tracked files, so do not hand-edit
the compose file on the server.

---

## Step 4 — Let the instance reach the providers

These are public internet APIs. There are no VPC endpoints for them, so the instance needs a
normal internet path.

| Layer | Must be true |
|---|---|
| Route | Public subnet: `0.0.0.0/0 → igw-…` and a public or Elastic IP. Private subnet: `0.0.0.0/0 → nat-…` |
| Security group | Outbound TCP 443 allowed (the default "allow all outbound" is fine). Provider IPs change — restrict by DNS name only with a firewall or proxy that supports FQDN rules |
| Network ACL | Outbound 443 **and inbound ephemeral ports 1024–65535** (NACLs are stateless) |
| DNS | VPC DNS resolution enabled; the resolver can resolve public names |
| Docker | Containers egress the same way the host does (test from inside `api` below) |

Hosts to allow — only for providers you configured:

| Provider | Host |
|---|---|
| Anthropic | `api.anthropic.com` |
| OpenAI | `api.openai.com` |
| Gemini | `generativelanguage.googleapis.com` |
| Groq | `api.groq.com` |
| OpenRouter | `openrouter.ai` |

**Test from the host, then from inside the `api` container.** No key is needed: *any* HTTP
status — even 401, 403 or 404 — proves the network path works.

```bash
HOSTS="https://api.anthropic.com/v1/messages https://api.openai.com/v1/models \
https://generativelanguage.googleapis.com/v1beta/models https://api.groq.com/openai/v1/models \
https://openrouter.ai/api/v1/models"

# 1) from the host
for u in $HOSTS; do printf '%-58s ' "$u"; curl -sS -m 10 -o /dev/null -w 'HTTP %{http_code}\n' "$u" 2>&1 | tr '\n' ' '; echo; done

# 2) from inside the api container (the path the manager really uses)
vc exec -T api sh -c 'for u in '"$HOSTS"'; do printf "%-58s " "$u"; curl -sS -m 10 -o /dev/null -w "HTTP %{http_code}\n" "$u" 2>&1 | tr "\n" " "; echo; done'
```

| Result | Meaning |
|---|---|
| `HTTP 200/401/403/404/405` | Network is fine |
| `HTTP 000` + `Could not resolve host` | DNS problem (VPC DNS, DHCP options, resolver) |
| `HTTP 000` + `Connection timed out` | No route out: IGW/NAT, security group, NACL |
| `HTTP 000` + `SSL certificate problem` | A TLS-inspecting proxy; the container does not trust its CA (see below) |
| Host works, container fails | Docker networking: `sysctl net.ipv4.ip_forward`, iptables, or a Docker subnet overlapping your VPC range |

**Egress through a proxy or TLS inspection is not supported out of the box:**
`HTTPS_PROXY` and a CA bundle are not forwarded into the containers (see Step 3). Use a NAT
gateway, an in-VPC gateway via the `*_BASE_URL` settings, or add the variables to
`x-backend-env` in the repo.

---

## Step 5 — Apply the change

`docker compose restart` re-uses the environment the container was created with, so it does
**not** pick up a new key. Re-create the containers:

```bash
vc up -d --force-recreate api worker
vc ps
```

`api` is unavailable for up to about a minute while it restarts. `migrate` may run again —
that is expected and safe. The frontend needs no restart; it holds no keys.

Other ways to apply the same change:

| Path | Command |
|---|---|
| A | `sudo -E RELEASE_REF=<tag-or-sha> bash /opt/vedha/deploy/aws/install.sh` (full redeploy: resolves keys from env → SSM → `.env`, rebuilds, runs smoke tests) |
| B | `cd /opt/Project-Vedha && make full` |

Note: `deploy/aws/verify.sh` checks containers, TLS and login but **not AI**, so "all checks
passed" says nothing about AI. Use Step 6.

---

## Step 6 — Verify in four levels

Work top to bottom; stop at the first level that fails.

### 6.1 Did the key reach the container?

Prints a length and the first 7 characters only, and flags the classic mistakes — wrong
prefix, quotes, whitespace:

```bash
vc exec -T api sh -s <<'SH'
chk() {
  v=$(printenv "$1" || true)
  if [ -z "$v" ]; then echo "$1: (empty)"; return; fi
  msg="$1: ${#v} chars, starts '$(printf %s "$v" | cut -c1-7)'"
  case "$v" in "$2"*) ;; *) msg="$msg  <-- expected prefix $2";; esac
  case "$v" in *[[:space:]\"\'\`]*) msg="$msg  <-- contains whitespace or a quote";; esac
  echo "$msg"
}
chk ANTHROPIC_API_KEY sk-ant-
chk OPENAI_API_KEY sk-
chk GEMINI_API_KEY AIza
chk GROQ_API_KEY gsk_
chk OPENROUTER_API_KEY sk-or-
echo
printenv | grep -E '^(LLM_|DEPLOYMENT_PROFILE|AI_|OPENROUTER_MODEL|OLLAMA_BASE_URL)' | sort
SH
```

Every key you set must show a length and the right prefix. `(empty)` for a key you set means
the container never received it: wrong `.env`, not re-created, or a later duplicate line
(Troubleshooting). Check that `LLM_PROVIDER` is empty and `DEPLOYMENT_PROFILE` is `cloud` or
`hybrid`.

### 6.2 What does the manager think — and does a real call work?

Runs inside the container, so it uses exactly the environment and code path the app uses. It
prints no key values and costs a fraction of a cent.

```bash
vc exec -T api python - <<'PY'
import asyncio

from app.config import get_settings
from app.schemas.ai import AiGenerateRequest
from app.services.llm import ManagerLlmService


async def main():
    s = get_settings()
    print("profile =", s.deployment_profile, "| LLM_PROVIDER =", repr(s.llm_provider), "| LLM_CHAIN =", repr(s.llm_chain))
    svc = ManagerLlmService()

    st = await svc.status()
    print("\n1) PROVIDERS  (configured=True only means a non-empty key is present - NOT that it works)")
    for p in st.providers:
        print(f"   {p.id:<13} configured={str(p.configured):<5} model={p.default_model:<24} {p.reason or ''}")

    print("\n2) LIVE CALL  (same code path as AI Brain; a fraction of a cent)")
    req = AiGenerateRequest(
        task="advisor", max_tokens=128,
        messages=[{"role": "user", "content": "Reply with the single word: pong"}],
    )
    try:
        text, rt, fallback = await svc.generate_with_fallback(req)
        print(f"   GENERATE OK -> served by {rt.provider} ({rt.model}) fallback={fallback} reply={text.strip()[:40]!r}")
    except Exception as exc:  # AiRuntimeError carries the operator-readable reason
        print(f"   GENERATE FAILED -> HTTP {getattr(exc, 'status_code', '?')}: {exc}")

    print("\n3) CHAIN AFTER THE CALL  (blocked/cooling + reason = what the call just learned)")
    st = await svc.status()
    if not st.chain:
        print("   (empty) ->", st.reason)
    for c in st.chain:
        print(f"   {c.provider:<11} tier={c.tier:<8} state={c.state:<8} reason={c.reason}")


asyncio.run(main())
PY
```

Healthy:

```
2) LIVE CALL
   GENERATE OK -> served by anthropic (claude-sonnet-4-6) fallback=False reply='pong'
3) CHAIN AFTER THE CALL
   anthropic   tier=premium  state=healthy  reason=None
```

Typical failures (the **Ollama "not reachable" row in section 1 is normal** when you do not use
Ollama — ignore it):

| Output | Go to |
|---|---|
| `GENERATE FAILED -> HTTP 503: no AI provider is configured` and `(empty) -> No cloud AI provider…` | no usable key reached the container → 6.1, Step 2 (or `DEPLOYMENT_PROFILE=sovereign`) |
| `No AI provider could answer — anthropic: API key rejected` · `state=blocked reason=auth` | wrong / placeholder / revoked key → Step 1, 2 |
| `… anthropic: out of credit` · `reason=billing` | add credit → Troubleshooting |
| `… anthropic: unreachable` · `reason=network` | Step 4 |
| `… served by openai … fallback=True` | the first provider is down; read section 3 for why |

### 6.3 Does the real HTTP API agree?

From the host. `/auth/login` returns an `access_token`; `/ai/status` needs it.

```bash
cd "$VEDHA_DIR"
API_PORT=$(grep -m1 '^API_PORT=' .env | cut -d= -f2-); API="http://127.0.0.1:${API_PORT:-18080}"
EMAIL=$(grep -m1 '^SEED_ADMIN_EMAIL=' .env | cut -d= -f2-)
PASS=$(grep -m1 '^SEED_ADMIN_PASSWORD=' .env | cut -d= -f2-)

TOKEN=$(jq -n --arg e "$EMAIL" --arg p "$PASS" '{email:$e,password:$p}' \
  | curl -sS -X POST "$API/auth/login" -H 'Content-Type: application/json' --data-binary @- \
  | jq -r .access_token)

curl -sS "$API/ai/status" -H "Authorization: Bearer $TOKEN" | jq '{provider, model, configured, reason, chain}'
```

Expect `configured: true` and a `chain` whose entries are `"state": "healthy"`. If login
returns `null`, the admin password was changed after install — use the UI (6.4) instead.

### 6.4 In the UI

Sign in → **AI Brain** (`/aibrain`).

- Header shows `RUNTIME  AUTO · ANTHROPIC` (or whichever provider is first). `NOT CONFIGURED`
  means no usable key (6.1).
- The *Automatic AI runtime* card lists the chain. Each row reads `ready`, or the reason it is
  being skipped: `key rejected`, `out of credit`, `monthly spend cap`, `rate limited`,
  `unreachable`, `timed out`.
- Ask a question. The answer shows `Anthropic · claude-sonnet-4-6`. A "fallback" badge means a
  lower provider answered because the first was unavailable.

---

## Troubleshooting

Start with the live check in 6.2 and match its first failing line. The wording below is what
the manager actually emits.

| What you see | What it means | Fix |
|---|---|---|
| `NOT CONFIGURED` · "No cloud AI provider is configured. Set ANTHROPIC_API_KEY, …" | No **usable** key reached `api`: empty, whitespace-only, or a non-ASCII character in it. Also what you see under `DEPLOYMENT_PROFILE=sovereign`, even with keys set | 6.1 shows what the container has. Fix `.env`, then Step 5. If the profile is `sovereign`, set `cloud` or `hybrid` |
| `anthropic: API key rejected` · chain `key rejected` | The provider answered 401/403: wrong, revoked, truncated or placeholder key. The shipped `.env.example` value `your_anthropic_api_key_here` counts as "configured" and is then rejected | Create a new key, paste it whole, Step 5, then **clear the cooldown** (blocked 1 h) |
| `out of credit` | Account has no balance. Anthropic returns 400 "credit balance is too low"; OpenAI returns 429 `insufficient_quota`. A key alone is not enough and subscriptions do not count | Add prepaid credit in the provider console, then clear the cooldown |
| `monthly spend cap` | Provider-side monthly limit reached (Anthropic pauses the API until the 1st) | Raise the limit in the console, then clear the cooldown — otherwise Vedha keeps skipping it until the 1st |
| `rate limited` | Per-minute or tier limit. Vedha honours `Retry-After` (60 s default) and the next provider answers meanwhile | Usually nothing; add a second provider or raise the provider tier |
| `unreachable` | Could not connect: DNS, route, SG/NACL or TLS. Two quick retries, then 30 s cooldown (doubling to 10 min). Logs: `ai.provider.transient_retry … status_code=network` | Step 4 |
| `timed out` | No answer in time. `LLM_REQUEST_TIMEOUT_SECONDS` (180 s) caps one attempt; each task has its own total deadline (90–240 s) | Step 4 tests; check NAT gateway health |
| `<provider>: rejected the request` and the provider still shows `ready` | A 4xx that is not auth/billing/rate-limit: usually a wrong model id (`LLM_MODEL`, `OPENROUTER_MODEL`), or a bad Gemini key (Google typically answers an invalid key with HTTP 400, which Vedha cannot tell apart from a malformed request) | Read the reason: `vc logs --since 15m api \| grep ai.provider.http_error` |
| Default runtime shows "Ollama is not reachable from Manager"; every answer is a fallback | `LLM_PROVIDER=ollama` is pinned but no Ollama runs on the host | Empty `LLM_PROVIDER` (Path A: use `LLM_CHAIN`, see Step 2A), Step 5 |
| Answers carry a *fallback* badge, tier "Free · masked" | Premium providers are blocked or cooling | Section 3 of 6.2 says why |
| "AI advisor unavailable — configure ANTHROPIC_API_KEY or OPENAI_API_KEY" or a report job fails "LLM not configured (set ANTHROPIC_API_KEY)" **while the key is set** | Those two paths call Claude through the `anthropic` Python SDK, which the default lean image does not contain | [Optional SDK features](#optional-sdk-features-install_extras) — or add an OpenAI key (the advisor can use it without the SDK) |
| Changed `.env`, behaviour unchanged | (a) used `restart` instead of `up -d --force-recreate` · (b) edited the other path's `.env` (Step 0) · (c) ran `docker compose` without `--env-file` · (d) a later duplicate line wins (Step 2A grep) · (e) Path A: an exported `ANTHROPIC_API_KEY` in your shell overrode `.env` during the install — `env \| grep API_KEY`, then `unset` | 6.1 shows what the container really has |
| Fixed the key but still `key rejected` / `out of credit` | Redis remembers the failure | Clear cooldowns (below) |
| After re-running `install.sh`, `LLM_PROVIDER` is blank again | It sits in the installer-managed block and is rewritten from your shell environment | Use `LLM_CHAIN`, or `export LLM_PROVIDER=…` for the run |
| "sovereign deployment requires an in-bank model: set LLM_PROVIDER=local_openai …" | `DEPLOYMENT_PROFILE=sovereign` refuses every cloud key by design | Set `cloud` or `hybrid` |
| A key is set but shows `configured=False` | Non-ASCII or whitespace-only value (a `₹` placeholder, a smart quote from a doc editor) | Retype the key by hand; check with 6.1 |
| Installer warned "no cloud AI key" though the SSM parameter exists | The installer hides SSM errors | Test by hand — Step 2B |
| Customer portal shows the assistant locked | A plan lock (`ai_assistant`) on the customer's plan, not a connection fault | Operator: unlock it on that customer's plan |

### Clear the remembered failures

After you fix the cause (new key, added credit, raised limit), forget what Redis remembers.
It is safe: the next request simply re-tests each provider. Spend counters and unrelated keys
are left alone.

```bash
# What is remembered, and for how long (seconds)
vc exec -T redis sh -c 'for k in $(redis-cli --scan --pattern "ai:cool:*"); do echo "$k ttl=$(redis-cli ttl $k) $(redis-cli get $k)"; done'

# Forget every provider's cooldown, strikes and probe lock
vc exec -T redis sh -c 'for p in "ai:cool:*" "ai:strikes:*" "ai:probe:*"; do redis-cli --scan --pattern "$p" | xargs -r redis-cli del; done'

# Optional: also drop reused answers (identical briefs and report sections are cached for 7 days)
vc exec -T redis sh -c 'redis-cli --scan --pattern "ai:ans:*" | xargs -r redis-cli del'
```

Then re-run 6.2.

**Still stuck?** Collect the output of 6.1 and 6.2 (neither contains a key value) and the last
`ai.provider.http_error` lines from the logs, and share those. Never share `.env`,
`docker inspect` or `printenv` output.

**A real example.** The 28 Sep production outage ([STATUS.md](../STATUS.md)) was four of the rows
above at once: `LLM_PROVIDER=ollama` seeded into `.env` with no Ollama running, an Anthropic
account with no credit, an OpenAI key that appeared to be missing its `sk-` prefix, and no Gemini key on the server.
If you are recovering that host, work them in that order, add the Gemini key, then clear the
cooldowns.

---

## Day-2: cost caps, key rotation, logs

### Cost caps

Set the provider-side limit first (Anthropic Console spend limit, OpenAI budget) — it is the
only hard stop. Then add Vedha's own daily cap so a runaway loop steps down the chain instead
of burning the month:

```
AI_DAILY_CAP_USD=anthropic=20,openai=10
AI_MODEL_PRICES=gpt-4o-mini=<input>:<output>
```

**A cap only works for a model that has a price.** Vedha meters spend from each reply's token
usage × a per-model price (USD per 1M tokens, `input:output`); only `claude-sonnet-4-6` is
priced by default. Without a price entry the model is not metered and its cap never triggers
(tested: with the cap `openai=0.01` and no price both calls were served; with
`AI_MODEL_PRICES` set the second call was refused with "openai: daily spend cap reached"). Take
prices from the provider's pricing page, and add an entry whenever you change a model. The day
turns at midnight IST.

### Rotate a key

1. Create the new key at the provider.
2. Update `.env` (Path A with SSM: update the parameter and re-run the installer).
3. `vc up -d --force-recreate api worker`.
4. Verify with 6.2.
5. **Revoke the old key** at the provider.
6. Clear cooldowns if the provider shows blocked.

Rotate immediately if a key was ever pasted into a ticket, chat or log. Error text that echoes
a key is scrubbed before it is logged, but never rely on that. Do not paste `docker inspect`
or `printenv` output anywhere — both print keys.

### Logs and audit

```bash
vc logs --since 30m api worker 2>&1 | grep -E 'ai\.(attempt|provider|gateway|spend|kv)'
```

| Event | Meaning |
|---|---|
| `ai.attempt … outcome=served index=0` | The first provider answered |
| `ai.attempt … outcome=failed detail=auth` (or `billing`, `network`, `rate_limit`, …) | That provider failed and why |
| `ai.provider.http_error … reason=…` | The provider's own error text — the best clue for "rejected the request" |
| `ai.provider.cooldown … seconds=…` | A provider was benched, for how long |
| `ai.gateway.pseudonymized` | Identifiers were masked before sending (hybrid, or a free tier) |
| `ai.kv.redis_unavailable` | Redis was down; each worker kept its own cooldowns (AI still answers) |

Every model call also writes a hash-chained audit row (hashes only, never the prompt). As an
admin, `GET /ai/audit/verify` recomputes the chain.

---

## Optional SDK features (`INSTALL_EXTRAS`)

The default image is **lean** (`INSTALL_EXTRAS=0`). Chat, briefs, remediation guidance,
compliance briefs and engagement reports use plain HTTPS and work on it. Two paths call Claude
through the `anthropic` Python SDK, which only the full image contains:

- the **advisor agent** — otherwise "AI advisor unavailable — configure ANTHROPIC_API_KEY or OPENAI_API_KEY"
  (it can still run on an OpenAI key without the SDK);
- the **per-section report job** — otherwise "LLM not configured (set ANTHROPIC_API_KEY)" when
  Anthropic is your only key.

To enable it: put `INSTALL_EXTRAS=1` in `.env`, then rebuild the backend image — Path A re-run the
installer, Path B `make full` — and verify:

```bash
vc exec -T api python -c "import anthropic; print('anthropic sdk', anthropic.__version__)"
```

The full image also installs the heavy ML, Active Directory and Neo4j libraries: expect a larger
image, a longer build and more disk. Memory use was not measured here — watch `docker stats`
and raise `API_MEM_LIMIT` in `.env` (default `768M`) if the `api` container is OOM-killed. If
you only need the advisor, adding an OpenAI key is the cheaper route.

---

## Not supported today

| You might expect | Reality |
|---|---|
| **Amazon Bedrock**, or an EC2 instance role (IAM) calling a model | There is no Bedrock provider in the code (it appears only as an example region in a design spec). Use an API key |
| Signing in with a Claude Pro/Max or ChatGPT Plus account | Subscriptions have no API access |
| Pasting a key into the UI | Keys are environment only; the UI never receives or stores them |
| Reading keys from SSM or Secrets Manager at runtime | SSM is read only by `install.sh`; for Secrets Manager, export the value before running the installer |
| Egress via `HTTPS_PROXY` or a custom CA | Not forwarded into the containers (Step 3) |

---

## Command cheat sheet

```bash
# as root (sudo -i):  export VEDHA_DIR=/opt/vedha     # Path B: /opt/Project-Vedha — then paste vc() from Step 0

vc ps                                          # container status
nano "$VEDHA_DIR/.env"                         # edit keys
vc up -d --force-recreate api worker           # apply (restart does NOT re-read .env)
# 6.1 key reached container · 6.2 live call · 6.3 HTTP API · 6.4 AI Brain in the UI
vc logs --since 30m api worker 2>&1 | grep -E 'ai\.(attempt|provider|gateway)'
# clear remembered failures: see "Clear the remembered failures"
```

| Where it is wired (maintainers) | |
|---|---|
| `manager/docker-compose.yml` → `x-backend-env` | The allow-list of variables forwarded into `api`, `worker`, `migrate` |
| `manager/backend/app/config.py` | `Settings` — reads the process environment |
| `manager/backend/app/services/llm.py` | `ManagerLlmService`: key check, chain, provider adapters, error wording |
| `manager/backend/app/ai/` | `routing`, `failures`, `health`, `spend`, `gateway`, `kv` |
| `manager/backend/app/routers/ai.py` | `GET /ai/status`, `POST /ai/generate`, `GET /ai/audit/verify` |
| `deploy/aws/install.sh` | §6 SSM, §8 AI keys, §11 the managed `.env` block |
| `scripts/gen-env.sh` | Builds `.env` for Path B |

_Verified 2026-10-05 against `64051cd`: the error wording, routing and cap behaviour above were
produced by running the real `ManagerLlmService` against mocked provider responses, and the
compose behaviour with `docker compose config`. The commands have not yet been run on a live EC2
host._
_Owner: platform. See [`../README.md`](../README.md) for the docs map._
