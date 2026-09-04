# Node Description Batch 128 of 332

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_engine_models_fact_ref": ".ref()" | kind=code-symbol | source=manager/detection_engine/models.py:L60 | neighbors=[Fact, A stable, human-readable pointer back t…]
- "detection_engine_models_make_finding_id": "make_finding_id()" | kind=code-symbol | source=manager/detection_engine/models.py:L125 | neighbors=[models.py, Deterministic finding ID: the SAME (ass…]
- "detection_engine_port_intel_banner_confirms_backdoor": "_banner_confirms_backdoor()" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L156 | neighbors=[port_intel.py, classify_port()]
- "detection_engine_port_intel_normalized": "_normalized()" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L197 | neighbors=[port_intel.py, contradicts_port_hypothesis()]
- "detection_engine_port_intel_portrisk": "PortRisk" | kind=code-symbol | source=manager/detection_engine/port_intel.py:L34 | neighbors=[port_intel.py, classify_port()]
- "detection_engine_posture_rules_dns_zone_transfer": "_dns_zone_transfer()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L428 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_exposed_title": "_exposed_title()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L934 | neighbors=[posture_rules.py, detect_exposed_services()]
- "detection_engine_posture_rules_ftp_anonymous": "_ftp_anonymous()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L419 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_ipmi_cipher_zero": "_ipmi_cipher_zero()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L517 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_is_validated": "is_validated()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L56 | neighbors=[posture_rules.py, _state_for()]
- "detection_engine_posture_rules_ldap_anonymous_bind": "_ldap_anonymous_bind()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L448 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_msrpc_exposed": "_msrpc_exposed()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L367 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_nfs_world_readable": "_nfs_world_readable()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L440 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_rdp_auth": "_rdp_auth()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L321 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_rdp_exposed": "_rdp_exposed()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L313 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_rsync_anonymous": "_rsync_anonymous()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L498 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smb_null_session": "_smb_null_session()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L506 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smb_signing": "_smb_signing()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L250 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smbv1": "_smbv1()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L246 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smtp_no_starttls": "_smtp_no_starttls()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L490 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smtp_user_enum": "_smtp_user_enum()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L478 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_snmp_default": "_snmp_default()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L387 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_ssh_terrapin": "_ssh_terrapin()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L400 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_ssh_weak_algos": "_ssh_weak_algos()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L408 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_summarize_traces": "summarize_traces()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1046 | neighbors=[posture_rules.py, Engagement-level coverage roll-up over …]
- "detection_engine_posture_rules_tls_cipher": "_tls_cipher()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L349 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_tls_expired": "_tls_expired()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L362 | neighbors=[posture_rules.py, _cert()]
- "detection_engine_posture_rules_tls_self_signed": "_tls_self_signed()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L357 | neighbors=[posture_rules.py, _cert()]
- "detection_engine_posture_rules_tls_version": "_tls_version()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L335 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_udp_amplifier": "_udp_amplifier()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L375 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_verdict_for_rule": "verdict_for_rule()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1028 | neighbors=[posture_rules.py, Collapse every trace for one rule into …]
- "detection_engine_posture_rules_vnc_no_auth": "_vnc_no_auth()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L457 | neighbors=[posture_rules.py, _d()]
- "detection_engine_update_snapshot_all_known_cve_ids": "_all_known_cve_ids()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L223 | neighbors=[update_snapshot.py, main()]
- "detection_engine_verifier_deception_score": "deception_score()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L75 | neighbors=[verifier.py, A starter honeypot/deception heuristic …]
- "detection_engine_version_compare_clear_validation_cache": "_clear_validation_cache()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L219 | neighbors=[version_compare.py, Test hook: drop the in-memory record of…]
- "detection_engine_version_compare_split_segments": "_split_segments()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L84 | neighbors=[version_compare.py, _compare_part()]
- "detection_engine_vuln_db_vulndb_build_cve_index": "._build_cve_index()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L96 | neighbors=[VulnDB, .__init__()]
- "detection_engine_vuln_db_vulndb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L90 | neighbors=[VulnDB, ._build_cve_index()]
- "detection_explain_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L11 | neighbors=[route.ts, GET()]
- "detection_explain_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L16 | neighbors=[route.ts, fail()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-127.json

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
