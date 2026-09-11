"""obs.py — observability (Phase 8): redacted structured logs, low-cardinality
heartbeat metrics, and a redacted diagnostics bundle.

Redaction is the point: logs and the diagnostics bundle are the most likely
accidental-disclosure vectors, and metric labels must stay bounded (no per-host /
per-target labels, or they melt a time-series DB). Pure — the CLI wires the IO.
"""
from __future__ import annotations

import json
import re

# whole-word sensitive tokens (word-split avoids false hits like 'path' for 'pat')
_WORD_SENSITIVE = {"pat", "token", "password", "secret", "authorization",
                   "credential", "apikey", "key", "pwd"}


def _is_sensitive(key: str) -> bool:
    words = set(re.split(r"[^a-z0-9]+", key.lower()))
    return bool(words & _WORD_SENSITIVE) or any(
        s in key.lower() for s in ("password", "secret", "authorization", "api_key"))


def redact(fields: dict) -> dict:
    return {k: ("[REDACTED]" if _is_sensitive(k) else v) for k, v in fields.items()}


def log_line(level: str, event: str, fields: dict | None = None, *,
             ts: float = 0.0, corr_id: str | None = None) -> str:
    rec: dict = {"ts": ts, "level": level, "event": event}
    if corr_id:
        rec["corr_id"] = corr_id
    rec.update(redact(fields or {}))
    return json.dumps(rec, sort_keys=True, separators=(",", ":"))


def mask_ip(ip: str) -> str:
    """Mask the host octet so an own-IP never lands verbatim in a shared bundle."""
    parts = ip.split(".")
    if len(parts) == 4 and all(p.isdigit() for p in parts):
        return f"{parts[0]}.{parts[1]}.{parts[2]}.x"
    return ip


def _mask_addr(addr: str) -> str:
    ip, _, prefix = addr.partition("/")
    masked = mask_ip(ip)
    return f"{masked}/{prefix}" if prefix else masked


def heartbeat_metrics(*, version: str, os_name: str, artifact_hash: str,
                      since_last_contact_s: float, queue_depth: int,
                      oldest_unsent_age_s: float, job_outcomes: dict,
                      restart_count: int, last_exit_class: str,
                      rss_bytes: int, cpu_pct: float, privileged: bool) -> dict:
    """Bounded-cardinality fleet-health signal. No IPs/hostnames/targets as keys."""
    return {
        "agent_version": version,
        "os": os_name,
        "artifact_hash": artifact_hash,
        "since_last_contact_s": since_last_contact_s,
        "queue_depth": queue_depth,
        "oldest_unsent_age_s": oldest_unsent_age_s,
        "job_outcomes": dict(job_outcomes),
        "restart_count": restart_count,
        "last_exit_class": last_exit_class,
        "rss_bytes": rss_bytes,
        "cpu_pct": cpu_pct,
        "privileged": privileged,
    }


def build_diagnostics(*, config_values: dict, doctor_checks, interfaces: list[dict],
                      recent_logs: list[str], clock_offset_s: float) -> dict:
    """A support bundle with secrets stripped and own-IPs masked."""
    return {
        "config": redact(config_values),
        "doctor": [{"name": c.name, "status": c.status, "detail": c.detail} for c in doctor_checks],
        "interfaces": [
            {"name": i.get("name"), "kind": i.get("kind"),
             "addresses": [_mask_addr(a) for a in i.get("addresses", [])]}
            for i in interfaces
        ],
        "clock_offset_s": clock_offset_s,
        "recent_logs": recent_logs,
    }
