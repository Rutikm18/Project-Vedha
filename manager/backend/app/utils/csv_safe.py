"""A spreadsheet must never run exported text as a formula."""
from __future__ import annotations

from typing import Any

_FORMULA_LEAD = ("=", "+", "-", "@", "\t", "\r")


def csv_cell(value: Any) -> Any:
    """None → empty; text that would start a formula gets a leading apostrophe."""
    if value is None:
        return ""
    if isinstance(value, str) and value.startswith(_FORMULA_LEAD):
        return "'" + value
    return value
