#!/usr/bin/env bash
# setup-https.sh — interactive HTTPS setup for a deployed Vedha manager.
#
#   ./setup-https.sh
#
# Asks only what it can't detect (your domain + an email), shows the exact DNS
# records to create, can create them / open the ports itself on AWS, waits for
# DNS, then runs scripts/enable-tls.sh (certificates, HTTPS switch, checks,
# automatic troubleshooting). Safe to re-run; `./setup-https.sh --rollback`
# undoes it. Previous answers are remembered.
set -Eeuo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
TLS=scripts/enable-tls.sh

if [ -t 1 ]; then B=$'\e[1m'; G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; C=$'\e[36m'; N=$'\e[0m'
else B=""; G=""; Y=""; R=""; C=""; N=""; fi
say()  { printf '%s\n' "$*"; }
ok()   { printf '  %s✓%s %s\n' "$G" "$N" "$*"; }
warn() { printf '  %s!%s %s\n' "$Y" "$N" "$*"; }
die()  { printf '\n%s✗ %s%s\n' "$R" "$*" "$N" >&2; exit 1; }
ask()  {  # ask VAR "Question" "default"
  local var="$1" q="$2" def="${3:-}" ans
  if [ -n "$def" ]; then printf '%s?%s %s %s[%s]%s: ' "$C" "$N" "$q" "$Y" "$def" "$N"
  else printf '%s?%s %s: ' "$C" "$N" "$q"; fi
  read -r ans </dev/tty || true
  printf -v "$var" '%s' "${ans:-$def}"
}
yesno() {  # yesno "Question" default(y|n) → 0 for yes
  local q="$1" def="${2:-y}" ans hint="[Y/n]"
  [ "$def" = n ] && hint="[y/N]"
  printf '%s?%s %s %s%s%s: ' "$C" "$N" "$q" "$Y" "$hint" "$N"
  read -r ans </dev/tty || true
  ans="${ans:-$def}"; case "$ans" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}
env_get() { [ -f .env ] && grep -m1 "^$1=" .env | cut -d= -f2- || true; }

[ -f "$TLS" ] || die "Run this from the Vedha repository (missing $TLS). Try: git pull"
case "${1:-}" in
  --rollback) exec bash "$TLS" --rollback ;;
  --status)   exec bash "$TLS" --status ;;
  -h|--help)  sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
esac
[ -t 0 ] || [ -e /dev/tty ] || die "This is interactive. For automation use: make tls DOMAIN=… EMAIL=… TLS_ARGS=--yes"

# Docker access: re-run with sudo automatically if needed (answers are kept).
if ! docker info >/dev/null 2>&1; then
  if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null; then
    say "Docker needs elevated rights here — re-running with sudo…"
    exec sudo -E bash "$0" "$@"
  fi
  die "Docker isn't running. Start it: sudo systemctl start docker — then re-run."
fi

cat <<EOF

