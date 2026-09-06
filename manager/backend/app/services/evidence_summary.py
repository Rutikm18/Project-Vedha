"""evidence_summary.py — flatten the arbitrary evidence JSONB into plain facts.

Findings carry a free-form ``evidence`` dict whose shape depends on the scanner /
posture rule that produced it. Rendered raw it is a wall of keys and stringified
JSON — the opposite of "understandable at a glance". This module turns it into a
short, ordered ``[{label, value}]`` fact list:

  * friendly, human labels for the keys that actually matter (Port, Service,
    Version, exposure, KEV/EPSS …), in a fixed priority order;
  * plain values (booleans → Yes/No, lists → comma-joined, no JSON braces);
  * internal/duplicated keys (title, remediation, mitre — shown elsewhere) dropped;
  * a hard cap so the panel never becomes a data dump.

Pure and defensive: any input that is not a dict returns ``[]`` (an already-shaped
``[{label, value}]`` list passes straight through), and nested/complex values are
summarised rather than dumped.
"""
from __future__ import annotations

from typing import Any

_MAX_FACTS = 24
_MAX_VALUE_LEN = 220
_MAX_LIST_ITEMS = 8

# (evidence key, display label) in the order we want them to appear. First match
# wins, so aliases for the same concept collapse to one label.
_PRIORITY: list[tuple[str, str]] = [
    ("ip", "Host"),
    ("host", "Host"),
    ("hostname", "Host"),
    ("target", "Host"),
    ("port", "Port"),
    ("service", "Service"),
    ("product", "Product"),
    ("version", "Version"),
    ("protocol", "Protocol"),
    ("cpe", "CPE"),
    ("banner", "Banner"),
    ("observed", "Observed"),
    ("observation", "Observed"),
    ("actual", "Observed"),
    ("expected", "Expected"),
    ("weak_algorithms", "Weak algorithms"),
    ("weak_ciphers", "Weak ciphers"),
    ("ciphers", "Ciphers"),
    ("server", "Server"),
    ("exposure", "Exposure"),
    ("internet_facing", "Internet-facing"),
    ("auth_enforced", "Authentication required"),
    ("scanner", "Detected by"),
    ("source", "Detected by"),
    ("rule_id", "Detection rule"),
    ("confidence", "Confidence"),
]

# Shown elsewhere in the UI or purely internal — never render as an evidence fact.
_SKIP: frozenset[str] = frozenset({
    "title", "description", "remediation", "mitre", "mitre_techniques",
    "correlation", "regression", "attack_narrative", "references", "severity",
    "state", "enrichment", "scan_status", "scan_error", "poc", "poc_available",
    "kev", "epss", "epss_score",
})


def _sentence_case(key: str) -> str:
    text = str(key).replace("_", " ").replace("-", " ").strip()
    return (text[:1].upper() + text[1:]) if text else key


def _format_value(value: Any) -> str | None:
    """Render one evidence value as a short plain string, or None to skip it."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (list, tuple)):
        parts = [str(x) for x in value if x is not None and x != ""]
        if not parts:
            return None
        shown = ", ".join(parts[:_MAX_LIST_ITEMS])
        if len(parts) > _MAX_LIST_ITEMS:
            shown += f" (+{len(parts) - _MAX_LIST_ITEMS} more)"
        return shown[:_MAX_VALUE_LEN]
    if isinstance(value, float):
        return (f"{value:.4f}").rstrip("0").rstrip(".")
    if isinstance(value, dict):
        # Do not dump nested JSON; summarise as a key list so it stays glanceable.
        keys = [str(k) for k in value.keys()]
        if not keys:
            return None
        return _sentence_case(", ".join(keys[:_MAX_LIST_ITEMS]))
    return str(value)[:_MAX_VALUE_LEN]


def _percentile(value: Any) -> str | None:
    try:
        pct = float(value)
    except (TypeError, ValueError):
        return None
    if pct <= 1:  # stored as a 0–1 fraction
        pct *= 100
    return f"{round(pct)}th percentile"


def _enrichment_facts(enrichment: dict[str, Any]) -> list[dict[str, str]]:
    facts: list[dict[str, str]] = []
    if enrichment.get("kev"):
        facts.append({"label": "CISA KEV", "value": "Listed — exploited in the wild"})
    pct = _percentile(enrichment.get("epss_percentile"))
    if pct:
        facts.append({"label": "EPSS percentile", "value": pct})
    if enrichment.get("nvd_published"):
        facts.append({"label": "NVD published", "value": str(enrichment["nvd_published"])[:_MAX_VALUE_LEN]})
    return facts


def summarize_evidence(evidence: Any) -> list[dict[str, str]]:
    """Return a short, ordered, human-readable ``[{label, value}]`` fact list.

    Non-dict input → ``[]``. An already-shaped ``[{label, value}]`` list is returned
    unchanged so callers can pre-build facts when they have richer context.
    """
    if isinstance(evidence, list):
        if all(isinstance(e, dict) and "label" in e and "value" in e for e in evidence):
            return evidence
        return []
    if not isinstance(evidence, dict):
        return []

    facts: list[dict[str, str]] = []
    seen_labels: set[str] = set()

    # 1) Priority keys, in order, de-duplicated by label (aliases collapse).
    for key, label in _PRIORITY:
        if key not in evidence or label in seen_labels:
            continue
        rendered = _format_value(evidence[key])
        if rendered is None:
            continue
        facts.append({"label": label, "value": rendered})
        seen_labels.add(label)

    # 2) Enrichment block → a couple of high-signal exploitation facts.
    enrichment = evidence.get("enrichment")
    if isinstance(enrichment, dict):
        for fact in _enrichment_facts(enrichment):
            if fact["label"] not in seen_labels:
                facts.append(fact)
                seen_labels.add(fact["label"])

    # 3) Any remaining simple scalar keys, sentence-cased, until the cap.
    priority_keys = {k for k, _ in _PRIORITY}
    for key, value in evidence.items():
        if len(facts) >= _MAX_FACTS:
            break
        if key in _SKIP or key in priority_keys:
            continue
        label = _sentence_case(key)
        if label in seen_labels:
            continue
        rendered = _format_value(value)
        if rendered is None:
            continue
        facts.append({"label": label, "value": rendered})
        seen_labels.add(label)

    return facts[:_MAX_FACTS]
