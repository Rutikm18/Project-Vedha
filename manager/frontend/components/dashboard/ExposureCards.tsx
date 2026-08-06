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
import { useQuery } from "@tanstack/react-query";
import { Activity, Shield } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { Meter } from "../console/Primitives";

interface Exposure {
  protocols: { name: string; value: number }[];
  zones: { name: string; score: number }[];
}

export function useExposure() {
  return useQuery({
    queryKey: ["exposure"],
    queryFn: () => fetchJson<Exposure>("/api/analytics/exposure"),
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
    <div className="console-row" style={{ padding: "12px 20px", display: "flex", flexDirection: "column", gap: 8 }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
        <span
          className="num-mono"
          style={{ fontSize: 12, fontWeight: 600, color: "var(--text-primary)", letterSpacing: "-0.01em", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", minWidth: 0 }}
        >
          {name}
        </span>
        <span style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-muted)", flexShrink: 0 }}>{band.word}</span>
        <span
          className="num-mono"
          style={{ marginLeft: "auto", fontSize: 12.5, fontWeight: 700, color: band.color, flexShrink: 0 }}
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

  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={4} height={42} /></div>;
  if (error) return <ErrorState title="Protocol risk didn't load. The analytics service returned an error." onRetry={() => refetch()} />;

  const protocols = [...(data?.protocols ?? [])].sort((a, b) => b.value - a.value);
  if (protocols.length === 0) {
    return (
      <div style={{ padding: 28 }}>
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
      <p style={scaleNote}>Worst open finding per exposed service. Higher is worse.</p>
      {protocols.map((p) => (
        <MeterRow key={p.name} name={p.name} value={p.value} unit="%" band={riskBand(p.value)} ariaVerb="risk" />
      ))}
    </>
  );
}

export function ZoneHealthCard() {
  const { data, isLoading, error, refetch } = useExposure();

  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={4} height={42} /></div>;
  if (error) return <ErrorState title="Zone health didn't load. The analytics service returned an error." onRetry={() => refetch()} />;

  const zones = [...(data?.zones ?? [])].sort((a, b) => a.score - b.score);
  if (zones.length === 0) {
    return (
      <div style={{ padding: 28 }}>
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
      <p style={scaleNote}>Remaining headroom per network zone. Higher is better. Weakest first.</p>
      {zones.map((z) => (
        <MeterRow key={z.name} name={z.name} value={z.score} band={healthBand(z.score)} ariaVerb="health score" />
      ))}
    </>
  );
}

const scaleNote: React.CSSProperties = {
  margin: 0,
  padding: "9px 20px",
  borderBottom: "0.5px solid var(--border-subtle)",
  background: "var(--bg-surface)",
  fontFamily: "var(--font-ui)",
  fontSize: 11,
  color: "var(--text-muted)",
};
