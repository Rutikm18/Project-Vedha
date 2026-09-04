"use client";

/**
 * Portal → Probe. The customer's view of the scanning probe assigned to their
 * engagement.
 *
 * Intentionally NOT the operator /fleet screen. That one manages a tenant's
 * whole fleet — enrollment requests, tokens, capabilities, job dispatch — none
 * of which a customer may see or do. What a customer legitimately needs is
 * narrower and answers one question: *is the thing that scans my network
 * working right now, and when did it last check in?*
 *
 * The backing route (/portal/agents) projects only those fields; enrollment
 * secrets, signing keys and hardware identifiers never leave the operator side.
 */

import { useQuery } from "@tanstack/react-query";
import {
  Activity, Cpu, Info, MapPin, ServerCog,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { Timestamp } from "../../../components/portal/Timestamp";
import { portalApi, usePortalEngagement } from "../../../lib/portal-client";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";

interface PortalAgent {
  id: string;
  name: string;
  status: "ONLINE" | "BUSY" | "OFFLINE" | string;
  activity: string;
  location: string | null;
  last_heartbeat: string | null;
}

const STATUS: Record<string, { color: string; label: string; pulse: boolean }> = {
  ONLINE:  { color: "var(--nominal-color)", label: "Online",  pulse: false },
  BUSY:    { color: "var(--state-busy)",    label: "Scanning", pulse: true },
  OFFLINE: { color: "var(--text-muted)",    label: "Offline", pulse: false },
};

export default function PortalFleet() {
  const agents = useQuery({
    queryKey: ["portal", "agents"],
    queryFn: () => portalApi<PortalAgent[]>("/agents"),
    refetchInterval: 15_000,
  });
  const eng = usePortalEngagement();

  const list = agents.data ?? [];
  const online = list.filter((a) => a.status === "ONLINE" || a.status === "BUSY").length;

  const statusItems = [{
    label: "PROBE",
    value: agents.isLoading ? "—" : list.length === 0 ? "NONE" : `${online}/${list.length}`,
    color: online > 0 ? "var(--accent)" : "var(--text-faint)",
  }];

  return (
    <PortalShell
      title="Probe"
      subtitle={eng.data?.name ?? "The scanner assigned to your network"}
      statusItems={statusItems}
      live={list.some((a) => a.status === "BUSY")}
    >
      <div className="panel">
        <div className="panel-head" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <ServerCog size={15} style={{ color: "var(--accent)" }} />
          <h2 className="panel-title">Assigned probe</h2>
        </div>

        <DataState
          loading={agents.isLoading}
          error={agents.error}
          isEmpty={!agents.isLoading && list.length === 0}
          onRetry={() => agents.refetch()}
          skeleton={<div style={{ padding: 16 }}><SkeletonRows rows={2} /></div>}
          empty={
            <EmptyState
              icon={Cpu}
              title="No probe assigned yet"
              hint="Your security team assigns a probe to your engagement before the first scan can run. Contact them if you were expecting one."
            />
          }
        >
          <div>
            {list.map((a) => {
              const st = STATUS[a.status] ?? STATUS.OFFLINE;
              return (
                <div key={a.id} className="console-row"
                  style={{ display: "flex", alignItems: "center", gap: 12, padding: "14px 16px" }}>
                  <span
                    aria-hidden
                    style={{
                      width: 8, height: 8, borderRadius: 999, flexShrink: 0,
                      background: st.color,
                      boxShadow: st.pulse
                        ? `0 0 0 3px color-mix(in srgb, ${st.color} 22%, transparent)` : "none",
                    }}
                  />
                  <div style={{ minWidth: 0, flex: 1 }}>
                    <div style={{ fontWeight: 500, color: "var(--text-primary)" }}>{a.name}</div>
                    <div className="muted" style={{ fontSize: 12, marginTop: 1 }}>{a.activity}</div>
                  </div>
                  {a.location && (
                    <div className="muted" style={{ fontSize: 12, display: "flex",
                                                    alignItems: "center", gap: 4 }}>
                      <MapPin size={11} /> {a.location}
                    </div>
                  )}
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 12, color: st.color }}>{st.label}</div>
                    <div className="muted" style={{ fontSize: 11 }}>
                      last seen <Timestamp value={a.last_heartbeat} relative />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </DataState>
      </div>

      <div className="panel" style={{ marginTop: 16 }}>
        <div className="panel-head" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Activity size={15} style={{ color: "var(--accent)" }} />
          <h2 className="panel-title">What the probe does</h2>
        </div>
        <ul className="muted" style={{ fontSize: 13, lineHeight: 1.75,
                                       padding: "14px 16px 16px 34px", margin: 0 }}>
          <li>
            It runs inside your network and scans only the ranges on your{" "}
            <a href="/portal/scope" style={{ color: "var(--accent)" }}>Scope</a> page.
          </li>
          <li>It collects evidence and sends it here; all analysis happens on our side.</li>
          <li>
            {eng.data?.has_assigned_agent
              ? "Offline simply means it is not currently reachable — scheduled scans resume when it reconnects."
              : "Until a probe is assigned, scan requests will queue rather than run."}
          </li>
        </ul>
      </div>

      <p className="muted" style={{ fontSize: 12, marginTop: 12, display: "flex",
                                    gap: 6, alignItems: "center" }}>
        <Info size={12} /> Probe enrollment and configuration are managed by your security team.
      </p>
    </PortalShell>
  );
}
