"""Tests for agent/hw_bind.py"""
from __future__ import annotations

import os

import pytest

from agent.hw_bind import get_hw_id, check_hw_bind, HWBindError


class TestGetHwId:
    def test_returns_32_hex_chars(self):
        hw_id = get_hw_id()
        assert len(hw_id) == 32
        assert all(c in "0123456789abcdef" for c in hw_id)

    def test_deterministic_within_session(self):
        assert get_hw_id() == get_hw_id()


class TestCheckHwBind:
    def test_passes_when_match(self, monkeypatch):
        expected = get_hw_id()
        monkeypatch.setenv("HW_BIND_FINGERPRINT", expected)
        monkeypatch.setenv("LICENSE_ENFORCED", "true")
        check_hw_bind()  # should not raise

    def test_raises_on_mismatch(self, monkeypatch):
        monkeypatch.setenv("HW_BIND_FINGERPRINT", "00000000000000000000000000000000")
        monkeypatch.setenv("LICENSE_ENFORCED", "true")
        with pytest.raises(HWBindError, match="bound to a different machine"):
            check_hw_bind()

    def test_skips_when_unset_and_dev_mode(self, monkeypatch):
        monkeypatch.delenv("HW_BIND_FINGERPRINT", raising=False)
        monkeypatch.setenv("LICENSE_ENFORCED", "false")
        check_hw_bind()  # should not raise

    def test_raises_when_unset_and_enforced(self, monkeypatch):
        monkeypatch.delenv("HW_BIND_FINGERPRINT", raising=False)
        monkeypatch.setenv("LICENSE_ENFORCED", "true")
        with pytest.raises(HWBindError, match="not properly hardware-bound"):
            check_hw_bind()