${B}Vedha — HTTPS setup${N}
This gives your platform trusted certificates (Let's Encrypt, auto-renewing):
  dashboard + portal  →  https://<your domain>
  API + probes        →  https://api.<your domain>

EOF

# ── 1. questions (only what can't be detected) ─────────────────────────────────
PUBIP="${TLS_PUBLIC_IP:-}"
token="$(curl -fsS -m 2 -X PUT http://169.254.169.254/latest/api/token -H 'X-aws-ec2-metadata-token-ttl-seconds: 60' 2>/dev/null || true)"
[ -z "$PUBIP" ] && [ -n "$token" ] && PUBIP="$(curl -fsS -m 2 -H "X-aws-ec2-metadata-token: $token" http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || true)"
[ -n "$PUBIP" ] || PUBIP="$(curl -fsS -m 4 https://checkip.amazonaws.com 2>/dev/null | tr -d '\n' || true)"
[ -n "$PUBIP" ] || die "Couldn't detect this server's public IP (is it on the internet?)."
ok "This server's public IP: ${B}$PUBIP${N}"

while :; do
  ask DOMAIN "Your domain for the dashboard (e.g. vedha.yourcompany.com)" "$(env_get TLS_DOMAIN)"
  DOMAIN="$(printf '%s' "$DOMAIN" | tr 'A-Z' 'a-z' | sed -E 's#^https?://##; s#/.*##; s/[[:space:]]//g')"
  printf '%s' "$DOMAIN" | grep -qE '^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$' && break
  warn "'$DOMAIN' isn't a valid domain name — enter just the host, like vedha.example.com"
done
ask API_HOST "Host name for the API/probes" "$(env_get TLS_API_HOST | grep . || echo "api.$DOMAIN")"
while :; do
  ask EMAIL "Email for certificate expiry notices" "$(env_get TLS_EMAIL)"
  printf '%s' "$EMAIL" | grep -qE '^[^@ ]+@[^@ ]+\.[^@ ]+$' && break
  warn "Please enter a valid email address."
done

# ── 2. DNS + ports: automatic on AWS where possible ────────────────────────────
ARGS=(--domain "$DOMAIN" --api-host "$API_HOST" --email "$EMAIL" --yes)
HAVE_AWS=0
command -v aws >/dev/null 2>&1 && aws sts get-caller-identity >/dev/null 2>&1 && HAVE_AWS=1

say ""
say "${B}DNS${N} — both names must point to this server:"
say "    $DOMAIN        A   $PUBIP"
say "    $API_HOST    A   $PUBIP"
if [ "$HAVE_AWS" = 1 ] && yesno "Is your domain's DNS hosted in AWS Route 53? (I'll create the records for you)" n; then
  ARGS+=(--route53)
else
  say "  Create those two A records at your DNS provider now (TTL 300)."
  say "  ${Y}Cloudflare users:${N} set them to 'DNS only' (grey cloud)."
fi

say ""
say "${B}Firewall${N} — the EC2 security group must allow inbound TCP 80 and 443 from anywhere."
if [ "$HAVE_AWS" = 1 ]; then
  yesno "Open ports 80 and 443 in the security group automatically if they're closed?" y && ARGS+=(--open-ports)
else
  say "  (AWS CLI not configured on this box — if the check below flags a port, add it in"
  say "   EC2 → Security Groups → Inbound rules: TCP 80 and 443 from 0.0.0.0/0.)"
fi

# ── 3. check first, fixing what can be fixed, waiting for DNS ─────────────────
say ""
say "${B}Checking everything before changing anything…${N}"
CHECK_ARGS=(--check --domain "$DOMAIN" --api-host "$API_HOST")
if ! TLS_FROM_WIZARD=1 bash "$TLS" "${CHECK_ARGS[@]}"; then
  if printf '%s ' "${ARGS[@]}" | grep -qE -- '--route53|--open-ports'; then
    say ""; say "The automatic fixes (Route 53 / security group) run in the next step."
    yesno "Continue and let them fix it?" y || die "Stopped — nothing was changed. Fix the items above and re-run ./setup-https.sh"
  else
    say ""
    if yesno "Fix the items above now and let me re-check when DNS is ready? (I'll wait up to 20 min)" y; then
      ARGS+=(--wait-dns 20)
    else
      die "Stopped — nothing was changed. Re-run ./setup-https.sh when ready."
    fi
  fi
fi

# ── 4. first-time safety: optional trial run on the staging CA ────────────────
if [ -z "$(env_get TLS_DOMAIN)" ] && yesno "Do a no-risk trial first with Let's Encrypt staging (avoids rate limits)?" n; then
  bash "$TLS" "${ARGS[@]}" --staging \
    || die "Trial failed — the cause and fix are listed above. Fix it and re-run ./setup-https.sh (or undo: ./setup-https.sh --rollback)."
  ok "Trial worked — now getting the real, trusted certificates."
fi

# ── 5. go ─────────────────────────────────────────────────────────────────────
say ""
if [ -n "$(env_get TLS_API_HOST)" ] && grep -q "http://$PUBIP" deploy/tls/Caddyfile 2>/dev/null; then
  yesno "Are all probes already re-pointed to https://$API_HOST? (closes the old http://$PUBIP access)" n \
    && ARGS+=(--no-legacy-http)
fi
yesno "Enable HTTPS now?" y || die "Cancelled — nothing was changed."
bash "$TLS" "${ARGS[@]}" || {
  say ""
  say "${Y}Not finished yet — the reason and fix are listed above.${N}"
  say "Caddy keeps retrying by itself. After fixing: ${B}./setup-https.sh --status${N}"
  say "To undo:  ${B}./setup-https.sh --rollback${N}"
  exit 1
}
say ""
ok "All done. Open ${B}https://$DOMAIN${N}"
