"""
license.py — host-locked, vendor-signed anti-copy gate for the probe.

DESIGN (proper asymmetric, not a shared secret):
  - The VENDOR holds an Ed25519 PRIVATE key (kept off every client machine)
    and signs a small license payload binding {customer, hostid, expiry}.
  - The probe embeds only the Ed25519 PUBLIC key (below). It can VERIFY a
    license but can NEVER forge one — extracting the public key from the
    (Nuitka-compiled) binary buys an attacker nothing.
  - The license is bound to a host fingerprint, so a copied probe (or a
    copied license) won't validate on a different machine.

Toggle with LICENSE_ENFORCED=false for dev. Issue licenses with
tools/issue_license.py (vendor-side; needs the private key).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import platform
import uuid
from datetime import date

# Replace with your real vendor public key (hex) — printed by
# `python3 tools/issue_license.py keygen`. The matching private key is the
# vendor's secret and must NEVER ship to a client.
VENDOR_PUBLIC_KEY_HEX = os.environ.get("PROBE_LICENSE_PUBKEY", "")


class LicenseError(Exception):
    def __init__(self, friendly: str):
        super().__init__(friendly)
        self.friendly = friendly


def host_fingerprint() -> str:
    """Stable per-machine ID, derived from hw_bind's hardware fingerprint."""
    from agent.hw_bind import get_hw_id
    return get_hw_id()[:24]  # license uses 24 chars; HW bind uses 32


def short_id() -> str:
    return host_fingerprint()[:12]


def _b64d(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def verify_license(token: str, *, pubkey_hex: str | None = None,
                   this_host: str | None = None) -> dict:
    """Returns the license payload dict if valid; raises LicenseError otherwise.
    Token format: <b64url(payload_json)>.<b64url(signature)>."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature

    pub = (pubkey_hex or VENDOR_PUBLIC_KEY_HEX).strip()
    if not pub:
        raise LicenseError("No vendor public key configured in this probe build.")
    try:
        payload_b64, sig_b64 = token.strip().split(".", 1)
        payload_bytes = _b64d(payload_b64)
        signature = _b64d(sig_b64)
    except (ValueError, Exception):
        raise LicenseError("License is malformed.")

    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub)).verify(signature, payload_bytes)
    except InvalidSignature:
        raise LicenseError("License signature is invalid (not issued by the vendor).")
    except Exception:
        raise LicenseError("License could not be verified.")

    lic = json.loads(payload_bytes.decode())

    host = this_host or host_fingerprint()
    if lic.get("hostid") not in (host, "*"):   # "*" = floating license (not host-locked)
        raise LicenseError(f"This license is not valid for this machine "
                           f"(Host ID {short_id()}). Request a license for this host.")
    if lic.get("expires") and date.fromisoformat(lic["expires"]) < date.today():
        raise LicenseError(f"License expired on {lic['expires']}.")
    return lic


def check_license() -> dict | None:
    """The gate the agent calls at startup. Honors LICENSE_ENFORCED and
    reads the token from PROBE_LICENSE or PROBE_LICENSE_FILE."""
    if os.environ.get("LICENSE_ENFORCED", "true").lower() in ("false", "0", "no"):
        return None
    token = os.environ.get("PROBE_LICENSE", "")
    if not token and os.environ.get("PROBE_LICENSE_FILE"):
        try:
            token = open(os.environ["PROBE_LICENSE_FILE"]).read().strip()
        except OSError:
            pass
    if not token:
        raise LicenseError(f"No license found. This machine's Host ID is "
                           f"{short_id()} — give it to your administrator to get a license.")
    return verify_license(token)


def gauntlet() -> None:
    """Combined startup gauntlet: HW bind → license check. Fails fast.

    This is the first thing the compiled binary runs. If HW binding is
    configured AND license enforcement is on, both must pass. If either
    fails, the binary exits before any network I/O occurs.

    Deployed probes that were compiled with a HW_BIND_FINGERPRINT always
    run this check. Development builds (LICENSE_ENFORCED=false) skip it.
    """
    from agent.hw_bind import check_hw_bind, HWBindError

    try:
        check_hw_bind()
    except HWBindError:
        raise   # let the caller format the message

    try:
        lic = check_license()
    except LicenseError:
        raise

    # If we got here, both checks passed. lic is the license dict or None
    # (None = enforcement off in dev mode). Caller uses it for logging.
