"""
gateway.py — the AI egress gateway: what may leave the manager, and in what form.

Every provider call is decided by the deployment profile (``DEPLOYMENT_PROFILE``):

  cloud      raw to any configured provider (optional pseudonymization opt-in)
  hybrid     cloud allowed ONLY for pseudonymized payloads; local models get raw
  sovereign  local models only; any cloud provider is refused (fail closed)

Pseudonymization swaps network identifiers — IPv4/IPv6, hostnames/FQDNs, e-mails,
DOMAIN\\user accounts, MAC addresses — for stable per-request tokens such as
``[IP-1]`` / ``[HOST-2]`` before egress, and swaps them back in the answer. The
mapping lives only in memory for the one request. Tokens are assigned in order of
appearance, so the same input always yields the same prompt and the provider's
prompt cache still hits.

What pseudonymization does NOT hide: finding titles, CVE ids, product names and
versions — the model needs those to reason. That is the documented residual for
hybrid; sovereign exists for customers who cannot accept it.
"""
from __future__ import annotations

import ipaddress
import re
from typing import Literal

Decision = Literal["raw", "pseudonymize"]
PROFILES = ("cloud", "hybrid", "sovereign")


class GatewayDenied(RuntimeError):
    """The deployment profile forbids this egress."""


def egress_decision(profile: str, privacy: str, *, force_pseudonymize: bool) -> Decision:
    profile = (profile or "cloud").strip().lower()
    if profile not in PROFILES:
        # Unknown profile: fail closed to the strictest behaviour that still works.
        profile = "hybrid"
    if privacy == "local":
        return "raw"
    if profile == "sovereign":
        raise GatewayDenied("sovereign deployment: cloud AI providers are disabled; "
                            "configure a local model (LLM_PROVIDER=ollama)")
    if profile == "hybrid" or force_pseudonymize:
        return "pseudonymize"
    return "raw"


# ── pseudonymizer ────────────────────────────────────────────────────────────

_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
_IPV4 = re.compile(rf"(?<![\d.]){_OCTET}(?:\.{_OCTET}){{3}}(?![\d.]|\w)")
_IPV6_CANDIDATE = re.compile(r"(?<![\w:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?![\w:])")
_MAC = re.compile(r"(?<![\w:-])(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}(?![\w:-])")
_EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]{1,64}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63})+")
# DOMAIN\user — one or two backslashes (JSON escapes a literal backslash).
_DOMAIN_USER = re.compile(r"(?<![\w\\])[A-Za-z][\w.-]{0,30}\\{1,2}[A-Za-z0-9_.$-]{1,64}")
_FQDN = re.compile(
    r"(?<![\w.@-])(?=[A-Za-z0-9-]*[A-Za-z])[A-Za-z0-9-]{1,63}"
    r"(?:\.[A-Za-z0-9-]{1,63}){2,}\.?(?![\w-])")
_INTERNAL_2LABEL = re.compile(
    r"(?<![\w.@-])[A-Za-z0-9-]{1,63}\.(?:local|lan|corp|internal|intra|intranet|home|ad)(?![\w.-])",
    re.IGNORECASE)
# Values under these JSON keys are identifiers even without a recognisable shape.
_KEYED = re.compile(
    r'"(hostname|fqdn|host|asset_hostname|computer_name|netbios_name|username|user|'
    r'account|email|owner)"\s*:\s*"([^"\\]{3,255})"')
_KEY_KIND = {"username": "USER", "user": "USER", "account": "USER", "email": "EMAIL", "owner": "USER"}
_TOKEN = re.compile(r"\[?\b(IP|HOST|EMAIL|USER|MAC)-(\d+)\b\]?")


class Pseudonymizer:
    def __init__(self) -> None:
        self._fwd: dict[str, str] = {}      # value → token
        self._rev: dict[str, str] = {}      # "IP-1" → value
        self._counts: dict[str, int] = {}

    @property
    def replaced(self) -> dict[str, int]:
        return dict(self._counts)

    def _token(self, kind: str, value: str) -> str:
        if value in self._fwd:
            return self._fwd[value]
        n = self._counts.get(kind, 0) + 1
        self._counts[kind] = n
        tok = f"[{kind}-{n}]"
        self._fwd[value] = tok
        self._rev[f"{kind}-{n}"] = value
        return tok

    def _classify(self, value: str, default: str) -> str:
        try:
            ipaddress.ip_address(value)
            return "IP"
        except ValueError:
            return "EMAIL" if "@" in value else default

    def pseudonymize(self, text: str) -> str:
        if not text:
            return text
        # 1) register identifiers named by structured keys, in order of appearance
        literals: list[str] = []
        for m in _KEYED.finditer(text):
            value = m.group(2)
            kind = self._classify(value, _KEY_KIND.get(m.group(1), "HOST"))
            self._token(kind, value)
            literals.append(value)
        # 2) shape-based identifiers
        text = _EMAIL.sub(lambda m: self._token("EMAIL", m.group(0)), text)
        text = _MAC.sub(lambda m: self._token("MAC", m.group(0)), text)
        text = _DOMAIN_USER.sub(lambda m: self._token("USER", m.group(0).replace("\\\\", "\\")), text)
        text = _IPV6_CANDIDATE.sub(self._ipv6, text)
        text = _IPV4.sub(lambda m: self._token("IP", m.group(0)), text)
        text = _FQDN.sub(lambda m: self._token("HOST", m.group(0).rstrip(".")), text)
        text = _INTERNAL_2LABEL.sub(lambda m: self._token("HOST", m.group(0)), text)
        # 3) keyed literals wherever else they appear (e.g. a bare hostname in prose)
        for value in sorted(set(literals), key=len, reverse=True):
            if value in text:
                pat = re.compile(rf"(?<![\w.-]){re.escape(value)}(?![\w-])")
                text = pat.sub(self._fwd[value], text)
        return text

    def _ipv6(self, m: re.Match) -> str:
        raw = m.group(0)
        if raw.count(":") < 2:
            return raw
        try:
            ipaddress.IPv6Address(raw)
        except ValueError:
            return raw
        return self._token("IP", raw)

    def rehydrate(self, text: str) -> str:
        if not text or not self._rev:
            return text
        return _TOKEN.sub(lambda m: self._rev.get(f"{m.group(1)}-{m.group(2)}", m.group(0)), text)


def sdk_pseudonymizer(settings) -> Pseudonymizer | None:
    """Gateway decision for the direct Anthropic-SDK callers (report generator,
    advisor agent), which are always cloud egress. Raises GatewayDenied under the
    sovereign profile; returns a run-scoped Pseudonymizer under hybrid (or when
    AI_PSEUDONYMIZE is set), else None for raw."""
    decision = egress_decision(getattr(settings, "deployment_profile", "cloud"), "cloud",
                               force_pseudonymize=bool(getattr(settings, "ai_pseudonymize", False)))
    return Pseudonymizer() if decision == "pseudonymize" else None


def rehydrate_obj(p: Pseudonymizer | None, obj):
    """Rehydrate every string inside a JSON-shaped object (model tool input)."""
    if p is None:
        return obj
    if isinstance(obj, str):
        return p.rehydrate(obj)
    if isinstance(obj, list):
        return [rehydrate_obj(p, v) for v in obj]
    if isinstance(obj, dict):
        return {k: rehydrate_obj(p, v) for k, v in obj.items()}
    return obj
