"""answer_store.py — reuse an answer when the question is byte-for-byte the same.

Vedha's one-shot tasks (briefs, remediation refinement, compliance, report
sections) are built from recorded data, so identical input means an identical
question — a customer reopening a finding, an operator regenerating a report. The
key is a hash of the exact task, system prompt (which embeds the evidence) and
messages; when the evidence changes the hash changes, so answers go stale on
their own.

Exact-hash only, deliberately: two "similar" findings on different hosts must
never share an answer, so semantic (embedding) caching is out.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from app.ai.kv import KvStore


@dataclass(frozen=True)
class StoredAnswer:
    text: str
    provider: str
    model: str
    privacy: str
    tier: str


class AnswerStore:
    def __init__(self, kv: KvStore, ttl_s: float) -> None:
        self._kv = kv
        self.ttl_s = ttl_s

    @staticmethod
    def key(task: str, system: str, messages: list[dict[str, str]], lowest_tier: str) -> str:
        canonical = json.dumps([task, lowest_tier, system, messages],
                               sort_keys=True, separators=(",", ":"), default=str)
        return "ai:ans:" + hashlib.sha256(canonical.encode()).hexdigest()

    async def get(self, key: str) -> StoredAnswer | None:
        raw = await self._kv.get(key)
        if not raw:
            return None
        try:
            return StoredAnswer(**json.loads(raw))
        except (ValueError, TypeError):
            return None

    async def put(self, key: str, answer: StoredAnswer) -> None:
        await self._kv.set(key, json.dumps(asdict(answer)), self.ttl_s)
