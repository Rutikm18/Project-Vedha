"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { Activity, CheckCircle2, ChevronRight, Loader2, Radar, RefreshCw, Target } from "lucide-react";
import { PageShell } from "../../components/PageShell";
import FleetJobs from "../fleet/FleetJobs";
import CampaignProgress from "./[id]/CampaignProgress";

interface CampaignSummary {
  campaign_id: string; targets: string[]; status: "running" | "completed";
  percent: number; current_stage: string | null;
  started_at: string; updated_at: string; stage_count: number;
}

interface EngagementSummary {
  id: string;
  name: string;
  client?: string;
  status: string;
  progress?: number;
  findingCount?: number;
}

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(path, { credentials: "same-origin", headers: { "Content-Type": "application/json" } });
  const body = await res.json().catch(() => ([]));
  if (!res.ok) throw new Error((body as { error?: string }).error ?? res.statusText);
  return body as T;
}

function ago(iso: string): string {
  if (!iso) return "—";
  const s = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 1000));
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return `${Math.floor(s / 86400)}d ago`;
}

export default function CampaignListPage() {
  const [rows, setRows] = useState<CampaignSummary[]>([]);
  const [engagements, setEngagements] = useState<EngagementSummary[]>([]);
  const [selectedEngagement, setSelectedEngagement] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const [campaignRows, engagementData] = await Promise.all([
        fetchJson<CampaignSummary[]>("/api/scan/campaigns"),
        fetchJson<{ engagements?: EngagementSummary[] }>("/api/engagements"),
      ]);
      const nextEngagements = engagementData.engagements ?? [];
      setRows(campaignRows);
      setEngagements(nextEngagements);
      setSelectedEngagement((current) => current || nextEngagements.find((item) => item.status === "ACTIVE")?.id || nextEngagements[0]?.id || "");
    } catch { /* keep prior rows on a transient failure */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- mount fetch + 5s poll; setState runs after an await
    void load();
    const t = window.setInterval(() => void load(), 5000);
    return () => window.clearInterval(t);
  }, [load]);

  const running = rows.filter((r) => r.status === "running").length;

  return (
    <PageShell
      title="VA Campaigns"
      subtitle="Sequential, full-network vulnerability-assessment runs"
      statusItems={[
        { label: "Total", value: String(rows.length), color: "var(--text-secondary)" },
        { label: "Running", value: String(running), color: running ? "var(--accent)" : "var(--text-faint)" },
      ]}
      headerActions={
        <div style={{ display: "flex", gap: 8 }}>
          <Link href="/scan" className="cmpl-primary"><Radar size={14} /> Launch campaign</Link>
          <button className="cmpl-refresh" onClick={() => void load()} aria-label="Refresh campaigns">
            <RefreshCw size={14} /> Refresh
          </button>
        </div>
      }
    >
      <style>{STYLES}</style>
      <div className="cmpl-page">
        <section className="cmpl-section">
          <header className="cmpl-section-head">
            <div><Activity size={15} /><div><strong>Engagement pipeline</strong><span>Jobs, detection, correlation, prioritization, and remediation</span></div></div>
            <select value={selectedEngagement} onChange={(event) => setSelectedEngagement(event.target.value)} aria-label="Select engagement pipeline">
              <option value="">Select an engagement</option>
              {engagements.map((engagement) => (
                <option value={engagement.id} key={engagement.id}>{engagement.name} · {engagement.status.toLowerCase()}</option>
              ))}
            </select>
          </header>
          {selectedEngagement ? (
            <CampaignProgress engagementId={selectedEngagement} />
          ) : (
            <div className="cmpl-inline-empty">Create or select an engagement to inspect its vulnerability pipeline.</div>
          )}
        </section>

        <section className="cmpl-section cmpl-job-section">
          <header className="cmpl-section-head">
            <div><Target size={15} /><div><strong>Tenant job queue</strong><span>Every probe job, resolved to its engagement</span></div></div>
          </header>
          <FleetJobs />
        </section>

        <div className="cmpl-subhead"><Radar size={14} /><div><strong>Collector stage snapshots</strong><span>Low-level progress reported directly by vedha-agent campaigns</span></div></div>
        {loading && rows.length === 0 ? (
          <div className="cmpl-empty"><Loader2 size={16} className="cmpl-spin" /> Loading campaigns…</div>
        ) : rows.length === 0 ? (
          <div className="cmpl-empty-block">
            <Radar size={24} color="var(--text-faint)" />
            <div className="cmpl-empty-title">No campaigns yet</div>
            <div className="cmpl-empty-hint">
              Launch one from a vedha-agent — <code>python -m scanner.va_campaign 10.0.0.0/24</code> — or dispatch the{" "}
              <strong>Network Vulnerability Assessment</strong> use-case from Fleet. Live progress lands here as
              the vedha-agent reports each stage.
            </div>
          </div>
        ) : (
          <div className="cmpl-list">
            {rows.map((r) => {
              const isRun = r.status === "running";
              return (
                <Link key={r.campaign_id} href={`/campaign/${r.campaign_id}`} className="cmpl-row">
                  <span className="cmpl-status" aria-label={r.status}>
                    {isRun
                      ? <Loader2 size={16} className="cmpl-spin" color="var(--accent)" />
                      : <CheckCircle2 size={16} color="var(--nominal-color)" />}
                  </span>
                  <div className="cmpl-main">
                    <div className="cmpl-top">
                      <span className="cmpl-id">{r.campaign_id}</span>
                      <span className="cmpl-scope"><Target size={12} /> {r.targets.join(", ") || "—"}</span>
                    </div>
                    <div className="cmpl-sub">
                      {isRun
                        ? <>Running <strong>{r.current_stage ?? "…"}</strong></>
                        : <>Completed</>}
                      {" · "}updated {ago(r.updated_at)}
                    </div>
                  </div>
                  <div className="cmpl-progress">
                    <div className="cmpl-bar"><div className="cmpl-bar-fill" data-running={isRun}
                      style={{ width: `${Math.min(100, Math.max(0, r.percent))}%` }} /></div>
                    <span className="cmpl-pct">{Math.round(r.percent)}%</span>
                  </div>
                  <ChevronRight size={16} color="var(--text-faint)" />
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </PageShell>
  );
}

const STYLES = `
.cmpl-page { display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 1180px; }
.cmpl-primary { display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 650; color: #fff;
  padding: 7px 12px; border: 1px solid var(--accent); border-radius: var(--radius-md); background: var(--accent); text-decoration: none; }
.cmpl-primary:hover { background: var(--accent-dim); }
.cmpl-refresh { display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px; color: var(--text-secondary);
  padding: 6px 11px; border: 1px solid var(--border-default); border-radius: var(--radius-md); background: transparent; cursor: pointer; }
.cmpl-refresh:hover { color: var(--text-primary); background: var(--bg-hover); }
.cmpl-section { display: flex; flex-direction: column; gap: 14px; }
.cmpl-job-section { padding: 18px 20px; background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 12px; }
.cmpl-section-head, .cmpl-subhead { display: flex; align-items: center; justify-content: space-between; gap: 14px; }
.cmpl-section-head > div, .cmpl-subhead { color: var(--accent); }
.cmpl-section-head > div, .cmpl-subhead > div { display: flex; align-items: center; gap: 9px; }
.cmpl-section-head > div > div, .cmpl-subhead > div { display: flex; flex-direction: column; align-items: flex-start; gap: 1px; }
.cmpl-section-head strong, .cmpl-subhead strong { color: var(--text-primary); font-size: 14px; font-weight: 650; }
.cmpl-section-head span, .cmpl-subhead span { color: var(--text-muted); font-size: 11.5px; }
.cmpl-section-head select { min-width: 250px; padding: 8px 10px; color: var(--text-primary); background: var(--bg-panel);
  border: 1px solid var(--border-default); border-radius: 8px; font: inherit; }
.cmpl-inline-empty { padding: 24px; color: var(--text-muted); background: var(--bg-surface); border-radius: 10px; }
.cmpl-subhead { justify-content: flex-start; padding-top: 4px; }
.cmpl-empty { display: flex; align-items: center; gap: 8px; color: var(--text-muted); font-size: 13px; padding: 28px 6px; }
.cmpl-empty-block { display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; padding: 44px 24px;
  background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-lg); }
.cmpl-empty-title { font-weight: 600; color: var(--text-primary); }
.cmpl-empty-hint { font-size: 12.5px; color: var(--text-muted); max-width: 500px; line-height: 1.6; }
.cmpl-empty-hint code { font-family: var(--font-mono); font-size: 11.5px; background: var(--bg-elevated); padding: 1px 6px; border-radius: var(--radius-sm); }

.cmpl-list { display: flex; flex-direction: column; gap: 8px; }
.cmpl-row { display: flex; align-items: center; gap: 14px; padding: 14px 16px; text-decoration: none;
  background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-lg); transition: border-color .15s, background .15s; }
.cmpl-row:hover { border-color: var(--border-accent); background: var(--bg-hover); }
.cmpl-status { flex-shrink: 0; display: grid; place-items: center; }
.cmpl-main { flex: 1; min-width: 0; }
.cmpl-top { display: flex; align-items: baseline; gap: 10px; }
.cmpl-id { font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--text-primary); }
.cmpl-scope { display: inline-flex; align-items: center; gap: 4px; font-family: var(--font-mono); font-size: 11.5px; color: var(--text-muted); }
.cmpl-sub { font-size: 12px; color: var(--text-muted); margin-top: 3px; }
.cmpl-sub strong { color: var(--text-secondary); font-weight: 600; }
.cmpl-progress { display: flex; align-items: center; gap: 9px; width: 160px; flex-shrink: 0; }
.cmpl-bar { flex: 1; height: 6px; background: var(--bg-elevated); border-radius: 99px; overflow: hidden; }
.cmpl-bar-fill { height: 100%; background: var(--nominal-color); border-radius: 99px; transition: width .5s var(--ease-out); }
.cmpl-bar-fill[data-running="true"] { background: var(--accent); }
.cmpl-pct { font-family: var(--font-mono); font-size: 12px; color: var(--text-secondary); font-variant-numeric: tabular-nums; width: 34px; text-align: right; }

.cmpl-spin { animation: cmpl-spin 1s linear infinite; }
@keyframes cmpl-spin { to { transform: rotate(360deg); } }
@media (max-width: 720px) {
  .cmpl-section-head { align-items: stretch; flex-direction: column; }
  .cmpl-section-head select { width: 100%; min-width: 0; }
  .cmpl-progress { width: 120px; }
}
`;
