# Node Description Batch 55 of 92

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

- "main_scripts_findings_rationale_718": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=main_scripts/findings.py:L718 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_725": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=main_scripts/findings.py:L725 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_735": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=main_scripts/findings.py:L735 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_findings_rationale_740": "NFS anonymous export exposure. A world-readable export is the high-value     fin" | kind=entity | source=main_scripts/findings.py:L740 | neighbors=[_rule_nfs()] | lang=en
- "main_scripts_findings_rationale_748": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=main_scripts/findings.py:L748 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_753": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=main_scripts/findings.py:L753 | neighbors=[_rule_ftp()] | lang=en
- "main_scripts_findings_rationale_758": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=main_scripts/findings.py:L758 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_775": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=main_scripts/findings.py:L775 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_777": "Confirmed FTP anonymous access (upgrades the port-based cleartext hint).     Hig" | kind=entity | source=main_scripts/findings.py:L777 | neighbors=[_rule_ftp()] | lang=en
- "main_scripts_findings_rationale_782": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=main_scripts/findings.py:L782 | neighbors=[_rule_rsync()] | lang=en
- "main_scripts_findings_rationale_794": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=main_scripts/findings.py:L794 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_798": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=main_scripts/findings.py:L798 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_806": "rsync daemon exposure. Anonymously-selectable modules are the high finding     (" | kind=entity | source=main_scripts/findings.py:L806 | neighbors=[_rule_rsync()] | lang=en
- "main_scripts_findings_rationale_810": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=main_scripts/findings.py:L810 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_820": "VNC/RFB authentication exposure. 'None' security type = unauthenticated     remo" | kind=entity | source=main_scripts/findings.py:L820 | neighbors=[_rule_vnc()] | lang=en
- "main_scripts_findings_rationale_840": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=main_scripts/findings.py:L840 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_findings_rationale_851": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=main_scripts/findings.py:L851 | neighbors=[_rule_ipmi()] | lang=pt
- "main_scripts_findings_rationale_860": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=main_scripts/findings.py:L860 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_863": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=main_scripts/findings.py:L863 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_875": "IPMI/BMC exposure. Cipher-zero is a critical auth bypass; a merely reachable" | kind=entity | source=main_scripts/findings.py:L875 | neighbors=[_rule_ipmi()] | lang=pt
- "main_scripts_findings_rationale_880": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=main_scripts/findings.py:L880 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_883": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=main_scripts/findings.py:L883 | neighbors=[_rule_smtp()] | lang=en
- "main_scripts_findings_rationale_907": "SMTP hygiene: VRFY/EXPN user enumeration, and missing STARTTLS (cleartext)." | kind=entity | source=main_scripts/findings.py:L907 | neighbors=[_rule_smtp()] | lang=en
- "main_scripts_findings_rationale_917": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=main_scripts/findings.py:L917 | neighbors=[_rule_msrpc()] | lang=en
- "main_scripts_findings_rationale_926": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=main_scripts/findings.py:L926 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_941": "Windows RPC endpoint-mapper disclosure — the internal RPC service map." | kind=entity | source=main_scripts/findings.py:L941 | neighbors=[_rule_msrpc()] | lang=en
- "main_scripts_findings_rationale_943": "Two or more cleartext services on one host — any sniffing position harvests" | kind=entity | source=main_scripts/findings.py:L943 | neighbors=[_corr_cleartext_cluster()] | lang=en
- "main_scripts_findings_rationale_944": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=main_scripts/findings.py:L944 | neighbors=[_rule_printer()] | lang=en
- "main_scripts_findings_rationale_949": "Read a scanner's JSONL output into fact dicts (skips blank/garbage lines)." | kind=entity | source=main_scripts/findings.py:L949 | neighbors=[load_facts_jsonl()] | lang=pt
- "main_scripts_findings_rationale_964": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=main_scripts/findings.py:L964 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_findings_rationale_965": "CLI: derive findings from one or more scanner JSONL files.          python -m ma" | kind=entity | source=main_scripts/findings.py:L965 | neighbors=[_main()] | lang=en
- "main_scripts_findings_rationale_966": "Derive findings from collected facts. Pure; deterministic; safe.      Accepts Sc" | kind=entity | source=main_scripts/findings.py:L966 | neighbors=[run_findings()] | lang=en
- "main_scripts_findings_rationale_968": "Exposed network printer — an information leak and an attack surface." | kind=entity | source=main_scripts/findings.py:L968 | neighbors=[_rule_printer()] | lang=en
- "main_scripts_findings_rationale_98": "Accept a raw JSONL dict or a ScanResult; return a plain dict view." | kind=entity | source=main_scripts/findings.py:L98 | neighbors=[_as_dict()] | lang=pt
- "main_scripts_findings_rationale_987": "SMBv1 (wormable) + exposed RDP (brute-force/BlueKeep) on one host — the     clas" | kind=entity | source=main_scripts/findings.py:L987 | neighbors=[_corr_legacy_windows()] | lang=en
- "main_scripts_findings_rationale_990": "SMB signing not required => a viable NTLM relay target. If SMBv1 is also on," | kind=entity | source=main_scripts/findings.py:L990 | neighbors=[_corr_ntlm_relay()] | lang=en
- "main_scripts_host_discovery_hostdiscoveryscanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/host_discovery.py:L394 | neighbors=[HostDiscoveryScanner] | lang=en
- "main_scripts_host_discovery_main": "main()" | kind=code-symbol | source=main_scripts/host_discovery.py:L495 | neighbors=[host_discovery.py] | lang=en
- "main_scripts_iot_scanner_main": "main()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L559 | neighbors=[iot_scanner.py] | lang=en
- "main_scripts_ja4s_match_suspicious": "match_suspicious()" | kind=code-symbol | source=main_scripts/ja4s.py:L131 | neighbors=[ja4s.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-054.json

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
