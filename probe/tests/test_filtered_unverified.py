"""A `filtered` verdict nobody re-checked is counted apart, not shown as a firewall.

The cleanup pass gives silent ports a second, gentler look, but it is capped
(reprobe_max_candidates) and bounded by the host clock. On the Windows agent,
before the SYN-retry fix, 1110 of 1110 re-checked ports turned out CLOSED; on a
65,535-port sweep the cap would have left ~62,000 more ports reported
`filtered` with nothing saying they were never confirmed.

Now every host summary carries `filtered_unverified`, and when the host's own
re-checks say "silence here means closed" the scan warns. A genuinely firewalled
host (silent on the second look too) is NOT flagged.
"""
from __future__ import annotations

import asyncio
import logging

import pytest

from scanner.port_scanner import PortScanner
from scanner.scanner_base import ScopeGuard

SCOPE = ScopeGuard.from_list(["10.0.0.0/24"])
TARGET = "10.0.0.1"
PORTS = list(range(1, 500))


def _scanner(**kw):
    return PortScanner(SCOPE, ports=PORTS, rate=10_000, concurrency=50, timeout=0.01,
                       adaptive_timeout=False, congestion=False, reprobe_rate=100_000.0,
                       reprobe_retries=0, **kw)


def _host(scanner, second_look: str):
    """Silent in the main sweep; `second_look` is what the cleanup pass sees."""
    async def _attempt(target, port, est=None, min_timeout=None):
        if min_timeout is None:
            return scanner._build(target, port, "filtered", "no_response", "silence")
        if second_look == "closed":
            return scanner._build(target, port, "closed", "connection_refused", "RST")
        return scanner._build(target, port, "filtered", "no_response", "silence")
    return _attempt


async def _summary(scanner):
    results = await scanner.scan_target(TARGET)
    return next(r for r in results if r.status == "scan_summary").data


@pytest.mark.asyncio
async def test_windows_like_host_flags_the_unchecked_ports(monkeypatch, caplog):
    scanner = _scanner(reprobe_max_candidates=50)
    monkeypatch.setattr(scanner, "_attempt", _host(scanner, "closed"))
    with caplog.at_level(logging.WARNING, logger="scanner"):
        summary = await _summary(scanner)
    assert summary["reprobe"]["resolved"] == 50
    assert summary["filtered_unverified"] == 449
    assert summary["reprobe"]["unverified"] == 449
    assert any("treat them as unverified" in r.getMessage() for r in caplog.records)


@pytest.mark.asyncio
async def test_firewalled_host_is_not_flagged(monkeypatch, caplog):
    scanner = _scanner(reprobe_max_candidates=50)
    monkeypatch.setattr(scanner, "_attempt", _host(scanner, "silent"))
    with caplog.at_level(logging.WARNING, logger="scanner"):
        summary = await _summary(scanner)
    assert summary["filtered_unverified"] == 449      # still counted honestly
    assert not any("treat them as unverified" in r.getMessage() for r in caplog.records)


@pytest.mark.asyncio
async def test_nothing_unchecked_means_zero(monkeypatch):
    scanner = _scanner(reprobe_max_candidates=0)      # 0 = no cap
    monkeypatch.setattr(scanner, "_attempt", _host(scanner, "closed"))
    summary = await _summary(scanner)
    assert summary["filtered_unverified"] == 0
    assert summary["reprobe"]["resolved"] == len(PORTS)


@pytest.mark.asyncio
async def test_key_is_present_even_without_a_cleanup_pass(monkeypatch):
    scanner = _scanner(reprobe_max_candidates=50, reprobe=False)
    monkeypatch.setattr(scanner, "_attempt", _host(scanner, "closed"))
    summary = await _summary(scanner)
    assert summary["filtered_unverified"] == 0
