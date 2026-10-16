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
import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowUpRight, ChevronDown, Clock3, CircleSlash, Trash2 } from "lucide-react";
import { CAMPAIGN_CSS } from "../../../components/campaign/campaign-css";
import RawFacts from "./RawFacts";
import { createScannerWorkspaceApi, type ScannerWorkspaceSurface } from "../../../lib/scanner-workspace-api";

// Mirrors MAX_PENDING_JOBS_PER_ENGAGEMENT in the manager (agents router). The
// backend is authoritative and rejects the 4th queued job with 409; this copy
// exists only so the UI can WARN before the operator hits that wall.
const MAX_QUEUED_JOBS = 3;

type PhaseState = "done" | "active" | "pending";
interface Phase { name: string; status: PhaseState; count: number | null }
interface JobSummary {
  scanners?: string[]; scanner_count?: number; fact_count?: number | null;
  open_ports?: number | null; profile?: string | null; ok?: boolean | null;
}
interface Job {
  id: string; use_case_id: string | null; job_type: string; status: string;
  phase: string; agent_name: string | null; result_summary: JobSummary;
  reference?: string | null;
  created_at: string | null; started_at: string | null; completed_at: string | null;
}
interface Finding {
  id: string; title: string; severity: string; risk_score: number | null;
  confidence?: number | null; corroborated_by?: string[];
  cve_ids: string[] | null; mitre_techniques: string[] | null; state: string;
  remediation: string | null;
}
interface Coverage {
  rules_total: number; rules_assessed: number; rules_blind: number;
  rules_unassessed: number; blind_rule_ids: string[]; has_gaps: boolean;
}
interface Progress {
  engagement_id: string;
  engagement?: { name: string | null; status: string };
  overall_status: string;
  is_complete: boolean;
  reasons?: string[];
  coverage?: Coverage;
  evidence?: { submissions: number; covered: number; fully_covered: boolean };
  queue?: { pending: boolean; overdue: boolean; dead: boolean };
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
  detecting: "Detecting", stalled: "Stalled", complete: "Complete",
  complete_with_gaps: "Complete — with gaps", error: "Error",
  cancelled: "Cancelled",
};

/** How a job's bar should read.
 *
 *  `running` is INDETERMINATE on purpose. The old code drew a fixed 56% for every
 *  running job, which is a number the app does not have: the probe reports no
 *  percentage, so a static bar claims progress it cannot know and never moves.
 *  An indeterminate bar says "working, duration unknown", which is the truth.
 *
 *  Terminal states are all 100% — a cancelled job is FINISHED, not 12% done.
 *  They differ by colour, not by length. */
function jobBar(status: string): { pct: number; color: string; indeterminate: boolean } {
  switch (status) {
    case "completed":
      return { pct: 100, color: "var(--nominal-color)", indeterminate: false };
    case "failed":
      return { pct: 100, color: "var(--sev-critical-color)", indeterminate: false };
    case "cancelled":
      // Muted, never the accent: an operator stop must not look like live work.
      return { pct: 100, color: "var(--text-faint)", indeterminate: false };
    case "running":
      return { pct: 100, color: "var(--accent)", indeterminate: true };
    default:                                    // pending / queued — nothing yet
      return { pct: 0, color: "var(--accent)", indeterminate: false };
  }
}

const PHASE_LABEL: Record<string, string> = {
  scanning: "Scanning", aggregating: "Aggregating", detection: "Detection",
  correlation: "Correlation", prioritization: "Prioritization", remediation: "Remediation",
};
const SEV_COLOR: Record<string, string> = {
  critical: "var(--sev-critical, #ef4444)", high: "var(--sev-high, #f97316)",
  medium: "var(--sev-medium, #eab308)", low: "var(--sev-low, #3b82f6)",
  info: "var(--text-muted)",
};

/** Split a remediation string into ordered, human steps (numbered / sentence-based). */
function remediationSteps(text: string | null): string[] {
  if (!text) return [];
  const byLine = text.split(/\r?\n|(?:^|\s)\d+[.)]\s+/).map((s) => s.trim()).filter(Boolean);
  if (byLine.length > 1) return byLine;
  return text.split(/(?<=[.;])\s+(?=[A-Z(])/).map((s) => s.trim()).filter(Boolean);
}

