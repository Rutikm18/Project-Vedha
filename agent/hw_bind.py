"""
hw_bind.py — hardware fingerprinting for binary host-locking.

The compiled binary embeds the specific machine's hardware fingerprint at
build time via HW_BIND_FINGERPRINT. At startup get_hw_id() is compared
against the embedded value; a mismatch means the binary was copied to a
different machine and should refuse to run.

Design: deterministic, simple, no external deps (stdlib only).
"""
from __future__ import annotations

import hashlib
import hmac
import os
import platform
import uuid

class HWBindError(RuntimeError):
    """Raised when the binary is running on an unauthorized machine."""


def get_hw_id() -> str:
    """Deterministic per-machine fingerprint built from stable hardware IDs.

    Combines MAC address (uuid.getnode), node hostname, and CPU architecture,
    hashed into a compact 32-hex-char string. This is the same value baked
    into the compiled binary at build time.
    """
    raw = f"{uuid.getnode()}|{platform.node()}|{platform.machine()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def check_hw_bind() -> None:
    """Verify the binary is running on the machine it was compiled for.

    Reads HW_BIND_FINGERPRINT (set by the Nuitka build pipeline). If it
    differs from the actual fingerprint, raises HWBindError and the binary
    must refuse to start.

    When LICENSE_ENFORCED is false (dev mode) or HW_BIND_FINGERPRINT is not
    set, the check is skipped — this allows development without a compiled
    binary.
    """
    expected = os.environ.get("HW_BIND_FINGERPRINT", "")
    if not expected:
        # Dev mode: no binding required when enforcement is off
        if os.environ.get("LICENSE_ENFORCED", "true").lower() in ("false", "0", "no"):
            return
        raise HWBindError(
            "No HW_BIND_FINGERPRINT configured — this binary was not properly "
            "hardware-bound. Set LICENSE_ENFORCED=false for development."
        )
    actual = get_hw_id()
    if not hmac.compare_digest(actual, expected):
        raise HWBindError(
            f"This compiled probe binary is bound to a different machine.\n"
            f"  This host HW ID: {actual[:12]}…\n"
            f"  Expected HW ID:  {expected[:12]}…\n"
            f"The binary cannot run on this machine. Deploy the probe build "
            f"generated specifically for this host, or request a new license."
        )
