"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";
import {
  Play, Shield, Globe, Database, Server, Wifi,
  Activity, Eye, RefreshCw, ChevronRight, ChevronDown,
  CheckCircle, Clock, XCircle, Loader,
  Cpu, Network, RotateCcw, Target,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useToast } from "../../hooks/useToast";

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
}

interface JobStatus {
  job_id: string;
  engagement_id: string;
  status: "pending" | "running" | "completed" | "failed";
  created_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  agent_id: string | null;
  agent_name: string | null;
  use_case_id: string | null;
  result: Record<string, unknown> | null;
}

/* ══════════════════════════════════════════════════════
   USE-CASE METADATA
══════════════════════════════════════════════════════ */

const UC_META: Record<string, { cat: string; icon: React.ReactNode; risk: "passive" | "low" | "medium" | "high" }> = {
  uc_discovery_only:       { cat: "Discovery",   icon: <Network size={16} />,   risk: "low"     },
  uc_iot_device_survey:    { cat: "Discovery",   icon: <Wifi size={16} />,      risk: "low"     },
  uc_full_assessment:      { cat: "Assessment",  icon: <Shield size={16} />,    risk: "high"    },
  uc_rescan_delta:         { cat: "Assessment",  icon: <RefreshCw size={16} />, risk: "high"    },
  uc_external_web_triage:  { cat: "Targeted",    icon: <Globe size={16} />,     risk: "medium"  },
  uc_web_app_triage:       { cat: "Targeted",    icon: <Globe size={16} />,     risk: "medium"  },
  uc_db_exposure:          { cat: "Targeted",    icon: <Database size={16} />,  risk: "medium"  },
  uc_windows_estate:       { cat: "Targeted",    icon: <Server size={16} />,    risk: "medium"  },
  uc_udp_service_exposure: { cat: "Targeted",    icon: <Activity size={16} />,  risk: "medium"  },
  uc_ot_passive:           { cat: "Specialized", icon: <Eye size={16} />,       risk: "passive" },
  uc_ai_endpoint_sweep:    { cat: "Specialized", icon: <Cpu size={16} />,       risk: "medium"  },
};

const RISK: Record<string, { color: string; bg: string; label: string }> = {
  passive: { color: "#6ee7b7",                      bg: "rgba(110,231,183,0.10)", label: "Passive"   },
  low:     { color: "var(--sev-low-color)",          bg: "var(--sev-low-bg)",      label: "Low noise" },
  medium:  { color: "var(--sev-medium-color)",       bg: "var(--sev-medium-bg)",   label: "Moderate"  },
  high:    { color: "var(--sev-high-color)",         bg: "var(--sev-high-bg)",     label: "Active"    },
};

const PROFILE_BADGE: Record<string, { label: string; color: string }> = {
  it:  { label: "IT",  color: "var(--accent)" },
  iot: { label: "IoT", color: "#f59e0b"       },
  ot:  { label: "OT",  color: "#10b981"       },
};

/* ══════════════════════════════════════════════════════
   AUTH HELPER
══════════════════════════════════════════════════════ */

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("adversa_token") || sessionStorage.getItem("adversa_token");
}

async function apiFetch<T>(path: string, opts?: RequestInit): Promise<T> {
  const token = getToken();
  const res = await fetch(path, {
    ...opts,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(opts?.headers ?? {}),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText })) as { error?: string };
    throw new Error(err.error ?? res.statusText);
  }
  return res.json() as Promise<T>;
}

/* ══════════════════════════════════════════════════════
   PROBE BAR
══════════════════════════════════════════════════════ */

