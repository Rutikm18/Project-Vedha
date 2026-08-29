"use client";

/**
 * CampaignProgress — the VA Campaigns live view for one engagement.
 *
 * Drop into app/campaign/[id]/page.tsx:  <CampaignProgress engagementId={id} />
 *
 * Renders, from GET /api/engagements/{id}/campaign-progress:
 *   • per-probe job cards (status + a SAFE raw-result summary — scanners, ports, facts)
 *   • the full pipeline ticker: Scanning → Aggregating → Detection → Correlation
 *     → Prioritization → Remediation, with a 0–100% bar
 *   • findings with step-by-step remediation guidance
 * Polls every 4s while anything is still running; stops when detection is done.
 */
import { useCallback, useEffect, useState } from "react";
import RawFacts from "./RawFacts";

type PhaseState = "done" | "active" | "pending";
interface Phase { name: string; status: PhaseState; count: number | null }
interface JobSummary {
  scanners?: string[]; scanner_count?: number; fact_count?: number | null;
  open_ports?: number | null; profile?: string | null; ok?: boolean | null;
}
interface Job {
  id: string; use_case_id: string | null; job_type: string; status: string;
  phase: string; agent_name: string | null; result_summary: JobSummary;
  created_at: string | null; started_at: string | null; completed_at: string | null;
}
interface Finding {
  id: string; title: string; severity: string; risk_score: number | null;
  cve_ids: string[] | null; mitre_techniques: string[] | null; state: string;
  remediation: string | null;
}
interface Progress {
  engagement_id: string;
  engagement?: { name: string | null; status: string };
  overall_status: string;
  is_complete: boolean;
  jobs: Job[];
  job_stats?: { total: number; running: number; complete: number; failed: number; probes: string[] };
  detection: { status: string; facts_count: number; findings_new: number;
    findings_current: number; by_severity: Record<string, number> };
  summary?: { total_findings: number; by_severity: Record<string, number>;
    max_risk_score: number; exploitable: number; actionable: number;
    top_techniques: { technique: string; count: number }[] };
  phases: Phase[];
  percent: number;
  findings: Finding[];
}

const STATUS_LABEL: Record<string, string> = {
  pending: "Pending", scanning: "Scanning", aggregating: "Aggregating",
  detecting: "Detecting", complete: "Complete", error: "Error",
};

const PHASE_LABEL: Record<string, string> = {
  scanning: "Scanning", aggregating: "Aggregating", detection: "Detection",
  correlation: "Correlation", prioritization: "Prioritization", remediation: "Remediation",
};
const SEV_COLOR: Record<string, string> = {
  critical: "var(--sev-critical, #ef4444)", high: "var(--sev-high, #f97316)",
  medium: "var(--sev-medium, #eab308)", low: "var(--sev-low, #3b82f6)",
  info: "var(--text-muted)",
};

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(path, { credentials: "same-origin" });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error ?? res.statusText);
  return body as T;
}

/** Split a remediation string into ordered, human steps (numbered / sentence-based). */
function remediationSteps(text: string | null): string[] {
  if (!text) return [];
  const byLine = text.split(/\r?\n|(?:^|\s)\d+[.)]\s+/).map((s) => s.trim()).filter(Boolean);
  if (byLine.length > 1) return byLine;
  return text.split(/(?<=[.;])\s+(?=[A-Z(])/).map((s) => s.trim()).filter(Boolean);
}

