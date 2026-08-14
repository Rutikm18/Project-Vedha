"""Pure-logic tests for the ARP/MAC/mobile-detection helpers in
host_discovery. No network, fully deterministic."""

from scanner.host_discovery import (
    normalize_mac, is_locally_administered, vendor_for_mac, device_hint,
)


class TestNormalizeMac:
    def test_zero_pads_octets(self):
        # macOS `arp -a` strips leading zeros; we must restore them.
        assert normalize_mac("d2:58:2b:ff:cb:4") == "d2:58:2b:ff:cb:04"

    def test_lowercases(self):
        assert normalize_mac("34:F3:9A:A1:A9:8C") == "34:f3:9a:a1:a9:8c"

    def test_extracts_from_arp_line(self):
        line = "? (192.168.1.68) at 34:f3:9a:a1:a9:8c on en0 ifscope [ethernet]"
        assert normalize_mac(line) == "34:f3:9a:a1:a9:8c"

    def test_rejects_broadcast(self):
        assert normalize_mac("ff:ff:ff:ff:ff:ff") is None

    def test_rejects_multicast(self):
        assert normalize_mac("01:00:5e:00:00:fb") is None

    def test_rejects_garbage(self):
        assert normalize_mac("not-a-mac") is None
        assert normalize_mac("") is None


class TestLocallyAdministered:
    def test_randomized_phone_macs(self):
        # 2nd-LSB of first octet set -> randomized (0x2,0x6,0xa,0xe nibble).
        for mac in ("96:f5:cb:90:09:52", "42:76:60:6d:e8:ac",
                    "d2:58:2b:ff:cb:04", "6e:bc:2b:81:3f:e8"):
            assert is_locally_administered(mac), mac

    def test_globally_unique_macs(self):
        for mac in ("34:f3:9a:a1:a9:8c", "5c:8c:30:fd:d5:90", "b8:27:eb:00:00:01"):
            assert not is_locally_administered(mac), mac


class TestVendorLookup:
    def test_known_oui(self):
        assert vendor_for_mac("b8:27:eb:00:00:01") == "Raspberry Pi"

    def test_unknown_oui(self):
        assert vendor_for_mac("de:ad:be:ef:00:01") is None


class TestDeviceHint:
    def test_iphone_lockdownd_port(self):
        assert "apple-mobile" in device_hint("34:f3:9a:a1:a9:8c", None, {62078})

    def test_randomized_mac_is_mobile(self):
        assert "randomized" in device_hint("96:f5:cb:90:09:52", None, set())

    def test_mobile_vendor(self):
        assert device_hint("b8:27:eb:00:00:01", "Samsung", set()) == "mobile (Samsung)"

    def test_plain_vendor_passthrough(self):
        assert device_hint("b8:27:eb:00:00:01", "Raspberry Pi", set()) == "Raspberry Pi"

    def test_no_signal(self):
        assert device_hint(None, None, set()) is None
