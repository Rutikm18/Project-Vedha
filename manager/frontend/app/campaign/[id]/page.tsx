"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft, Boxes, CheckCircle2, CircleDashed, Clock3,
  Loader2, Network, RefreshCw, ScanLine, Server, Target, XCircle,
} from "lucide-react";
import { PageShell } from "../../../components/PageShell";

// ── snapshot contract (mirrors the probe's ProgressReporter.snapshot) ──────────
type StageStatus = "pending" | "running" | "done" | "skipped" | "error";
interface StageSnapshot {
  id: string; name: string; detail: string; status: StageStatus;
  started_at: string | null; ended_at: string | null; count: number; note: string;
}
interface CampaignSnapshot {
  campaign_id: string; targets: string[]; status: "running" | "completed";
  started_at: string; updated_at: string; percent: number;
  current_stage: string | null; eta_seconds: number | null;
  stages: StageSnapshot[];
  totals: { live_hosts?: number; open_ports?: number; facts?: number };
}

// Stage status → color + icon. Never color-only: the status word + an aria-label
// always accompany the dot (a11y — matches the Fleet page's convention).
function stageBadge(status: StageStatus): { color: string; Icon: typeof CheckCircle2; spin?: boolean; word: string } {
  switch (status) {
    case "running": return { color: "var(--accent)", Icon: Loader2, spin: true, word: "running" };
    case "done":    return { color: "var(--nominal-color)", Icon: CheckCircle2, word: "done" };
    case "error":   return { color: "var(--sev-high-color)", Icon: XCircle, word: "error" };
    case "skipped": return { color: "var(--text-faint)", Icon: CircleDashed, word: "skipped" };
    default:        return { color: "var(--text-faint)", Icon: Clock3, word: "waiting" };
  }
}

function fmtEta(seconds: number | null): string {
  if (seconds == null || seconds <= 0) return "—";
  if (seconds < 60) return `~${Math.round(seconds)}s`;
  if (seconds < 3600) return `~${Math.round(seconds / 60)}m`;
  return `~${(seconds / 3600).toFixed(1)}h`;
}

function fmtDuration(start: string | null, end: string | null): string {
  if (!start) return "";
  const a = new Date(start).getTime();
  const b = end ? new Date(end).getTime() : Date.now();
  const s = Math.max(0, Math.round((b - a) / 1000));
  if (s < 60) return `${s}s`;
  if (s < 3600) return `${Math.floor(s / 60)}m ${s % 60}s`;
  return `${Math.floor(s / 3600)}h ${Math.floor((s % 3600) / 60)}m`;
}

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(path, { credentials: "same-origin", headers: { "Content-Type": "application/json" } });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error ?? res.statusText);
  return body as T;
}

