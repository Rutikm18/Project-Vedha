# Node Description Batch 145 of 380

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_engine_posture_rules_dns_zone_transfer": "_dns_zone_transfer()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L518 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_exposed_title": "_exposed_title()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L1139 | neighbors=[posture_rules.py, detect_exposed_services()]
- "detection_engine_posture_rules_ftp_anonymous": "_ftp_anonymous()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L509 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_group_key_for": "group_key_for()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L394 | neighbors=[posture_rules.py, A stable handle for collapsing identica…]
- "detection_engine_posture_rules_ipmi_cipher_zero": "_ipmi_cipher_zero()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L607 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_is_validated": "is_validated()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L58 | neighbors=[posture_rules.py, _state_for()]
- "detection_engine_posture_rules_ldap_anonymous_bind": "_ldap_anonymous_bind()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L538 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_msrpc_exposed": "_msrpc_exposed()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L369 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_nfs_world_readable": "_nfs_world_readable()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L530 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_rdp_auth": "_rdp_auth()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L323 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_rdp_exposed": "_rdp_exposed()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L315 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_rsync_anonymous": "_rsync_anonymous()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L588 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smb_null_session": "_smb_null_session()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L596 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smb_signing": "_smb_signing()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L252 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smbv1": "_smbv1()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L248 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smtp_no_starttls": "_smtp_no_starttls()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L580 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_smtp_user_enum": "_smtp_user_enum()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L568 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_snmp_default": "_snmp_default()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L389 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_ssh_terrapin": "_ssh_terrapin()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L490 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_ssh_weak_algos": "_ssh_weak_algos()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L498 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_tls_cipher": "_tls_cipher()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L351 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_tls_expired": "_tls_expired()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L364 | neighbors=[posture_rules.py, _cert()]
- "detection_engine_posture_rules_tls_self_signed": "_tls_self_signed()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L359 | neighbors=[posture_rules.py, _cert()]
- "detection_engine_posture_rules_tls_version": "_tls_version()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L337 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_udp_amplifier": "_udp_amplifier()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L377 | neighbors=[posture_rules.py, _d()]
- "detection_engine_posture_rules_vnc_no_auth": "_vnc_no_auth()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L547 | neighbors=[posture_rules.py, _d()]
- "detection_engine_update_snapshot_all_known_cve_ids": "_all_known_cve_ids()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L223 | neighbors=[update_snapshot.py, main()]
- "detection_engine_verifier_deception_score": "deception_score()" | kind=code-symbol | source=manager/detection_engine/verifier.py:L75 | neighbors=[verifier.py, A starter honeypot/deception heuristic …]
- "detection_engine_version_compare_clear_validation_cache": "_clear_validation_cache()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L219 | neighbors=[version_compare.py, Test hook: drop the in-memory record of…]
- "detection_engine_version_compare_split_segments": "_split_segments()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L84 | neighbors=[version_compare.py, _compare_part()]
- "detection_engine_vuln_db_vulndb_build_cve_index": "._build_cve_index()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L96 | neighbors=[VulnDB, .__init__()]
- "detection_engine_vuln_db_vulndb_init": ".__init__()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L90 | neighbors=[VulnDB, ._build_cve_index()]
- "detection_explain_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L11 | neighbors=[route.ts, GET()]
- "detection_explain_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-explain/route.ts:L16 | neighbors=[route.ts, fail()]
- "detection_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/detection/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "detection_logger_as_uuid": "_as_uuid()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L69 | neighbors=[logger.py, .log_action()]
- "detection_logger_rationale_1": "AttackLogger — records every attack action to the ``attack_timeline`` table.  Al" | kind=entity | source=manager/backend/app/detection/logger.py:L1 | neighbors=[logger.py, AttackTimeline]
- "detection_logger_rationale_40": "Persist a single attack action. Returns the AttackTimeline row.          ``times" | kind=entity | source=manager/backend/app/detection/logger.py:L40 | neighbors=[.log_action(), AttackTimeline]
- "detection_prioritization_posture_risk_on_manager_scale": "_posture_risk_on_manager_scale()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L57 | neighbors=[prioritization.py, Score a posture finding with the Manage…]
- "detection_resolution_resolutionoutcome": "ResolutionOutcome" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L75 | neighbors=[resolution.py, decide_resolution()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-144.json

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
