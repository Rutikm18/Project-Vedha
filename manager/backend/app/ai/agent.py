"""AgentDecisionEngine — provider-routed, recommend-only security advisor.

The default path gathers a deterministic, bounded snapshot through read-only
Postgres methods and asks the Manager LLM adapter for one structured recommendation
batch. An injected Anthropic-compatible client retains the legacy tool-use loop as
a narrow compatibility/test seam.

WHY IT IS SAFE (recommend-only, by construction):
  * The tool surface is READ-ONLY plus a single terminal `submit_recommendations`
    tool. The model literally cannot launch a scan, run an exploit, or mutate a
    finding — its only write is a batch of recommendations that land "pending".
  * Every recommendation is human-approved before the existing gated path acts on
    it. This is the deterministic-first / human-in-the-loop posture the rest of
    the platform already uses (llm_outputs, exploit approvals, ScopeGuard).
  * Grounded: the model is told to use only tool-returned data — no invented CVEs,
    scores, or hosts.

The injected-client adapter sends no temperature, caps reasoning effort, and
handles model refusals instead of silently producing nothing. The default path
requires any Manager-configured provider; no Anthropic SDK is required.
"""
from __future__ import annotations

import json
import uuid
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

import structlog
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
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
from app.schemas.ai import InternalAiGenerateRequest
from app.services.llm import AiRuntimeError, ManagerLlmService

logger = structlog.get_logger()

class AgentUnavailableError(RuntimeError):
    """Raised when no configured advisor runtime can produce a valid result."""


_CATEGORIES = {CAT_TRIAGE, CAT_NEXT_ACTION, CAT_ATTACK_PATH}

# next_action recommendations may only propose one of these. They are PROPOSALS —
# each still routes through the platform's gated path on human approval.
ALLOWED_ACTIONS = [
    "run_discovery_scan", "run_targeted_scan", "request_exploit_validation",
    "recheck_finding", "mark_false_positive", "escalate_finding", "no_action",
]