export default function CampaignProgress({ engagementId }: { engagementId: string }) {
  const [data, setData] = useState<Progress | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [open, setOpen] = useState<Record<string, boolean>>({});

  const load = useCallback(async () => {
    try {
      setData(await fetchJson<Progress>(`/api/engagements/${engagementId}/campaign-progress`));
    } catch (e) { setErr((e as Error).message); }
  }, [engagementId]);

  useEffect(() => {
    void load();
    // Keep polling until the WHOLE pipeline is complete — not just the scan job.
    if (data?.is_complete) return;
    const t = setInterval(load, 4000);
    return () => clearInterval(t);
  }, [load, data?.is_complete]);

  if (err) return <div style={{ color: "var(--sev-high,#f97316)", fontSize: 12 }}>Failed to load campaign: {err}</div>;
  if (!data) return <div style={{ color: "var(--text-muted)", fontSize: 12 }}>Loading campaign…</div>;

  const statusColor = data.is_complete ? "var(--sev-low,#3b82f6)"
    : data.overall_status === "error" ? "var(--sev-high,#f97316)" : "var(--accent)";
  const s = data.summary;

  return (
    <section style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      {/* ── high-level exec band: authoritative status + risk rollup ── */}
      <div style={{ display: "flex", alignItems: "center", gap: 14, flexWrap: "wrap",
        padding: "12px 16px", borderRadius: 12, border: "0.5px solid var(--border-accent)",
        background: "var(--bg-panel)", boxShadow: "var(--shadow-md)" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ width: 9, height: 9, borderRadius: "50%", background: statusColor,
            animation: data.is_complete ? "none" : "pulse 1.4s infinite" }} />
          <strong style={{ fontSize: 13, color: "var(--text-primary)" }}>
            {STATUS_LABEL[data.overall_status] ?? data.overall_status}
          </strong>
          {/* the fix: "Complete" appears ONLY when the whole pipeline is done */}
          {!data.is_complete && <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>· in progress ({data.percent}%)</span>}
        </span>
        {data.engagement?.name && <span style={{ fontSize: 11.5, color: "var(--text-secondary)" }}>{data.engagement.name}</span>}
        {data.job_stats && (
          <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
            {data.job_stats.probes.length || 0} probe(s) · {data.job_stats.running} running · {data.job_stats.complete}/{data.job_stats.total} jobs done
          </span>
        )}
        {s && (
          <span style={{ marginLeft: "auto", display: "flex", gap: 12, alignItems: "center" }}>
            <span style={{ fontSize: 11, color: "var(--text-muted)" }}><strong style={{ color: "var(--text-primary)" }}>{s.total_findings}</strong> findings</span>
            {s.actionable > 0 && <span style={{ fontSize: 11, color: "var(--text-muted)" }}><strong style={{ color: "var(--accent)" }}>{s.actionable}</strong> actionable</span>}
            {s.exploitable > 0 && <span style={{ fontSize: 11, color: "var(--sev-critical,#ef4444)" }}><strong>{s.exploitable}</strong> exploitable</span>}
            {s.max_risk_score > 0 && <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-muted)" }}>max risk {Math.round(s.max_risk_score)}</span>}
          </span>
        )}
      </div>

      {/* ── pipeline ticker + progress bar ── */}
      <div style={{ borderRadius: 12, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", overflow: "hidden", boxShadow: "var(--shadow-md)" }}>
        <div style={{ padding: "13px 16px", display: "flex", alignItems: "center", gap: 11, borderBottom: "0.5px solid var(--border-subtle)" }}>
          <span style={{ fontSize: 12.5, fontWeight: 700, color: "var(--text-primary)" }}>Detection pipeline</span>
          <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-muted)" }}>{data.percent}%</span>
        </div>
        {/* 0–100% bar */}
        <div style={{ height: 4, background: "var(--border-subtle)" }}>
          <div style={{ height: "100%", width: `${data.percent}%`, background: "var(--accent)", transition: "width var(--dur-slow,.6s)" }} />
        </div>
        {/* phase ticker */}
        <div style={{ display: "flex", alignItems: "center", padding: "12px 16px", gap: 4, flexWrap: "wrap" }}>
          {data.phases.map((p, i) => (
            <span key={p.name} style={{ display: "flex", alignItems: "center", gap: 4 }}>
              <span style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4, minWidth: 74 }}>
                <span style={{ width: 9, height: 9, borderRadius: "50%",
                  background: p.status === "done" ? "var(--accent)" : p.status === "active" ? "var(--accent)" : "var(--border-accent)",
                  boxShadow: p.status === "active" ? "0 0 0 3px var(--accent-ghost)" : "none",
                  animation: p.status === "active" ? "pulse 1.4s infinite" : "none" }} />
                <span style={{ fontSize: 10, fontWeight: 600, color: p.status === "pending" ? "var(--text-faint)" : "var(--text-secondary)" }}>
                  {PHASE_LABEL[p.name] ?? p.name}{p.count != null ? ` · ${p.count}` : ""}
                </span>
              </span>
              {i < data.phases.length - 1 && (
                <span style={{ width: 22, height: 1, background: p.status === "done" ? "var(--accent)" : "var(--border-subtle)" }} />
              )}
            </span>
          ))}
        </div>
        {/* severity rollup */}
        <div style={{ display: "flex", gap: 12, padding: "8px 16px 12px", borderTop: "0.5px solid var(--border-subtle)", flexWrap: "wrap" }}>
          {(["critical", "high", "medium", "low", "info"] as const).map((s) => (
            <span key={s} style={{ fontSize: 11, color: "var(--text-muted)" }}>
              <strong style={{ color: SEV_COLOR[s] }}>{data.detection.by_severity[s] ?? 0}</strong> {s}
            </span>
          ))}
        </div>
      </div>

      {/* ── per-probe jobs ── */}
      <div>
        <div style={{ fontSize: 10.5, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.4, textTransform: "uppercase", marginBottom: 10 }}>Jobs ({data.jobs.length})</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {data.jobs.map((j) => (
            <div key={j.id} style={{ borderRadius: 12, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", padding: "12px 16px", boxShadow: "var(--shadow-md)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                <span style={{ fontSize: 12.5, fontWeight: 700, color: "var(--text-primary)", fontFamily: "var(--font-display)" }}>{j.use_case_id ?? j.job_type}</span>
                <span style={{ fontSize: 10.5, fontFamily: "var(--font-mono)", padding: "2px 8px", borderRadius: 6, background: "var(--accent-ghost)", color: "var(--accent)", textTransform: "capitalize" }}>{j.phase}</span>
                {j.agent_name && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>vedha-agent <strong style={{ color: "var(--text-secondary)" }}>{j.agent_name}</strong></span>}
                <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-faint)" }}>{j.id.slice(0, 8)}</span>
              </div>
              {/* SAFE raw-result summary */}
              <div style={{ display: "flex", gap: 14, marginTop: 8, flexWrap: "wrap", fontSize: 11, color: "var(--text-muted)" }}>
                {j.result_summary?.scanner_count != null && <span><strong style={{ color: "var(--text-secondary)" }}>{j.result_summary.scanner_count}</strong> scanners</span>}
                {j.result_summary?.fact_count != null && <span><strong style={{ color: "var(--text-secondary)" }}>{j.result_summary.fact_count}</strong> facts</span>}
                {j.result_summary?.profile && <span>profile <strong style={{ color: "var(--text-secondary)" }}>{j.result_summary.profile}</strong></span>}
                {j.result_summary?.scanners?.length ? <span style={{ fontFamily: "var(--font-mono)", color: "var(--text-faint)" }}>{j.result_summary.scanners.join(" · ")}</span> : null}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── findings + step-by-step remediation ── */}
      <div>
        <div style={{ fontSize: 10.5, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.4, textTransform: "uppercase", marginBottom: 10 }}>Findings & Remediation ({data.findings.length})</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {data.findings.length === 0 && <div style={{ fontSize: 12, color: "var(--text-muted)" }}>No findings yet — {data.is_complete ? "clean against the current rules." : "detection in progress."}</div>}
          {data.findings.map((f) => {
            const steps = remediationSteps(f.remediation);
            const isOpen = open[f.id];
            return (
              <div key={f.id} style={{ borderRadius: 10, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", overflow: "hidden" }}>
                <button onClick={() => setOpen((o) => ({ ...o, [f.id]: !o[f.id] }))}
                  style={{ width: "100%", display: "flex", alignItems: "center", gap: 9, padding: "10px 14px", cursor: "pointer", background: "transparent", border: "none", textAlign: "left" }}>
                  <span style={{ width: 8, height: 8, borderRadius: "50%", background: SEV_COLOR[f.severity], flexShrink: 0 }} />
                  <span style={{ fontSize: 12.5, fontWeight: 600, color: "var(--text-primary)" }}>{f.title}</span>
                  {f.mitre_techniques?.length ? <span style={{ fontSize: 10, fontFamily: "var(--font-mono)", color: "var(--text-faint)" }}>{f.mitre_techniques.join(", ")}</span> : null}
                  <span style={{ marginLeft: "auto", fontSize: 10.5, fontFamily: "var(--font-mono)", color: "var(--text-muted)" }}>
                    {f.severity}{f.risk_score != null ? ` · risk ${Math.round(f.risk_score)}` : ""}{f.state === "confirmed" ? " · confirmed" : ""}
                  </span>
                </button>
                {isOpen && (
                  <div style={{ padding: "0 14px 14px 31px" }}>
                    {steps.length ? (
                      <ol style={{ margin: 0, paddingLeft: 16, display: "flex", flexDirection: "column", gap: 6 }}>
                        {steps.map((s, i) => <li key={i} style={{ fontSize: 11.5, color: "var(--text-secondary)", lineHeight: 1.5 }}>{s}</li>)}
                      </ol>
                    ) : <span style={{ fontSize: 11.5, color: "var(--text-muted)" }}>No remediation guidance recorded.</span>}
                    {f.cve_ids?.length ? <div style={{ marginTop: 8, fontSize: 10.5, fontFamily: "var(--font-mono)", color: "var(--text-faint)" }}>{f.cve_ids.join(", ")}</div> : null}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* ── raw scanner evidence (the facts the vedha-agent actually collected) ── */}
      <RawFacts engagementId={engagementId} />
    </section>
  );
}
