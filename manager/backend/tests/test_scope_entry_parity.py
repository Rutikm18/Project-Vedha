"""
B2 (manager half) — pin the rule the probe mirrors.

probe/tests/test_scope_parity.py asserts that ScopeGuard.from_list(strict=True)
accepts exactly what `ipaddress.ip_network(value, strict=False)` accepts. That
is only a real contract if THIS side keeps using the same predicate, so this
test pins it from the manager's end against the same corpus.

The two processes deploy separately and cannot import each other — the same
reason _USE_CASE_CODES is duplicated with a parity test rather than shared. The
shared artefact here is the RULE, and it is one line: parse as a network, or
reject.
"""
from __future__ import annotations

import ipaddress

import pytest

from app.schemas.engagement import validate_scope_entries

# Byte-identical to CORPUS in probe/tests/test_scope_parity.py.
CORPUS = [
    "10.0.0.0/24",
    "192.168.1.50",
    "192.168.1.50/32",
    "2001:db8::/32",
    "fe80::1",
    "0.0.0.0/0",
    "10.0.0.0/244",
    "10.0.0.",
    "scanme.example.com",
    "not an address",
    "10.0.0.1-10.0.0.9",
]


def _parses_as_network(entry: str) -> bool:
    try:
        ipaddress.ip_network(entry.strip(), strict=False)
        return True
    except ValueError:
        return False


@pytest.mark.parametrize("entry", CORPUS)
def test_the_manager_rule_is_exactly_ip_network(entry):
    """If this ever loosens, the probe's strict mode silently diverges again."""
    if _parses_as_network(entry):
        assert validate_scope_entries([entry]) == [entry]
    else:
        with pytest.raises(ValueError):
            validate_scope_entries([entry])


def test_a_hostname_cannot_enter_an_engagement_scope():
    """The divergence that destroyed whole results starts here, and is closed."""
    with pytest.raises(ValueError, match="invalid IP address or CIDR"):
        validate_scope_entries(["printer.corp.local"])


def test_a_malformed_exclusion_is_refused_not_silently_dropped():
    """Same validator guards excluded_cidrs — see EngagementCreate."""
    with pytest.raises(ValueError):
        validate_scope_entries(["10.0.0.5/33"])


def test_blank_entries_are_refused():
    with pytest.raises(ValueError, match="cannot be blank"):
        validate_scope_entries(["10.0.0.0/24", "  "])
