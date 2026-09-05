# Node Description Batch 228 of 336

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

- "main_scripts_service_enum_rationale_245": "Run the three name sources concurrently off the event loop." | kind=entity | source=probe/main_scripts/service_enum.py:L245 | neighbors=[resolve_hostnames()]
- "main_scripts_service_enum_rationale_259": "Which deprecated TLS/SSL versions the server still accepts (weak-config)." | kind=entity | source=probe/main_scripts/service_enum.py:L259 | neighbors=[tls_accepts_old()]
- "main_scripts_service_enum_rationale_265": "One permissive TLS handshake: negotiated version + cert subject/issuer." | kind=entity | source=probe/main_scripts/service_enum.py:L265 | neighbors=[tls_info()]
- "main_scripts_service_enum_rationale_288": "Which deprecated TLS/SSL versions the server still accepts (weak-config)." | kind=entity | source=probe/main_scripts/service_enum.py:L288 | neighbors=[tls_accepts_old()]
- "main_scripts_service_enum_rationale_294": "Negotiate against 445; report whether SMBv1 is offered (defensive flag)." | kind=entity | source=probe/main_scripts/service_enum.py:L294 | neighbors=[smb_dialects()]
- "main_scripts_service_enum_rationale_313": "Best-effort OS guess from voluntary evidence. Returns (label, confidence)." | kind=entity | source=probe/main_scripts/service_enum.py:L313 | neighbors=[guess_os()]
- "main_scripts_service_enum_rationale_323": "Negotiate against 445; report whether SMBv1 is offered (defensive flag)." | kind=entity | source=probe/main_scripts/service_enum.py:L323 | neighbors=[smb_dialects()]
- "main_scripts_service_enum_rationale_342": "Best-effort OS guess from voluntary evidence. Returns (label, confidence)." | kind=entity | source=probe/main_scripts/service_enum.py:L342 | neighbors=[guess_os()]
- "main_scripts_service_enum_rationale_361": "Descriptive role tags from the open-port signature." | kind=entity | source=probe/main_scripts/service_enum.py:L361 | neighbors=[classify_roles()]
- "main_scripts_service_enum_rationale_390": "Descriptive role tags from the open-port signature." | kind=entity | source=probe/main_scripts/service_enum.py:L390 | neighbors=[classify_roles()]
- "main_scripts_service_enum_rationale_396": "Directly-connected subnets and default gateway(s) from the OS route table." | kind=entity | source=probe/main_scripts/service_enum.py:L396 | neighbors=[local_topology()]
- "main_scripts_service_enum_rationale_425": "Directly-connected subnets and default gateway(s) from the OS route table." | kind=entity | source=probe/main_scripts/service_enum.py:L425 | neighbors=[local_topology()]
- "main_scripts_service_enum_rationale_466": "Connect to one port and read whatever it voluntarily advertises." | kind=entity | source=probe/main_scripts/service_enum.py:L466 | neighbors=[._probe_port()]
- "main_scripts_service_enum_rationale_495": "Connect to one port and read whatever it voluntarily advertises." | kind=entity | source=probe/main_scripts/service_enum.py:L495 | neighbors=[._probe_port()]
- "main_scripts_service_enum_reverse_dns": "reverse_dns()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L148 | neighbors=[service_enum.py]
- "main_scripts_service_enum_serviceenumscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L481 | neighbors=[ServiceEnumScanner]
- "main_scripts_smb_enum_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L307 | neighbors=[smb_enum_scanner.py]
- "main_scripts_smb_enum_scanner_rationale_1": "smb_enum_scanner.py — SMB null-session enumeration (VA checklist: anonymous info" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L1 | neighbors=[smb_enum_scanner.py]
- "main_scripts_smb_enum_scanner_rationale_103": "Enumerate domain/local users via the SAMR named pipe, reusing the null     sessi" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L103 | neighbors=[_enum_users_samr()]
- "main_scripts_smb_enum_scanner_rationale_149": "RID-cycling fallback via LSAT: resolve <DomainSID>-<rid> for each rid to a     n" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L149 | neighbors=[_enum_users_ridcycle()]
- "main_scripts_smb_enum_scanner_rationale_201": "Merge user lists, de-duplicated by (name, rid); SAMR entries win over RID     cy" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L201 | neighbors=[_merge_users()]
- "main_scripts_smb_enum_scanner_rationale_228": "Blocking: attempt a null session and enumerate what the server         volunteer" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L228 | neighbors=[._enumerate()]
- "main_scripts_smb_enum_scanner_rationale_53": "Parse 'a-b,c-d,e' into a sorted, de-duplicated, bounded list of RIDs.      Bound" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L53 | neighbors=[parse_rid_ranges()]
- "main_scripts_smb_enum_scanner_rationale_88": "List SMB shares over the null session. Read-only (share listing, no file     acc" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L88 | neighbors=[_enum_shares()]
- "main_scripts_smb_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L452 | neighbors=[smb_scanner.py]
- "main_scripts_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[smb_scanner.py]
- "main_scripts_smb_scanner_rationale_116": "NTLMSSP NEGOTIATE (Type-1). Sets NEGOTIATE_VERSION so the server discloses     i" | kind=entity | source=probe/main_scripts/smb_scanner.py:L116 | neighbors=[build_ntlmssp_negotiate()]
- "main_scripts_smb_scanner_rationale_134": "Wrap an NTLMSSP Type-1 in a minimal SPNEGO NegTokenInit (GSS-API)." | kind=entity | source=probe/main_scripts/smb_scanner.py:L134 | neighbors=[_spnego_init()]
- "main_scripts_smb_scanner_rationale_142": "Map an NT major.minor.build to a friendly release. Client and server share     s" | kind=entity | source=probe/main_scripts/smb_scanner.py:L142 | neighbors=[windows_release_from_build()]
- "main_scripts_smb_scanner_rationale_177": "Parse an NTLMSSP CHALLENGE (Type-2) out of any containing buffer (SPNEGO or" | kind=entity | source=probe/main_scripts/smb_scanner.py:L177 | neighbors=[parse_ntlm_challenge()]
- "main_scripts_smb_scanner_rationale_204": "SMB2 SESSION_SETUP request (MessageId 1, SessionId 0) carrying `security_blob`." | kind=entity | source=probe/main_scripts/smb_scanner.py:L204 | neighbors=[_smb2_session_setup()]
- "main_scripts_smb_scanner_rationale_250": "Pad to the 8-byte boundary MS-SMB2 requires between negotiate contexts." | kind=entity | source=probe/main_scripts/smb_scanner.py:L250 | neighbors=[_align8()]
- "main_scripts_smb_scanner_rationale_255": "SMB2_PREAUTH_INTEGRITY_CAPABILITIES (MS-SMB2 2.2.3.1.1): mandatory for any     c" | kind=entity | source=probe/main_scripts/smb_scanner.py:L255 | neighbors=[_preauth_integrity_context()]
- "main_scripts_smb_scanner_rationale_266": "SMB2_ENCRYPTION_CAPABILITIES (MS-SMB2 2.2.3.1.2): offer AES-128-GCM/CCM so     t" | kind=entity | source=probe/main_scripts/smb_scanner.py:L266 | neighbors=[_encryption_context()]
- "main_scripts_smb_scanner_rationale_317": "Read one length-prefixed (Direct-TCP/NBT) SMB frame in full, STRIPPING the     4" | kind=entity | source=probe/main_scripts/smb_scanner.py:L317 | neighbors=[_recv_smb_frame()]
- "main_scripts_smb_scanner_rationale_338": "Pre-auth SMB2 NEGOTIATE → SESSION_SETUP → parse the NTLMSSP CHALLENGE Version" | kind=entity | source=probe/main_scripts/smb_scanner.py:L338 | neighbors=[ntlm_os_build()]
- "main_scripts_smb_scanner_rationale_37": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=probe/main_scripts/smb_scanner.py:L37 | neighbors=[parse_smb2_security_mode()]
- "main_scripts_smb_scanner_rationale_370": "SMB negotiate against the first address that actually answers.          Walks ev" | kind=entity | source=probe/main_scripts/smb_scanner.py:L370 | neighbors=[._negotiate()]
- "main_scripts_smb_scanner_rationale_39": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=probe/main_scripts/smb_scanner.py:L39 | neighbors=[parse_smb2_security_mode()]
- "main_scripts_smb_scanner_rationale_394": "Best-effort: SMB2 NEGOTIATE then a pre-auth SESSION_SETUP to harvest the" | kind=entity | source=probe/main_scripts/smb_scanner.py:L394 | neighbors=[._ntlm_fingerprint()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-227.json

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
