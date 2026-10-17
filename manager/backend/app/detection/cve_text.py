"""
cve_text.py — the description and remediation a version-matched CVE finding shows.

Pure: reads only the detection engine's CVE record (the dict persisted as the
finding's evidence) and returns plain text. Nothing is guessed: a missing port or fix
version is left out of the sentence, never printed as a placeholder, and the text
says how the version was observed, because that decides how far a client can trust it:

  * ``authoritative``      the host's own installed-package list;
  * ``package`` scheme     a Debian package version read from the banner;
  * ``upstream`` scheme    a banner's upstream version, which a distribution may
                           have patched without changing (backport caveat).

Banner text never reaches these strings: only the engine's own fields (product
name from the CPE vocabulary, versions it parsed, the CVE id) are used, each
bounded, so a hostile banner cannot write the finding's prose.
"""
from __future__ import annotations

import re
from typing import Any

# CPE product -> the name a client recognises. Anything else: underscores to spaces.
_PRODUCT_NAMES = {
    "openssh": "OpenSSH", "http_server": "Apache HTTP Server", "nginx": "nginx",
    "vsftpd": "vsftpd", "proftpd": "ProFTPD", "pure-ftpd": "Pure-FTPd",
    "samba": "Samba", "openssl": "OpenSSL", "bind": "BIND", "dnsmasq": "dnsmasq",
    "lighttpd": "lighttpd", "mariadb": "MariaDB", "mysql": "MySQL",
    "postgresql": "PostgreSQL", "redis": "Redis", "curl": "curl", "dropbear": "Dropbear SSH",
    "tomcat": "Apache Tomcat", "exim": "Exim", "postfix": "Postfix", "dovecot": "Dovecot",
    "squid": "Squid", "cups": "CUPS", "jenkins": "Jenkins", "docker": "Docker",
    "internet_information_services": "Microsoft IIS", "caddy": "Caddy",
}
_SSVC_DECISIONS = {"Track", "Track*", "Attend", "Act"}
_SAFE = re.compile(r"[^0-9A-Za-z.+~:_\-\[\]\(\), ]")
_CVE = re.compile(r"^(?:CVE-\d{4}-\d{4,7}|[A-Z]{2,10}-[\w.-]{1,40})$")


def _clean(value: Any, limit: int = 60) -> str | None:
    if value is None:
        return None
    text = _SAFE.sub("", str(value)).strip()[:limit]
    return text or None


def product_name(d: dict) -> str:
    product = _clean(d.get("product"), 40)
    if not product:
        cpe = str(d.get("cpe") or "").split(":")
        product = _clean(cpe[4], 40) if len(cpe) > 4 and cpe[4] not in ("*", "-") else None
    if not product:
        return "The affected product"
    return _PRODUCT_NAMES.get(product.lower(), product.replace("_", " "))


def _cve(d: dict) -> str:
    cve = str(d.get("cve_id") or "").strip().upper()
    return cve if _CVE.match(cve) else "this vulnerability"


def _where(d: dict) -> str:
    ports = [p for p in (d.get("ports") or [d.get("port")]) if isinstance(p, int)]
    proto = _clean(d.get("proto"), 8) or "tcp"
    if not ports:
        return ""
    listed = ", ".join(f"{p}/{proto}" for p in sorted(set(ports))[:6])
    return f" on port{'s' if len(set(ports)) > 1 else ''} {listed}"


def _observed_how(d: dict) -> str:
    if d.get("source_confidence") == "authoritative":
        return "from the host's installed-package list"
    if d.get("version_scheme") == "package":
        return "from the Debian package version the service banner names"
    return "from the service banner"


def cve_description(d: dict) -> str:
    name, cve = product_name(d), _cve(d)
    version = _clean(d.get("matched_version"), 40)
    seen = f"{name} {version}" if version else name
    text = (f"{seen} was observed{_where(d)} ({_observed_how(d)}). That version is in "
            f"the affected range for {cve} in the vulnerability database")
    rng = _clean(d.get("matched_range"), 80)
    text += f" ({rng})." if rng else "."
    ssvc = d.get("ssvc") if isinstance(d.get("ssvc"), dict) else None
    if ssvc and ssvc.get("decision") in _SSVC_DECISIONS:
        text += (f" CISA SSVC: {ssvc['decision']} (exploitation "
                 f"{_clean(ssvc.get('exploitation'), 10) or 'unknown'}, automatable "
                 f"{_clean(ssvc.get('automatable'), 5) or 'unknown'}, technical impact "
                 f"{_clean(ssvc.get('technical_impact'), 10) or 'unknown'}).")
    if d.get("source_confidence") != "authoritative" and d.get("version_scheme") != "package":
        text += (" A distribution may have backported the fix without changing the "
                 "version this service reports, so confirm the installed package before "
                 "treating it as exploitable.")
    return text


def cve_remediation(d: dict) -> str:
    name, cve = product_name(d), _cve(d)
    fix = _clean(d.get("fixed_version"), 60)
    where = _where(d).replace(" on port", " port") if _where(d) else ""
    restrict = (f" Until it is applied, restrict access to{where} to the hosts that need it."
                if where else "")
    if fix and (d.get("source_confidence") == "authoritative"
                or d.get("version_scheme") == "package"):
        return (f"Install the security update that brings the {name} package to {fix} or "
                f"later (for example with the system package manager), then restart the "
                f"service and re-scan.{restrict}")
    if fix:
        return (f"Upgrade {name} to {fix} or later, the first release that fixes {cve}. "
                f"If this host runs a distribution package, install the distribution's "
                f"security update for {cve} instead and confirm the installed package "
                f"version, then re-scan.{restrict}")
    return (f"No upstream release that fixes {cve} is recorded for this version. Check the "
            f"vendor or distribution advisory for {cve}, apply its update or mitigation, "
            f"then re-scan.{restrict}")


def is_engine_notes_description(text: str | None) -> bool:
    """True for the old auto-generated description (the matcher's notes joined with
    '; '), which a reaffirmation may replace; never for anything a person wrote."""
    return bool(text) and " | matched range " in text
