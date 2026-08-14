#!/usr/bin/env bash

# UC — Full TCP Port Scan
#
# Usage:
#   ./uc_full_tcp_scan.sh <IP>
#
# Example:
#   ./uc_full_tcp_scan.sh 192.168.1.68

set -u

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <IP>"
    echo "Example: $0 192.168.1.68"
    exit 1
fi

TARGET="$1"

# Load existing shared UC functions
. "$(dirname "$0")/_uc_lib.sh"

# Full-scan defaults
export RATE="${RATE:-500}"
export CONC="${CONC:-200}"
export TOUT="${TOUT:-2}"

uc_init "$TARGET"

echo "── Full TCP Scan"
echo "   Target      : $TARGET"
echo "   Ports       : 1-65535"
echo "   Rate        : $RATE/sec"
echo "   Concurrency : $CONC"
echo "   Timeout     : ${TOUT}s"
echo

uc_run \
    "Full TCP port scan (1-65535)" \
    port_scanner \
    -p "1-65535"

uc_open "$UC_LAST"