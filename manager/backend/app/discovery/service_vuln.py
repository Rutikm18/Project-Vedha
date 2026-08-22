"""
service_vuln.py — turn network-service banner facts into Finding rows.

WHY THIS EXISTS: a port/service scan captures a service's product + version and
its advertised crypto (e.g. the SSH KEXINIT algorithm lists) in `service_banner`
facts, but nothing converted those into dashboard findings. The Debian-OSV/KEV
detection engine (app.detection.engine_bridge) matches *package* inventory, not
network banners, and finding_translator only persists findings the probe already
self-assessed (TLS/SMB). So a genuinely outdated SSH daemon or a service still
offering SHA-1 / DSA crypto — visible right there in the banner — fell in a
coverage gap and produced zero findings.

This is that missing bridge for network services: a small, deterministic rule
set over the structured banner facts. It does NOT invent an intel feed — every
rule keys on something concrete in the fact (product/version, or a weak
algorithm token the server itself advertised).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.discovery.finding_translator import _resolve_asset, _find_open_duplicate

logger = structlog.get_logger()

# SSH algorithm tokens that are cryptographically deprecated. Each maps to the
# reason it is flagged; presence in the KEXINIT banner is sufficient evidence.
_WEAK_SSH_ALGOS = {
    "ssh-dss": "DSA host keys (1024-bit, deprecated by OpenSSH 7.0)",
    "diffie-hellman-group1-sha1": "SHA-1 / 1024-bit MODP key exchange",
    "diffie-hellman-group14-sha1": "SHA-1 key exchange",
    "hmac-sha1": "SHA-1 message authentication",
    "hmac-md5": "MD5 message authentication",
    "arcfour": "RC4 stream cipher (broken)",
    "3des-cbc": "3DES (64-bit block, Sweet32)",
}

def _new_finding(engagement_id, asset, *, title, severity, description,
                 remediation, evidence, cvss, cve_ids=None) -> Finding:
    now = datetime.now(timezone.utc)
    return Finding(
        engagement_id=engagement_id,
        asset_id=asset.id if asset else None,
        title=title,
        description=description,
        severity=severity,
        status=FindingStatus.open,
        cve_ids=cve_ids or None,
        cvss_score=Decimal(str(cvss)) if cvss is not None else None,
        remediation=remediation,
        evidence=evidence,
        first_seen=now,
        last_seen=now,
    )


def _ssh_rules(data: dict, banner: str, port: int, target: str) -> list[dict]:
    """SSH hygiene findings the CVE engine does NOT cover.

    Outdated-version → CVE matching now lives in the detection engine
    (cpe_normalizer + NVD/CPE snapshot → matcher), so it is intentionally NOT
    duplicated here. What remains is the crypto-negotiation weakness the engine
    can't see: the algorithms the server advertises in its KEXINIT banner.
    """
    out: list[dict] = []

    # Weak advertised crypto (KEXINIT tokens the server itself offered).
    low_banner = banner.lower()
    weak = sorted({name for name in _WEAK_SSH_ALGOS if name in low_banner})
    if weak:
        reasons = "; ".join(f"{n} — {_WEAK_SSH_ALGOS[n]}" for n in weak)
        out.append(dict(
            title="Weak SSH cryptographic algorithms offered",
            severity=FindingSeverity.medium, cvss=5.9, cve_ids=None,
            description=(
                f"The SSH service on port {port} advertises deprecated algorithms: "
                f"{reasons}. A network attacker can negotiate the weakest option, "
                "undermining confidentiality/integrity of the session."
            ),
            remediation=("Disable legacy host keys (ssh-dss), SHA-1/group1 key "
                         "exchange, and HMAC-SHA1/MD5. Offer only curve25519 / "
                         "ecdh-sha2-nistp256+, AES-GCM, and HMAC-SHA2."),
            evidence={"port": port, "weak_algorithms": weak},
        ))
    return out


def _http_rules(data: dict, banner: str, port: int, target: str) -> list[dict]:
    """Findings for an HTTP service, from its Server header / banner."""
    out: list[dict] = []
    text = f"{banner} {data.get('product') or ''}".lower()
    if "thttpd" in text:
        out.append(dict(
            title="Legacy embedded web server exposed (thttpd)",
            severity=FindingSeverity.low, cvss=3.7, cve_ids=None,
            description=(
                f"Port {port} serves thttpd, a minimal embedded web server most "
                "often fronting a router/IoT administration interface. Exposing it "
                "broadens attack surface and frequently ships on unpatched firmware."
            ),
            remediation=("Restrict the admin interface to trusted networks/VPN and "
                         "keep device firmware current."),
            evidence={"port": port, "server": "thttpd",
                      "banner_first_line": data.get("first_line")},
        ))
    return out


# Cleartext / legacy protocols that are a finding purely by being open.
_CLEARTEXT_PORTS = {
    21: ("FTP", "credentials and data traverse the network in cleartext"),
    23: ("Telnet", "credentials and the entire session traverse the network in cleartext"),
    69: ("TFTP", "unauthenticated file transfer with no encryption"),
    512: ("rexec", "legacy remote execution with cleartext credentials"),
    513: ("rlogin", "legacy remote login with cleartext credentials"),
}


def _cleartext_rule(port: int, target: str) -> list[dict]:
    info = _CLEARTEXT_PORTS.get(port)
    if not info:
        return []
    name, why = info
    return [dict(
        title=f"Cleartext service exposed ({name})",
        severity=FindingSeverity.medium, cvss=5.9, cve_ids=None,
        description=f"{name} is open on port {port}: {why}.",
        remediation=f"Disable {name} and use an encrypted equivalent (e.g. SSH/SFTP/HTTPS).",
        evidence={"port": port, "service": name},
    )]


async def create_service_vuln_findings(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
) -> int:
    """Scan the result's `facts` for weak/outdated network services and persist
    Finding rows. Idempotent per (engagement, asset, title). Returns the count
    created. Best-effort: the caller wraps this so a rule bug never fails submit.
    """
    facts = result.get("facts") if isinstance(result, dict) else None
    if not isinstance(facts, list):
        return 0

    created = 0
    for fact in facts:
        if not isinstance(fact, dict) or fact.get("status") != "open":
            continue
        data = fact.get("data") if isinstance(fact.get("data"), dict) else {}
        port = fact.get("port")
        target = fact.get("target")
        banner = data.get("banner") or ""
        service = (data.get("service") or "").lower()

        candidates: list[dict] = []
        if service == "ssh" or port == 22:
            candidates += _ssh_rules(data, banner, port, target)
        if service in ("http", "https") or port in (80, 443, 8080, 8443):
            candidates += _http_rules(data, banner, port, target)
        candidates += _cleartext_rule(port, target)
        if not candidates:
            continue

        asset = await _resolve_asset(db, engagement_id, target)
        for c in candidates:
            if await _find_open_duplicate(db, engagement_id, asset.id if asset else None, c["title"]):
                continue
            db.add(_new_finding(engagement_id, asset, **c))
            created += 1

    if created:
        await db.flush()
        logger.info("service_vuln.created", engagement_id=str(engagement_id), count=created)
    return created
