// manager/frontend/components/dashboard/ExposureCards.tsx
"use client";

/**
 * Exposure analytics — Protocol Risk and Zone Health.
 *
 * Both read the same /api/analytics/exposure payload under one React Query
 * key, so the two cards cost one request.
 *
 * Design decision worth calling out: these two cards previously rendered
 * *identical* bars with *opposite* polarity — a long red bar meant "bad" in
 * Protocol Risk and a long green bar meant "good" in Zone Health. Same shape,
 * inverted meaning, no label to disambiguate. Fixed three ways here: each card
 * states its direction in the header, each row carries a word for its band
 * ("Severe exposure", "Healthy"), and colour is never the only cue.
 *
 * ProtocolRow.tsx and ZoneRow.tsx are superseded by MeterRow below.
 */
import React from "react";
import { Activity, Shield } from "lucide-react";
import { useConsoleQuery } from "../../lib/console-source";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { Meter } from "../console/Primitives";

interface Exposure {
  protocols: { name: string; value: number }[];
  zones: { name: string; score: number }[];
}

export function useExposure() {
  return useConsoleQuery<Exposure>("exposure", {
    refetchInterval: 60_000,
  });
}

/* --------------------------------------------------------------- banding */

/** Risk: higher is worse. */
function riskBand(v: number) {
  if (v >= 85) return { color: "var(--sev-critical-color)", word: "Severe exposure" };
  if (v >= 65) return { color: "var(--sev-high-color)", word: "High exposure" };
  if (v >= 45) return { color: "var(--sev-medium-color)", word: "Elevated" };
  return { color: "var(--accent)", word: "Contained" };
}

/** Health: higher is better. */
function healthBand(v: number) {
  if (v >= 90) return { color: "var(--nominal-color)", word: "Healthy" };
  if (v >= 75) return { color: "var(--accent)", word: "Stable" };
  if (v >= 60) return { color: "var(--sev-medium-color)", word: "Watch" };
  return { color: "var(--sev-critical-color)", word: "Degraded" };
}

/* -------------------------------------------------------------- MeterRow */

function MeterRow({
  name, value, band, unit = "", ariaVerb,
}: {
  name: string;
  value: number;
  band: { color: string; word: string };
  unit?: string;
  ariaVerb: string;
}) {
  return (
    <div className="console-row" style={{ padding: "var(--space-3) var(--space-5)", display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: "var(--space-3)" }}>
        <span
          className="mono"
          style={{ fontSize: "var(--fs-body-s)", fontWeight: 600, color: "var(--text-primary)", letterSpacing: "-0.01em", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", minWidth: 0 }}
        >
          {name}
        </span>
        <span style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)", color: "var(--text-muted)", flexShrink: 0 }}>{band.word}</span>
        <span
          className="num-mono"
          style={{ marginLeft: "auto", fontSize: "var(--fs-body)", fontWeight: 700, color: band.color, flexShrink: 0 }}
        >
          {value}{unit}
        </span>
      </div>
      <Meter value={value} color={band.color} height={4} ticks label={`${name}: ${ariaVerb} ${value}${unit} — ${band.word}`} />
    </div>
  );
}

/* ------------------------------------------------------------------ cards */

export function ProtocolRiskCard() {
  const { data, isLoading, error, refetch } = useExposure();
  // Hooks must run unconditionally — declare state BEFORE any early return
  // (isLoading/error), or the hook count changes between renders (React #310).
  const [showAll, setShowAll] = React.useState(false);

  if (isLoading) return <div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={51} /></div>;
  if (error) return <ErrorState title="Protocol risk didn't load. The analytics service returned an error." onRetry={() => refetch()} />;

  const protocols = [...(data?.protocols ?? [])].sort((a, b) => b.value - a.value);
  const CAP = 6;
  const visible = showAll ? protocols : protocols.slice(0, CAP);
  if (protocols.length === 0) {
    return (
      <div style={{ padding: "var(--space-6)" }}>
        <EmptyState
          icon={Activity}
          title="No exposed services yet"
          hint="Protocol risk appears once discovery finds services listening on your assets."
        />
      </div>
    );
  }

  return (
    <>
      {visible.map((p) => (
        <MeterRow key={p.name} name={p.name} value={p.value} unit="%" band={riskBand(p.value)} ariaVerb="risk" />
      ))}
      {protocols.length > CAP && <ShowAllButton showAll={showAll} onClick={() => setShowAll((v) => !v)} total={protocols.length} />}
    </>
  );
}

export function ZoneHealthCard() {
  const { data, isLoading, error, refetch } = useExposure();
  const [showAll, setShowAll] = React.useState(false);   // unconditional — before early returns (React #310)

  if (isLoading) return <div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={51} /></div>;
  if (error) return <ErrorState title="Zone health didn't load. The analytics service returned an error." onRetry={() => refetch()} />;

  const zones = [...(data?.zones ?? [])].sort((a, b) => a.score - b.score);
  const CAP = 6;
  const visible = showAll ? zones : zones.slice(0, CAP);
  if (zones.length === 0) {
    return (
      <div style={{ padding: "var(--space-6)" }}>
        <EmptyState
          icon={Shield}
          title="No zones yet"
          hint="Tag assets with an environment and their zone health shows up here."
        />
      </div>
    );
  }

  return (
    <>
      {visible.map((z) => (
        <MeterRow key={z.name} name={z.name} value={z.score} band={healthBand(z.score)} ariaVerb="health score" />
      ))}
      {zones.length > CAP && <ShowAllButton showAll={showAll} onClick={() => setShowAll((v) => !v)} total={zones.length} />}
    </>
  );
}

/** Disclosure for capped meter lists (keeps band-3 panels height-balanced). */
function ShowAllButton({ showAll, onClick, total }: { showAll: boolean; onClick: () => void; total: number }) {
  return (
    <button type="button" className="focusable" onClick={onClick}
      style={{ width: "100%", minHeight: 44, padding: "var(--space-3) var(--space-5)",
        background: "none", border: "none", borderTop: "var(--hairline) solid var(--border-subtle)",
        color: "var(--accent)", cursor: "pointer", fontFamily: "var(--font-ui)",
        fontSize: "var(--fs-body-s)", textAlign: "left" }}>
      {showAll ? "Show fewer" : `Show all ${total}`}
    </button>
  );
}
