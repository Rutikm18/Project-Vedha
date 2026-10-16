"""What each audit action means, in words a reader can use.

One place maps an action code to a category (the filter the page offers), a plain label,
and whether a customer may see it. An action not listed here still shows, labelled from
its code and filed under "Other", so a new event is never hidden by a missing entry.

Categories follow how auditors group evidence:
  authentication   sign-in, sign-out, MFA, API keys           (PCI 10.2.1.x, SOC 2 CC6.1)
  access_control   users, roles, customer access, denials      (PCI 10.2.1.5, ISO A.5.15)
  findings         triage, reopen, exceptions                  (SOC 2 CC7.x)
  scanning         scans, schedules, overrides, probes         (change of security posture)
  remediation      fix plans, deadline extensions
  reports          generated reports and briefs
  configuration    organisation settings, integrations, policy (PCI 10.2.1.6, ISO A.8.9)
  exploitation     approvals and execution of exploit steps
  other
"""
from __future__ import annotations

from dataclasses import dataclass

CATEGORIES: dict[str, str] = {
    "authentication": "Sign-in and sessions",
    "access_control": "Access control",
    "findings": "Findings",
    "scanning": "Scanning and probes",
    "remediation": "Remediation",
    "reports": "Reports",
    "configuration": "Configuration",
    "exploitation": "Exploitation",
    "other": "Other",
}


@dataclass(frozen=True)
class ActionInfo:
    category: str
    label: str
    customer_visible: bool = False


_A = ActionInfo
CATALOG: dict[str, ActionInfo] = {
    # authentication
    "auth.login.success": _A("authentication", "Signed in", True),
    "auth.login.failure": _A("authentication", "Sign-in failed", True),
    "auth.login.locked": _A("authentication", "Sign-in blocked after repeated failures", True),
    "auth.logout": _A("authentication", "Signed out", True),
    "auth.mfa.challenge_failed": _A("authentication", "Two-step code rejected", True),
    "auth.mfa.enabled": _A("authentication", "Two-step sign-in turned on", True),
    "auth.mfa.disabled": _A("authentication", "Two-step sign-in turned off", True),
    "auth.mfa.recovery_code_used": _A("authentication", "Recovery code used", True),
    "auth.mfa.recovery_codes_replaced": _A("authentication", "Recovery codes replaced", True),
    "auth.mfa.reset_by_admin": _A("authentication", "Two-step sign-in reset by an administrator", True),
    "auth.api_key.created": _A("authentication", "API key created"),
    "auth.api_key.revoked": _A("authentication", "API key revoked"),
    # access control
    "access.denied": _A("access_control", "Request refused: role not permitted"),
    "user.activated": _A("access_control", "User re-enabled"),
    "user.deactivated": _A("access_control", "User disabled"),
    "client_user.provisioned": _A("access_control", "Customer user created", True),
    "client_user.updated": _A("access_control", "Customer user changed", True),
    "client_user.password_revealed": _A("access_control", "Customer password shown to an administrator"),
    "entitlement.configured": _A("access_control", "Customer plan configured", True),
    "entitlement.adjusted": _A("access_control", "Customer plan adjusted", True),
    "agent.access_expiry.set": _A("access_control", "Probe access expiry set"),
    "agent.revoked": _A("access_control", "Probe access revoked"),
    # findings
    "finding.updated": _A("findings", "Finding changed", True),
    "finding.reopened": _A("findings", "Finding reopened", True),
    "finding.compliance_brief": _A("findings", "Compliance brief generated", True),
    "portal.finding.compliance_brief": _A("findings", "Compliance brief generated", True),
    "asset.tags.update": _A("findings", "Asset tags changed"),
    # scanning
    "scan_job.created": _A("scanning", "Scan started", True),
    "scan_job.cancelled": _A("scanning", "Scan cancelled", True),
    "scan_request.created": _A("scanning", "Scan requested", True),
    "scan_request.approved": _A("scanning", "Scan request approved", True),
    "scan_request.rejected": _A("scanning", "Scan request declined", True),
    "scan_schedule.created": _A("scanning", "Scan schedule created"),
    "scan_schedule.updated": _A("scanning", "Scan schedule changed"),
    "scan_schedule.deleted": _A("scanning", "Scan schedule removed"),
    "scan.blackout_override": _A("scanning", "Scan run through a blackout window"),
    "scan.fragile_override": _A("scanning", "Scan run against fragile targets"),
    "probe.enrollment.approved": _A("scanning", "Probe enrolment approved"),
    "probe.enrollment_token.created": _A("scanning", "Probe enrolment token created"),
    "probe.enrollment_token.revoked": _A("scanning", "Probe enrolment token revoked"),
    "portal.agent.assigned": _A("scanning", "Probe assigned", True),
    "engagement.agent_assigned": _A("scanning", "Probe assigned", True),
    # remediation
    "remediation.published": _A("remediation", "Fix plan published", True),
    "remediation.workspace_previewed": _A("remediation", "Fix workspace previewed"),
    "remediation.extension_requested": _A("remediation", "Deadline extension requested", True),
    "remediation.extension_withdrawn": _A("remediation", "Deadline extension withdrawn", True),
    "remediation.extension_approved": _A("remediation", "Deadline extension approved", True),
    "remediation.extension_rejected": _A("remediation", "Deadline extension declined", True),
    # reports
    "report.ai_generated": _A("reports", "AI report section generated", True),
    "portal.assistant.chat": _A("reports", "Assistant used", True),
    # configuration
    "engagement.created": _A("configuration", "Engagement created", True),
    "engagement.updated": _A("configuration", "Engagement changed", True),
    "portal.engagement.updated": _A("configuration", "Engagement changed", True),
    "portal.engagement.evidence_imported": _A("configuration", "Evidence imported", True),
    "engagement.profile.update": _A("configuration", "Compliance profile changed", True),
    "integration.updated": _A("configuration", "Integration changed"),
    "integration.deleted": _A("configuration", "Integration removed"),
    "notification_rules.updated": _A("configuration", "Notification rules changed"),
    "sla_policy.updated": _A("configuration", "SLA policy changed"),
    "intel_bundle.installed": _A("configuration", "Intelligence bundle installed"),
    "intel_bundle.rejected": _A("configuration", "Intelligence bundle rejected"),
    "audit.exported": _A("configuration", "Audit log exported"),
    # exploitation
    "exploit.approval_required": _A("exploitation", "Exploit approval requested"),
    "exploit.approval.approved": _A("exploitation", "Exploit approved"),
    "exploit.approval.rejected": _A("exploitation", "Exploit declined"),
    "exploit.execute.start": _A("exploitation", "Exploit run started"),
    "exploit.execute.complete": _A("exploitation", "Exploit run finished"),
}


