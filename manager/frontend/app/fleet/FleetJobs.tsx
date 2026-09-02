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

interface Job {
  job_id: string; agent_id: string | null; agent_name: string | null;
  engagement_id: string | null; engagement_name: string | null;
  job_type: string; status: string; use_case_id: string | null;
  created_at: string | null; started_at: string | null; completed_at: string | null;
}

const STATUS_COLOR: Record<string, string> = {
  running: "var(--accent)", pending: "var(--text-muted)",
  completed: "var(--sev-low,#3b82f6)", failed: "var(--sev-high,#f97316)",
};

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(path, { credentials: "same-origin" });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error ?? res.statusText);
  return body as T;
}

export default function FleetJobs() {
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
      setJobs(await fetchJson<Job[]>(`/api/fleet/jobs?${q.toString()}`));
    } catch (e) { setErr((e as Error).message); }
  }, [probe, engagement, runningOnly]);

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

  const selectStyle = { fontSize: 11.5, padding: "5px 9px", borderRadius: 8,
    border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)",
    color: "var(--text-secondary)" } as const;

  return (
    <section style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {/* ── filter bar ── */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
        <span style={{ fontSize: 10.5, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.4, textTransform: "uppercase" }}>Jobs</span>
        <span style={{ fontSize: 11, color: "var(--text-muted)" }}><strong style={{ color: "var(--accent)" }}>{running}</strong> running · {jobs.length} total</span>
        <select value={probe} onChange={(e) => setProbe(e.target.value)} style={selectStyle}>
          <option value="">All probes</option>
          {probes.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
        </select>
        <select value={engagement} onChange={(e) => setEngagement(e.target.value)} style={selectStyle}>
          <option value="">All engagements</option>
          {engagements.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
        </select>
        <label style={{ fontSize: 11, color: "var(--text-muted)", display: "flex", alignItems: "center", gap: 5, cursor: "pointer" }}>
          <input type="checkbox" checked={runningOnly} onChange={(e) => setRunningOnly(e.target.checked)} /> running only
        </label>
      </div>

      {err && <div style={{ fontSize: 12, color: "var(--sev-high,#f97316)" }}>Failed to load jobs: {err}</div>}

      {/* ── job rows ── */}
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {jobs.length === 0 && <div style={{ fontSize: 12, color: "var(--text-muted)" }}>No jobs match the current filters.</div>}
        {jobs.map((j) => (
          <div key={j.job_id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "9px 14px",
            borderRadius: 10, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", flexWrap: "wrap" }}>
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: STATUS_COLOR[j.status] ?? "var(--text-muted)",
              animation: j.status === "running" ? "pulse 1.4s infinite" : "none", flexShrink: 0 }} />
            <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-primary)" }}>{j.use_case_id ?? j.job_type}</span>
            <span style={{ fontSize: 10.5, textTransform: "capitalize", color: STATUS_COLOR[j.status] ?? "var(--text-muted)" }}>{j.status}</span>
            {j.agent_name && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>probe <strong style={{ color: "var(--text-secondary)" }}>{j.agent_name}</strong></span>}
            {j.engagement_name && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>· {j.engagement_name}</span>}
            <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-faint)" }}>{j.job_id.slice(0, 8)}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
