"""Canonical integrity checks for recorded evidence content.

The digest covers the exact JSON value stored in ``content``.  A named basis is
persisted beside the digest so a report never treats an opaque legacy hash as
proof that the displayed content is unchanged.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

CANONICAL_SHA256_BASIS = "vedha_canonical_json_v1"


def canonical_evidence_bytes(content: Any) -> bytes | None:
    """Return deterministic UTF-8 JSON bytes, or ``None`` for unsupported data."""
    try:
        encoded = json.dumps(
            content,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return None
    return encoded.encode("utf-8")


def canonical_content_sha256(content: Any) -> str | None:
    encoded = canonical_evidence_bytes(content)
    return hashlib.sha256(encoded).hexdigest() if encoded is not None else None


def verify_canonical_sha256(content: Any, digest: str, basis: str | None) -> bool | None:
    """True/False for the named canonical basis; None means it is unverifiable."""
    if basis != CANONICAL_SHA256_BASIS:
        return None
    expected = canonical_content_sha256(content)
    if expected is None:
        return None
    return hmac.compare_digest(expected, digest.lower())
