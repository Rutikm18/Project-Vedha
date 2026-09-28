"""
_sealed.py — build-time constants for the sealed (Nuitka-compiled) probe.

This checked-in copy is the UNSEALED default used by the plaintext image and by
development. Dockerfile.sealed overwrites it with tools/write_sealed_consts.py
BEFORE Nuitka compiles, so in a sealed binary these are compiled-in constants.

Why constants and not environment variables: a customer controls `docker run
-e …`. When the licence switch, the vendor public key or the host fingerprint
came from the environment, `-e LICENSE_ENFORCED=false` (or a self-generated key
pair) switched the licence off. A sealed build ignores those variables.
"""
SEALED = False
LICENSE_PUBKEY_HEX = ""
HW_BIND_FINGERPRINT = ""
