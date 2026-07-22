"""
result_spool.py — local result persistence with upload retry.

When the probe completes a job but cannot reach the manager to submit the
result (network partition, manager restart, etc.), the result is persisted
to disk and retried. On startup, any spooled-but-unsubmitted results from
a previous probe run are flushed first.

Design: simple JSON files in a spool directory, one per job_id. The probe
loads them, attempts upload, and removes the file on success.
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Callable

LOG = logging.getLogger("spool")


class ResultSpool:
    """Persists scan results locally and retries failed uploads."""

    def __init__(
        self,
        spool_dir: str | Path,
        max_retries: int = 5,
        retry_delay_sec: float = 15.0,
    ):
        self.spool_dir = Path(spool_dir)
        self.max_retries = max_retries
        self.retry_delay_sec = retry_delay_sec

    # ── Save ──────────────────────────────────────────────────────────────────

    def save(self, job_id: str, payload: dict[str, Any]) -> Path:
        """Atomically write a result payload to the spool directory.

        Returns the spool file path.

        Crash-safety: the payload is written to a temp file, fsync'd, then
        atomically renamed into place (os.replace). A crash mid-write leaves the
        old file intact and only an orphan ``*.tmp`` (ignored by the ``*.json``
        globs). A plain ``write_text`` could leave a truncated, unparseable file
        as the ONLY copy of the result — silent data loss on the next flush.
        """
        self.spool_dir.mkdir(parents=True, exist_ok=True)
        p = self.spool_dir / f"{job_id}.json"
        tmp = self.spool_dir / f"{job_id}.json.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(payload))
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, p)  # atomic on POSIX and Windows
        LOG.debug("spooled result for job %s -> %s", job_id, p)
        return p

    def exists(self, job_id: str) -> bool:
        """Check if a spooled result exists for this job."""
        return (self.spool_dir / f"{job_id}.json").exists()

    def load(self, job_id: str) -> dict[str, Any] | None:
        """Load a previously spooled result, returning None if missing/corrupt."""
        p = self.spool_dir / f"{job_id}.json"
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            LOG.warning("corrupt spool file: %s", p)
            return None

    def remove(self, job_id: str) -> None:
        """Remove the spool file for a successfully uploaded result."""
        (self.spool_dir / f"{job_id}.json").unlink(missing_ok=True)

    # ── Upload with retry ─────────────────────────────────────────────────────

    def submit_with_retry(
        self,
        job_id: str,
        payload: dict[str, Any],
        upload_fn: Callable[[str, dict[str, Any]], bool],
    ) -> bool:
        """Attempt to upload a result with retries and local spool as fallback.

        Args:
            job_id: Scan job ID (used as the spool filename).
            payload: The full result dict to upload.
            upload_fn: A callable(job_id, payload) -> bool that attempts the
                       actual HTTP/WebSocket upload and returns True on success.

        Returns:
            True if the upload succeeded (or was already spooled).
            False if all retries were exhausted — caller should keep the spool.
        """
        # Save locally first (crash-safe: the result is never lost)
        spool_file = self.save(job_id, payload)

        for attempt in range(1, self.max_retries + 1):
            try:
                if upload_fn(job_id, payload):
                    spool_file.unlink(missing_ok=True)
                    LOG.info("result for job %s uploaded (attempt %d)", job_id, attempt)
                    return True
                LOG.warning(
                    "upload attempt %d/%d for job %s rejected by manager",
                    attempt, self.max_retries, job_id,
                )
            except Exception as exc:
                LOG.warning(
                    "upload attempt %d/%d for job %s failed: %s",
                    attempt, self.max_retries, job_id, exc,
                )
            if attempt < self.max_retries:
                time.sleep(self.retry_delay_sec)

        LOG.error(
            "result for job %s spooled at %s after %d failed upload attempts",
            job_id, spool_file, self.max_retries,
        )
        return False

    # ── Flush spool on startup ────────────────────────────────────────────────

    def flush_spool(self, upload_fn: Callable[[str, dict[str, Any]], bool]) -> int:
        """Re-attempt upload of all previously spooled results.

        Called once at probe startup (before entering the main event loop).
        Returns the number of spooled files that were successfully flushed.
        """
        if not self.spool_dir.exists():
            return 0

        flushed = 0
        for p in sorted(self.spool_dir.glob("*.json")):
            job_id = p.stem
            try:
                payload = json.loads(p.read_text())
                if upload_fn(job_id, payload):
                    p.unlink(missing_ok=True)
                    flushed += 1
                    LOG.info("flushed spooled result for job %s", job_id)
            except (OSError, json.JSONDecodeError, Exception):
                LOG.warning("failed to flush spool file %s — will retry later", p)
        return flushed

    @property
    def spool_count(self) -> int:
        """Number of pending (unsubmitted) results in the spool."""
        if not self.spool_dir.exists():
            return 0
        return len(list(self.spool_dir.glob("*.json")))
