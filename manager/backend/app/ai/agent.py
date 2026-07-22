"""
agent.py — AgentDecisionEngine: the agentic AI advisor.

WHAT IT IS: a Claude tool-use loop that reasons over an engagement's REAL data
(read-only tools that query Postgres) and proposes recommendations across three
use cases: finding triage, next-action orchestration, and attack-path reasoning.

WHY IT IS SAFE (recommend-only, by construction):
  * The tool surface is READ-ONLY plus a single terminal `submit_recommendations`
    tool. The model literally cannot launch a scan, run an exploit, or mutate a
    finding — its only write is a batch of recommendations that land "pending".
  * Every recommendation is human-approved before the existing gated path acts on
    it. This is the deterministic-first / human-in-the-loop posture the rest of
    the platform already uses (llm_outputs, exploit approvals, ScopeGuard).
  * Grounded: the model is told to use only tool-returned data — no invented CVEs,
    scores, or hosts.

Modern-model compatible (Sonnet 4.6 / Opus 4.6+ / Fable 5): sends NO `temperature`
(400s on Opus 4.7/4.8 and Fable), uses `output_config.effort` to cap thinking-token
spend, and handles a `stop_reason == "refusal"` (pentest content can trip
classifiers) instead of silently producing nothing.

The `anthropic` package + API key are optional: absent either, `available` is
False and `run()` raises AgentUnavailableError so the API returns a clean 503.
"""
from __future__ import annotations

import json
import uuid
from decimal import Decimal, InvalidOperation
from typing import Any

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.agent_recommendation import (
    AgentRecommendation, CAT_ATTACK_PATH, CAT_NEXT_ACTION, CAT_TRIAGE, STATUS_PENDING,
)
from app.models.asset import Asset
from app.models.attack_path import AttackPath
from app.models.finding import Finding
from app.models.service import Service

logger = structlog.get_logger()

try:
    from anthropic import APIConnectionError, APIStatusError, AsyncAnthropic, RateLimitError

    _HAS_ANTHROPIC = True
except ImportError:  # pragma: no cover
    AsyncAnthropic = None  # type: ignore
    APIStatusError = RateLimitError = APIConnectionError = Exception  # type: ignore
    _HAS_ANTHROPIC = False


class AgentUnavailableError(RuntimeError):
    """Raised when the Anthropic SDK or API key is not configured."""


_CATEGORIES = {CAT_TRIAGE, CAT_NEXT_ACTION, CAT_ATTACK_PATH}

# next_action recommendations may only propose one of these. They are PROPOSALS —
# each still routes through the platform's gated path on human approval.
ALLOWED_ACTIONS = [
    "run_discovery_scan", "run_targeted_scan", "request_exploit_validation",
    "recheck_finding", "mark_false_positive", "escalate_finding", "no_action",
]

_SEV_RANK = {"critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1}

SYSTEM_PROMPT = (
    "You are the Vedha security advisor — an assistant that reviews an authorized "
    "penetration-test engagement's data and proposes next steps for a human operator.\n\n"
    "STRICT RULES (override everything else):\n"
    "1. Use ONLY data returned by the tools. Never invent findings, CVE IDs, CVSS "
    "scores, hosts, or attack paths. If the data doesn't support a claim, don't make it.\n"
    "2. You RECOMMEND ONLY. You cannot execute anything. Every next_action is a "
    "proposal a human will approve before it runs — choose the action from the allowed "
    "set only, and never assume it has been performed.\n"
    "3. Cover three use cases where the data warrants it:\n"
    "   - triage: judge which findings are real / mis-prioritized / likely false positives.\n"
    "   - next_action: propose gated follow-up work (deeper scan, exploit validation, recheck).\n"
    "   - attack_path: turn correlated findings + attack paths into a short narrative + fix.\n"
    "4. Be precise and concise. Prefer a few high-signal recommendations over many weak ones.\n\n"
    "WORKFLOW: first call the read tools to gather the engagement's real state, then call "
    "`submit_recommendations` exactly once with your recommendations. Do not submit before "
    "you have looked at the data."
)

_READ_TOOLS = [
    {
        "name": "get_engagement_overview",
        "description": "Counts for this engagement: findings by severity, asset/service/attack-path totals.",
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "list_findings",
        "description": "Findings for this engagement, highest severity first. Fields: id, title, "
                       "severity, cvss, status, cve_ids, exploitable.",
        "input_schema": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "description": "max rows (default 50)"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "list_assets",
        "description": "Assets (hosts) for this engagement with their open services.",
        "input_schema": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "description": "max rows (default 40)"}},
            "additionalProperties": False,
        },
    },
    {
        "name": "list_attack_paths",
        "description": "Discovered attack paths for this engagement: id, risk_score, hop count, chokepoints.",
        "input_schema": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "description": "max rows (default 20)"}},
            "additionalProperties": False,
        },
    },
]

