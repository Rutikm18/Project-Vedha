"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Loader2, Radar, ShieldCheck } from "lucide-react";
import { PortalShell } from "../../components/portal/PortalShell";
import {
  portalApi, severityChip, SEVERITY_VAR, GRADE_VAR,
  type PortalEngagement, type PortalSummary, type PortalTrends, type PortalFinding,
} from "../../lib/portal-client";

const SEVS = ["critical", "high", "medium", "low", "info"] as const;
const SEV_ORDER: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

function Kpi({ label, value, hint, color }: { label: string; value: React.ReactNode; hint?: string; color?: string }) {
  return (
    <div className="panel" style={{ padding: 16 }}>
      <div className="eyebrow">{label}</div>
      <div className="num" style={{ marginTop: 4, fontSize: 26, fontWeight: 600,
        color: color ?? "var(--text-primary)" }}>{value}</div>
      {hint && <div style={{ marginTop: 2, fontSize: 11, color: "var(--text-faint)" }}>{hint}</div>}
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="panel">
      <div className="panel-head"><h2 className="panel-title">{title}</h2></div>
      <div style={{ padding: 16 }}>{children}</div>
    </div>
  );
}

export default function PortalOverview() {
  const eng = useQuery({ queryKey: ["portal", "engagement"], queryFn: () => portalApi<PortalEngagement>("/engagement") });
  const summary = useQuery({ queryKey: ["portal", "summary"], queryFn: () => portalApi<PortalSummary>("/summary") });
  const trends = useQuery({ queryKey: ["portal", "trends"], queryFn: () => portalApi<PortalTrends>("/trends") });
  const findings = useQuery({ queryKey: ["portal", "findings"], queryFn: () => portalApi<PortalFinding[]>("/findings") });

  const requestAction = (
    <Link href="/portal/scans" style={{ display: "inline-flex", alignItems: "center", gap: 6,
      borderRadius: 7, background: "var(--accent)", color: "#fff", padding: "6px 12px",
      fontSize: 12, fontWeight: 600, textDecoration: "none" }}>
      <Radar style={{ width: 14, height: 14 }} /> Request scan
    </Link>
  );

  const statusItems = summary.data
    ? [{ label: "QUEUE", value: String(summary.data.pending_requests + summary.data.running_jobs),
         color: "var(--accent)" }]
    : [];

  const s = summary.data;
  const t = trends.data;
  const maxSev = t ? Math.max(1, ...SEVS.map((k) => t.by_severity[k] ?? 0)) : 1;
  const maxTl = t ? Math.max(1, ...t.timeline.map((p) => Math.max(p.opened, p.closed))) : 1;
  const topOpen = [...(findings.data ?? [])]
    .filter((f) => f.status === "open" || f.status === "confirmed")
    .sort((a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9))
    .slice(0, 6);

  return (
    <PortalShell
      title={eng.data?.name ?? "Dashboard"}
      subtitle="Your security posture at a glance"
      statusItems={statusItems}
      headerActions={requestAction}
    >
      {summary.isLoading ? (
        <div style={{ display: "flex", alignItems: "center", gap: 8, color: "var(--text-muted)" }}>
          <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} /> Loading your dashboard…
        </div>
      ) : summary.isError ? (
        <div className="panel" style={{ padding: 16, color: "var(--sev-critical-color)" }}>
          {(summary.error as Error).message}
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {/* KPI row */}
          <div style={{ display: "grid", gap: 12,
            gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))" }}>
            <Kpi label="Posture grade" value={s?.posture.grade ?? "—"}
              color={GRADE_VAR[s?.posture.grade ?? ""] ?? "var(--text-primary)"}
              hint={`score ${s?.posture.posture_score ?? 0}/100`} />
            <Kpi label="Risk index" value={s?.posture.risk_index ?? 0} hint="0 low · 100 high" />
            <Kpi label="Exploitable" value={s?.posture.exploitable_score ?? 0} hint="weighted exposure" />
            <Kpi label="Open" value={s?.open_findings ?? 0} color="var(--sev-high-color)" />
            <Kpi label="Closed" value={s?.closed_findings ?? 0} color="var(--nominal-color)" />
          </div>

          <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))" }}>
            {/* Severity breakdown */}
            <Panel title="Open findings by severity">
              {t && SEVS.every((k) => (t.by_severity[k] ?? 0) === 0) ? (
                <div style={{ fontSize: 13, color: "var(--text-muted)" }}>No open findings.</div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {SEVS.map((k) => {
                    const v = t?.by_severity[k] ?? 0;
                    return (
                      <div key={k} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <span className="chip" style={{ ...severityChip(k), width: 78, justifyContent: "center",
                          textTransform: "capitalize" }}>{k}</span>
                        <div className="meter" style={{ flex: 1, height: 8 }}>
                          <div className="meter-fill" style={{ width: `${(v / maxSev) * 100}%`,
                            background: SEVERITY_VAR[k] }} />
                        </div>
                        <span className="num" style={{ width: 24, textAlign: "right", fontSize: 12,
                          color: "var(--text-secondary)" }}>{v}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </Panel>

            {/* Opened vs closed timeline */}
            <Panel title="Opened vs closed (6 mo)">
              {t && (
                <div style={{ display: "flex", alignItems: "flex-end", gap: 10, height: 130,
                  paddingTop: 6 }}>
                  {t.timeline.map((p) => (
                    <div key={p.period} style={{ flex: 1, display: "flex", flexDirection: "column",
                      alignItems: "center", gap: 4, minWidth: 0 }}>
                      <div style={{ display: "flex", alignItems: "flex-end", gap: 3, height: 96 }}>
                        <div title={`${p.opened} opened`} style={{ width: 9,
                          height: `${(p.opened / maxTl) * 100}%`, minHeight: p.opened ? 3 : 0,
                          background: "var(--sev-high-color)", borderRadius: 2 }} />
                        <div title={`${p.closed} closed`} style={{ width: 9,
                          height: `${(p.closed / maxTl) * 100}%`, minHeight: p.closed ? 3 : 0,
                          background: "var(--nominal-color)", borderRadius: 2 }} />
                      </div>
                      <span style={{ fontSize: 9, color: "var(--text-faint)" }}>{p.period.slice(5)}</span>
                    </div>
                  ))}
                </div>
              )}
              <div style={{ display: "flex", gap: 14, marginTop: 10 }}>
                <Legend color="var(--sev-high-color)" label="Opened" />
                <Legend color="var(--nominal-color)" label="Closed" />
              </div>
            </Panel>
          </div>

          <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))" }}>
            {/* Queue */}
            <Panel title="Scan queue">
              <div style={{ display: "flex", gap: 24 }}>
                <QueueStat label="Pending review" value={s?.pending_requests ?? 0} />
                <QueueStat label="Running / queued" value={s?.running_jobs ?? 0} />
              </div>
              <Link href="/portal/scans" style={{ display: "inline-block", marginTop: 14,
                fontSize: 12, color: "var(--accent)", textDecoration: "none" }}>
                View scans & request a new one →
              </Link>
            </Panel>

            {/* Top open incidents */}
            <Panel title="Top open findings">
              {topOpen.length === 0 ? (
                <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13,
                  color: "var(--text-muted)" }}>
                  <ShieldCheck style={{ width: 16, height: 16, color: "var(--nominal-color)" }} />
                  Nothing open — you&apos;re clear.
                </div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {topOpen.map((f) => (
                    <div key={f.id} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <span className="chip" style={{ ...severityChip(f.severity), width: 70,
                        justifyContent: "center", textTransform: "capitalize" }}>{f.severity}</span>
                      <span style={{ flex: 1, fontSize: 13, color: "var(--text-primary)", overflow: "hidden",
                        textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{f.title}</span>
                      <span className="num" style={{ fontSize: 12, color: "var(--text-muted)" }}>
                        {f.risk_score ?? "—"}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </Panel>
          </div>
        </div>
      )}
    </PortalShell>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 5, fontSize: 11,
      color: "var(--text-muted)" }}>
      <span style={{ width: 9, height: 9, borderRadius: 2, background: color }} /> {label}
    </span>
  );
}

function QueueStat({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="num" style={{ fontSize: 24, fontWeight: 600, color: "var(--text-primary)" }}>{value}</div>
      <div style={{ fontSize: 11, color: "var(--text-muted)" }}>{label}</div>
    </div>
  );
}
