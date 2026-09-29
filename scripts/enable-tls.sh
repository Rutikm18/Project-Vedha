#!/usr/bin/env bash
# enable-tls.sh — one command: HTTPS for an already-deployed Vedha manager.
#
#   make tls DOMAIN=vedha.example.com EMAIL=you@example.com
#   (or)  bash scripts/enable-tls.sh --domain vedha.example.com --email you@example.com
#
# What it does, in order (every step checks itself and explains any failure):
#   1. Pre-flight: Docker + the running stack, the server's public IP (EC2 IMDSv2),
#      that ports 80/443 are reachable from the internet (security group), DNS
#      (A records, CAA, Cloudflare-proxy detection). Optional auto-fixes:
#        --route53     create/update the two A records in Route 53
#        --open-ports  open inbound 80/443 in the instance's security group
#   2. Replaces the plain-HTTP port-80 "edge" proxy with a Caddy TLS proxy on
#      80/443. Caddy obtains Let's Encrypt certificates (ZeroSSL fallback),
#      redirects HTTP→HTTPS and renews automatically (~30 days before expiry).
#        https://DOMAIN        → dashboard + customer portal
#        https://api.DOMAIN    → API + probes (REST and WSS)
#   3. Switches the app to HTTPS: secure cookies, MANAGER_PUBLIC_URL, CORS, and
#      binds API/dashboard ports to 127.0.0.1 so HTTPS can't be bypassed.
#   4. Verifies the real certificate end to end; on failure reads Caddy's log
#      and names the cause (DNS, blocked port, rate limit, CAA, proxy…) + fix.
#
# Other modes:
#   --check      diagnose only, change nothing
#   --status     certificate issuer / expiry / renewal for both hosts
#   --rollback   restore the previous .env and the plain-HTTP edge proxy
#
# Options:
#   --api-host HOST       default api.DOMAIN (must also resolve to this server)
#   --staging             Let's Encrypt staging CA (test without rate limits;
#                         browsers will NOT trust it — rerun without it after)
#   --no-legacy-http      stop serving the API on http://<server-ip> (keep it
#                         until every probe is re-pointed to https://api.DOMAIN)
#   --wait-dns MINUTES    how long to wait for DNS to point here (default 10)
#   --yes                 don't ask for confirmation
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT/.env"
TLS_DIR="$ROOT/deploy/tls"
CADDYFILE="$TLS_DIR/Caddyfile"
OVERLAY="$TLS_DIR/docker-compose.tls.yml"
BACKUP_DIR="$TLS_DIR/backup"
BASE_COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$ROOT/manager/docker-compose.yml")

DOMAIN="" EMAIL="" API_HOST="" MODE="apply" STAGING=0 LEGACY_HTTP=1
ROUTE53=0 OPEN_PORTS=0 WAIT_DNS=10 ASSUME_YES=0 DRY_RUN="${TLS_DRY_RUN:-0}"

# ── output ────────────────────────────────────────────────────────────────────
if [ -t 1 ]; then B=$'\e[1m'; G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; D=$'\e[2m'; N=$'\e[0m'
else B=""; G=""; Y=""; R=""; D=""; N=""; fi
step() { printf '\n%s▶ %s%s\n' "$B" "$*" "$N"; }
ok()   { printf '  %s✓%s %s\n' "$G" "$N" "$*"; }
warn() { printf '  %s!%s %s\n' "$Y" "$N" "$*"; WARNINGS=$((WARNINGS + 1)); }
bad()  { printf '  %s✗%s %s\n' "$R" "$N" "$*"; PROBLEMS=$((PROBLEMS + 1)); }
fix()  { printf '    %s→ fix:%s %s\n' "$B" "$N" "$*"; }
info() { printf '  %s%s%s\n' "$D" "$*" "$N"; }
die()  { printf '\n%s✗ %s%s\n' "$R" "$*" "$N" >&2; exit 1; }
WARNINGS=0 PROBLEMS=0