_SUBMIT_TOOL = {
    "name": "submit_recommendations",
    "description": "Submit your final recommendations. Call exactly once, after reviewing the data.",
    "input_schema": {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "enum": sorted(_CATEGORIES)},
                        "title": {"type": "string", "description": "one-line summary"},
                        "rationale": {"type": "string", "description": "why, grounded in the data"},
                        "target_type": {"type": "string", "description": "e.g. finding | asset | engagement"},
                        "target_id": {"type": "string", "description": "id of the target, if any"},
                        "action": {"type": "string", "enum": ALLOWED_ACTIONS,
                                   "description": "for next_action only"},
                        "confidence": {"type": "number", "description": "0-100"},
                        "priority": {"type": "string", "description": "critical|high|medium|low"},
                    },
                    "required": ["category", "title", "rationale"],
                },
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False,
    },
}

_TOOLS = _READ_TOOLS + [_SUBMIT_TOOL]


class AgentDecisionEngine:
    def __init__(self, db: AsyncSession, *, client: Any = None):
        settings = get_settings()
        self._db = db
        self._model = settings.llm_model
        self._effort = settings.llm_effort
        self._max_tokens = settings.llm_max_tokens
        self._max_iters = 8

        if client is not None:
            self._client = client
        elif _HAS_ANTHROPIC and settings.anthropic_api_key:
            self._client = AsyncAnthropic(api_key=settings.anthropic_api_key, max_retries=2)
        else:
            self._client = None

    @property
    def available(self) -> bool:
        return self._client is not None

    # ── main agentic loop ─────────────────────────────────────────────────────────

    async def run(self, engagement_id: uuid.UUID) -> dict:
        if self._client is None:
            raise AgentUnavailableError(
                "Anthropic SDK or ANTHROPIC_API_KEY not configured — advisor unavailable"
            )

        run_id = uuid.uuid4()
        messages: list[dict] = [{
            "role": "user",
            "content": (
                "Review this engagement and propose recommendations. Start by calling the "
                "read tools to see the findings, assets, and attack paths, then submit."
            ),
        }]

        stored = 0
        for iteration in range(self._max_iters):
            resp = await self._create(messages)

            if getattr(resp, "stop_reason", None) == "refusal":
                detail = getattr(getattr(resp, "stop_details", None), "explanation", "") or ""
                raise AgentUnavailableError(f"model declined to advise on this content: {detail}".strip())

            messages.append({"role": "assistant", "content": resp.content})
            tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
            if not tool_uses:
                logger.info("agent.no_tool_use", engagement=str(engagement_id), iteration=iteration)
                break

            tool_results: list[dict] = []
            submit_input: dict | None = None
            for tu in tool_uses:
                if tu.name == "submit_recommendations":
                    submit_input = tu.input or {}
                    n = len((submit_input.get("recommendations") or []))
                    tool_results.append(_tool_result(tu.id, {"ok": True, "received": n}))
                else:
                    out = await self._exec_read_tool(tu.name, tu.input or {}, engagement_id)
                    tool_results.append(_tool_result(tu.id, out))
            messages.append({"role": "user", "content": tool_results})

            if submit_input is not None:
                stored = await self._persist(engagement_id, run_id, submit_input)
                break
        else:
            logger.warning("agent.no_submit", engagement=str(engagement_id),
                           hint="advisor hit the iteration cap without submitting")

        logger.info("agent.run_complete", engagement=str(engagement_id),
                    run_id=str(run_id), stored=stored)
        return {"run_id": str(run_id), "recommendations_stored": stored}

    async def _create(self, messages: list[dict]):
        kwargs: dict[str, Any] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "system": SYSTEM_PROMPT,
            "tools": _TOOLS,
            "messages": messages,
        }
        if self._effort:
            kwargs["output_config"] = {"effort": self._effort}  # cap thinking-token spend
        return await self._client.messages.create(**kwargs)

    # ── read tools (the model's only window into the data) ──────────────────────────

    async def _exec_read_tool(self, name: str, args: dict, engagement_id: uuid.UUID) -> dict:
        try:
            if name == "get_engagement_overview":
                return await self._overview(engagement_id)
            if name == "list_findings":
                return await self._list_findings(engagement_id, int(args.get("limit") or 50))
            if name == "list_assets":
                return await self._list_assets(engagement_id, int(args.get("limit") or 40))
            if name == "list_attack_paths":
                return await self._list_attack_paths(engagement_id, int(args.get("limit") or 20))
            return {"error": f"unknown tool {name!r}"}
        except Exception as exc:  # noqa: BLE001 — a tool error must not crash the loop
            logger.warning("agent.tool_failed", tool=name, error=str(exc))
            return {"error": f"{type(exc).__name__}: {exc}"}

    async def _overview(self, eid: uuid.UUID) -> dict:
        findings = (await self._db.execute(
            select(Finding.severity, func.count()).where(Finding.engagement_id == eid)
            .group_by(Finding.severity)
        )).all()
        sev_counts = {_val(s): int(c) for s, c in findings}
        assets = await self._count(Asset, Asset.engagement_id == eid)
        paths = await self._count(AttackPath, AttackPath.engagement_id == eid)
        services = (await self._db.execute(
            select(func.count()).select_from(Service).join(Asset, Service.asset_id == Asset.id)
            .where(Asset.engagement_id == eid)
        )).scalar_one()
        return {
            "findings_by_severity": sev_counts,
            "total_findings": sum(sev_counts.values()),
            "asset_count": assets, "service_count": int(services or 0),
            "attack_path_count": paths,
        }

    async def _list_findings(self, eid: uuid.UUID, limit: int) -> dict:
        rows = (await self._db.execute(
            select(Finding).where(Finding.engagement_id == eid)
        )).scalars().all()
        rows.sort(key=lambda f: _SEV_RANK.get(_val(f.severity), 0), reverse=True)
        out = [{
            "id": str(f.id), "title": f.title, "severity": _val(f.severity),
            "cvss": float(f.cvss_score) if f.cvss_score is not None else None,
            "status": _val(f.status), "cve_ids": list(f.cve_ids or []),
            "exploitable": bool(getattr(f, "exploitable", False)),
        } for f in rows[: max(1, min(limit, 200))]]
        return {"count": len(rows), "findings": out}

    async def _list_assets(self, eid: uuid.UUID, limit: int) -> dict:
        assets = (await self._db.execute(
            select(Asset).where(Asset.engagement_id == eid).limit(max(1, min(limit, 200)))
        )).scalars().all()
        out = []
        for a in assets:
            svcs = (await self._db.execute(
                select(Service).where(Service.asset_id == a.id).limit(30)
            )).scalars().all()
            out.append({
                "id": str(a.id),
                "ip": getattr(a, "ip_address", None),
                "hostname": getattr(a, "hostname", None),
                "os": getattr(a, "os", None),
                "services": [{
                    "port": s.port, "proto": s.protocol,
                    "product": s.product, "version": s.version,
                } for s in svcs],
            })
        return {"count": len(out), "assets": out}

    async def _list_attack_paths(self, eid: uuid.UUID, limit: int) -> dict:
        paths = (await self._db.execute(
            select(AttackPath).where(AttackPath.engagement_id == eid).limit(max(1, min(limit, 100)))
        )).scalars().all()
        out = [{
            "id": str(p.id),
            "risk_score": float(p.risk_score) if p.risk_score is not None else None,
            "hops": len(p.path_nodes or []),
            "chokepoints": len(p.chokepoints or []),
        } for p in paths]
        return {"count": len(out), "attack_paths": out}

    async def _count(self, model, where) -> int:
        return int((await self._db.execute(
            select(func.count()).select_from(model).where(where)
        )).scalar_one() or 0)

    # ── persistence (the ONLY write; everything lands pending) ───────────────────────

    async def _persist(self, eid: uuid.UUID, run_id: uuid.UUID, submit_input: dict) -> int:
        recs = submit_input.get("recommendations") or []
        stored = 0
        for r in recs:
            if not isinstance(r, dict):
                continue
            category = str(r.get("category") or "").strip()
            title = str(r.get("title") or "").strip()
            if category not in _CATEGORIES or not title:
                continue  # drop malformed / off-schema rows rather than persist junk
            action = r.get("action")
            if category == CAT_NEXT_ACTION:
                # A next_action must name a valid gated action, or it isn't actionable
                # (and a non-allowlisted action must never be persisted at all) — drop it.
                if action not in ALLOWED_ACTIONS:
                    logger.info("agent.dropped_action", category=category, action=action)
                    continue
            else:
                action = None  # triage / attack_path rows don't carry an action
            self._db.add(AgentRecommendation(
                engagement_id=eid, run_id=run_id,
                category=category,
                target_type=(str(r["target_type"])[:32] if r.get("target_type") else None),
                target_id=_maybe_uuid(r.get("target_id")),
                action=action,
                title=title[:500],
                rationale=(str(r["rationale"]) if r.get("rationale") else None),
                confidence=_maybe_decimal(r.get("confidence")),
                priority=(str(r["priority"])[:16] if r.get("priority") else None),
                status=STATUS_PENDING,
                evidence=r,
                model=self._model,
            ))
            stored += 1
        if stored:
            await self._db.flush()
        return stored


# ── helpers ─────────────────────────────────────────────────────────────────────

def _tool_result(tool_use_id: str, obj: Any) -> dict:
    return {"type": "tool_result", "tool_use_id": tool_use_id,
            "content": json.dumps(obj, default=str)}


def _val(v: Any) -> str:
    return str(getattr(v, "value", v)) if v is not None else ""


def _maybe_uuid(value: Any):
    if not value:
        return None
    try:
        return uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return None


def _maybe_decimal(value: Any):
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
