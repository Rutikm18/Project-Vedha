"""
ai_refine.py — AI refinement layered ON TOP of the knowledge-base plan.

The KB plan is always the floor; the model may only sharpen it. Guarantees:

  * Transport: ``ManagerLlmService`` → AI gateway (cloud / hybrid pseudonymised
    / sovereign local model) → audit chain. No direct provider SDK here.
  * Injection boundary: scan facts (banners, products, hostnames) travel only in
    ``AiGenerateRequest.context``, which the service fences as untrusted DATA.
  * Overlay, not replacement: a field the model omits keeps its KB value; every
    change is recorded in ``ai_changes`` for the "what the AI changed" view.
  * Guards: destructive commands are dropped (HallucinationGuard); CVE ids and
    versions not supplied to the model are stripped/labelled; unknown step
    numbers are ignored; at most 3 extra steps.
  * Staleness: the refinement stores a fingerprint of the facts it saw; if the
    live facts differ later (new version, port, exposure) the plan is stale.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Iterable

import structlog

from app.ai.hallucination import HallucinationGuard
from app.remediation.context import RemediationContext
from app.remediation.recipes import TIERS
from app.services.finding_ai import _extract_json

logger = structlog.get_logger()

_CVE = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.I)
_VERSIONISH = re.compile(r"\b\d+(?:\.\d+)+[a-z0-9]*\b", re.I)
UNVERIFIED_VERSION_LABEL = " (AI-suggested — verify against the vendor advisory)"
MAX_EXTRA_STEPS = 3
_MAX_TEXT = 1500
_MAX_CMDS = 8

_FACT_FIELDS = ("ip", "os", "os_version", "port", "product", "version", "cpe")


def _fact_payload(ctx: RemediationContext) -> dict:
    out = {name: ctx.text(name) for name in ("host", *_FACT_FIELDS, "service_name", "banner_excerpt")}
    out.update({"os_family": ctx.os_family, "exposure": ctx.exposure, "fixed_version": ctx.fixed_version,
                "rule_id": ctx.rule_id, "cve_ids": list(ctx.cve_ids), "fragile": ctx.fragile})
    return out


def facts_fingerprint(contexts: Iterable[RemediationContext]) -> str:
    """sha256 over the facts that shape a plan, order-independent."""
    rows = sorted(json.dumps({k: str(v) for k, v in {**{n: ctx.text(n) for n in _FACT_FIELDS},
                                                     "exposure": ctx.exposure,
                                                     "fixed_version": ctx.fixed_version,
                                                     "rule_id": ctx.rule_id,
                                                     "cves": ",".join(ctx.cve_ids)}.items()},
                              sort_keys=True) for ctx in contexts)
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def allowed_tokens(contexts: Iterable[RemediationContext]) -> tuple[set[str], set[str]]:
    cves: set[str] = set()
    versions: set[str] = set()
    for ctx in contexts:
        cves.update(c.upper() for c in ctx.cve_ids)
        for v in (ctx.fixed_version, ctx.version.value if ctx.version.recorded else None,
                  ctx.os_version.value if ctx.os_version.recorded else None):
            if v:
                versions.add(str(v).lower())
    return cves, versions


def compact_plan(plan: dict) -> dict:
    """The part of the KB plan the model needs (bounded for the 32k context cap)."""
    return {
        "title": plan.get("title"), "target_state": plan.get("target_state"),
        "remediation_type": plan.get("remediation_type"), "os": plan.get("os"),
        "steps": [{"step": s["step"], "tier": s.get("tier"), "title": s["title"],
                   "description": s["description"], "commands": s.get("commands_for_os", [])[:_MAX_CMDS],
                   "pre_checks": s.get("pre_checks", []), "rollback": s.get("rollback", "")}
                  for s in plan.get("steps", [])],
        "verification": plan.get("verification_check"),
    }


def build_context_payload(plan: dict, contexts: list[RemediationContext]) -> dict:
    cves, versions = allowed_tokens(contexts)
    return {
        "kb_plan": compact_plan(plan),
        "facts": [_fact_payload(c) for c in contexts[:25]],
        "hosts_total": len(contexts),
        "allowed": {"cves": sorted(cves), "versions": sorted(versions)},
    }


def _scrub(text: Any, allowed_cves: set[str]) -> str:
    """Bound length and remove any CVE id the model was not given."""
    s = str(text or "")[:_MAX_TEXT]
    return _CVE.sub(lambda m: m.group(0) if m.group(0).upper() in allowed_cves else "[unverified CVE removed]", s)


def _safe_cmds(cmds: Any, guard: HallucinationGuard) -> tuple[list[str], bool]:
    if not isinstance(cmds, list):
        return [], False
    safe, dropped = [], False
    for c in cmds[:_MAX_CMDS]:
        c = str(c).strip()
        if not c:
            continue
        if guard.validate_remediation_commands(c)["valid"]:
            safe.append(c[:400])
        else:
            dropped = True
    return safe, dropped


def overlay(kb_plan: dict, ai: dict, *, allowed_cves: set[str], allowed_versions: set[str],
            guard: HallucinationGuard) -> tuple[dict, list[dict]]:
    """Merge a parsed AI response onto the KB plan. Returns (plan, changes)."""
    plan = copy.deepcopy(kb_plan)
    changes: list[dict] = []

    def change(field: str, before: Any, after: Any, step: int | None = None) -> None:
        changes.append({"field": field, "step": step, "before": before, "after": after})

    for field in ("summary", "sequencing_rationale"):
        val = ai.get(field)
        if isinstance(val, str) and val.strip():
            new = _scrub(val, allowed_cves).strip()
            if new != plan.get(field):
                change(field, plan.get(field), new)
                plan[field] = new

    target = ai.get("target_state")
    if isinstance(target, str) and target.strip():
        new = _scrub(target, allowed_cves).strip()
        cited = {v.lower() for v in _VERSIONISH.findall(new)}
        if cited - allowed_versions:
            new += UNVERIFIED_VERSION_LABEL
        if new != plan.get("target_state"):
            change("target_state", plan.get("target_state"), new)
            plan["target_state"] = new

    by_step = {s["step"]: s for s in plan.get("steps", [])}
    for raw in ai.get("steps") or []:
        if not isinstance(raw, dict):
            continue
        step = by_step.get(raw.get("step")) if isinstance(raw.get("step"), int) else None
        if step is None:
            continue
        touched = False
        if isinstance(raw.get("description"), str) and raw["description"].strip():
            new = _scrub(raw["description"], allowed_cves).strip()
            if new != step["description"]:
                change("description", step["description"], new, step["step"])
                step["description"] = new
                touched = True
        if "commands" in raw:
            cmds, dropped = _safe_cmds(raw["commands"], guard)
            if dropped:
                step["unsafe_commands_removed"] = True
            if cmds and cmds != step.get("commands_for_os"):
                change("commands", step.get("commands_for_os"), cmds, step["step"])
                step["commands_for_os"] = cmds
                touched = True
        if isinstance(raw.get("pre_checks"), list):
            pre = [_scrub(p, allowed_cves) for p in raw["pre_checks"][:6] if str(p).strip()]
            if pre and pre != step.get("pre_checks"):
                change("pre_checks", step.get("pre_checks"), pre, step["step"])
                step["pre_checks"] = pre
                touched = True
        if isinstance(raw.get("rollback"), str) and raw["rollback"].strip():
            new = _scrub(raw["rollback"], allowed_cves).strip()
            if new != step.get("rollback"):
                change("rollback", step.get("rollback"), new, step["step"])
                step["rollback"] = new
                touched = True
        if touched:
            step["ai_changed"] = True

    extra = [x for x in (ai.get("additional_steps") or []) if isinstance(x, dict)][:MAX_EXTRA_STEPS]
    for raw in extra:
        title = _scrub(raw.get("title"), allowed_cves).strip()
        desc = _scrub(raw.get("description"), allowed_cves).strip()
        if not title or not desc:
            continue
        tier = raw.get("tier") if raw.get("tier") in TIERS else "hardening"
        cmds, dropped = _safe_cmds(raw.get("commands"), guard)
        new_step = {"step": len(plan["steps"]) + 1, "tier": tier, "title": title[:200],
                    "description": desc, "commands": {}, "commands_for_os": cmds, "pre_checks": [],
                    "reboot_required": None, "downtime": "", "rollback": "", "risk": "medium",
                    "verification": "", "ai_changed": True, "ai_added": True}
        if dropped:
            new_step["unsafe_commands_removed"] = True
        plan["steps"].append(new_step)
        change("step_added", None, title[:200], new_step["step"])

    plan["ai_changes"] = changes
    return plan, changes


def _request(context_payload: dict, *, bundle: bool):
    from app.schemas.ai import AiGenerateRequest, AiMessage
    subject = "fix bundle (every listed host)" if bundle else "finding"
    return AiGenerateRequest(
        task="remediation_refine",
        messages=[AiMessage(role="user", content=f"Refine the remediation plan for this {subject}.")],
        context=context_payload,
        max_tokens=1800,
    )


async def refine(db: Any, *, engagement: Any, kb_plan: dict, contexts: list[RemediationContext],
                 findings: list[Any], actor_id: Any, svc: Any = None) -> dict:
    """Run the refinement through the gateway; return the merged plan.

    Raises ``AiRuntimeError`` when no provider can serve (the caller maps it to
    503 and caches nothing). Audit records are persisted on success."""
    from app.ai.audit_chain import persist_ai_calls
    from app.services.domain_context import domain_brief_for
    from app.services.llm import AiRuntimeError, ManagerLlmService

    svc = svc or ManagerLlmService()
    payload = build_context_payload(kb_plan, contexts)
    brief = await domain_brief_for(db, engagement, findings[:10])
    text, runtime, _fallback = await svc.generate_with_fallback(
        _request(payload, bundle=len(contexts) > 1), domain_brief=brief.text if brief else None)
    await persist_ai_calls(db, list(getattr(svc, "audit_records", None) or []),
                           actor_id=actor_id, engagement_id=engagement.id)
    parsed = _extract_json(text or "")
    if parsed is None:
        raise AiRuntimeError("the model did not return a usable plan", 502)
    cves, versions = allowed_tokens(contexts)
    merged, changes = overlay(kb_plan, parsed, allowed_cves=cves, allowed_versions=versions,
                              guard=HallucinationGuard())
    merged["source"] = "ai"
    merged["model"] = runtime.model
    merged["provider"] = runtime.provider
    merged["provenance"] = {**merged.get("provenance", {}), "source": "ai_refinement",
                            "kb_recipe_id": kb_plan.get("recipe_id"), "changes": len(changes)}
    logger.info("remediation.refined", provider=runtime.provider, model=runtime.model,
                changes=len(changes), hosts=len(contexts))
    return merged