usage() { sed -n '2,37p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --domain) DOMAIN="${2:-}"; shift 2 ;;
    --email) EMAIL="${2:-}"; shift 2 ;;
    --api-host) API_HOST="${2:-}"; shift 2 ;;
    --staging) STAGING=1; shift ;;
    --no-legacy-http) LEGACY_HTTP=0; shift ;;
    --route53) ROUTE53=1; shift ;;
    --open-ports) OPEN_PORTS=1; shift ;;
    --wait-dns) WAIT_DNS="${2:-10}"; shift 2 ;;
    --check) MODE="check"; shift ;;
    --status) MODE="status"; shift ;;
    --rollback) MODE="rollback"; shift ;;
    --yes|-y) ASSUME_YES=1; shift ;;
    -h|--help) usage 0 ;;
    *) printf 'Unknown option: %s\n\n' "$1" >&2; usage 1 ;;
  esac
done

# ── helpers ───────────────────────────────────────────────────────────────────
env_get() { [ -f "$ENV_FILE" ] && grep -m1 "^$1=" "$ENV_FILE" | cut -d= -f2- || true; }
env_set() {  # idempotent KEY=VALUE upsert, keeps file mode 600
  local k="$1" v="$2" tmp
  tmp="$(mktemp "$ENV_FILE.XXXXXX")"; chmod 600 "$tmp"
  if grep -q "^$k=" "$ENV_FILE" 2>/dev/null; then
    awk -v k="$k" -v v="$v" -F= 'BEGIN{OFS="="} $1==k {print k"="v; next} {print}' "$ENV_FILE" > "$tmp"
  else
    cat "$ENV_FILE" > "$tmp"; printf '%s=%s\n' "$k" "$v" >> "$tmp"
  fi
  mv "$tmp" "$ENV_FILE"
}
valid_host() { printf '%s' "$1" | grep -qE '^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$'; }
valid_ip()   { printf '%s' "$1" | grep -qE '^([0-9]{1,3}\.){3}[0-9]{1,3}$'; }

imds() {  # EC2 instance metadata (IMDSv2); empty off EC2
  local token
  token="$(curl -fsS -m 2 -X PUT 'http://169.254.169.254/latest/api/token' \
    -H 'X-aws-ec2-metadata-token-ttl-seconds: 120' 2>/dev/null || true)"
  [ -n "$token" ] || return 0
  curl -fsS -m 2 -H "X-aws-ec2-metadata-token: $token" \
    "http://169.254.169.254/latest/meta-data/$1" 2>/dev/null || true
}

public_ip() {
  local ip="${TLS_PUBLIC_IP:-}"
  [ -n "$ip" ] || ip="$(imds public-ipv4)"
  [ -n "$ip" ] || ip="$(curl -fsS -m 4 https://checkip.amazonaws.com 2>/dev/null | tr -d '\n' || true)"
  valid_ip "$ip" && printf '%s' "$ip" || true
}

# Public DNS view via DNS-over-HTTPS (not the VPC resolver, which can differ).
doh() {  # doh NAME TYPE → one answer per line (Answer section, that type only)
  local name="$1" type="$2" code out
  case "$type" in A) code=1 ;; CAA) code=257 ;; *) code="" ;; esac
  out="$(curl -fsS -m 6 -H 'accept: application/dns-json' \
    "https://cloudflare-dns.com/dns-query?name=${name}&type=${type}" 2>/dev/null || true)"
  [ -n "$out" ] || out="$(curl -fsS -m 6 "https://dns.google/resolve?name=${name}&type=${type}" 2>/dev/null || true)"
  # Only the Answer array: a missing record comes back with the zone's SOA in
  # "Authority", which must not be mistaken for an answer.
  printf '%s' "$out" | tr -d '\n' | sed -n 's/.*"Answer": *\[\([^]]*\)\].*/\1/p' \
    | sed 's/}, *{/}\
{/g' | grep -E "\"type\": *${code}[,}]" \
    | grep -oE '"data": *"([^"\\]|\\.)*"' | sed -E 's/"data": *"(.*)"/\1/; s/\\"/"/g' || true
}
resolve_a() { doh "$1" A | grep -E '^([0-9]{1,3}\.){3}[0-9]{1,3}$' || true; }

