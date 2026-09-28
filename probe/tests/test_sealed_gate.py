"""
A sealed build must not be switchable from `docker run -e …`: the licence is
always enforced, and the vendor key and host fingerprint are compiled-in
constants. Unsealed (dev / plaintext image) behaviour is unchanged.
"""
from __future__ import annotations

import base64
import importlib.util
import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from agent import _sealed, hw_bind, license as lic

_TOOLS = Path(__file__).resolve().parent.parent / "tools" / "write_sealed_consts.py"
_spec = importlib.util.spec_from_file_location("write_sealed_consts", _TOOLS)
wsc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wsc)


def _keypair():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
    return priv, pub


def _token(priv, **payload) -> str:
    body = json.dumps(payload).encode()
    b = lambda x: base64.urlsafe_b64encode(x).decode().rstrip("=")
    return f"{b(body)}.{b(priv.sign(body))}"


@pytest.fixture
def sealed(monkeypatch):
    priv, pub = _keypair()
    monkeypatch.setattr(_sealed, "SEALED", True)
    monkeypatch.setattr(_sealed, "LICENSE_PUBKEY_HEX", pub)
    monkeypatch.setattr(_sealed, "HW_BIND_FINGERPRINT", "")
    return priv


class TestSealedIgnoresEnvironment:
    def test_license_enforced_false_is_ignored(self, sealed, monkeypatch):
        monkeypatch.setenv("LICENSE_ENFORCED", "false")
        monkeypatch.delenv("PROBE_LICENSE", raising=False)
        monkeypatch.delenv("PROBE_LICENSE_FILE", raising=False)
        with pytest.raises(lic.LicenseError, match="No license"):
            lic.check_license()

    def test_customer_supplied_pubkey_cannot_sign_a_licence(self, sealed, monkeypatch):
        attacker, attacker_pub = _keypair()
        monkeypatch.setenv("PROBE_LICENSE_PUBKEY", attacker_pub)
        monkeypatch.setenv("PROBE_LICENSE", _token(attacker, hostid="*", expires="2099-01-01"))
        with pytest.raises(lic.LicenseError, match="signature is invalid"):
            lic.check_license()

    def test_vendor_licence_still_verifies(self, sealed, monkeypatch):
        monkeypatch.setenv("PROBE_LICENSE", _token(sealed, hostid="*", expires="2099-01-01",
                                                   customer="acme"))
        assert lic.check_license()["customer"] == "acme"

    def test_fingerprint_from_env_is_ignored(self, monkeypatch, sealed):
        monkeypatch.setattr(_sealed, "HW_BIND_FINGERPRINT", "0" * 32)   # bound elsewhere
        monkeypatch.setenv("HW_BIND_FINGERPRINT", hw_bind.get_hw_id())  # attacker's override
        monkeypatch.setenv("LICENSE_ENFORCED", "false")
        with pytest.raises(hw_bind.HWBindError, match="different machine"):
            hw_bind.check_hw_bind()

    def test_floating_sealed_build_skips_hw_bind(self, sealed):
        hw_bind.check_hw_bind()     # empty compiled fingerprint = not host-locked


class TestUnsealedUnchanged:
    def test_dev_switch_still_works(self, monkeypatch):
        monkeypatch.setattr(_sealed, "SEALED", False)
        monkeypatch.setenv("LICENSE_ENFORCED", "false")
        assert lic.check_license() is None


class TestWriteSealedConsts:
    def test_renders_valid_python_with_the_values(self):
        pub = "ab" * 32
        ns: dict = {}
        exec(wsc.render(pub, "cd" * 16), ns)
        assert ns["SEALED"] is True
        assert ns["LICENSE_PUBKEY_HEX"] == pub and ns["HW_BIND_FINGERPRINT"] == "cd" * 16

    @pytest.mark.parametrize("pub,fp", [
        ("", ""), ("ab" * 31, ""), ("zz" * 32, ""),
        ("ab" * 32, "123"), ("ab" * 32, "'; import os; os.system('x') #" + "a" * 2),
    ])
    def test_rejects_bad_or_injected_values(self, pub, fp):
        with pytest.raises(ValueError):
            wsc.render(pub, fp)

    def test_checked_in_copy_is_unsealed(self):
        src = (Path(__file__).resolve().parent.parent / "agent" / "_sealed.py").read_text()
        assert "SEALED = False" in src
