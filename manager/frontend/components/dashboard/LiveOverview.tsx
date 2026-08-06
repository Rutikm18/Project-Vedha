// manager/frontend/components/dashboard/LiveOverview.tsx
"use client";

/**
 * LiveOverview — the console's headline instrument.
 *
 * Design decision worth stating: this replaces four floating KPI cards with a
 * single "threat ledger". Four equal-weight cards ask the analyst to read four
 * numbers and rank them; the ledger ranks for them — one count, one plain-
 * language verdict, one proportional bar, one legend that doubles as a filter.
 * That is the whole job of the top of a SOC dashboard: what is on fire, right
 * now, and how much of it.
 *
 * Data: /api/findings/summary and /api/engagements (server is authoritative).
 *
 * Accessibility contract:
 *  - Severity is colour + word + sigil, never colour alone.
 *  - The ledger bar has a text equivalent (the legend below it), so the bar is
 *    aria-hidden rather than fighting a screen reader with a fake image label.
 *  - Legend chips are real buttons at 32px+ with visible focus when a filter
 *    handler is supplied; otherwise they are inert text and say so.
 *  - Reduced motion: the only animation is the critical pulse dot, and the
 *    count next to it carries the same information.
 */
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldCheck, Radar } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState } from "../states/DataState";
import { SEVERITY, SEVERITY_ORDER, Severity } from "../../lib/severity";
import { Readout } from "../console/Primitives";

interface Engagement { id: string; status?: string }

interface FindingSummary {
  openTotal: number; criticalOpen: number; highOpen: number;
  mediumOpen: number; lowOpen: number; infoOpen: number;
}

/** Engagements use a different status vocabulary than findings: a draft
 *  ("PLANNING") and a running ("ACTIVE") engagement both count as in-progress. */
function isActiveEngagement(s?: string) {
  return !s || ["PLANNING", "ACTIVE"].includes(s.toUpperCase());
}

/** Plain-language verdict. Written for the person on shift, not the schema. */
function verdict(counts: Record<Severity, number>, total: number): { text: string; tone: string } {
  if (total === 0) return { text: "Nothing open. The last scan came back clean.", tone: "var(--nominal-color)" };
  if (counts.CRITICAL > 0) {
    return {
      text: `${counts.CRITICAL} critical ${counts.CRITICAL === 1 ? "finding needs" : "findings need"} action now.`,
      tone: "var(--sev-critical-color)",
    };
  }
  if (counts.HIGH > 0) {
    return { text: `No criticals open. ${counts.HIGH} high to work through next.`, tone: "var(--sev-high-color)" };
  }
  return { text: "No critical or high findings open.", tone: "var(--nominal-color)" };
}

