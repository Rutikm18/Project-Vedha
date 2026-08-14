#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# seal-probe.sh — turn your PLAINTEXT scanners into a sealed, native-binary probe.
#
# The flow you asked for:
#   1) edit your scanners freely in  main_scripts/   (the source of truth)
#   2) run THIS one command
#   3) ship the sealed image — it contains NO Python and NO source, only machine
#      code (Nuitka-compiled), gated by a vendor-signed, host-locked license.
#
# Why this beats "encrypt the .py + a decoder": an encrypted .py must be decrypted
# to run, so it can be dumped from memory. A Nuitka binary has no source to dump —
# the Python is gone, compiled to C → machine code. Only YOU can mint a license
# (the Ed25519 PRIVATE key never leaves this machine); the probe can only verify.
#
# Usage:
#   ./seal-probe.sh                         # floating build (any machine, license-gated)
#   ./seal-probe.sh --hostid <HOST_ID>      # host-locked to one machine's fingerprint
#   HW_BIND_FINGERPRINT=<fp> ./seal-probe.sh
#   MTLS_DIR=/path/to/certs ./seal-probe.sh # also embed mTLS client cert/key/ca
#
# Get a target's HOST_ID first:  docker run --rm vedha-probe:sealed hostid
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"                     # probe/

IMAGE="${SEALED_IMAGE:-vedha-probe:sealed}"
PY="./.venv/bin/python"; [ -x "$PY" ] || PY="python3"

command -v docker >/dev/null || { echo "docker is required (Nuitka build runs in a container)"; exit 1; }

# ── 1. Vendor key (once) — the private half never leaves this machine ─────────
if [ ! -f tools/vendor_private.key ]; then
  echo "→ first run: generating the vendor keypair"
  echo "  tools/vendor_private.key is your MASTER SECRET — it is gitignored; back it"
  echo "  up privately. Anyone with it can mint licenses for your probes."
  "$PY" tools/issue_license.py keygen >/dev/null
fi
PUBKEY="$("$PY" tools/issue_license.py pubkey)"
echo "• vendor public key (baked into the binary): ${PUBKEY:0:16}…"

# ── 2. Sync your edited scanners into the build tree ──────────────────────────
# main_scripts/ is where you work; scanner/ is what the build compiles. Exact
# sync (delete-then-copy) so a module you removed from main_scripts can't linger
# in the shipped binary. The drift-guard test enforces they match at commit time.
rm -f scanner/*.py
cp main_scripts/*.py scanner/
echo "• synced main_scripts/ → scanner/ ($(ls scanner/*.py | wc -l | tr -d ' ') modules)"

# ── 3. Host-lock (optional) ───────────────────────────────────────────────────
HW_FP="${HW_BIND_FINGERPRINT:-}"
if [ "${1:-}" = "--hostid" ] && [ -n "${2:-}" ]; then HW_FP="$2"; fi
if [ -n "$HW_FP" ]; then
  echo "• host-locking to fingerprint ${HW_FP:0:12}… (refuses to run on any other machine)"
else
  echo "• floating build (runs on any machine that presents a valid license)"
fi

# ── 4. Optional mTLS material to embed ────────────────────────────────────────
MTLS_ARGS=()
if [ -n "${MTLS_DIR:-}" ] && [ -f "$MTLS_DIR/probe.crt" ]; then
  MTLS_ARGS+=(
    --build-arg "MTLS_CERT=$(cat "$MTLS_DIR/probe.crt")"
    --build-arg "MTLS_KEY=$(cat "$MTLS_DIR/probe.key")"
    --build-arg "MTLS_CA_CERT=$(cat "$MTLS_DIR/ca.pem")"
  )
  echo "• embedding mTLS client certificate from $MTLS_DIR"
fi

# ── 5. Compile to a native binary (Nuitka, in Docker) ─────────────────────────
echo "→ compiling probe → C → machine code (this takes a few minutes)…"
# NOTE the ${arr[@]+"${arr[@]}"} guard: on macOS bash 3.2, a bare
# "${MTLS_ARGS[@]}" on an EMPTY array under `set -u` aborts with "unbound
# variable". The guard expands to nothing when the array is empty.
docker build -f Dockerfile.sealed -t "$IMAGE" \
  --build-arg PROBE_LICENSE_PUBKEY="$PUBKEY" \
  --build-arg HW_BIND_FINGERPRINT="$HW_FP" \
  ${MTLS_ARGS[@]+"${MTLS_ARGS[@]}"} \
  .

cat <<EOF

✓ sealed image built: $IMAGE
   • no .py / .pyc inside — native machine code only
   • starts only with a valid, unexpired, vendor-signed license$([ -n "$HW_FP" ] && echo " bound to this host")

Next:
  1) get the target host id :  docker run --rm $IMAGE hostid
  2) mint a license         :  $PY tools/issue_license.py issue --hostid <id> --customer "<name>" --days 365
  3) run it                 :  see probe/SEALING.md (mount the license, set PLATFORM_URL)
EOF
