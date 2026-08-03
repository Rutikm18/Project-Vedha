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
import re
import time
from pathlib import Path
from typing import Any, Callable

LOG = logging.getLogger("spool")
_SAFE_JOB_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
PERMANENT_REJECTION = "permanent_rejection"


class ResultSpool:
    """Persists scan results locally and retries failed uploads."""

    def __init__(
        self,
        spool_dir: str | Path,
        max_retries: int = 5,
        retry_delay_sec: float = 15.0,
        max_bytes: int = 512 << 20,
        max_files: int = 1024,
    ):
        self.spool_dir = Path(spool_dir)
        self.max_retries = max_retries
        self.retry_delay_sec = retry_delay_sec
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        if max_files <= 0:
            raise ValueError("max_files must be positive")
        self.max_bytes = max_bytes
        self.max_files = max_files

    # ── Save ──────────────────────────────────────────────────────────────────

    def _path(self, job_id: str) -> Path:
        if (
            not isinstance(job_id, str)
            or not _SAFE_JOB_ID.fullmatch(job_id)
            or ".." in job_id
        ):
            raise ValueError(f"invalid job ID for result spool: {job_id!r}")
        return self.spool_dir / f"{job_id}.json"

    def _sync_directory(self) -> None:
        if os.name != "posix" or not self.spool_dir.exists():
            return
        directory_fd = os.open(self.spool_dir, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)

    def save(self, job_id: str, payload: dict[str, Any]) -> Path:
        """Atomically write a result payload to the spool directory.

        Returns the spool file path.

        Crash-safety: the payload is written to a temp file, fsync'd, then
        atomically renamed into place (os.replace). A crash mid-write leaves the
        old file intact and only an orphan ``*.tmp`` (ignored by the ``*.json``
        globs). A plain ``write_text`` could leave a truncated, unparseable file
        as the ONLY copy of the result — silent data loss on the next flush.
        """
        p = self._path(job_id)
        self.spool_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        if os.name == "posix":
            os.chmod(self.spool_dir, 0o700)
        tmp = p.with_suffix(".json.tmp")
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        fd = os.open(tmp, flags, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(payload))
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, p)  # atomic on POSIX and Windows
        self._sync_directory()
        LOG.debug("spooled result for job %s -> %s", job_id, p)
        return p

    def exists(self, job_id: str) -> bool:
        """Check if a spooled result exists for this job."""
        return self._path(job_id).exists()

    def load(self, job_id: str) -> dict[str, Any] | None:
        """Load a previously spooled result, returning None if missing/corrupt."""
        p = self._path(job_id)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            LOG.warning("corrupt spool file: %s", p)
            return None

    def remove(self, job_id: str) -> None:
        """Remove the spool file for a successfully uploaded result."""
        self._path(job_id).unlink(missing_ok=True)
        self._sync_directory()

    def quarantine(self, job_id: str) -> Path:
        """Move a terminally rejected result out of the retry queue."""
        source = self._path(job_id)
        rejected_dir = self.spool_dir / "rejected"
        rejected_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        if os.name == "posix":
            os.chmod(rejected_dir, 0o700)
        destination = rejected_dir / source.name
        os.replace(source, destination)
        self._sync_directory()
        return destination

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
                outcome = upload_fn(job_id, payload)
                if outcome == PERMANENT_REJECTION:
                    destination = self.quarantine(job_id)
                    LOG.error(
                        "result for job %s permanently rejected; quarantined at %s",
                        job_id, destination,
                    )
                    return False
                if outcome is True:
                    self.remove(job_id)
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
                self._path(job_id)
                payload = json.loads(p.read_text())
                outcome = upload_fn(job_id, payload)
                if outcome == PERMANENT_REJECTION:
                    destination = self.quarantine(job_id)
                    LOG.error(
                        "spooled result for job %s permanently rejected; quarantined at %s",
                        job_id, destination,
                    )
                elif outcome is True:
                    self.remove(job_id)
                    flushed += 1
                    LOG.info("flushed spooled result for job %s", job_id)
            except Exception:
                LOG.warning("failed to flush spool file %s — will retry later", p)
        return flushed

    @property
    def spool_count(self) -> int:
        """Number of pending (unsubmitted) results in the spool."""
        if not self.spool_dir.exists():
            return 0
        return len(list(self.spool_dir.glob("*.json")))

    @property
    def spool_bytes(self) -> int:
        """Total bytes held by pending result files, ignoring vanished files."""
        if not self.spool_dir.exists():
            return 0
        total = 0
        for path in self.spool_dir.glob("*.json"):
            try:
                total += path.stat().st_size
            except OSError:
                continue
        return total

    @property
    def at_capacity(self) -> bool:
        """Whether new jobs must pause until pending results are uploaded.

        These are high-water marks, not eviction limits. The probe is sequential,
        so the result already in flight is preserved even if it crosses a mark;
        no further job is claimed until the spool drains below both thresholds.
        """
        return self.spool_count >= self.max_files or self.spool_bytes >= self.max_bytes
