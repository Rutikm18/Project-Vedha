#!/usr/bin/env bash
# =============================================================================
# gen_mtls_certs.sh — generate mTLS CA + per-probe client certificates.
#
# The manager holds the CA cert/key and trusts probes that present a client
# cert signed by that CA.  Each probe gets a unique client cert + key.
#
# Usage:
#   # One-time: create the CA (on the manager host)
#   ./gen_mtls_certs.sh ca --ca-dir ./ca
#
#   # Per-probe: create a client cert signed by the CA
#   ./gen_mtls_certs.sh client --ca-dir ./ca --agent-id probe-01 --out-dir ./certs/probe-01
#
#   # Then build the probe with these certs:
#   MTLS_DIR=./certs/probe-01 ./build_probe.sh
#
# Output (per probe):
#   mtls_cert.pem   — client certificate (X.509, signed by CA)
#   mtls_key.pem    — client private key (secp256r1)
#   ca_cert.pem     — CA certificate (for the probe to verify the manager)
# =============================================================================
set -euo pipefail

CMD="${1:-}"; shift 2>/dev/null || true

# Parse optional CLI args (override env vars)
while [ $# -gt 0 ]; do
    case "$1" in
        --ca-dir)     CA_DIR="$2"; shift 2 ;;
        --agent-id)   AGENT_ID="$2"; shift 2 ;;
        --out-dir)    OUT_DIR="$2"; shift 2 ;;
        --days)       DAYS_VALID="$2"; shift 2 ;;
        *) shift ;;
    esac
done

CA_DIR="${CA_DIR:-./ca}"
AGENT_ID="${AGENT_ID:-probe-unknown}"
OUT_DIR="${OUT_DIR:-./certs/${AGENT_ID}}"
DAYS_VALID="${DAYS_VALID:-3650}"  # 10 years by default (renew on rotation)

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
say()  { echo -e "${GREEN}[mTLS]${NC} $*"; }
err()  { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }

# ── CA generation ────────────────────────────────────────────────────────────

generate_ca() {
    mkdir -p "$CA_DIR"

    # Generate CA private key (secp256r1 — widely supported, no licensing issues)
    openssl ecparam -genkey -name prime256v1 -noout \
        -out "${CA_DIR}/ca_key.pem"

    # Self-sign CA certificate
    openssl req -new -x509 -key "${CA_DIR}/ca_key.pem" \
        -out "${CA_DIR}/ca_cert.pem" \
        -days "$DAYS_VALID" \
        -subj "/CN=Vedha Scanner CA/O=Vedha/C=US"

    # Set restrictive permissions on the private key
    chmod 600 "${CA_DIR}/ca_key.pem"
    chmod 644 "${CA_DIR}/ca_cert.pem"

    say "CA created:"
    say "  Certificate: ${CA_DIR}/ca_cert.pem"
    say "  Private key: ${CA_DIR}/ca_key.pem  (KEEP SECRET — never embed in probe)"
    say ""
    say "Next: use 'client' command to issue per-probe certificates."
}

# ── Client certificate generation ────────────────────────────────────────────

generate_client() {
    if [ ! -f "${CA_DIR}/ca_key.pem" ] || [ ! -f "${CA_DIR}/ca_cert.pem" ]; then
        err "CA not found at ${CA_DIR}. Run 'ca' command first."
    fi

    mkdir -p "$OUT_DIR"

    # Generate client private key
    openssl ecparam -genkey -name prime256v1 -noout \
        -out "${OUT_DIR}/mtls_key.pem"

    # Create CSR — the Common Name is the agent_id so the manager can
    # extract it from the mTLS cert's Subject CN at connection time
    openssl req -new -key "${OUT_DIR}/mtls_key.pem" \
        -out "${OUT_DIR}/mtls_csr.pem" \
        -subj "/CN=${AGENT_ID}/O=Vedha Probe/C=US"

    # Sign with CA, adding Subject Alternative Name for the agent_id
    openssl x509 -req \
        -in "${OUT_DIR}/mtls_csr.pem" \
        -CA "${CA_DIR}/ca_cert.pem" \
        -CAkey "${CA_DIR}/ca_key.pem" \
        -CAcreateserial \
        -out "${OUT_DIR}/mtls_cert.pem" \
        -days "$DAYS_VALID" \
        -extfile <(printf "subjectAltName=DNS:%s,DNS:%s.probe.internal" "$AGENT_ID" "$AGENT_ID")

    # Copy CA cert so the probe can verify the manager
    cp "${CA_DIR}/ca_cert.pem" "${OUT_DIR}/ca_cert.pem"

    # Clean up CSR (not needed after signing)
    rm -f "${OUT_DIR}/mtls_csr.pem"

    # Set permissions
    chmod 644 "${OUT_DIR}/mtls_cert.pem" "${OUT_DIR}/ca_cert.pem"
    chmod 600 "${OUT_DIR}/mtls_key.pem"

    say "Probe certificate created for '${AGENT_ID}':"
    say "  Certificate:  ${OUT_DIR}/mtls_cert.pem"
    say "  Private key:  ${OUT_DIR}/mtls_key.pem   (embedded in binary)"
    say "  CA cert:      ${OUT_DIR}/ca_cert.pem"
    say ""
    say "Build probe with:"
    say "  MTLS_DIR=${OUT_DIR} ./build_probe.sh"
}

# ── Verify certificates ──────────────────────────────────────────────────────

verify_certs() {
    if [ ! -f "${OUT_DIR}/mtls_cert.pem" ]; then
        err "No certificate at ${OUT_DIR}/mtls_cert.pem. Run 'client' first."
    fi

    say "Verifying certificates..."
    openssl verify -CAfile "${OUT_DIR}/ca_cert.pem" "${OUT_DIR}/mtls_cert.pem" && \
        say "  Certificate chain: VALID" || \
        err "  Certificate chain: INVALID"

    # Verify cert belongs to the agent
    CN=$(openssl x509 -in "${OUT_DIR}/mtls_cert.pem" -noout -subject | grep -o 'CN=[^,]*' | cut -d= -f2)
    say "  Certificate CN: ${CN}"
}

# ── Main dispatch ────────────────────────────────────────────────────────────

case "$CMD" in
    ca)
        generate_ca
        ;;
    client)
        generate_client
        ;;
    verify)
        verify_certs
        ;;
    *)
        echo "Usage: $0 {ca|client|verify}"
        echo ""
        echo "  ca         Generate a new CA certificate and key"
        echo "  client     Generate a per-probe client certificate"
        echo "  verify     Verify an existing client certificate chain"
        echo ""
        echo "Environment variables:"
        echo "  CA_DIR     CA directory (default: ./ca)"
        echo "  AGENT_ID   Probe identifier (default: probe-unknown)"
        echo "  OUT_DIR    Output directory for client certs (default: ./certs/\$AGENT_ID)"
        exit 1
        ;;
esac
