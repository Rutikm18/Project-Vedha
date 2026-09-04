# Node Description Batch 224 of 330

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
- "main_scripts_snmp_scanner_snmpscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L252 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L329 | neighbors=[SNMPScanner] | lang=en
- "main_scripts_ssh_collector_collect_over_ssh": "_collect_over_ssh()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L52 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_main": "main()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L125 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_rationale_1": "ssh_collector.py — credentialed (authenticated) inventory collection for Linux." | kind=entity | source=probe/main_scripts/ssh_collector.py:L1 | neighbors=[ssh_collector.py] | lang=en
- "main_scripts_ssh_collector_sshcollector_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L83 | neighbors=[SSHCollector] | lang=en
- "main_scripts_ssh_kexdb_rationale_1": "ssh_kexdb.py — vendored SSH algorithm weakness database (the \"content\" half of t" | kind=entity | source=probe/main_scripts/ssh_kexdb.py:L1 | neighbors=[ssh_kexdb.py] | lang=en
- "main_scripts_ssh_kexdb_rationale_478": "Return (failures, warnings, infos) for one offered algorithm, or None if     the" | kind=entity | source=probe/main_scripts/ssh_kexdb.py:L478 | neighbors=[lookup()] | lang=en
- "main_scripts_ssh_scanner_cursor_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L73 | neighbors=[_Cursor] | lang=en
- "main_scripts_ssh_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L336 | neighbors=[ssh_scanner.py] | lang=en
- "main_scripts_ssh_scanner_rationale_1": "ssh_scanner.py — SSH configuration / algorithm audit (VA checklist §6).  METHOD" | kind=entity | source=probe/main_scripts/ssh_scanner.py:L1 | neighbors=[ssh_scanner.py] | lang=en
- "main_scripts_ssh_scanner_rationale_107": "Parse a SSH_MSG_KEXINIT body into its name-lists.      Accepts the payload with" | kind=entity | source=probe/main_scripts/ssh_scanner.py:L107 | neighbors=[parse_kexinit()] | lang=en
- "main_scripts_ssh_scanner_rationale_134": "Grade a server's offered algorithms against the vendored weakness table.      Re" | kind=entity | source=probe/main_scripts/ssh_scanner.py:L134 | neighbors=[evaluate_algorithms()] | lang=en
- "main_scripts_ssh_scanner_rationale_196": "Read the server SSH identification line, skipping any pre-banner text     lines" | kind=entity | source=probe/main_scripts/ssh_scanner.py:L196 | neighbors=[_read_ident()] | lang=en
- "main_scripts_ssh_scanner_rationale_226": "Read one unencrypted SSH binary packet and return its payload (RFC 4253     §6)." | kind=entity | source=probe/main_scripts/ssh_scanner.py:L226 | neighbors=[_read_packet()] | lang=en
- "main_scripts_ssh_scanner_rationale_250": "Blocking: connect, exchange identification, read the server KEXINIT.         Ret" | kind=entity | source=probe/main_scripts/ssh_scanner.py:L250 | neighbors=[._probe()] | lang=en

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
