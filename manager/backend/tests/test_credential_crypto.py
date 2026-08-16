"""test_credential_crypto.py — symmetric at-rest encryption for recoverable creds."""
from __future__ import annotations

from app.services import credential_crypto as cc


def test_roundtrip_recovers_plaintext():
    token = cc.encrypt_credential("s3cret-Passw0rd!")
    assert token != "s3cret-Passw0rd!"
    assert cc.decrypt_credential(token) == "s3cret-Passw0rd!"


def test_decrypt_none_or_blank_is_none():
    assert cc.decrypt_credential(None) is None
    assert cc.decrypt_credential("") is None


def test_decrypt_garbage_is_none_not_raise():
    # A corrupt/foreign token (e.g. stored before the key existed) must not raise.
    assert cc.decrypt_credential("not-a-valid-fernet-token") is None


def test_ciphertext_varies_but_decrypts_same():
    a = cc.encrypt_credential("pw")
    b = cc.encrypt_credential("pw")
    assert a != b                       # random IV/timestamp per encryption
    assert cc.decrypt_credential(a) == "pw"
    assert cc.decrypt_credential(b) == "pw"
