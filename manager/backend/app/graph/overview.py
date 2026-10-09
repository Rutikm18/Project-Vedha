"""
overview.py — one engagement's line on the tenant-wide attack-paths overview.

Pure: takes what an engagement's stored analysis holds (see
routers/attack_paths._recompute_and_store) and the labels of the few hosts it names,
and returns the small, flat row the dashboard shows. It never computes anything and
never reads the database, so "what does the overview say?" is testable without one.

Honesty rules the row follows:
  * an engagement nobody has computed paths for is `computed: false` — NOT "0 routes";
    zero routes and "never looked" are different claims;
  * zero routes carries the reasons the analysis recorded (`why_empty`), so an empty
    row is never read as "safe";
  * coverage is reported as the analysis recorded it ("observed" / "partial"), or
    None when the analysis predates the coverage report — never filled in.
"""
from __future__ import annotations

from typing import Any

# How many hosts of the minimum fix set a row names; the rest are counted.
FIX_ASSETS_SHOWN = 3


def fix_asset_ids(analysis: dict[str, Any] | None, shown: int = FIX_ASSETS_SHOWN) -> tuple[list[str], int]:
    """(the first `shown` hosts of the minimum fix set, how many more there are)."""
    fix = ((analysis or {}).get("choke") or {}).get("min_fix_set") or {}
    ids = [str(a) for a in (fix.get("assets") or [])]
    return ids[:shown], max(len(ids) - shown, 0)


def build_row(
    *,
    engagement_id: Any,
    name: str,
    status: Any,
    computed_at: Any = None,
    path_count: int | None = None,
    analysis: dict[str, Any] | None = None,
    labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    """The overview row for one engagement. `analysis is None` = never computed."""
    labels = labels or {}
    row: dict[str, Any] = {
        "engagement_id": str(engagement_id),
        "name": name,
        "status": str(getattr(status, "value", status) or ""),
        "computed": analysis is not None,
        "computed_at": computed_at.isoformat() if computed_at is not None else None,
        "path_count": None,
        "entry_points": None,
        "crown_jewels": None,
        "fix_set_size": None,
        "fix_assets": [],
        "fix_assets_more": 0,
        "coverage": None,
        "stale_assets": None,
        "why_empty": [],
    }
    if analysis is None:
        return row

    choke = analysis.get("choke") or {}
    fix = choke.get("min_fix_set") or {}
    ids, more = fix_asset_ids(analysis)
    paths = int(path_count or 0)
    coverage = analysis.get("coverage") or {}
    freshness = analysis.get("freshness") or {}
    row.update({
        "path_count": paths,
        "entry_points": choke.get("entry_points"),
        "crown_jewels": len(choke.get("targets") or []),
        "fix_set_size": fix.get("size", len(fix.get("assets") or [])),
        "fix_assets": [labels.get(i, i) for i in ids],
        "fix_assets_more": more,
        "coverage": coverage.get("confidence") if coverage else None,
        "stale_assets": freshness.get("stale_assets") if freshness else None,
    })
    if paths == 0:
        reasons = (analysis.get("diagnostics") or {}).get("reasons") or []
        row["why_empty"] = [{"code": r.get("code"), "detail": r.get("detail")} for r in reasons
                            if isinstance(r, dict) and r.get("code")]
    return row


def row_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
    """Engagements with routes first (most routes first), then ones computed with none,
    then ones never computed; ties by name so the order is stable."""
    if not row.get("computed"):
        return (2, 0, str(row.get("name") or "").lower())
    paths = int(row.get("path_count") or 0)
    return (0 if paths > 0 else 1, -paths, str(row.get("name") or "").lower())
