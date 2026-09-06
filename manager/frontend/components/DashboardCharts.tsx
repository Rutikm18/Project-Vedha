"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from "recharts";
import { Users, ShieldAlert, ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";
import Link from "next/link";
import { useCountUp } from "../hooks/useCountUp";
import { fetchJson } from "../lib/fetcher";

/* ─── Types ─── */
interface TimelinePoint { date: string; CRITICAL: number; HIGH: number; MEDIUM: number; LOW: number; }
interface Engagement {
  id: string; name: string;
  findingsBySeverity: { CRITICAL: number; HIGH: number; MEDIUM: number; LOW: number };
  findingCount: number; assetCount: number; status: string;
}
interface ActivityItem { id: string; timestamp: string; actor: string; action: string; detail: string; engagementId: string; }
interface Finding {
  id: string; title: string; severity: keyof typeof SEV | "INFO";
  riskScore: number; affectedHost: string; status: string; kevListed?: boolean;
}
interface FindingPage { items: Finding[]; total: number; }
interface FindingSummary { validated: number; }

const SEV = {
  CRITICAL: { color: "var(--sev-critical-color)", bg: "var(--sev-critical-bg)", glow: "var(--sev-critical-glow)" },
  HIGH:     { color: "var(--sev-high-color)",     bg: "var(--sev-high-bg)",     glow: "var(--sev-high-glow)"     },
  MEDIUM:   { color: "var(--sev-medium-color)",   bg: "var(--sev-medium-bg)",   glow: "var(--sev-medium-glow)"   },
  LOW:      { color: "var(--sev-low-color)",       bg: "var(--sev-low-bg)",      glow: "var(--sev-low-bg)"        },
};

/* ─── Skeleton ─── */
function Bone({ w, h, radius = 6 }: { w: number | string; h: number; radius?: number }) {
  return <div className="shimmer" style={{ width: w, height: h, borderRadius: radius }} />;
}

/* ─── Custom tooltip ─── */
function ChartTooltip({ active, payload, label }: { active?: boolean; payload?: { name: string; value: number; color: string }[]; label?: string }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: "var(--bg-panel)", border: "0.5px solid var(--border-default)",
      borderRadius: 8, padding: "10px 14px",
      boxShadow: "var(--shadow-md)",
    }}>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-muted)", marginBottom: 7 }}>{label}</div>
      {payload.map((p) => (
        <div key={p.name} style={{ display: "flex", justifyContent: "space-between", gap: 16, fontFamily: "var(--font-mono)", fontSize: 11, marginBottom: 3 }}>
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ color: "var(--text-primary)", fontWeight: 700 }}>{p.value}</span>
        </div>
      ))}
    </div>
  );
}

