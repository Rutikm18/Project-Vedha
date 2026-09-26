"""
plan.py — assemble a contextual remediation plan (pure).

``build_plan(finding, ctx)`` resolves the recipe for the finding, fills its
templates with the recorded facts (a missing fact renders "not recorded"),
selects commands for the OS the scan saw, and returns the plan dict the API,
the report and the tracker all consume.

The dict is a SUPERSET of the pre-v2 KB plan contract (``category``, ``source``,
``steps[].commands_for_os`` …) so older clients keep working.

Urgency is a CISA SSVC-shaped label (act / attend / track* / track) derived
from signals already on the finding. It is informational: the due date always
comes from the configured SLA (services/deadlines.py), never from this label.
"""
from __future__ import annotations

from typing import Any

from app.remediation.context import NOT_RECORDED, RemediationContext
from app.remediation.recipes import Recipe, resolve_recipe
from app.services.project_time import project_now

FRAGILE_PREFIX = ("Coordinate with the asset owner — no automated change on this fragile asset "
                  "({reason}). ")

_OS_FOR_FAMILY = {"windows": "windows", "linux": "linux", "macos": "macos", "network": "generic",
                  "unknown": "generic"}
_RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return NOT_RECORDED


def _enum(v: Any) -> Any:
    return getattr(v, "value", v)


def target_state_for(recipe: Recipe, ctx: RemediationContext) -> str:
    """The end state that closes the finding. For version-matched CVEs the fixed
    release comes from the vulnerability DB; without one the plan says so."""
    if recipe.recipe_id == "CVE-PATCH":
        product = ctx.text("product")
        if ctx.fixed_version:
            return f"{product} ≥ {ctx.fixed_version}"
        return (f"{product} at a release outside the affected range — confirm the fixed version "
                "in the vendor advisory")
    return recipe.target_state


def _fields(ctx: RemediationContext, finding: Any, target: str) -> _SafeDict:
    service = ctx.text("service_name")
    if service == NOT_RECORDED and ctx.product.recorded:
        service = str(ctx.product.value)
    values = {
        "host": ctx.text("host"), "ip": ctx.text("ip"), "port": ctx.text("port"),
        "product": ctx.text("product"), "version": ctx.text("version"), "os": ctx.text("os_version")
        if ctx.os_version.recorded else ctx.text("os"), "os_version": ctx.text("os_version"),
        "service": service if service != NOT_RECORDED else "the service",
        "fixed_version": ctx.fixed_version or NOT_RECORDED, "target": target,
        "title": getattr(finding, "title", "") or "this finding",
    }
    return _SafeDict(values)


def _fmt(text: str, values: _SafeDict) -> str:
    return text.format_map(values) if text else text


def _severity(finding: Any) -> str:
    return str(_enum(getattr(finding, "severity", "")) or "").lower()


def urgency_for(ctx: RemediationContext, severity: str) -> dict:
    """SSVC-shaped urgency (informational). Decision points:
    exploitation (active: KEV · poc: EPSS ≥ 0.5 or reproduced · none),
    automatable (internet-facing), technical impact (total for critical),
    mission prevalence (asset criticality)."""
    drivers: list[str] = []
    if ctx.kev:
        exploitation = "active"
        drivers.append("On the CISA Known Exploited Vulnerabilities list")
    elif ctx.exploit_validated or (ctx.epss or 0) >= 0.5:
        exploitation = "poc"
        if ctx.exploit_validated:
            drivers.append("Reproduced during this assessment")
        if (ctx.epss or 0) >= 0.5:
            drivers.append(f"EPSS {ctx.epss:.2f} (high exploitation probability)")
    else:
        exploitation = "none"
    automatable = ctx.exposure == "internet"
    if automatable:
        drivers.append("Internet-facing")
    total = severity == "critical"
    if total:
        drivers.append("Critical technical impact")
    crit = str(ctx.criticality.value or "").lower() if ctx.criticality.recorded else ""
    mission = "high" if crit in ("critical", "high") else "medium" if crit == "medium" else "low"
    if mission == "high":
        drivers.append(f"Asset criticality {crit}")

    if exploitation == "active" and automatable and (total or mission == "high"):
        label = "act"
    elif exploitation == "active":
        label = "attend"
    elif exploitation == "poc" and mission == "high":
        label = "attend"
    elif exploitation == "poc" and total and automatable:
        label = "track_star"
    else:
        label = "track"
    return {"label": label, "drivers": drivers, "framework": "CISA SSVC (informational)"}


