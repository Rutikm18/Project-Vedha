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
 * states its direction in the header, each row carries a word for its band,
 * and colour is never the only cue.
 *
 * The band a protocol row shows now comes from the SERVER'S severity, not from
 * thresholding the meter number. It used to be thresholded at 85/65/45 against
 * severity weights of 100/70/40/15/5 — so no value could ever land in the
 * "Elevated" band (45-64) and a MEDIUM finding was labelled "Contained". Reading
 * the severity directly removes the second, contradictory severity scale.
 *
 * ProtocolRow.tsx and ZoneRow.tsx are superseded by MeterRow below.
 */
import React from "react";
import { Activity, Shield, Info } from "lucide-react";
import { useConsoleQuery } from "../../lib/console-source";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { Meter } from "../console/Primitives";
import { SEVERITY, toSeverity } from "../../lib/severity";

interface Protocol {
  name: string;
  /** Worst severity attributable to this service; null = nothing found on it. */
  severity: string | null;
  /** Severity weight 0-100. Meter length only — never the band label. */
  value: number;
  findings: number;
  assets: number;
}
interface Zone {
  name: string;
  score: number;
  assets: number;
  affected: number;
}
interface Exposure {
  protocols: Protocol[];
  zones: Zone[];
  /** Open findings naming no port, so they can't be charged to a protocol. */
  unattributedFindings: number;
}

export function useExposure() {
  return useConsoleQuery<Exposure>("exposure", {
    refetchInterval: 60_000,
  });
}

/* --------------------------------------------------------------- banding */

/** Protocol: the band IS the worst finding's severity. No second scale. */
function protocolBand(severity: string | null) {
  if (!severity) return { color: "var(--nominal-color)", word: "Clean" };
  const m = SEVERITY[toSeverity(severity)];
  return { color: m.color, word: m.label };
}

/** Health: higher is better. */
function healthBand(v: number) {
  if (v >= 90) return { color: "var(--nominal-color)", word: "Healthy" };
  if (v >= 75) return { color: "var(--accent)", word: "Stable" };
  if (v >= 60) return { color: "var(--sev-medium-color)", word: "Watch" };
  return { color: "var(--sev-critical-color)", word: "Degraded" };
}

function plural(n: number, one: string, many = `${one}s`) {
  return `${n} ${n === 1 ? one : many}`;
}

/* -------------------------------------------------------------- MeterRow */

function MeterRow({
  name, band, readout, meterValue, sub, ariaLabel,
}: {
  name: string;
  band: { color: string; word: string };
  /** Right-aligned figure — the concrete count the row rests on. */
  readout: string;
  /** 0–100 bar length. */
  meterValue: number;
  sub?: string;
  ariaLabel: string;
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
        <span style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)", color: band.color, fontWeight: 600, flexShrink: 0 }}>{band.word}</span>
        <span
          className="num-mono"
          style={{ marginLeft: "auto", fontSize: "var(--fs-label)", fontWeight: 600, color: "var(--text-muted)", flexShrink: 0 }}
        >
          {readout}
        </span>
      </div>
      <Meter value={meterValue} color={band.color} height={4} ticks label={ariaLabel} />
      {sub && (
        <span style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)", color: "var(--text-muted)" }}>{sub}</span>
      )}
    </div>
  );
}

/** A one-line caveat under a panel — says what the panel is NOT showing. */
function PanelNote({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      display: "flex", alignItems: "flex-start", gap: "var(--space-2)",
      padding: "var(--space-3) var(--space-5)",
      borderTop: "var(--hairline) solid var(--border-subtle)",
      fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)",
      color: "var(--text-muted)", lineHeight: 1.5,
    }}>
      <Info size={12} style={{ flexShrink: 0, marginTop: 2 }} aria-hidden />
      <span>{children}</span>
    </div>
  );
}

/* ------------------------------------------------------------------ cards */

const CAP = 6;

export function ProtocolRiskCard() {
  const { data, isLoading, error, refetch } = useExposure();
  // Hooks must run unconditionally — declare state BEFORE any early return
  // (isLoading/error), or the hook count changes between renders (React #310).
  const [showAll, setShowAll] = React.useState(false);

  if (isLoading) return <div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={51} /></div>;
  if (error) return <ErrorState title="Protocol risk didn't load. The analytics service returned an error." onRetry={() => refetch()} />;

  const protocols = data?.protocols ?? [];   // server sorts worst-first
  const unattributed = data?.unattributedFindings ?? 0;
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
      {visible.map((p) => {
        const band = protocolBand(p.severity);
        return (
          <MeterRow
            key={p.name}
            name={p.name}
            band={band}
            readout={p.findings > 0 ? plural(p.findings, "finding") : "—"}
            meterValue={p.value}
            sub={`Exposed on ${plural(p.assets, "asset")}`}
            ariaLabel={
              p.severity
                ? `${p.name}: worst finding ${band.word}, ${plural(p.findings, "finding")} on ${plural(p.assets, "asset")}`
                : `${p.name}: no findings, exposed on ${plural(p.assets, "asset")}`
            }
          />
        );
      })}
      {protocols.length > CAP && (
        <ShowAllButton showAll={showAll} onClick={() => setShowAll((v) => !v)} total={protocols.length} />
      )}
      {unattributed > 0 && (
        <PanelNote>
          {plural(unattributed, "open finding")} {unattributed === 1 ? "is" : "are"} not tied
          to a listening service, so {unattributed === 1 ? "it is" : "they are"} not counted
          here. They still appear in Findings.
        </PanelNote>
      )}
    </>
  );
}

export function ZoneHealthCard() {
  const { data, isLoading, error, refetch } = useExposure();
  const [showAll, setShowAll] = React.useState(false);   // unconditional — before early returns (React #310)

  if (isLoading) return <div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={51} /></div>;
  if (error) return <ErrorState title="Zone health didn't load. The analytics service returned an error." onRetry={() => refetch()} />;

  const zones = data?.zones ?? [];   // server sorts weakest-first
  const visible = showAll ? zones : zones.slice(0, CAP);
  // Every untagged asset lands in one "UNZONED" bucket, so the empty state below
  // could never fire while assets existed — the panel showed a single
  // meaningless bar instead of the advice that would make it useful.
  const onlyUnzoned = zones.length === 1 && zones[0].name === "UNZONED";

  if (zones.length === 0) {
    return (
      <div style={{ padding: "var(--space-6)" }}>
        <EmptyState
          icon={Shield}
          title="No assets yet"
          hint="Zone health appears once discovery finds assets to group."
        />
      </div>
    );
  }

  return (
    <>
      {visible.map((z) => {
        const band = healthBand(z.score);
        return (
          <MeterRow
            key={z.name}
            name={z.name}
            band={band}
            readout={String(z.score)}
            meterValue={z.score}
            sub={
              z.affected > 0
                ? `${z.affected} of ${plural(z.assets, "asset")} with open findings`
                : `${plural(z.assets, "asset")}, all clear`
            }
            ariaLabel={`${z.name}: health score ${z.score} out of 100 — ${band.word}, ${z.affected} of ${z.assets} assets with open findings`}
          />
        );
      })}
      {zones.length > CAP && (
        <ShowAllButton showAll={showAll} onClick={() => setShowAll((v) => !v)} total={zones.length} />
      )}
      {onlyUnzoned && (
        <PanelNote>
          None of your assets carry an environment tag, so they are all in one
          bucket. Tag them (prod, dmz, corp…) to see health per zone.
        </PanelNote>
      )}
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