# Cloudflare's proxy ranges (the "orange cloud") — a proxied record breaks ACME.
cloudflare_ip() {
  case "$1" in
    104.1[6-9].*|104.2[0-9].*|104.3[01].*|172.6[4-9].*|172.7[01].*|188.114.9[6-9].*|\
    162.15[89].*|173.245.*|103.21.24[4-7].*|103.22.20[0-3].*|103.31.[4-7].*|141.101.*|\
    108.162.*|190.93.*|197.234.24[0-3].*|198.41.*) return 0 ;;
  esac
  return 1
}

compose_tls() { "${BASE_COMPOSE[@]}" -f "$OVERLAY" "$@"; }
tls_container() { compose_tls ps -q tls 2>/dev/null | head -1; }
http_code() { curl -s -o /dev/null -w '%{http_code}' --max-time "${2:-8}" "$1" 2>/dev/null || true; }

confirm() {
  [ "$ASSUME_YES" = 1 ] && return 0
  [ -t 0 ] || die "Not interactive — rerun with --yes to proceed."
  printf '\n%s%s%s [y/N] ' "$B" "$1" "$N"; read -r reply
  case "$reply" in y|Y|yes|YES) return 0 ;; *) die "Cancelled — nothing was changed." ;; esac
}

# ── diagnostics: turn Caddy/ACME log lines into a cause and a fix ─────────────
explain_acme_log() {
  local log="$1" found=0
  if printf '%s' "$log" | grep -qiE 'timeout during connect|connection refused|Fetching http://[^ ]*/\.well-known'; then
    bad "Let's Encrypt could not reach this server on port 80 (HTTP challenge)."
    fix "Open inbound TCP 80 from 0.0.0.0/0 in the EC2 security group (and any network ACL) — or rerun with --open-ports."
    found=1
  fi
  if printf '%s' "$log" | grep -qiE 'NXDOMAIN|no valid A records|DNS problem|SERVFAIL'; then
    bad "Let's Encrypt could not resolve the domain in public DNS."
    fix "Create A records for $DOMAIN and $API_HOST → $PUBIP (or rerun with --route53), then wait for propagation."
    found=1
  fi
  if printf '%s' "$log" | grep -qiE 'Invalid response|unauthorized|urn:ietf:params:acme:error:unauthorized'; then
    bad "The domain answered, but not from this server (DNS points elsewhere, or a CDN/proxy is in front)."
    fix "Point both A records straight at $PUBIP. On Cloudflare set them to 'DNS only' (grey cloud)."
    found=1
  fi
  if printf '%s' "$log" | grep -qiE 'rateLimited|too many (certificates|failed authorizations|new orders)'; then
    bad "Let's Encrypt rate limit hit (too many recent attempts for this domain)."
    fix "Wait (limits reset within hours), and test with --staging first. Caddy also retries via ZeroSSL automatically."
    found=1
  fi
  if printf '%s' "$log" | grep -qiE 'caa'; then
    bad "A CAA DNS record forbids the certificate authority."
    fix "Add CAA records: 0 issue \"letsencrypt.org\" and 0 issue \"sectigo.com\" (ZeroSSL), or remove the CAA record."
    found=1
  fi
  if printf '%s' "$log" | grep -qiE 'address already in use|bind: '; then
    bad "Another process is already using port 80 or 443."
    fix "Find it: sudo ss -ltnp '( sport = :80 or sport = :443 )' — stop it (e.g. nginx/httpd), then rerun."
    found=1
  fi
  [ "$found" = 1 ] || { warn "No known ACME error pattern in the log. Last lines:"; printf '%s\n' "$log" | tail -15 | sed 's/^/      /'; }
}