export function LiveOverview({ onSelectSeverity }: { onSelectSeverity?: (s: Severity) => void }) {
  const findings = useQuery({
    queryKey: ["findings-summary"],
    queryFn: () => fetchJson<FindingSummary>("/api/findings/summary"),
    refetchInterval: 60_000,
  });
  const engagements = useQuery({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<{ engagements: Engagement[] }>("/api/engagements"),
    refetchInterval: 60_000,
  });

  if (findings.isLoading) {
    return <div className="panel" style={{ padding: 18 }}><SkeletonRows rows={3} height={44} /></div>;
  }
  if (findings.error) {
    return <ErrorState title="Findings didn't load. The manager API returned an error." onRetry={() => findings.refetch()} />;
  }

  const s = findings.data;
  const counts: Record<Severity, number> = {
    CRITICAL: s?.criticalOpen ?? 0,
    HIGH: s?.highOpen ?? 0,
    MEDIUM: s?.mediumOpen ?? 0,
    LOW: s?.lowOpen ?? 0,
    INFO: s?.infoOpen ?? 0,
  };
  const total = s?.openTotal ?? 0;
  const v = verdict(counts, total);

  // Engagements failing shouldn't blank the findings headline — degrade that
  // one readout instead of the whole strip.
  const engs = engagements.data?.engagements ?? [];
  const engFailed = Boolean(engagements.error);
  const activeEngs = engs.filter((e) => isActiveEngagement(e.status)).length;

  const segments = SEVERITY_ORDER.map((k) => ({ k, n: counts[k] })).filter((x) => x.n > 0);
  const worst = segments[0]?.k;
  const rail = worst ? SEVERITY[worst].color : "var(--nominal-color)";

  return (
    <section
      className="panel"
      style={{ "--rail": rail } as React.CSSProperties}
      aria-label="Live operations overview"
    >
      <div style={{ display: "flex", flexWrap: "wrap", alignItems: "stretch" }}>
        {/* ---- headline: count + verdict ---------------------------------- */}
        <div style={{ flex: "3 1 320px", minWidth: 0, padding: "20px 24px 18px" }}>
          <span className="eyebrow">Open findings</span>
          <div style={{ display: "flex", alignItems: "baseline", gap: 14, marginTop: 8, flexWrap: "wrap" }}>
            <span
              className="num"
              style={{
                fontFamily: "var(--font-display)", fontSize: 56, fontWeight: 600,
                lineHeight: 0.88, letterSpacing: "-0.035em", color: "var(--text-primary)",
              }}
            >
              {total}
            </span>
            <span
              style={{
                display: "inline-flex", alignItems: "center", gap: 8,
                fontFamily: "var(--font-ui)", fontSize: 13, color: v.tone, fontWeight: 500,
              }}
            >
              {counts.CRITICAL > 0 && <span className="pulse-dot" aria-hidden />}
              {v.text}
            </span>
          </div>
        </div>

        {/* ---- engagement context ----------------------------------------- */}
        <div style={{ borderLeft: "0.5px solid var(--border-subtle)", display: "flex" }}>
          <Readout
            label="Engagements running"
            value={engFailed ? "—" : activeEngs}
            size={28}
            color={engFailed ? "var(--text-faint)" : "var(--text-primary)"}
            sub={
              engFailed ? (
                <button
                  type="button"
                  className="focusable"
                  onClick={() => engagements.refetch()}
                  style={{ background: "none", border: "none", padding: 0, color: "var(--accent)", cursor: "pointer", font: "inherit" }}
                >
                  Couldn&apos;t load — retry
                </button>
              ) : (
                `${engs.length} total`
              )
            }
          />
        </div>
      </div>

      {/* ---- the ledger ---------------------------------------------------- */}
      {total > 0 ? (
        <div style={{ padding: "0 24px 20px" }}>
          <div
            aria-hidden
            style={{ display: "flex", gap: 2, height: 10, borderRadius: 999, overflow: "hidden", background: "rgba(128,128,128,0.16)" }}
          >
            {segments.map(({ k, n }) => (
              // minWidth stops a count of 1 next to a count of 400 collapsing
              // to a sub-pixel sliver that reads as "zero".
              <div
                key={k}
                style={{ flex: `${n} 1 0`, minWidth: 6, background: SEVERITY[k].color, borderRadius: 999 }}
                title={`${n} ${SEVERITY[k].label}`}
              />
            ))}
          </div>

          <ul
            style={{ display: "flex", gap: 8, marginTop: 12, flexWrap: "wrap", listStyle: "none", padding: 0, margin: "12px 0 0" }}
          >
            {SEVERITY_ORDER.map((k) => {
              const n = counts[k];
              const m = SEVERITY[k];
              const interactive = Boolean(onSelectSeverity) && n > 0;
              const inner = (
                <>
                  <span aria-hidden style={{ color: m.color, fontSize: 9 }}>{m.sigil}</span>
                  <span style={{ color: n > 0 ? "var(--text-secondary)" : "var(--text-faint)" }}>{m.label}</span>
                  <strong
                    className="num-mono"
                    style={{ fontSize: 12, fontWeight: 700, color: n > 0 ? "var(--text-primary)" : "var(--text-faint)" }}
                  >
                    {n}
                  </strong>
                </>
              );
              return (
                <li key={k}>
                  {interactive ? (
                    <button
                      type="button"
                      className="legend-chip"
                      style={{ "--sev-edge": m.edge } as React.CSSProperties}
                      onClick={() => onSelectSeverity?.(k)}
                    >
                      {inner}
                      <span className="sr-only">— filter findings to {m.label}</span>
                    </button>
                  ) : (
                    <span className="legend-chip" data-static="true">{inner}</span>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      ) : (
        <div
          style={{
            display: "flex", alignItems: "center", gap: 10, margin: "0 24px 20px",
            padding: "12px 14px", borderRadius: "var(--r-md)",
            background: "var(--nominal-bg)", border: "0.5px solid var(--nominal-edge)",
          }}
        >
          <ShieldCheck size={15} style={{ color: "var(--nominal-color)", flexShrink: 0 }} aria-hidden />
          <span style={{ fontFamily: "var(--font-ui)", fontSize: 12.5, color: "var(--text-secondary)" }}>
            No open findings.{" "}
            <span style={{ display: "inline-flex", alignItems: "center", gap: 5, color: "var(--text-muted)" }}>
              <Radar size={12} aria-hidden /> Start a scan from an engagement to populate this view.
            </span>
          </span>
        </div>
      )}
    </section>
  );
}
