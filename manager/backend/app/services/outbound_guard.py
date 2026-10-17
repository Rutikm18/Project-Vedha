"""outbound_guard.py — SSRF guard for URLs and hosts that a tenant supplies.

SIEM/EDR base URLs, Jira/ServiceNow URLs, Slack webhooks and SMTP hosts are typed in
by tenant admins and then called by the Manager from inside its own network. Without
a guard a tenant admin can point them at 127.0.0.1, the cloud metadata service
(169.254.169.254) or internal services, and read the outcome back from errors or
timing.

Policy (settings.outbound_*):
  * always refused: loopback, link-local (incl. metadata), unspecified, multicast,
    reserved, and the AWS IPv6 metadata address;
  * other non-public addresses (RFC 1918, ULA, CGNAT, ...): allowed by default, because
    on-prem Jira, ServiceNow, SIEM, EDR and mail servers normally live on the private
    network. OUTBOUND_ALLOW_PRIVATE_NETWORKS=false is the strict mode: every private
    target is then refused unless its host is in OUTBOUND_HOST_ALLOWLIST, and https is
    required;
  * targets that must be public (``public_only=True``: Slack webhooks, an engagement's
    critical webhook) refuse private addresses in every mode, unless the host is in
    OUTBOUND_HOST_ALLOWLIST;
  * no credentials in the URL;
  * the name is resolved here and EVERY address it resolves to is checked, so
    "internal.attacker.example -> 10.0.0.5" and decimal/octal IP spellings are caught.

Callers also must not follow redirects. Residual risk: the resolution here and the one
made by the HTTP client are separate lookups, so a DNS-rebinding host can still change
answer between them; the always-refused ranges and the egress firewall are the backstop.
"""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit

from app.config import get_settings

SMTP_PORTS = frozenset({25, 465, 587, 2525})

_AWS_IPV6_METADATA = ipaddress.ip_address("fd00:ec2::254")


class OutboundBlocked(ValueError):
    """The destination is not an allowed outbound target."""


def _always_refused(ip: ipaddress._BaseAddress) -> bool:
    return (
        ip.is_loopback or ip.is_link_local or ip.is_unspecified
        or ip.is_multicast or ip.is_reserved or ip == _AWS_IPV6_METADATA
    )


def _allowlist() -> set[str]:
    raw = get_settings().outbound_host_allowlist or ""
    return {h.strip().lower().rstrip(".") for h in raw.split(",") if h.strip()}


def _check_address(ip: ipaddress._BaseAddress, host: str, public_only: bool = False) -> None:
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped                      # ::ffff:127.0.0.1 is 127.0.0.1
    if _always_refused(ip):
        raise OutboundBlocked(f"{host} resolves to a refused address ({ip})")
    if ip.is_global:
        return
    cfg = get_settings()
    if host.lower().rstrip(".") in _allowlist():
        return
    if cfg.outbound_allow_private_networks and not public_only:
        return
    if public_only:
        raise OutboundBlocked(
            f"{host} resolves to a private address ({ip}); this target must be public "
            "(list the host in OUTBOUND_HOST_ALLOWLIST to permit it)"
        )
    raise OutboundBlocked(
        f"{host} resolves to a private address ({ip}); private targets are not allowed "
        "(set OUTBOUND_ALLOW_PRIVATE_NETWORKS=true or list the host in OUTBOUND_HOST_ALLOWLIST)"
    )


def _resolve(host: str, port: int) -> list[ipaddress._BaseAddress]:
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise OutboundBlocked(f"{host} does not resolve") from exc
    # getaddrinfo also accepts decimal/octal/hex IPv4 spellings; we judge what it returns.
    return [ipaddress.ip_address(info[4][0].split("%")[0]) for info in infos]


def check_host(host: str, port: int, *, resolve: bool = True, public_only: bool = False) -> None:
    """Raise OutboundBlocked unless host:port is an allowed destination."""
    host = (host or "").strip()
    if not host:
        raise OutboundBlocked("host is empty")
    try:
        literal = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        literal = None
    if literal is not None:
        _check_address(literal, host, public_only)
        return
    if not resolve:
        return
    for ip in _resolve(host, port):
        _check_address(ip, host, public_only)


def check_url(url: str, *, resolve: bool = True, public_only: bool = False) -> str:
    """Validate a tenant-supplied URL; return it unchanged or raise OutboundBlocked.

    resolve=False checks syntax, scheme and literal IPs only (config-time, where DNS
    may legitimately not answer yet); the send path always uses resolve=True.
    public_only=True is for targets that are never on the private network (a Slack
    webhook, a critical-findings webhook): private addresses are refused in every mode.
    """
    if not url or not isinstance(url, str):
        raise OutboundBlocked("URL is empty")
    try:
        parts = urlsplit(url.strip())
        port = parts.port
    except ValueError as exc:
        raise OutboundBlocked("URL is malformed") from exc
    scheme = (parts.scheme or "").lower()
    allow_private = get_settings().outbound_allow_private_networks
    if scheme not in ("https", "http") or (scheme == "http" and not allow_private):
        raise OutboundBlocked("URL must use https")
    if parts.username or parts.password:
        raise OutboundBlocked("URL must not contain credentials")
    if not parts.hostname:
        raise OutboundBlocked("URL has no host")
    check_host(parts.hostname, port or (443 if scheme == "https" else 80),
               resolve=resolve, public_only=public_only)
    return url


def check_smtp(host: str, port: int, *, resolve: bool = True) -> None:
    if port not in SMTP_PORTS:
        raise OutboundBlocked(f"SMTP port {port} is not allowed (use one of {sorted(SMTP_PORTS)})")
    check_host(host, port, resolve=resolve)


def check_scan_target(host: str) -> None:
    """For an IP the Manager itself will connect to for an active assessment (AD
    domain controller). Such a target is normally private, so this does not apply the
    public-only policy; it requires an IP literal and refuses loopback, link-local
    (metadata) and other special-purpose addresses. The caller still applies the
    engagement scope check."""
    try:
        ip = ipaddress.ip_address((host or "").strip().strip("[]"))
    except ValueError as exc:
        raise OutboundBlocked("target must be an IP address") from exc
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    if _always_refused(ip):
        raise OutboundBlocked(f"{ip} is a refused address (loopback, link-local or reserved)")
