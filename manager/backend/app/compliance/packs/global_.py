"""Global, tag-triggered — SWIFT Customer Security Controls Framework.

PCI DSS, ISO 27001, NIST 800-53, SOC 2 and HIPAA live in
app.services.finding_compliance (always shown)."""
from __future__ import annotations

from app.compliance.registry import C, Framework, register

register(
    Framework(
        id="swift_cscf", name="SWIFT Customer Security Controls Framework (CSCF)",
        authority="SWIFT (Customer Security Programme)",
        source="SWIFT CSCF — mandatory and advisory controls",
        jurisdictions=("GLOBAL",), sectors=(), granularity="control",
        trigger_tags=frozenset({"compliance_scope:swift_cscf_scope"}),
        themes={
            "asset_inventory": C("1.1 SWIFT Environment Protection", why="The secure zone must be scoped and isolated."),
            "secure_configuration": C("2.3 System Hardening", why="SWIFT-related systems must be hardened."),
            "patch_vulnerability_mgmt": C("2.2 Security Updates", "2.7 Vulnerability Scanning",
                                          why="Security updates and vulnerability scanning are mandatory."),
            "access_control": C("5.1 Logical Access Control", "1.2 Operating System Privileged Account Control",
                                why="Access must follow least privilege."),
            "authentication": C("4.1 Password Policy", "4.2 Multi-Factor Authentication",
                                why="Strong passwords and MFA are mandatory."),
            "remote_access": C("1.1 SWIFT Environment Protection", "4.2 Multi-Factor Authentication",
                               why="Access into the secure zone must be restricted and use MFA."),
            "network_security": C("1.1 SWIFT Environment Protection", "1.4 Restriction of Internet Access",
                                  why="The secure zone must be segregated from the wider network."),
            "crypto_in_transit": C("2.1 Internal Data Flow Security", "2.6 Operator Session Confidentiality and Integrity",
                                   why="Data flows and operator sessions must be protected."),
            "data_protection": C("2.1 Internal Data Flow Security", why="Transaction data must be protected."),
            "logging_monitoring": C("6.4 Logging and Monitoring", why="Security events must be logged and monitored."),
            "incident_response": C("7.1 Cyber Incident Response Planning", why="An incident response plan is mandatory."),
        },
        baseline=C("1.1 SWIFT Environment Protection", why="The SWIFT secure zone must be protected."),
        note="Applies to assets tagged as in SWIFT CSCF scope; confirm your architecture type (A1–B).",
    ),
)
