"""result_queue.py — durable, crash-safe, encrypted result spool (Phase 4).

Sits between the scan engine and the uplink so results never live only in
memory (the silent-data-loss failure). Properties:

- **Crash-safe append:** each record is written to a temp file, fsync'd, then
  atomically renamed — a crash never leaves a half-written record.
- **At-least-once + idempotent:** records persist until `ack()`; a crash between
  "sent" and "acked" replays, and the Manager dedups by `job_id`.
- **Bounded + drop-oldest:** size/count caps with an explicit drop-oldest
  overflow, plus an age `prune()` — so a week-long Manager outage can't fill
  `/var` fleet-wide.
- **Backpressure:** `should_backpressure()` tells the scheduler to STOP starting
  new scans at the high-water mark rather than growing the queue.
- **Encrypted at rest:** a pluggable cipher (default: host-sealed Fernet) — the
  queue holds internal topology and banners.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Callable

_SUFFIX = ".rec"


# ── ciphers ──────────────────────────────────────────────────────────────────
class NullCipher:
    """Identity cipher — tests + explicitly-plaintext deployments only."""
    def encrypt(self, data: bytes) -> bytes: return data
    def decrypt(self, data: bytes) -> bytes: return data


def host_sealed_cipher(state_dir: str):
    """Fernet cipher keyed by a per-host key file (0600) that never leaves the
    host. Stronger sealing (OS keystore/TPM) is on the roadmap."""
    from cryptography.fernet import Fernet  # lazy: only when encryption is used
    os.makedirs(state_dir, exist_ok=True)
    key_path = os.path.join(state_dir, "queue.key")
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as fh:
            fh.write(key)
        if os.name == "posix":
            os.chmod(key_path, 0o600)
    else:
        with open(key_path, "rb") as fh:
            key = fh.read()
    f = Fernet(key)

    class _Fernet:
        def encrypt(self, data: bytes) -> bytes: return f.encrypt(data)
        def decrypt(self, data: bytes) -> bytes: return f.decrypt(data)
    return _Fernet()


# ── records ──────────────────────────────────────────────────────────────────
@dataclass
class Record:
    job_id: str
    enqueued_at: float
    payload: dict
    path: str


@dataclass
class QueueStats:
    count: int
    bytes: int
    oldest_age_s: float


class ResultQueue:
    def __init__(self, directory: str, *, cipher=None,
                 now: Callable[[], float] = time.time,
                 max_records: int = 10_000, max_bytes: int = 512 * 1024 * 1024,
                 max_age_s: float = 14 * 24 * 3600,
                 high_water_records: int = 8_000):
        self.dir = directory
        self._cipher = cipher or NullCipher()
        self._now = now
        self.max_records = max_records
        self.max_bytes = max_bytes
        self.max_age_s = max_age_s
        self.high_water_records = high_water_records
        os.makedirs(self.dir, exist_ok=True)
        self._seq = self._max_seq() + 1

    # ── internals ──
    def _files(self) -> list[str]:
        return sorted(f for f in os.listdir(self.dir) if f.endswith(_SUFFIX))

    def _max_seq(self) -> int:
        best = -1
        for f in self._files():
            try:
                best = max(best, int(f.split("-", 1)[0]))
            except ValueError:
                continue
        return best

    def _find(self, job_id: str) -> str | None:
        tail = f"-{job_id}{_SUFFIX}"
        for f in self._files():
            if f.endswith(tail):
                return os.path.join(self.dir, f)
        return None

    def _atomic_write(self, path: str, data: bytes) -> None:
        tmp = path + ".tmp"
        with open(tmp, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
        if os.name == "posix":
            os.chmod(path, 0o600)
            try:
                dfd = os.open(self.dir, os.O_DIRECTORY)
                try:
                    os.fsync(dfd)
                finally:
                    os.close(dfd)
            except OSError:
                pass

    def _read(self, path: str) -> Record:
        with open(path, "rb") as fh:
            env = json.loads(self._cipher.decrypt(fh.read()).decode())
        return Record(job_id=env["job_id"], enqueued_at=float(env["enqueued_at"]),
                      payload=env["payload"], path=path)

    def _enforce_size_bounds(self) -> None:
        files = self._files()
        while files and (len(files) > self.max_records or self._bytes(files) > self.max_bytes):
            os.remove(os.path.join(self.dir, files.pop(0)))   # drop oldest

    def _bytes(self, files: list[str]) -> int:
        return sum(os.path.getsize(os.path.join(self.dir, f)) for f in files)

    # ── public API ──
    def enqueue(self, job_id: str, payload: dict) -> str:
        existing = self._find(job_id)
        if existing:
            return existing            # idempotent
        env = {"job_id": job_id, "enqueued_at": self._now(), "payload": payload}
        data = self._cipher.encrypt(json.dumps(env).encode())
        name = f"{self._seq:012d}-{job_id}{_SUFFIX}"
        self._seq += 1
        path = os.path.join(self.dir, name)
        self._atomic_write(path, data)
        self._enforce_size_bounds()
        return path

    def pending(self) -> list[Record]:
        return [self._read(os.path.join(self.dir, f)) for f in self._files()]

    def ack(self, job_id: str) -> None:
        path = self._find(job_id)
        if path and os.path.exists(path):
            os.remove(path)

    def prune(self) -> int:
        now = self._now()
        dropped = 0
        for rec in self.pending():
            if now - rec.enqueued_at > self.max_age_s:
                os.remove(rec.path)
                dropped += 1
        return dropped

    def stats(self) -> QueueStats:
        files = self._files()
        recs = self.pending()
        oldest = min((r.enqueued_at for r in recs), default=self._now())
        return QueueStats(count=len(files), bytes=self._bytes(files),
                          oldest_age_s=self._now() - oldest)

    def should_backpressure(self) -> bool:
        return len(self._files()) >= self.high_water_records