function ProbeBar({ probes }: { probes: Probe[] }) {
  if (!probes.length) {
    return (
      <div style={{ padding: "10px 14px", borderRadius: 8, background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)", fontSize: 12, color: "var(--text-muted)" }}>
        No probes registered — deploy a probe agent to start scanning
      </div>
    );
  }
  const online = probes.filter((p) => p.online).length;
  const busy   = probes.filter((p) => p.current_job_id).length;
  return (
    <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
      {probes.map((p) => {
        const dot = !p.online ? "var(--text-faint)" : p.current_job_id ? "var(--sev-medium-color)" : "var(--sev-low-color)";
        const label = !p.online ? "offline" : p.current_job_id ? "busy" : "idle";
        return (
          <div key={p.id} style={{ display: "flex", alignItems: "center", gap: 7, padding: "6px 12px", borderRadius: 8, background: "var(--bg-surface)", border: `0.5px solid ${p.online ? "var(--border-accent)" : "var(--border-subtle)"}`, fontSize: 12 }}>
            <span style={{ width: 7, height: 7, borderRadius: "50%", background: dot, flexShrink: 0 }} />
            <span style={{ fontWeight: 600, color: "var(--text-primary)" }}>{p.name}</span>
            {p.location && <span style={{ color: "var(--text-muted)" }}>{p.location}</span>}
            <span style={{ color: dot }}>{label}</span>
          </div>
        );
      })}
      <div style={{ padding: "6px 12px", borderRadius: 8, background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)", fontSize: 11, color: "var(--text-secondary)" }}>
        {online}/{probes.length} online · {busy} busy
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   USE-CASE CARD
══════════════════════════════════════════════════════ */

function UseCaseCard({ uc, selected, onClick }: { uc: UseCase; selected: boolean; onClick: () => void }) {
  const meta  = UC_META[uc.use_case_id] ?? { cat: "Other", icon: <Target size={16} />, risk: "medium" as const };
  const risk  = RISK[meta.risk];
  const prof  = PROFILE_BADGE[uc.profile];
  return (
    <button
      onClick={onClick}
      style={{
        textAlign: "left", cursor: "pointer",
        padding: "13px 14px", borderRadius: 10,
        background: selected ? "var(--accent-ghost)" : "var(--bg-surface)",
        border: `1px solid ${selected ? "var(--accent)" : "var(--border-subtle)"}`,
        boxShadow: selected ? "0 0 0 1px var(--accent)" : "none",
        transition: "all 0.12s", display: "flex", flexDirection: "column", gap: 8, width: "100%",
      }}
    >
      <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
        <div style={{ width: 30, height: 30, borderRadius: 7, flexShrink: 0, background: selected ? "var(--accent-ghost)" : "var(--bg-card)", border: "0.5px solid var(--border-subtle)", display: "flex", alignItems: "center", justifyContent: "center", color: selected ? "var(--accent)" : "var(--text-secondary)" }}>
          {meta.icon}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, fontSize: 12.5, color: "var(--text-primary)", lineHeight: 1.3 }}>{uc.display_name}</div>
          <div style={{ display: "flex", gap: 4, marginTop: 4, flexWrap: "wrap" }}>
            <span style={{ fontSize: 10, fontWeight: 700, color: prof.color, background: `${prof.color}18`, border: `0.5px solid ${prof.color}40`, borderRadius: 4, padding: "1px 5px" }}>{prof.label}</span>
            <span style={{ fontSize: 10, fontWeight: 600, color: risk.color, background: risk.bg, border: `0.5px solid ${risk.color}40`, borderRadius: 4, padding: "1px 5px" }}>{risk.label}</span>
            <span style={{ fontSize: 10, color: "var(--text-muted)", fontFamily: "'JetBrains Mono', monospace" }}>~{uc.expected_runtime_hint}</span>
          </div>
        </div>
        {selected && <CheckCircle size={13} color="var(--accent)" style={{ flexShrink: 0, marginTop: 2 }} />}
      </div>
      <p style={{ margin: 0, fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.5 }}>{uc.description}</p>
      <code style={{ fontSize: 9.5, color: "var(--text-muted)", background: "var(--bg-card)", border: "0.5px solid var(--border-subtle)", borderRadius: 3, padding: "1px 6px" }}>
        {uc.scan_type}
      </code>
    </button>
  );
}

/* ══════════════════════════════════════════════════════
   JOB PANEL
══════════════════════════════════════════════════════ */

function JobPanel({ job, ucName }: { job: JobStatus; ucName?: string }) {
  const r = job.result ?? {};
  const elapsed = job.started_at && job.completed_at
    ? Math.round((new Date(job.completed_at).getTime() - new Date(job.started_at).getTime()) / 1000)
    : null;

  const STATUS_ICON: Record<string, React.ReactNode> = {
    pending:   <Clock size={12} />,
    running:   <Loader size={12} style={{ animation: "spin 1s linear infinite" }} />,
    completed: <CheckCircle size={12} />,
    failed:    <XCircle size={12} />,
  };
  const STATUS_COLOR: Record<string, string> = {
    pending:   "var(--text-muted)",
    running:   "var(--accent)",
    completed: "var(--sev-low-color)",
    failed:    "var(--sev-critical-color)",
  };
  const sc = STATUS_COLOR[job.status] ?? "var(--text-muted)";

  return (
    <div style={{ borderRadius: 10, border: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)", overflow: "hidden" }}>
      {/* Header */}
      <div style={{ padding: "10px 14px", display: "flex", alignItems: "center", gap: 10, background: `${sc}0d`, borderBottom: "0.5px solid var(--border-subtle)" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 5, color: sc, fontWeight: 700, fontSize: 12 }}>
          {STATUS_ICON[job.status]} {job.status.toUpperCase()}
        </span>
        {ucName && <span style={{ fontSize: 12, color: "var(--text-secondary)" }}>{ucName}</span>}
        {elapsed !== null && <span style={{ marginLeft: "auto", fontSize: 11, color: "var(--text-muted)", fontFamily: "'JetBrains Mono', monospace" }}>{elapsed}s</span>}
      </div>

      {/* Stats */}
      {job.status === "completed" && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)" }}>
          {([
            ["Hosts",      (r.host_count    ?? (r.run_stats as Record<string,unknown>)?.host_count    ?? "—")],
            ["Open Ports", (r.open_ports    ?? (r.run_stats as Record<string,unknown>)?.open_ports    ?? "—")],
            ["Facts",      (r.fact_count    ?? (r.run_stats as Record<string,unknown>)?.fact_count    ?? "—")],
            ["Findings",   (r.finding_count ?? "0")],
          ] as [string, unknown][]).map(([label, val], i) => (
            <div key={label} style={{ padding: "14px 12px", textAlign: "center", borderRight: i < 3 ? "0.5px solid var(--border-subtle)" : "none" }}>
              <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 22, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1 }}>{String(val)}</div>
              <div style={{ fontSize: 10, color: "var(--text-muted)", marginTop: 4, textTransform: "uppercase", letterSpacing: 0.8 }}>{label}</div>
            </div>
          ))}
        </div>
      )}

      {/* Meta */}
      <div style={{ padding: "8px 14px", display: "flex", flexWrap: "wrap", gap: 12, borderTop: "0.5px solid var(--border-subtle)" }}>
        {job.agent_name && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Probe: <strong style={{ color: "var(--text-secondary)" }}>{job.agent_name}</strong></span>}
        {job.created_at && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Queued: <strong style={{ color: "var(--text-secondary)" }}>{new Date(job.created_at).toLocaleTimeString()}</strong></span>}
        {job.started_at && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Started: <strong style={{ color: "var(--text-secondary)" }}>{new Date(job.started_at).toLocaleTimeString()}</strong></span>}
        <span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-faint)", fontFamily: "'JetBrains Mono', monospace" }}>{job.job_id.slice(0, 8)}</span>
      </div>

      {/* Error */}
      {job.status === "failed" && r.error && (
        <div style={{ padding: "10px 14px", background: "rgba(248,113,113,0.06)", borderTop: "0.5px solid var(--border-subtle)", fontSize: 12, color: "var(--sev-critical-color)", fontFamily: "'JetBrains Mono', monospace" }}>
          {String(r.error)}
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   PAGE
══════════════════════════════════════════════════════ */

const CATS = ["Discovery", "Assessment", "Targeted", "Specialized"];

export default function ScanPage() {
  const { success: toastOk, error: toastErr } = useToast();

  const [useCases,     setUseCases]     = useState<UseCase[]>([]);
  const [probes,       setProbes]       = useState<Probe[]>([]);
  const [engagements,  setEngagements]  = useState<Engagement[]>([]);
  const [loadingData,  setLoadingData]  = useState(true);

  const [selectedUc,   setSelectedUc]   = useState("");
  const [selectedEng,  setSelectedEng]  = useState("");
  const [targets,      setTargets]      = useState("");
  const [expandedCat,  setExpandedCat]  = useState("Discovery");

  const [launching,    setLaunching]    = useState(false);
  const [job,          setJob]          = useState<JobStatus | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoadingData(true);
      try {
        const [uc, pr, engRaw] = await Promise.all([
          apiFetch<UseCase[]>("/api/scan/use-cases"),
          apiFetch<Probe[]>("/api/scan/probes"),
          apiFetch<{ engagements?: Engagement[] } | Engagement[]>("/api/engagements"),
        ]);
        if (!alive) return;
        setUseCases(uc);
        setProbes(pr);
        const engs = Array.isArray(engRaw) ? engRaw : (engRaw as { engagements?: Engagement[] }).engagements ?? [];
        setEngagements(engs);
        if (engs.length === 1) setSelectedEng(engs[0].id);
      } catch (e) {
        toastErr("Load failed", (e as Error).message);
      } finally {
        if (alive) setLoadingData(false);
      }
    })();
    return () => { alive = false; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const startPolling = useCallback((jobId: string) => {
    if (pollRef.current) clearInterval(pollRef.current);
    pollRef.current = setInterval(async () => {
      try {
        const j = await apiFetch<JobStatus>(`/api/scan/jobs/${jobId}`);
        setJob(j);
        if (j.status === "completed" || j.status === "failed") {
          clearInterval(pollRef.current!);
          pollRef.current = null;
          if (j.status === "completed") toastOk("Scan complete");
          else toastErr("Scan failed");
        }
      } catch { /* network blip */ }
    }, 4000);
  }, [toastOk, toastErr]);

  useEffect(() => () => { if (pollRef.current) clearInterval(pollRef.current); }, []);

  const ucObj       = useCases.find((u) => u.use_case_id === selectedUc);
  const idleProbes  = probes.filter((p) => p.online && !p.current_job_id);

  async function launch() {
    if (!selectedUc)  { toastErr("Select a use-case"); return; }
    if (!selectedEng) { toastErr("Select an engagement"); return; }

    const targetList = targets.split(/[\s,\n]+/).map((t) => t.trim()).filter(Boolean);
    setLaunching(true);
    setJob(null);
    try {
      const res = await apiFetch<{ job_id: string; status: string }>("/api/scan/launch", {
        method: "POST",
        body: JSON.stringify({ engagement_id: selectedEng, use_case_id: selectedUc, targets: targetList.length ? targetList : undefined }),
      });
      const newJob: JobStatus = {
        job_id: res.job_id, engagement_id: selectedEng,
        status: "pending", created_at: new Date().toISOString(),
        started_at: null, completed_at: null,
        agent_id: null, agent_name: null,
        use_case_id: selectedUc, result: null,
      };
      setJob(newJob);
      startPolling(res.job_id);
      toastOk("Job queued", "Probe picks up on next poll (~10s)");
    } catch (e) {
      toastErr("Launch failed", (e as Error).message);
    } finally {
      setLaunching(false);
    }
  }

  // group by category
  const byCat: Record<string, UseCase[]> = {};
  for (const uc of useCases) {
    const cat = UC_META[uc.use_case_id]?.cat ?? "Other";
    (byCat[cat] ??= []).push(uc);
  }

  const canLaunch = !!selectedUc && !!selectedEng && !launching;

  return (
    <PageShell title="Scanner" subtitle="Dispatch scan jobs to field-deployed probes">
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}.spin{animation:spin 1s linear infinite}`}</style>

      <div style={{ display: "flex", flexDirection: "column", gap: 22, maxWidth: 1100 }}>

        {/* ── Probe health ── */}
        <section>
          <div style={{ fontSize: 11, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.3, textTransform: "uppercase", marginBottom: 8 }}>Registered Probes</div>
          {loadingData ? <div style={{ fontSize: 12, color: "var(--text-muted)" }}>Loading...</div> : <ProbeBar probes={probes} />}
        </section>

        {/* ── Two-column layout ── */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 310px", gap: 18, alignItems: "start" }}>

          {/* Left: use-case picker */}
          <section>
            <div style={{ fontSize: 11, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.3, textTransform: "uppercase", marginBottom: 12 }}>Select Use-Case</div>
            {loadingData ? (
              <div style={{ fontSize: 12, color: "var(--text-muted)" }}>Loading use-cases...</div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                {CATS.map((cat) => {
                  const items = byCat[cat] ?? [];
                  if (!items.length) return null;
                  const open = expandedCat === cat;
                  const hasSelected = items.some((u) => u.use_case_id === selectedUc);
                  return (
                    <div key={cat} style={{ borderRadius: 10, border: "0.5px solid var(--border-subtle)", overflow: "hidden" }}>
                      <button
                        onClick={() => setExpandedCat(open ? "" : cat)}
                        style={{ width: "100%", textAlign: "left", cursor: "pointer", padding: "10px 14px", background: "var(--bg-surface)", border: "none", display: "flex", alignItems: "center", gap: 8 }}
                      >
                        <span style={{ fontWeight: 700, fontSize: 12, color: "var(--text-primary)" }}>{cat}</span>
                        <span style={{ fontSize: 11, color: "var(--text-muted)" }}>{items.length} scan{items.length !== 1 ? "s" : ""}</span>
                        {hasSelected && <span style={{ fontSize: 10, fontWeight: 700, color: "var(--accent)", background: "var(--accent-ghost)", borderRadius: 4, padding: "1px 6px" }}>SELECTED</span>}
                        {open ? <ChevronDown size={13} color="var(--text-muted)" style={{ marginLeft: "auto" }} /> : <ChevronRight size={13} color="var(--text-muted)" style={{ marginLeft: "auto" }} />}
                      </button>
                      {open && (
                        <div style={{ padding: "8px 10px 10px", background: "var(--bg-card)", borderTop: "0.5px solid var(--border-subtle)", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                          {items.map((uc) => (
                            <UseCaseCard key={uc.use_case_id} uc={uc} selected={selectedUc === uc.use_case_id} onClick={() => setSelectedUc(uc.use_case_id)} />
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          {/* Right: config + launch */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12, position: "sticky", top: 16 }}>

            {/* Selected summary */}
            {ucObj ? (
              <div style={{ padding: "12px 14px", borderRadius: 10, background: "var(--accent-ghost)", border: "1px solid var(--border-accent)" }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: "var(--accent)", textTransform: "uppercase", letterSpacing: 1, marginBottom: 5 }}>Selected</div>
                <div style={{ fontWeight: 600, fontSize: 13, color: "var(--text-primary)" }}>{ucObj.display_name}</div>
                <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "var(--text-muted)", marginTop: 4 }}>
                  {ucObj.scan_type} · {ucObj.profile.toUpperCase()} profile · ~{ucObj.expected_runtime_hint}
                </div>
              </div>
            ) : (
              <div style={{ padding: "12px 14px", borderRadius: 10, background: "var(--bg-surface)", border: "0.5px dashed var(--border-subtle)", textAlign: "center", fontSize: 12, color: "var(--text-muted)" }}>
                Select a use-case from the left
              </div>
            )}

            {/* Engagement */}
            <div>
              <label style={{ fontSize: 11, fontWeight: 600, color: "var(--text-secondary)", display: "block", marginBottom: 5, textTransform: "uppercase", letterSpacing: 0.8 }}>Engagement</label>
              <select
                value={selectedEng}
                onChange={(e) => setSelectedEng(e.target.value)}
                style={{ width: "100%", padding: "8px 10px", borderRadius: 8, fontSize: 12, background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)", color: "var(--text-primary)", cursor: "pointer" }}
              >
                <option value="">— select engagement —</option>
                {engagements.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
              </select>
            </div>

            {/* Target override */}
            <div>
              <label style={{ fontSize: 11, fontWeight: 600, color: "var(--text-secondary)", display: "block", marginBottom: 5, textTransform: "uppercase", letterSpacing: 0.8 }}>
                Targets <span style={{ fontWeight: 400, color: "var(--text-muted)", textTransform: "none", letterSpacing: 0, fontSize: 10 }}>(optional — uses engagement scope if blank)</span>
              </label>
              <textarea
                value={targets}
                onChange={(e) => setTargets(e.target.value)}
                placeholder={"192.168.1.0/24\n10.0.0.0/8\n172.16.0.5"}
                rows={4}
                style={{ width: "100%", padding: "8px 10px", borderRadius: 8, background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)", color: "var(--text-primary)", fontSize: 12, fontFamily: "'JetBrains Mono', monospace", resize: "vertical", boxSizing: "border-box" }}
              />
            </div>

            {/* Probe note */}
            {probes.length > 0 && (
              <div style={{ fontSize: 11, color: "var(--text-muted)", display: "flex", alignItems: "center", gap: 5 }}>
                <span style={{ width: 6, height: 6, borderRadius: "50%", background: idleProbes.length > 0 ? "var(--sev-low-color)" : "var(--sev-critical-color)", flexShrink: 0 }} />
                {idleProbes.length > 0 ? `${idleProbes.length} idle probe${idleProbes.length > 1 ? "s" : ""} ready` : "All probes offline/busy — job will queue"}
              </div>
            )}

            {/* OT warning */}
            {ucObj?.profile === "ot" && (
              <div style={{ padding: "8px 12px", borderRadius: 8, background: "rgba(16,185,129,0.08)", border: "0.5px solid rgba(16,185,129,0.3)", fontSize: 11, color: "#10b981" }}>
                <strong>OT Safe Mode:</strong> Zero active packets — passive capture only. Safe for SCADA/ICS/PLC networks.
              </div>
            )}

            {/* Launch */}
            <button
              onClick={launch}
              disabled={!canLaunch}
              style={{ width: "100%", padding: "11px 0", borderRadius: 9, background: canLaunch ? "var(--accent)" : "var(--bg-surface)", border: "none", cursor: canLaunch ? "pointer" : "not-allowed", color: canLaunch ? "#fff" : "var(--text-muted)", fontWeight: 700, fontSize: 14, display: "flex", alignItems: "center", justifyContent: "center", gap: 8, transition: "background 0.12s" }}
            >
              {launching ? <><Loader size={14} className="spin" /> Dispatching...</> : <><Play size={14} /> Launch Scan</>}
            </button>

            {(selectedUc || selectedEng || targets) && (
              <button
                onClick={() => { setSelectedUc(""); setSelectedEng(engagements.length === 1 ? engagements[0].id : ""); setTargets(""); setJob(null); }}
                style={{ background: "none", border: "none", cursor: "pointer", fontSize: 11, color: "var(--text-muted)", display: "flex", alignItems: "center", gap: 4, padding: 0 }}
              >
                <RotateCcw size={10} /> Reset
              </button>
            )}
          </div>
        </div>

        {/* ── Active job ── */}
        {job && (
          <section>
            <div style={{ fontSize: 11, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.3, textTransform: "uppercase", marginBottom: 10 }}>
              Job Status
              {(job.status === "pending" || job.status === "running") && (
                <span style={{ marginLeft: 8, fontSize: 10, color: "var(--accent)" }}>
                  <Loader size={9} className="spin" style={{ display: "inline", verticalAlign: "middle" }} /> polling every 4s
                </span>
              )}
            </div>
            <JobPanel job={job} ucName={ucObj?.display_name} />
          </section>
        )}

        {/* ── Legend ── */}
        <section>
          <div style={{ fontSize: 11, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.3, textTransform: "uppercase", marginBottom: 12 }}>
            Scanner Profiles &amp; Scan Types
          </div>

          {/* Profile cards */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 10, marginBottom: 12 }}>
            {([
              { badge: "IT",  badgeColor: "var(--accent)", title: "IT Profile",       desc: "Standard enterprise IT network. 34-port sweep covering web, TLS, SMB, databases, SSH, RDP, LDAP, email services.", ports: "21-22, 25, 53, 80, 139, 389, 443, 445, 1433, 3306, 3389, 5432, 8080, 9200…", branches: ["TLS deep scan","Web app scan","SMB enum","DB fingerprint","UDP probe","AI endpoint"] },
              { badge: "IoT", badgeColor: "#f59e0b",        title: "IoT Profile",      desc: "IoT and embedded device discovery using protocol-aware port list targeting MQTT, RTSP, CoAP, Modbus-adjacent ports.", ports: "22-23, 80, 443, 554 (RTSP), 1883 (MQTT), 5683 (CoAP), 8883, 9100, 37777…", branches: ["TLS surface","Web panel scan"] },
              { badge: "OT",  badgeColor: "#10b981",        title: "OT/ICS Profile",   desc: "Operational Technology — PASSIVE ONLY. Zero active packets. Structurally enforced; cannot be overridden per job.", ports: "No active probing. Passive traffic capture only.", branches: ["Passive collection"] },
            ] as { badge: string; badgeColor: string; title: string; desc: string; ports: string; branches: string[] }[]).map(({ badge, badgeColor, title, desc, ports, branches }) => (
              <div key={badge} style={{ padding: 14, borderRadius: 10, background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 7, marginBottom: 8 }}>
                  <span style={{ fontWeight: 700, fontSize: 11, color: badgeColor, background: `${badgeColor}18`, border: `0.5px solid ${badgeColor}40`, borderRadius: 5, padding: "2px 7px" }}>{badge}</span>
                  <span style={{ fontWeight: 600, fontSize: 12, color: "var(--text-primary)" }}>{title}</span>
                </div>
                <p style={{ margin: "0 0 8px", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.5 }}>{desc}</p>
                <div style={{ fontSize: 10, fontFamily: "'JetBrains Mono', monospace", color: "var(--text-muted)", marginBottom: 8 }}>{ports}</div>
                <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
                  {branches.map((b) => <span key={b} style={{ fontSize: 10, color: "var(--text-secondary)", background: "var(--bg-card)", border: "0.5px solid var(--border-subtle)", borderRadius: 4, padding: "1px 5px" }}>{b}</span>)}
                </div>
              </div>
            ))}
          </div>

          {/* Scan-type table */}
          <div style={{ borderRadius: 10, border: "0.5px solid var(--border-subtle)", overflow: "hidden" }}>
            <div style={{ padding: "8px 14px", background: "var(--bg-surface)", borderBottom: "0.5px solid var(--border-subtle)", fontSize: 11, fontWeight: 700, color: "var(--text-secondary)", textTransform: "uppercase", letterSpacing: 0.8 }}>
              Available Scan Types
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "150px 1fr 60px" }}>
              {([
                ["discovery",         "Host liveness + port sweep (triage mode). Fastest scan — no deep service analysis. Uses profile port list.",           "IT/IoT"],
                ["assessment",        "Full funnel: discovery → ports → banners → all service branches (TLS, web, SMB, DB, UDP, AI endpoints).",              "IT"],
                ["tls_scan",          "TLS/HTTPS surface: cert chain, cipher suites, protocol versions, HSTS header, OCSP stapling.",                         "IT"],
                ["web_scan",          "HTTP layer: request methods, response headers, server/framework fingerprinting, common web misconfigurations.",          "IT"],
                ["db_fingerprint",    "Protocol handshake on DB ports: MySQL 3306, PostgreSQL 5432, MSSQL 1433, Redis 6379, MongoDB 27017, Oracle 1521.",     "IT"],
                ["smb_enum",          "SMB dialect negotiation, message signing check, null session attempt, exposed share enumeration.",                      "IT"],
                ["udp_scan",          "UDP attack surface: DNS (53), SNMP community strings (161), NTP monlist (123), NetBIOS (137).",                        "IT"],
                ["mcp_discovery",     "AI inference and MCP server discovery: Ollama (11434), Gradio (7860), LMStudio (1234), vLLM (8000), OpenWebUI…",      "IT"],
                ["passive_discovery", "Zero active packets. Passive traffic capture on the wire. OT/ICS structurally safe.",                                   "OT"],
              ] as [string, string, string][]).map(([type, desc, profile], i) => (
                <React.Fragment key={type}>
                  <div style={{ padding: "9px 14px", background: i % 2 === 0 ? "var(--bg-card)" : "var(--bg-surface)", borderBottom: "0.5px solid var(--border-subtle)", fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "var(--accent)" }}>{type}</div>
                  <div style={{ padding: "9px 14px", background: i % 2 === 0 ? "var(--bg-card)" : "var(--bg-surface)", borderBottom: "0.5px solid var(--border-subtle)", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4 }}>{desc}</div>
                  <div style={{ padding: "9px 14px", background: i % 2 === 0 ? "var(--bg-card)" : "var(--bg-surface)", borderBottom: "0.5px solid var(--border-subtle)", fontSize: 10, color: "var(--text-muted)", textAlign: "center" }}>{profile}</div>
                </React.Fragment>
              ))}
            </div>
          </div>
        </section>

      </div>
    </PageShell>
  );
}
