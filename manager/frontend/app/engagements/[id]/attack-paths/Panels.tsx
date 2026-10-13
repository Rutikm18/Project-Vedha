"use client";

import { AlertTriangle, ArrowRight, CheckCircle2, Info, ShieldAlert, Target } from "lucide-react";
import { SkeletonRows } from "../../../../components/states/DataState";
import {
  basisInfo, caveatSummary, capabilityLabel, emptyReasons, fixFirstSummary, freshnessInfo, riskLabel, riskShare,
  suggestedTargetsNote, techniqueLabel,
  type Analysis, type ChokeAnalysis, type ChokeTarget, type Diagnostics, type PathDetail, type PathSummary,
} from "../../../../lib/attack-paths";

// ── Beta ─────────────────────────────────────────────────────────────────────

/** Attack paths is a beta feature. Says so, and says what that means in practice:
 *  the specific limits of today's model, not a generic "may change". */
export function BetaNotice() {
  return (
    <p className="ap-fine ap-beta">
      <span className="badge badge-info">Beta</span>{" "}
      Attack paths is in beta. Routes use only findings already marked exploitable and network
      reachability inferred from addressing, so a network can show few or no routes without being safe.
      Crown jewels are the assets you mark critical. Wording, ranking and the API may change.
    </p>
  );
}

// ── What these paths do not cover ────────────────────────────────────────────

