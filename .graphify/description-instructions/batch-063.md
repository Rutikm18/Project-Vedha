# Node Description Batch 64 of 131

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

- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L30 | neighbors=[snmp_scanner.py, ._query()]
- "scanner_snmp_scanner_extract_sysdescr": "_extract_sysdescr()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L44 | neighbors=[snmp_scanner.py, .scan_target()]
- "scanner_snmp_scanner_snmpscanner_query": "._query()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L84 | neighbors=[SNMPScanner, _build_get()]
- "scanner_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L100 | neighbors=[SNMPScanner, _extract_sysdescr()]
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]
- "scanner_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L95 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "scanner_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L162 | neighbors=[TLSScanner, .scan_target()]
- "scanner_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L180 | neighbors=[TLSScanner, ._scan_port()]
- "scanner_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L88 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L99 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L83 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L72 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L173 | neighbors=[UDPScanner, ._probe()]
- "scanner_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L77 | neighbors=[web_scanner.py, parse_allow_header()]
- "scanner_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/web_scanner.py:L54 | neighbors=[web_scanner.py, .redirect_request()]
- "scanner_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L142 | neighbors=[WebScanner, .scan_target()]
- "scanner_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L159 | neighbors=[WebScanner, ._scan_port()]
- "scanner_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "scanner_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "schemas_ai_aigenerateresponse": "AiGenerateResponse" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L56 | neighbors=[ai.py, BaseModel]
- "schemas_ai_aimessage": "AiMessage" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L13 | neighbors=[ai.py, BaseModel]
- "schemas_auth_loginrequest": "LoginRequest" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L9 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreate": "PersonalAccessTokenCreate" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L32 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokencreated": "PersonalAccessTokenCreated" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L38 | neighbors=[auth.py, BaseModel]
- "schemas_auth_personalaccesstokenout": "PersonalAccessTokenOut" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L49 | neighbors=[auth.py, BaseModel]
- "schemas_auth_tokenresponse": "TokenResponse" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L14 | neighbors=[auth.py, BaseModel]
- "schemas_common_errordetail": "ErrorDetail" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L18 | neighbors=[common.py, BaseModel]
- "schemas_common_paginate": "paginate()" | kind=code-symbol | source=manager/backend/app/schemas/common.py:L22 | neighbors=[common.py, PaginatedResponse]
- "schemas_engagement_engagementcreate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L66 | neighbors=[EngagementCreate, validate_engagement_dates()]
- "schemas_engagement_engagementcreate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L62 | neighbors=[EngagementCreate, validate_scope_entries()]
- "schemas_engagement_rationale_13": "Validate and de-duplicate exact IP/CIDR authorization boundaries." | kind=entity | source=manager/backend/app/schemas/engagement.py:L13 | neighbors=[validate_scope_entries(), EngagementStatus]
- "schemas_engagement_validate_engagement_dates": "validate_engagement_dates()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L30 | neighbors=[engagement.py, .validate_dates()]
- "schemas_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/schemas/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "scripts_seed_admin_hash": "_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L135 | neighbors=[seed_admin.py, _seed_once()]
- "scripts_seed_admin_verify_hash": "_verify_hash()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L139 | neighbors=[seed_admin.py, _seed_once()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-063.json

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
