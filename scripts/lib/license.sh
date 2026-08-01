#!/usr/bin/env bash
# Deterministic container identity and license issuance.
set -Eeuo pipefail

probe_mac_for_name() {
  python3 - "$PROBE_CONTAINER" <<'PY'
import hashlib
import sys

digest = hashlib.sha256(sys.argv[1].encode()).digest()
print("02:42:%02x:%02x:%02x:%02x" % tuple(digest[:4]))
PY
}

probe_collect_identity() {
  local output identity
  PROBE_MAC_ADDRESS=${PROBE_MAC_ADDRESS:-$(probe_mac_for_name)}
  # Use the same default bridge networking as the installed container.
  # uuid.getnode() cannot observe the configured MAC on a network-less
  # container, which would produce an identity that fails at startup.
  output="$(docker run --rm \
    --read-only --cap-drop ALL --security-opt no-new-privileges:true \
    --pids-limit 64 --user 10001:10001 \
    --hostname "$PROBE_CONTAINER" --mac-address "$PROBE_MAC_ADDRESS" \
    "$PROBE_IMAGE" python -c \
    'import json; from agent.license import host_fingerprint; from agent.hw_bind import get_hw_id; print(json.dumps({"hostid":host_fingerprint(),"hwid":get_hw_id()}))' \
    2>&1)" || die "Could not obtain probe identity: $(sanitize_single_line "$output")"
  identity="$(printf '%s\n' "$output" | python3 -c \
    'import json,sys; rows=[x for x in sys.stdin.read().splitlines() if x.strip().startswith("{")]; print(rows[-1] if rows else "")')"
  [[ -n "$identity" ]] || die "Probe identity output did not contain JSON."
  PROBE_HOST_ID="$(printf '%s' "$identity" | python3 -c 'import json,sys; print(json.load(sys.stdin)["hostid"])')"
  PROBE_HW_ID="$(printf '%s' "$identity" | python3 -c 'import json,sys; print(json.load(sys.stdin)["hwid"])')"
  validate_host_id "$PROBE_HOST_ID" || die "Probe Host ID has an unexpected format."
  validate_hw_id "$PROBE_HW_ID" || die "Probe hardware ID has an unexpected format."
  log_ok "Probe Host ID: ${PROBE_HOST_ID:0:12}..."
}

license_public_key_from_vendor_key() {
  local key_file="$VEDHA_ROOT/probe/tools/vendor_private.key"
  [[ -f "$key_file" ]] || return 1
  PROBE_LICENSE_PUBKEY="$(python3 - "$key_file" <<'PY'
import sys
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

private = Ed25519PrivateKey.from_private_bytes(Path(sys.argv[1]).read_bytes())
print(private.public_key().public_bytes(
    serialization.Encoding.Raw,
    serialization.PublicFormat.Raw,
).hex())
PY
)"
  [[ "$PROBE_LICENSE_PUBKEY" =~ ^[a-f0-9]{64}$ ]]
}

license_validate_payload() {
  local token=$1
  LICENSE_TOKEN="$token" EXPECTED_HOST="$PROBE_HOST_ID" python3 - <<'PY'
import base64
import datetime as dt
import json
import os
import sys

try:
    payload = os.environ["LICENSE_TOKEN"].split(".", 1)[0]
    payload += "=" * (-len(payload) % 4)
    data = json.loads(base64.urlsafe_b64decode(payload))
    if data.get("hostid") not in (os.environ["EXPECTED_HOST"], "*"):
        raise ValueError("license Host ID does not match this probe")
    expiry = dt.date.fromisoformat(data["expires"])
    if expiry < dt.date.today():
        raise ValueError(f"license expired on {expiry.isoformat()}")
except Exception as exc:
    print(str(exc), file=sys.stderr)
    sys.exit(1)
PY
}

license_verify_signature() {
  [[ -n "${PROBE_LICENSE_PUBKEY:-}" ]] ||
    die "PROBE_LICENSE_PUBKEY is required to verify an externally supplied license."
  PYTHONPATH="$VEDHA_ROOT/probe" PROBE_LICENSE="$PROBE_LICENSE" \
    PROBE_LICENSE_PUBKEY="$PROBE_LICENSE_PUBKEY" EXPECTED_HOST="$PROBE_HOST_ID" \
    python3 - <<'PY'
import os
from agent.license import verify_license

verify_license(
    os.environ["PROBE_LICENSE"],
    pubkey_hex=os.environ["PROBE_LICENSE_PUBKEY"],
    this_host=os.environ["EXPECTED_HOST"],
)
PY
}

