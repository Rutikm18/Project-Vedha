# Node Description Batch 194 of 330

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_engine_posture_rules_rationale_466": "VNC type 2 is the legacy DES-based challenge with an 8-character password     ce" | kind=entity | source=manager/detection_engine/posture_rules.py:L466 | neighbors=[_vnc_weak_auth()] | lang=en
- "detection_engine_posture_rules_rationale_71": "Resolve `a.b.c` inside a Fact.data dict. Returns `_MISSING` (never None)     whe" | kind=entity | source=manager/detection_engine/posture_rules.py:L71 | neighbors=[get_path()] | lang=pt
- "detection_engine_posture_rules_rationale_768": "True when the scanner ran but the service did NOT answer — so a rule's     decla" | kind=entity | source=manager/detection_engine/posture_rules.py:L768 | neighbors=[_fact_indicates_no_service()] | lang=en
- "detection_engine_posture_rules_rationale_781": "Evaluate ONE rule against ONE fact and record the outcome. NEVER raises —     a" | kind=entity | source=manager/detection_engine/posture_rules.py:L781 | neighbors=[evaluate_rule()] | lang=en
- "detection_engine_posture_rules_rationale_816": "Best-effort confidence calibration (lazy import breaks the module cycle;     cal" | kind=entity | source=manager/detection_engine/posture_rules.py:L816 | neighbors=[_calibrate_host_findings()] | lang=en
- "detection_engine_posture_rules_rationale_830": "Like `detect_posture`, but ALSO returns a per-evaluation trace. The findings" | kind=entity | source=manager/detection_engine/posture_rules.py:L830 | neighbors=[detect_posture_traced()] | lang=en
- "detection_engine_posture_rules_rationale_910": "Apply every posture rule to one asset's facts. Deduplicates by     (rule_id, por" | kind=entity | source=manager/detection_engine/posture_rules.py:L910 | neighbors=[detect_posture()] | lang=en
- "detection_engine_posture_rules_rationale_942": "Findings for risky OPEN ports that have no dedicated scanner: backdoor/C2     li" | kind=entity | source=manager/detection_engine/posture_rules.py:L942 | neighbors=[detect_exposed_services()] | lang=en
- "detection_engine_posture_rules_tracerow_to_dict": ".to_dict()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L121 | neighbors=[TraceRow] | lang=en
- "detection_engine_update_snapshot_rationale_1": "update_snapshot.py — the ONLY module in this package that talks to the network." | kind=entity | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[update_snapshot.py] | lang=en
- "detection_engine_update_snapshot_rationale_118": "The full CISA Known Exploited Vulnerabilities catalog — a single flat     list," | kind=entity | source=manager/detection_engine/update_snapshot.py:L118 | neighbors=[sync_kev_snapshot()] | lang=en
- "detection_engine_update_snapshot_rationale_121": "The full CISA Known Exploited Vulnerabilities catalog — a single flat     list," | kind=entity | source=manager/detection_engine/update_snapshot.py:L121 | neighbors=[sync_kev_snapshot()] | lang=en
- "detection_engine_update_snapshot_rationale_140": "EPSS scores for exactly the CVE IDs this detection run actually cares     about" | kind=entity | source=manager/detection_engine/update_snapshot.py:L140 | neighbors=[sync_epss_snapshot()] | lang=en
- "detection_engine_update_snapshot_rationale_143": "EPSS scores for exactly the CVE IDs this detection run actually cares     about" | kind=entity | source=manager/detection_engine/update_snapshot.py:L143 | neighbors=[sync_epss_snapshot()] | lang=en
- "detection_engine_update_snapshot_rationale_178": "The ENTIRE EPSS catalog (every scored CVE) from FIRST.org's daily     gzipped CS" | kind=entity | source=manager/detection_engine/update_snapshot.py:L178 | neighbors=[sync_epss_full()] | lang=en
- "detection_engine_update_snapshot_rationale_38": "Some macOS python.org installs ship expecting `Install Certificates.     command" | kind=entity | source=manager/detection_engine/update_snapshot.py:L38 | neighbors=[_ssl_context()] | lang=en
- "detection_engine_update_snapshot_rationale_55": "All known vulnerabilities OSV has for this (product, ecosystem) pair,     with n" | kind=entity | source=manager/detection_engine/update_snapshot.py:L55 | neighbors=[_query_osv()] | lang=en
- "detection_engine_update_snapshot_rationale_79": "Fetch real OSV records for every product, write a pinned snapshot.      rate_lim" | kind=entity | source=manager/detection_engine/update_snapshot.py:L79 | neighbors=[sync_snapshot()] | lang=en
- "detection_engine_version_compare_rationale_1": "version_compare.py — per-scheme version comparators.  Spec calls this \"the highe" | kind=entity | source=manager/detection_engine/version_compare.py:L1 | neighbors=[version_compare.py] | lang=en
- "detection_engine_version_compare_rationale_105": "1:8.4p1-5+deb11u1' -> (epoch='1', upstream='8.4p1', revision='5+deb11u1').     N" | kind=entity | source=manager/detection_engine/version_compare.py:L105 | neighbors=[_split_dpkg_version()] | lang=en
- "detection_engine_version_compare_rationale_111": "1:8.4p1-5+deb11u1' -> (epoch='1', upstream='8.4p1', revision='5+deb11u1').     N" | kind=entity | source=manager/detection_engine/version_compare.py:L111 | neighbors=[_split_dpkg_version()] | lang=en
- "detection_engine_version_compare_rationale_124": "True when exactly one of the two version strings carries an explicit,     non-ze" | kind=entity | source=manager/detection_engine/version_compare.py:L124 | neighbors=[has_ambiguous_epoch()] | lang=en
- "detection_engine_version_compare_rationale_130": "True when exactly one of the two version strings carries an explicit,     non-ze" | kind=entity | source=manager/detection_engine/version_compare.py:L130 | neighbors=[has_ambiguous_epoch()] | lang=en
- "detection_engine_version_compare_rationale_167": "-1 if a<b, 0 if a==b, 1 if a>b, per Debian version ordering. Prefers     the rea" | kind=entity | source=manager/detection_engine/version_compare.py:L167 | neighbors=[dpkg_compare()] | lang=pt
- "detection_engine_version_compare_rationale_173": "-1 if a<b, 0 if a==b, 1 if a>b, per Debian version ordering.      Uses the pure-" | kind=entity | source=manager/detection_engine/version_compare.py:L173 | neighbors=[dpkg_compare()] | lang=pt
- "detection_engine_version_compare_rationale_178": "Plain dotted-numeric comparison for non-distro upstream versions     (banner-der" | kind=entity | source=manager/detection_engine/version_compare.py:L178 | neighbors=[semver_compare()] | lang=en
- "detection_engine_version_compare_rationale_190": "Plain dotted-numeric comparison for non-distro upstream versions     (banner-der" | kind=entity | source=manager/detection_engine/version_compare.py:L190 | neighbors=[semver_compare()] | lang=en
- "detection_engine_version_compare_rationale_220": "Test hook: drop the in-memory record of which snapshots were validated." | kind=entity | source=manager/detection_engine/version_compare.py:L220 | neighbors=[_clear_validation_cache()] | lang=en
- "detection_engine_version_compare_rationale_244": "Confirm pure-Python agrees with the real dpkg binary on the ordering of     `ver" | kind=entity | source=manager/detection_engine/version_compare.py:L244 | neighbors=[verify_pure_python_matches_dpkg()] | lang=en
- "detection_engine_version_compare_rationale_31": "Real dpkg --compare-versions. None (not an error) if dpkg isn't     installed or" | kind=entity | source=manager/detection_engine/version_compare.py:L31 | neighbors=[_dpkg_compare_via_binary()] | lang=en
- "detection_engine_version_compare_rationale_37": "Real dpkg --compare-versions. None (not an error) if dpkg isn't     installed or" | kind=entity | source=manager/detection_engine/version_compare.py:L37 | neighbors=[_dpkg_compare_via_binary()] | lang=en
- "detection_engine_version_compare_rationale_53": "dpkg's non-digit character ordering: '~' sorts before EVERYTHING,     including" | kind=entity | source=manager/detection_engine/version_compare.py:L53 | neighbors=[_char_order()] | lang=en
- "detection_engine_version_compare_rationale_59": "dpkg's non-digit character ordering: '~' sorts before EVERYTHING,     including" | kind=entity | source=manager/detection_engine/version_compare.py:L59 | neighbors=[_char_order()] | lang=en
- "detection_engine_version_compare_rationale_86": "upstream_version or debian_revision comparison (no epoch, no '-')." | kind=entity | source=manager/detection_engine/version_compare.py:L86 | neighbors=[_compare_part()] | lang=en
- "detection_engine_version_compare_rationale_92": "upstream_version or debian_revision comparison (no epoch, no '-')." | kind=entity | source=manager/detection_engine/version_compare.py:L92 | neighbors=[_compare_part()] | lang=en
- "detection_engine_vuln_db_rationale_1": "vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN" | kind=entity | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[vuln_db.py] | lang=en
- "detection_engine_vuln_db_rationale_102": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L102 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_rationale_106": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L106 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_rationale_110": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L110 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_113": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L113 | neighbors=[.get_cvss_vector()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-193.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
