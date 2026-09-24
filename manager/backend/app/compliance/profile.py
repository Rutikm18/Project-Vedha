"""
profile.py — an engagement's regulatory profile: which sector the customer is in
and which jurisdictions regulate it. Drives which compliance packs apply and
which domain skill the AI speaks with.

Stored at ``Engagement.rules_of_engagement["profile"]`` (JSONB), so no migration.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

Sector = Literal[
    "generic", "banking", "payments_fintech", "nbfc", "insurance",
    "capital_markets", "healthcare", "government",
]
SECTORS: tuple[str, ...] = Sector.__args__  # type: ignore[attr-defined]

# ISO-style codes; EU is a bloc. GLOBAL is implicit and never stored.
JURISDICTIONS: dict[str, str] = {
    "IN": "India", "EU": "European Union", "UK": "United Kingdom",
    "US": "United States", "SA": "Saudi Arabia", "AE": "United Arab Emirates",
    "SG": "Singapore", "HK": "Hong Kong SAR",
}


class EngagementProfile(BaseModel):
    sector: Sector = "generic"
    jurisdictions: list[str] = Field(default_factory=list, max_length=len(JURISDICTIONS))

    @field_validator("jurisdictions")
    @classmethod
    def _known_codes(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for code in v:
            c = code.strip().upper()
            if c not in JURISDICTIONS:
                raise ValueError(f"unknown jurisdiction '{code}'")
            if c not in out:
                out.append(c)
        return out


def profile_from_roe(roe: dict | None) -> EngagementProfile:
    """The stored profile, or the generic/global default when absent or invalid
    (a malformed profile must never break an AI or compliance request)."""
    raw = (roe or {}).get("profile") if isinstance(roe, dict) else None
    if not isinstance(raw, dict):
        return EngagementProfile()
    try:
        return EngagementProfile(**raw)
    except ValidationError:
        return EngagementProfile()
