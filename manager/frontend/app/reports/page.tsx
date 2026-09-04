"use client";

import React, { useCallback, useMemo, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Activity, AlertTriangle, BarChart3, CheckCircle2, ChevronDown,
  ChevronRight, Copy, FileSearch, FileText, Fingerprint, Flame,
  Globe, Lock, Printer, RefreshCw, Shield, ShieldAlert, ShieldCheck,
  Sparkles, Target, Terminal, Zap,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { DataState, EmptyState, SkeletonRows } from "../../components/states/DataState";
import { fetchJson, isUnauthorized } from "../../lib/fetcher";
import {
  SEV_COLOR, SEV_PALETTE, SEVERITY_ORDER, toSeverity, riskScoreColor,
  type Severity,
} from "../../lib/severity";

// ─── Types ────────────────────────────────────────────────────────────────────

type ReportTab = "executive" | "technical" | "evidence" | "cve" | "coverage";

interface Engagement {
  id: string; name: string; client: string; status: string;
  startDate: string; endDate: string; scopeCidrs: string[];
  assessor: string; description: string; assetCount: number;
  findingCount: number; findingsBySeverity: Record<Exclude<Severity, "INFO">, number>;
}

interface EvidenceItem { label: string; content: string; type?: string; }

interface Finding {
  id: string; title: string; severity: Severity; status: string;
  affectedHost: string; discoveredAt: string; description: string;
  technicalDetails: string; evidence: EvidenceItem[];
  impact: string; remediation: Array<string | { title?: string; description?: string; step?: string }>;
  mitre: Array<{ id: string; name: string }>; cwe?: Array<{ id: string; name: string }>;
  cve?: string[]; riskScore: number; cvss: string; cvssVector?: string;
  activelyExploited: boolean; detectionCoverage: string; reproductionSteps?: string;
}

interface FindingPage { items: Finding[]; total: number; page: number; pageSize: number; pages: number; }
interface FindingSummary { total: number; criticalOpen: number; validated: number; blind: number; averageRisk: number; }
interface ActivityItem { id: string; timestamp: string; actor: string; action: string; detail: string; }
interface AiJobStatus { job_id: string; status: "queued" | "running" | "complete" | "failed"; progress?: number; stage?: string; error?: string; }
interface AiDraft { sections: Array<{ id: string; title: string; content: string; review_status: "pending" | "approved" | "rejected" }>; }

// ─── Constants ────────────────────────────────────────────────────────────────

const TABS: Array<{ id: ReportTab; label: string; icon: React.ElementType }> = [
  { id: "executive",  label: "Executive",          icon: BarChart3 },
  { id: "technical",  label: "Technical Findings", icon: FileSearch },
  { id: "evidence",   label: "Evidence Vault",     icon: Fingerprint },
  { id: "cve",        label: "CVE Intelligence",   icon: Globe },
  { id: "coverage",   label: "MITRE Coverage",     icon: ShieldCheck },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fmtDate(v?: string) {
  if (!v) return "Not recorded";
  const d = new Date(v);
  return isNaN(d.getTime()) ? "Not recorded" : new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(d);
}
function fmtDatetime(v?: string) {
  if (!v) return "—";
  const d = new Date(v);
  return isNaN(d.getTime()) ? "—" : new Intl.DateTimeFormat("en", { dateStyle: "short", timeStyle: "short" }).format(d);
}
function remText(s: Finding["remediation"][number]) {
  return typeof s === "string" ? s : s.description || s.step || s.title || "";
}
function parseCvss(v: string): number | null {
  const m = v?.match(/(\d+\.\d+)/); return m ? parseFloat(m[1]) : null;
}
function cvssColor(n: number | null) {
  if (n === null) return SEV_PALETTE.SLATE;
  if (n >= 9) return SEV_PALETTE.RED;
  if (n >= 7) return SEV_PALETTE.ORANGE;
  if (n >= 4) return SEV_PALETTE.AMBER;
  return SEV_PALETTE.STONE;
}
function parseCvssVector(v: string) {
  if (!v?.startsWith("CVSS")) return [];
  return v.split("/").slice(1).map(p => { const [k, val] = p.split(":"); return { k: k ?? p, v: val ?? "" }; });
}
const VM_LABEL: Record<string, Record<string, string>> = {
  AV: { N: "Network", A: "Adjacent", L: "Local", P: "Physical" },
  AC: { L: "Low", H: "High" }, PR: { N: "None", L: "Low", H: "High" },
  UI: { N: "None", R: "Required" }, S: { U: "Unchanged", C: "Changed" },
  C: { N: "None", L: "Low", H: "High" }, I: { N: "None", L: "Low", H: "High" },
  A: { N: "None", L: "Low", H: "High" },
};
const VM_NAME: Record<string, string> = {
  AV: "Attack Vector", AC: "Attack Complexity", PR: "Privileges Required",
  UI: "User Interaction", S: "Scope", C: "Confidentiality", I: "Integrity", A: "Availability",
};

// ─── Atoms ────────────────────────────────────────────────────────────────────

function SevBadge({ sev }: { sev: Severity }) {
  const c = SEV_COLOR[sev];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", padding: "2px 8px",
      borderRadius: 4, border: `1px solid ${c}44`, background: `${c}16`,
      color: c, fontSize: 10, fontWeight: 800, fontFamily: "var(--font-mono)",
      letterSpacing: "0.06em",
    }}>{sev}</span>
  );
}

