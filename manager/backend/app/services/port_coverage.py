"""port_coverage.py — answer "what was port N on this host?" from stored facts.

The probe records EVERY requested port's state on the per-host `scan_summary`
fact, run-length encoded (probe/main_scripts/port_scanner.ScanMetrics):

    {"port_states": {"open":   [[22, 22], [443, 443]],
                     "closed": [[1, 21], [23, 442]],
                     "filtered": [[500, 510]],
                     "not_scanned": [[1000, 65535]]}}

That already arrives and is already persisted inside scan_results.facts — it
was simply not queryable. This module is the read side: no schema change, no
new storage, no second copy of the evidence.

FOUR ANSWERS, NOT TWO
---------------------
`open` / `closed` / `filtered` / `not_scanned` are four different facts, and
the last two are the pair that gets conflated:

  * filtered    — probed, stayed silent. Evidence about the TARGET.
  * not_scanned — never probed (host budget, cleanup cap, truncated sweep).
                  Evidence about the SCAN.

Reporting the second as the first would claim a firewall that may not exist.
And a port in NO range is `unknown` — the scan never spoke about it, which is
not the same as closed.

Pure functions only: the decoding is the part worth testing, and it needs no
database to be correct.
"""
from __future__ import annotations

#: A port the scan never expressed an opinion about.
UNKNOWN = "unknown"

#: States that mean "we actually probed this port".
_PROBED = ("open", "closed", "filtered", "unreachable", "error")

#: Always present in a summary, so a caller can branch without a key check
#: — the same contract port_scanner's own scan_summary keeps.
_REPORTED = (*_PROBED, "not_scanned")


def _spans(ranges: dict | None):
    """Yield (state, low, high) for every well-formed span.

    Facts come off the wire, so a malformed span is skipped rather than
    allowed to raise: one bad entry must not make a whole host unqueryable.
    """
    if not isinstance(ranges, dict):
        return
    for state, spans in ranges.items():
        if not isinstance(spans, (list, tuple)):
            continue
        for span in spans:
            if not isinstance(span, (list, tuple)) or len(span) != 2:
                continue
            low, high = span
            if not isinstance(low, int) or not isinstance(high, int):
                continue
            if isinstance(low, bool) or isinstance(high, bool) or high < low:
                continue
            yield state, low, high


def port_state_at(ranges: dict | None, port: int) -> str:
    """The recorded state of one port, or UNKNOWN if nothing covers it."""
    for state, low, high in _spans(ranges):
        if low <= port <= high:
            return state
    return UNKNOWN


def decode_port_states(ranges: dict | None) -> dict[int, str]:
    """Expand the ranges back to {port: state}.

    The inverse of the probe's encoder — useful for export and for tests that
    assert the round trip loses nothing. Callers answering a single question
    should use port_state_at() instead of materialising 65,535 entries.
    """
    expanded: dict[int, str] = {}
    for state, low, high in _spans(ranges):
        for port in range(low, high + 1):
            expanded[port] = state
    return expanded


def summarize_coverage(ranges: dict | None) -> dict:
    """Per-state counts plus how much of the requested range was really probed.

    `probed_fraction` is the number that says how much to trust the rest: a
    host whose sweep was cut short reports states for the ports it reached and
    `not_scanned` for the remainder, and a reader needs to know which.
    """
    counts: dict[str, int] = {state: 0 for state in _REPORTED}
    for state, low, high in _spans(ranges):
        counts[state] = counts.get(state, 0) + (high - low + 1)

    probed = sum(counts.get(state, 0) for state in _PROBED)
    total = sum(counts.values())
    summary = dict(counts)
    summary["probed"] = probed
    summary["total"] = total
    summary["probed_fraction"] = (probed / total) if total else 0.0
    return summary


def ranges_from_facts(facts, host: str) -> dict:
    """The port-state ranges one host's scan_summary carries.

    A host can have more than one summary in a job: the two-phase sweep emits
    one after the fast pass and another after the port tail. The LAST wins —
    it is the one that describes the widest coverage.
    """
    found: dict = {}
    for fact in facts or []:
        if not isinstance(fact, dict):
            continue
        if fact.get("status") != "scan_summary" or fact.get("target") != host:
            continue
        states = (fact.get("data") or {}).get("port_states")
        if isinstance(states, dict):
            found = states
    return found
