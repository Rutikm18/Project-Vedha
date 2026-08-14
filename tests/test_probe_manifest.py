"""
test_probe_manifest.py — the `agent.agent manifest` command that the seal-parity
CI job diffs between the plaintext build and the sealed native binary.

The manifest must be the ONLY thing on stdout (clean JSON) and stable, so a byte
diff between plaintext and sealed is meaningful. This test guards that contract
on the plaintext side; the CI job (.github/workflows/probe-seal-parity.yml)
guards that Nuitka reproduces it identically.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_PROBE = Path(__file__).resolve().parent.parent


def _manifest() -> dict:
    out = subprocess.run(
        [sys.executable, "-m", "agent.agent", "manifest"],
        cwd=_PROBE, capture_output=True, text=True, timeout=60,
    )
    assert out.returncode == 0, out.stderr
    # stdout must be pure JSON — any stray log line would break the CI diff.
    return json.loads(out.stdout)


def test_manifest_is_clean_parseable_json():
    data = _manifest()
    assert set(data) == {
        "version", "capabilities", "use_cases", "use_case_codes", "intensity_codes",
    }


def test_manifest_surfaces_the_capability_contract():
    data = _manifest()
    # a representative slice — if the seal drops any of these, the diff goes red
    for cap in ("discovery", "full_port_audit", "exposure_matrix", "device_inventory"):
        assert cap in data["capabilities"]
    assert data["use_case_codes"]["80"] == "uc_full_port_audit"
    assert data["use_case_codes"]["81"] == "uc_exposure_matrix"
    assert data["intensity_codes"] == {"1": "light", "2": "standard", "3": "deep"}


def test_manifest_is_deterministic():
    # No host state / time / network — two runs must be byte-identical, which is
    # the whole basis of the sealed-vs-plaintext parity diff.
    assert _manifest() == _manifest()
