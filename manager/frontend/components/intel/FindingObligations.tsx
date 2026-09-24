"use client";

import React, { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Clock3, Landmark, Loader2, Sparkles } from "lucide-react";
import { AssistantText } from "../assistant/AssistantText";
import {
  formatDeadline,
  SECTOR_LABEL,
  type ComplianceBriefResponse,
  type FindingObligationsResponse,
} from "../../lib/intel";

interface ObligationsApi {
  obligations: <T>(id: string) => Promise<T>;
  complianceBrief: <T>(id: string) => Promise<T>;
}

/** Regional obligations for one finding + an on-demand sector-expert brief. */
export function FindingObligations({
  findingId, api, surface,
}: { findingId: string; api: ObligationsApi; surface: "manager" | "portal" }) {
  const query = useQuery({
    queryKey: ["finding-obligations", surface, findingId],
    queryFn: () => api.obligations<FindingObligationsResponse>(findingId),
  });
  const [brief, setBrief] = useState<ComplianceBriefResponse | null>(null);
  const generate = useMutation({
    mutationFn: () => api.complianceBrief<ComplianceBriefResponse>(findingId),
    onSuccess: setBrief,
  });

  const data = query.data;
  if (query.isLoading) return <p className="engagement-empty-inline">Loading regional obligations…</p>;
  if (query.error || !data) return null;

  const profile = data.profile;
  return (
    <div className="finding-compliance-view intel-obligations">
      <div className="finding-section-heading">
        <div><Landmark size={15} aria-hidden /><h3>Regional obligations</h3></div>
        <span>
          {SECTOR_LABEL[profile.sector] ?? profile.sector}
          {profile.jurisdictions.length ? ` · ${profile.jurisdictions.join(", ")}` : " · no jurisdiction set"}
        </span>
      </div>

      {data.frameworks.length === 0 && (
        <p className="engagement-empty-inline">
          No regional framework applies — set the engagement&apos;s sector and jurisdictions on its Overview tab.
        </p>
      )}
      {data.frameworks.map((fw) => (
        <section key={fw.framework_id} title={`${fw.source}${fw.note ? ` — ${fw.note}` : ""}`}>
          <h4>{fw.framework} <small className="intel-muted">· {fw.authority}</small></h4>
          <p className="finding-compliance-rationale">{fw.rationale}</p>
          <ul>{fw.controls.map((control) => <li key={control}>{control}</li>)}</ul>
        </section>
      ))}

      {data.reporting.length > 0 && (
        <ul className="intel-clock-list">
          {data.reporting.map((clock) => (
            <li key={`${clock.authority}-${clock.deadline_hours}`} title={clock.reference}>
              <span className="intel-clock"><Clock3 size={12} /> {formatDeadline(clock.deadline_hours)}</span>
              <div><strong>{clock.authority}</strong><small>{clock.trigger}</small></div>
            </li>
          ))}
        </ul>
      )}

      <div className="intel-brief">
        <button type="button" className="btn btn-secondary" disabled={generate.isPending} onClick={() => generate.mutate()}>
          {generate.isPending ? <Loader2 size={13} className="animate-spin" /> : <Sparkles size={13} />}
          {brief?.content ? "Regenerate compliance brief" : "Generate compliance brief"}
        </button>
        {generate.error && <p className="intel-citation-warning">{(generate.error as Error).message}</p>}
        {brief?.error && <p className="intel-citation-warning">AI brief unavailable: {brief.error}</p>}
        {brief?.content && (
          <article className="intel-brief-body">
            <header>
              <span className="intel-skill">{brief.skill_label ?? "Security advisor"}</span>
              <small className="intel-muted">AI-generated from the obligations above · verify before relying on it</small>
            </header>
            <AssistantText content={brief.content} />
            {brief.unverified_citations.length > 0 && (
              <p className="intel-citation-warning" role="note">
                Not found in Vedha&apos;s compliance library — verify before relying on: {brief.unverified_citations.join(", ")}
              </p>
            )}
          </article>
        )}
      </div>

      <p className="intel-disclaimer">{data.disclaimer}</p>
    </div>
  );
}
