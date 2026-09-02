"""
cpe.py — derive a CPE 2.3 identity from an observed (service, product, version).

This is a PROBE-side, DB-free enrichment: it turns the soft-matched
service/product/version that service_banner already extracts into a CPE the
manager-side CVE correlator can match against NVD. The probe still emits NO CVE
claim — only the matchable identity. Deterministic, offline, no network.

The map is a curated product -> (CPE vendor, CPE product) table for the software
this probe actually fingerprints; extend it as more products are matched.
"""

from __future__ import annotations

import re

# Normalized product token (letters+digits, lowercased) -> (cpe_vendor, cpe_product).
# Order matters: more specific keys first (checked as substrings of the product).
_CPE_MAP: list[tuple[str, str, str]] = [
    ("mariadb", "mariadb", "mariadb"),
    ("mysql", "oracle", "mysql"),
    ("postgresql", "postgresql", "postgresql"),
    ("openssh", "openbsd", "openssh"),
    ("dropbear", "dropbear_ssh_project", "dropbear_ssh"),
    ("openssl", "openssl", "openssl"),
    # Java app servers: "Apache Tomcat" contains "apache", so it must precede the
    # httpd key or every Tomcat would be reported as http_server.
    ("apachetomcat", "apache", "tomcat"),
    ("tomcat", "apache", "tomcat"),
    ("apache", "apache", "http_server"),      # "Apache", "Apache httpd"
    ("nginx", "nginx", "nginx"),
    ("openresty", "openresty", "openresty"),
    ("lighttpd", "lighttpd", "lighttpd"),
    ("iis", "microsoft", "internet_information_services"),
    ("microsoftexchange", "microsoft", "exchange_server"),
    ("jetty", "eclipse", "jetty"),
    ("wildfly", "redhat", "wildfly"),
    ("glassfish", "oracle", "glassfish_server"),
    ("caddy", "caddyserver", "caddy"),
    ("gunicorn", "gunicorn", "gunicorn"),
    ("uvicorn", "encode", "uvicorn"),
    ("werkzeug", "palletsprojects", "werkzeug"),
    ("tornadoserver", "tornadoweb", "tornado"),
    ("litespeed", "litespeedtech", "litespeed_web_server"),
    ("squid", "squid-cache", "squid"),
    ("cups", "apple", "cups"),
    ("jenkins", "jenkins", "jenkins"),
    ("grafana", "grafana", "grafana"),
    ("prometheus", "prometheus", "prometheus"),
    # Products reachable on the risk-catalog ports (VA_RISK_PORTS).
    ("etcd", "etcd", "etcd"),
    ("influxdb", "influxdata", "influxdb"),
    ("consul", "hashicorp", "consul"),
    ("kibana", "elastic", "kibana"),
    ("cockpit", "redhat", "cockpit"),
    ("webmin", "webmin", "webmin"),
    ("proxmoxve", "proxmox", "virtual_environment"),
    ("apachehadoop", "apache", "hadoop"),
    ("apachehbase", "apache", "hbase"),
    ("apachezookeeper", "apache", "zookeeper"),
    ("portainer", "portainer", "portainer"),
    ("docker", "docker", "docker"),
    ("kubernetes", "kubernetes", "kubernetes"),
    ("rabbitmq", "vmware", "rabbitmq"),
    ("envoy", "envoyproxy", "envoy"),
    ("kong", "konghq", "kong"),
    ("haproxy", "haproxy", "haproxy"),
    ("varnish", "varnish-cache", "varnish"),
    ("php", "php", "php"),
    ("postfix", "postfix", "postfix"),
    ("exim", "exim", "exim"),
    ("sendmail", "sendmail", "sendmail"),
    ("hmailserver", "hmailserver", "hmailserver"),
    ("dovecot", "dovecot", "dovecot"),
    ("courierimap", "courier-mta", "courier-imap"),
    ("cyrusimap", "cyrus", "imap"),
    ("proftpd", "proftpd", "proftpd"),
    ("vsftpd", "vsftpd_project", "vsftpd"),
    ("pureftpd", "pureftpd", "pure-ftpd"),
    ("filezillaserver", "filezilla-project", "filezilla_server"),
    ("wuftpd", "washington_university", "wu-ftpd"),
    ("samba", "samba", "samba"),
    ("bind", "isc", "bind"),
    ("mongodb", "mongodb", "mongodb"),
    # Embedded / IoT web servers (routers, cameras, printers).
    ("rompager", "allegrosoft", "rompager"),
    ("goahead", "embedthis", "goahead"),
    ("minihttpd", "acme", "mini_httpd"),
    ("thttpd", "acme", "thttpd"),
    ("boa", "boa", "boa"),
    # Datastores / caches the banner grabbers reliably name. Conservative: only
    # products whose NVD vendor:product is unambiguous. ("elasticsearch" must
    # precede any shorter "elastic" key if one is ever added — substring match.)
    ("elasticsearch", "elastic", "elasticsearch"),
    ("couchdb", "apache", "couchdb"),
    ("memcached", "memcached", "memcached"),
    ("redis", "redis", "redis"),
]

_VER_RE = re.compile(r"(\d+(?:\.\d+)+(?:p\d+)?[a-z]?)")


def _extract_version(product, version) -> str | None:
    """Prefer an explicit version field; else pull a version-like token out of the
    product string (handles 'OpenSSH_8.2p1', 'nginx/1.18.0')."""
    for src in (version, product):
        m = _VER_RE.search(str(src or ""))
        if m:
            return m.group(1)
    if version:
        v = str(version).strip()
        return v or None
    return None


def to_cpe(service, product, version=None) -> dict | None:
    """Return {vendor, product, version, cpe23} for a recognized product, else None."""
    norm = re.sub(r"[^a-z0-9]", "", str(product or "").lower())
    if not norm:
        return None
    hit = next(((v, p) for key, v, p in _CPE_MAP if key in norm), None)
    if hit is None:
        return None
    vendor, cpe_product = hit
    ver = _extract_version(product, version)
    if not ver:
        return None
    cpe23 = f"cpe:2.3:a:{vendor}:{cpe_product}:{ver}:*:*:*:*:*:*:*"
    return {"vendor": vendor, "product": cpe_product, "version": ver, "cpe23": cpe23}