function StatusPill({ status }: { status: string }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", padding: "2px 8px",
      borderRadius: 4, background: "var(--bg-surface)", border: "1px solid var(--border-subtle)",
      color: "var(--text-muted)", fontSize: 10, fontWeight: 700, letterSpacing: "0.04em",
    }}>{status.toUpperCase().replace(/_/g, " ")}</span>
  );
}

function CopyBtn({ text }: { text: string }) {
  const [done, setDone] = useState(false);
  const click = useCallback(() => {
    void navigator.clipboard.writeText(text).then(() => { setDone(true); setTimeout(() => setDone(false), 1400); });
  }, [text]);
  return (
    <button onClick={click} title="Copy" style={{
      display: "inline-flex", alignItems: "center", justifyContent: "center",
      width: 24, height: 24, borderRadius: 5, border: "1px solid var(--border-subtle)",
      background: "transparent", color: "var(--text-muted)", cursor: "pointer",
    }}>
      {done ? <CheckCircle2 size={11} style={{ color: "var(--nominal-color)" }} /> : <Copy size={11} />}
    </button>
  );
}

function Metric({ label, value, note, tone = "var(--accent)" }: {
  label: string; value: string | number; note: string; tone?: string;
}) {
  return (
    <div className="rpt-metric">
      <small>{label}</small>
      <strong style={{ color: tone }}>{value}</strong>
      <span>{note}</span>
    </div>
  );
}

// ─── Severity strip ───────────────────────────────────────────────────────────

function SevStrip({ eng }: { eng: Engagement }) {
  const rows = (["CRITICAL", "HIGH", "MEDIUM", "LOW"] as const).map(s => ({ s, n: eng.findingsBySeverity[s] ?? 0 }));
  const total = Math.max(1, rows.reduce((a, r) => a + r.n, 0));
  return (
    <div>
      <div style={{ display: "flex", height: 10, borderRadius: 99, overflow: "hidden", background: "var(--bg-hover)", gap: 2 }}>
        {rows.filter(r => r.n > 0).map(r => (
          <span key={r.s} title={`${r.s}: ${r.n}`} style={{ flex: `${(r.n / total) * 100}`, background: SEV_COLOR[r.s] }} />
        ))}
      </div>
      <div style={{ display: "flex", gap: 20, marginTop: 10, flexWrap: "wrap" }}>
        {rows.map(r => (
          <span key={r.s} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11, color: "var(--text-secondary)" }}>
            <i style={{ width: 7, height: 7, borderRadius: "50%", background: SEV_COLOR[r.s], display: "inline-block" }} />
            {r.s} <strong style={{ color: "var(--text-primary)" }}>{r.n}</strong>
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── CVSS vector row ──────────────────────────────────────────────────────────

function CvssVector({ vector }: { vector: string }) {
  const parts = parseCvssVector(vector);
  if (!parts.length) return null;
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
      {parts.map(({ k, v }) => (
        <span key={k} title={`${VM_NAME[k] ?? k}: ${VM_LABEL[k]?.[v] ?? v}`} style={{
          display: "inline-flex", flexDirection: "column", alignItems: "center",
          padding: "4px 8px", borderRadius: 5, background: "var(--bg-surface)",
          border: "1px solid var(--border-subtle)", minWidth: 52,
        }}>
          <span style={{ fontSize: 8, fontWeight: 800, color: "var(--text-muted)", fontFamily: "var(--font-mono)", letterSpacing: "0.06em" }}>{k}</span>
          <span style={{ fontSize: 11, fontWeight: 700, color: "var(--text-primary)", marginTop: 1 }}>{VM_LABEL[k]?.[v] ?? v}</span>
        </span>
      ))}
    </div>
  );
}

// ─── Evidence block ───────────────────────────────────────────────────────────

function EvidBlock({ item }: { item: EvidenceItem }) {
  const [open, setOpen] = useState(false);
  const long = item.content.length > 300;
  const shown = open || !long ? item.content : item.content.slice(0, 300) + "\n…";
  return (
    <div style={{ border: "1px solid #1E293B", borderRadius: 7, overflow: "hidden" }}>
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "7px 12px", background: "#0F172A", borderBottom: "1px solid #1E293B",
      }}>
        <span style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, fontWeight: 600, color: "#64748B", fontFamily: "var(--font-mono)" }}>
          <Terminal size={12} style={{ color: "#475569" }} />
          {item.label}
          {item.type && (
            <span style={{ fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 3, background: "#1E293B", color: "#64748B" }}>{item.type}</span>
          )}
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <CopyBtn text={item.content} />
          {long && (
            <button onClick={() => setOpen(!open)} style={{
              fontSize: 10, fontWeight: 700, padding: "2px 7px", borderRadius: 4,
              border: "1px solid #1E293B", background: "transparent", color: "#64748B", cursor: "pointer",
            }}>
              {open ? "Collapse" : "Expand"}
            </button>
          )}
        </div>
      </div>
      <pre style={{
        margin: 0, padding: "12px 14px", background: "#0B1120",
        fontFamily: "var(--font-mono)", fontSize: 11.5, lineHeight: 1.7,
        color: "#CBD5E1", overflowX: "auto", whiteSpace: "pre-wrap",
        wordBreak: "break-all", maxHeight: open ? "none" : 280, overflowY: open ? "visible" : "auto",
      }}>{shown}</pre>
    </div>
  );
}

// ─── Finding card ─────────────────────────────────────────────────────────────