# ── modes ─────────────────────────────────────────────────────────────────────
status() {
  local host="${1}" out issuer until
  out="$(echo | openssl s_client -connect "$host:443" -servername "$host" 2>/dev/null \
         | openssl x509 -noout -issuer -enddate 2>/dev/null || true)"
  if [ -z "$out" ]; then bad "$host: no certificate served on :443"; return; fi
  issuer="$(printf '%s' "$out" | sed -nE 's/^issuer=.*O ?= ?([^,]*).*/\1/p')"
  until="$(printf '%s' "$out" | sed -n 's/^notAfter=//p')"
  ok "$host — issuer: ${issuer:-unknown}, valid until: $until (Caddy renews automatically)"
}

rollback() {
  step "Rolling back HTTPS"
  local last; last="$(ls -1t "$BACKUP_DIR"/env.* 2>/dev/null | head -1 || true)"
  [ -n "$last" ] || die "No backup found in $BACKUP_DIR — nothing to roll back."
  confirm "Restore $(basename "$last") and switch back to plain HTTP on port 80?"
  [ -f "$OVERLAY" ] && compose_tls rm -sf tls >/dev/null 2>&1 || true
  cp "$last" "$ENV_FILE"; chmod 600 "$ENV_FILE"
  mv "$OVERLAY" "$OVERLAY.disabled" 2>/dev/null || true
  "${BASE_COMPOSE[@]}" --profile edge --profile ui up -d --remove-orphans
  ok "Restored $(basename "$last"); edge proxy back on port 80. Certificates are kept in the caddy volume."
  exit 0
}

# ── argument validation ───────────────────────────────────────────────────────
[ "$MODE" = rollback ] && rollback
if [ "$MODE" = status ]; then
  DOMAIN="${DOMAIN:-$(env_get TLS_DOMAIN)}"; API_HOST="${API_HOST:-$(env_get TLS_API_HOST)}"
  [ -n "$DOMAIN" ] || die "No TLS domain configured yet. Run: make tls DOMAIN=... EMAIL=..."
  step "Certificates"; status "$DOMAIN"; status "$API_HOST"; exit 0
fi

DOMAIN="$(printf '%s' "${DOMAIN:-$(env_get TLS_DOMAIN)}" | tr 'A-Z' 'a-z' | sed -E 's#^https?://##; s#/.*##')"
[ -n "$DOMAIN" ] || die "Missing --domain. Example: make tls DOMAIN=vedha.example.com EMAIL=you@example.com"
valid_host "$DOMAIN" || die "'$DOMAIN' is not a valid domain name (give the bare host, e.g. vedha.example.com)."
API_HOST="$(printf '%s' "${API_HOST:-api.$DOMAIN}" | tr 'A-Z' 'a-z')"
valid_host "$API_HOST" || die "'$API_HOST' is not a valid host name."
EMAIL="${EMAIL:-$(env_get TLS_EMAIL)}"
if [ "$MODE" = apply ]; then
  [ -n "$EMAIL" ] || die "Missing --email (Let's Encrypt sends expiry warnings there)."
  printf '%s' "$EMAIL" | grep -qE '^[^@ ]+@[^@ ]+\.[^@ ]+$' || die "'$EMAIL' is not a valid email address."
fi

# ── 1. pre-flight ─────────────────────────────────────────────────────────────
step "Pre-flight"
[ -f "$ENV_FILE" ] || die ".env not found at $ENV_FILE — deploy first with: make full"
command -v curl >/dev/null || die "curl is required."
command -v openssl >/dev/null || warn "openssl missing — certificate details will be skipped (sudo dnf install -y openssl)."
if [ "$DRY_RUN" != 1 ]; then
  command -v docker >/dev/null || die "Docker is not installed."
  docker info >/dev/null 2>&1 || die "Docker isn't running or you lack permission (try: sudo systemctl start docker, or run with sudo)."
  docker compose version >/dev/null 2>&1 || die "Docker Compose v2 is required (docker compose …)."
  if [ -z "$("${BASE_COMPOSE[@]}" ps -q api 2>/dev/null)" ]; then
    bad "The Vedha stack isn't running."; fix "Start it first: make full"; exit 1
  fi
  ok "Docker and the Vedha stack are running"