export default function CampaignDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [snap, setSnap] = useState<CampaignSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!id) return;
    try {
      const data = await fetchJson<CampaignSnapshot>(`/api/scan/campaigns/${id}`);
      setSnap(data);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load campaign");
    } finally {
      setLoading(false);
    }
  }, [id]);

  // Poll every 3s while the campaign is still running; stop once it completes.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- mount fetch + poll; setState runs after an await, not synchronously
    void load();
    const t = window.setInterval(() => {
      setSnap((cur) => { if (cur?.status === "completed") return cur; void load(); return cur; });
    }, 3000);
    return () => window.clearInterval(t);
  }, [load]);

  const done = snap ? snap.stages.filter((s) => s.status === "done" || s.status === "skipped").length : 0;
  const total = snap?.stages.length ?? 0;
  const isRunning = snap?.status === "running";

  const statusItems = snap
    ? [
        { label: "Status", value: snap.status, color: isRunning ? "var(--accent)" : "var(--nominal-color)" },
        { label: "Stages", value: `${done}/${total}`, color: "var(--text-secondary)" },
        { label: "ETA", value: isRunning ? fmtEta(snap.eta_seconds) : "done", color: "var(--text-secondary)" },
      ]
    : undefined;

  return (
    <PageShell
      hideRefresh
      title="VA Campaign"
      subtitle={id ? `Live progress — ${id}` : "Live progress"}
      statusItems={statusItems}
      headerActions={
        <Link href="/campaign" className="cmp-back">
          <ArrowLeft size={14} /> All campaigns
        </Link>
      }
    >
      <style>{STYLES}</style>
      <div className="cmp-page">

        {loading && !snap ? (
          <div className="cmp-empty"><Loader2 size={16} className="cmp-spin" /> Loading campaign…</div>
        ) : error && !snap ? (
          <div className="cmp-empty-block">
            <XCircle size={22} color="var(--sev-high-color)" />
            <div className="cmp-empty-title">{error}</div>
            <div className="cmp-empty-hint">
              No snapshot for <code>{id}</code> yet. A campaign appears here once the vedha-agent (or an ingest
              POST to <code>/api/scan/campaigns</code>) has reported its first progress snapshot.
            </div>
          </div>
        ) : snap ? (
          <>
            {/* ── Overall progress ── */}
            <section className="cmp-card">
              <div className="cmp-overall">
                <div className="cmp-overall-head">
                  <span className="cmp-scope">
                    <Target size={14} color="var(--accent)" />
                    {snap.targets.length ? snap.targets.join(", ") : "no targets"}
                  </span>
                  <span className="cmp-pct">{Math.round(snap.percent)}%</span>
                </div>
                <div className="cmp-bar" role="progressbar" aria-valuenow={Math.round(snap.percent)} aria-valuemin={0} aria-valuemax={100}>
                  <div className="cmp-bar-fill" data-running={isRunning} style={{ width: `${Math.min(100, Math.max(0, snap.percent))}%` }} />
                </div>
                <div className="cmp-overall-foot">
                  <span>{isRunning
                    ? <>Running <strong>{snap.current_stage ?? "…"}</strong> · ETA {fmtEta(snap.eta_seconds)}</>
                    : <>Completed in {fmtDuration(snap.started_at, snap.updated_at)}</>}
                  </span>
                  <span className="cmp-updated">updated {fmtDuration(snap.updated_at, null)} ago</span>
                </div>
              </div>

              {/* ── Live totals ── */}
              <div className="cmp-totals">
                <Totals icon={Server}  label="Live hosts" value={snap.totals.live_hosts ?? 0} />
                <Totals icon={Network} label="Open ports" value={snap.totals.open_ports ?? 0} />
                <Totals icon={Boxes}   label="Facts"      value={snap.totals.facts ?? 0} />
              </div>
            </section>

            {/* ── Stage-by-stage: what we're doing, in order ── */}
            <section className="cmp-card cmp-stages">
              <header className="cmp-stages-head">
                <ScanLine size={15} color="var(--accent)" />
                <strong>What the campaign is doing</strong>
                <button className="cmp-refresh" onClick={() => void load()} aria-label="Refresh now">
                  <RefreshCw size={13} />
                </button>
              </header>
              <ol className="cmp-stage-list">
                {snap.stages.map((s) => {
                  const b = stageBadge(s.status);
                  const active = s.status === "running";
                  return (
                    <li key={s.id} className="cmp-stage" data-active={active} data-status={s.status}>
                      <span className="cmp-stage-icon" style={{ color: b.color }} aria-label={`Stage ${b.word}`}>
                        <b.Icon size={16} className={b.spin ? "cmp-spin" : undefined} />
                      </span>
                      <div className="cmp-stage-body">
                        <div className="cmp-stage-top">
                          <span className="cmp-stage-name">{s.name}</span>
                          <span className="cmp-stage-status" style={{ color: b.color }}>{b.word}</span>
                        </div>
                        <div className="cmp-stage-detail">{s.detail}</div>
                        {(s.note || s.count > 0 || s.started_at) && (
                          <div className="cmp-stage-meta">
                            {s.count > 0 && <span className="cmp-chip">{s.count.toLocaleString()} results</span>}
                            {s.note && <span className="cmp-note">{s.note}</span>}
                            {s.started_at && s.status !== "skipped" && (
                              <span className="cmp-time"><Clock3 size={11} /> {fmtDuration(s.started_at, s.ended_at)}</span>
                            )}
                          </div>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ol>
            </section>
          </>
        ) : null}
      </div>
    </PageShell>
  );
}

function Totals({ icon: Icon, label, value }: { icon: typeof Server; label: string; value: number }) {
  return (
    <div className="cmp-total">
      <span className="cmp-total-icon"><Icon size={15} /></span>
      <div>
        <div className="cmp-total-value">{value.toLocaleString()}</div>
        <div className="cmp-total-label">{label}</div>
      </div>
    </div>
  );
}

const STYLES = `
.cmp-page { display: flex; flex-direction: column; gap: 16px; width: 100%; max-width: 1180px; margin: 0 auto; }
.cmp-back { display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px; color: var(--text-secondary);
  text-decoration: none; padding: 5px 10px; border: 1px solid var(--border-default); border-radius: var(--radius-md); }
.cmp-back:hover { color: var(--text-primary); background: var(--bg-hover); }
.cmp-card { background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-lg); padding: 18px 20px; }
.cmp-empty { display: flex; align-items: center; gap: 8px; color: var(--text-muted); font-size: 13px; padding: 28px 6px; }
.cmp-empty-block { display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; padding: 40px 24px;
  background: var(--bg-card); border: 1px solid var(--border-default); border-radius: var(--radius-lg); }
.cmp-empty-title { font-weight: 600; color: var(--text-primary); }
.cmp-empty-hint { font-size: 12.5px; color: var(--text-muted); max-width: 460px; line-height: 1.5; }
.cmp-empty-hint code { font-family: var(--font-mono); font-size: 11.5px; background: var(--bg-elevated);
  padding: 1px 5px; border-radius: var(--radius-sm); }

.cmp-overall-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.cmp-scope { display: inline-flex; align-items: center; gap: 7px; font-family: var(--font-mono); font-size: 13px; color: var(--text-primary); }
.cmp-pct { font-family: var(--font-display); font-size: 26px; font-weight: 700; color: var(--text-primary); font-variant-numeric: tabular-nums; }
.cmp-bar { height: 8px; background: var(--bg-elevated); border-radius: 99px; overflow: hidden; }
.cmp-bar-fill { height: 100%; background: var(--nominal-color); border-radius: 99px; transition: width .5s var(--ease-out); }
.cmp-bar-fill[data-running="true"] { background: var(--accent); }
.cmp-overall-foot { display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: var(--text-muted); }
.cmp-overall-foot strong { color: var(--text-secondary); font-weight: 600; }
.cmp-updated { color: var(--text-faint); }

.cmp-totals { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 16px;
  padding-top: 16px; border-top: 1px solid var(--border-subtle); }
.cmp-total { display: flex; align-items: center; gap: 10px; }
.cmp-total-icon { display: grid; place-items: center; width: 32px; height: 32px; border-radius: var(--radius-md);
  background: var(--accent-ghost, var(--bg-elevated)); color: var(--accent); }
.cmp-total-value { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--text-primary); font-variant-numeric: tabular-nums; }
.cmp-total-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .04em; }

.cmp-stages-head { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; font-size: 13.5px; color: var(--text-primary); }
.cmp-stages-head strong { font-weight: 600; }
.cmp-refresh { margin-left: auto; display: grid; place-items: center; width: 26px; height: 26px; border-radius: var(--radius-sm);
  border: 1px solid var(--border-default); background: transparent; color: var(--text-muted); cursor: pointer; }
.cmp-refresh:hover { color: var(--text-primary); background: var(--bg-hover); }

.cmp-stage-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; }
.cmp-stage { display: flex; gap: 12px; padding: 12px 10px; border-radius: var(--radius-md);
  border-left: 2px solid transparent; }
.cmp-stage + .cmp-stage { border-top: 1px solid var(--border-subtle); }
.cmp-stage[data-active="true"] { background: var(--accent-ghost, var(--bg-elevated)); border-left-color: var(--accent); }
.cmp-stage[data-status="skipped"] { opacity: .62; }
.cmp-stage-icon { flex-shrink: 0; padding-top: 1px; }
.cmp-stage-body { flex: 1; min-width: 0; }
.cmp-stage-top { display: flex; align-items: baseline; gap: 8px; }
.cmp-stage-name { font-weight: 600; font-size: 13.5px; color: var(--text-primary); }
.cmp-stage-status { margin-left: auto; font-size: 11px; text-transform: uppercase; letter-spacing: .05em; font-weight: 600; }
.cmp-stage-detail { font-size: 12.5px; color: var(--text-muted); line-height: 1.5; margin-top: 2px; }
.cmp-stage-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 7px; }
.cmp-chip { font-family: var(--font-mono); font-size: 11px; color: var(--accent);
  background: var(--accent-ghost, var(--bg-elevated)); padding: 1px 7px; border-radius: 99px; }
.cmp-note { font-size: 12px; color: var(--text-secondary); }
.cmp-time { display: inline-flex; align-items: center; gap: 4px; font-size: 11px; color: var(--text-faint); }

.cmp-spin { animation: cmp-spin 1s linear infinite; }
@keyframes cmp-spin { to { transform: rotate(360deg); } }
`;
