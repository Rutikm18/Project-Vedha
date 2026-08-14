#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# seal_parity.sh — prove the SEALED native binary behaves identically to source.
#
# Nuitka compiles Python → machine code; a bad compile can silently drop a module
# or a capability registration. This builds the sealed image and asserts its
# deterministic `manifest` (version + capabilities + use-case/intensity codes)
# equals the plaintext build's. Any drift — or a sealed binary that can't even
# emit clean JSON — fails the check.
#
# Used by `make seal-parity` and .github/workflows/probe-seal-parity.yml so the
# local check and CI run the exact same logic.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")/../probe"

IMAGE="vedha-probe:seal-parity"
PY="./.venv/bin/python"; [ -x "$PY" ] || PY="python3"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

command -v docker >/dev/null || { echo "✗ docker is required (the Nuitka build runs in a container)"; exit 2; }
docker info >/dev/null 2>&1 || { echo "✗ docker daemon is not running"; exit 2; }

echo "→ 1/4  plaintext manifest"
"$PY" -m agent.agent manifest > "$WORK/plain.json"

echo "→ 2/4  building sealed image (Nuitka; a few minutes)…"
[ -f tools/vendor_private.key ] || "$PY" tools/issue_license.py keygen >/dev/null
PUBKEY="$("$PY" tools/issue_license.py pubkey)"
docker build -f Dockerfile.sealed -t "$IMAGE" \
  --build-arg PROBE_LICENSE_PUBKEY="$PUBKEY" . >/dev/null

echo "→ 3/4  sealed smoke (runs with NO source: version / hostid / manifest)"
docker run --rm -e LICENSE_ENFORCED=false "$IMAGE" version
docker run --rm -e LICENSE_ENFORCED=false "$IMAGE" hostid >/dev/null
# Capture ONLY stdout; any stray stdout noise is itself a parity failure below.
docker run --rm -e LICENSE_ENFORCED=false "$IMAGE" manifest > "$WORK/sealed.json"

echo "→ 4/4  parity check (sealed MUST equal plaintext, semantically)"
# Semantic JSON compare — robust to formatting, and it explicitly distinguishes
# "sealed emitted non-JSON" (a broken/noisy binary) from "sealed diverged".
if "$PY" - "$WORK/plain.json" "$WORK/sealed.json" <<'PYEOF'
import json, sys
plain_path, sealed_path = sys.argv[1], sys.argv[2]
try:
    plain = json.load(open(plain_path))
except Exception as exc:
    print(f"plaintext manifest is not valid JSON ({exc}) — build/test issue"); sys.exit(3)
raw = open(sealed_path).read()
try:
    sealed = json.loads(raw)
except Exception as exc:
    print(f"SEALED binary did not emit clean JSON ({exc}). First 500 bytes of its stdout:")
    print(raw[:500]); sys.exit(1)
if plain == sealed:
    sys.exit(0)
pk, sk = set(plain), set(sealed)
if pk != sk:
    print(f"  keys only in plaintext: {sorted(pk - sk)}")
    print(f"  keys only in sealed   : {sorted(sk - pk)}")
for k in sorted(pk & sk):
    if plain[k] != sealed[k]:
        print(f"  [{k}] plaintext={plain[k]!r}")
        print(f"       sealed   ={sealed[k]!r}")
sys.exit(1)
PYEOF
then
  echo "✓ SEAL PARITY OK — the sealed binary matches the source manifest"
else
  echo "✗ SEAL PARITY FAILURE — the sealed binary drifted from source (see above)"
  exit 1
fi
