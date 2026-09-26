"use client";

/**
 * SlaPolicyEditor — this engagement's remediation windows (operator only).
 *
 * Stored in the engagement's rules_of_engagement; overrides the organisation
 * policy (Settings → SLA Policy) for this engagement only. Approved extensions
 * still override both. Every due date on every surface is recomputed from it.
 */
import React, { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { SlidersHorizontal } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { DUE_SOURCE_LABEL } from "../../lib/remediation";

const SEVS = ["critical", "high", "medium", "low", "info"] as const;
type Policy = Record<`${(typeof SEVS)[number]}_hours`, number> & { source: string };

export function SlaPolicyEditor({ engagementId }: { engagementId: string }) {
  const qc = useQueryClient();
  const key = ["engagement-sla-policy", engagementId];
  const { data } = useQuery({
    queryKey: key, enabled: Boolean(engagementId),
    queryFn: () => fetchJson<Policy>(`/api/engagements/${engagementId}/sla-policy`),
  });
  // Local edits layered over the server values — no effect-driven state sync.
  const [edits, setEdits] = useState<Record<string, number>>({});
  const [open, setOpen] = useState(false);
  const value = (s: (typeof SEVS)[number]) => edits[s] ?? data?.[`${s}_hours`] ?? 0;
  const done = () => {
    setEdits({});
    void qc.invalidateQueries({ queryKey: key });
    void qc.invalidateQueries({ queryKey: ["remediation-bundles"] });
    void qc.invalidateQueries({ queryKey: ["finding-remediation"] });
  };
  const save = useMutation({
    mutationFn: () => fetchJson<Policy>(`/api/engagements/${engagementId}/sla-policy`, {
      method: "PUT", body: JSON.stringify(Object.fromEntries(SEVS.map((s) => [`${s}_hours`, value(s)]))),
    }),
    onSuccess: done,
  });
  const reset = useMutation({
    mutationFn: () => fetchJson<Policy>(`/api/engagements/${engagementId}/sla-policy`, { method: "DELETE" }),
    onSuccess: done,
  });
  if (!data) return null;

  return (
    <section className="rm-ext">
      <button type="button" className="rm-ai-diff-toggle" onClick={() => setOpen((o) => !o)} aria-expanded={open}
              style={{ all: "unset", cursor: "pointer", display: "flex", alignItems: "center", gap: 6 }}>
        <SlidersHorizontal size={14} aria-hidden />
        <strong style={{ fontSize: 12.5 }}>Due-date policy for this engagement</strong>
        <span className="rm-muted">— {DUE_SOURCE_LABEL[data.source] ?? data.source}
          {" "}({SEVS.slice(0, 4).map((s) => `${s} ${data[`${s}_hours`]}h`).join(" · ")})</span>
      </button>
      {open && (
        <form className="rm-ext-form" onSubmit={(e) => { e.preventDefault(); save.mutate(); }}>
          <p className="rm-ext-intro">
            Hours from first detection until a finding is due. Overrides the organisation policy for this engagement;
            approved extensions still win. 0 = no due date.
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(110px, 1fr))", gap: 8 }}>
            {SEVS.map((s) => (
              <label key={s}>
                <span style={{ textTransform: "capitalize" }}>{s} (hours)</span>
                <input type="number" min={0} max={8760} value={value(s)}
                       onChange={(e) => setEdits((d) => ({ ...d, [s]: Math.max(0, Math.min(8760, Number(e.target.value) || 0)) }))} />
              </label>
            ))}
          </div>
          <div className="rm-ext-actions">
            <button type="submit" className="btn btn-primary" disabled={save.isPending}>Save for this engagement</button>
            {data.source === "engagement" && (
              <button type="button" className="btn btn-secondary" disabled={reset.isPending} onClick={() => reset.mutate()}>
                Use organisation policy
              </button>
            )}
          </div>
          {(save.error || reset.error) && (
            <p className="rm-error">{String((save.error || reset.error) instanceof Error ? (save.error || reset.error)!.message : save.error || reset.error)}</p>
          )}
        </form>
      )}
    </section>
  );
}
