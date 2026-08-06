"""Tests for agent/scope_crypt.py"""
from __future__ import annotations

import pytest

from agent.scope_crypt import (
    generate_identity,
    encrypt_scope,
    decrypt_scope,
    encrypt_scope_b64,
    decrypt_scope_b64,
)


class TestKeyGeneration:
    def test_generates_32_byte_keys(self):
        sk, pk = generate_identity()
        assert len(sk) == 32
        assert len(pk) == 32

    def test_generates_different_keys_each_call(self):
        sk1, pk1 = generate_identity()
        sk2, pk2 = generate_identity()
        assert sk1 != sk2
        assert pk1 != pk2


class TestEncryptDecryptRoundtrip:
    def test_roundtrip_plaintext(self):
        sk, pk = generate_identity()
        scope = b'{"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": ["10.0.0.5/32"]}'
        blob = encrypt_scope(scope, pk)
        decrypted = decrypt_scope(blob, sk)
        assert decrypted == scope

    def test_roundtrip_empty_scope(self):
        sk, pk = generate_identity()
        scope = b'{"scope_cidrs": [], "excluded_cidrs": []}'
        blob = encrypt_scope(scope, pk)
        decrypted = decrypt_scope(blob, sk)
        assert decrypted == scope

    def test_different_recipient_cannot_decrypt(self):
        alice_sk, alice_pk = generate_identity()
        bob_sk, _bob_pk = generate_identity()
        scope = b'{"scope_cidrs": ["10.0.0.0/24"]}'
        blob = encrypt_scope(scope, alice_pk)
        with pytest.raises(ValueError, match="decryption failed|decryption failed"):
            decrypt_scope(blob, bob_sk)

    def test_tampered_blob(self):
        sk, pk = generate_identity()
        scope = b'{"scope_cidrs": ["10.0.0.0/24"]}'
        blob = bytearray(encrypt_scope(scope, pk))
        blob[40] ^= 0xFF  # corrupt a byte in the ciphertext
        with pytest.raises(ValueError, match="tampered|decryption failed"):
            decrypt_scope(bytes(blob), sk)

    def test_too_short_blob(self):
        sk, pk = generate_identity()
        with pytest.raises(ValueError, match="too short"):
            decrypt_scope(b"tooshort", sk)

    def test_different_plaintexts_are_distinct(self):
        sk, pk = generate_identity()
        blob1 = encrypt_scope(b"scope A", pk)
        blob2 = encrypt_scope(b"scope B", pk)
        assert blob1 != blob2  # fresh ephemeral key + nonce each time

    def test_b64_roundtrip(self):
        sk, pk = generate_identity()
        scope = b'{"scope_cidrs": ["10.0.0.0/24"]}'
        blob_b64 = encrypt_scope_b64(scope, pk)
        assert isinstance(blob_b64, str)
        decrypted = decrypt_scope_b64(blob_b64, sk)
        assert decrypted == scope

    def test_multiple_encrypts_different(self):
        """Each encryption uses a fresh ephemeral key, so blobs are different."""
        sk, pk = generate_identity()
        scope = b'{"scope_cidrs": ["10.0.0.0/24"]}'
        blobs = [encrypt_scope(scope, pk) for _ in range(5)]
        # All must be decryptable
        for blob in blobs:
            assert decrypt_scope(blob, sk) == scope
        # They must be different (fresh ephemeral key + nonce each time)
        assert len(set(blobs)) == 5