def _commands_for(step_cmds: dict[str, tuple[str, ...]], os: str, family: str) -> list[str]:
    order = [os]
    if family == "network":
        order.append("network")
    order.append("generic")
    for key in order:
        if step_cmds.get(key):
            return list(step_cmds[key])
    return []


def build_plan(finding: Any, ctx: RemediationContext, *, due: dict | None = None,
               os: str | None = None) -> dict:
    recipe = resolve_recipe(ctx, finding)
    target_raw = target_state_for(recipe, ctx)
    values = _fields(ctx, finding, "")
    target = _fmt(target_raw, values)
    values["target"] = target

    os_auto = _OS_FOR_FAMILY.get(ctx.os_family, "generic")
    selected = os if os in ("windows", "linux", "macos", "generic") else os_auto

    prefix = FRAGILE_PREFIX.format(reason=ctx.fragile_reason) if ctx.fragile else ""
    steps: list[dict] = []
    for i, s in enumerate(recipe.steps, start=1):
        commands = {k: [_fmt(c, values) for c in v] for k, v in s.commands.items()}
        steps.append({
            "step": i,
            "tier": s.tier,
            "title": _fmt(s.title, values),
            "description": prefix + _fmt(s.description, values),
            "commands": commands,
            "commands_for_os": _commands_for({k: tuple(v) for k, v in commands.items()},
                                             selected, ctx.os_family),
            "pre_checks": [_fmt(p, values) for p in s.pre_checks],
            "reboot_required": s.reboot_required,
            "downtime": _fmt(s.downtime, values),
            "rollback": _fmt(s.rollback, values),
            "risk": s.risk,
            "verification": "",
        })
    worst = max((s["risk"] for s in steps), key=lambda r: _RISK_ORDER.get(r, 0), default="low")

    v = recipe.verification
    manual = v.manual.get(selected) or v.manual.get("linux" if selected == "generic" else selected) or ""
    verification_check = {
        "scanner": v.scanner,
        "check": _fmt(v.check, values),
        "expected": _fmt(v.expected, values),
        "manual_command": _fmt(manual, values) if manual else "",
    }

    references = list(recipe.references)
    for cve in ctx.cve_ids:
        if cve not in references:
            references.insert(0, cve)

    title = _fmt(recipe.title, values)
    return {
        "category": recipe.recipe_id,
        "recipe_id": recipe.recipe_id,
        "recipe_version": recipe.version,
        "os": selected,
        "os_auto": os_auto,
        "source": "deterministic_kb",
        "title": title,
        "summary": f"{title}. Target: {target}.",
        "effort": recipe.effort,
        "remediation_risk": worst,
        "remediation_type": recipe.remediation_type,
        "risk_response": recipe.risk_response,
        "target_state": target,
        "urgency": urgency_for(ctx, _severity(finding)),
        "due": dict(due) if due else {"at": None, "source": None},
        "context": ctx.as_dict(),
        "exposure": ctx.exposure,
        "steps": steps,
        "verification": [f"{verification_check['check']} — expected: {verification_check['expected']}"],
        "verification_check": verification_check,
        "long_term_recommendations": [_fmt(t, values) for t in recipe.long_term],
        "compensating_controls": _fmt(recipe.compensating_controls, values),
        "references": references,
        "fragile_guard": {"active": ctx.fragile, "reason": ctx.fragile_reason},
        "provenance": {
            "source": "kb",
            "recipe_id": recipe.recipe_id,
            "recipe_version": recipe.version,
            "facts_used": ctx.facts_used(),
            "generated_at": project_now().isoformat(),
        },
    }
