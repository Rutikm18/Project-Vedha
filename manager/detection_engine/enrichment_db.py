"""
enrichment_db.py — load the pinned KEV/EPSS snapshots. Same discipline as
vuln_db.py: no network calls here, ever; update_snapshot.py is the only
module that fetches anything.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from update_snapshot import DEFAULT_EPSS_PATH, DEFAULT_KEV_PATH


class KevDB:
    def __init__(self, cve_ids: set[str], fetched_at: str):
        self._cve_ids = cve_ids
        self.fetched_at = fetched_at

    def is_kev(self, cve_id: str) -> bool:
        return cve_id.upper() in self._cve_ids


class EpssDB:
    def __init__(self, scores: dict[str, dict], fetched_at: str):
        self._scores = scores
        self.fetched_at = fetched_at

    def get(self, cve_id: str) -> dict | None:
        """{'epss': float, 'percentile': float} or None if not covered."""
        return self._scores.get(cve_id.upper())


# Same discipline as vuln_db.load_snapshot: the KEV/EPSS snapshots are
# immutable between out-of-band syncs but re-read on every detection run.
# Memoize by (path, mtime, size); an out-of-band re-sync changes mtime/size and
# invalidates automatically.
_kev_cache: dict[tuple[str, int, int], KevDB] = {}
_epss_cache: dict[tuple[str, int, int], EpssDB] = {}
_cache_lock = threading.Lock()


def _clear_caches() -> None:
    """Test hook: drop the memoized KEV/EPSS caches so the next load re-reads."""
    with _cache_lock:
        _kev_cache.clear()
        _epss_cache.clear()


def _cache_key(path: Path) -> tuple[str, int, int]:
    st = path.stat()
    return (str(path.resolve()), st.st_mtime_ns, st.st_size)


def load_kev(path: str | Path = DEFAULT_KEV_PATH) -> KevDB:
    path = Path(path)
    key = _cache_key(path)
    with _cache_lock:
        cached = _kev_cache.get(key)
    if cached is not None:
        return cached
    with path.open() as fh:
        snap = json.load(fh)
    db = KevDB(set(snap["cve_ids"]), snap["fetched_at"])
    with _cache_lock:
        return _kev_cache.setdefault(key, db)


def load_epss(path: str | Path = DEFAULT_EPSS_PATH) -> EpssDB:
    path = Path(path)
    key = _cache_key(path)
    with _cache_lock:
        cached = _epss_cache.get(key)
    if cached is not None:
        return cached
    with path.open() as fh:
        snap = json.load(fh)
    db = EpssDB(snap["scores"], snap["fetched_at"])
    with _cache_lock:
        return _epss_cache.setdefault(key, db)