export function CoveragePanel({ analysis }: { analysis: Analysis | undefined }) {
  if (!analysis) return <SkeletonRows rows={2} height={22} />;
  if (!analysis.computed) {
    return (
      <p className="ap-fine">
        Coverage and freshness have not been recorded for these paths yet. Recompute the paths to record them.
      </p>
    );
  }
  const { confidence, items } = caveatSummary(analysis.coverage, analysis.freshness);
  return (
    <>
      <span className="ap-confidence">
        {confidence === "observed" ? <CheckCircle2 size={14} color="var(--nominal-color)" /> : <AlertTriangle size={14} color="var(--sev-medium-color)" />}
        <span>
          Coverage: <strong>{confidence === "observed" ? "observed" : confidence === "partial" ? "partial" : "unknown"}</strong>
          {confidence === "observed"
            ? " — hosts were seen in every range in scope. The scanned address space itself is not tracked, so this is not proof the scan was complete."
            : confidence === "partial" ? " — see below." : "."}
        </span>
      </span>
      {items.length > 0 && (
        <ul className="ap-notes">
          {items.map((c) => (
            <li key={c.text} className="ap-note" data-tone={c.tone}>
              {c.tone === "weak" ? <AlertTriangle size={14} /> : <Info size={14} />}
              <span>{c.text}</span>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

/** P4b: when no asset was marked critical, the targets were SUGGESTED (domain controllers,
 *  hypervisors, datastores). Say so, so an auto-picked target never reads as a chosen scope. */
export function SuggestedTargetsNote({ analysis }: { analysis: Analysis | undefined }) {
  if (!analysis || !analysis.computed) return null;
  const note = suggestedTargetsNote(analysis.target_selection);
  if (!note) return null;
  return (
    <p className="ap-note" data-tone="neutral">
      <Target size={14} />
      <span>{note}</span>
    </p>
  );
}

// ── An empty list, explained ─────────────────────────────────────────────────

/** A crown jewel that is itself exposed has no route to list, so an empty list is the WORST case here,
 *  not "the model had nothing to go on". Said first, before any coverage or fix advice. */
export function ExposedCallout({ targets }: { targets: Pick<ChokeTarget, "asset_id" | "label">[] }) {
  const one = targets.length === 1;
  const who = one ? targets[0].label : `${targets.length} crown jewels`;
  return (
    <div className="ap-callout" data-tone="critical" role="status">
      <h3>{who} {one ? "is" : "are"} exposed to the internet</h3>
      <p className="ap-fine" style={{ color: "var(--text-secondary)" }}>
        No route is needed: {one ? "it is" : "they are"} reachable from outside and can be exploited directly.
        Fixing other hosts does not protect {one ? "it" : "them"}; remove that exposure first.
      </p>
      <p className="ap-fine">
        That is why there are no routes to list. It is not evidence that the network is safe.
      </p>
    </div>
  );
}

export function EmptyExplainer({ diagnostics }: { diagnostics: Diagnostics | null | undefined }) {
  const reasons = emptyReasons(diagnostics);
  return (
    <div className="ap-callout" role="status">
      <h3>No attack paths were modelled</h3>
      <p className="ap-fine" style={{ color: "var(--text-secondary)" }}>
        This is not evidence that the network is safe. It means the model did not have what it needs to
        draw a route.
      </p>
      {reasons.length > 0 ? (
        <ul className="ap-reasons">
          {reasons.map((r) => (
            <li key={r.code} className="ap-reason">
              <strong>{r.title}</strong>
              <span>{r.evidence}</span>
              {r.action && <em>{r.action}</em>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="ap-fine">The backend did not say why. Recompute the paths, or check that the engagement has hosts and findings.</p>
      )}
    </div>
  );
}

// ── Fix first ────────────────────────────────────────────────────────────────

const TOP_CHOKE = 8;

export function FixFirstPanel({ choke }: { choke: ChokeAnalysis }) {
  const summary = fixFirstSummary(choke);
  if (!summary) return null;
  const ranked = choke.ranked.slice(0, TOP_CHOKE);
  return (
    <div className="ap-card-body">
      <p className="ap-headline">{summary.headline}</p>
      {summary.routes.length > 0 && (
        <ul className="ap-routes-lines">{summary.routes.map((l) => <li key={l}>{l}</li>)}</ul>
      )}
      {ranked.length > 0 ? (
        <div className="ap-table-wrap" role="region" aria-label="Fix-first ranking" tabIndex={0}>
          <table className="ap-table">
            <caption className="ap-sr">Hosts ranked by the modelled risk removed if that one host were fixed</caption>
            <thead>
              <tr><th scope="col">Host</th><th scope="col">Risk removed if fixed alone</th><th scope="col">Effect</th><th scope="col">Priority</th></tr>
            </thead>
            <tbody>
              {ranked.map((r) => {
                const share = riskShare(r, choke.targets);
                return (
                  <tr key={r.asset_id}>
                    <td className="ap-host">{r.label}</td>
                    <td>
                      <span className="ap-share">
                        <span className="ap-bar" aria-hidden="true"><span style={{ width: `${Math.round(share * 100)}%` }} /></span>
                        <span className="ap-num">{Math.round(share * 100)}%</span>
                      </span>
                    </td>
                    <td>{r.targets_cut_off_labels.length > 0
                      ? `Cuts off ${r.targets_cut_off_labels.join(", ")}`
                      : "Lowers the risk but does not cut a route off"}</td>
                    <td><span className="ap-chip" data-priority={r.remediation_priority}>{r.remediation_priority}</span></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="ap-fine">No single host stands out: no one fix lowers the modelled risk on its own.</p>
      )}
      <p className="ap-fine">
        Risk removed is the share of the modelled risk to crown jewels that disappears if only that host were
        fixed. It ranks hosts against each other; it is not a prediction that an attack would succeed.
      </p>
    </div>
  );
}

// ── The routes ───────────────────────────────────────────────────────────────

export function PathTable({
  items, selectedId, onSelect,
}: {
  items: PathSummary[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  return (
    <div className="ap-table-wrap" role="region" aria-label="Attack paths" tabIndex={0}>
      <table className="ap-table">
        <caption className="ap-sr">Attack paths, highest risk first. Select a row to see it step by step.</caption>
        <thead>
          <tr>
            <th scope="col">Risk</th><th scope="col" className="ap-route-cell">Route</th><th scope="col">Hops</th>
            <th scope="col">Evidence</th><th scope="col">Fix points</th>
          </tr>
        </thead>
        <tbody>
          {items.map((p) => {
            const fresh = freshnessInfo(p.freshness);
            const selected = p.id === selectedId;
            return (
              <tr key={p.id} className="ap-row" data-selected={selected}>
                <td className="ap-num">{riskLabel(p.risk_score)}</td>
                <td className="ap-route-cell">
                  <button type="button" className="ap-rowbtn" aria-pressed={selected}
                    aria-label={`Show route from ${p.source_label ?? "entry"} to ${p.target_label ?? "target"}`}
                    onClick={() => onSelect(p.id)}>
                    <span className="ap-host">{p.source_label ?? "—"}</span>
                    <ArrowRight size={12} className="ap-arrow" aria-hidden="true" />
                    <span className="ap-host">{p.target_label ?? "—"}</span>
                  </button>
                </td>
                <td className="ap-num">{p.hops}</td>
                <td><span className="ap-chip" data-tone={fresh.tone}>{fresh.label}</span></td>
                <td className="ap-num">{p.chokepoint_count}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ── One route, step by step ──────────────────────────────────────────────────

export function PathDetailPanel({ detail, engagementId }: { detail: PathDetail; engagementId?: string }) {
  const fresh = freshnessInfo(detail.freshness);
  return (
    <div className="ap-card-body">
      <div className="ap-hop-chips">
        <span className="ap-chip">Risk {riskLabel(detail.risk_score)}</span>
        <span className="ap-chip" data-tone={fresh.tone}>{fresh.label}</span>
        <span className="ap-chip">{detail.hops.length} step{detail.hops.length === 1 ? "" : "s"}</span>
      </div>
      {detail.nodes[0] && (
        <p className="ap-start">
          Starts at <span className="ap-host">{detail.nodes[0]}</span>, an entry point marked internet-exposed.
        </p>
      )}
      <ol className="ap-hops">
        {detail.hops.map((h, i) => {
          const basis = basisInfo(h.basis);
          return (
            <li key={`${h.from}>${h.to}>${i}`} className="ap-hop" data-step={i + 1}>
              <div className="ap-hop-route">
                <span className="ap-host">{h.from}</span>
                <ArrowRight size={12} className="ap-arrow" aria-hidden="true" />
                <span className="ap-host">{h.to}</span>
              </div>
              <div className="ap-hop-chips">
                <span className="ap-chip">{techniqueLabel(h.technique)}</span>
                {capabilityLabel(h.capability) && <span className="ap-chip" data-tone="neutral">{capabilityLabel(h.capability)}</span>}
                <span className="ap-chip" data-tone={basis.tone} title={basis.caveat ?? undefined}>{basis.label}</span>
                {h.exploited && <span className="ap-chip" data-priority="high"><ShieldAlert size={11} aria-hidden="true" /> Exploits a finding{h.cvss != null ? ` · CVSS ${h.cvss}` : ""}</span>}
                {h.stale && <span className="ap-chip" data-tone="weak"><AlertTriangle size={11} aria-hidden="true" /> Not seen recently</span>}
              </div>
              {h.finding && <div className="ap-enabling-finding">
                <strong>Enabling vulnerability</strong>
                {engagementId ? <a href={`/findings?engagement=${encodeURIComponent(engagementId)}&finding=${encodeURIComponent(h.finding.id)}`}>{h.finding.title}</a> : <span>{h.finding.title}</span>}
                <span>{h.finding.severity} · {h.finding.lifecycle}{h.finding.cve_ids.length ? ` · ${h.finding.cve_ids.join(", ")}` : ""}</span>
                <p>Current finding metadata. This legacy modeled step does not establish an observed attack or a validated prerequisite bundle.</p>
              </div>}
              {!h.finding && h.finding_reference_state === "unavailable" && <p className="ap-fine">Enabling finding could not be resolved in this engagement. Inspect source evidence before using this step.</p>}
              {h.via.length > 0 && <p className="ap-fine">Via <span className="ap-host">{h.via.join(" → ")}</span></p>}
              <p className="ap-hop-text">{h.explanation}</p>
            </li>
          );
        })}
      </ol>
      {detail.chokepoints.length > 0 && (
        <p className="ap-fine">
          <Target size={12} className="ap-inline-icon" aria-hidden="true" />
          On this route and in the fix-first list: <span className="ap-host">{detail.chokepoints.join(", ")}</span>.
        </p>
      )}
    </div>
  );
}
