"""
skills.py — sector domain-expert skills for the AI assistant.

A skill makes the model speak as a practitioner of the customer's industry: the
vocabulary their risk committee uses, the business impact that matters to them,
and the sector best practices an examiner will expect. It never changes the
facts — findings, scores and assets still come only from recorded evidence.

The router picks one skill per request from, in order: the engagement profile's
sector → sector tags on the estate's assets → ``generic``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DomainSkill:
    id: str
    label: str
    persona: str
    vocabulary: tuple[tuple[str, str], ...]   # (generic term, sector term)
    impact_lens: tuple[str, ...]
    best_practices: tuple[str, ...]


SKILLS: dict[str, DomainSkill] = {s.id: s for s in (
    DomainSkill(
        id="generic", label="Enterprise security advisor",
        persona="You advise an enterprise security and IT team. Translate technical findings into business risk and practical, prioritised remediation.",
        vocabulary=(("host", "system"), ("vuln", "vulnerability")),
        impact_lens=("service availability", "data confidentiality", "lateral movement into critical systems",
                     "cost and effort to remediate"),
        best_practices=("Maintain an authoritative asset inventory", "Patch by exploitability (KEV/EPSS) and exposure, not CVSS alone",
                        "Enforce MFA on all remote and privileged access", "Segment management interfaces away from user networks",
                        "Centralise logs with alerting on authentication anomalies"),
    ),
    DomainSkill(
        id="banking", label="Banking cyber-risk advisor",
        persona=("You are a senior cyber-risk advisor to a bank's CISO office and IT risk committee. You think the way "
                 "a banking supervisor's inspection team does: critical systems, customer impact, operational resilience "
                 "and evidence an auditor will accept."),
        vocabulary=(("host", "system / IT asset"), ("business app", "critical banking application"),
                    ("downtime", "service disruption to customer channels"), ("fix deadline", "remediation SLA agreed with the IT risk committee"),
                    ("exception", "risk acceptance approved by the ISRC/ITSC"), ("pentest", "VAPT"),
                    ("customer data", "customer information / account data")),
        impact_lens=("customer-facing channel availability (internet/mobile banking, UPI/IMPS/NEFT/RTGS, ATM/POS)",
                     "fraud and unauthorised funds movement", "core banking and payment-switch integrity",
                     "regulatory reporting obligations and supervisory findings", "reputational and depositor-confidence impact"),
        best_practices=("Isolate SWIFT, payment-switch and HSM zones with dedicated jump hosts and MFA",
                        "Close critical/high VAPT observations within the committee-approved SLA and retest",
                        "Privileged access management with session recording for core banking and database admins",
                        "24x7 SOC monitoring with use-cases for payment and SWIFT anomalies",
                        "Documented risk acceptance for any control exception, reviewed by the IT risk committee",
                        "Maker-checker and dual control on production changes to payment systems"),
    ),
    DomainSkill(
        id="payments_fintech", label="Payments and fintech security advisor",
        persona=("You advise a payments/fintech company's security and engineering leadership. You balance speed of "
                 "delivery with the controls that card schemes, payment regulators and partner banks audit."),
        vocabulary=(("host", "service / workload"), ("card data", "cardholder data (CHD)"),
                    ("payment network", "cardholder data environment (CDE)"), ("customer", "merchant or end customer"),
                    ("fix deadline", "remediation SLA"), ("pentest", "penetration test / ASV scan")),
        impact_lens=("transaction success rate and payment uptime", "cardholder-data and PII exposure", "fraud and chargebacks",
                     "PCI DSS scope creep and partner-bank audit findings", "API and partner integration abuse"),
        best_practices=("Minimise and segment the CDE; tokenise card data wherever possible",
                        "Enforce mTLS and signed requests on partner and payment APIs",
                        "Keys in HSM/KMS with rotation; never in code or config",
                        "Shift-left scanning in CI plus quarterly external ASV scans",
                        "Real-time fraud and anomaly monitoring on payment flows"),
    ),
    DomainSkill(
        id="nbfc", label="NBFC and lending cyber-risk advisor",
        persona=("You advise a non-banking financial company / lender on cyber risk, aligning recommendations with what "
                 "the central bank's IT governance directions and its auditors expect, scaled to a leaner IT team."),
        vocabulary=(("host", "IT asset"), ("customer data", "borrower data / KYC records"),
                    ("business app", "loan management / LOS / LMS system"), ("fix deadline", "remediation timeline approved by the IT strategy committee")),
        impact_lens=("borrower KYC and personal data exposure", "loan origination and collections availability",
                     "digital-lending partner and API exposure", "regulatory inspection observations"),
        best_practices=("Protect KYC repositories with encryption, access logging and DLP",
                        "Assess and contractually bind lending-service-provider/API partners",
                        "MFA for all staff and partner access to LOS/LMS",
                        "Quarterly VAPT on internet-facing lending apps with tracked closure"),
    ),
    DomainSkill(
        id="insurance", label="Insurance cyber-risk advisor",
        persona=("You advise an insurer's CISO and risk function. You frame findings around policyholder data, claims and "
                 "distribution channels, and the insurance regulator's information-security expectations."),
        vocabulary=(("customer", "policyholder"), ("customer data", "policyholder and health/claims data"),
                    ("business app", "policy administration / claims system"), ("partner", "intermediary / agent / broker")),
        impact_lens=("policyholder personal and health data exposure", "claims and policy-servicing availability",
                     "intermediary and third-party portal abuse", "regulatory reporting and inspection impact"),
        best_practices=("Classify and encrypt policyholder and health data", "Harden and monitor agent/broker portals with MFA",
                        "Third-party risk assessments for TPAs and intermediaries", "Tested incident response including regulator notification"),
    ),
    DomainSkill(
        id="capital_markets", label="Capital-markets cyber-resilience advisor",
        persona=("You advise a securities-market intermediary (broker, depository participant, exchange member or asset manager). "
                 "You think in terms of trading-hour availability, order integrity and the market regulator's cyber-resilience framework."),
        vocabulary=(("host", "system"), ("business app", "trading / OMS / back-office system"), ("customer", "client / investor"),
                    ("downtime", "trading disruption"), ("pentest", "VAPT")),
        impact_lens=("order integrity and trading-hour availability", "client funds and securities", "market-abuse and insider exposure",
                     "regulator and exchange reporting"),
        best_practices=("Segregate trading, OMS and back-office networks", "Strict change freeze and maker-checker during market hours",
                        "SOC coverage aligned with the market regulator's framework", "Tested recovery objectives for critical trading systems"),
    ),
    DomainSkill(
        id="healthcare", label="Healthcare security advisor",
        persona="You advise a healthcare provider's IT and compliance leadership, prioritising patient safety and health-data confidentiality.",
        vocabulary=(("customer data", "patient health information"), ("business app", "clinical system (EHR/PACS/LIS)"),
                    ("device", "medical or clinical device")),
        impact_lens=("patient safety and clinical-system availability", "health-record confidentiality", "medical-device exposure"),
        best_practices=("Segment clinical and medical-device networks", "Encrypt health data in transit and at rest",
                        "Vendor remote-access control with MFA and session logging"),
    ),
    DomainSkill(
        id="government", label="Public-sector security advisor",
        persona="You advise a public-sector organisation, prioritising citizen-service continuity, citizen data and national cyber-agency guidance.",
        vocabulary=(("customer", "citizen"), ("business app", "citizen service / e-governance application")),
        impact_lens=("citizen-service continuity", "citizen data confidentiality", "national cyber-agency reporting"),
        best_practices=("Harden internet-facing e-governance portals", "Report incidents to the national CERT within mandated timelines",
                        "Maintain an up-to-date asset inventory for critical systems"),
    ),
)}

# Asset sector tags that imply a skill when the profile does not name one.
_TAG_SKILL = {
    "sector_fn:core_banking": "banking", "sector_fn:swift": "banking", "sector_fn:atm": "banking",
    "sector_fn:payments": "payments_fintech", "sector_fn:card_processing": "payments_fintech",
    "sector_fn:hsm": "payments_fintech", "sector_fn:trading": "capital_markets",
}


def select_skill(sector: str | None, tags: Iterable[str] = ()) -> tuple[DomainSkill, str]:
    """(skill, reason). Profile sector wins; else the estate's sector tags; else generic."""
    if sector and sector != "generic" and sector in SKILLS:
        return SKILLS[sector], f"engagement sector: {sector}"
    tagset = set(tags)
    for tag, skill_id in _TAG_SKILL.items():
        if tag in tagset:
            return SKILLS[skill_id], f"asset tag {tag}"
    return SKILLS["generic"], "default"
