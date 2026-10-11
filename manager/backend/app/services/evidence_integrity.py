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

# Keys the manager stamps ONTO an evidence item as chain-of-custody or provenance
# metadata, rather than observed scanner content. They are excluded from the
# integrity digest for two reasons: the digest cannot cover itself (``sha256`` /
# ``sha256_basis``), and ``scan_provenance`` advances after the fact — the outbox
# worker fills its ``detection_run_id`` once the detection run exists — so a digest
# that covered it would break on every legitimate link. ``captured_at`` moves on
# each re-stamp, and ``dedup_key`` is a manager routing key, so both are custody
# metadata too. The digest therefore proves the OBSERVED content is unchanged.
_CUSTODY_KEYS = frozenset(
    {
        "sha256",
        "sha256_basis",
        "captured_at",
        "captured_by",
        "source_host",
        "scan_provenance",
        "dedup_key",
        "signals",          # manager roll-up of merged producers; rebuilt every detection run
    }
)
_CONTENT_KEYS = ("content", "output", "value")


def content_for_integrity(content: Any) -> Any:
    """Return ``content`` with top-level custody/provenance keys removed.

    Only the outermost mapping is filtered: a nested value legitimately named
    ``source_host`` is observed content and is preserved. Non-mappings pass
    through unchanged.
    """
    if isinstance(content, dict):
        return {key: value for key, value in content.items() if key not in _CUSTODY_KEYS}
    return content


def extract_integrity_content(item: Any) -> Any:
    """Mirror the report's artifact-content extraction, then strip custody keys.

    A stamp and its later verification must hash the SAME value. The report
    displays ``item[content|output|value]`` when present, else the whole item;
    this reproduces that choice so both sides agree on the digested bytes.
    """
    if isinstance(item, dict):
        for key in _CONTENT_KEYS:
            if key in item:
                return content_for_integrity(item[key])
        return content_for_integrity(item)
    return item


def item_content_sha256(item: Any) -> str | None:
    """Canonical digest of an evidence item's observed content, or ``None``."""
    return canonical_content_sha256(extract_integrity_content(item))


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
