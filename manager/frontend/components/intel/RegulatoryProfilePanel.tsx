"use client";

import React, { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Check, Clock3, Landmark, Loader2, Pencil, X } from "lucide-react";
import { useToast } from "../../hooks/useToast";
import {
  createEngagementWorkspaceApi,
  type EngagementWorkspaceSurface,
} from "../../lib/engagement-workspace-api";
import {
  formatDeadline,
  SECTOR_LABEL,
  type ComplianceResponse,
  type ProfileResponse,
} from "../../lib/intel";

export function RegulatoryProfilePanel({
  engagementId, surface,
}: { engagementId: string; surface: EngagementWorkspaceSurface }) {
  const api = useMemo(() => createEngagementWorkspaceApi(surface), [surface]);
  const queryClient = useQueryClient();
  const toast = useToast();
  const [editing, setEditing] = useState(false);

  const compliance = useQuery({
    queryKey: ["compliance", surface, engagementId],
    queryFn: () => api.compliance<ComplianceResponse>(engagementId),
  });
  const options = useQuery({
    queryKey: ["engagement-profile", surface, engagementId],
    queryFn: () => api.profile<ProfileResponse>(engagementId),
    enabled: api.canEditIntel && editing,
  });

  const [sector, setSector] = useState("generic");
  const [jurisdictions, setJurisdictions] = useState<string[]>([]);

  const save = useMutation({
    mutationFn: () => api.setProfile(engagementId, { sector, jurisdictions }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["compliance", surface, engagementId] });
      void queryClient.invalidateQueries({ queryKey: ["engagement-profile", surface, engagementId] });
      toast.success("Regulatory profile saved", "The AI assistant and compliance mapping now use it.");
      setEditing(false);
    },
    onError: (error) => toast.error("Could not save profile", error instanceof Error ? error.message : "Unknown error"),
  });

  function startEditing() {
    setSector(compliance.data?.profile.sector ?? "generic");
    setJurisdictions(compliance.data?.profile.jurisdictions ?? []);
    setEditing(true);
  }

  const data = compliance.data;
  const profile = data?.profile;
  const jurisdictionNames = options.data?.options.jurisdictions ?? {};

  return (
    <article className="engagement-panel intel-profile">
      <header>
        <div><Landmark size={16} /><span>Regulatory profile</span></div>
        {api.canEditIntel && !editing && (
          <button type="button" className="intel-link" onClick={startEditing}><Pencil size={12} /> Edit</button>
        )}
      </header>
      <div className="engagement-panel-body">
        {compliance.isLoading && <span className="engagement-empty-inline">Loading regulatory profile…</span>}
        {compliance.error && <span className="engagement-empty-inline">Regulatory profile unavailable.</span>}
        {!compliance.isLoading && !compliance.error && !editing && !(data && profile) && (
          <span className="engagement-empty-inline">
            No regulatory profile is set for this engagement{api.canEditIntel ? " — choose a sector and jurisdictions with Edit." : "."}
          </span>
        )}

        {editing && (
          <div className="intel-profile-form">
            <label>
              <span className="engagement-field-label">Sector</span>
              <select value={sector} onChange={(event) => setSector(event.target.value)}>
                {(options.data?.options.sectors ?? Object.keys(SECTOR_LABEL)).map((value) => (
                  <option key={value} value={value}>{SECTOR_LABEL[value] ?? value}</option>
                ))}
              </select>
            </label>
            <fieldset>
              <legend className="engagement-field-label">Regulated in</legend>
              <div className="intel-check-grid">
                {Object.entries(jurisdictionNames).map(([code, name]) => (
                  <label key={code} className="intel-check">
                    <input
                      type="checkbox"
                      checked={jurisdictions.includes(code)}
                      onChange={(event) => setJurisdictions((current) =>
                        event.target.checked ? [...current, code] : current.filter((item) => item !== code))}
                    />
                    {name}
                  </label>
                ))}
                {options.isLoading && <span className="engagement-empty-inline">Loading options…</span>}
              </div>
            </fieldset>
            <div className="intel-editor-actions">
              <button type="button" className="btn btn-secondary" onClick={() => setEditing(false)}><X size={13} /> Cancel</button>
              <button type="button" className="btn btn-primary" disabled={save.isPending} onClick={() => save.mutate()}>
                {save.isPending ? <Loader2 size={13} className="animate-spin" /> : <Check size={13} />} Save profile
              </button>
            </div>
          </div>
        )}

        {data && profile && !editing && (
          <>
            <div className="intel-profile-summary">
              <span className="intel-tag" data-tone="sector">{SECTOR_LABEL[profile.sector] ?? profile.sector}</span>
              {profile.jurisdictions.length
                ? profile.jurisdictions.map((code) => <span key={code} className="intel-tag">{code}</span>)
                : <span className="engagement-empty-inline">No jurisdiction set — only global frameworks apply</span>}
            </div>

            {data.frameworks.length > 0 && (
              <div className="intel-section">
                <span className="engagement-field-label">Applicable regional frameworks ({data.frameworks.length})</span>
                <ul className="intel-framework-list">
                  {data.frameworks.map((fw) => (
                    <li key={fw.id} title={`${fw.source}${fw.note ? ` — ${fw.note}` : ""}`}>
                      <strong>{fw.name}</strong>
                      <small>
                        {fw.authority} · {fw.jurisdictions.join(", ")}
                        {fw.tag_triggered && " · triggered by asset tags"}
                      </small>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {data.reporting.length > 0 && (
              <div className="intel-section">
                <span className="engagement-field-label">Incident-reporting clocks, if a weakness is exploited</span>
                <ul className="intel-clock-list">
                  {data.reporting.map((clock) => (
                    <li key={`${clock.framework_id}-${clock.authority}-${clock.deadline_hours}`} title={clock.reference}>
                      <span className="intel-clock"><Clock3 size={12} /> {formatDeadline(clock.deadline_hours)}</span>
                      <div><strong>{clock.authority}</strong><small>{clock.trigger}</small></div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <p className="intel-disclaimer">{data.disclaimer}</p>
          </>
        )}
      </div>
    </article>
  );
}
