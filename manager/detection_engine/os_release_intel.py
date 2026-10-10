"""
os_release_intel.py — the OS release a host's own services announce.

`os_fingerprint` names an exact OS release only when SMB answers on 445 (the
NTLM build). A TTL guess says "Linux" or "Windows", never which release, so on
every Linux host and every Windows host with 445 closed the end-of-life rule had
nothing to read. The Ubuntu and Debian rows in eol_catalog.py could never fire.

A distribution's packaged OpenSSH announces the release it was built for:

    SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.7      -> Ubuntu 18.04
    SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u7       -> Debian 9

A distribution keeps the same upstream OpenSSH version for the life of a
release (security fixes are backported, not rebased), so the upstream version
plus the distro tag identifies the release. The Debian `+debNuM` suffix names
the release outright.

Only releases whose packaged OpenSSH version is unique to them are listed. An
unlisted version returns None (release unknown), never a guess: a wrong release
here would become a false end-of-life finding.
"""
from __future__ import annotations

import re
from typing import Optional

# Upstream OpenSSH version -> Ubuntu LTS release that ships it.
_UBUNTU_OPENSSH = {
    "6.6.1p1": "14.04",
    "7.2p2": "16.04",
    "7.6p1": "18.04",
    "8.2p1": "20.04",
    "8.9p1": "22.04",
    "9.6p1": "24.04",
}

# Upstream OpenSSH version -> Debian release, for banners without a +debN suffix.
_DEBIAN_OPENSSH = {
    "6.7p1": "8",
    "7.4p1": "9",
    "7.9p1": "10",
    "8.4p1": "11",
    "9.2p1": "12",
}

_SOFTWARE = re.compile(r"^OpenSSH_(\d+\.\d+(?:\.\d+)?p\d+)$")
_DEB_SUFFIX = re.compile(r"\+deb(\d+)u\d+")


def release_from_ssh_banner(software: str | None, comments: str | None) -> Optional[str]:
    """'OpenSSH_7.6p1', 'Ubuntu-4ubuntu0.7' -> 'Ubuntu 18.04'; None when unknown."""
    if not software or not comments:
        return None
    m = _SOFTWARE.match(str(software).strip())
    if not m:
        return None
    upstream = m.group(1)
    tag = str(comments).strip()
    low = tag.lower()
    if "ubuntu" in low:
        # Ubuntu's own tag ("Ubuntu-…" today, "Debian-…ubuntu…" before 13.x).
        rel = _UBUNTU_OPENSSH.get(upstream)
        return f"Ubuntu {rel}" if rel else None
    if low.startswith(("debian-", "raspbian-")):
        deb = _DEB_SUFFIX.search(tag)
        rel = deb.group(1) if deb else _DEBIAN_OPENSSH.get(upstream)
        return f"Debian {rel}" if rel else None
    return None


def release_from_ssh_fact(data: dict) -> Optional[dict]:
    """{os_release, os_release_source, os_release_evidence} from one ssh_scan fact's
    data, or None. Reads the parsed banner the probe already ships
    (data.banner = {software, comments, raw})."""
    if not isinstance(data, dict):
        return None
    banner = data.get("banner")
    if not isinstance(banner, dict):
        return None
    release = release_from_ssh_banner(banner.get("software"), banner.get("comments"))
    if not release:
        return None
    return {"os_release": release, "os_release_source": "ssh_banner",
            "os_release_evidence": banner.get("raw")
            or f"{banner.get('software')} {banner.get('comments')}"}
