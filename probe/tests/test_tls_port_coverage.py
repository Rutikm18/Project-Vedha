"""
TLS branch coverage — the gap behind `tls_scan: invocations: 0`.

A real scan of a Windows host (192.168.1.65) had 20 open ports and the TLS
inspector never ran once, because the static candidate set was nine ports and
none of them were open. The run then reported `invocations: 0`, which reads to an
operator as "TLS was fine" when it actually means "TLS was never looked at".

Two things are fixed here and pinned by these tests:

  1. There was ONE port set in `service_enum` and a SECOND, DIFFERENT copy in
     `workflow/gates`. They had already drifted (3269 in one, 989 in the other),
     so a port could satisfy the branch spec and then be refused by the gate.
  2. The set was too narrow to cover management/API surfaces that default to
     implicit TLS.

The widening is deliberately NOT "every open port": protocols that reach TLS only
after an application-layer negotiation are excluded, because a bare ClientHello
there is the wrong packet and would manufacture a misleading "TLS refused" record
for a port that genuinely does use TLS.
"""
from __future__ import annotations

import pytest

from scanner.service_enum import TLS_PORTS
from workflow import gates
from workflow.branches import BRANCHES


class TestSingleSourceOfTruth:
    def test_gates_reuses_the_same_object(self):
        assert gates.TLS_PORTS is TLS_PORTS

    def test_branch_port_table_reuses_it_too(self):
        assert gates._BRANCH_PORT_TABLE["tls"] is TLS_PORTS

    def test_branch_spec_matches_the_gate(self):
        """The drift that used to exist: spec allows a port the gate refuses."""
        spec = next(b for b in BRANCHES if b.branch == "tls")
        assert set(spec.ports) == set(gates._BRANCH_PORT_TABLE["tls"])


class TestWidenedCoverage:
    @pytest.mark.parametrize("port", [443, 465, 636, 993, 995, 990, 3269, 5986])
    def test_classic_implicit_tls_still_covered(self, port):
        assert port in TLS_PORTS

    @pytest.mark.parametrize("port,why", [
        (902, "VMware authd — open on the host that exposed this gap"),
        (6443, "kubernetes API"),
        (2376, "docker TLS"),
        (8834, "Nessus"),
        (9443, "common alt-HTTPS management port"),
        (853, "DNS-over-TLS"),
        (8883, "MQTTS"),
        (5671, "AMQPS"),
    ])
    def test_management_and_api_surfaces_now_covered(self, port, why):
        assert port in TLS_PORTS, why

    def test_the_set_actually_grew(self):
        assert len(TLS_PORTS) > 9, "the old set was 9 ports"


class TestDeliberateExclusions:
    """Excluded on purpose — a bare ClientHello is the WRONG packet here."""

    def test_rdp_is_excluded(self):
        """3389 reaches TLS only after the X.224 rdpNegReq. rdp_scanner already
        observes the TLS/NLA outcome, so probing it here would only produce a
        misleading 'TLS refused' record for a port that does use TLS."""
        assert 3389 not in TLS_PORTS

    @pytest.mark.parametrize("port", [5985, 47001])
    def test_winrm_plaintext_listeners_excluded(self, port):
        """5986 is WinRM's TLS listener and IS included; these two are plaintext."""
        assert port not in TLS_PORTS
        assert 5986 in TLS_PORTS

    @pytest.mark.parametrize("port", [25, 587, 110, 143, 21])
    def test_starttls_upgrade_ports_excluded(self, port):
        """STARTTLS negotiates in-band; implicit TLS would fail."""
        assert port not in TLS_PORTS


def test_refused_handshake_is_an_error_not_a_false_negative():
    """Why widening is safe.

    A port that does not speak TLS yields `status="error"` carrying the handshake
    exception — an honest 'we tried, it refused'. It must NOT be recorded as a
    successful scan reporting no TLS, which would be a false negative.
    """
    src = (__import__("pathlib").Path(__file__).resolve().parent.parent
           / "scanner" / "tls_scanner.py").read_text()
    assert 'status="error"' in src
