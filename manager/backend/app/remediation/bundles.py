"""
bundles.py — deterministic fix bundles (pure).

A bundle is ONE unit of work that closes many findings: "disable SMBv1" across
fourteen hosts, "upgrade OpenSSH to ≥ 9.8p1" closing every OpenSSH CVE on a box.
Bundles are derived live from findings + context; nothing here is persisted.

Identity (``fix_key``) is a hash of the recipe, the product family and the
normalised target state, so the same fix yields the same key on every scan and
customer extension requests / tickets never point at the wrong item. Two
deliberate exceptions:
  * CVE-PATCH keys on the product only; the bundle's target becomes the highest
    fixed release among its members (one upgrade closes them all).
  * GENERIC keys on the finding itself — unrelated findings never merge.

Each finding keeps its own record; a bundle is a view. Hosts close one by one on
their own retest, which is what the per-host checklist shows.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Any

from app.remediation.context import NOT_RECORDED, RemediationContext
from app.remediation.plan import _SafeDict, _severity, build_plan, os_for_context, urgency_for
from app.remediation.recipes import resolve_recipe

_URGENCY_RANK = {"act": 3, "attend": 2, "track_star": 1, "track": 0}
_EXCLUDED = {"accepted": "risk accepted", "fp": "false positive"}
_OPEN = {"open", "confirmed"}


def _enum(v: Any) -> Any:
    return getattr(v, "value", v)


def _norm(text: str | None) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def product_family(ctx: RemediationContext) -> str:
    """The device/software identity a fix applies to — product, else service.
    Normalised so banner casing/padding never splits a bundle (mirrors the
    detection engine's ``group_key_for`` signature)."""
    if ctx.product.recorded:
        return _norm(ctx.product.value)
    if ctx.service_name.recorded:
        return _norm(ctx.service_name.value)
    return ""


def fix_key_for(recipe_id: str, family: str, target_state: str) -> str:
    raw = f"{recipe_id}|{_norm(family)}|{_norm(target_state)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def fix_ref(fix_key: str) -> str:
    return "FIX-" + fix_key[:6].upper()


def _version_key(v: str) -> list:
    """Natural ordering for release strings (9.8p1 > 8.8p1, 2.4.10 > 2.4.9)."""
    return [(0, int(p)) if p.isdigit() else (1, p) for p in re.findall(r"\d+|[a-z]+", str(v).lower())]


def _as_dt(v: Any) -> datetime | None:
    if isinstance(v, datetime):
        return v
    if isinstance(v, str) and v:
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return None
    return None


def _member_state(finding: Any) -> tuple[str, str | None]:
    status = str(_enum(getattr(finding, "status", "open")) or "open").lower()
    if status in _OPEN:
        return "open", None
    if status in _EXCLUDED:
        return "excluded", _EXCLUDED[status]
    return "closed", None


def _key_for(finding: Any, ctx: RemediationContext) -> tuple[str, str, str]:
    """(fix_key, recipe_id, family)."""
    recipe = resolve_recipe(ctx, finding)
    family = product_family(ctx)
    if recipe.recipe_id == "GENERIC":
        return fix_key_for("GENERIC", str(getattr(finding, "id", "")), ""), recipe.recipe_id, family
    if recipe.recipe_id == "CVE-PATCH":
        return fix_key_for("CVE-PATCH", family, ""), recipe.recipe_id, family
    plan_target = build_plan(finding, ctx)["target_state"]
    return fix_key_for(recipe.recipe_id, family, plan_target), recipe.recipe_id, family


def _title(recipe_title: str, ctx: RemediationContext, n_hosts: int, finding: Any) -> str:
    host = ctx.text("host") if n_hosts == 1 else f"{n_hosts} hosts"
    values = _SafeDict({
        "host": host, "product": ctx.text("product"), "service": ctx.text("service_name")
        if ctx.service_name.recorded else "the service",
        "port": ctx.text("port"), "ip": ctx.text("ip") if n_hosts == 1 else f"{n_hosts} hosts",
        "title": getattr(finding, "title", "") or "this finding",
    })
    return recipe_title.format_map(values)


def build_bundles(items: list[tuple[Any, RemediationContext, dict | None]], *, now: datetime) -> list[dict]:
    """Group ``(finding, context, due)`` items into ordered fix bundles."""
    groups: dict[str, dict[str, Any]] = {}
    for finding, ctx, due in items:
        key, recipe_id, family = _key_for(finding, ctx)
        g = groups.setdefault(key, {"recipe_id": recipe_id, "family": family, "members": []})
        g["members"].append((finding, ctx, due or {}))

    bundles = [_assemble(key, g) for key, g in groups.items()]
    open_b = [b for b in bundles if b["status"] == "open"]
    done_b = [b for b in bundles if b["status"] == "done"]
    open_b.sort(key=lambda b: (_due_sort(b["due_at"]), -len(b["resolves"]), b["ref"]))
    done_b.sort(key=lambda b: b["ref"])
    return open_b + done_b


def _assemble(key: str, g: dict) -> dict:
    members = g["members"]
    rep_finding, rep_ctx, _ = members[0]
    rep_plan = build_plan(rep_finding, rep_ctx)
    recipe = resolve_recipe(rep_ctx, rep_finding)

    # One representative plan per OS family present → steps grouped by OS.
    steps_by_os: dict[str, list[dict]] = {}
    for f, ctx, _ in members:
        os_name = os_for_context(ctx)
        if os_name not in steps_by_os:
            steps_by_os[os_name] = build_plan(f, ctx, os=os_name)["steps"]

    target = rep_plan["target_state"]
    if g["recipe_id"] == "CVE-PATCH":
        fixed = [c.fixed_version for _, c, _ in members if c.fixed_version]
        if fixed:
            product = rep_ctx.text("product")
            target = f"{product} ≥ {max(fixed, key=_version_key)}"

    hosts: dict[str, dict] = {}
    resolves: list[str] = []
    open_ids: list[str] = []
    excluded: list[dict] = []
    open_count = closed_count = 0
    open_dues: list[tuple[datetime, str | None]] = []
    urgency = "track"
    sev_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
    max_sev, any_kev = "info", False
    for f, ctx, due in members:
        fid = str(getattr(f, "id", ""))
        state, reason = _member_state(f)
        ip = ctx.text("ip")
        h = hosts.setdefault(ip, {
            "host": ctx.text("host"), "ip": ip,
            "os": ctx.text("os_version") if ctx.os_version.recorded else ctx.text("os"),
            "os_family": ctx.os_family, "ports": [], "finding_ids": [], "states": [],
            "due_at": None, "due_source": None, "closed_at": None,
        })
        port = ctx.port.value if ctx.port.recorded else None
        if port is not None and port not in h["ports"]:
            h["ports"].append(port)
        h["finding_ids"].append(fid)
        h["states"].append((state, due.get("source")))
        if state == "excluded":
            excluded.append({"finding_id": fid, "reason": reason})
            continue
        resolves.append(fid)
        if state == "closed":
            closed_count += 1
            h["closed_at"] = getattr(f, "resolved_at", None) or h["closed_at"]
            continue
        open_count += 1
        open_ids.append(fid)
        at = _as_dt(due.get("at"))
        if at is not None:
            open_dues.append((at, due.get("source")))
            if h["due_at"] is None or at < h["due_at"]:
                h["due_at"], h["due_source"] = at, due.get("source")
        sev = _severity(f)
        if sev_rank.get(sev, 0) > sev_rank[max_sev]:
            max_sev = sev
        any_kev = any_kev or ctx.kev
        u = urgency_for(ctx, sev)["label"]
        if _URGENCY_RANK[u] > _URGENCY_RANK[urgency]:
            urgency = u

    host_rows = []
    for h in hosts.values():
        states = h.pop("states")
        open_states = [s for s in states if s[0] == "open"]
        if open_states:
            h["status"] = ("extension_approved" if all(src == "extension" for _, src in open_states)
                           else "open")
        elif any(s[0] == "closed" for s in states):
            h["status"] = "closed"
        else:
            h["status"] = "excluded"
        host_rows.append(h)
    host_rows.sort(key=lambda r: (r["status"] != "open", r["ip"]))

    due_at, due_source = (min(open_dues, key=lambda d: d[0]) if open_dues else (None, None))
    return {
        "fix_key": key,
        "ref": fix_ref(key),
        "recipe_id": g["recipe_id"],
        "product_family": g["family"] or None,
        "title": _title(recipe.title, rep_ctx, len(hosts), rep_finding),
        "remediation_type": rep_plan["remediation_type"],
        "risk_response": rep_plan["risk_response"],
        "target_state": target,
        "effort": rep_plan["effort"],
        "remediation_risk": rep_plan["remediation_risk"],
        "steps_by_os": steps_by_os,
        "verification_check": rep_plan["verification_check"],
        "compensating_controls": rep_plan["compensating_controls"],
        "references": rep_plan["references"],
        "hosts": host_rows,
        "resolves": resolves,
        "open_finding_ids": open_ids,
        "excluded": excluded,
        "open_count": open_count,
        "closed_count": closed_count,
        "due_at": due_at,
        "due_source": due_source,
        "urgency": urgency,
        # Open members only — drives the "compensating control required" rule.
        "max_severity": max_sev if open_count else None,
        "kev": any_kev,
        "progress": {"closed": closed_count, "total": open_count + closed_count},
        "status": "open" if open_count else "done",
    }


def bundle_link(finding: Any, ctx: RemediationContext) -> dict:
    """The fix bundle a single finding belongs to (key + display ref)."""
    key, recipe_id, _ = _key_for(finding, ctx)
    return {"fix_key": key, "ref": fix_ref(key), "recipe_id": recipe_id}


def by_host(bundles: list[dict]) -> list[dict]:
    """Pivot bundles into host → the bundles it needs, soonest due first."""
    hosts: dict[str, dict] = {}
    for b in bundles:
        for h in b["hosts"]:
            row = hosts.setdefault(h["ip"], {"host": h["host"], "ip": h["ip"], "os": h["os"],
                                             "bundles": []})
            row["bundles"].append({
                "fix_key": b["fix_key"], "ref": b["ref"], "recipe_id": b["recipe_id"],
                "title": b["title"], "target_state": b["target_state"],
                "remediation_type": b["remediation_type"], "urgency": b["urgency"],
                "status": h["status"], "due_at": h["due_at"], "due_source": h["due_source"],
                "finding_ids": h["finding_ids"], "ports": h["ports"],
            })
    out = list(hosts.values())
    for row in out:
        row["bundles"].sort(key=lambda x: (_due_sort(x["due_at"]), x["ref"]))
        row["open_count"] = sum(1 for x in row["bundles"] if x["status"] in ("open", "extension_approved"))
        dues = [x["due_at"] for x in row["bundles"] if x["due_at"] is not None]
        row["next_due_at"] = min(dues) if dues else None
    out.sort(key=lambda r: (_due_sort(r["next_due_at"]), r["ip"]))
    return out


def _due_sort(d: datetime | None) -> tuple[bool, float]:
    """Soonest first, undated last — without comparing naive and aware values."""
    return (d is None, d.timestamp() if d is not None else 0.0)


__all__ = ["NOT_RECORDED", "build_bundles", "bundle_link", "by_host", "fix_key_for", "fix_ref",
           "product_family"]
