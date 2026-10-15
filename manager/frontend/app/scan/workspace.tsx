"use client";

import React, { useState, useEffect, useCallback, useMemo, useRef } from "react";
import {
  Play, RefreshCw, CheckCircle2, Clock, XCircle, Loader,
  Cpu, RotateCcw, ShieldAlert, Send, ChevronDown, Radar, ScanLine, SlidersHorizontal, Link2,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { PortalShell } from "../../components/portal/PortalShell";
import { useToast } from "../../hooks/useToast";
import { createScannerWorkspaceApi, type ScannerWorkspaceSurface } from "../../lib/scanner-workspace-api";
import { DEEP_SCAN_UC, buildDeepScanLaunch, type ScanLaunchBody } from "../../lib/scan-launch";
import { ScannerFleetStrip, NetworkVaHero } from "../../components/scan/ScannerContext";
import { ScanIntensityControl } from "../../components/scan/ScanIntensityControl";
import { scanIpAllowed, type ScanAssetOption } from "../../lib/scan-target";
import "./scanner-workspace.css";
import { INTENSITY, type Intensity } from "../../lib/scan-intensity";
import { launchableModes, modeShort } from "../../lib/entitlements";
import { DeepScanCard } from "../../components/portal/DeepScanCard";
import { useQueryClient } from "@tanstack/react-query";
import { usePortalEntitlement } from "../../lib/portal-client";
import CampaignProgress from "../campaign/[id]/CampaignProgress";

/* ══════════════════════════════════════════════════════
   TYPES
══════════════════════════════════════════════════════ */

interface UseCase {
  use_case_id: string;
  display_name: string;
  description: string;
  scan_type: string;
  profile: "it" | "iot" | "ot";
  expected_runtime_hint: string;
  status?: "available" | "coming_soon";
}

interface Probe {
  id: string;
  name: string;
  location: string | null;
  status: string;
  capabilities: string[];
  network_segments: string[];
  last_heartbeat: string | null;
  current_job_id: string | null;
  online: boolean;
}

interface Engagement {
  id: string;
  name: string;
  status: string;
  scopeCidrs?: string[];
  excludedCidrs?: string[];
}

interface JobStatus {
  job_id: string;
  engagement_id: string;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  created_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  agent_id: string | null;
  agent_name: string | null;
  use_case_id: string | null;
  result: Record<string, unknown> | null;
}

interface ScannerRun {
  id: string;
  label?: string;
  role?: string;
  status: "completed" | "cached" | "skipped" | "degraded" | "failed";
  attempted_targets?: number;
  fact_count?: number;
  error_count?: number;
  reused_fact_count?: number;
  skip_reason?: string;
}

interface EngineManifest {
  orchestrator?: {
    id?: string;
    label?: string;
    version?: string;
    build_sha?: string;
  };
  external_engines?: Array<{
    id: string;
    label?: string;
    available?: boolean;
    execution?: string;
    role?: string;
  }>;
}

/* ══════════════════════════════════════════════════════
   METADATA
══════════════════════════════════════════════════════ */

const NETWORK_VA_ID = "uc_network_va";
// Product decision: the Scanner surface currently exposes only the complete
// Network VA workflow. The catalog and Manager capabilities remain intact so
// specialized use cases can be enabled later without a backend migration.
const NETWORK_VA_FALLBACK: UseCase = {
  use_case_id: NETWORK_VA_ID,
  display_name: "Network Vulnerability Assessment",
  description: "Discover assets, assess exposed services, correlate evidence, and prioritize remediation in one traceable campaign.",
  scan_type: "network_va",
  profile: "it",
  expected_runtime_hint: "30–90 min per /24",
  status: "available",
};

const SectionLabel = ({ children }: { children: React.ReactNode }) => <h2 className="scanner-section-heading">{children}</h2>;

const REC_ST: Record<string, { color: string; label: string }> = {
  pending:   { color: "var(--text-muted)",         label: "Queued"    },
  running:   { color: "var(--accent)",             label: "Running"   },
  completed: { color: "var(--nominal-color)",      label: "Completed" },
  failed:    { color: "var(--text-secondary)", label: "Failed" },
  cancelled: { color: "var(--text-muted)", label: "Cancelled" },
};

function JobPanel({ job, ucName }: { job: JobStatus; ucName?: string }) {
  const r = job.result ?? {};
  const scannerRuns = Array.isArray(r.scanner_runs)
    ? (r.scanner_runs as ScannerRun[]).filter((run) => run && typeof run.id === "string")
    : [];
  const manifest = (
    r.engine_manifest && typeof r.engine_manifest === "object"
      ? r.engine_manifest
      : {}
  ) as EngineManifest;
  const orchestrator = manifest.orchestrator;
  const externalEngines = Array.isArray(manifest.external_engines)
    ? manifest.external_engines
    : [];
  const issues = Array.isArray(r.issues)
    ? (r.issues as Array<{ message?: string; remediation?: string }>).filter(Boolean)
    : [];
  const degraded = r.degraded === true || r.outcome === "partial";
  const elapsed = job.started_at && job.completed_at
    ? Math.round((new Date(job.completed_at).getTime() - new Date(job.started_at).getTime()) / 1000)
    : null;

  const ST: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
    pending:   { icon: <Clock size={13} />, color: "var(--text-muted)",        label: "Queued"    },
    running:   { icon: <Loader size={13} className="scn-spin" />, color: "var(--accent)", label: "Running" },
    completed: degraded
      ? { icon: <ShieldAlert size={13} />, color: "var(--sev-medium-color)", label: "Completed with errors" }
      : { icon: <CheckCircle2 size={13} />, color: "var(--nominal-color)", label: "Completed" },
    failed:    { icon: <XCircle size={13} />, color: "var(--text-secondary)", label: "Failed" },
    cancelled: { icon: <XCircle size={13} />, color: "var(--text-muted)", label: "Cancelled" },
  };
  const s = ST[job.status] ?? ST.pending;


  return (
    <div style={{ borderRadius: 12, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", overflow: "hidden", boxShadow: "var(--shadow-md)" }}>
      <div style={{ padding: "13px 16px", display: "flex", alignItems: "center", gap: 11, background: `color-mix(in srgb, ${s.color} 7%, transparent)`, borderBottom: "0.5px solid var(--border-subtle)" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 7, color: s.color, fontWeight: 700, fontSize: 12.5 }}>
          {s.icon} {s.label}
        </span>
        {ucName && <span style={{ fontSize: 12.5, color: "var(--text-secondary)", fontWeight: 500 }}>{ucName}</span>}
        {elapsed !== null && <span style={{ marginLeft: "auto", fontSize: 11.5, color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>{elapsed}s</span>}
      </div>

      {(job.status === "completed" || (job.status === "failed" && scannerRuns.length > 0)) && (
        <div className="scn-result-stats" style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)" }}>
          {([
            ["Hosts",      (r.host_count    ?? (r.run_stats as Record<string, unknown>)?.host_count    ?? "—")],
            ["Open Ports", (r.open_ports    ?? (r.run_stats as Record<string, unknown>)?.open_ports    ?? "—")],
            ["Facts",      (r.fact_count    ?? (r.run_stats as Record<string, unknown>)?.fact_count    ?? "—")],
            ["Findings",   (r.finding_count ?? "—")],
          ] as [string, unknown][]).map(([label, val], i) => (
            <div key={label} style={{ padding: "16px 12px", textAlign: "center", borderRight: i < 3 ? "0.5px solid var(--border-subtle)" : "none" }}>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 24, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1 }}>{String(val)}</div>
              <div style={{ fontSize: 9.5, color: "var(--text-muted)", marginTop: 5, textTransform: "uppercase", letterSpacing: 0.8 }}>{label}</div>
            </div>
          ))}
        </div>
      )}

      {(job.status === "completed" || job.status === "failed") && scannerRuns.length > 0 && (
        <div style={{ borderTop: "0.5px solid var(--border-subtle)" }}>
          <div style={{ padding: "11px 16px", display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
            <Cpu size={13} color="var(--accent)" />
            <span style={{ fontSize: 11.5, fontWeight: 650, color: "var(--text-primary)" }}>
              {orchestrator?.label ?? String(r.engine ?? "vedha-agent collector")}
            </span>
            {orchestrator?.version && (
              <span style={{ fontSize: 9.5, fontFamily: "var(--font-mono)", color: "var(--text-faint)" }}>
                v{orchestrator.version}
              </span>
            )}
            <span style={{ marginLeft: "auto", fontSize: 9.5, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>
              {scannerRuns.length} components
            </span>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))", borderTop: "0.5px solid var(--border-subtle)" }}>
            {scannerRuns.map((run) => {
              const runColor = run.status === "failed"
                ? "var(--sev-critical-color)"
                : run.status === "degraded"
                  ? "var(--sev-medium-color)"
                  : run.status === "completed" || run.status === "cached"
                    ? "var(--nominal-color)"
                    : "var(--text-faint)";
              return (
                <div key={run.id} title={run.role ?? run.skip_reason} style={{ minWidth: 0, padding: "9px 12px", borderRight: "0.5px solid var(--border-subtle)", borderBottom: "0.5px solid var(--border-subtle)" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 6, minWidth: 0 }}>
                    <span style={{ width: 6, height: 6, borderRadius: "50%", flexShrink: 0, background: runColor }} />
                    <span style={{ fontSize: 10.5, fontWeight: 600, color: "var(--text-secondary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                      {run.label ?? run.id}
                    </span>
                    <span style={{ marginLeft: "auto", color: runColor, fontFamily: "var(--font-mono)", fontSize: 8.5, textTransform: "uppercase" }}>
                      {run.status}
                    </span>
                  </div>
                  <div style={{ marginTop: 4, fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-faint)" }}>
                    {run.fact_count ?? 0} facts
                    {run.reused_fact_count ? ` · ${run.reused_fact_count} cached` : ""}
                    {run.error_count ? ` · ${run.error_count} errors` : ""}
                  </div>
                </div>
              );
            })}
          </div>

          {externalEngines.length > 0 && (
            <div style={{ padding: "9px 16px", display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", color: "var(--text-faint)", fontSize: 9.5 }}>
              <span style={{ fontWeight: 650, textTransform: "uppercase" }}>Standalone validation</span>
              {externalEngines.map((external) => (
                <span key={external.id} title={`${external.role ?? ""} Not executed by this job.`} style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
                  <span style={{ width: 5, height: 5, borderRadius: "50%", background: external.available ? "var(--nominal-color)" : "var(--text-faint)" }} />
                  {external.label ?? external.id} {external.available ? "available" : "not installed"}
                </span>
              ))}
            </div>
          )}

          {issues.length > 0 && (
            <div style={{ padding: "9px 16px", background: "var(--sev-medium-bg)", color: "var(--sev-medium-color)", fontSize: 10.5, lineHeight: 1.5 }}>
              {issues.slice(0, 3).map((issue, index) => (
                <div key={`${issue.message}-${index}`}>
                  {issue.message ?? "Collector error"}
                  {issue.remediation ? ` · ${issue.remediation}` : ""}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div style={{ padding: "10px 16px", display: "flex", flexWrap: "wrap", gap: 14, borderTop: "0.5px solid var(--border-subtle)" }}>
        {job.agent_name && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>vedha-agent <strong style={{ color: "var(--text-secondary)", fontWeight: 600 }}>{job.agent_name}</strong></span>}
        {job.created_at && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Queued <strong style={{ color: "var(--text-secondary)", fontWeight: 600 }}>{new Date(job.created_at).toLocaleTimeString()}</strong></span>}
        <span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>{job.job_id.slice(0, 8)}</span>
      </div>

      {job.status === "failed" && r.error && (
        <div style={{ padding: "11px 16px", background: "var(--sev-critical-bg)", borderTop: "0.5px solid var(--border-subtle)", fontSize: 11.5, color: "var(--sev-critical-color)", fontFamily: "var(--font-mono)" }}>
          {String(r.error)}
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   DISPATCH RECEIPT — prints the exact request sent to the probe
══════════════════════════════════════════════════════ */

function DispatchReceipt({ payload }: { payload: Record<string, unknown> }) {
  const [open, setOpen] = useState(false);
  const params = (payload.params ?? {}) as Record<string, unknown>;
  const line = (k: string, v: unknown) => (v === undefined || v === null || v === "" ? null : (
    <div key={k} style={{ display: "flex", gap: 10, padding: "4px 0", fontSize: 11.5, borderBottom: "0.5px solid var(--border-subtle)" }}>
      <span style={{ color: "var(--text-faint)", fontFamily: "var(--font-mono)", width: 132, flexShrink: 0, fontSize: 10.5 }}>{k}</span>
      <span style={{ color: "var(--text-secondary)", fontFamily: "var(--font-mono)", wordBreak: "break-word", flex: 1 }}>
        {Array.isArray(v) ? v.join("  ·  ") : typeof v === "object" ? JSON.stringify(v) : String(v)}
      </span>
    </div>
  ));
  return (
    <div style={{ borderRadius: 12, border: "0.5px solid var(--border-accent)", background: "var(--bg-panel)", overflow: "hidden", boxShadow: "var(--shadow-md)" }}>
      <button onClick={() => setOpen((v) => !v)} style={{ width: "100%", display: "flex", alignItems: "center", gap: 9, padding: "12px 16px", cursor: "pointer", background: "var(--accent-ghost)", border: "none", borderBottom: open ? "0.5px solid var(--border-subtle)" : "none" }}>
        <Send size={13} color="var(--accent)" />
        <span style={{ fontSize: 12.5, fontWeight: 700, color: "var(--text-primary)", fontFamily: "var(--font-display)" }}>Dispatch details</span>
        <ChevronDown size={14} color="var(--text-muted)" style={{ marginLeft: "auto", transform: open ? "rotate(180deg)" : "none", transition: "transform var(--dur-fast)" }} />
      </button>
      {open && (
        <div style={{ padding: "6px 16px 14px" }}>
          {line("use_case_id", payload.use_case_id)}
          {line("job_type", payload.job_type)}
          {line("engagement_id", payload.engagement_id)}
          {line("scope (targets)", params.targets ?? "→ engagement scope")}
          {line("excluded_cidrs", params.excluded_cidrs)}
          {line("intensity", params.intensity)}
          {line("rate / conc / timeout", params.rate !== undefined ? `${params.rate} pps · ${params.concurrency} · ${params.timeout}s` : undefined)}
          {line("passive_listen_seconds", params.passive_listen_seconds)}
          <div style={{ marginTop: 11, display: "flex", gap: 7, alignItems: "flex-start" }}>
            <ShieldAlert size={13} color="var(--accent)" style={{ flexShrink: 0, marginTop: 1 }} />
            <span style={{ fontSize: 10, color: "var(--text-muted)", lineHeight: 1.5 }}>
              The vedha-agent re-validates this against the engagement&apos;s authoritative scope and exclusions before sending a single packet. Secret-bearing job parameters are rejected by the Manager.
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   PAGE
══════════════════════════════════════════════════════ */

export function ScannerWorkspace({ surface = "manager" }: { surface?: ScannerWorkspaceSurface }) {
  const { success: toastOk, error: toastErr } = useToast();
  const api = useMemo(() => createScannerWorkspaceApi(surface), [surface]);
  const isPortal = surface === "portal";
  const queryClient = useQueryClient();
  // The customer's plan gates launching (the API enforces it; this explains it).
  const { data: plan } = usePortalEntitlement(isPortal);
  // Regular scan types the plan lets the customer run right now. Deep is
  // separate: it requires a single selected asset.
  const portalDial = launchableModes(plan).filter((m): m is Intensity => m !== "deep");

  const [useCases,    setUseCases]    = useState<UseCase[]>([NETWORK_VA_FALLBACK]);
  const [probes,      setProbes]      = useState<Probe[]>([]);
  const [engagements, setEngagements] = useState<Engagement[]>([]);
  const [loadingData, setLoadingData] = useState(true);
  const [setupErrors, setSetupErrors] = useState<Record<string, string>>({});
  const [setupAttempt, setSetupAttempt] = useState(0);
  const inheritedInitialScope = useRef(false);
  const [pollState, setPollState] = useState<{ jobId: string; error: string | null; updatedAt: string | null } | null>(null);
  const pollGeneration = useRef(0);

  const selectedUc = NETWORK_VA_ID;
  const [selectedEng, setSelectedEng] = useState("");
  const [selectedProbe, setSelectedProbe] = useState("");
  const [targets,     setTargets]     = useState("");
  const [excluded,    setExcluded]    = useState("");
  const [scanKind, setScanKind] = useState<"engagement" | "deep">("engagement");
  const [assets, setAssets] = useState<{ engagementId: string; rows: ScanAssetOption[]; loading: boolean; error: string | null }>({ engagementId: "", rows: [], loading: false, error: null });
  const [assetAttempt, setAssetAttempt] = useState(0);
  const currentEngagement = useRef("");
  const dispatchLock = useRef(false);
  const [dispatched,  setDispatched]  = useState<Record<string, unknown> | null>(null);

  // ── Scan tuning ──
  const [intensity,    setIntensity]    = useState<Intensity>("normal");
  // If the remembered choice isn't in the plan (or ran out), show and send the
  // first type that is — derived, so it can never lag the plan.
  const shownIntensity: Intensity = isPortal && portalDial.length && !portalDial.includes(intensity)
    ? portalDial[0] : intensity;
  const [passiveSecs,  setPassiveSecs]  = useState(60);
  const [launching, setLaunching] = useState(false);
  const [job,       setJob]       = useState<JobStatus | null>(null);
  const [recentJobs, setRecentJobs] = useState<JobStatus[]>([]);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const restoreIntensity = useCallback((engagementId: string) => {
    let saved: string | null = null;
    try { saved = sessionStorage.getItem(`vedha.scan-intensity.${surface}.${engagementId}`); } catch { /* storage may be disabled */ }
    setIntensity(INTENSITY.some(option => option.id === saved) ? saved as Intensity : "normal");
  }, [surface]);

  useEffect(() => {
    let alive = true;
    void (async () => {
      setLoadingData(true);
      const [catalog, fleet, scope] = await Promise.allSettled([
        api.useCases<UseCase[]>(),
        api.probes<Probe[]>(),
        api.engagements<{ engagements?: Engagement[] } | Engagement[]>(),
      ]);
      if (!alive) return;
      const errors: Record<string, string> = {};
      if (catalog.status === "fulfilled") setUseCases(catalog.value);
      else errors["Scan catalog"] = catalog.reason instanceof Error ? catalog.reason.message : "Request failed";
      if (fleet.status === "fulfilled") setProbes(fleet.value);
      else errors["Probe inventory"] = fleet.reason instanceof Error ? fleet.reason.message : "Request failed";
      if (scope.status === "fulfilled") {
        const engs = Array.isArray(scope.value) ? scope.value : scope.value.engagements ?? [];
        setEngagements(engs);
        if (!inheritedInitialScope.current) {
          inheritedInitialScope.current = true;
          if (engs.length === 1) {
            currentEngagement.current = engs[0].id;
            setSelectedEng(engs[0].id);
            restoreIntensity(engs[0].id);
            setTargets((engs[0].scopeCidrs ?? []).join("\n"));
            setExcluded((engs[0].excludedCidrs ?? []).join("\n"));
          }
        }
      } else errors["Engagement scope"] = scope.reason instanceof Error ? scope.reason.message : "Request failed";
      setSetupErrors(errors);
      setLoadingData(false);
    })();
    return () => { alive = false; };
  }, [api, setupAttempt, restoreIntensity]);

  const startPolling = useCallback((jobId: string) => {
    if (pollRef.current) clearInterval(pollRef.current);
    const generation = ++pollGeneration.current;
    let inFlight = false;
    const poll = async () => {
      if (inFlight) return;
      inFlight = true;
      try {
        const j = await api.job<JobStatus>(jobId);
        if (generation !== pollGeneration.current) return;
        setPollState({ jobId, error: null, updatedAt: new Date().toISOString() });
        setJob((cur) => (cur && cur.job_id !== j.job_id ? cur : j));
        setRecentJobs((prev) => prev.some((rj) => rj.job_id === j.job_id)
          ? prev.map((rj) => (rj.job_id === j.job_id ? { ...rj, ...j } : rj))
          : [j, ...prev]);
        if (j.status === "completed" || j.status === "failed" || j.status === "cancelled") {
          clearInterval(pollRef.current!); pollRef.current = null;
          if (j.status === "completed") toastOk("Scan complete"); else if (j.status === "failed") toastErr("Scan failed");
        }
      } catch (cause) {
        if (generation !== pollGeneration.current) return;
        setPollState((previous) => ({ jobId, error: cause instanceof Error ? cause.message : "Request failed", updatedAt: previous?.jobId === jobId ? previous.updatedAt : null }));
      } finally { inFlight = false; }
    };
    pollRef.current = setInterval(() => { void poll(); }, 4000);
    void poll();
  }, [api, toastOk, toastErr]);

  // Rehydrate this engagement's jobs from the DB so a launched job survives a
  // page refresh or navigation (root-cause fix: the queue lived only in memory).
  const loadJobs = useCallback(async (engagementId: string) => {
    if (!engagementId) { setRecentJobs([]); return; }
    try {
      const rows = await api.jobs<Array<{
        id: string; status: JobStatus["status"]; agent_id: string | null;
        agent_name: string | null; use_case_id: string | null;
        result: Record<string, unknown> | null;
        created_at: string | null; started_at: string | null; completed_at: string | null;
      }>>(engagementId);
      if (currentEngagement.current !== engagementId) return;
      const jobs: JobStatus[] = rows.map((r) => ({
        job_id: r.id, engagement_id: engagementId, status: r.status,
        created_at: r.created_at, started_at: r.started_at, completed_at: r.completed_at,
        agent_id: r.agent_id, agent_name: r.agent_name ?? null,
        use_case_id: r.use_case_id ?? null, result: r.result,
      }));
      setRecentJobs(jobs);
      // Restore an in-flight job and resume polling — this is exactly what a
      // refresh used to drop.
      const active = jobs.find((j) => j.status === "pending" || j.status === "running");
      setJob((cur) => cur ?? active ?? null);
      if (active && !pollRef.current) startPolling(active.job_id);
    } catch { /* history is non-critical; leave the launcher usable */ }
  }, [api, startPolling]);

  useEffect(() => () => { if (pollRef.current) clearInterval(pollRef.current); pollGeneration.current += 1; }, []);

  // Load (and restore) jobs whenever the selected engagement changes — covers
  // the single-engagement auto-select on mount and manual selection alike.
  // Wrapped in an async IIFE (same pattern as the initial load effect) so no
  // setState runs synchronously in the effect body.
  useEffect(() => {
    (async () => {
      if (selectedEng) await loadJobs(selectedEng);
      else setRecentJobs([]);
    })();
  }, [selectedEng, loadJobs]);

  const ucObj      = useCases.find((u) => u.use_case_id === selectedUc);
  const selectedEngagement = engagements.find((engagement) => engagement.id === selectedEng);
  const inheritedScope = (selectedEngagement?.scopeCidrs ?? []).join("\n");
  const inheritedExcluded = (selectedEngagement?.excludedCidrs ?? []).join("\n");
  const compatibleProbes = ucObj
    ? probes.filter((p) => p.online && p.capabilities.includes(scanKind === "deep" ? "deep_port_sweep" : ucObj.scan_type))
    : [];
  const compatibleIdleProbes = compatibleProbes.filter((p) => !p.current_job_id);

  // Derive the effective probe: honor an explicit operator choice when it's still
  // compatible, otherwise default to an active probe (idle preferred). Derived at
  // render time — no effect needed, so it can never lag the compatible set.
  const effectiveProbe = (selectedProbe && compatibleProbes.some((p) => p.id === selectedProbe))
    ? selectedProbe
    : (compatibleIdleProbes[0]?.id ?? compatibleProbes[0]?.id ?? "");

  const isOt         = ucObj?.profile === "ot";
  const parseList    = (s: string) => s.split(/[\s,\n]+/).map((t) => t.trim()).filter(Boolean);
  const targetCount  = parseList(targets).length;
  const excludeCount = parseList(excluded).length;
  // True when the field still matches what the engagement declared (i.e. the
  // operator hasn't overridden it) — drives the "inherited" UI + launch payload.
  const scopeIsInherited   = inheritedScope.trim()    !== "" && targets.trim()  === inheritedScope.trim();
  const excludeIsInherited = inheritedExcluded.trim() !== "" && excluded.trim() === inheritedExcluded.trim();


  function chooseIntensity(value: Intensity) {
    setIntensity(value);
    if (selectedEng) try { sessionStorage.setItem(`vedha.scan-intensity.${surface}.${selectedEng}`, value); } catch { /* session preference is optional */ }
  }

  function selectEngagement(engagementId: string) {
    if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; }
    pollGeneration.current += 1;
    currentEngagement.current = engagementId;
    const engagement = engagements.find(item => item.id === engagementId);
    setSelectedEng(engagementId);
    setTargets((engagement?.scopeCidrs ?? []).join("\n"));
    setExcluded((engagement?.excludedCidrs ?? []).join("\n"));
    setSelectedProbe(""); setJob(null); setRecentJobs([]); setDispatched(null); setPollState(null);
    restoreIntensity(engagementId);
  }

  useEffect(() => {
    if (!selectedEng) return;
    let alive = true;
    void (async () => {
      setAssets({ engagementId: selectedEng, rows: [], loading: true, error: null });
      try {
        const rows = await api.assets<ScanAssetOption[]>(selectedEng);
        if (alive) setAssets({ engagementId: selectedEng, rows, loading: false, error: null });
      } catch (error) {
        if (alive) setAssets({ engagementId: selectedEng, rows: [], loading: false, error: error instanceof Error ? error.message : "Could not load IPs" });
      }
    })();
    return () => { alive = false; };
  }, [api, selectedEng, assetAttempt]);

  function buildLaunchBody(): ScanLaunchBody {
    const targetList  = parseList(targets);
    const excludeList = parseList(excluded);
    const b: ScanLaunchBody = {
      engagement_id: selectedEng, use_case_id: selectedUc,
      // Only send an explicit list when the operator narrowed it beyond what the
      // engagement declares; otherwise send nothing and let the backend apply the
      // engagement's authoritative scope/exclusions (no duplication).
      targets: (targetList.length && !scopeIsInherited) ? targetList : undefined,
      excluded_cidrs: (excludeList.length && !excludeIsInherited) ? excludeList : undefined,
      preferred_agent_id: effectiveProbe || undefined,
    };
    if (isOt) b.passive_listen_seconds = passiveSecs; else b.intensity = shownIntensity;
    return b;
  }

  async function launch() {
    if (launching || loadingData || Object.keys(setupErrors).length > 0) return;
    if (!selectedUc)  { toastErr("Select a scan"); return; }
    if (!selectedEng) { toastErr("Select an engagement"); return; }
    if (!compatibleProbes.length) {
      toastErr("No compatible probe", `An online probe must advertise ${ucObj?.scan_type ?? "this capability"}.`);
      return;
    }
    await dispatch(buildLaunchBody(), selectedUc);
  }

  /** Deep scan: every port on exactly one asset. On the portal the manager pins
   *  the use case, preset and target and charges the plan; on the operator
   *  Scanner it is a plain enqueue that is never charged to the customer. */
  async function launchDeep(ip: string) {
    if (launching || loadingData || Object.keys(setupErrors).length) return;
    if (!selectedEng) { toastErr("Select an engagement"); return; }
    if (!scanIpAllowed(ip, selectedEngagement?.scopeCidrs ?? [], selectedEngagement?.excludedCidrs ?? [])) {
      toastErr("Choose one IP inside this engagement’s authorized scope"); return;
    }
    const probe = deepProbes.find(p => p.id === effectiveProbe);
    if (!probe) { toastErr("No compatible agent is available for deep scanning"); return; }
    await dispatch(buildDeepScanLaunch({
      engagementId: selectedEng, ip, probeId: probe?.id,
      audience: isPortal ? "portal" : "operator",
    }), DEEP_SCAN_UC);
  }

  async function dispatch(body: ScanLaunchBody, launchedUc: string) {
    if (dispatchLock.current) return;
    dispatchLock.current = true;
    if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; }
    pollGeneration.current += 1;
    setLaunching(true); setJob(null); setDispatched(null);
    try {
      const res = await api.launch<{
        job_id: string; status: string; dispatched?: Record<string, unknown>;
        fragile_excluded?: Array<{ ip: string; reasons: string[] }>;
      }>(body);
      if (res.dispatched) setDispatched(res.dispatched);
      const launched: JobStatus = {
        job_id: res.job_id, engagement_id: body.engagement_id, status: "pending",
        created_at: new Date().toISOString(), started_at: null, completed_at: null,
        agent_id: null, agent_name: null, use_case_id: launchedUc, result: null,
      };
      setJob(launched);
      // Reflect it in the DB-backed history immediately (the poll keeps it fresh).
      setRecentJobs((prev) => [launched, ...prev.filter((rj) => rj.job_id !== launched.job_id)]);
      startPolling(res.job_id);
      if (isPortal) void queryClient.invalidateQueries({ queryKey: ["portal", "entitlement"] });
      const protectedHosts = res.fragile_excluded ?? [];
      toastOk("Job queued", protectedHosts.length
        ? `Probe picks up on next poll (~10s). ${protectedHosts.length} fragile host${protectedHosts.length === 1 ? "" : "s"} (HSM / ATM / SWIFT / ICS) kept out of this scan: ${protectedHosts.map((h) => h.ip).join(", ")}`
        : "Probe picks up on next poll (~10s)");
    } catch (e) {
      toastErr("Launch failed", (e as Error).message);
      // A refusal (plan, asset already deep-scanned…) may mean the plan moved on.
      if (isPortal) void queryClient.invalidateQueries({ queryKey: ["portal", "entitlement"] });
    } finally {
      dispatchLock.current = false;
      setLaunching(false);
    }
  }

  function reset() {
    selectEngagement(engagements.length === 1 ? engagements[0].id : "");
    setScanKind("engagement"); chooseIntensity("normal"); setPassiveSecs(60);
  }

  // Portal: explain exactly why Launch is off — the plan, the chosen type, or none left.
  const planBlock = !isPortal ? null : !plan ? "Checking scan allowance…"
    : !plan.can_scan ? plan.reason
    : isOt ? null
    : !portalDial.length ? "No regular scan types are left in your plan."
    : !plan.modes[shownIntensity]?.can_scan ? plan.modes[shownIntensity]?.reason ?? "This scan type isn't available."
    : null;
  const canLaunch = !!ucObj && !!selectedEng && compatibleProbes.length > 0 && !launching && !planBlock && !loadingData && Object.keys(setupErrors).length === 0 && targetCount > 0;
  const deepProbes = probes.filter((p) => p.online && p.capabilities.includes("deep_port_sweep"));
  const intensityObj = INTENSITY.find((i) => i.id === shownIntensity)!;

  const ucNameFor = (id: string | null) =>
    useCases.find((u) => u.use_case_id === id)?.display_name ?? (id === DEEP_SCAN_UC ? "Deep scan · one IP" : "Scan");

  // Bring a job (from the recent list) back into the active panel; resume polling
  // if it's still in flight, otherwise stop any poll and just show its result.
  function viewJob(rj: JobStatus) {
    setJob(rj);
    if (rj.status === "pending" || rj.status === "running") startPolling(rj.job_id);
    else { if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; } pollGeneration.current += 1; }
  }

  const Shell = isPortal ? PortalShell : PageShell;
  const setupBlocked = loadingData || Object.keys(setupErrors).length > 0;
  const readiness = setupBlocked ? "Scan setup must be verified before launch."
    : !selectedEng ? "Select an engagement to continue."
    : !compatibleProbes.length ? "No compatible agent is online. Connect an agent to start scanning."
    : compatibleIdleProbes.length ? "Agent ready" : "Agent busy · scan will queue";
  const selectedAssets = assets.engagementId === selectedEng ? assets : null;

  return (
    <Shell title="Scanner" subtitle="Run a network assessment with a deployed vedha-agent." hideRefresh
      headerActions={<button type="button" className="btn btn-secondary" disabled={loadingData}
        onClick={() => setSetupAttempt(attempt => attempt + 1)}><RefreshCw size={14} /> {loadingData ? "Refreshing setup…" : "Refresh setup"}</button>}>
      <div className="scn-page scanner-workspace" data-input="keyboard"
        onPointerDownCapture={event => { event.currentTarget.dataset.input = "pointer"; }}
        onKeyDownCapture={event => { event.currentTarget.dataset.input = "keyboard"; }}>
        {Object.keys(setupErrors).length > 0 && <div role="alert" className="scn-recovery">
          <strong>Could not verify scan setup</strong>
          {Object.entries(setupErrors).map(([label, message]) => <p key={label}>{label}: {message}</p>)}
          <button type="button" className="btn btn-secondary" disabled={loadingData}
            onClick={() => setSetupAttempt(attempt => attempt + 1)}>Retry setup</button>
        </div>}
        {!setupErrors["Probe inventory"] && <ScannerFleetStrip probes={probes} loading={loadingData}
          href={isPortal ? "/portal/fleet" : "/fleet"} />}
        <NetworkVaHero available={!!ucObj} loading={loadingData} disabled={launching} selected={scanKind === "engagement"}
          onConfigure={() => { setScanKind("engagement"); setSelectedProbe(""); }}
          campaignHref={isPortal ? "/portal/scans#campaign" : "/campaign"} />
        <section className="scanner-setup" aria-labelledby="scanner-setup-title" aria-busy={loadingData}>
          <header className="scanner-setup-header">
            <span className="scanner-config-icon"><SlidersHorizontal size={18} aria-hidden="true" /></span>
            <div><h2 id="scanner-setup-title">Configure &amp; launch</h2><p>Set the engagement, scope, and scan intensity.</p></div>
            <span className="scanner-config-context">{scanKind === "deep" ? "Deep scan · one IP" : "Network assessment"}</span>
          </header>
          <div className="scanner-console-body" data-kind={scanKind}>
          <div className="scanner-target-column">
            <h3>Target and agent</h3>
            <div className="scanner-fields">
              <div><label htmlFor="scan-engagement">Engagement</label>
                <select id="scan-engagement" value={selectedEng} disabled={loadingData || launching}
                  onChange={event => selectEngagement(event.target.value)}>
                  <option value="">Select an engagement…</option>
                  {engagements.map(engagement => <option key={engagement.id} value={engagement.id}>{engagement.name}</option>)}
                </select>
              </div>
              <div><label htmlFor="scan-probe">vedha-agent</label>
                <select id="scan-probe" value={effectiveProbe} disabled={!compatibleProbes.length || launching || !selectedEng}
                  onChange={event => setSelectedProbe(event.target.value)}>
                  {!compatibleProbes.length && <option value="">No compatible agent online</option>}
                  {compatibleProbes.map(probe => <option key={probe.id} value={probe.id}>{probe.name}{probe.current_job_id ? " · busy" : " · idle"}</option>)}
                </select>
              </div>
            </div>
            <fieldset className="scanner-coverage" disabled={launching}>
              <legend>Scan type</legend>
              <div className="scanner-coverage-options">
                <label data-selected={scanKind === "engagement"}><input type="radio" name="scan-coverage" value="engagement"
                  checked={scanKind === "engagement"} onChange={() => { setScanKind("engagement"); setSelectedProbe(""); }} /><Radar size={15} aria-hidden="true" /> Network assessment</label>
                <label data-selected={scanKind === "deep"}><input type="radio" name="scan-coverage" value="deep"
                  checked={scanKind === "deep"} onChange={() => { setScanKind("deep"); setSelectedProbe(""); }} /><ScanLine size={15} aria-hidden="true" /> Deep scan · one IP</label>
              </div>
            </fieldset>
            <div key={scanKind} className="scanner-target-content">
            {scanKind === "engagement" ? <>
              <div className="scanner-scope-heading"><label htmlFor="scan-scope">Target scope</label>
                {scopeIsInherited && <span><Link2 size={12} aria-hidden="true" />From engagement</span>}
                {!scopeIsInherited && inheritedScope && <button type="button" className="scanner-text-action" disabled={launching}
                  onClick={() => setTargets(inheritedScope)}>Reset scope</button>}
              </div>
              <textarea id="scan-scope" value={targets} disabled={!selectedEng || launching} rows={3}
                placeholder={selectedEng ? "No scope configured for this engagement" : "Select an engagement to load its scope"}
                onChange={event => setTargets(event.target.value)} aria-describedby="scan-scope-help" />
              <p id="scan-scope-help" className="scanner-help">{scopeIsInherited ? "Targets are inherited from this engagement." : "Narrow targets within the engagement’s authorized scope."}</p>
              <details className="scanner-details">
                <summary>Excluded scope{excludeCount ? ` · ${excludeCount} exclusion${excludeCount === 1 ? "" : "s"}` : " · optional"}</summary>
                <label htmlFor="scan-excluded">Excluded IPs or CIDRs</label>
                <textarea id="scan-excluded" value={excluded} disabled={!selectedEng || launching} rows={2}
                  onChange={event => setExcluded(event.target.value)} />
                <p className="scanner-help">{excludeIsInherited ? "Inherited engagement exclusions remain enforced." : "These exclusions are applied in addition to engagement boundaries."}</p>
              </details>
            </> : !selectedEng ? <p className="scanner-help">Select an engagement to choose one IP for a deep scan.</p>
              : isPortal && !plan ? <p className="scanner-help">Checking deep scan allowance…</p> : <DeepScanCard key={selectedEng}
                plan={isPortal ? plan : null} scope={selectedEngagement?.scopeCidrs ?? []}
                excluded={selectedEngagement?.excludedCidrs ?? []} assets={selectedAssets?.rows ?? []}
                assetsLoading={!selectedAssets || selectedAssets.loading} assetsError={selectedAssets?.error}
                onRetryAssets={() => setAssetAttempt(attempt => attempt + 1)}
                probeReady={deepProbes.length > 0} launching={launching}
                blockedReason={setupBlocked ? "Scan setup must be verified before launch." : null}
                onLaunch={ip => void launchDeep(ip)} />}
            </div>
          </div>
          {scanKind === "engagement" && <aside className="scanner-review-column" aria-label="Scan review and launch">
            {!isOt && <ScanIntensityControl value={shownIntensity} onChange={chooseIntensity} disabled={!selectedEng || launching}
              allowed={isPortal ? portalDial : undefined} badges={isPortal && plan ? {
                stealth: modeShort(plan.modes.stealth), normal: modeShort(plan.modes.normal), aggressive: modeShort(plan.modes.aggressive),
              } : undefined} />}
            {isOt && <label htmlFor="scan-passive-seconds">Passive listen window (seconds)
              <input id="scan-passive-seconds" type="number" min={5} max={3600} value={passiveSecs}
                onChange={event => setPassiveSecs(Math.max(5, Math.min(3600, Number(event.target.value) || 0)))} /></label>}
            <dl className="scanner-review-facts" aria-label="Scan summary">
              <div><dt>Mode</dt><dd>{isOt ? `Passive · ${passiveSecs}s` : intensityObj.label}</dd></div>
              <div><dt>Scope</dt><dd>{!selectedEng ? "Select engagement" : targetCount ? `${targetCount} target ${targetCount === 1 ? "entry" : "entries"}` : "Not configured"}</dd></div>
              <div><dt>Exclusions</dt><dd>{!selectedEng ? "—" : excludeCount ? `${excludeCount} applied` : "None configured"}</dd></div>
            </dl>
            <div className="scanner-launch-review">
              <p className="scanner-readiness" role="status" data-ready={!setupBlocked && !!selectedEng && compatibleIdleProbes.length > 0}><span aria-hidden="true" />{readiness}</p>
              {planBlock && <p className="scanner-help">{planBlock}</p>}
              {isPortal && plan?.modes[shownIntensity]?.left != null && <p className="scanner-help">Uses 1 of {plan.modes[shownIntensity].left} remaining {intensityObj.label.toLowerCase()} scans.</p>}
              <button type="button" className="btn btn-primary" onClick={launch} disabled={!canLaunch}>
                {launching ? <><Loader size={15} className="scn-spin" /> Dispatching…</> : <><Play size={15} /> Launch scan</>}
              </button>
              <button type="button" className="scanner-text-action" disabled={launching} onClick={reset}><RotateCcw size={13} /> Reset configuration</button>
            </div>
          </aside>}
          </div>
        </section>
        {/* ── Active job + dispatch receipt ── */}
        {job && (
          <section>
            <SectionLabel>Active Job</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {dispatched && <DispatchReceipt payload={dispatched} />}
              {pollState?.jobId === job.job_id && pollState.error && (
                <div role="status" className="scn-recovery">
                  <strong>Job status may be out of date</strong>
                  <p>{pollState.error}</p>
                  <p>{pollState.updatedAt ? `Last successful update: ${new Date(pollState.updatedAt).toLocaleString()}` : "No successful status update yet."} The last known job is shown below; execution has not been restarted.</p>
                  <button type="button" className="btn btn-secondary" onClick={() => startPolling(job.job_id)}>Retry job status</button>
                </div>
              )}
              <JobPanel job={job} ucName={ucNameFor(job.use_case_id) || ucObj?.display_name} />
            </div>
          </section>
        )}

        {/* ── Detection pipeline — extends the scan past "Complete" into the
             manager's Detection → Correlation → Prioritization → Remediation,
             with per-probe jobs and findings + step-by-step remediation. ── */}
        {selectedEng && (job || recentJobs.length > 0) && (
          <details className="scanner-details">
            <summary>Assessment progress</summary>
            <CampaignProgress engagementId={selectedEng} surface={surface} />
          </details>
        )}

        {/* ── Recent scans (loaded from the DB — survives refresh / navigation) ── */}
        {recentJobs.length > 0 && (
          <section>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
              <SectionLabel>Recent Scans</SectionLabel>
              <button onClick={() => selectedEng && loadJobs(selectedEng)} className="scn-reset" title="Refresh from server">
                <RefreshCw size={11} /> Refresh
              </button>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {recentJobs.map((rj) => {
                const st = REC_ST[rj.status] ?? REC_ST.pending;
                const isCur = job?.job_id === rj.job_id;
                return (
                  <button key={rj.job_id} onClick={() => viewJob(rj)} className="scn-recent" data-on={isCur}>
                    <span className="scn-recent-dot" style={{ width: 7, height: 7, borderRadius: "50%", background: st.color, flexShrink: 0 }} />
                    <span className="scn-recent-name" style={{ fontWeight: 600, fontSize: 12.5, color: "var(--text-primary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{ucNameFor(rj.use_case_id)}</span>
                    <span className="scn-recent-status" style={{ fontSize: 9.5, fontWeight: 700, color: st.color, textTransform: "uppercase", letterSpacing: 0.4 }}>{st.label}</span>
                    {rj.agent_name && <span className="scn-recent-agent" style={{ fontSize: 11, color: "var(--text-muted)" }}>{rj.agent_name}</span>}
                    <span className="scn-recent-time" style={{ marginLeft: "auto", fontSize: 10.5, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>
                      {rj.created_at ? new Date(rj.created_at).toLocaleString() : ""}
                    </span>
                    <span className="scn-recent-id" style={{ fontSize: 9.5, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>{rj.job_id.slice(0, 8)}</span>
                  </button>
                );
              })}
            </div>
          </section>
        )}
      </div>
    </Shell>
  );
}

export default function ScanPage() {
  return <ScannerWorkspace surface="manager" />;
}
