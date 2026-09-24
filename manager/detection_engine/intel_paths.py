"""
intel_paths.py — where the pinned intel snapshots are read from.

Packaged snapshots live next to this module (``snapshots/``). A sovereign
(air-gapped) manager can install newer, signed snapshots from an offline bundle
into ``$VEDHA_INTEL_DIR`` (see manager/backend/app/intel/bundle.py); a file
present there wins over the packaged one. Resolution happens per call, and the
loaders cache by path+mtime, so an imported bundle takes effect on the next
detection run without a restart.
"""
from __future__ import annotations

import os
from pathlib import Path

PACKAGED_DIR = Path(__file__).parent / "snapshots"


def resolve(name: str) -> Path:
    override = os.environ.get("VEDHA_INTEL_DIR", "").strip()
    if override:
        candidate = Path(override) / name
        if candidate.is_file():
            return candidate
    return PACKAGED_DIR / name
