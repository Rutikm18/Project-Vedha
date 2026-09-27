"""Remediation platform auto-detection.

The fix plan must pick the target platform from what Vedha already knows about
the asset — its OS string, an operator's os_family tag, or a service banner —
and say where that came from. Unknown stays `generic` (never a silent Linux
default), and BSD / network OSes stay `generic` because the KB's Linux commands
(apt, systemctl) would be wrong there.
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.remediation_os import (
    PlatformResolution,
    platform_for_request,
    resolve_finding_platform,
    resolve_platform,
)


def _asset(os=None, tags=None):
    return SimpleNamespace(id=uuid.uuid4(), ip_address="10.0.0.5", hostname="h1",
                           fqdn=None, os=os, asset_type="server", device_role=None,
                           role_detail=None, role_confidence=None, tags=tags)


def _svc(port, banner=None, product=None, name=None):
    return SimpleNamespace(port=port, protocol="tcp", service_name=name,
                           product=product, banner=banner, exposure=None)


@pytest.mark.parametrize("os_string,expected", [
    ("Windows Server 2019", "windows"),
    ("Microsoft Windows 10 Pro", "windows"),
    ("Ubuntu 22.04 LTS", "linux"),
    ("Linux 5.15", "linux"),
    ("Red Hat Enterprise Linux 8", "linux"),
    ("Mac OS X 13.4", "macos"),
    ("Darwin 23.1", "macos"),
])
def test_asset_os_string_resolves_platform(os_string, expected):
    r = resolve_platform(_asset(os=os_string), [])
    assert r.os == expected
    assert r.source == "asset_os"
    assert r.confidence == pytest.approx(0.85)
    assert os_string in (r.evidence or "")


def test_banner_resolves_windows_when_os_unknown():
    r = resolve_platform(_asset(os=None), [_svc(443, banner="Microsoft-IIS/10.0")])
    assert (r.os, r.family, r.source) == ("windows", "windows", "service_banner")
    assert r.confidence == pytest.approx(0.6)
    assert "443" in (r.evidence or "")


def test_banner_resolves_linux_distro():
    r = resolve_platform(_asset(os=None), [_svc(22, banner="SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5")])
    assert (r.os, r.source) == ("linux", "service_banner")


def test_os_string_beats_banner():
    r = resolve_platform(_asset(os="Windows Server 2016"),
                         [_svc(22, banner="OpenSSH_8.2p1 Ubuntu")])
    assert r.os == "windows"
    assert r.source == "asset_os"


@pytest.mark.parametrize("os_string,family", [
    ("FreeBSD 13.2", "bsd"),
    ("pfSense 2.7", "bsd"),
    ("Cisco IOS XE 17.3", "network_os"),
    ("FortiOS 7.2", "network_os"),
])
def test_bsd_and_network_os_stay_generic(os_string, family):
    r = resolve_platform(_asset(os=os_string), [])
    assert r.os == "generic"
    assert r.family == family
    assert r.source == "asset_os"


def test_manual_operator_tag_wins():
    tags = {"v": 1, "auto": [], "manual": [{"key": "os_family", "value": "linux"}]}
    r = resolve_platform(_asset(os="Windows 10", tags=tags), [])
    assert (r.os, r.source, r.confidence) == ("linux", "manual_tag", 1.0)


def test_nothing_known_is_generic_not_detected():
    r = resolve_platform(_asset(os=None), [_svc(80, banner="nginx")])
    assert (r.os, r.family, r.source) == ("generic", None, "not_detected")


def test_no_asset():
    r = resolve_platform(None, [])
    assert (r.os, r.source) == ("generic", "no_asset")


def test_to_dict_shape():
    d = resolve_platform(_asset(os="Ubuntu"), []).to_dict()
    assert set(d) == {"os", "family", "source", "evidence", "confidence"}


def test_resolve_finding_platform_without_asset_makes_no_queries():
    db = MagicMock()
    db.execute = AsyncMock()
    finding = SimpleNamespace(asset_id=None, engagement_id=uuid.uuid4())
    r = asyncio.run(resolve_finding_platform(db, finding))
    assert r.source == "no_asset"
    db.execute.assert_not_called()


def test_resolve_finding_platform_loads_asset_and_services():
    asset = _asset(os=None)
    services = [_svc(3389, product="Microsoft Terminal Services", banner="Microsoft Windows RDP")]
    asset_res = MagicMock()
    asset_res.scalar_one_or_none = MagicMock(return_value=asset)
    svc_res = MagicMock()
    svc_res.scalars.return_value.all.return_value = services
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[asset_res, svc_res])
    finding = SimpleNamespace(asset_id=asset.id, engagement_id=uuid.uuid4())
    r = asyncio.run(resolve_finding_platform(db, finding))
    assert (r.os, r.source) == ("windows", "service_banner")
    assert db.execute.await_count == 2


def test_platform_for_request_explicit_os_skips_detection():
    db = MagicMock()
    db.execute = AsyncMock()
    finding = SimpleNamespace(asset_id=uuid.uuid4(), engagement_id=uuid.uuid4())
    r = asyncio.run(platform_for_request(db, finding, "Windows"))
    assert (r.os, r.source) == ("windows", "requested")
    db.execute.assert_not_called()


@pytest.mark.parametrize("requested", ["auto", "AUTO", " auto ", None, ""])
def test_platform_for_request_auto_detects(requested):
    db = MagicMock()
    db.execute = AsyncMock()
    finding = SimpleNamespace(asset_id=None, engagement_id=uuid.uuid4())
    r = asyncio.run(platform_for_request(db, finding, requested))
    assert r.source == "no_asset"
    assert isinstance(r, PlatformResolution)
