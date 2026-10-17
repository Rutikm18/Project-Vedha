"""Asset OS from the scan (testing-round gap 7): fill empty fields, upgrade only the
probe's TTL-family guess, never overwrite what an operator or discovery recorded."""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from app.detection import engine_bridge as EB

UBUNTU = {"os": "Ubuntu", "os_version": "16.04", "source": "ssh_banner"}


async def _run(asset, info):
    async def fake_resolve(db, eid, ip, *, cache=None, identity=None):
        return asset
    with patch.object(EB, "_resolve_asset", side_effect=fake_resolve):
        return await EB._promote_host_os(None, "e", {"10.0.0.30": info}, cache={}, identity=None)


@pytest.mark.asyncio
async def test_empty_fields_are_filled():
    a = SimpleNamespace(os=None, os_version=None)
    assert await _run(a, UBUNTU) == 1
    assert (a.os, a.os_version) == ("Ubuntu", "16.04")


@pytest.mark.asyncio
async def test_operator_value_is_never_overwritten():
    a = SimpleNamespace(os="RHEL", os_version="8.9")
    assert await _run(a, UBUNTU) == 0
    assert (a.os, a.os_version) == ("RHEL", "8.9")


@pytest.mark.asyncio
async def test_ttl_family_guess_is_upgraded_by_a_banner_identification():
    a = SimpleNamespace(os="Linux/Unix/macOS", os_version=None)
    await _run(a, UBUNTU)
    assert (a.os, a.os_version) == ("Ubuntu", "16.04")


@pytest.mark.asyncio
async def test_ttl_guess_does_not_replace_a_ttl_guess_from_the_same_source():
    a = SimpleNamespace(os="Linux/Unix/macOS", os_version=None)
    await _run(a, {"os": "Network/Embedded", "os_version": None, "source": "os_fingerprint"})
    assert a.os == "Linux/Unix/macOS"


@pytest.mark.asyncio
async def test_version_is_only_added_to_a_matching_os():
    a = SimpleNamespace(os="Windows", os_version=None)
    await _run(a, {"os": "Windows", "os_version": "Windows Server 2019", "source": "smb_scan"})
    assert a.os_version == "Windows Server 2019"
