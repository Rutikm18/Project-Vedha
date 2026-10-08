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

import httpx
import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.ai.health import ProviderHealth
from app.ai.openai_tools import OpenAiToolClient
from app.services.llm import _provider_error_reason, _usable_key, cached_system_prompt
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
    """Raised when no configured provider (Claude, then OpenAI) can serve the advisor."""


_CATEGORIES = {CAT_TRIAGE, CAT_NEXT_ACTION, CAT_ATTACK_PATH}

# next_action recommendations may only propose one of these. They are PROPOSALS —
# each still routes through the platform's gated path on human approval.
ALLOWED_ACTIONS = [
    "run_discovery_scan", "run_targeted_scan", "request_exploit_validation",
    "recheck_finding", "mark_false_positive", "escalate_finding", "no_action",
]

_SEV_RANK = {"critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1}

# ── what a model-authored recommendation may point at ──────────────────────────
# The advisor reads scan data an attacker on the target network can influence
# (banners, hostnames, finding titles), so its output is untrusted. Whatever a
# recommendation names must be a real object of THIS engagement; anything else is
# dropped before it is stored, so the later approval step never acts on a target a
# model (or a poisoned banner) invented or took from another tenant.
TARGET_TYPES = ("finding", "asset", "attack_path", "engagement")
# Actions that only make sense against one concrete finding or asset.
_TARGETED_ACTIONS = {
    "run_targeted_scan", "request_exploit_validation", "recheck_finding",
    "mark_false_positive", "escalate_finding",
}
_TARGETED_TYPES = {"finding", "asset"}
MAX_RECOMMENDATIONS_PER_RUN = 50
_TITLE_MAX = 500
_RATIONALE_MAX = 4000
_EVIDENCE_MAX_BYTES = 8 * 1024

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
    def __init__(self, db: AsyncSession, *, client: Any = None,
                 clients: list[tuple[str, Any, str]] | None = None):
        settings = get_settings()
        self._settings = settings
        self._db = db
        self._model = settings.llm_model
        self._effort = settings.llm_effort
        self._max_tokens = settings.llm_max_tokens
        self._max_iters = 8
        # SYSTEM_PROMPT plus, once run() starts, the engagement's sector brief.
        self._system = SYSTEM_PROMPT

        # Ordered (provider, client, model) list: Claude first, then OpenAI tool
        # calling behind the same SDK shape (app/ai/openai_tools.py). The loop's
        # history stays in Anthropic format, so failover can happen mid-run.
        if clients is not None:
            self._clients = list(clients)
        elif client is not None:
            self._clients = [("anthropic", client, settings.llm_model)]
        else:
            self._clients = []
            if _HAS_ANTHROPIC and settings.anthropic_api_key:
                # One SDK retry: a second provider is waiting, so long local
                # backoff on a 429 only delays the advisor.
                self._clients.append(("anthropic", AsyncAnthropic(
                    api_key=settings.anthropic_api_key, max_retries=1), settings.llm_model))
            if _usable_key(settings.openai_api_key):
                self._clients.append(("openai", OpenAiToolClient(settings), settings.openai_model))
        self._client = self._clients[0][1] if self._clients else None

    @property
    def available(self) -> bool:
        return self._client is not None

    # ── main agentic loop ─────────────────────────────────────────────────────────

    async def run(self, engagement_id: uuid.UUID) -> dict:
        if self._client is None:
            raise AgentUnavailableError(
                "Anthropic SDK or ANTHROPIC_API_KEY not configured — advisor unavailable"
            )

        # AI gateway: always cloud egress. Under hybrid, tool results are
        # pseudonymized before they reach the model and the model's tool inputs /
        # final submission are rehydrated before we act on or persist them.
        from app.ai.gateway import GatewayDenied, rehydrate_obj, sdk_pseudonymizer
        try:
            pseudo = sdk_pseudonymizer(self._settings)
        except GatewayDenied as exc:
            raise AgentUnavailableError(str(exc)) from exc

        self._system = await self._system_with_domain(engagement_id)
        run_id = uuid.uuid4()
        messages: list[dict] = [{
            "role": "user",
            "content": (
                "Review this engagement and propose recommendations. Start by calling the "
                "read tools to see the findings, assets, and attack paths, then submit."
            ),
        }]

        stored = 0
        from app.ai.llm_report import _audit_sdk_call
        for iteration in range(self._max_iters):
            resp = await self._create(messages)
            await _audit_sdk_call(
                self._db, self._settings, task="advisor_agent", model=self._model, pseudo=pseudo,
                system=self._system, messages=messages,
                response=repr(getattr(resp, "content", "")), engagement_id=engagement_id)

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
                tool_input = rehydrate_obj(pseudo, tu.input or {})
                if tu.name == "submit_recommendations":
                    submit_input = tool_input
                    n = len((submit_input.get("recommendations") or []))
                    tool_results.append(_tool_result(tu.id, {"ok": True, "received": n}))
                else:
                    out = await self._exec_read_tool(tu.name, tool_input, engagement_id)
                    result = _tool_result(tu.id, out)
                    if pseudo is not None:
                        result["content"] = pseudo.pseudonymize(result["content"])
                    tool_results.append(result)
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

    async def _system_with_domain(self, engagement_id: uuid.UUID) -> str:
        """SYSTEM_PROMPT plus the engagement's sector/jurisdiction brief (same
        trusted block the chat assistant uses). Fail-soft: any lookup problem
        leaves the plain prompt, so the advisor never fails because of it."""
        from app.models.engagement import Engagement
        from app.services.domain_context import domain_brief_for
        try:
            eng = (await self._db.execute(
                select(Engagement).where(Engagement.id == engagement_id))).scalar_one_or_none()
            brief = await domain_brief_for(self._db, eng) if eng is not None else None
        except Exception as exc:  # noqa: BLE001 — the brief is advisory
            logger.warning("agent.domain_brief_failed", engagement=str(engagement_id), error=str(exc))
            return SYSTEM_PROMPT
        return f"{SYSTEM_PROMPT}\n\n{brief.text}" if brief and brief.text else SYSTEM_PROMPT

    async def _create(self, messages: list[dict]):
        """One model turn from the first provider that can serve it. Failures are
        recorded in the shared circuit breaker, so a provider that just
        rate-limited the advisor is skipped by every other AI caller too."""
        health = ProviderHealth()
        last_exc: Exception | None = None
        for name, client, model in self._clients:
            if not ProviderHealth.allows(await health.acquire(name)):
                continue
            kwargs: dict[str, Any] = {
                "model": model,
                "max_tokens": self._max_tokens,
                # Prompt caching: SYSTEM_PROMPT + the (large, stable) _TOOLS
                # definitions are identical across all 8 loop iterations. A cache
                # breakpoint on the system block caches BOTH (Anthropic order:
                # tools → system → messages), so each iteration only pays for the
                # growing message tail.
                "system": cached_system_prompt(self._system),
                "tools": _TOOLS,
                "messages": messages,
            }
            if self._effort and name == "anthropic":
                kwargs["output_config"] = {"effort": self._effort}  # cap thinking-token spend
            try:
                response = await client.messages.create(**kwargs)
            except (APIStatusError, APIConnectionError, httpx.HTTPError, KeyError, ValueError) as exc:
                last_exc = exc
                await health.record_failure(name, _classify_sdk_error(exc))
                logger.warning("agent.provider_failed", provider=name, error=type(exc).__name__)
                continue
            await health.record_success(name)
            if model != self._model:
                logger.warning("agent.provider_fallback", served_by=name, model=model)
            self._model = model
            return response
        raise AgentUnavailableError(
            f"no AI provider could serve the advisor: {last_exc or 'all providers are cooling down'}")

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
        # Fetch every asset's services in ONE batched query keyed by asset_id, then
        # group in Python (still capping at 30 per asset). This replaces the previous
        # per-asset query — an N+1 that issued 1 + len(assets) round-trips.
        svcs_by_asset: dict[uuid.UUID, list] = {}
        asset_ids = [a.id for a in assets]
        if asset_ids:
            svc_rows = (await self._db.execute(
                select(Service).where(Service.asset_id.in_(asset_ids))
            )).scalars().all()
            for s in svc_rows:
                bucket = svcs_by_asset.setdefault(s.asset_id, [])
                if len(bucket) < 30:
                    bucket.append(s)
        out = []
        for a in assets:
            svcs = svcs_by_asset.get(a.id, [])
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

    async def _targets_in_engagement(self, eid: uuid.UUID, wanted: dict[str, set[uuid.UUID]]) -> dict[str, set[uuid.UUID]]:
        """Of the ids a model named, the ones that really belong to this engagement
        (one query per type, however many recommendations there are)."""
        found: dict[str, set[uuid.UUID]] = {t: set() for t in TARGET_TYPES}
        found["engagement"] = {eid} if eid in wanted.get("engagement", set()) else set()
        for target_type, model in (("finding", Finding), ("asset", Asset), ("attack_path", AttackPath)):
            ids = wanted.get(target_type)
            if not ids:
                continue
            rows = (await self._db.execute(
                select(model.id).where(model.engagement_id == eid, model.id.in_(ids))
            )).scalars().all()
            found[target_type] = set(rows)
        return found

    async def _persist(self, eid: uuid.UUID, run_id: uuid.UUID, submit_input: dict) -> int:
        recs = submit_input.get("recommendations") or []
        if not isinstance(recs, list):
            return 0
        recs = [r for r in recs if isinstance(r, dict)][:MAX_RECOMMENDATIONS_PER_RUN]

        # Resolve every target the model named against this engagement up front.
        wanted: dict[str, set[uuid.UUID]] = {}
        for r in recs:
            target_type = str(r.get("target_type") or "").strip().lower()
            target_id = _maybe_uuid(r.get("target_id"))
            if target_type in TARGET_TYPES and target_id is not None:
                wanted.setdefault(target_type, set()).add(target_id)
        valid = await self._targets_in_engagement(eid, wanted) if wanted else {t: set() for t in TARGET_TYPES}

        stored = 0
        for r in recs:
            category = str(r.get("category") or "").strip()
            title = _clean_text(r.get("title") or "", _TITLE_MAX)
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

            target_type = str(r.get("target_type") or "").strip().lower() or None
            raw_target = r.get("target_id")
            target_id = _maybe_uuid(raw_target)
            if target_type is not None or raw_target:
                # A named target must be a known type AND a real object of this
                # engagement; otherwise the whole recommendation is dropped.
                if target_type not in TARGET_TYPES or target_id is None or target_id not in valid[target_type]:
                    logger.warning("agent.dropped_target", category=category, action=action,
                                   target_type=target_type)
                    continue
            if action in _TARGETED_ACTIONS and not (target_type in _TARGETED_TYPES and target_id is not None):
                logger.info("agent.dropped_untargeted_action", action=action)
                continue

            self._db.add(AgentRecommendation(
                engagement_id=eid, run_id=run_id,
                category=category,
                target_type=target_type,
                target_id=target_id,
                action=action,
                title=title,
                rationale=_clean_text(r["rationale"], _RATIONALE_MAX) if r.get("rationale") else None,
                confidence=_maybe_decimal(r.get("confidence")),
                priority=(_clean_text(r["priority"], 16) or None) if r.get("priority") else None,
                status=STATUS_PENDING,
                evidence=_bounded_evidence(r),
                model=self._model,
            ))
            stored += 1
        if stored:
            await self._db.flush()
        return stored


# ── recommendation hygiene ──────────────────────────────────────────────────────

def _clean_text(value: Any, maximum: int) -> str:
    """Single-line, control-free, bounded text for a model-supplied string."""
    text = "".join(" " if (ch.isspace() or not ch.isprintable()) else ch for ch in str(value))
    return " ".join(text.split())[:maximum].strip()


def _bounded_evidence(rec: dict) -> dict:
    """The raw model payload, capped. Oversized payloads keep only their scalar
    top-level fields so a runaway tool input cannot bloat the database."""
    try:
        if len(json.dumps(rec, default=str)) <= _EVIDENCE_MAX_BYTES:
            return rec
    except (TypeError, ValueError):
        pass
    return {k: (v if isinstance(v, (str, int, float, bool)) or v is None else None)
            for k, v in rec.items() if isinstance(k, str)}


# ── helpers ─────────────────────────────────────────────────────────────────────

def _classify_sdk_error(exc: Exception):
    """Routing meaning of an Anthropic-SDK or httpx failure (app/ai/failures.py)."""
    from app.ai.failures import NETWORK, TIMEOUT, classify_http, parse_retry_after
    response = getattr(exc, "response", None)
    status = getattr(exc, "status_code", None) or getattr(response, "status_code", None)
    if isinstance(status, int):
        retry_after = parse_retry_after(response.headers.get("retry-after")) if response is not None else None
        reason = str(getattr(exc, "message", "") or exc)
        if isinstance(exc, httpx.HTTPStatusError):
            reason = _provider_error_reason(exc.response)
        return classify_http(status, reason, retry_after)
    if isinstance(exc, httpx.TimeoutException) or "timeout" in type(exc).__name__.lower():
        return TIMEOUT
    return NETWORK


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
    """A confidence in [0, 100] with one decimal place, or None. The column is
    Numeric(4,1), so an out-of-range or non-finite model value would otherwise fail
    the flush and abort the whole advisor request."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None
    if not number.is_finite():
        return None
    return min(Decimal(100), max(Decimal(0), number)).quantize(Decimal("0.1"))
