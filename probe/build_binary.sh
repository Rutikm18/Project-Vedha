#!/usr/bin/env bash
# build_binary.sh — compile the probe to a single NATIVE binary with Nuitka.
# Your Python (scanners, workflow, agent) becomes C → machine code: no .py,
# no readable bytecode ships to the client. Pair with the host-locked license
# (agent/license.py) for anti-copy.
#
#   ./build_binary.sh          → dist/intrynx-probe   (standalone binary)
#
# Embed your vendor public key first (so the binary can verify licenses):
#   export PROBE_LICENSE_PUBKEY=<hex from: python3 tools/issue_license.py keygen>
#   ...or hardcode it in agent/license.py VENDOR_PUBLIC_KEY_HEX before building.
set -euo pipefail
cd "$(dirname "$0")"

python3 -m pip install --quiet --upgrade nuitka

# --onefile: one self-contained executable. --follow-imports: pull in
# scanner/, workflow/, agent/. --include-package: make sure dynamic imports
# (engine dispatch) are bundled. Standard-library only otherwise + httpx +
# cryptography for the license.
python3 -m nuitka \
  --onefile \
  --standalone \
  --output-dir=dist \
  --output-filename=intrynx-probe \
  --follow-imports \
  --include-package=scanner \
  --include-package=workflow \
  --include-package=agent \
  --include-package=cryptography \
  --include-package=httpx \
  --remove-output \
  --assume-yes-for-downloads \
  agent/agent.py

echo ""
echo "Built dist/intrynx-probe — ship this single file. No source/bytecode inside."
echo "Run:   PLATFORM_URL=... PROBE_LICENSE=... ./dist/intrynx-probe"
echo "HostID: ./dist/intrynx-probe hostid"
