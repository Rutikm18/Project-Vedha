"""
outbound.py — SSRF guard for URLs an operator can make the manager call.

Integration endpoints (Slack webhook, Jira / ServiceNow base URL) and the
engagement's `critical_webhook_url` are tenant-supplied. Without a check, an
admin could point them at the cloud metadata service (169.254.169.254), the
loopback API, or an internal Postgres/Redis HTTP-ish port, and read the response
via the delivery error log. `validate_outbound_url` refuses those.

Self-hosted Jira / ServiceNow normally live on private addresses, so
`allow_private=True` permits RFC 1918 / ULA for those; loopback, link-local
(incl. metadata), unspecified, multicast and reserved ranges are refused always.
Hostnames are resolved and EVERY address is checked, so a name that resolves to
an internal IP is rejected too. The check must also run at send time (DNS may
change after save).
"""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit


def _getaddrinfo(host, port):
    """DNS lookup, isolated so tests can stub it without touching real sockets."""
    return socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)


class UnsafeOutboundURL(ValueError):
    """The URL is malformed or points somewhere the manager must not call."""


def _blocked(ip: ipaddress._BaseAddress, allow_private: bool) -> str | None:
    if ip.is_loopback:
        return "loopback"
    if ip.is_link_local:
        return "link-local / cloud metadata"
    if ip.is_unspecified or ip.is_multicast or ip.is_reserved:
        return "reserved"
    if ip.is_private and not allow_private:
        return "private network"
    return None


def validate_outbound_url(url: str, *, allow_private: bool = False,
                          resolve: bool = True) -> str:
    """Return the URL unchanged if safe, else raise UnsafeOutboundURL."""
    try:
        parts = urlsplit((url or "").strip())
        host = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise UnsafeOutboundURL("not a valid URL") from exc
    if parts.scheme not in ("http", "https"):
        raise UnsafeOutboundURL("only http(s) URLs are allowed")
    if not host:
        raise UnsafeOutboundURL("URL has no host")
    if parts.username or parts.password:
        raise UnsafeOutboundURL("credentials in the URL are not allowed")

    try:
        literals = [ipaddress.ip_address(host)]
    except ValueError:
        literals = []
        if resolve:
            try:
                infos = _getaddrinfo(host, port or (443 if parts.scheme == "https" else 80))
            except socket.gaierror as exc:
                raise UnsafeOutboundURL(f"host '{host}' does not resolve") from exc
            literals = [ipaddress.ip_address(i[4][0].split("%")[0]) for i in infos]

    for ip in literals:
        # An IPv4-mapped IPv6 address (::ffff:169.254.169.254) is the v4 address.
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
            ip = ip.ipv4_mapped
        reason = _blocked(ip, allow_private)
        if reason:
            raise UnsafeOutboundURL(f"{ip} is a {reason} address")
    return url