function FindingCard({ f, idx }: { f: Finding; idx: number }) {
  const [open, setOpen] = useState(false);
  const sev = toSeverity(f.severity);
  const sevColor = SEV_COLOR[sev];
  const cvss = parseCvss(f.cvss);
  const riskCol = riskScoreColor(f.riskScore);

  return (
    <div style={{
      border: "1px solid var(--border-subtle)", borderLeft: `3px solid ${sevColor}`,
      borderRadius: 8, background: "var(--bg-panel)", overflow: "hidden",
      transition: "border-color 0.12s",
    }}>
      {/* ── Header (always visible) ── */}
      <button
        onClick={() => setOpen(!open)}
        style={{
          display: "grid", gridTemplateColumns: "28px 1fr auto 20px", gap: 12,
          alignItems: "center", width: "100%", padding: "14px 16px",
          background: "none", border: "none", cursor: "pointer", textAlign: "left",
        }}
      >
        {/* Index */}
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 800, color: "var(--text-faint)" }}>
          {String(idx + 1).padStart(2, "0")}
        </span>

        {/* Title + meta */}
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 3, fontFamily: "var(--font-mono)" }}>
            {f.id} · {f.affectedHost}
          </div>
          <div style={{ fontSize: 13.5, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1.35 }}>{f.title}</div>
        </div>

        {/* Badges */}
        <div style={{ display: "flex", alignItems: "center", gap: 6, flexShrink: 0, flexWrap: "wrap", justifyContent: "flex-end" }}>
          <SevBadge sev={sev} />
          {cvss !== null && (
            <span style={{
              fontFamily: "var(--font-mono)", fontSize: 10, fontWeight: 800,
              color: cvssColor(cvss), padding: "2px 7px", borderRadius: 4,
              border: `1px solid ${cvssColor(cvss)}44`, background: `${cvssColor(cvss)}12`,
            }}>CVSS {cvss.toFixed(1)}</span>
          )}
          <StatusPill status={f.status} />
          {f.activelyExploited && (
            <span style={{
              display: "inline-flex", alignItems: "center", gap: 3,
              fontSize: 9, fontWeight: 800, color: SEV_PALETTE.RED,
              padding: "2px 6px", borderRadius: 4, background: `${SEV_PALETTE.RED}14`,
            }}>
              <Flame size={9} /> KEV
            </span>
          )}
        </div>

        {/* Chevron */}
        {open ? <ChevronDown size={14} style={{ color: "var(--text-muted)", flexShrink: 0 }} />
               : <ChevronRight size={14} style={{ color: "var(--text-muted)", flexShrink: 0 }} />}
      </button>

      {/* ── Body (expanded) ── */}
      {open && (
        <div style={{ borderTop: "1px solid var(--border-subtle)" }}>

          {/* Metadata strip */}
          <div style={{
            display: "flex", flexWrap: "wrap", gap: 0,
            borderBottom: "1px solid var(--border-subtle)",
          }}>
            {[
              ["Affected Host", f.affectedHost],
              ["Risk Score", f.riskScore, riskCol],
              ["CVSS", cvss !== null ? cvss.toFixed(1) : "—", cvssColor(cvss)],
              ["Discovered", fmtDate(f.discoveredAt)],
              ["Detection", f.detectionCoverage],
            ].map(([label, val, col]) => (
              <div key={String(label)} style={{
                padding: "9px 14px", borderRight: "1px solid var(--border-subtle)", flexShrink: 0,
              }}>
                <div style={{ fontSize: 9, fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em", fontFamily: "var(--font-mono)" }}>{label}</div>
                <div style={{ fontSize: 12, fontWeight: 700, color: col ? String(col) : "var(--text-primary)", marginTop: 2 }}>{String(val)}</div>
              </div>
            ))}
          </div>

          <div style={{ padding: "16px" }}>

            {/* CVSS Vector */}
            {f.cvssVector && (
              <div className="fc-section">
                <div className="fc-section-label">CVSS Vector</div>
                <code style={{ display: "block", fontSize: 10.5, fontFamily: "var(--font-mono)", color: "var(--text-muted)", marginBottom: 8, wordBreak: "break-all" }}>{f.cvssVector}</code>
                <CvssVector vector={f.cvssVector} />
              </div>
            )}

            {/* Description */}
            <div className="fc-section">
              <div className="fc-section-label">Description</div>
              <div className="fc-prose">
                {(f.description || f.technicalDetails || "No description recorded.").split("\n\n").map((p, i) => <p key={i}>{p}</p>)}
              </div>
            </div>

            {/* Impact */}
            {f.impact && (
              <div className="fc-section">
                <div className="fc-section-label">Business Impact</div>
                <div className="fc-prose">
                  {f.impact.split("\n\n").map((p, i) => <p key={i}>{p}</p>)}
                </div>
              </div>
            )}

            {/* Steps to reproduce */}
            {f.reproductionSteps && (
              <div className="fc-section">
                <div className="fc-section-label">Steps to Reproduce</div>
                <EvidBlock item={{ label: "Reproduction", content: f.reproductionSteps }} />
              </div>
            )}

            {/* Evidence */}
            {f.evidence.length > 0 && (
              <div className="fc-section">
                <div className="fc-section-label">Evidence ({f.evidence.length})</div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {f.evidence.map((item, i) => <EvidBlock key={i} item={item} />)}
                </div>
              </div>
            )}

            {/* Remediation */}
            <div className="fc-section fc-section--rem">
              <div className="fc-section-label"><Shield size={11} /> Remediation</div>
              {f.remediation.length > 0 ? (
                <ol className="fc-rem-list">
                  {f.remediation.map((s, i) => { const t = remText(s); return t ? <li key={i}>{t}</li> : null; })}
                </ol>
              ) : (
                <p className="report-missing">No remediation steps recorded.</p>
              )}
            </div>

            {/* Tags row */}
            {(f.mitre.length > 0 || (f.cwe?.length ?? 0) > 0 || (f.cve?.length ?? 0) > 0) && (
              <div className="fc-section" style={{ marginBottom: 0 }}>
                <div className="fc-section-label">References</div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {f.mitre.map(t => (
                    <a key={t.id} href={`https://attack.mitre.org/techniques/${t.id.replace(".", "/")}/`}
                       target="_blank" rel="noopener noreferrer" className="rpt-chip rpt-chip--mitre" title={t.name}>
                      {t.id}
                    </a>
                  ))}
                  {f.cwe?.map(c => <span key={c.id} className="rpt-chip" title={c.name}>{c.id}</span>)}
                  {f.cve?.map(cve => (
                    <a key={cve} href={`https://nvd.nist.gov/vuln/detail/${cve}`}
                       target="_blank" rel="noopener noreferrer" className="rpt-chip rpt-chip--cve">
                      {cve}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── AI panel (compact) ───────────────────────────────────────────────────────

function AiPanel({ engId }: { engId: string }) {
  const qc = useQueryClient();
  const [jobId, setJobId] = useState<string | null>(null);
  const [showDraft, setShowDraft] = useState(false);

  const statusQ = useQuery({
    queryKey: ["ai-report-status", engId, jobId],
    queryFn: () => fetchJson<AiJobStatus>(`/api/ai/report/${engId}/status/${jobId}`),
    enabled: Boolean(jobId),
    refetchInterval: q => { const s = q.state.data?.status; return (s === "complete" || s === "failed") ? false : 2500; },
  });
  const draftQ = useQuery({
    queryKey: ["ai-report-draft", engId],
    queryFn: () => fetchJson<AiDraft>(`/api/ai/report/${engId}/draft`),
    enabled: showDraft,
  });
  const genMut = useMutation({
    mutationFn: () => fetchJson<{ job_id: string }>(`/api/ai/report/${engId}/generate`, { method: "POST" }),
    onSuccess: d => { setJobId(d.job_id); void qc.invalidateQueries({ queryKey: ["ai-report-draft", engId] }); },
  });
  const approveMut = useMutation({
    mutationFn: (sid: string) => fetchJson(`/api/ai/report/${engId}/approve`, { method: "POST", body: JSON.stringify({ section_id: sid }) }),
    onSuccess: () => void qc.invalidateQueries({ queryKey: ["ai-report-draft", engId] }),
  });

  const st = statusQ.data;
  const running = st && st.status !== "complete" && st.status !== "failed";
  const done = st?.status === "complete";
  const failed = st?.status === "failed";

  return (
    <div style={{
      border: "1px solid var(--border-default)", borderRadius: 10,
      background: "color-mix(in srgb, var(--accent) 3%, var(--bg-panel))",
      padding: "14px 16px", marginBottom: 18,
    }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
          <Sparkles size={14} style={{ color: "var(--accent)" }} />
          <span style={{ fontSize: 13, fontWeight: 700 }}>AI Report Generation</span>
          <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>Claude Sonnet · hallucination-guarded</span>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {done && (
            <button className="btn btn-secondary" style={{ fontSize: 11, padding: "5px 10px" }} onClick={() => setShowDraft(!showDraft)}>
              {showDraft ? "Hide draft" : "Review draft"}
            </button>
          )}
          {!jobId && (
            <button className="btn btn-primary" style={{ fontSize: 11, padding: "5px 12px", display: "flex", alignItems: "center", gap: 5 }}
              onClick={() => genMut.mutate()} disabled={genMut.isPending}>
              {genMut.isPending ? <RefreshCw size={11} className="spin" /> : <Zap size={11} />}
              Generate draft
            </button>
          )}
        </div>
      </div>

      {jobId && (
        <div style={{ marginTop: 12 }}>
          <div style={{ height: 3, borderRadius: 2, background: "var(--bg-surface)", overflow: "hidden", marginBottom: 6 }}>
            <div style={{
              height: "100%", borderRadius: 2, transition: "width 0.6s ease",
              background: failed ? "var(--sev-critical-color)" : done ? "var(--nominal-color)" : "var(--accent)",
              width: `${done ? 100 : failed ? 100 : (st?.progress ?? 55)}%`,
            }} />
          </div>
          <span style={{ fontSize: 11, color: "var(--text-secondary)" }}>
            {failed ? `Failed: ${st?.error ?? "Unknown error"}` : done ? "Draft ready for review" : st?.stage ?? "Processing…"}
          </span>
        </div>
      )}

      {showDraft && draftQ.data && (
        <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 10 }}>
          {draftQ.data.sections.map(s => (
            <div key={s.id} style={{
              borderRadius: 7, border: "1px solid var(--border-subtle)",
              overflow: "hidden",
              ...(s.review_status === "approved" ? { borderColor: "var(--nominal-color)" } : {}),
            }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "9px 12px", background: "var(--bg-surface)", borderBottom: "1px solid var(--border-subtle)" }}>
                <strong style={{ fontSize: 12 }}>{s.title}</strong>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{
                    fontSize: 9, fontWeight: 800, letterSpacing: "0.05em", padding: "2px 6px", borderRadius: 4,
                    color: s.review_status === "approved" ? "var(--nominal-color)" : "var(--sev-medium-color)",
                    background: s.review_status === "approved" ? "var(--nominal-bg)" : "var(--sev-medium-bg)",
                  }}>{s.review_status.toUpperCase()}</span>
                  {s.review_status === "pending" && (
                    <button className="btn btn-secondary" style={{ fontSize: 10, padding: "3px 8px" }}
                      onClick={() => approveMut.mutate(s.id)} disabled={approveMut.isPending}>Approve</button>
                  )}
                </div>
              </div>
              <div style={{ padding: "12px", fontSize: 12.5, color: "var(--text-primary)", lineHeight: 1.65 }}>
                {s.content.split("\n\n").map((p, i) => <p key={i} style={{ margin: "0 0 8px" }}>{p}</p>)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Tab: Executive ───────────────────────────────────────────────────────────

function ExecTab({ eng, findings, summary }: { eng: Engagement; findings: Finding[]; summary: FindingSummary }) {
  const crit = eng.findingsBySeverity.CRITICAL ?? 0;
  const high = eng.findingsBySeverity.HIGH ?? 0;
  const posture = crit > 0 ? "Critical risk — immediate action required"
    : high > 0 ? "Elevated risk — remediation required"
    : summary.total > 0 ? "Risk managed — address findings"
    : "No findings recorded";

  const actions = [
    crit > 0 && `Assign owners and remediation deadlines to ${crit} critical finding${crit > 1 ? "s" : ""}.`,
    summary.validated > 0 && `Prioritise ${summary.validated} exploit-validated finding${summary.validated > 1 ? "s" : ""} — confirmed attack paths exist.`,
    summary.blind > 0 && `Address ${summary.blind} detection blind spot${summary.blind > 1 ? "s" : ""} — no SOC telemetry exists for these assets.`,
    summary.total > 0 && "Retest all remediated findings and retain verification evidence before closing.",
    !summary.total && "Commission an authorised assessment before drawing any security conclusion.",
  ].filter(Boolean) as string[];

  return (
    <>
      <AiPanel engId={eng.id} />

      {/* Risk position hero */}
      <div style={{
        display: "flex", justifyContent: "space-between", alignItems: "flex-start",
        gap: 20, padding: 20, borderRadius: 10, marginBottom: 16,
        background: "linear-gradient(135deg, var(--bg-surface), var(--bg-panel))",
        border: "1px solid var(--border-subtle)",
      }}>
        <div>
          <div style={{ fontSize: 9, fontWeight: 800, color: "var(--text-muted)", letterSpacing: "0.12em", fontFamily: "var(--font-mono)", textTransform: "uppercase" }}>RISK POSITION</div>
          <h2 style={{ margin: "6px 0 8px", fontSize: 22, fontWeight: 750, color: "var(--text-primary)" }}>{posture}</h2>
          <p style={{ margin: 0, fontSize: 12, color: "var(--text-secondary)", maxWidth: 640, lineHeight: 1.6 }}>
            All metrics are derived from Vedha scanner evidence for <strong>{eng.name}</strong>. Untested assets and controls are outside this report's scope.
          </p>
        </div>
        <ShieldAlert size={28} style={{ color: "var(--sev-critical-color)", flexShrink: 0 }} />
      </div>

      {/* Metrics */}
      <div className="rpt-metrics">
        <Metric label="Total findings" value={summary.total} note="All severities" tone={SEV_PALETTE.RED} />
        <Metric label="Critical open" value={summary.criticalOpen} note="Open / confirmed" tone={SEV_PALETTE.RED} />
        <Metric label="Exploit validated" value={summary.validated} note="Evidence-backed" tone={SEV_PALETTE.ORANGE} />
        <Metric label="Avg risk score" value={summary.averageRisk} note="0–1000 composite" tone={SEV_PALETTE.VIOLET} />
      </div>

      {/* Severity distribution */}
      <div className="rpt-section">
        <div className="rpt-section-head"><small>RISK DISTRIBUTION</small><h3>Severity profile</h3></div>
        <SevStrip eng={eng} />
      </div>

      {/* Priority actions */}
      <div className="rpt-section">
        <div className="rpt-section-head"><small>DECISION QUEUE</small><h3>Priority management actions</h3></div>
        <ol style={{ margin: 0, paddingLeft: 22, display: "grid", gap: 8 }}>
          {actions.map(a => (
            <li key={a} style={{ fontSize: 12.5, color: "var(--text-primary)", lineHeight: 1.6 }}>{a}</li>
          ))}
        </ol>
      </div>

      {/* Top findings table */}
      <div className="rpt-section">
        <div className="rpt-section-head" style={{ marginBottom: 0 }}>
          <small>HIGHEST RISK</small><h3>Top findings</h3>
          <span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-muted)" }}>Top {Math.min(10, findings.length)} of {summary.total}</span>
        </div>
        {findings.length === 0 && <p className="report-missing">No findings recorded.</p>}
        <div className="report-table-wrap">
          <table className="report-table">
            <thead><tr><th>Sev</th><th>Finding</th><th>Asset</th><th>CVSS</th><th>Status</th></tr></thead>
            <tbody>
              {findings.slice(0, 10).map(f => {
                const sc = parseCvss(f.cvss);
                const sev = toSeverity(f.severity);
                return (
                  <tr key={f.id}>
                    <td><SevBadge sev={sev} /></td>
                    <td><strong>{f.title}</strong><small>{f.id}</small></td>
                    <td>{f.affectedHost}</td>
                    <td>{sc !== null ? <span style={{ color: cvssColor(sc), fontWeight: 700 }}>{sc.toFixed(1)}</span> : "—"}</td>
                    <td><StatusPill status={f.status} /></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

// ─── Tab: Technical Findings ──────────────────────────────────────────────────

function TechTab({ findings, total }: { findings: Finding[]; total: number }) {
  const [filter, setFilter] = useState<Severity | "ALL">("ALL");
  const filtered = filter === "ALL" ? findings : findings.filter(f => toSeverity(f.severity) === filter);

  return (
    <>
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 14 }}>
        <span style={{ fontSize: 11, color: "var(--text-muted)", fontWeight: 600 }}>Severity:</span>
        {(["ALL", ...SEVERITY_ORDER] as const).map(s => (
          <button key={s} onClick={() => setFilter(s as Severity | "ALL")} style={{
            padding: "4px 10px", borderRadius: 20, fontSize: 10.5, fontWeight: 700, cursor: "pointer",
            border: `1px solid ${filter === s ? (s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity]) : "var(--border-subtle)"}`,
            background: filter === s ? (s === "ALL" ? "var(--accent-ghost)" : `${SEV_COLOR[s as Severity]}14`) : "transparent",
            color: filter === s ? (s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity]) : "var(--text-muted)",
          }}>{s}</button>
        ))}
        <span style={{ marginLeft: "auto", fontSize: 11, color: "var(--text-muted)" }}>{filtered.length} / {total}</span>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {filtered.length === 0 && <p className="report-missing">No findings match the selected filter.</p>}
        {filtered.map((f, i) => <FindingCard key={f.id} f={f} idx={i} />)}
      </div>
    </>
  );
}

// ─── Tab: Evidence Vault ──────────────────────────────────────────────────────

function EvidTab({ findings, activity, total }: { findings: Finding[]; activity: ActivityItem[]; total: number }) {
  const all = findings.flatMap(f => f.evidence.map(e => ({ ...e, finding: f })));
  const withEvid = findings.filter(f => f.evidence.length > 0).length;

  return (
    <>
      <div className="rpt-metrics">
        <Metric label="Evidence artifacts" value={all.length} note={`Across ${findings.length} findings`} />
        <Metric label="With evidence" value={withEvid} note={`${findings.length - withEvid} without`} />
        <Metric label="Activity events" value={activity.length} note="Latest recorded" />
        <Metric label="Loaded / total" value={`${findings.length}/${total}`} note="Finding coverage" />
      </div>

      <div className="rpt-section">
        <div className="rpt-section-head"><small>EVIDENCE INVENTORY</small><h3>Scanner artifacts — verbatim output</h3></div>
        {all.length === 0 && <p className="report-missing">No evidence artifacts in the loaded findings.</p>}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {all.map((item, i) => (
            <div key={`${item.finding.id}-${i}`} style={{ border: "1px solid var(--border-subtle)", borderRadius: 8, overflow: "hidden" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 12px", background: "var(--bg-surface)", borderBottom: "1px solid var(--border-subtle)" }}>
                <SevBadge sev={toSeverity(item.finding.severity)} />
                <span style={{ fontSize: 11, fontFamily: "var(--font-mono)", color: "var(--text-muted)" }}>{item.finding.id}</span>
                <span style={{ fontSize: 11, color: "var(--text-muted)" }}>·</span>
                <span style={{ fontSize: 11, color: "var(--text-secondary)" }}>{item.finding.affectedHost}</span>
                <span style={{ fontSize: 11, fontWeight: 600, color: "var(--text-secondary)", marginLeft: "auto" }}>{item.finding.title}</span>
              </div>
              <EvidBlock item={item} />
            </div>
          ))}
        </div>
      </div>

      <div className="rpt-section">
        <div className="rpt-section-head"><small>AUDIT TRAIL</small><h3>Assessment activity log</h3></div>
        {activity.length === 0 && <p className="report-missing">No activity recorded for this engagement.</p>}
        <div className="report-activity">
          {activity.map(e => (
            <article key={e.id}><Activity size={13} /><div><strong>{e.action}</strong><p>{e.detail}</p></div><time>{fmtDatetime(e.timestamp)}</time></article>
          ))}
        </div>
      </div>
    </>
  );
}

// ─── Tab: CVE Intelligence ────────────────────────────────────────────────────

function CveTab({ findings, total }: { findings: Finding[]; total: number }) {
  const withCve = findings.filter(f => f.cve && f.cve.length > 0);
  const allCves = [...new Set(findings.flatMap(f => f.cve ?? []))];
  const exploited = findings.filter(f => f.activelyExploited).length;

  return (
    <>
      <div className="rpt-metrics">
        <Metric label="Unique CVEs" value={allCves.length} note="Across loaded findings" tone={SEV_PALETTE.RED} />
        <Metric label="Findings with CVEs" value={withCve.length} note={`of ${findings.length} loaded`} tone={SEV_PALETTE.ORANGE} />
        <Metric label="Actively exploited" value={exploited} note="CISA KEV confirmed" tone={SEV_PALETTE.RED} />
        <Metric label="Total findings" value={total} note="Full scope" />
      </div>

      {exploited > 0 && (
        <div style={{ display: "flex", gap: 10, alignItems: "flex-start", padding: "11px 13px", borderRadius: 8, marginBottom: 14, background: `${SEV_PALETTE.RED}10`, border: `1px solid ${SEV_PALETTE.RED}33` }}>
          <Flame size={15} style={{ color: SEV_PALETTE.RED, flexShrink: 0, marginTop: 1 }} />
          <div><strong style={{ fontSize: 11, color: "var(--text-primary)", display: "block" }}>Active exploitation detected</strong><span style={{ fontSize: 11, color: "var(--text-secondary)", marginTop: 3, display: "block", lineHeight: 1.5 }}>{exploited} finding(s) are on the CISA KEV list — treat as P0 regardless of CVSS base score.</span></div>
        </div>
      )}

      <div className="rpt-section">
        <div className="rpt-section-head"><small>CVE INTELLIGENCE</small><h3>Findings with published vulnerability IDs</h3></div>
        {withCve.length === 0 && <p className="report-missing">No CVE IDs in loaded findings. CVEs appear when Vedha maps banner/CPE data to the NVD.</p>}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {withCve.map(f => {
            const sc = parseCvss(f.cvss);
            return (
              <div key={f.id} style={{ padding: "14px", borderRadius: 8, border: "1px solid var(--border-subtle)", background: "var(--bg-panel)" }}>
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 10 }}>
                  <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
                    <SevBadge sev={toSeverity(f.severity)} />
                    <div>
                      <div style={{ fontSize: 13.5, fontWeight: 700, color: "var(--text-primary)" }}>{f.title}</div>
                      <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2, fontFamily: "var(--font-mono)" }}>{f.id} · {f.affectedHost}</div>
                    </div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
                    {sc !== null && <span style={{ fontSize: 20, fontWeight: 800, fontFamily: "var(--font-mono)", color: cvssColor(sc) }}>{sc.toFixed(1)}</span>}
                    {f.activelyExploited && <span style={{ fontSize: 9, fontWeight: 800, color: SEV_PALETTE.RED, padding: "2px 6px", borderRadius: 4, background: `${SEV_PALETTE.RED}14` }}><Flame size={9} /> KEV</span>}
                  </div>
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {f.cve!.map(cve => (
                    <a key={cve} href={`https://nvd.nist.gov/vuln/detail/${cve}`} target="_blank" rel="noopener noreferrer" className="rpt-chip rpt-chip--cve">
                      <Globe size={10} /> {cve}
                    </a>
                  ))}
                </div>
                {f.description && <p style={{ margin: "10px 0 0", fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55 }}>{f.description.slice(0, 220)}{f.description.length > 220 ? "…" : ""}</p>}
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

// ─── Tab: MITRE Coverage ─────────────────────────────────────────────────────

function CoverageTab({ findings, total }: { findings: Finding[]; total: number }) {
  const techniques = useMemo(() => {
    const map = new Map<string, { name: string; findings: Finding[] }>();
    findings.forEach(f => f.mitre.forEach(t => {
      const e = map.get(t.id) ?? { name: t.name, findings: [] };
      e.findings.push(f); map.set(t.id, e);
    }));
    return [...map.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [findings]);

  const covered = findings.filter(f => f.detectionCoverage === "COVERED").length;
  const blind = findings.filter(f => f.detectionCoverage === "BLIND").length;

  return (
    <>
      <div style={{ display: "flex", gap: 10, alignItems: "flex-start", padding: "11px 13px", borderRadius: 8, marginBottom: 14, background: "var(--sev-medium-bg)", border: "1px solid var(--border-default)" }}>
        <AlertTriangle size={15} style={{ color: "var(--sev-medium-color)", flexShrink: 0, marginTop: 1 }} />
        <div><strong style={{ fontSize: 11, color: "var(--text-primary)", display: "block" }}>MITRE ATT&amp;CK mapping only — no inferred compliance verdicts</strong><span style={{ fontSize: 11, color: "var(--text-secondary)", marginTop: 3, display: "block" }}>Formal NIST, ISO 27001, or PCI DSS compliance requires an approved scope, tested controls, and a qualified reviewer.</span></div>
      </div>
      <div className="rpt-metrics">
        <Metric label="Techniques observed" value={techniques.length} note="Linked to findings" />
        <Metric label="SOC covered" value={covered} note="Telemetry confirmed" tone={SEV_PALETTE.GREEN} />
        <Metric label="Blind spots" value={blind} note="No alerting telemetry" tone={SEV_PALETTE.RED} />
        <Metric label="Coverage" value={total > 0 ? `${Math.round((covered / total) * 100)}%` : "N/A"} note="Of total findings" />
      </div>
      <div className="rpt-section">
        <div className="rpt-section-head"><small>ATT&amp;CK MAPPING</small><h3>Observed adversary techniques</h3><span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-muted)" }}>{techniques.length} techniques · {findings.length}/{total} loaded</span></div>
        {techniques.length === 0 && <p className="report-missing">No ATT&amp;CK references in the loaded findings.</p>}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 8 }}>
          {techniques.map(([id, { name, findings: fgs }]) => {
            const worst = fgs.reduce<Severity>((w, f) => {
              const fi = SEVERITY_ORDER.indexOf(toSeverity(f.severity));
              const wi = SEVERITY_ORDER.indexOf(w);
              return fi < wi ? toSeverity(f.severity) : w;
            }, "INFO");
            return (
              <a key={id} href={`https://attack.mitre.org/techniques/${id.replace(".", "/")}/`}
                 target="_blank" rel="noopener noreferrer"
                 style={{ display: "flex", flexDirection: "column", gap: 5, padding: "10px 12px", borderRadius: 7, textDecoration: "none",
                   border: `1px solid var(--border-subtle)`, borderLeft: `3px solid ${SEV_COLOR[worst]}`,
                   background: "var(--bg-panel)", transition: "background 0.1s" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <code style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 700, color: "var(--accent)" }}>{id}</code>
                  <SevBadge sev={worst} />
                </div>
                <span style={{ fontSize: 11.5, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1.3 }}>{name || "Unnamed technique"}</span>
                <span style={{ fontSize: 10, color: "var(--text-muted)" }}>{fgs.length} finding{fgs.length !== 1 ? "s" : ""}</span>
              </a>
            );
          })}
        </div>
      </div>
    </>
  );
}

// ─── Page root ────────────────────────────────────────────────────────────────

export default function ReportsPage() {
  const [selId, setSelId] = useState("");
  const [tab, setTab] = useState<ReportTab>("executive");

  const engQ = useQuery({ queryKey: ["engagements"], queryFn: () => fetchJson<{ engagements: Engagement[] }>("/api/engagements"), retry: (c, e) => !isUnauthorized(e) && c < 2 });
  const engs = engQ.data?.engagements ?? [];
  const engId = selId || engs[0]?.id || "";
  const eng = engs.find(e => e.id === engId);

  const findQ = useQuery({ queryKey: ["rpt-findings", engId], queryFn: () => fetchJson<FindingPage>(`/api/findings?paginated=true&engagement_id=${encodeURIComponent(engId)}&page=1&page_size=100&sort=risk`), enabled: Boolean(engId), retry: (c, e) => !isUnauthorized(e) && c < 2 });
  const sumQ  = useQuery({ queryKey: ["rpt-summary",  engId], queryFn: () => fetchJson<FindingSummary>(`/api/findings/summary?engagement_id=${encodeURIComponent(engId)}`), enabled: Boolean(engId), retry: (c, e) => !isUnauthorized(e) && c < 2 });
  const actQ  = useQuery({ queryKey: ["rpt-activity", engId], queryFn: () => fetchJson<ActivityItem[]>(`/api/activity?engagement_id=${encodeURIComponent(engId)}&limit=50`), enabled: Boolean(engId), retry: (c, e) => !isUnauthorized(e) && c < 2 });

  const findings = findQ.data?.items ?? [];
  const summary: FindingSummary = sumQ.data ?? { total: eng?.findingCount ?? 0, criticalOpen: 0, validated: 0, blind: 0, averageRisk: 0 };
  const loading  = engQ.isLoading || (Boolean(engId) && (findQ.isLoading || sumQ.isLoading));
  const loadErr  = engQ.error || findQ.error || sumQ.error;

  return (
    <PageShell
      title="Reports"
      subtitle="Professional VAPT deliverables — grounded in verified scanner evidence"
      headerActions={
        <button className="btn btn-secondary no-print" onClick={() => window.print()} disabled={!eng}>
          <Printer size={14} /> Export PDF
        </button>
      }
    >
      {/* Warning banner */}
      <div className="reports-beta-banner">
        <AlertTriangle size={14} />
        <div>
          <strong>Assessment report workspace</strong>
          <span>Data is sourced from the selected engagement. Review evidence, scope, and wording before client delivery. AI-generated sections require human approval.</span>
        </div>
      </div>

      {/* Controls */}
      <div className="report-controls no-print">
        <label>
          <span>Engagement</span>
          <select value={engId} onChange={e => { setSelId(e.target.value); setTab("executive"); }}>
            {engs.map(e => <option key={e.id} value={e.id}>{e.name} · {e.client}</option>)}
          </select>
        </label>
        <div role="tablist">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button key={id} role="tab" aria-selected={tab === id} data-active={tab === id} onClick={() => setTab(id)}>
              <Icon size={13} />{label}
            </button>
          ))}
        </div>
      </div>

      <DataState
        loading={loading} error={loadErr} isEmpty={!eng}
        onRetry={() => { void engQ.refetch(); void findQ.refetch(); void sumQ.refetch(); }}
        skeleton={<SkeletonRows rows={5} height={88} />}
        empty={<EmptyState icon={FileText} title="No engagement available" hint="Create an engagement and run an assessment before generating a report." />}
      >
        {eng && (
          <main className="report-document">
            {/* Cover */}
            <header className="report-cover">
              <div>
                <span><CheckCircle2 size={13} /> LIVE DATA</span>
                <h1>{eng.name}</h1>
                <p>{eng.client} · Vulnerability Assessment &amp; Penetration Test Report</p>
              </div>
              <dl>
                <div><dt>Status</dt><dd>{eng.status}</dd></div>
                <div><dt>Assessment window</dt><dd>{fmtDate(eng.startDate)} — {fmtDate(eng.endDate)}</dd></div>
                <div><dt>Lead assessor</dt><dd>{eng.assessor || "Not recorded"}</dd></div>
                <div><dt>Scope</dt><dd>{eng.scopeCidrs.length ? eng.scopeCidrs.join(", ") : "Not recorded"}</dd></div>
                <div><dt>Assets in scope</dt><dd>{eng.assetCount}</dd></div>
                <div><dt>Total findings</dt><dd>{eng.findingCount}</dd></div>
              </dl>
            </header>

            {/* Evidence boundary notice */}
            <div className="report-boundary" style={{ marginBottom: 0 }}>
              <Lock size={15} />
              <div>
                <strong>Evidence boundary</strong>
                <span>Detailed sections load up to 100 of {summary.total} findings (ranked by risk). Aggregate metrics cover the full engagement. Missing data is stated explicitly — never inferred.</span>
              </div>
            </div>

            {/* Tab content */}
            <div style={{ padding: "20px 24px 24px" }}>
              {tab === "executive" && <ExecTab eng={eng} findings={findings} summary={summary} />}
              {tab === "technical" && <TechTab findings={findings} total={summary.total} />}
              {tab === "evidence"  && <EvidTab findings={findings} activity={actQ.data ?? []} total={summary.total} />}
              {tab === "cve"       && <CveTab findings={findings} total={summary.total} />}
              {tab === "coverage"  && <CoverageTab findings={findings} total={summary.total} />}
            </div>

            <footer className="report-footer">
              <FileText size={12} />
              Vedha VAPT Platform · {eng.name} · Human review required before delivery
            </footer>
          </main>
        )}
      </DataState>
    </PageShell>
  );
}