_SEV_RANK = {"critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1}
_TARGET_TYPES = {"finding", "asset", "attack_path", "engagement"}
_PRIORITIES = {"critical", "high", "medium", "low"}
_MAX_RECOMMENDATIONS = 20
_CONTEXT_CHAR_LIMIT = 28_000

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


class _RecommendationCandidate(BaseModel):
    """Strict server-side validation for one model-proposed recommendation."""

    model_config = ConfigDict(extra="forbid")

    category: Literal["triage", "next_action", "attack_path"]
    title: str = Field(min_length=1, max_length=500)
    rationale: str = Field(min_length=1, max_length=6_000)
    target_type: Literal["finding", "asset", "attack_path", "engagement"] | None = None
    target_id: uuid.UUID | None = None
    action: Literal[
        "run_discovery_scan",
        "run_targeted_scan",
        "request_exploit_validation",
        "recheck_finding",
        "mark_false_positive",
        "escalate_finding",
        "no_action",
    ] | None = None
    confidence: float | None = Field(default=None, ge=0, le=100)
    priority: Literal["critical", "high", "medium", "low"] | None = None

    @model_validator(mode="after")
    def validate_semantics(self):
        self.title = self.title.strip()
        self.rationale = self.rationale.strip()
        if not self.title or not self.rationale:
            raise ValueError("title and rationale must contain text")
        if self.category == CAT_NEXT_ACTION and self.action is None:
            raise ValueError("next_action requires an allowlisted action")
        if self.category != CAT_NEXT_ACTION and self.action is not None:
            raise ValueError("only next_action may carry an action")
        if (self.target_type is None) != (self.target_id is None):
            raise ValueError("target_type and target_id must be supplied together")
        return self


class AgentDecisionEngine:
    def __init__(
        self,
        db: AsyncSession,
        *,
        client: Any = None,
        llm_service: ManagerLlmService | None = None,
    ):
        settings = llm_service.settings if llm_service is not None else get_settings()
        self._db = db
        self._model = settings.llm_model
        self._effort = settings.llm_effort
        self._max_tokens = settings.llm_max_tokens
        self._max_iters = 8
        self._client = client
        self._llm_service = (
            None if client is not None else (llm_service or ManagerLlmService(settings))
        )

    @property
    def available(self) -> bool:
        return self._client is not None or bool(
            self._llm_service is not None and self._llm_service.configured
        )

    # ── main agentic loop ─────────────────────────────────────────────────────────

    async def run(self, engagement_id: uuid.UUID) -> dict:
        if self._client is not None:
            return await self._run_injected_tool_loop(engagement_id)
        if self._llm_service is None or not self._llm_service.configured:
            raise AgentUnavailableError(
                "No Manager AI provider is configured — advisor unavailable"
            )

        return await self._run_manager_generation(engagement_id)

    async def _run_manager_generation(self, engagement_id: uuid.UUID) -> dict:
        """Gather bounded local context, then make one provider-agnostic JSON call."""
        run_id = uuid.uuid4()
        context = await self._gather_context(engagement_id)
        try:
            request = InternalAiGenerateRequest(
                task="advisor_recommendation",
                messages=[{
                    "role": "user",
                    "content": (
                        "Review the supplied engagement snapshot and return the "
                        "recommendation JSON object required by the system rules."
                    ),
                }],
                context=context,
                max_tokens=max(128, min(self._max_tokens, 4_096)),
            )
            text, runtime, fallback_used = await self._llm_service.generate_with_fallback(request)
        except (AiRuntimeError, ValidationError) as exc:
            raise AgentUnavailableError(str(exc)) from exc

        submit_input = _parse_submission(text)
        stored = await self._persist(
            engagement_id,
            run_id,
            submit_input,
            model=runtime.model,
            allowed_targets=_allowed_target_pairs(context),
        )
        logger.info(
            "agent.run_complete",
            engagement=str(engagement_id),
            run_id=str(run_id),
            stored=stored,
            provider=runtime.provider,
            model=runtime.model,
            fallback=fallback_used,
        )
        return {"run_id": str(run_id), "recommendations_stored": stored}

    async def _run_injected_tool_loop(self, engagement_id: uuid.UUID) -> dict:
        """Legacy Anthropic tool-use adapter retained for injected clients/tests."""

        run_id = uuid.uuid4()
        messages: list[dict] = [{
            "role": "user",
            "content": (
                "Review this engagement and propose recommendations. Start by calling the "
                "read tools to see the findings, assets, and attack paths, then submit."
            ),
        }]

        stored = 0
        allowed_targets: set[tuple[str, uuid.UUID]] = {("engagement", engagement_id)}
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
                    allowed_targets.update(_target_pairs_from_read(tu.name, out))
                    tool_results.append(_tool_result(tu.id, out))
            messages.append({"role": "user", "content": tool_results})

            if submit_input is not None:
                stored = await self._persist(
                    engagement_id,
                    run_id,
                    submit_input,
                    allowed_targets=allowed_targets,
                )
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

    async def _gather_context(self, engagement_id: uuid.UUID) -> dict:
        """Use the existing read-tool seam to build a bounded grounding snapshot."""
        overview = await self._exec_read_tool(
            "get_engagement_overview", {}, engagement_id,
        )
        findings = await self._exec_read_tool(
            "list_findings", {"limit": 50}, engagement_id,
        )
        attack_paths = await self._exec_read_tool(
            "list_attack_paths", {"limit": 20}, engagement_id,
        )
        assets = await self._exec_read_tool(
            "list_assets", {"limit": 25}, engagement_id,
        )
        # Dependency errors are useful in server logs but should not be sent to a
        # third-party model. Replace their potentially sensitive detail with a flag.
        for payload in (overview, findings, attack_paths, assets):
            if "error" in payload:
                payload.clear()
                payload["unavailable"] = True
        return _build_bounded_context(
            engagement_id,
            overview=overview,
            findings=findings,
            attack_paths=attack_paths,
            assets=assets,
        )

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

    async def _persist(
        self,
        eid: uuid.UUID,
        run_id: uuid.UUID,
        submit_input: dict,
        *,
        model: str | None = None,
        allowed_targets: set[tuple[str, uuid.UUID]] | None = None,
    ) -> int:
        recs = submit_input.get("recommendations") or []
        if not isinstance(recs, list):
            return 0
        recs = recs[:_MAX_RECOMMENDATIONS]
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

            target_type = str(r.get("target_type") or "").strip() or None
            raw_target_id = r.get("target_id")
            target_id = _maybe_uuid(raw_target_id)
            if target_type is not None and target_type not in _TARGET_TYPES:
                logger.info("agent.dropped_target_type", target_type=target_type)
                continue
            if (target_type is None) != (target_id is None):
                logger.info("agent.dropped_target", reason="incomplete_or_invalid")
                continue
            if (
                allowed_targets is not None
                and target_type is not None
                and (target_type, target_id) not in allowed_targets
            ):
                logger.info(
                    "agent.dropped_target",
                    reason="not_in_grounding_context",
                    target_type=target_type,
                )
                continue

            priority = str(r.get("priority") or "").strip().lower() or None
            if priority is not None and priority not in _PRIORITIES:
                logger.info("agent.dropped_priority", priority=priority)
                continue
            raw_confidence = r.get("confidence")
            confidence = _maybe_decimal(raw_confidence)
            if raw_confidence is not None and confidence is None:
                logger.info("agent.dropped_confidence", confidence="invalid")
                continue
            if confidence is not None and not (Decimal("0") <= confidence <= Decimal("100")):
                logger.info("agent.dropped_confidence", confidence=str(confidence))
                continue

            self._db.add(AgentRecommendation(
                engagement_id=eid, run_id=run_id,
                category=category,
                target_type=target_type,
                target_id=target_id,
                action=action,
                title=title[:500],
                rationale=(str(r["rationale"])[:6_000] if r.get("rationale") else None),
                confidence=confidence,
                priority=priority,
                status=STATUS_PENDING,
                evidence=r,
                model=(model or self._model)[:64],
            ))
            stored += 1
        if stored:
            await self._db.flush()
        return stored


# ── helpers ─────────────────────────────────────────────────────────────────────

def _parse_submission(text: str) -> dict:
    """Parse and validate the provider's single structured recommendation batch."""
    value = (text or "").strip()
    fence = chr(96) * 3
    if value.startswith(fence):
        parts = value.split(fence)
        if len(parts) >= 2:
            value = parts[1]
            if value.startswith("json"):
                value = value[4:]
            value = value.strip()
    try:
        raw = json.loads(value)
    except json.JSONDecodeError:
        start, end = value.find("{"), value.rfind("}") + 1
        try:
            raw = json.loads(value[start:end]) if 0 <= start < end else None
        except json.JSONDecodeError as exc:
            raise AgentUnavailableError(
                "AI advisor returned invalid structured output"
            ) from exc
    if not isinstance(raw, dict) or not isinstance(raw.get("recommendations"), list):
        raise AgentUnavailableError("AI advisor returned an invalid recommendation schema")
    raw_recommendations = raw["recommendations"]
    if len(raw_recommendations) > _MAX_RECOMMENDATIONS:
        raise AgentUnavailableError(
            f"AI advisor exceeded the {_MAX_RECOMMENDATIONS}-recommendation limit"
        )

    validated: list[dict] = []
    for index, candidate in enumerate(raw_recommendations):
        try:
            parsed = _RecommendationCandidate.model_validate(candidate)
        except ValidationError:
            logger.info("agent.dropped_recommendation", index=index, reason="schema")
            continue
        validated.append(parsed.model_dump(mode="json"))
    if raw_recommendations and not validated:
        raise AgentUnavailableError("AI advisor returned no valid recommendations")
    return {"recommendations": validated}


def _build_bounded_context(
    engagement_id: uuid.UUID,
    *,
    overview: dict,
    findings: dict,
    attack_paths: dict,
    assets: dict,
) -> dict:
    """Build a deterministic snapshot with an explicit inclusion/omission manifest."""
    context: dict[str, Any] = {
        "context_version": 1,
        "engagement_id": str(engagement_id),
        "overview": _compact_overview(overview),
        "findings": [],
        "attack_paths": [],
        "assets": [],
    }
    record_budget = _CONTEXT_CHAR_LIMIT - 1_000  # reserve for coverage metadata

    def append_if_fits(bucket: str, item: dict) -> None:
        context[bucket].append(item)
        if _json_chars(context) > record_budget:
            context[bucket].pop()

    finding_rows = findings.get("findings") if isinstance(findings, dict) else []
    path_rows = attack_paths.get("attack_paths") if isinstance(attack_paths, dict) else []
    asset_rows = assets.get("assets") if isinstance(assets, dict) else []
    for item in finding_rows if isinstance(finding_rows, list) else []:
        if isinstance(item, dict):
            append_if_fits("findings", _compact_finding(item))
    for item in path_rows if isinstance(path_rows, list) else []:
        if isinstance(item, dict):
            append_if_fits("attack_paths", _compact_attack_path(item))
    for item in asset_rows if isinstance(asset_rows, list) else []:
        if isinstance(item, dict):
            append_if_fits("assets", _compact_asset(item))

    totals = {
        "findings": _safe_count(
            overview.get("total_findings"),
            findings.get("count"),
            len(finding_rows) if isinstance(finding_rows, list) else 0,
        ),
        "attack_paths": _safe_count(
            overview.get("attack_path_count"),
            attack_paths.get("count"),
            len(path_rows) if isinstance(path_rows, list) else 0,
        ),
        "assets": _safe_count(
            overview.get("asset_count"),
            assets.get("count"),
            len(asset_rows) if isinstance(asset_rows, list) else 0,
        ),
    }
    included = {
        name: len(context[name])
        for name in ("findings", "attack_paths", "assets")
    }
    context["coverage"] = {
        "included": included,
        "total": totals,
        "omitted": {name: max(0, totals[name] - included[name]) for name in totals},
        "context_limit_chars": _CONTEXT_CHAR_LIMIT,
    }
    if _json_chars(context) > _CONTEXT_CHAR_LIMIT:  # defensive invariant
        raise AgentUnavailableError("Advisor context could not be bounded safely")
    return context


def _compact_overview(value: dict) -> dict:
    if value.get("unavailable"):
        return {"unavailable": True}
    counts = value.get("findings_by_severity")
    return {
        "findings_by_severity": counts if isinstance(counts, dict) else {},
        "total_findings": _safe_count(value.get("total_findings"), 0),
        "asset_count": _safe_count(value.get("asset_count"), 0),
        "service_count": _safe_count(value.get("service_count"), 0),
        "attack_path_count": _safe_count(value.get("attack_path_count"), 0),
    }


def _compact_finding(value: dict) -> dict:
    cves = value.get("cve_ids") if isinstance(value.get("cve_ids"), list) else []
    return {
        "id": str(value.get("id") or "")[:36],
        "title": str(value.get("title") or "")[:500],
        "severity": str(value.get("severity") or "")[:16],
        "cvss": value.get("cvss"),
        "status": str(value.get("status") or "")[:32],
        "cve_ids": [str(item)[:32] for item in cves[:20]],
        "exploitable": bool(value.get("exploitable")),
    }


def _compact_attack_path(value: dict) -> dict:
    return {
        "id": str(value.get("id") or "")[:36],
        "risk_score": value.get("risk_score"),
        "hops": _safe_count(value.get("hops"), 0),
        "chokepoints": _safe_count(value.get("chokepoints"), 0),
    }


def _compact_asset(value: dict) -> dict:
    services = value.get("services") if isinstance(value.get("services"), list) else []
    compact_services = []
    for service in services[:12]:
        if not isinstance(service, dict):
            continue
        compact_services.append({
            "port": service.get("port"),
            "proto": str(service.get("proto") or "")[:16],
            "product": str(service.get("product") or "")[:120],
            "version": str(service.get("version") or "")[:120],
        })
    return {
        "id": str(value.get("id") or "")[:36],
        "ip": str(value.get("ip") or "")[:64],
        "hostname": str(value.get("hostname") or "")[:255],
        "os": str(value.get("os") or "")[:255],
        "services": compact_services,
    }


def _allowed_target_pairs(context: dict) -> set[tuple[str, uuid.UUID]]:
    allowed = {("engagement", uuid.UUID(str(context["engagement_id"])))}
    for bucket, target_type in (
        ("findings", "finding"),
        ("assets", "asset"),
        ("attack_paths", "attack_path"),
    ):
        for item in context.get(bucket, []):
            target_id = _maybe_uuid(item.get("id")) if isinstance(item, dict) else None
            if target_id is not None:
                allowed.add((target_type, target_id))
    return allowed


def _target_pairs_from_read(name: str, output: dict) -> set[tuple[str, uuid.UUID]]:
    bucket_and_type = {
        "list_findings": ("findings", "finding"),
        "list_assets": ("assets", "asset"),
        "list_attack_paths": ("attack_paths", "attack_path"),
    }.get(name)
    if bucket_and_type is None or not isinstance(output, dict):
        return set()
    bucket, target_type = bucket_and_type
    pairs: set[tuple[str, uuid.UUID]] = set()
    for item in output.get(bucket, []):
        target_id = _maybe_uuid(item.get("id")) if isinstance(item, dict) else None
        if target_id is not None:
            pairs.add((target_type, target_id))
    return pairs


def _safe_count(*values: Any) -> int:
    counts: list[int] = []
    for value in values:
        try:
            counts.append(max(0, int(value)))
        except (TypeError, ValueError):
            continue
    return max(counts, default=0)


def _json_chars(value: Any) -> int:
    return len(json.dumps(value, default=str, separators=(",", ":")))


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
        parsed = Decimal(str(value))
        return parsed if parsed.is_finite() else None
    except (InvalidOperation, ValueError, TypeError):
        return None
