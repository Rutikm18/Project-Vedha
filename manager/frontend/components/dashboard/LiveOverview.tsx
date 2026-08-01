"use client";

/**
 * LiveOverview — real-time situational-awareness strip for the ops console.
 *
 * Replaces mock KPI numbers with LIVE data from the BFF (/api/findings,
 * /api/engagements). For a security operations console, truthful real-time
 * state is the single most important UX property — a dashboard that looks
 * great but shows fake numbers is worse than a plain one showing real ones.
 *
 * UX rules applied (ui-ux-pro-max): semantic severity color + LABEL (never
 * color alone), tabular figures so numbers don't jitter, skeleton on load,
 * explicit empty/error states, 44px+ targets, visible focus, reduced-motion
 * safe (no essential info conveyed by animation).
 */
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldAlert, Activity, Crosshair, Layers } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState } from "../states/DataState";

type Sev = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
interface Engagement { id: string; status?: string }
interface FindingSummary {
  openTotal: number; criticalOpen: number; highOpen: number;
  mediumOpen: number; lowOpen: number; infoOpen: number;
}

const SEV: Record<Sev, { color: string; bg: string; label: string }> = {
  CRITICAL: { color: "var(--sev-critical-color)", bg: "var(--sev-critical-bg)", label: "Critical" },
  HIGH:     { color: "var(--sev-high-color)",     bg: "var(--sev-high-bg)",     label: "High" },
  MEDIUM:   { color: "var(--sev-medium-color)",   bg: "var(--sev-medium-bg)",   label: "Medium" },
  LOW:      { color: "var(--sev-low-color, var(--accent))", bg: "var(--bg-hover)", label: "Low" },
  INFO:     { color: "var(--text-muted)",         bg: "var(--bg-hover)",         label: "Info" },
};

/** Engagements use different statuses than findings. "PLANNING" (draft) and
 *  "ACTIVE" are both considered open/in-progress. */
function isActiveEngagement(s?: string) {
  return !s || ["PLANNING", "ACTIVE"].includes(s.toUpperCase());
}

function Kpi({ icon, label, value, color, sub }: {
  icon: React.ReactNode; label: string; value: number | string; color: string; sub?: string;
}) {
  return (
    <div
      tabIndex={0}
      className="dashboard-kpi-surface"
      style={{
        "--kpi-accent": color,
        flex: "1 1 0", minWidth: 168,
        padding: "18px 20px 16px", display: "flex", flexDirection: "column", gap: 12,
        transition: "transform var(--dur-fast) var(--ease-out), border-color var(--dur-fast), box-shadow var(--dur-fast)",
        outlineColor: "var(--accent)", cursor: "default",
      } as React.CSSProperties}
      onMouseEnter={(e) => { e.currentTarget.style.borderColor = color; e.currentTarget.style.transform = "translateY(-3px)"; e.currentTarget.style.boxShadow = "var(--shadow-md)"; }}
      onMouseLeave={(e) => { e.currentTarget.style.borderColor = "var(--border-subtle)"; e.currentTarget.style.transform = "translateY(0)"; e.currentTarget.style.boxShadow = "var(--shadow-sm)"; }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{
          color,
          width: 28,
          height: 28,
          borderRadius: 7,
          background: "var(--bg-surface)",
          border: "0.5px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }} aria-hidden>{icon}</span>
        <span style={{ fontSize: 10.5, fontWeight: 600, letterSpacing: 0.8, textTransform: "uppercase",
          color: "var(--text-muted)", fontFamily: "'Inter', sans-serif" }}>{label}</span>
      </div>
      <div style={{ fontSize: 40, fontWeight: 650, lineHeight: 0.96, color: "var(--text-primary)",
        fontFamily: "var(--font-display)", fontVariantNumeric: "tabular-nums", letterSpacing: 0 }}>{value}</div>
      {sub && <div style={{ fontSize: 12, color: "var(--text-muted)", letterSpacing: 0.1 }}>{sub}</div>}
    </div>
  );
}

export function LiveOverview() {
  const findings = useQuery({ queryKey: ["findings-summary"], queryFn: () => fetchJson<FindingSummary>("/api/findings/summary") });
  const engagements = useQuery({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<{ engagements: Engagement[] }>("/api/engagements"),
  });

  if (findings.isLoading || engagements.isLoading) return <SkeletonRows rows={1} height={92} />;
  if (findings.error) return <ErrorState title="Couldn't load live findings." onRetry={() => findings.refetch()} />;

  const summary = findings.data;
  const by = (s: Sev) => ({
    CRITICAL: summary?.criticalOpen ?? 0,
    HIGH: summary?.highOpen ?? 0,
    MEDIUM: summary?.mediumOpen ?? 0,
    LOW: summary?.lowOpen ?? 0,
    INFO: summary?.infoOpen ?? 0,
  })[s];
  const engs = engagements.data?.engagements ?? [];
  const activeEngs = engs.filter((e) => isActiveEngagement(e.status)).length;
  const total = summary?.openTotal ?? 0;

  // severity distribution bar segments (only non-zero, so it reads cleanly)
  const segs = (["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] as Sev[])
    .map((s) => ({ s, n: by(s) })).filter((x) => x.n > 0);

  return (
    <section aria-label="Live operations overview"
      style={{ position: "relative", display: "flex", flexDirection: "column", gap: 14 }}>
      <div style={{ position: "relative", zIndex: 1, display: "flex", gap: 14, flexWrap: "wrap" }}>
        <Kpi icon={<Layers size={16} />} label="Active Engagements" value={activeEngs} color="var(--accent)"
             sub={`${engs.length} total`} />
        <Kpi icon={<ShieldAlert size={16} />} label="Open Findings" value={total} color="var(--text-primary)"
             sub="across all engagements" />
        <Kpi icon={<Crosshair size={16} />} label="Critical" value={by("CRITICAL")} color={SEV.CRITICAL.color}
             sub="needs immediate action" />
        <Kpi icon={<Activity size={16} />} label="High" value={by("HIGH")} color={SEV.HIGH.color}
             sub="prioritize next" />
      </div>

      {/* severity distribution — color + count label, never color alone */}
      {total > 0 ? (
        <div style={{ position: "relative", zIndex: 1 }}>
          <div role="img" aria-label={`Severity distribution: ${segs.map((x) => `${by(x.s)} ${SEV[x.s].label}`).join(", ")}`}
            style={{ display: "flex", height: 8, borderRadius: 999, overflow: "hidden", background: "var(--bg-hover)" }}>
            {segs.map(({ s, n }) => (
              <div key={s} style={{ flex: n, background: SEV[s].color }} title={`${n} ${SEV[s].label}`} />
            ))}
          </div>
          <div style={{ display: "flex", gap: 16, marginTop: 8, flexWrap: "wrap" }}>
            {segs.map(({ s, n }) => (
              <span key={s} style={{ display: "inline-flex", alignItems: "center", gap: 6,
                fontSize: 12, color: "var(--text-secondary)", fontFamily: "'Inter', sans-serif" }}>
                <span style={{ width: 8, height: 8, borderRadius: 2, background: SEV[s].color }} aria-hidden />
                {SEV[s].label} <strong style={{ color: "var(--text-primary)", fontVariantNumeric: "tabular-nums" }}>{n}</strong>
              </span>
            ))}
          </div>
        </div>
      ) : (
        <div style={{ fontSize: 13, color: "var(--text-muted)", padding: "8px 2px" }}>
          No open findings yet — run a scan from an engagement to populate this view.
        </div>
      )}
    </section>
  );
}
