"""
test_main_scripts_device.py — device-role classification (P0 "Device
classification" use case) in main_scripts/device_classifier.py.

Pure logic: fuse OS family + open ports + service hints -> role, with honest
confidence (single-signal capped) and transparent evidence.
"""
from __future__ import annotations

import pytest

from main_scripts import device_classifier as dc
from main_scripts.device_classifier import classify_device, classify_from_results
from main_scripts.scanner_base import ScanResult


class TestClassifyDevice:
    def test_windows_workstation(self):
        r = classify_device(os_guess="Windows",
                            open_tcp_ports=[135, 139, 445, 3389, 49664])
        assert r["device_type"] == dc.WORKSTATION
        assert "netbios_139" in r["evidence"]
        assert r["confidence"] < 1.0

    def test_domain_controller(self):
        r = classify_device(os_guess="Windows",
                            open_tcp_ports=[53, 88, 135, 389, 445, 636, 3268, 3389])
        assert r["device_type"] == dc.SERVER
        assert r["role_detail"] == "domain_controller"

    def test_printer(self):
        r = classify_device(os_guess="Network/Embedded",
                            open_tcp_ports=[80, 443, 515, 631, 9100])
        assert r["device_type"] == dc.PRINTER
        assert r["role_detail"] == "print_server"

    def test_network_device_router(self):
        r = classify_device(os_guess="Network/Embedded",
                            open_tcp_ports=[22, 23, 53, 80, 443],
                            open_udp_ports=[161])
        assert r["device_type"] == dc.NETWORK_DEVICE

    def test_vmware_hypervisor(self):
        r = classify_device(open_tcp_ports=[443, 902, 903])
        assert r["device_type"] == dc.HYPERVISOR
        assert r["role_detail"] == "vmware_hypervisor"

    def test_iot_camera(self):
        r = classify_device(os_guess="Network/Embedded",
                            open_tcp_ports=[80, 554])
        assert r["device_type"] == dc.IOT

    def test_unknown_when_no_evidence(self):
        r = classify_device()
        assert r["device_type"] == dc.UNKNOWN
        assert r["confidence"] == 0.0

    def test_single_signal_confidence_capped(self):
        # One open port is a hint, not a verdict: <= 0.5, never absolute.
        r = classify_device(open_tcp_ports=[9100])
        assert r["device_type"] == dc.PRINTER
        assert r["confidence"] <= 0.5

    def test_service_product_reinforces_server(self):
        r = classify_device(os_guess="Windows", open_tcp_ports=[80, 443],
                            services=["Microsoft-IIS"])
        assert r["device_type"] == dc.SERVER
        assert any("service_" in e for e in r["evidence"])


class TestClassifyFromResults:
    def test_extracts_signals_from_scan_results(self):
        results = [
            ScanResult("port_scan", "t", port=445, proto="tcp", status="open"),
            ScanResult("port_scan", "t", port=3389, proto="tcp", status="open"),
            ScanResult("port_scan", "t", port=25, proto="tcp", status="closed"),  # ignored
            ScanResult("os_fingerprint", "t", data={"os_guess": "Windows"}),
            ScanResult("snmp_scan", "t", port=161, proto="udp", status="open"),          # confirmed
            ScanResult("udp_scan", "t", port=500, proto="udp", status="open|filtered"),  # silence
            ScanResult("service_banner", "t", port=445, proto="tcp", status="open",
                       data={"service": "smb"}),
        ]
        r = classify_from_results(results)
        assert r["device_type"] in (dc.WORKSTATION, dc.SERVER)
        assert r["signals"]["os_guess"] == "Windows"
        assert r["signals"]["open_tcp"] == [445, 3389]      # closed 25 excluded
        assert r["signals"]["open_udp"] == [161]            # confirmed only; 500 silence dropped