# The leading part of an action code, for actions the catalogue does not list.
HEAD_CATEGORY: dict[str, str] = {
    "auth": "authentication", "access": "access_control", "user": "access_control",
    "client_user": "access_control", "finding": "findings", "scan": "scanning",
    "scan_job": "scanning", "scan_request": "scanning", "scan_schedule": "scanning",
    "probe": "scanning", "remediation": "remediation", "report": "reports",
    "org_settings": "configuration", "integration": "configuration",
    "engagement": "configuration", "exploit": "exploitation",
}


def _from_code(action: str) -> ActionInfo:
    head = action.split(".", 1)[0]
    return ActionInfo(HEAD_CATEGORY.get(head, "other"), action.replace("_", " ").replace(".", " · "), False)


def describe(action: str) -> ActionInfo:
    """Category, label and customer visibility for an action code."""
    if action in CATALOG:
        return CATALOG[action]
    if action.startswith("org_settings.") and action.endswith(".updated"):
        section = action.split(".")[1].replace("-", " ")
        return ActionInfo("configuration", f"Organisation {section} policy changed", False)
    return _from_code(action)


def category_clause(column, category: str):
    """SQL condition selecting a category's entries: catalogued actions plus any action
    whose leading part belongs to the category. "other" is everything else."""
    from sqlalchemy import and_, not_, or_

    def _in(cat: str):
        exact = [code for code, info in CATALOG.items() if info.category == cat]
        elsewhere = [code for code, info in CATALOG.items() if info.category != cat]
        heads = [h for h, c in HEAD_CATEGORY.items() if c == cat]
        # A catalogued action belongs to its catalogued category, whatever its prefix.
        return or_(column.in_(exact),
                   *[and_(column.like(f"{h}.%"), not_(column.in_(elsewhere))) for h in heads])

    if category == "other":
        return and_(*[not_(_in(c)) for c in CATEGORIES if c != "other"])
    return _in(category)


def customer_visible_actions() -> list[str]:
    return [code for code, info in CATALOG.items() if info.customer_visible]