export default function CampaignProgress({ engagementId, surface = "manager" }: {
  engagementId: string;
  surface?: ScannerWorkspaceSurface;
}) {
  const api = useMemo(() => createScannerWorkspaceApi(surface), [surface]);
  const [data, setData] = useState<Progress | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  // Per-job in-flight/error state so one failing cancel can't blank the page and
  // a double-click can't fire two cancels.
  const [cancelling, setCancelling] = useState<Record<string, boolean>>({});
  const [cancelErr, setCancelErr] = useState<Record<string, string>>({});

  const load = useCallback(async () => {
    try {
      setData(await api.campaignProgress<Progress>(engagementId));
    } catch (e) { setErr((e as Error).message); }
  }, [api, engagementId]);

  // Stop a running job or drop a queued one. Both go to the same endpoint: the
  // manager decides which case applies. On success we reload immediately rather
  // than wait for the 4s poll, so the card reflects the click straight away.
  const cancelJob = useCallback(async (jobId: string, running: boolean) => {
    const verb = running ? "Stop this running job" : "Remove this queued job";
    if (!window.confirm(`${verb}? This cannot be undone.`)) return;
    setCancelling((c) => ({ ...c, [jobId]: true }));
    setCancelErr((e) => ({ ...e, [jobId]: "" }));
    try {
      await api.cancelJob(jobId);
      await load();
    } catch (e) {
      // A 409 means it finished on its own between render and click — reload so
      // the card stops offering an action that no longer applies.
      setCancelErr((prev) => ({ ...prev, [jobId]: (e as Error).message }));
      await load();
    } finally {
      setCancelling((c) => ({ ...c, [jobId]: false }));
    }
  }, [api, load]);

  useEffect(() => {
    const initial = window.setTimeout(() => void load(), 0);
    // Keep polling until the WHOLE pipeline is complete — not just the scan job.
    if (data?.is_complete) return;
    // Back off on a stalled queue so a dead worker doesn't get hammered every 4s.
    const delay = data?.overall_status === "stalled" ? 30000 : 4000;
    const t = setInterval(load, delay);
    return () => { window.clearTimeout(initial); clearInterval(t); };
  }, [load, data?.is_complete, data?.overall_status]);

  if (err) return <p className="cpg-empty" data-tone="bad" role="alert"><style>{CAMPAIGN_CSS}</style>Failed to load campaign: {err}</p>;
  if (!data) return <p className="cpg-empty"><style>{CAMPAIGN_CSS}</style>Loading campaign…</p>;

  const gaps = data.coverage?.has_gaps ?? false;
  const statusColor = data.overall_status === "error" ? "var(--sev-high,#f97316)"
    : gaps ? "var(--sev-medium,#eab308)"
    : data.is_complete ? "var(--sev-low,#3b82f6)" : "var(--accent)";
  const s = data.summary;
  const reasons = data.reasons ?? [];
  const queued = data.jobs.filter((j) => j.status === "pending").length;
  const queueFull = queued >= MAX_QUEUED_JOBS;

  return (
    <section className="cpg">
      <style>{CAMPAIGN_CSS}</style>

      {/* ── exec band: authoritative status + risk rollup ── */}
      <div className="cpg-card cpg-band">
        <span className="cpg-state">
          <i style={{ background: statusColor }} data-live={!data.is_complete} aria-hidden />
          <strong>{STATUS_LABEL[data.overall_status] ?? data.overall_status}</strong>
          {/* "Complete" appears ONLY when the whole pipeline is done */}
          {!data.is_complete && <small>in progress ({data.percent}%)</small>}
        </span>
        {data.engagement?.name && <span className="cpg-dim">{data.engagement.name}</span>}
        {data.job_stats && (
          <span className="cpg-dim">
            {data.job_stats.probes.length || 0} {(data.job_stats.probes.length || 0) === 1 ? "probe" : "probes"} · {data.job_stats.running} running · {data.job_stats.complete}/{data.job_stats.total} jobs done
          </span>
        )}
        {s && (
          <span className="cpg-rollup">
            <span><b>{s.total_findings}</b> {s.total_findings === 1 ? "finding" : "findings"}</span>
            {s.actionable > 0 && <span><b style={{ color: "var(--accent)" }}>{s.actionable}</b> actionable</span>}
            {s.exploitable > 0 && <span style={{ color: "var(--sev-critical-color)" }}><b>{s.exploitable}</b> exploitable</span>}
            {s.max_risk_score > 0 && <span className="cpg-mono">max risk {Math.round(s.max_risk_score)}</span>}
          </span>
        )}
        <span className="cpg-links">
          <Link href={surface === "portal" ? "/portal/scope" : `/engagements/${engagementId}`} className="cpg-link">
            Engagement view <ArrowUpRight size={12} aria-hidden />
          </Link>
          <Link href={surface === "portal" ? "/portal/findings" : `/findings?engagement=${engagementId}`} className="cpg-link">
            All results <ArrowUpRight size={12} aria-hidden />
          </Link>
        </span>
      </div>

      {/* ── reasons banner: state what happened, never leave a silent spinner ── */}
      {reasons.length > 0 && (
        <div className="cpg-reasons" style={{ ["--cpg-tone" as string]: statusColor }}>
          {reasons.map((r, i) => (
            <span key={i}><b aria-hidden>⚠</b> {r}</span>
          ))}
          {gaps && data.coverage && data.coverage.blind_rule_ids.length > 0 && (
            <code>blind checks: {data.coverage.blind_rule_ids.join(" · ")}</code>
          )}
        </div>
      )}

      {/* ── coverage strip: what did detection actually CHECK? ── */}
      {data.coverage && data.coverage.rules_total > 0 && (
        <div className="cpg-card cpg-strip">
          <span className="cpg-label">Coverage</span>
          <span><b>{data.coverage.rules_assessed}</b>/{data.coverage.rules_total} checks assessed</span>
          {data.coverage.rules_blind > 0 && (
            <span style={{ color: "var(--sev-medium-color)" }}><b>{data.coverage.rules_blind}</b> blind (unknown, not clean)</span>
          )}
          {data.coverage.rules_unassessed > 0 && <span>{data.coverage.rules_unassessed} not run</span>}
          {data.evidence && data.evidence.submissions > 0 && (
            <span className="cpg-end" style={{ color: data.evidence.fully_covered ? undefined : "var(--sev-medium-color)" }}>
              {data.evidence.covered}/{data.evidence.submissions} submissions detected
            </span>
          )}
        </div>
      )}

      {/* ── pipeline ticker + progress bar ── */}
      <div className="cpg-card" style={{ overflow: "hidden" }}>
        <div className="cpg-pipe-head">
          <h3>Detection pipeline</h3>
          <span>{data.percent}%</span>
        </div>
        <div className="cpg-track" role="progressbar" aria-label="Detection pipeline progress"
          aria-valuenow={data.percent} aria-valuemin={0} aria-valuemax={100}>
          <i style={{ transform: `scaleX(${Math.min(100, Math.max(0, data.percent)) / 100})` }} />
        </div>
        <ol className="cpg-phases" aria-label="Pipeline stages">
          {data.phases.map((p, i) => (
            <li key={p.name} className="cpg-phase" data-status={p.status}>
              <div>
                <i aria-hidden />
                <span>
                  {PHASE_LABEL[p.name] ?? p.name}{p.count != null && <> · <em>{p.count}</em></>}
                  <span className="sr-only"> ({p.status})</span>
                </span>
              </div>
              {i < data.phases.length - 1 && <hr aria-hidden />}
            </li>
          ))}
        </ol>
        <div className="cpg-sevs">
          {(["critical", "high", "medium", "low", "info"] as const).map((sev) => {
            const n = data.detection.by_severity[sev] ?? 0;
            return (
              <span key={sev} data-zero={n === 0}>
                <i style={{ background: SEV_COLOR[sev] }} aria-hidden /><b>{n}</b> {sev}
              </span>
            );
          })}
        </div>
      </div>

      {/* ── per-probe jobs ── */}
      <div>
        <div className="cpg-head">
          <h3>Jobs</h3>
          <span className="cpg-count">{data.jobs.length}</span>
          {/* Surface the queue cap BEFORE the operator hits it, so a refused enqueue is never a surprise. */}
          <span className="cpg-chip" data-tone={queueFull ? "warn" : undefined}
            title={queueFull
              ? `Queue is full (${MAX_QUEUED_JOBS} max). Remove a queued job before adding another.`
              : `${queued} of ${MAX_QUEUED_JOBS} queue slots used`}>
            queue {queued}/{MAX_QUEUED_JOBS}{queueFull ? " · full" : ""}
          </span>
        </div>
        {data.jobs.length === 0 ? (
          <p className="cpg-empty">No jobs yet. Launch a campaign from the Scanner and its jobs appear here as they are queued and run.</p>
        ) : (
          <div className="cpg-jobs">
            {data.jobs.map((j) => {
              const bar = jobBar(j.status);
              const actionable = j.status === "running" || j.status === "pending";
              const ref = j.reference ?? j.id.slice(0, 8);
              return (
                <article key={j.id} className="cpg-card cpg-job">
                  <div className="cpg-job-top">
                    <strong>{j.use_case_id ?? j.job_type}</strong>
                    <span className="cpg-chip" data-tone="accent" style={{ textTransform: "capitalize" }}>{j.phase}</span>
                    <span className="cpg-status" data-status={j.status}><i aria-hidden />{j.status}</span>
                    {j.agent_name && <span className="cpg-dim">vedha-agent <b>{j.agent_name}</b></span>}
                    {/* The quotable reference, not eight characters of a UUID. */}
                    <span className="cpg-ref" title={j.reference ? `Job ${j.reference}` : j.id}>{ref}</span>
                    {/* Stop / Remove — offered ONLY for jobs that can still be acted on. A finished
                        job shows no control at all, rather than a disabled one. */}
                    {actionable && (
                      <button
                        type="button"
                        className="cpg-act"
                        onClick={() => void cancelJob(j.id, j.status === "running")}
                        disabled={!!cancelling[j.id]}
                        title={j.status === "running"
                          ? "Stop this running job and free the probe for the next queued job"
                          : "Remove this job from the queue"}
                        aria-label={`${j.status === "running" ? "Stop" : "Remove"} job ${ref}`}
                      >
                        {j.status === "running" ? <CircleSlash size={11} aria-hidden /> : <Trash2 size={11} aria-hidden />}
                        {cancelling[j.id] ? "Stopping…" : j.status === "running" ? "Stop" : "Remove"}
                      </button>
                    )}
                  </div>
                  {/* SAFE raw-result summary */}
                  {(j.result_summary?.scanner_count != null || j.result_summary?.fact_count != null
                    || j.result_summary?.open_ports != null || j.result_summary?.profile
                    || j.result_summary?.scanners?.length) && (
                    <div className="cpg-facts">
                      {j.result_summary?.scanner_count != null && <span><b>{j.result_summary.scanner_count}</b> scanners</span>}
                      {j.result_summary?.fact_count != null && <span><b>{j.result_summary.fact_count}</b> facts</span>}
                      {j.result_summary?.open_ports != null && <span><b>{j.result_summary.open_ports}</b> open ports</span>}
                      {j.result_summary?.profile && <span>profile <b>{j.result_summary.profile}</b></span>}
                      {j.result_summary?.scanners?.length ? <span className="cpg-mono">{j.result_summary.scanners.join(" · ")}</span> : null}
                    </div>
                  )}
                  <div
                    className="cpg-bar"
                    role="progressbar"
                    aria-label={`${j.use_case_id ?? j.job_type} job progress`}
                    {...(bar.indeterminate
                      // No aria-valuenow when the value is genuinely unknown: a screen reader
                      // should hear "in progress", not a made-up number.
                      ? { "aria-valuetext": "in progress" }
                      : { "aria-valuenow": bar.pct, "aria-valuemin": 0, "aria-valuemax": 100 })}
                  >
                    <i style={{
                      width: bar.indeterminate ? "40%" : "100%",
                      transform: bar.indeterminate ? undefined : `scaleX(${Math.min(100, Math.max(0, bar.pct)) / 100})`,
                      background: bar.color,
                      animation: bar.indeterminate ? "vedhaIndeterminate 1.4s ease-in-out infinite" : undefined,
                    }} />
                  </div>
                  {cancelErr[j.id] && <div role="alert" className="cpg-err">Could not stop this job: {cancelErr[j.id]}</div>}
                  <div className="cpg-times">
                    {j.created_at && <span><Clock3 size={10} style={{ display: "inline", verticalAlign: -1, marginRight: 4 }} aria-hidden />queued {new Date(j.created_at).toLocaleString()}</span>}
                    {j.started_at && <span>started {new Date(j.started_at).toLocaleString()}</span>}
                    {j.completed_at && <span>finished {new Date(j.completed_at).toLocaleString()}</span>}
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </div>

      {/* ── findings + step-by-step remediation ── */}
      <div>
        <div className="cpg-head">
          <h3>Findings &amp; remediation</h3>
          <span className="cpg-count">{data.findings.length}</span>
        </div>
        <div className="cpg-finds">
          {data.findings.length === 0 && <FindingsEmpty data={data} gaps={gaps} />}
          {data.findings.map((f) => {
            const steps = remediationSteps(f.remediation);
            const isOpen = !!open[f.id];
            const sevColor = SEV_COLOR[f.severity] ?? "var(--text-muted)";
            return (
              <div key={f.id} className="cpg-card cpg-find">
                <button type="button" className="cpg-find-head" aria-expanded={isOpen}
                  onClick={() => setOpen((o) => ({ ...o, [f.id]: !o[f.id] }))}>
                  <span className="cpg-sev" style={{ color: sevColor }}>{f.severity}</span>
                  <strong>{f.title}</strong>
                  <span className="cpg-find-meta">
                    {f.mitre_techniques?.length ? <span className="cpg-chip cpg-mono">{f.mitre_techniques.join(", ")}</span> : null}
                    {f.corroborated_by && f.corroborated_by.length > 0 && (
                      <span className="cpg-chip" data-tone="accent"
                        title={`Confidence raised by cross-signal corroboration: ${f.corroborated_by.join(", ")}`}>corroborated</span>
                    )}
                    {f.risk_score != null && <span className="cpg-chip cpg-mono">risk {Math.round(f.risk_score)}</span>}
                    {f.confidence != null && <span className="cpg-chip cpg-mono">conf {f.confidence}</span>}
                    {f.state === "confirmed" && <span className="cpg-chip">confirmed</span>}
                  </span>
                  <ChevronDown size={14} aria-hidden style={{ color: "var(--text-faint)", transform: isOpen ? "rotate(180deg)" : undefined }} />
                </button>
                {isOpen && (
                  <div className="cpg-find-body">
                    {steps.length ? (
                      <ol className="cpg-steps">{steps.map((st, i) => <li key={i}>{st}</li>)}</ol>
                    ) : <p className="cpg-dim" style={{ margin: "10px 0 0" }}>No remediation guidance recorded.</p>}
                    {f.cve_ids?.length ? (
                      <div className="cpg-cves">{f.cve_ids.map((c) => <span key={c} className="cpg-chip cpg-mono">{c}</span>)}</div>
                    ) : null}
                    <Link href={surface === "portal" ? `/portal/findings?finding=${f.id}` : `/findings?engagement=${engagementId}&finding=${f.id}`}
                      className="cpg-link" style={{ marginTop: 10 }}>
                      Open finding result <ArrowUpRight size={12} aria-hidden />
                    </Link>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* ── raw scanner evidence (the facts the vedha-agent actually collected) ── */}
      <RawFacts engagementId={engagementId} surface={surface} />
    </section>
  );
}


/**
 * The honest empty state. "No findings" is NOT "clean" — it can mean detection is
 * still running, it stalled, it errored, or (worst) it ran but couldn't assess some
 * checks against the data the scanner returned. Say which; never assert a security
 * conclusion the backend hasn't established.
 */
function FindingsEmpty({ data, gaps }: { data: Progress; gaps: boolean }) {
  if (data.overall_status === "error")
    return <p className="cpg-empty" data-tone="bad">
      Detection failed — {data.reasons?.[0] ?? "see run error"}. This is NOT a clean result.
    </p>;
  if (data.overall_status === "aggregating" || data.overall_status === "stalled")
    return <p className="cpg-empty" data-tone="warn">
      Detection hasn&apos;t produced results yet — {data.reasons?.[0] ?? "waiting on the detection worker"}.
    </p>;
  if (gaps && data.coverage)
    return <p className="cpg-empty" data-tone="warn">
      No findings, but the scan was incomplete: {data.coverage.rules_blind} of{" "}
      {data.coverage.rules_total} checks couldn&apos;t run against the data the scanner
      returned. <strong>Treat this as unknown, not clean.</strong>
    </p>;
  if (!data.is_complete)
    return <p className="cpg-empty">Detection in progress…</p>;
  return <p className="cpg-empty">
    No findings — all {data.coverage?.rules_assessed ?? "applicable"} checks ran against
    this data and none matched.
  </p>;
}
