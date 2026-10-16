"use client";

/**
 * FleetJobs — the tenant-wide job feed for the Fleet page.
 *
 * Drop into app/fleet/page.tsx:  <FleetJobs />
 *
 * Shows every probe's scan jobs (from GET /api/fleet/jobs) with the probe and
 * engagement names, filterable by probe, by engagement, and a "running only"
 * toggle. Polls every 5s so the live queue stays current.
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import { CAMPAIGN_CSS } from "../../components/campaign/campaign-css";
import { createFleetWorkspaceApi, type FleetWorkspaceSurface } from "../../lib/fleet-workspace-api";

interface Job {
  job_id: string; reference?: string | null; agent_id: string | null; agent_name: string | null;
  engagement_id: string | null; engagement_name: string | null;
  job_type: string; status: string; use_case_id: string | null;
  created_at: string | null; started_at: string | null; completed_at: string | null;
}

export default function FleetJobs({ surface = "manager" }: { surface?: FleetWorkspaceSurface }) {
  const api = useMemo(() => createFleetWorkspaceApi(surface), [surface]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [probe, setProbe] = useState<string>("");        // agent_id filter
  const [engagement, setEngagement] = useState<string>(""); // engagement_id filter
  const [runningOnly, setRunningOnly] = useState(false);

  const load = useCallback(async () => {
    try {
      const q = new URLSearchParams();
      if (probe) q.set("agent_id", probe);
      if (engagement) q.set("engagement_id", engagement);
      if (runningOnly) q.set("running", "true");
      setJobs(await api.jobs<Job[]>(q.toString()));
    } catch (e) { setErr((e as Error).message); }
  }, [api, probe, engagement, runningOnly]);

  useEffect(() => {
    const initial = window.setTimeout(() => void load(), 0);
    const t = setInterval(load, 5000);       // keep the live queue current
    return () => { window.clearTimeout(initial); clearInterval(t); };
  }, [load]);

  // filter option lists derived from the current feed (probe + engagement names)
  const probes = useMemo(() => {
    const m = new Map<string, string>();
    jobs.forEach((j) => { if (j.agent_id) m.set(j.agent_id, j.agent_name ?? j.agent_id.slice(0, 8)); });
    return [...m.entries()];
  }, [jobs]);
  const engagements = useMemo(() => {
    const m = new Map<string, string>();
    jobs.forEach((j) => { if (j.engagement_id) m.set(j.engagement_id, j.engagement_name ?? j.engagement_id.slice(0, 8)); });
    return [...m.entries()];
  }, [jobs]);

  const running = jobs.filter((j) => j.status === "running" || j.status === "pending").length;
  const filtered = Boolean(probe || engagement || runningOnly);

  return (
    <section className="cpg" style={{ gap: 4 }}>
      <style>{CAMPAIGN_CSS}</style>
      {/* ── filter bar ── */}
      <div className="cpg-q-filters">
        <span className="cpg-dim" aria-live="polite"><b style={{ color: "var(--accent)" }}>{running}</b> running · {jobs.length} total</span>
        <select value={probe} onChange={(e) => setProbe(e.target.value)} aria-label="Filter by probe">
          <option value="">All probes</option>
          {probes.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
        </select>
        {surface === "manager" ? (
          <select value={engagement} onChange={(e) => setEngagement(e.target.value)} aria-label="Filter by engagement">
            <option value="">All engagements</option>
            {engagements.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
          </select>
        ) : (
          <span className="cpg-chip">Assigned engagement</span>
        )}
        <label>
          <input type="checkbox" checked={runningOnly} onChange={(e) => setRunningOnly(e.target.checked)} /> Running only
        </label>
      </div>

      {err && <p className="cpg-err" role="alert">Failed to load jobs: {err}</p>}

      {/* ── job rows ── */}
      <div className="cpg-q-list">
        {jobs.length === 0 && !err && (
          <p className="cpg-empty">
            {filtered ? "No jobs match these filters." : "No jobs yet. A job appears here when a scan is queued for a probe."}
          </p>
        )}
        {jobs.map((j) => (
          <div key={j.job_id} className="cpg-q-row">
            <strong>{j.use_case_id ?? j.job_type}</strong>
            <span className="cpg-status" data-status={j.status}><i aria-hidden />{j.status}</span>
            {j.agent_name && <span className="cpg-dim">probe <b>{j.agent_name}</b></span>}
            {j.engagement_name && <span className="cpg-dim">· {j.engagement_name}</span>}
            <span className="cpg-ref" title={j.job_id}>{j.reference ?? j.job_id.slice(0, 8)}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
