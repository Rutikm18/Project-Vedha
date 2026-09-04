# Node Description Batch 225 of 332

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

- "main_scripts_smb_enum_scanner_rationale_149": "RID-cycling fallback via LSAT: resolve <DomainSID>-<rid> for each rid to a     n" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L149 | neighbors=[_enum_users_ridcycle()] | lang=en
- "main_scripts_smb_enum_scanner_rationale_201": "Merge user lists, de-duplicated by (name, rid); SAMR entries win over RID     cy" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L201 | neighbors=[_merge_users()] | lang=en
- "main_scripts_smb_enum_scanner_rationale_228": "Blocking: attempt a null session and enumerate what the server         volunteer" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L228 | neighbors=[._enumerate()] | lang=en
- "main_scripts_smb_enum_scanner_rationale_53": "Parse 'a-b,c-d,e' into a sorted, de-duplicated, bounded list of RIDs.      Bound" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L53 | neighbors=[parse_rid_ranges()] | lang=en
- "main_scripts_smb_enum_scanner_rationale_88": "List SMB shares over the null session. Read-only (share listing, no file     acc" | kind=entity | source=probe/main_scripts/smb_enum_scanner.py:L88 | neighbors=[_enum_shares()] | lang=en
- "main_scripts_smb_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L452 | neighbors=[smb_scanner.py] | lang=en
- "main_scripts_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[smb_scanner.py] | lang=en
- "main_scripts_smb_scanner_rationale_116": "NTLMSSP NEGOTIATE (Type-1). Sets NEGOTIATE_VERSION so the server discloses     i" | kind=entity | source=probe/main_scripts/smb_scanner.py:L116 | neighbors=[build_ntlmssp_negotiate()] | lang=en
- "main_scripts_smb_scanner_rationale_134": "Wrap an NTLMSSP Type-1 in a minimal SPNEGO NegTokenInit (GSS-API)." | kind=entity | source=probe/main_scripts/smb_scanner.py:L134 | neighbors=[_spnego_init()] | lang=en
- "main_scripts_smb_scanner_rationale_142": "Map an NT major.minor.build to a friendly release. Client and server share     s" | kind=entity | source=probe/main_scripts/smb_scanner.py:L142 | neighbors=[windows_release_from_build()] | lang=en
- "main_scripts_smb_scanner_rationale_177": "Parse an NTLMSSP CHALLENGE (Type-2) out of any containing buffer (SPNEGO or" | kind=entity | source=probe/main_scripts/smb_scanner.py:L177 | neighbors=[parse_ntlm_challenge()] | lang=en
- "main_scripts_smb_scanner_rationale_204": "SMB2 SESSION_SETUP request (MessageId 1, SessionId 0) carrying `security_blob`." | kind=entity | source=probe/main_scripts/smb_scanner.py:L204 | neighbors=[_smb2_session_setup()] | lang=en
- "main_scripts_smb_scanner_rationale_250": "Pad to the 8-byte boundary MS-SMB2 requires between negotiate contexts." | kind=entity | source=probe/main_scripts/smb_scanner.py:L250 | neighbors=[_align8()] | lang=en
- "main_scripts_smb_scanner_rationale_255": "SMB2_PREAUTH_INTEGRITY_CAPABILITIES (MS-SMB2 2.2.3.1.1): mandatory for any     c" | kind=entity | source=probe/main_scripts/smb_scanner.py:L255 | neighbors=[_preauth_integrity_context()] | lang=en
- "main_scripts_smb_scanner_rationale_266": "SMB2_ENCRYPTION_CAPABILITIES (MS-SMB2 2.2.3.1.2): offer AES-128-GCM/CCM so     t" | kind=entity | source=probe/main_scripts/smb_scanner.py:L266 | neighbors=[_encryption_context()] | lang=en
- "main_scripts_smb_scanner_rationale_317": "Read one length-prefixed (Direct-TCP/NBT) SMB frame in full, STRIPPING the     4" | kind=entity | source=probe/main_scripts/smb_scanner.py:L317 | neighbors=[_recv_smb_frame()] | lang=en
- "main_scripts_smb_scanner_rationale_338": "Pre-auth SMB2 NEGOTIATE → SESSION_SETUP → parse the NTLMSSP CHALLENGE Version" | kind=entity | source=probe/main_scripts/smb_scanner.py:L338 | neighbors=[ntlm_os_build()] | lang=en
- "main_scripts_smb_scanner_rationale_37": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=probe/main_scripts/smb_scanner.py:L37 | neighbors=[parse_smb2_security_mode()] | lang=en
- "main_scripts_smb_scanner_rationale_370": "SMB negotiate against the first address that actually answers.          Walks ev" | kind=entity | source=probe/main_scripts/smb_scanner.py:L370 | neighbors=[._negotiate()] | lang=en
- "main_scripts_smb_scanner_rationale_39": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=probe/main_scripts/smb_scanner.py:L39 | neighbors=[parse_smb2_security_mode()] | lang=en
- "main_scripts_smb_scanner_rationale_394": "Best-effort: SMB2 NEGOTIATE then a pre-auth SESSION_SETUP to harvest the" | kind=entity | source=probe/main_scripts/smb_scanner.py:L394 | neighbors=[._ntlm_fingerprint()] | lang=en
- "main_scripts_smb_scanner_smbscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L365 | neighbors=[SMBScanner] | lang=en
- "main_scripts_smtp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L147 | neighbors=[smtp_scanner.py] | lang=en
- "main_scripts_smtp_scanner_rationale_1": "smtp_scanner.py — SMTP hygiene: user enumeration + transport encryption (VA chec" | kind=entity | source=probe/main_scripts/smtp_scanner.py:L1 | neighbors=[smtp_scanner.py] | lang=en
- "main_scripts_smtp_scanner_rationale_40": "Extract EHLO capability tokens from a multi-line 250 response." | kind=entity | source=probe/main_scripts/smtp_scanner.py:L40 | neighbors=[parse_ehlo_capabilities()] | lang=en
- "main_scripts_smtp_scanner_rationale_52": "VRFY leaks usernames when it gives DIFFERENT definitive answers for an     exist" | kind=entity | source=probe/main_scripts/smtp_scanner.py:L52 | neighbors=[vrfy_leaks()] | lang=en
- "main_scripts_smtp_scanner_rationale_88": "Blocking: greeting → EHLO → STARTTLS/VRFY/EXPN checks. Monkeypatchable." | kind=entity | source=probe/main_scripts/smtp_scanner.py:L88 | neighbors=[._probe()] | lang=en
- "main_scripts_smtp_scanner_smtpscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L63 | neighbors=[SMTPScanner] | lang=en
- "main_scripts_snmp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L401 | neighbors=[snmp_scanner.py] | lang=en
- "main_scripts_snmp_scanner_rationale_1": "snmp_scanner.py — full SNMP enumeration: community discovery, targeted MIB walk," | kind=entity | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[snmp_scanner.py] | lang=en
- "main_scripts_snmp_scanner_rationale_105": "Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L105 | neighbors=[_ber_parse()] | lang=en
- "main_scripts_snmp_scanner_rationale_127": "Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response" | kind=entity | source=probe/main_scripts/snmp_scanner.py:L127 | neighbors=[_parse_varbinds()] | lang=en
- "main_scripts_snmp_scanner_rationale_246": "Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +     Phase 3 (ampli" | kind=entity | source=probe/main_scripts/snmp_scanner.py:L246 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_snmp_scanner_rationale_278": "Return (community, sysdescr) for the first responding community, or None." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L278 | neighbors=[._discover_community()] | lang=en
- "main_scripts_snmp_scanner_rationale_292": "GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L292 | neighbors=[._walk_subtree()] | lang=en
- "main_scripts_snmp_scanner_rationale_315": "One GETBULK request — measure response/request size ratio." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L315 | neighbors=[._amplification_factor()] | lang=en
- "main_scripts_snmp_scanner_rationale_325": "Send a SNMPv3 Discover. Any reply = v3 agent present." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L325 | neighbors=[._snmpv3_present()] | lang=pt
- "main_scripts_snmp_scanner_rationale_46": "Dotted-notation OID string → BER-encoded bytes." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L46 | neighbors=[_encode_oid()] | lang=en
- "main_scripts_snmp_scanner_rationale_64": "BER-encoded OID bytes → dotted-notation string." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L64 | neighbors=[_decode_oid()] | lang=en
- "main_scripts_snmp_scanner_rationale_79": "Human-readable SNMP value for common ASN.1/SNMP types." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L79 | neighbors=[_decode_value()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-224.json

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
