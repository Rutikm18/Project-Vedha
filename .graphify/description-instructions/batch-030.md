# Node Description Batch 31 of 330

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

- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …]
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings, AiRuntimeError]
- "assistant_modelswitcher": "ModelSwitcher.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L1 | neighbors=[AssistantDrawer.tsx, AiStatus, ModelSelection, ModelSwitcher(), ProviderStatus, readStored()]
- "auth_exceptions_vedhaautherror": "VedhaAuthError" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L15 | neighbors=[exceptions.py, AuthenticationError, DatabaseUnavailableError, PasswordRotationError, Base for all Vedha auth exceptions., SeedConfigurationError]
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…]
- "cli_auth_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L46 | neighbors=[auth.ts, serverUrl(), admin.ts, engagement.ts, interactive.ts, report.ts]
- "cli_llm_client": "client()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L10 | neighbors=[llm.ts, commentOnStage(), explainFindings(), planExploit(), recommendNextPhase(), streamAsk()]
- "commands_interactive_picktargets": "pickTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L226 | neighbors=[interactive.ts, ask(), choose(), confirm(), detectLocalSubnet(), inferHostsFromFindings()]
- "commands_interactive_wizardengagement": "wizardEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1769 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), divider(), fetchEngagements()]
- "commands_interactive_wizardreport": "wizardReport()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1847 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardvalidate": "wizardValidate()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1465 | neighbors=[interactive.ts, mainMenu(), runValidationFlow(), ask(), choose(), confirm()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@185e6487d540cf5b1805c4d2a41a6ca0e9bd42c0": "185e648 docs: pending-work inventory (buckets A-G)" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, ui-ux-backend-updates0109]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2be040ca5c7a29aa1dd6caa2bfefb6f305d23693": "2be040c improve(probe/install): portability, supply-chain, ops hardening" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, ui-ux-backend-updates0109]
- "commit:repo:github.com/Rutikm18/Project-Vedha@5b980e1cf0c571409a6d765442112df458b0456f": "5b980e1 docs(spec): installer warning + fleet job visibility + engagement host-…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, ui-ux-backend-updates0109]
- "commit:repo:github.com/Rutikm18/Project-Vedha@9e188b89006db238b7f9a09dd1b17eb4eba7ad87": "9e188b8 fix(probe/install): LOCAL preflight + self-healing venv + daemon/lock g…" | kind=Commit | source=git | neighbors=[22e4f8d chore: update version, addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), Protocol, CPECandidate, Fact, pipeline.py — Phase 1 + Phase 2 end to …]
- "detection_engine_bridge_detect_findings_from_facts": "detect_findings_from_facts()" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L257 | neighbors=[engine_bridge.py, detect_all_from_facts_traced(), CVE finding dicts only — backward-compa…, create_findings_from_facts(), _ensure_importable(), facts (ScanResult dicts) -> detection_e…]
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()]
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()]
- "detection_verification": "verification.py" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, de2d1c9 feat(verification): optional fa…, compute_verdict(), _int_confidence(), _qualifies_for_llm(), VerificationVerdict]
- "discovery_finding_translator_create_findings_from_probe_result": "create_findings_from_probe_result()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L152 | neighbors=[finding_translator.py, _escalate_by_exposure(), _find_open_duplicate(), _map_severity(), _resolve_asset(), Convert a probe's self-assessed `findin…]
- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L24 | neighbors=[xml_parser.py, ._parse_host(), .open_ports(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …]
- "enum": "Enum" | kind=code-symbol | neighbors=[models.py, FindingState, SourceConfidence, verifier.py, agent.py, enums.py]
- "frontend_proxy": "proxy.ts" | kind=code-symbol | source=manager/frontend/proxy.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, config, isPublic(), proxy(), PUBLIC_PATHS, PUBLIC_PREFIXES]
- "jobs_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/route.ts:L1 | neighbors=[25c014d feat: enhance campaign progress…, b393dbe feat: Enhance Sidebar UI and in…, f3bb8db feat(manager): cross-worker WS …, GET, backend.ts, backend()]
- "lib_assistant_access": "assistant-access.ts" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L1 | neighbors=[AssistantProvider.tsx, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, AssistantAuthState, canMountAssistant()]
- "lib_console_source_useconsolequery": "useConsoleQuery()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L165 | neighbors=[DashboardCharts.tsx, DashboardGrid.tsx, ExposureCards.tsx, LiveOverview.tsx, PostureScorecard.tsx, SlaStatus.tsx]
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()]
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, proxy.ts, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost()]
- "main_scripts_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L162 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()]
- "main_scripts_nfs_scanner_xdr": "_XDR" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L56 | neighbors=[nfs_scanner.py, parse_mount_export(), parse_portmap_dump(), Minimal, BOUNDED big-endian XDR reader …, .__init__(), .opaque()]
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_echo_ttl": "._icmp_echo_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L405 | neighbors=[OSFingerprintScanner, accept_echo_reply(), build_icmp_echo(), _open_icmp_socket(), parse_icmp_reply(), Send one ICMP echo; return observed TTL…]
- "main_scripts_printer_scanner_printerscanner": "PrinterScanner" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L96 | neighbors=[printer_scanner.py, BaseScanner, .__init__(), ._probe(), ._probe_ipp(), ._probe_pjl()]
- "main_scripts_rsync_scanner": "rsync_scanner.py" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _handshake(), main(), parse_modules(), _recv_until()]
- "main_scripts_rsync_scanner_rsyncscanner": "RsyncScanner" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L93 | neighbors=[rsync_scanner.py, BaseScanner, .__init__(), ._list_modules(), ._probe(), ._scan_port()]
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L129 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "main_scripts_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L946 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "main_scripts_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L916 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "main_scripts_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L366 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), ._connect(), ._read_some(), One probe-ladder rung on its own connec…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-030.json

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
