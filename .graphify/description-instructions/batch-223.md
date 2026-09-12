# Node Description Batch 224 of 380

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

- "detection_engine_posture_rules_rationale_1252": "Engagement-level coverage roll-up over a set of traces. `rules_blind > 0`     is" | kind=entity | source=manager/detection_engine/posture_rules.py:L1252 | neighbors=[summarize_traces()] | lang=en
- "detection_engine_posture_rules_rationale_1284": "Traced counterpart of `detect_all` — findings identical, plus the full trace." | kind=entity | source=manager/detection_engine/posture_rules.py:L1284 | neighbors=[detect_all_traced()] | lang=en
- "detection_engine_posture_rules_rationale_1298": "Run posture detection across every asset. Accepts an IngestResult (uses its" | kind=entity | source=manager/detection_engine/posture_rules.py:L1298 | neighbors=[detect_all()] | lang=en
- "detection_engine_posture_rules_rationale_136": "severity × exposure × state → (risk_score 0-100, priority).      Authentication" | kind=entity | source=manager/detection_engine/posture_rules.py:L136 | neighbors=[compute_risk()] | lang=en
- "detection_engine_posture_rules_rationale_138": "severity × exposure × state → (risk_score 0-100, priority).      Authentication" | kind=entity | source=manager/detection_engine/posture_rules.py:L138 | neighbors=[compute_risk()] | lang=en
- "detection_engine_posture_rules_rationale_162": "Deterministic id — same (asset, rule, port) always hashes the same, so     re-sc" | kind=entity | source=manager/detection_engine/posture_rules.py:L162 | neighbors=[make_posture_id()] | lang=en
- "detection_engine_posture_rules_rationale_164": "Deterministic id — same (asset, rule, port) always hashes the same, so     re-sc" | kind=entity | source=manager/detection_engine/posture_rules.py:L164 | neighbors=[make_posture_id()] | lang=en
- "detection_engine_posture_rules_rationale_258": "Fires on EITHER of the rdp_scanner's two independent probes.      The scanner pr" | kind=entity | source=manager/detection_engine/posture_rules.py:L258 | neighbors=[_rdp_no_nla()] | lang=en
- "detection_engine_posture_rules_rationale_260": "Fires on EITHER of the rdp_scanner's two independent probes.      The scanner pr" | kind=entity | source=manager/detection_engine/posture_rules.py:L260 | neighbors=[_rdp_no_nla()] | lang=en
- "detection_engine_posture_rules_rationale_299": "The server REFUSED a TLS-capable negotiation, so the session falls back to     l" | kind=entity | source=manager/detection_engine/posture_rules.py:L299 | neighbors=[_rdp_no_tls()] | lang=en
- "detection_engine_posture_rules_rationale_301": "The server REFUSED a TLS-capable negotiation, so the session falls back to     l" | kind=entity | source=manager/detection_engine/posture_rules.py:L301 | neighbors=[_rdp_no_tls()] | lang=en
- "detection_engine_posture_rules_rationale_395": "A stable handle for collapsing identical findings across a fleet.      Twelve id" | kind=entity | source=manager/detection_engine/posture_rules.py:L395 | neighbors=[group_key_for()] | lang=pt
- "detection_engine_posture_rules_rationale_419": "A device from a known-defaults vendor that is exposing a login.      CANDIDATE," | kind=entity | source=manager/detection_engine/posture_rules.py:L419 | neighbors=[_default_cred_candidate()] | lang=en
- "detection_engine_posture_rules_rationale_460": "An OS past its vendor end-of-SECURITY-support date.      Reads the release strin" | kind=entity | source=manager/detection_engine/posture_rules.py:L460 | neighbors=[_os_eol()] | lang=en
- "detection_engine_posture_rules_rationale_466": "VNC type 2 is the legacy DES-based challenge with an 8-character password     ce" | kind=entity | source=manager/detection_engine/posture_rules.py:L466 | neighbors=[_vnc_weak_auth()] | lang=en
- "detection_engine_posture_rules_rationale_556": "VNC type 2 is the legacy DES-based challenge with an 8-character password     ce" | kind=entity | source=manager/detection_engine/posture_rules.py:L556 | neighbors=[_vnc_weak_auth()] | lang=en
- "detection_engine_posture_rules_rationale_616": "A database that served data to an UNAUTHENTICATED probe.      The strongest stat" | kind=entity | source=manager/detection_engine/posture_rules.py:L616 | neighbors=[_db_unauthenticated()] | lang=en
- "detection_engine_posture_rules_rationale_634": "A database listener that cannot negotiate TLS at all.      `ssl_supported is Fal" | kind=entity | source=manager/detection_engine/posture_rules.py:L634 | neighbors=[_db_cleartext_transport()] | lang=en
- "detection_engine_posture_rules_rationale_651": "Auth posture for risk shaping — only when the server stated it." | kind=entity | source=manager/detection_engine/posture_rules.py:L651 | neighbors=[_db_auth()] | lang=en
- "detection_engine_posture_rules_rationale_71": "Resolve `a.b.c` inside a Fact.data dict. Returns `_MISSING` (never None)     whe" | kind=entity | source=manager/detection_engine/posture_rules.py:L71 | neighbors=[get_path()] | lang=pt
- "detection_engine_posture_rules_rationale_73": "Resolve `a.b.c` inside a Fact.data dict. Returns `_MISSING` (never None)     whe" | kind=entity | source=manager/detection_engine/posture_rules.py:L73 | neighbors=[get_path()] | lang=pt
- "detection_engine_posture_rules_rationale_768": "True when the scanner ran but the service did NOT answer — so a rule's     decla" | kind=entity | source=manager/detection_engine/posture_rules.py:L768 | neighbors=[_fact_indicates_no_service()] | lang=en
- "detection_engine_posture_rules_rationale_781": "Evaluate ONE rule against ONE fact and record the outcome. NEVER raises —     a" | kind=entity | source=manager/detection_engine/posture_rules.py:L781 | neighbors=[evaluate_rule()] | lang=en
- "detection_engine_posture_rules_rationale_816": "Best-effort confidence calibration (lazy import breaks the module cycle;     cal" | kind=entity | source=manager/detection_engine/posture_rules.py:L816 | neighbors=[_calibrate_host_findings()] | lang=en
- "detection_engine_posture_rules_rationale_830": "Like `detect_posture`, but ALSO returns a per-evaluation trace. The findings" | kind=entity | source=manager/detection_engine/posture_rules.py:L830 | neighbors=[detect_posture_traced()] | lang=en
- "detection_engine_posture_rules_rationale_910": "Apply every posture rule to one asset's facts. Deduplicates by     (rule_id, por" | kind=entity | source=manager/detection_engine/posture_rules.py:L910 | neighbors=[detect_posture()] | lang=en
- "detection_engine_posture_rules_rationale_942": "Findings for risky OPEN ports that have no dedicated scanner: backdoor/C2     li" | kind=entity | source=manager/detection_engine/posture_rules.py:L942 | neighbors=[detect_exposed_services()] | lang=en
- "detection_engine_posture_rules_rationale_973": "True when the scanner ran but the service did NOT answer — so a rule's     decla" | kind=entity | source=manager/detection_engine/posture_rules.py:L973 | neighbors=[_fact_indicates_no_service()] | lang=en
- "detection_engine_posture_rules_rationale_986": "Evaluate ONE rule against ONE fact and record the outcome. NEVER raises —     a" | kind=entity | source=manager/detection_engine/posture_rules.py:L986 | neighbors=[evaluate_rule()] | lang=en
- "detection_engine_posture_rules_tracerow_to_dict": ".to_dict()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L123 | neighbors=[TraceRow] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-223.json

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