fi

PUBIP="$(public_ip)"
[ -n "$PUBIP" ] || die "Could not detect this server's public IPv4 (set TLS_PUBLIC_IP=… to override)."
ok "Public IP: $PUBIP"

# Security group: ports 80 (ACME challenge + redirect) and 443 (HTTPS).
SG_IDS=""
if command -v aws >/dev/null 2>&1 && [ "$DRY_RUN" != 1 ]; then
  MAC="$(imds mac)"; REGION="$(imds placement/region)"
  [ -n "$MAC" ] && SG_IDS="$(imds "network/interfaces/macs/$MAC/security-group-ids" | tr '\n' ' ')"
  if [ -n "$SG_IDS" ] && [ -n "$REGION" ]; then
    for port in 80 443; do
      open="$(aws ec2 describe-security-groups --region "$REGION" --group-ids $SG_IDS \
        --query "SecurityGroups[].IpPermissions[?FromPort<=\`$port\` && ToPort>=\`$port\`].IpRanges[].CidrIp" \
        --output text 2>/dev/null || echo "?")"
      if [ "$open" = "?" ]; then
        warn "Couldn't read the security group (no IAM permission) — checking port $port by probing instead."
      elif printf '%s' "$open" | grep -q '0.0.0.0/0'; then
        ok "Security group allows TCP $port from anywhere"
      elif [ "$OPEN_PORTS" = 1 ] && [ "$MODE" = apply ]; then
        sg="${SG_IDS%% *}"
        aws ec2 authorize-security-group-ingress --region "$REGION" --group-id "$sg" \
          --ip-permissions "IpProtocol=tcp,FromPort=$port,ToPort=$port,IpRanges=[{CidrIp=0.0.0.0/0,Description=vedha-https}]" \
          >/dev/null 2>&1 && ok "Opened TCP $port in $sg" || bad "Could not open TCP $port in $sg (IAM: ec2:AuthorizeSecurityGroupIngress)"
      else
        bad "Security group does not allow TCP $port from 0.0.0.0/0 (Let's Encrypt validates from many IPs)."
        fix "EC2 → Security Groups → $SG_IDS → Inbound: add TCP $port from 0.0.0.0/0 — or rerun with --open-ports."
      fi
    done
  fi
fi
# Probe port 80 from outside-in (hairpin through the public IP exercises the SG).
if [ "$DRY_RUN" != 1 ]; then
  code="$(http_code "http://$PUBIP/health" 6)"
  case "$code" in
    2*|3*|4*) ok "Port 80 answers on the public IP (HTTP $code)" ;;
    *) warn "Port 80 on $PUBIP didn't answer from here — if Let's Encrypt fails, the security group/NACL is the likely cause." ;;
  esac
  if command -v ss >/dev/null 2>&1; then
    holder="$(ss -ltnpH '( sport = :443 )' 2>/dev/null | grep -v docker-proxy | head -1 || true)"
    [ -z "$holder" ] || { bad "Port 443 is used by a non-Docker process: $holder"; fix "Stop it (e.g. sudo systemctl stop nginx httpd) and rerun."; }
  fi
fi

# DNS: both names must resolve (in public DNS) straight to this server.
if [ "$ROUTE53" = 1 ] && [ "$MODE" = apply ]; then
  step "Route 53"
  command -v aws >/dev/null || die "--route53 needs the AWS CLI (and IAM route53:ChangeResourceRecordSets)."
  zone_id="" zone_name=""; probe="$DOMAIN"
  while [ -z "$zone_id" ] && printf '%s' "$probe" | grep -q '\.'; do
    read -r zone_id zone_name < <(aws route53 list-hosted-zones-by-name --dns-name "$probe." --max-items 1 \
      --query "HostedZones[?Name=='$probe.' && Config.PrivateZone==\`false\`].[Id,Name]" --output text 2>/dev/null || true) || true
    probe="${probe#*.}"
  done
  [ -n "$zone_id" ] || die "No public Route 53 hosted zone found for $DOMAIN. Create the A records at your DNS provider instead."
  changes=""
  for h in "$DOMAIN" "$API_HOST"; do
    changes="$changes{\"Action\":\"UPSERT\",\"ResourceRecordSet\":{\"Name\":\"$h.\",\"Type\":\"A\",\"TTL\":60,\"ResourceRecords\":[{\"Value\":\"$PUBIP\"}]}},"
  done
  change_id="$(aws route53 change-resource-record-sets --hosted-zone-id "${zone_id##*/}" \
    --change-batch "{\"Comment\":\"vedha tls\",\"Changes\":[${changes%,}]}" --query ChangeInfo.Id --output text)" \
    || die "Route 53 update failed (IAM route53:ChangeResourceRecordSets on $zone_name)."
  info "Waiting for Route 53 to apply…"
  aws route53 wait resource-record-sets-changed --id "$change_id" && ok "A records set in $zone_name → $PUBIP"
fi

step "DNS"
check_dns() {  # 0 = both names point here
  local h ips all=0
  for h in "$DOMAIN" "$API_HOST"; do
    ips="$(resolve_a "$h" | xargs)"
    if printf ' %s ' "$ips" | grep -q " $PUBIP "; then
      [ "$(printf '%s' "$ips" | wc -w)" -gt 1 ] && warn "$h also resolves to other IPs ($ips) — remove the extra A records." || true
      ok "$h → $PUBIP"
    elif [ -z "$ips" ]; then
      all=1; [ "${1:-}" = quiet ] || { bad "$h has no A record in public DNS yet."; fix "Create: $h  A  $PUBIP  (TTL 300) — or rerun with --route53."; }
    else
      all=1
      if [ "${1:-}" != quiet ]; then
        first="${ips%% *}"
        if cloudflare_ip "$first"; then
          bad "$h resolves to Cloudflare's proxy ($ips) — certificates can't be issued through it."
          fix "In Cloudflare DNS set $h to 'DNS only' (grey cloud) pointing at $PUBIP."
        else
          bad "$h points to $ips, not this server ($PUBIP)."
          fix "Change the A record for $h to $PUBIP (an old Elastic IP? a load balancer?)."
        fi
      fi
    fi
  done
  return "$all"
}
if ! check_dns; then
  if [ "$MODE" = apply ] && [ "$WAIT_DNS" -gt 0 ] && [ "$DRY_RUN" != 1 ]; then
    info "Waiting up to $WAIT_DNS min for DNS to propagate (checks every 20s)…"
    deadline=$(( $(date +%s) + WAIT_DNS * 60 ))
    until check_dns quiet; do
      [ "$(date +%s)" -lt "$deadline" ] || die "DNS still doesn't point here after $WAIT_DNS min. Fix the records above, then rerun."
      sleep 20
    done
    PROBLEMS=0; check_dns
  fi
fi
caa="$(doh "$DOMAIN" CAA | xargs)"
if [ -n "$caa" ] && ! printf '%s' "$caa" | grep -qiE 'letsencrypt|sectigo'; then
  bad "CAA records ($caa) don't allow Let's Encrypt or ZeroSSL."
  fix "Add CAA: 0 issue \"letsencrypt.org\" (and 0 issue \"sectigo.com\")."
fi

if [ "$MODE" = check ]; then
  step "Result"
  if [ "$PROBLEMS" -eq 0 ]; then
    if [ -n "${TLS_FROM_WIZARD:-}" ]; then ok "Ready for HTTPS."
    else ok "Ready for HTTPS. Run: make tls DOMAIN=$DOMAIN EMAIL=<you@example.com>"; fi
  else printf '  %s%d problem(s) to fix first (see above).%s\n' "$R" "$PROBLEMS" "$N"; fi
  exit $(( PROBLEMS > 0 ))
fi
[ "$PROBLEMS" -eq 0 ] || die "$PROBLEMS pre-flight problem(s) — fix them (see → fix lines) and rerun. Nothing was changed."

# ── 2. write the Caddy config ─────────────────────────────────────────────────
step "Writing TLS configuration"
mkdir -p "$TLS_DIR" "$BACKUP_DIR"
ACME_CA=""
[ "$STAGING" = 1 ] && ACME_CA="    acme_ca https://acme-staging-v02.api.letsencrypt.org/directory"
LEGACY=""
if [ "$LEGACY_HTTP" = 1 ]; then
  LEGACY="# Legacy: probes still configured with http://$PUBIP keep working until
# they're re-pointed to https://$API_HOST. Remove with --no-legacy-http.
http://$PUBIP {
    reverse_proxy api:8000
}"
fi
cat > "$CADDYFILE.tmp" <<EOF
# Generated by scripts/enable-tls.sh — rerun it to change; don't edit by hand.
{
    email $EMAIL
$ACME_CA
    # Certificates: Let's Encrypt, automatic ZeroSSL fallback, auto-renewal.
}

(secure) {
    encode zstd gzip
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
        -Server
    }
}

$DOMAIN {
    import secure
    header X-Frame-Options "SAMEORIGIN"
    reverse_proxy frontend:3000 {
        header_up X-Real-IP {remote_host}
    }
}

$API_HOST {
    import secure
    # REST and the probes' WSS (/agents/ws) — WebSockets are proxied natively.
    reverse_proxy api:8000 {
        header_up X-Real-IP {remote_host}
    }
}

$LEGACY
EOF
mv "$CADDYFILE.tmp" "$CADDYFILE"
cat > "$OVERLAY" <<EOF
# Generated by scripts/enable-tls.sh — HTTPS ingress (replaces the port-80 edge).
services:
  tls:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "443:443/udp"
    volumes:
      - $CADDYFILE:/etc/caddy/Caddyfile:ro
      - vedha_tls_data:/data
      - vedha_tls_config:/config
    depends_on:
      api:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "caddy", "validate", "--config", "/etc/caddy/Caddyfile"]
      interval: 60s
      timeout: 10s
      retries: 3
    logging:
      driver: json-file
      options: {max-size: "10m", max-file: "3"}
volumes:
  vedha_tls_data:
  vedha_tls_config:
EOF
ok "Wrote $CADDYFILE"
ok "Wrote $OVERLAY"

if [ "$DRY_RUN" = 1 ]; then
  info "TLS_DRY_RUN=1 — stopping before any change to Docker or .env."
  exit 0
fi

docker run --rm -v "$CADDYFILE:/etc/caddy/Caddyfile:ro" caddy:2-alpine \
  caddy validate --config /etc/caddy/Caddyfile >/dev/null 2>&1 \
  && ok "Caddy configuration is valid" || die "Generated Caddyfile failed validation — please report this."

cat <<EOF

  ${B}About to switch this server to HTTPS:${N}
    Dashboard / portal  https://$DOMAIN
    API / probes        https://$API_HOST
    Certificates        Let's Encrypt$( [ "$STAGING" = 1 ] && echo ' STAGING (untrusted — test only)' ) · auto-renew
    Plain http://$PUBIP  $( [ "$LEGACY_HTTP" = 1 ] && echo 'API kept for existing probes' || echo 'closed' )
    Ports 3000 / API    bound to 127.0.0.1 (no HTTPS bypass)
EOF
confirm "Proceed?"

# ── 3. app config (.env) — backed up first, so --rollback can restore it ──────
step "Switching the app to HTTPS"
cp "$ENV_FILE" "$BACKUP_DIR/env.$(date +%Y%m%d-%H%M%S)"; chmod 600 "$BACKUP_DIR"/env.*
env_set TLS_DOMAIN "$DOMAIN"
env_set TLS_API_HOST "$API_HOST"
env_set TLS_EMAIL "$EMAIL"
env_set AUTH_COOKIE_SECURE true
env_set MANAGER_PUBLIC_URL "https://$API_HOST"
env_set CORS_ORIGINS "https://$DOMAIN,https://$API_HOST"
env_set API_BIND 127.0.0.1
env_set FRONTEND_BIND 127.0.0.1
ok ".env updated (backup in deploy/tls/backup/)"

# The old port-80 edge proxy must release the port before Caddy takes it.
"${BASE_COMPOSE[@]}" --profile edge rm -sf edge >/dev/null 2>&1 || true
compose_tls --profile ui up -d --remove-orphans api frontend tls \
  || die "docker compose failed to start the stack — see the output above."
ok "HTTPS proxy started; api/frontend restarted with the new settings"

# ── 4. verify the real certificate ────────────────────────────────────────────
step "Obtaining certificates (usually under a minute)"
deadline=$(( $(date +%s) + 240 )); got=0
while [ "$(date +%s)" -lt "$deadline" ]; do
  # --resolve pins the name to this box, so we test the cert, not hairpin routing.
  if curl -fsS -o /dev/null --max-time 8 --resolve "$API_HOST:443:127.0.0.1" "https://$API_HOST/health" 2>/dev/null \
     && curl -fsS -o /dev/null --max-time 8 --resolve "$DOMAIN:443:127.0.0.1" "https://$DOMAIN/" 2>/dev/null; then
    got=1; break
  fi
  [ "$STAGING" = 1 ] && curl -ksS -o /dev/null --max-time 8 --resolve "$API_HOST:443:127.0.0.1" "https://$API_HOST/health" 2>/dev/null \
    && { got=2; break; }
  sleep 6
done

if [ "$got" = 0 ]; then
  bad "Certificates were not obtained within 4 minutes."
  explain_acme_log "$(docker logs "$(tls_container)" 2>&1 | tail -200 || true)"
  printf '\n  Caddy keeps retrying on its own. After fixing the cause: %smake tls-status%s\n' "$B" "$N"
  printf '  To undo everything: %smake tls-rollback%s\n' "$B" "$N"
  exit 1
fi
if [ "$got" = 2 ]; then warn "Staging certificates issued (not browser-trusted). Rerun without --staging for real ones."
else ok "Trusted certificates issued and served"; fi
command -v openssl >/dev/null && { status "$DOMAIN"; status "$API_HOST"; }

# Outside-in reachability of 443 (security group), without failing the run.
code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 "https://$API_HOST/health" 2>/dev/null || true)"
[ "$code" = 200 ] && ok "https://$API_HOST reachable via the public IP" \
  || warn "https://$API_HOST didn't answer via the public IP from here — make sure TCP 443 is open to 0.0.0.0/0."

step "Done"
cat <<EOF
  Dashboard / portal : ${B}https://$DOMAIN${N}
  API / probes       : ${B}https://$API_HOST${N}   (health: https://$API_HOST/health)
  Renewal            : automatic (Caddy). Check any time: make tls-status

  Re-point existing probes (on each probe host):
    ./install.sh https://$API_HOST        # or set PLATFORM_URL=https://$API_HOST in probe.env
$( [ "$LEGACY_HTTP" = 1 ] && printf '  When every probe is moved: make tls DOMAIN=%s EMAIL=%s TLS_ARGS=--no-legacy-http\n' "$DOMAIN" "$EMAIL" )
  Undo               : make tls-rollback
EOF
[ "$WARNINGS" -eq 0 ] || printf '\n  %s%d warning(s) above — worth a look.%s\n' "$Y" "$WARNINGS" "$N"
