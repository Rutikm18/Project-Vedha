"use client";

/**
 * Portal → Scope. The authorised targets, promoted out of the Settings page into
 * a page of its own so a customer can answer "what are you allowed to touch?"
 * without hunting for it.
 *
 * READ-ONLY BY DESIGN, and that is a security boundary rather than an omission.
 * Scope is the authorisation record for active scanning: if a customer could
 * widen it themselves the platform would scan ranges nobody verified they own.
 * Changes go through the security team, exactly as the Settings copy already
 * promised — this page states the boundary instead of leaving it implicit.
 */

import { useQuery } from "@tanstack/react-query";
import {
  Building2, Info, Lock, ShieldCheck, Target,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { portalApi, usePortalEngagement, type PortalScan } from "../../../lib/portal-client";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";

/** Split a CIDR so the prefix can be de-emphasised against the network part. */
function splitCidr(cidr: string): [string, string] {
  const i = cidr.lastIndexOf("/");
  return i === -1 ? [cidr, ""] : [cidr.slice(0, i), cidr.slice(i)];
}

/** Usable host count for an IPv4 CIDR; null for IPv6 or anything unparseable — a
 *  /64 holds 2**64 addresses and printing that number helps nobody. */
function hostCount(cidr: string): number | null {
  const m = /^(\d{1,3}(?:\.\d{1,3}){3})\/(\d{1,2})$/.exec(cidr.trim());
  if (!m) return null;
  const bits = Number(m[2]);
  if (bits < 0 || bits > 32) return null;
  if (bits >= 31) return 2 ** (32 - bits);
  return 2 ** (32 - bits) - 2;              // minus network + broadcast
}

function Kpi({ label, value, hint }: { label: string; value: React.ReactNode; hint?: string }) {
  return (
    <div className="panel" style={{ padding: 16 }}>
      <div className="eyebrow">{label}</div>
      <div className="num" style={{ marginTop: 4, fontSize: 26, fontWeight: 600 }}>{value}</div>
      {hint && <div style={{ marginTop: 2, fontSize: 11, color: "var(--text-faint)" }}>{hint}</div>}
    </div>
  );
}

export default function PortalScope() {
  const eng = usePortalEngagement();
  const scans = useQuery({
    queryKey: ["portal", "scans"],
    queryFn: () => portalApi<PortalScan[]>("/scans"),
  });

  const cidrs = eng.data?.scope_cidrs ?? [];
  const total = cidrs.reduce<number | null>((acc, c) => {
    if (acc === null) return null;
    const n = hostCount(c);
    return n === null ? null : acc + n;
  }, 0);
  const lastScan = scans.data?.[0];

  return (
    <PortalShell
      title="Scope"
      subtitle={eng.data?.name ?? "The network ranges your security team has authorised us to assess."}
    >
      {/* the authorisation boundary, stated before anything else */}
      <div className="panel" style={{ display: "flex", gap: 12, alignItems: "flex-start", padding: 16 }}>
        <Lock size={16} style={{ color: "var(--accent)", flexShrink: 0, marginTop: 2 }} />
        <div>
          <strong style={{ display: "block", marginBottom: 3 }}>Managed by your security team</strong>
          <span className="muted" style={{ fontSize: 13, lineHeight: 1.55 }}>
            Scope is the authorisation record for active scanning, so it is read-only here.
            Nothing outside these ranges is ever probed. To add or remove a range, contact
            your security team — they verify ownership before it takes effect.
          </span>
        </div>
      </div>

      <div style={{ display: "grid", gap: 12, marginTop: 16,
                    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))" }}>
        <Kpi label="Authorised ranges" value={eng.data ? eng.data.scope_cidr_count : "—"} />
        <Kpi label="Addresses in scope"
             value={total === null ? "—" : total.toLocaleString()}
             hint={total === null ? "IPv6 range present — not counted" : undefined} />
        <Kpi label="Engagement"
             value={<span style={{ textTransform: "capitalize" }}>{eng.data?.status ?? "—"}</span>} />
        <Kpi label="Probe assigned"
             value={eng.data ? (eng.data.has_assigned_agent ? "Yes" : "Not yet") : "—"} />
      </div>

      <div className="panel" style={{ marginTop: 16 }}>
        <div className="panel-head" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Building2 size={15} style={{ color: "var(--accent)" }} />
          <h2 className="panel-title">{eng.data?.name ?? "Authorised network ranges"}</h2>
        </div>

        <DataState
          loading={eng.isLoading}
          error={eng.error}
          isEmpty={!eng.isLoading && cidrs.length === 0}
          onRetry={() => eng.refetch()}
          skeleton={<div style={{ padding: 16 }}><SkeletonRows rows={4} /></div>}
          empty={
            <EmptyState
              icon={Target}
              title="No ranges authorised yet"
              hint="Your security team has not added any network ranges to this engagement. Until they do, no scanning can take place."
            />
          }
        >
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", minWidth: 460, fontSize: 13, borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th className="eyebrow" style={{ textAlign: "left", padding: "10px 16px" }}>Range</th>
                  <th className="eyebrow" style={{ textAlign: "left", padding: "10px 16px" }}>Type</th>
                  <th className="eyebrow" style={{ textAlign: "right", padding: "10px 16px" }}>Addresses</th>
                </tr>
              </thead>
              <tbody>
                {cidrs.map((cidr) => {
                  const [net, prefix] = splitCidr(cidr);
                  const n = hostCount(cidr);
                  return (
                    <tr key={cidr} className="console-row">
                      <td className="num-mono" style={{ padding: "10px 16px" }}>
                        {net}<span className="muted">{prefix}</span>
                      </td>
                      <td style={{ padding: "10px 16px" }}>
                        <span className="chip">{cidr.includes(":") ? "IPv6" : "IPv4"}</span>
                      </td>
                      <td className="muted" style={{ padding: "10px 16px", textAlign: "right" }}>
                        {n === null ? "—" : n.toLocaleString()}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </DataState>
      </div>

      <div className="panel" style={{ marginTop: 16 }}>
        <div className="panel-head" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <ShieldCheck size={15} style={{ color: "var(--accent)" }} />
          <h2 className="panel-title">How scope is enforced</h2>
        </div>
        <ul className="muted" style={{ fontSize: 13, lineHeight: 1.75, padding: "14px 16px 16px 34px", margin: 0 }}>
          <li>Every probe checks each target against this list before sending a packet.</li>
          <li>A target outside these ranges is refused, and the refusal is recorded.</li>
          <li>
            Hosts found during a scan — including IPv6 neighbours on the same segment —
            are reported to you but <strong>not</strong> scanned unless they already fall
            inside an authorised range.
          </li>
          {lastScan && (
            <li>
              Most recent assessment:{" "}
              <strong>{lastScan.at ? new Date(lastScan.at).toLocaleString() : "—"}</strong>
              {lastScan.status ? <> — {lastScan.status}</> : null}
            </li>
          )}
        </ul>
      </div>

      <p className="muted" style={{ fontSize: 12, marginTop: 12, display: "flex", gap: 6, alignItems: "center" }}>
        <Info size={12} /> These are the same ranges the probes enforce — there is no second,
        hidden scope.
      </p>
    </PortalShell>
  );
}
