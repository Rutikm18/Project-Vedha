"""
matcher.py — does this CPE candidate's version fall inside a vulnerable
range, per the offline snapshot?

OSV's range format (not NVD's versionStart/EndIncluding/Excluding fields —
see vuln_db.py's docstring for why this project uses OSV): each `ranges[]`
entry holds an `events[]` sequence, version-ordered, alternating
`introduced` / `fixed` / `last_affected` markers. A version is vulnerable if
it falls in any [introduced, fixed) or [introduced, last_affected] interval
the sequence describes. There can be multiple such intervals in one
sequence (vulnerable, fixed, regressed, fixed again) — this walks the whole
sequence, not just the first pair.

THE CORE ANTI-FALSE-POSITIVE RULE (per spec 1.4): a version-range match
alone is never enough to call a finding "confirmed". Confirmed requires
BOTH a range match AND Fact.source_confidence == authoritative (the host's
own credentialed package list said so). A match from an inferred source
(a banner, a header) can only ever produce "suspected" — distros backport
security fixes while keeping the upstream version string unchanged, so a
banner-only version match against a backport-patched host is a classic,
well-documented false-positive trap, not a confirmed vulnerability.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

from cpe_normalizer import CPECandidate
from models import Finding, FindingState, SourceConfidence, make_finding_id
from version_compare import dpkg_compare, has_ambiguous_epoch
from vuln_db import VulnDB


def _safe_compare(a: str, b: str) -> int | None:
    """dpkg_compare, but None instead of a misleading answer when one side
    has an explicit epoch the other structurally can never carry (see
    version_compare.has_ambiguous_epoch's docstring — found via testing a
    real banner-derived MariaDB version against a real epoch-1 CVE range).
    """
    if has_ambiguous_epoch(a, b):
        return None
    return dpkg_compare(a, b)


# ── banner (upstream) versions vs Debian package bounds ──────────────────────
# A network banner carries the UPSTREAM version only ("vsftpd 3.0.5", "OpenSSH_9.6p1"):
# no Debian epoch, no Debian revision, no "+dfsg" repack tag. The snapshot's bounds are
# full Debian package versions ("1:9.6p1-1", "3.0.5-0.1", "1.3.8+dfsg-1"). Comparing the
# two with dpkg semantics is wrong in both directions:
#   * revision: dpkg ranks "3.0.5" BELOW "3.0.5-0.1", so the upstream release that
#     carries the fix still read as vulnerable (vsftpd 2.3.4 / 3.0.5 false positives);
#   * epoch:   _safe_compare refuses an epoch-vs-no-epoch comparison, so EVERY bound of
#     an epoch'd package (openssh, samba, redis, bind9, ...) was skipped and a banner
#     could only ever hit open-ended ranges (regreSSHion on OpenSSH 9.6p1 was missed).
# So a banner is compared upstream-to-upstream. Where the upstream parts are EQUAL the
# Debian revision decides what the bound means:
#   * a first-packaging revision ("-1", "-0", "-0.1", also "-1~deb11u1" for a stable
#     backport of a new upstream) means Debian fixed it by packaging that upstream
#     release, so the upstream release itself carries the fix;
#   * any other revision ("-12+deb11u1", "-3") means Debian fixed it with its own
#     patch, so the upstream release is still vulnerable (and a Debian host may have the
#     patch: that is why a banner match is only ever `suspected`, backport-possible).
_REPACK_SUFFIX = re.compile(r"[+~.](?:dfsg|ds|repack)\d*$", re.IGNORECASE)
_FIRST_PACKAGING = re.compile(r"^(?:0|1|0\.1)$")
_PORTABLE_SUFFIX = re.compile(r"p(\d+)")


# Bump when a change to this module can change WHICH CVEs a given input matches.
# Stamped on every Finding; auto-resolution will not read "absent under a different
# matcher" as "fixed" (app/detection/resolution.py).
#   1  dpkg comparison for every source (implicit before this constant existed)
#   2  banner versions compared upstream-to-upstream / Debian-revision / distro build
#   3  a banner without OpenSSH's portable suffix ("10.3") equals "10.3p1"
#   4  "+debNuM"/"~debNuM" (M>1) revisions are Debian patches; multi-branch products
#      need a fix on the banner's own line; DEBIAN-CVE ids merge with CVE ids
MATCHER_REVISION = "4"


# Products that maintain several release lines at once: a fix known only on a NEWER
# line (Debian 13 moved Redis to 8.0) says nothing about whether the banner's own line
# (Redis 7.2, which upstream fixed in 7.2.11) has it. For these, an upstream banner
# match is only a version signal when the fix is on the banner's own line. Keyed by
# the OSV source package (CPECandidate.lookup_key).
_MULTI_BRANCH = frozenset({
    "redis", "mariadb", "postgresql-15", "openssl", "bind9", "samba", "nginx",
    "squid", "tomcat9", "jetty9", "python-werkzeug", "exim4", "dovecot", "postfix",
})


def _branch(version: str | None, lookup_key: str) -> tuple[int, ...] | None:
    """The release line of an upstream version: major.minor ("7.2.16" -> (7, 2)),
    PostgreSQL 10+ by major alone, OpenSSL 1.x by three parts ("1.1.1f" -> (1,1,1))."""
    nums = [int(n) for n in re.findall(r"\d+", (version or "").split("-", 1)[0])[:3]]
    if not nums:
        return None
    if lookup_key.startswith("postgresql") and nums[0] >= 10:
        return tuple(nums[:1])
    if lookup_key == "openssl" and nums[0] < 3:
        return tuple(nums[:3])
    return tuple(nums[:2])


def _fix_on_other_line(interval: str | None, version: str, lookup_key: str) -> bool:
    """True when the matched interval's fixed bound is on a different release line
    than the banner version (multi-branch products only)."""
    if lookup_key not in _MULTI_BRANCH:
        return False
    fixed = _fixed_bound(interval) or (interval or "").strip("[]").split(",")[-1].strip()
    if not fixed or fixed == "unbounded":
        return False
    upstream, _ = _split_bound(fixed)
    a, b = _branch(version, lookup_key), _branch(upstream, lookup_key)
    return a is not None and b is not None and a != b


def _canonical_id(record_id: str) -> str:
    """'DEBIAN-CVE-2025-46817' (a record with no upstream list) -> 'CVE-2025-46817', so
    it merges with the same CVE from another record instead of duplicating it."""
    m = re.fullmatch(r"DEBIAN-(CVE-\d{4}-\d{4,7})", record_id or "")
    return m.group(1) if m else record_id


def _debian_release(revision: str | None) -> int | None:
    """'2+deb12u3' -> 12; '0+deb11u1' -> 11; '2' -> None (release not named)."""
    m = re.search(r"deb(\d{1,2})u\d", revision or "")
    return int(m.group(1)) if m else None


def _split_bound(bound: str) -> tuple[str, str | None]:
    """'1:9.6p1-1' -> ('9.6p1', '1'); '1.3.8+dfsg-1' -> ('1.3.8', '1'); '0' -> ('0', None)."""
    rest = bound.split(":", 1)[1] if ":" in bound else bound
    upstream, revision = (rest.rsplit("-", 1) + [None])[:2] if "-" in rest else (rest, None)
    return _REPACK_SUFFIX.sub("", upstream), revision


def banner_upstream(version: str) -> str:
    """The upstream part of an observed (banner) version: no epoch, nothing after the
    first '-' ("10.11.6-MariaDB-0+deb12u1" -> "10.11.6")."""
    v = version.split(":", 1)[1] if ":" in version else version
    return v.split("-", 1)[0]


def _revision_is_first_packaging(revision: str | None) -> bool:
    """True when a Debian revision means "upstream release X as first packaged":
    "1", "0", "0.1", a stable rebuild of it ("1~deb11u1", "1~bpo11+1"). False for
    Debian's own fixes on top: "1+deb12u1" (stable/security update), "1~deb12u4"
    (the 4th update of that rebuild), "3", "12+deb11u1"."""
    if revision is None:
        return True          # a bound with no revision IS an upstream version
    base, _, tail = revision.partition("~")
    if not _FIRST_PACKAGING.match(base):
        return False         # includes "1+deb12u1": a "+" update carries a patch
    m = re.fullmatch(r"(?:deb\d+u|bpo\d+\+)(\d+)", tail)
    return not (m and int(m.group(1)) > 1)


def _upstream_compare(version: str, bound: str, *, fixed: bool = False) -> int | None:
    """Compare an upstream (banner) version with a Debian bound, upstream to upstream.

    Returns -1 / 0 / 1 like dpkg_compare. For a `fixed` bound with an equal upstream part
    the revision decides (see the block comment above): first packaging -> 0 (at the fix,
    not vulnerable), a Debian patch revision -> -1 (upstream release still vulnerable)."""
    if bound == "0":
        return 1             # OSV's "no lower bound" sentinel
    upstream, revision = _split_bound(bound)
    if not upstream:
        return None
    portable = _PORTABLE_SUFFIX.fullmatch(upstream[len(version):]) \
        if upstream.startswith(version) else None
    if portable:
        # The banner omits OpenSSH's portable suffix ("OpenSSH_10.3" from Alpine,
        # macOS, Windows) and the bound is that release plus "pN". Every build of the
        # release is at least p1, so p1 counts as equal; p2+ cannot be told apart
        # ("9.3" may be 9.3p1 or 9.3p2), so no claim is made either way.
        if portable.group(1) != "1":
            return None
        c = 0
    else:
        c = dpkg_compare(version, upstream)
    if c == 0 and fixed and not _revision_is_first_packaging(revision):
        return -1
    return c


def _debian_rev_compare(version: str, bound: str) -> int | None:
    """A banner-derived Debian package version ("9.2p1-2+deb12u3", no epoch: the
    banner never shows one) against a Debian bound: dpkg order with the bound's
    epoch dropped, revision kept. Exact for the release the revision belongs to."""
    if bound == "0":
        return 1
    rest = bound.split(":", 1)[1] if ":" in bound else bound
    return dpkg_compare(version, rest)


def _version_in_ranges(
    version: str, ranges: list[dict], *, upstream: bool = False, debian_rev: bool = False
) -> tuple[bool, str | None, str | None]:
    """Returns (matched, matched_interval_desc, range_kind).

    `range_kind` records how *specific* the matched interval is — the axis the
    false-positive fix (gap #4) turns on:
        "bounded"  [introduced, fixed)        — a real upper version bound
        "capped"   [introduced, last_affected]— a known greatest-affected bound
        "open"     [introduced, unbounded)    — NO upper bound; matches every
                                                version from `introduced` onward
    and is None when nothing matched. An open interval carries no version
    discrimination (an `introduced:"0"` open range matches literally every
    version), so the caller must treat an inferred-source open match as
    product-presence, not a version-range vulnerability — see match_candidate.

    A range boundary this version's epoch can't be safely compared against
    is treated as "cannot determine" (skipped), never as a coincidental
    match or non-match — see _safe_compare.

    `debian_rev=True` is for a banner that carries the Debian package revision
    (see _debian_rev_compare); the caller limits `ranges` to that release.

    `upstream=True` is for a banner (upstream-only) version: every bound is
    compared upstream-to-upstream (_upstream_compare), so the Debian epoch and
    revision neither skip the bound nor shift the answer. The caller passes the
    version already reduced by banner_upstream().
    """
    def cmp(bound: str, *, fixed: bool = False) -> int | None:   # version vs bound
        if debian_rev:
            return _debian_rev_compare(version, bound)
        if upstream:
            return _upstream_compare(version, bound, fixed=fixed)
        c = _safe_compare(bound, version)
        return None if c is None else -c

    def at_or_after(bound: str) -> bool | None:          # bound <= version
        c = cmp(bound)
        return None if c is None else c >= 0

    def before_fixed(bound: str) -> bool | None:         # version < fixed
        c = cmp(bound, fixed=True)
        return None if c is None else c < 0

    def at_or_before(bound: str) -> bool | None:         # version <= last_affected
        c = cmp(bound)
        return None if c is None else c <= 0

    for rng in ranges:
        if rng.get("type") not in ("ECOSYSTEM", "SEMVER"):
            continue
        events = rng.get("events", [])
        introduced = None
        for ev in events:
            if "introduced" in ev:
                introduced = ev["introduced"]
            elif "fixed" in ev:
                if introduced is not None:
                    if at_or_after(introduced) and before_fixed(ev["fixed"]):
                        return True, f"[{introduced}, {ev['fixed']})", "bounded"
                introduced = None
            elif "last_affected" in ev:
                if introduced is not None:
                    if at_or_after(introduced) and at_or_before(ev["last_affected"]):
                        return True, f"[{introduced}, {ev['last_affected']}]", "capped"
                introduced = None
        # Sequence ended with an open lower bound and no closing event —
        # OSV convention: still vulnerable from `introduced` onward. The match
        # stands (so an authoritative dpkg finding for an unfixed package is not
        # lost), but it is tagged "open" so an inferred match can be demoted.
        if introduced is not None and at_or_after(introduced):
            return True, f"[{introduced}, unbounded)", "open"
    return False, None, None


def _upstream_past_a_fix(version: str, affected_entries: list[dict]) -> bool:
    """True when some distro release recorded a fix for this CVE and the banner's
    upstream version is at or past it: a range whose LAST event is `fixed` (no later
    re-introduction) with version >= that bound, per _upstream_compare.

    Used only for an inferred (banner) version with an open-ended match: Debian 11
    listing "no fix shipped" while Debian 13 fixed the CVE by packaging upstream 3.0.5
    says nothing about an upstream 3.0.5 build, which already carries the fix. A
    regression (fixed, then introduced again) never counts: its last event is not
    `fixed`."""
    for aff in affected_entries:
        if aff.get("package", {}).get("ecosystem") == "NVD/CPE":
            continue                      # the NVD companion has its own check
        for rng in aff.get("ranges", []):
            if rng.get("type") not in ("ECOSYSTEM", "SEMVER"):
                continue
            events = rng.get("events", [])
            if not events or "fixed" not in events[-1]:
                continue
            c = _upstream_compare(version, events[-1]["fixed"], fixed=True)
            if c is not None and c >= 0:
                return True
    return False


def _nvd_excludes_version(version: str, affected_entries: list[dict]) -> bool:
    """True iff an upstream NVD/CPE-ecosystem *bounded* range exists for this CVE
    and the version is confidently OUTSIDE every one of them — i.e. the host is
    not vulnerable to this CVE by its upstream version (gap #4 phase 2: "bound
    the open-ended distro records with upstream NVD data").

    Only the NVD/CPE companion is consulted here, on purpose: its ranges are
    clean upstream SEMVER (``introduced:"0" → fixed:X``) with no Debian epoch /
    revision, so comparing a network-banner version against them is reliable —
    exactly the comparison the Debian ecosystem cannot do for a banner. Never
    suppresses on an ambiguous/undeterminable comparison (``_safe_compare`` None)
    or when no evaluable NVD bounded range is present: absence of proof is not
    proof of safety.
    """
    saw_evaluable_bounded = False
    for aff in affected_entries:
        if aff.get("package", {}).get("ecosystem") != "NVD/CPE":
            continue
        for rng in aff.get("ranges", []):
            if rng.get("type") not in ("ECOSYSTEM", "SEMVER"):
                continue
            introduced = None
            for ev in rng.get("events", []):
                if "introduced" in ev:
                    introduced = ev["introduced"]
                elif "fixed" in ev:
                    lo = _safe_compare(introduced, version) if introduced is not None else 0
                    hi = _safe_compare(version, ev["fixed"])
                    if lo is not None and hi is not None:
                        saw_evaluable_bounded = True
                        if lo <= 0 and hi < 0:
                            return False  # vulnerable per upstream NVD — never suppress
                    introduced = None
                elif "last_affected" in ev:
                    lo = _safe_compare(introduced, version) if introduced is not None else 0
                    hi = _safe_compare(version, ev["last_affected"])
                    if lo is not None and hi is not None:
                        saw_evaluable_bounded = True
                        if lo <= 0 and hi <= 0:
                            return False
                    introduced = None
    return saw_evaluable_bounded


def _fixed_bound(interval: str | None) -> str | None:
    """The first non-vulnerable release of a matched ``[introduced, fixed)``
    interval — the upgrade target a remediation plan names. A ``last_affected``
    interval (closed ``]``) or an unbounded one has no known fixed release, so it
    returns None rather than guessing."""
    if not interval or not interval.endswith(")"):
        return None
    hi = interval[1:-1].split(",", 1)[-1].strip()
    return None if hi in ("", "unbounded") else hi


def _fix_for_scheme(bound: str | None, compare_version: str, *, package: bool) -> str | None:
    """The fix version in the same terms as the observed version.

    package=True (a dpkg or Debian-revision version): the Debian package version
    itself — what `apt` installs. package=False (an upstream banner): the upstream
    release, without epoch / revision / repack tag ("1:9.8p1-1" -> "9.8p1"); None when
    the fix was only a Debian patch on the very upstream release observed, because no
    upstream release is then known to carry it."""
    if not bound:
        return None
    if package:
        return bound
    upstream, revision = _split_bound(bound)
    if not upstream:
        return None
    if dpkg_compare(compare_version, upstream) >= 0 and not _revision_is_first_packaging(revision):
        return None
    return upstream


def match_candidate(asset_ip: str, candidate: CPECandidate, db: VulnDB) -> list[Finding]:
    """All Findings this single CPE candidate produces against the snapshot.
    Empty list if the product isn't in the snapshot or no range matches —
    that's a correct negative, not a failure. asset_ip is passed explicitly
    by the caller (which already knows which Asset this candidate's
    underlying Fact came from) — CPECandidate.source_ref only points at a
    file:line, not the asset, by design (see cpe_normalizer.py).
    """
    # version_raw, not version_normalized — OSV's Debian-ecosystem range
    # strings are FULL dpkg version strings (epoch:upstream-revision).
    # version_normalized deliberately strips epoch/revision for CPE display
    # purposes (cpe_normalizer.py), but epoch dominates dpkg comparison: a
    # stripped "9.6p1" (implicit epoch 0) would compare as OLDER than a
    # range string like "1:3.9p1-1" (epoch 1) purely from the missing
    # epoch — found via testing against real data, not a hypothetical.
    version = candidate.version_raw or candidate.version_normalized
    if not version:
        return []  # a wildcard-version candidate (e.g. a tech_hint) has
                    # nothing to range-match against; correlate.py may still
                    # want to surface "product present, version unknown"
                    # separately, but that's not this function's job.

    # lookup_key, not product — the vuln_db snapshot is indexed by OSV
    # source-package name, which can differ from the CPE product name
    # (e.g. "apache2" vs "http_server"). See cpe_normalizer.py's
    # _PACKAGE_TO_CPE module comment for the full explanation.
    records = db.lookup(candidate.lookup_key)
    is_authoritative = candidate.source_confidence == SourceConfidence.authoritative
    # How the observed version is compared (see the banner block comment above):
    #   authoritative  the host's own dpkg version: exact dpkg order, unchanged.
    #   debian_rev     a banner naming a Debian build WITH its package revision
    #                  ("OpenSSH_9.2p1 Debian-2+deb12u3"): the real package
    #                  version, compared within its own Debian release. Exact, so
    #                  no backport caveat.
    #   distro         a banner naming a backporting build WITHOUT a revision
    #                  (Ubuntu, RHEL, "Apache (Debian)", Microsoft's OpenSSH port):
    #                  the version cannot show which fixes are in. Compared
    #                  upstream-to-upstream but reported as `range-distro`
    #                  product presence, never as a customer finding.
    #   upstream       any other banner: upstream-to-upstream.
    debian_rev = (not is_authoritative and candidate.distro == "debian"
                  and bool(candidate.distro_revision))
    distro_build = not is_authoritative and bool(candidate.distro) and not debian_rev
    if is_authoritative:
        compare_version = version
    elif debian_rev:
        compare_version = f"{banner_upstream(version)}-{candidate.distro_revision}"
    else:
        compare_version = banner_upstream(version)
    release = _debian_release(candidate.distro_revision) if debian_rev else None
    upstream_mode = not is_authoritative and not debian_rev
    if not is_authoritative and not compare_version[:1].isdigit():
        # A banner "version" that does not start with a digit ("", "for_Windows_9.5"
        # before cleaning, a hostile string) has no order against a version bound:
        # it would sort below everything and match every [0, ...) range.
        return []

    # Gap #4 phase 2: aggregate every matching range PER CVE before emitting, so
    # the most *specific* verdict wins. A bounded match ([intro,fixed) /
    # [intro,last_affected]) is a real version signal and beats an open-ended
    # match (which matches every version and is only product-presence). This also
    # collapses the old one-finding-per-record duplication into one finding per
    # CVE. Insertion order is preserved for deterministic output.
    agg: dict[str, dict] = {}
    for rec in records:
        cve_ids = rec.get("upstream") or [_canonical_id(rec["id"])]
        for aff in rec.get("affected", []):
            if aff.get("package", {}).get("name") != candidate.lookup_key:
                continue
            ecosystem = aff.get("package", {}).get("ecosystem") or ""
            if debian_rev:
                # A package revision only means something inside its own release.
                # Known release: only that release's ranges. Unknown (no "debNNuM"):
                # every Debian release's ranges, and all of them must agree below.
                if not ecosystem.startswith("Debian"):
                    continue
                if release is not None and ecosystem != f"Debian:{release}":
                    continue
            matched, interval, range_kind = _version_in_ranges(
                compare_version, aff.get("ranges", []),
                upstream=upstream_mode, debian_rev=debian_rev)
            for cve_id in cve_ids:
                slot = agg.setdefault(cve_id, {"bounded": None, "open": None, "affected": [],
                                               "entries": 0, "entries_matched": 0,
                                               "other_line": None})
                slot["affected"].append(aff)
                slot["entries"] += 1
                slot["entries_matched"] += 1 if matched else 0
                if matched and range_kind in ("bounded", "capped"):
                    # Prefer a fix on the banner's own release line (multi-branch
                    # products); remember one on another line in case it is all there is.
                    if upstream_mode and _fix_on_other_line(interval, compare_version,
                                                            candidate.lookup_key):
                        slot["other_line"] = slot["other_line"] or interval
                    elif slot["bounded"] is None:
                        slot["bounded"] = interval
                elif matched and range_kind == "open" and slot["open"] is None:
                    slot["open"] = interval

    findings: list[Finding] = []
    for cve_id, slot in agg.items():
        if debian_rev and release is None and slot["entries_matched"] < slot["entries"]:
            continue  # some Debian release already ships this exact package fixed
        other_line = False
        if slot["bounded"] is not None:
            interval, open_ended = slot["bounded"], False
        elif slot["other_line"] is not None and not (
                slot["open"] is not None and _upstream_past_a_fix(compare_version, slot["affected"])):
            # Only fixed on another release line of a multi-branch product: whether
            # the banner's own line has a backport is unknown -> product presence.
            interval, open_ended, other_line = slot["other_line"], False, True
        elif slot["other_line"] is not None:
            continue
        elif slot["open"] is not None:
            # Open-ended match only. For an inferred (banner) source, consult the
            # upstream NVD/CPE companion: if a bounded upstream range confidently
            # excludes this version, the host is NOT vulnerable to this CVE —
            # suppress the finding entirely rather than emit open-ended noise. An
            # authoritative (dpkg) finding against the distro is kept regardless:
            # the distro's "no fix released" verdict is the authority there.
            if not is_authoritative and not debian_rev and (
                    _nvd_excludes_version(compare_version, slot["affected"])
                    or _upstream_past_a_fix(compare_version, slot["affected"])):
                continue
            interval, open_ended = slot["open"], True
        else:
            continue  # no range matched for this CVE — a correct negative

        # Confirmed requires authoritative evidence, not just a range match (see
        # module docstring). An open-ended match from an inferred source is
        # demoted to `potential` under a distinct `range-open` basis so it never
        # sits in the suspected queue beside real bounded matches; an
        # authoritative open-ended match keeps its confirmed state (a genuine "no
        # fix released yet" distro fact), only annotated. A distro build without
        # a revision is `range-distro`: product presence, verify the patch level.
        if open_ended and not is_authoritative:
            state, basis = FindingState.potential, "range-open"
        elif distro_build:
            state, basis = FindingState.potential, "range-distro"
        elif other_line:
            state, basis = FindingState.potential, "range-branch"
        else:
            state = FindingState.confirmed if is_authoritative else FindingState.suspected
            basis = "range"
        backport_possible = not is_authoritative and not debian_rev
        findings.append(Finding(
            finding_id=make_finding_id(asset_ip, cve_id, candidate.cpe23()),
            asset_ip=asset_ip,
            cpe=candidate.cpe23(),
            cve_id=cve_id,
            match_basis=basis,
            state=state,
            source_confidence=(SourceConfidence.authoritative if is_authoritative
                               else SourceConfidence.inferred),
            evidence_refs=[candidate.source_ref],
            db_snapshot_hash=db.meta.content_hash,
            created_at=datetime.now(timezone.utc).isoformat(),
            matched_version=version,
            fixed_version=_fix_for_scheme(_fixed_bound(interval), compare_version,
                                          package=is_authoritative or debian_rev),
            fixed_version_raw=_fixed_bound(interval),
            matched_range=interval,
            version_scheme="package" if (is_authoritative or debian_rev) else "upstream",
            port=candidate.port,
            proto=candidate.proto,
            ports=[candidate.port] if candidate.port is not None else [],
            product=candidate.product,
            vendor=candidate.vendor,
            distro=candidate.distro,
            ai_assisted=candidate.ai_assisted,
            matcher_revision=MATCHER_REVISION,
            notes=[f"{candidate.basis} | matched range {interval}"]
                  + (["version-inferred, backport-possible"] if backport_possible else [])
                  + ([f"Debian package {compare_version} read from the banner, "
                      f"compared within Debian {release or '(all releases agree)'}"]
                     if debian_rev else [])
                  + ([f"fixed on another {candidate.product} release line "
                      f"({_fixed_bound(interval) or interval}); whether this line "
                      "has a backported fix is unknown from the version alone — "
                      "verify against the vendor advisory"] if other_line else [])
                  + ([f"{candidate.distro} build: the banner version cannot show "
                      "backported fixes — product presence; verify the patch level "
                      "with a credentialed scan"] if distro_build else [])
                  + (["open-ended range (no fixed release) — product-presence only, "
                      "version not discriminated"] if open_ended and not is_authoritative else [])
                  + (["distro lists no fixed release for this package (open-ended range)"]
                     if open_ended and is_authoritative else [])
                  + (["AI-assisted normalization — extra scrutiny advised"] if candidate.ai_assisted else []),
        ))
    return findings
