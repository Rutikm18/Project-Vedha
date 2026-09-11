"""config_model.py — single config precedence chain + effective source map.

Implements the 0b contract: one documented precedence
(CLI > process env > probe.env > Manager-pushed > default), one resolver, and
`render_effective` for `config show --effective`. Pure — no IO. This removes the
config-drift class of bugs (the service unit is rendered FROM the resolved
object, never a third hardcoded copy).
"""
from __future__ import annotations


def _to_bool(v: object) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes", "on")


# field -> (env var name, default, coerce)
_FIELDS: dict[str, tuple[str, object, object]] = {
    "manager_url":        ("PLATFORM_URL", "", str),
    "name":               ("PROBE_NAME", "", str),
    "verify_tls":         ("VERIFY_TLS", True, _to_bool),
    "ca_bundle":          ("PROBE_CA_BUNDLE", None, str),
    "heartbeat_interval": ("HEARTBEAT_INTERVAL", 30, int),
    "poll_interval":      ("POLL_INTERVAL", 10, int),
    "job_limit":          ("JOB_LIMIT", 1, int),
    "max_targets":        ("PROBE_MAX_TARGETS", 4096, int),
    "max_job_seconds":    ("PROBE_MAX_JOB_SECONDS", 7200, int),
    "state_dir":          ("STATE_FILE", "", str),
}


def parse_env_file(text: str) -> dict[str, str]:
    """Parse KEY=VALUE lines; ignore blanks and #comments."""
    out: dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def resolve(cli: dict, env: dict, probe_env: dict, pushed: dict
            ) -> tuple[dict, dict]:
    """Return (values, sources). Precedence: cli > env > probe.env > manager > default.
    `cli`/`pushed` are keyed by FIELD name; `env`/`probe_env` by ENV var name."""
    values: dict[str, object] = {}
    sources: dict[str, str] = {}
    for field, (envname, default, coerce) in _FIELDS.items():
        if cli.get(field) is not None:
            raw, src = cli[field], "cli"
        elif envname in env:
            raw, src = env[envname], "env"
        elif envname in probe_env:
            raw, src = probe_env[envname], "probe.env"
        elif pushed.get(field) is not None:
            raw, src = pushed[field], "manager"
        else:
            raw, src = default, "default"
        if src == "default":
            values[field] = default
        else:
            try:
                values[field] = coerce(raw)  # type: ignore[operator]
            except (ValueError, TypeError):
                values[field], src = default, "default(coerce-failed)"
        sources[field] = src
    return values, sources


def render_effective(values: dict, sources: dict) -> list[tuple[str, object, str]]:
    """Rows of (field, value, winning-source) for `config show --effective`."""
    return [(f, values[f], sources[f]) for f in sorted(_FIELDS)]