/* ─── KPI Card ─── */
function KpiCard({
  label, value, icon, accentColor, trend, loading, delay = 0,
}: {
  label: string; value: number; icon: React.ReactNode;
  accentColor: string; trend?: number; loading?: boolean; delay?: number;
}) {
  const displayValue = useCountUp(loading ? 0 : value, 900, delay);

  return (
    <div
      className="stagger-item dashboard-kpi-surface"
      style={{
        "--kpi-accent": accentColor,
        animationDelay: `${delay}ms`,
        background: "var(--bg-panel)",
        border: "0.5px solid var(--border-subtle)",
        borderRadius: 8,
        padding: "16px 18px 14px",
        position: "relative",
        overflow: "hidden",
        cursor: "default",
        boxShadow: "var(--shadow-sm)",
      } as React.CSSProperties}
    >
      <div style={{ position: "relative", zIndex: 1 }}>
        {loading ? (
          <>
            <Bone w={90} h={10} /><div style={{ marginTop: 12 }}><Bone w={56} h={28} /></div>
          </>
        ) : (
          <>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
              <span style={{ fontFamily: "var(--font-body)", fontSize: 11, fontWeight: 500, color: "var(--text-secondary)" }}>
                {label}
              </span>
              <div style={{
                opacity: 0.78,
                color: accentColor,
                width: 26,
                height: 26,
                borderRadius: 7,
                background: "var(--bg-surface)",
                border: "0.5px solid var(--border-subtle)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}>
                {icon}
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "flex-end", gap: 10 }}>
              <span className="animate-count-up" style={{
                fontFamily: "var(--font-body)", fontSize: 30, fontWeight: 700,
                color: "var(--text-primary)", lineHeight: 1,
                letterSpacing: 0,
                animationDelay: `${delay + 100}ms`,
              }}>
                {displayValue}
              </span>
              {trend !== undefined && (
                <div style={{
                  display: "flex", alignItems: "center", gap: 2, marginBottom: 5,
                  fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 600,
                  color: trend > 0 ? "var(--sev-critical-color)" : trend < 0 ? "var(--accent)" : "var(--text-muted)",
                  background: trend > 0 ? "var(--sev-critical-bg)" : trend < 0 ? "var(--accent-ghost)" : "var(--bg-surface)",
                  borderRadius: 6, padding: "2px 6px",
                }}>
                  {trend > 0 ? <ArrowUpRight size={11} /> : trend < 0 ? <ArrowDownRight size={11} /> : <Minus size={11} />}
                  {Math.abs(trend)}%
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

/* ─── Severity badge ─── */
function SevBadge({ sev }: { sev: keyof typeof SEV }) {
  const s = SEV[sev];
  return (
    <span style={{
      fontFamily: "var(--font-body)", fontSize: 10, fontWeight: 700, letterSpacing: 0.5,
      color: s.color, background: s.bg, borderRadius: 5, padding: "2px 8px",
      textTransform: "uppercase" as const,
      transition: "transform 0.15s var(--ease-out)",
    }}>
      {sev}
    </span>
  );
}

/* ─── Score bar ─── */
function ScoreBar({ score }: { score: number }) {
  const pct   = score / 10;
  const color = score >= 900 ? "var(--sev-critical-color)" : score >= 700 ? "var(--sev-high-color)" : "var(--sev-medium-color)";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div className="progress-track" style={{ width: 64, height: 4 }}>
        <div className="progress-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 700, color, minWidth: 36 }}>
        {score}
      </span>
    </div>
  );
}

const STATUS_STYLE: Record<string, { color: string; bg: string }> = {
  OPEN:           { color: "var(--sev-critical-color)", bg: "var(--sev-critical-bg)" },
  IN_REVIEW:      { color: "var(--sev-high-color)",     bg: "var(--sev-high-bg)"     },
  IN_REMEDIATION: { color: "var(--accent)",             bg: "var(--accent-ghost)"    },
  VERIFIED:       { color: "var(--nominal-color)",     bg: "var(--nominal-bg)"      },
  CLOSED:         { color: "var(--text-muted)",         bg: "var(--bg-surface)"      },
};

/* ─── Main component ─── */
export function DashboardCharts() {
  const { data, isLoading } = useQuery({
    queryKey: ["engagements"],
    // Must use fetchJson (injects the Bearer token) — a raw fetch hits the
    // withBackend route with no Authorization header and 401s, which is why the
    // KPIs/charts previously rendered all-zero while LiveOverview showed real data.
    queryFn: () => fetchJson<{
      engagements?: Engagement[];
      timeline?: TimelinePoint[];
      activity?: ActivityItem[];
      stats?: Record<string, number>;
    }>("/api/engagements"),
  });

  // Real findings drive the "Critical findings" table and the KEV count — same
  // queryKey as LiveOverview so React Query serves one shared, deduped request.
  const { data: findingsData } = useQuery({
    queryKey: ["dashboard-top-findings"],
    queryFn: () => fetchJson<FindingPage>("/api/findings?paginated=true&page=1&page_size=5&sort=risk"),
  });
  const findings: Finding[] = findingsData?.items ?? [];
  const { data: findingSummary } = useQuery({
    queryKey: ["findings-summary"],
    queryFn: () => fetchJson<FindingSummary>("/api/findings/summary"),
  });

  // Real activity feed (merged scan + finding events) — replaces the engagements
  // payload's always-empty activity array.
  const { data: activityData, isLoading: activityLoading } = useQuery({
    queryKey: ["activity"],
    queryFn: () => fetchJson<ActivityItem[]>("/api/activity?limit=20"),
    refetchInterval: 30_000,
  });
  const activity: ActivityItem[] = activityData ?? [];

  const engagements: Engagement[] = data?.engagements ?? [];
  const timeline: TimelinePoint[]  = data?.timeline ?? [];
  const stats = data?.stats ?? {};

  // Top findings by risk score (open first), replacing the old static list.
  const topFindings = [...findings]
    .sort((a, b) => (b.riskScore ?? 0) - (a.riskScore ?? 0))
    .slice(0, 5);
  const validatedCount = findingSummary?.validated ?? 0;

  const totalAssets       = stats.totalAssets   ?? engagements.reduce((s, e) => s + (e.assetCount ?? 0), 0);

  const slimTimeline = timeline.map((t, i) => ({
    ...t, displayDate: i % 5 === 0 ? t.date.slice(5) : "",
  }));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

      {/* ── KPI Row ── */}
      <div className="dashboard-kpi-grid">
        {/* Trend arrows removed: there is no historical snapshot store to compute
            a real delta, and a security console must never show fabricated deltas.
            TASK 9: "Total Findings" and "Active Engagements" removed — they restated
            the LiveOverview ledger's open-findings total and engagement count. The
            two below are unique to this section (not on the ledger) and are kept. */}
        <KpiCard label="Assets Discovered"  value={isLoading ? 0 : totalAssets}       icon={<Users         size={14} />} accentColor="var(--sev-medium-color)" delay={0}  loading={isLoading} />
        <KpiCard label="Validated Findings" value={isLoading ? 0 : validatedCount}    icon={<ShieldAlert   size={14} />} accentColor="var(--sev-high-color)"   delay={50} loading={isLoading} />
      </div>

      {/* ── Charts Row ── */}
      <div className="dashboard-chart-grid">

        {/* Area chart */}
        <div className="stagger-item dashboard-card" style={{
          animationDelay: "120ms",
          background: "var(--bg-panel)", border: "0.5px solid var(--border-subtle)",
          borderRadius: 8, padding: "16px 18px 12px",
          boxShadow: "var(--shadow-sm)",
          transition: "border-color 0.18s ease",
        }}
          onMouseEnter={(e) => (e.currentTarget.style.borderColor = "var(--border-strong)")}
          onMouseLeave={(e) => (e.currentTarget.style.borderColor = "var(--border-subtle)")}
        >
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
            <span style={{ fontFamily: "var(--font-body)", fontSize: 13, fontWeight: 600, color: "var(--text-primary)" }}>
              Findings trend
            </span>
            <span style={{ fontFamily: "var(--font-body)", fontSize: 11, color: "var(--text-muted)", background: "var(--bg-surface)", borderRadius: 6, padding: "3px 9px" }}>
              Last 30 days
            </span>
          </div>
          {isLoading ? (
            <Bone w="100%" h={160} />
          ) : slimTimeline.length === 0 ? (
            <div style={{ height: 160, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-muted)" }}>
              Trend history not available yet — needs periodic finding snapshots.
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={160}>
              <AreaChart data={slimTimeline} margin={{ top: 4, right: 0, bottom: 0, left: -24 }}>
                <defs>
                  {(["CRITICAL", "HIGH", "MEDIUM"] as const).map((s) => (
                    <linearGradient key={s} id={`grad-${s}`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor={SEV[s].color} stopOpacity={0.18} />
                      <stop offset="95%" stopColor={SEV[s].color} stopOpacity={0}   />
                    </linearGradient>
                  ))}
                </defs>
                <XAxis dataKey="displayDate" tick={{ fontFamily: "var(--font-mono)", fontSize: 9, fill: "var(--text-muted)" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontFamily: "var(--font-mono)", fontSize: 9, fill: "var(--text-muted)" }} axisLine={false} tickLine={false} allowDecimals={false} />
                <Tooltip content={<ChartTooltip />} />
                {(["CRITICAL", "HIGH", "MEDIUM"] as const).map((s) => (
                  <Area key={s} type="monotone" dataKey={s} stroke={SEV[s].color} fill={`url(#grad-${s})`} strokeWidth={2} dot={false} animationDuration={800} />
                ))}
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>

      </div>

      {/* ── Findings + Activity ── */}
      <div className="dashboard-main-grid">

        {/* Top findings table */}
        <div className="stagger-item dashboard-card" style={{
          animationDelay: "200ms",
          background: "var(--bg-panel)", border: "0.5px solid var(--border-subtle)",
          borderRadius: 8, overflow: "hidden",
          boxShadow: "var(--shadow-sm)",
          transition: "border-color 0.18s ease",
        }}
          onMouseEnter={(e) => (e.currentTarget.style.borderColor = "var(--border-strong)")}
          onMouseLeave={(e) => (e.currentTarget.style.borderColor = "var(--border-subtle)")}
        >
          <div className="dashboard-card-header">
            <span style={{ fontFamily: "var(--font-body)", fontSize: 13, fontWeight: 600, color: "var(--text-primary)" }}>
              Critical findings
            </span>
            <Link href="/findings" style={{
              display: "flex", alignItems: "center", gap: 4,
              fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 500,
              color: "var(--accent)", textDecoration: "none",
              transition: "opacity 0.15s ease",
            }}
              onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.7")}
              onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
            >
              View all <ArrowUpRight size={12} />
            </Link>
          </div>

          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr className="dashboard-table-head">
                {["Title", "Host", "Risk Score", "Status"].map((h) => (
                  <th key={h} style={{
                    padding: "8px 20px", textAlign: "left",
                    fontFamily: "var(--font-body)", fontSize: 11, fontWeight: 600,
                    color: "var(--text-muted)", letterSpacing: 0.3,
                    borderBottom: "0.5px solid var(--border-subtle)",
                  }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                [0, 1, 2, 3, 4].map((i) => (
                  <tr key={i} style={{ borderBottom: i < 4 ? "0.5px solid var(--border-subtle)" : "none" }}>
                    <td style={{ padding: "11px 20px" }} colSpan={4}><Bone w="90%" h={12} /></td>
                  </tr>
                ))
              ) : topFindings.length === 0 ? (
                <tr>
                  <td colSpan={4} style={{ padding: "36px 20px", textAlign: "center", fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-muted)" }}>
                    No findings yet — run a scan to populate this table.
                  </td>
                </tr>
              ) : (
                topFindings.map((f, i) => {
                  const ss = STATUS_STYLE[f.status] ?? STATUS_STYLE.OPEN;
                  const sev = (f.severity in SEV ? f.severity : "LOW") as keyof typeof SEV;
                  return (
                    <tr key={f.id} className="table-row-hover stagger-item" style={{
                      animationDelay: `${240 + i * 40}ms`,
                      borderBottom: i < topFindings.length - 1 ? "0.5px solid var(--border-subtle)" : "none",
                      cursor: "pointer",
                    }}>
                      <td style={{ padding: "11px 20px", maxWidth: 280 }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
                          <SevBadge sev={sev} />
                          <span style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-primary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                            {f.title}
                          </span>
                        </div>
                      </td>
                      <td style={{ padding: "11px 20px" }}>
                        <span style={{
                          fontFamily: "var(--font-mono)", fontSize: 11,
                          color: "var(--accent)", background: "var(--accent-ghost)",
                          borderRadius: 5, padding: "2px 7px",
                        }}>
                          {f.affectedHost}
                        </span>
                      </td>
                      <td style={{ padding: "11px 20px" }}>
                        <ScoreBar score={f.riskScore} />
                      </td>
                      <td style={{ padding: "11px 20px" }}>
                        <span style={{
                          fontFamily: "var(--font-body)", fontSize: 11, fontWeight: 600,
                          color: ss.color, background: ss.bg, borderRadius: 5, padding: "3px 8px",
                        }}>
                          {f.status.replace(/_/g, " ")}
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Activity feed */}
        <div className="stagger-item dashboard-card" style={{
          animationDelay: "240ms",
          background: "var(--bg-panel)", border: "0.5px solid var(--border-subtle)",
          borderRadius: 8, overflow: "hidden", display: "flex", flexDirection: "column",
          boxShadow: "var(--shadow-sm)",
          transition: "border-color 0.18s ease",
        }}
          onMouseEnter={(e) => (e.currentTarget.style.borderColor = "var(--border-strong)")}
          onMouseLeave={(e) => (e.currentTarget.style.borderColor = "var(--border-subtle)")}
        >
          <div className="dashboard-card-header" style={{ flexShrink: 0 }}>
            <span style={{ fontFamily: "var(--font-body)", fontSize: 13, fontWeight: 600, color: "var(--text-primary)" }}>
              Recent activity
            </span>
            <Link href="/engagements" style={{ display: "flex", alignItems: "center", gap: 4, fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 500, color: "var(--accent)", textDecoration: "none" }}>
              All <ArrowUpRight size={12} />
            </Link>
          </div>
          <div style={{ overflowY: "auto", flex: 1 }}>
            {activityLoading ? (
              [1, 2, 3, 4].map((i) => (
                <div key={i} style={{ padding: "12px 16px", borderBottom: "0.5px solid var(--border-subtle)" }}>
                  <Bone w="75%" h={10} /><div style={{ marginTop: 5 }}><Bone w="55%" h={8} /></div>
                </div>
              ))
            ) : activity.length === 0 ? (
              <div style={{ padding: "36px 16px", textAlign: "center", fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-muted)" }}>
                No recent activity
              </div>
            ) : (
              activity.slice(0, 8).map((a, i) => (
                <div key={a.id} className="stagger-item"
                  style={{
                    animationDelay: `${280 + i * 35}ms`,
                    padding: "11px 16px",
                    borderBottom: i < Math.min(activity.length, 8) - 1 ? "0.5px solid var(--border-subtle)" : "none",
                    display: "flex", gap: 10, cursor: "default",
                    transition: "background 0.12s ease",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "var(--bg-surface)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
                >
                  <div style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--accent)", marginTop: 4, flexShrink: 0 }} />
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontFamily: "var(--font-body)", fontSize: 11, fontWeight: 600, color: "var(--accent)", marginBottom: 2 }}>{a.action}</div>
                    <div style={{ fontFamily: "var(--font-body)", fontSize: 12, color: "var(--text-primary)", lineHeight: 1.4, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{a.detail}</div>
                    <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-muted)", marginTop: 2 }}>
                      {new Date(a.timestamp).toLocaleString()}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

    </div>
  );
}
