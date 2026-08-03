"""Single source of truth for the deployed application version.

The value is injected at image-build time from the repo-root VERSION file via the
VEDHA_VERSION build arg (see manager/backend/Dockerfile + docker-compose.yml). At
runtime we read the environment first; when it is unset (running straight from a
source checkout, tests, etc.) we fall back to reading the VERSION file by walking
up from this module, and finally to a dev sentinel.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


@lru_cache
def get_version() -> str:
    env = os.getenv("VEDHA_VERSION", "").strip()
    if env:
        return env
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "VERSION"
        if candidate.is_file():
            text = candidate.read_text().strip()
            if text:
                return text
    return "0.0.0-dev"
