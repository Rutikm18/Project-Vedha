#!/usr/bin/env bash
# =============================================================================
# build_probe.sh — 7-phase pipeline: test → compile → bind → sign → verify
#
# Produces a SINGLE native binary (dist/vedha-probe) with:
#   - All Python compiled to machine code (Nuitka --onefile)
#   - Hardware binding (binary only runs on the target machine)
#   - Embedded mTLS client certificate for manager auth
#   - Embedded vendor public key for license verification
#   - Stripped + UPX compressed (optional)
#   - Vendor Ed25519 signature (dist/vedha-probe.sig)
#
# Prerequisites:
#   pip install nuitka[onefile]   (or let --install-deps handle it)
#   export PROBE_LICENSE_PUBKEY=<vendor hex>   (from: tools/issue_license.py keygen)
#   export PROBE_HW_ID=<target machine fingerprint>  (optional; auto-detected)
#
# Usage:
#   ./build_probe.sh                      # build for THIS machine
#   PROBE_HW_ID=abc123 ./build_probe.sh   # build for a SPECIFIC machine
#   SKIP_TESTS=1 ./build_probe.sh         # skip test phase (dangerous)
#   SKIP_UPX=1 ./build_probe.sh           # skip UPX compression
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"

# ── Configuration ────────────────────────────────────────────────────────────
DIST_DIR="${DIST_DIR:-dist}"
BINARY_NAME="${BINARY_NAME:-vedha-probe}"
PROBE_LICENSE_PUBKEY="${PROBE_LICENSE_PUBKEY:-}"
HW_BIND_FINGERPRINT="${PROBE_HW_ID:-}"   # set by user, or auto-detected below
SKIP_TESTS="${SKIP_TESTS:-0}"
SKIP_UPX="${SKIP_UPX:-0}"
MTLS_DIR="${MTLS_DIR:-}"
VENDOR_KEY="${VENDOR_KEY:-tools/vendor_private.key}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
say()  { echo -e "${GREEN}[BUILD]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

# ── Phase 1: TEST ───────────────────────────────────────────────────────────
say "Phase 1/7: Running tests..."

if [ "$SKIP_TESTS" = "1" ]; then
    warn "Tests SKIPPED (SKIP_TESTS=1) — binary may be broken."
else
    python3 -m pytest tests/ -v --tb=short || err "Tests failed. Fix them before building."
    say "  All tests passed."
fi

# ── Phase 2: GATHER HARDWARE FINGERPRINT ─────────────────────────────────────
say "Phase 2/7: Hardware fingerprint..."

if [ -z "$HW_BIND_FINGERPRINT" ]; then
    # Auto-detect: run hw_bind module to get THIS machine's fingerprint
    HW_BIND_FINGERPRINT=$(python3 -c "from agent.hw_bind import get_hw_id; print(get_hw_id())" 2>/dev/null || true)
    if [ -z "$HW_BIND_FINGERPRINT" ]; then
        warn "Could not auto-detect HW fingerprint. Binary will NOT be hardware-bound."
        warn "Set PROBE_HW_ID=<fingerprint> to bind, or LICENSE_ENFORCED=false at runtime."
    else
        say "  Auto-detected HW ID: ${HW_BIND_FINGERPRINT:0:12}…"
    fi
else
    say "  Using provided HW ID: ${HW_BIND_FINGERPRINT:0:12}…"
fi

# ── Phase 3: GENERATE mTLS CERTIFICATES (optional) ───────────────────────────
say "Phase 3/7: mTLS certificates..."

if [ -n "$MTLS_DIR" ] && [ -d "$MTLS_DIR" ]; then
    say "  Using certificates from: $MTLS_DIR"
    MTLS_CERT_DATA="--include-data-files=${MTLS_DIR}/mtls_cert.pem=agent/mtls_cert.pem"
    MTLS_KEY_DATA="--include-data-files=${MTLS_DIR}/mtls_key.pem=agent/mtls_key.pem"
    MTLS_CA_DATA="--include-data-files=${MTLS_DIR}/ca_cert.pem=agent/ca_cert.pem"
    MTLS_FLAGS="$MTLS_CERT_DATA $MTLS_KEY_DATA $MTLS_CA_DATA"
else
    say "  No mTLS certs provided (MTLS_DIR not set). Binary will use Bearer token auth."
    MTLS_FLAGS=""
fi

# ── Phase 4: COMPILE (Nuitka) ────────────────────────────────────────────────
say "Phase 4/7: Compiling with Nuitka (this may take 2-5 minutes)..."

# Ensure Nuitka is available
pip3 install --quiet --upgrade "nuitka[onefile]" 2>/dev/null || true

# Build environment variable flags for Nuitka embedding
ENV_FLAGS=()
if [ -n "$PROBE_LICENSE_PUBKEY" ]; then
    ENV_FLAGS+=("--include-env=PROBE_LICENSE_PUBKEY=$PROBE_LICENSE_PUBKEY")
fi
if [ -n "$HW_BIND_FINGERPRINT" ]; then
    ENV_FLAGS+=("--include-env=HW_BIND_FINGERPRINT=$HW_BIND_FINGERPRINT")
fi

mkdir -p "$DIST_DIR"

python3 -m nuitka \
    --onefile \
    --standalone \
    --output-dir="$DIST_DIR" \
    --output-filename="$BINARY_NAME" \
    --follow-imports \
    --include-package=scanner \
    --include-package=workflow \
    --include-package=agent \
    --include-package=cryptography \
    --include-package=httpx \
    --include-package=websockets \
    ${MTLS_FLAGS:-} \
    "${ENV_FLAGS[@]:-}" \
    --remove-output \
    --assume-yes-for-downloads \
    agent/agent.py

say "  Binary compiled: ${DIST_DIR}/${BINARY_NAME}"
BINARY_SIZE=$(du -h "${DIST_DIR}/${BINARY_NAME}" | cut -f1)
say "  Size: ${BINARY_SIZE}"

# ── Phase 5: STRIP + UPX ────────────────────────────────────────────────────
say "Phase 5/7: Stripping and packing..."

# Strip debug symbols (reduces size ~30%)
strip "${DIST_DIR}/${BINARY_NAME}" 2>/dev/null && say "  Stripped symbols." || warn "  strip not available; skipping."

# UPX compression (reduces size further ~50%)
if [ "$SKIP_UPX" != "1" ]; then
    if command -v upx &>/dev/null; then
        upx --best --quiet "${DIST_DIR}/${BINARY_NAME}" 2>/dev/null && \
            say "  UPX compressed." || \
            warn "  UPX compression failed (binary may already be small)."
    else
        warn "  UPX not installed. Skipping compression. Install: brew install upx"
    fi
fi

FINAL_SIZE=$(du -h "${DIST_DIR}/${BINARY_NAME}" | cut -f1)
say "  Final size: ${FINAL_SIZE}"

# ── Phase 6: SIGN ────────────────────────────────────────────────────────────
say "Phase 6/7: Signing binary..."

if [ -f "$VENDOR_KEY" ]; then
    python3 -c "
import sys; sys.path.insert(0, '.')
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import hashlib

# Read vendor key
priv = Ed25519PrivateKey.from_private_bytes(open('${VENDOR_KEY}', 'rb').read())
# Read and hash the binary
binary_hash = hashlib.sha256(open('${DIST_DIR}/${BINARY_NAME}', 'rb').read()).digest()
# Sign the hash
sig = priv.sign(binary_hash)
with open('${DIST_DIR}/${BINARY_NAME}.sig', 'wb') as f:
    f.write(sig)
print(f'  Signed: ${DIST_DIR}/${BINARY_NAME}.sig')
"
else
    warn "  No vendor key at ${VENDOR_KEY}. Binary NOT signed."
    warn "  Run: python3 tools/issue_license.py keygen  (if vendor)"
fi

# ── Phase 7: VERIFY ──────────────────────────────────────────────────────────
say "Phase 7/7: Verifying binary..."

# Self-test: the binary should print "Self-test passed" and exit 0
if "${DIST_DIR}/${BINARY_NAME}" self-test 2>&1; then
    say "  Self-test PASSED."
else
    err "  Self-test FAILED. The binary may be broken."
fi

# Verify HW bind is embedded (if applicable)
if [ -n "$HW_BIND_FINGERPRINT" ]; then
    # Check the binary contains the fingerprint (embedded as an env var string)
    if strings "${DIST_DIR}/${BINARY_NAME}" | grep -q "$HW_BIND_FINGERPRINT"; then
        say "  HW bind: fingerprint embedded ✓"
    else
        warn "  HW bind: fingerprint NOT found in binary. Check Nuitka --include-env."
    fi
fi

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
say "============================================"
say "  Build complete — ship this single file:"
say "    ${DIST_DIR}/${BINARY_NAME}"
if [ -f "${DIST_DIR}/${BINARY_NAME}.sig" ]; then
    say "  Signature: ${DIST_DIR}/${BINARY_NAME}.sig"
fi
say ""
say "  Run:"
say "    PLATFORM_URL=https://manager:443 \\"
say "      PROBE_LICENSE=<token> \\"
say "      ${DIST_DIR}/${BINARY_NAME}"
say ""
say "  Check host ID:"
say "    ${DIST_DIR}/${BINARY_NAME} hostid"
say "============================================"