license_issue() {
  local tool="$VEDHA_ROOT/probe/tools/issue_license.py" response
  [[ -f "$tool" ]] || die "License tool is missing: $tool"
  [[ -f "$VEDHA_ROOT/probe/tools/vendor_private.key" ]] ||
    die "Vendor signing key is absent. Run '$tool keygen' on the authorized vendor workstation, or provide VEDHA_PROBE_LICENSE."
  validate_positive_int "$LICENSE_DAYS" || die "License days must be a positive integer."
  response="$(secure_temp_file)"
  if ! python3 "$tool" issue --hostid "$PROBE_HOST_ID" \
    --customer "$CUSTOMER_NAME" --days "$LICENSE_DAYS" > "$response"; then
    die "License issuance failed."
  fi
  PROBE_LICENSE="$(tr -d '\r\n' < "$response")"
  [[ "$PROBE_LICENSE" == *.* ]] || die "License tool returned an invalid token format."
  license_public_key_from_vendor_key ||
    die "Could not derive the public verification key."
  license_validate_payload "$PROBE_LICENSE" ||
    die "Issued license payload is invalid or expired."
  license_verify_signature ||
    die "Issued license signature verification failed."
  log_ok "Issued and verified license for ${PROBE_HOST_ID:0:12}... (${LICENSE_DAYS} days)."
}

license_reuse_volume_token() {
  [[ "${LICENSE_ENFORCED:-}" == "true" ]] || return 1
  [[ -n "${PROBE_LICENSE_PUBKEY:-}" ]] || return 1
  docker volume inspect "$PROBE_STATE_VOLUME" >/dev/null 2>&1 || return 1
  if docker run --rm --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
    --hostname "$PROBE_CONTAINER" \
    --mac-address "$PROBE_MAC_ADDRESS" -v "$PROBE_STATE_VOLUME:/state:ro" \
    -e PUBKEY="$PROBE_LICENSE_PUBKEY" -e HOST_ID="$PROBE_HOST_ID" \
    --entrypoint python "$PROBE_IMAGE" -c \
    'import os; from agent.license import verify_license; token=open("/state/license.token",encoding="utf-8").read().strip(); verify_license(token,pubkey_hex=os.environ["PUBKEY"],this_host=os.environ["HOST_ID"])' \
    >/dev/null 2>&1
  then
    log_ok "Reusing the verified license from the protected Docker volume."
    return 0
  fi
  return 1
}

license_prepare() {
  PROBE_LICENSE=${PROBE_LICENSE:-${VEDHA_PROBE_LICENSE:-}}
  PROBE_LICENSE_PUBKEY=${PROBE_LICENSE_PUBKEY:-${VEDHA_PROBE_LICENSE_PUBKEY:-}}
  LICENSE_DAYS=${LICENSE_DAYS:-365}
  CUSTOMER_NAME=${CUSTOMER_NAME:-Vedha Local Lab}

  if [[ -n "$PROBE_LICENSE" ]]; then
    LICENSE_ENFORCED=true
    license_validate_payload "$PROBE_LICENSE" ||
      die "Supplied license payload is invalid, expired, or for another Host ID."
    license_verify_signature ||
      die "Supplied license signature could not be verified."
    log_ok "Supplied probe license is valid."
    return 0
  fi

  if license_reuse_volume_token; then
    return 0
  fi

  if [[ "${LICENSE_ENFORCED:-}" == "false" ]]; then
    log_warn "Probe licensing is disabled for local development."
    return 0
  fi

  if [[ -f "$VEDHA_ROOT/probe/tools/vendor_private.key" ]]; then
    LICENSE_ENFORCED=true
    license_issue
    return 0
  fi

  if is_local_platform_url "$PLATFORM_URL"; then
    LICENSE_ENFORCED=false
    log_warn "No vendor key is present; using LICENSE_ENFORCED=false for the local development manager."
    return 0
  fi
  die "Remote installation requires VEDHA_PROBE_LICENSE or an authorized vendor signing key."
}

license_store_in_volume() {
  [[ "${LICENSE_ENFORCED:-false}" == "true" ]] || return 0
  if [[ -z "${PROBE_LICENSE:-}" ]]; then
    license_reuse_volume_token ||
      die "License enforcement is enabled but the stored license is unavailable."
    return 0
  fi
  [[ -n "${PROBE_LICENSE:-}" ]] || die "License enforcement is enabled but no license is available."
  probe_prepare_state_volume
  if ! printf '%s' "$PROBE_LICENSE" | docker run --rm -i --network none \
    --read-only --cap-drop ALL --security-opt no-new-privileges:true \
    --pids-limit 64 --user 10001:10001 \
    -v "$PROBE_STATE_VOLUME:/state" --entrypoint python "$PROBE_IMAGE" -c \
    'import os,sys; os.umask(0o077); open("/state/license.token","w",encoding="utf-8").write(sys.stdin.read())'
  then
    die "Could not store the license in the protected probe state volume."
  fi
}
