"""
test_runtime_requirements_coverage.py — the probe IMAGE must be able to run every
branch the workflow wires.

`requirements.txt` is the development set; `requirements-runtime.txt` is what the
Dockerfile actually installs into the shipped probe. They drifted: impacket, ldap3
and dnspython were declared in the former and missing from the latter, so
smb_enum_scan / ldap_scan / dns_scan were dispatched on every assessment, failed
with "<pkg> not installed", and were recorded as scanner_errors. Three manager
posture rules (SMB-NULL-SESSION, LDAP-ANONYMOUS-BIND, DNS-ZONE-TRANSFER) became
unreachable from any containerised probe, and every network VA reported
outcome="partial"/degraded=true — training operators to ignore the signal.

Nothing in the code caught it because a missing dependency is handled gracefully:
it degrades instead of crashing. This test makes the drift loud. Same governed-data
discipline as test_two_tree_parity and test_risk_port_coverage: add a dependency to
a scanner and this list must grow with it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_RUNTIME = _ROOT / "requirements-runtime.txt"
_DEV = _ROOT / "requirements.txt"

# Third-party package -> the scanner module that cannot run without it. Every one
# of these backs a branch listed in workflow/branches.py, so the workflow WILL
# dispatch it against any host with the matching port open.
REQUIRED_BY_WIRED_BRANCH = {
    "impacket": "smb_enum_scanner",
    "ldap3": "ldap_scanner",
    "dnspython": "dns_scanner",
    "cryptography": "tls_scanner",
}


def _declared(path: Path) -> set[str]:
    """Package names declared in a requirements file, normalised and lowercased."""
    names: set[str] = set()
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", line)
        if m:
            names.add(m.group(1).lower().replace("_", "-"))
    return names


@pytest.mark.parametrize("package,scanner", sorted(REQUIRED_BY_WIRED_BRANCH.items()))
def test_runtime_image_installs_every_wired_branch_dependency(package, scanner):
    runtime = _declared(_RUNTIME)
    assert package in runtime, (
        f"{package} backs {scanner}, which workflow/branches.py dispatches "
        f"unconditionally, but it is missing from requirements-runtime.txt — the "
        f"file the Dockerfile installs. The branch will fail with "
        f"'{package} not installed' on every scan and degrade the whole run."
    )


def test_runtime_is_a_subset_of_the_development_set():
    """A package shipped in the image but absent from requirements.txt is a
    dependency nothing develops or tests against."""
    missing = _declared(_RUNTIME) - _declared(_DEV)
    assert not missing, f"in requirements-runtime.txt but not requirements.txt: {sorted(missing)}"
