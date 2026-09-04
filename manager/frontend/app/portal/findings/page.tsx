"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Bug, ArrowUp, ArrowDown, ChevronDown, ChevronUp, ExternalLink, Copy, CheckCheck } from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import {
  portalApi, severityChip, SEVERITY_VAR,
  type PortalFinding, usePortalEngagement,
} from "../../../lib/portal-client";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";
import { Timestamp } from "../../../components/portal/Timestamp";

const SEVS = ["critical", "high", "medium", "low", "info"] as const;
const SEV_ORDER: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

type SortKey = "severity" | "cvss" | "risk" | "status" | "first_seen";
type SortDir = "asc" | "desc";

function SortHead({ k, label, align, sortKey, sortDir, onSort }: {
  k: SortKey; label: string; align?: "right";
  sortKey: SortKey; sortDir: SortDir; onSort: (k: SortKey) => void;
}) {
  const isActive = sortKey === k;
  const aria: "ascending" | "descending" | "none" =
    isActive ? (sortDir === "asc" ? "ascending" : "descending") : "none";
  return (
    <th aria-sort={aria} style={{ padding: 0 }}>
      <button onClick={() => onSort(k)} className="focusable" aria-label={`Sort by ${label}`}
        style={{ display: "inline-flex", alignItems: "center", gap: 4, width: "100%",
          padding: "10px 16px", background: "none", border: "none", cursor: "pointer",
          justifyContent: align === "right" ? "flex-end" : "flex-start" }}>
        <span className="eyebrow">{label}</span>
        {isActive && (sortDir === "asc"
          ? <ArrowUp style={{ width: 11, height: 11, color: "var(--accent)" }} />
          : <ArrowDown style={{ width: 11, height: 11, color: "var(--accent)" }} />)}
      </button>
    </th>
  );
}

function CveChip({ cve }: { cve: string }) {
  const [copied, setCopied] = useState(false);
  const nvdUrl = `https://nvd.nist.gov/vuln/detail/${cve}`;
  function copy(e: React.MouseEvent) {
    e.stopPropagation();
    navigator.clipboard.writeText(cve).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }).catch(() => {});
  }
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      padding: "2px 7px 2px 8px", borderRadius: 6,
      border: "0.5px solid var(--border-default)",
      background: "var(--bg-surface)", fontSize: 11,
      fontFamily: "var(--font-mono)", color: "var(--text-secondary)",
    }}>
      <a href={nvdUrl} target="_blank" rel="noopener noreferrer"
        onClick={(e) => e.stopPropagation()}
        style={{ color: "var(--accent)", textDecoration: "none", display: "flex",
          alignItems: "center", gap: 3 }}>
        {cve} <ExternalLink size={9} />
      </a>
      <button onClick={copy} aria-label={`Copy ${cve}`}
        style={{ background: "none", border: "none", cursor: "pointer", padding: 0,
          color: copied ? "var(--nominal-color)" : "var(--text-faint)", display: "flex" }}>
        {copied ? <CheckCheck size={10} /> : <Copy size={10} />}
      </button>
    </span>
  );
}

function FindingDetail({ f }: { f: PortalFinding }) {
  const sevColor = SEVERITY_VAR[f.severity] ?? SEVERITY_VAR.info;
  return (
    <tr>
      <td colSpan={6} style={{ padding: 0, borderBottom: "var(--hairline) solid var(--border-subtle)" }}>
        <div style={{
          borderLeft: `3px solid ${sevColor}`,
          background: `color-mix(in srgb, ${sevColor} 4%, var(--bg-surface))`,
          padding: "16px 20px 16px 20px",
          display: "flex", flexDirection: "column", gap: 14,
        }}>
          {/* Description */}
          {f.description && (
            <div>
              <div className="eyebrow" style={{ marginBottom: 6 }}>Description</div>
              <p style={{ margin: 0, fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.6 }}>
                {f.description}
              </p>
            </div>
          )}

          {/* Scores row */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
            <div>
              <div className="eyebrow" style={{ marginBottom: 3 }}>CVSS</div>
              <span className="num" style={{ fontSize: 16, fontWeight: 600,
                color: f.cvss_score !== null ? sevColor : "var(--text-muted)" }}>
                {f.cvss_score ?? "—"}
              </span>
            </div>
            <div>
              <div className="eyebrow" style={{ marginBottom: 3 }}>Risk score</div>
              <span className="num" style={{ fontSize: 16, fontWeight: 600,
                color: f.risk_score !== null ? sevColor : "var(--text-muted)" }}>
                {f.risk_score ?? "—"}
              </span>
            </div>
            <div>
              <div className="eyebrow" style={{ marginBottom: 3 }}>Status</div>
              <span style={{ fontSize: 13, color: "var(--text-secondary)", textTransform: "capitalize" }}>
                {f.status}
              </span>
            </div>
            <div>
              <div className="eyebrow" style={{ marginBottom: 3 }}>First seen</div>
              <span style={{ fontSize: 13, color: "var(--text-secondary)" }}>
                <Timestamp value={f.first_seen} relative />
              </span>
            </div>
          </div>

          {/* CVE IDs */}
          {f.cve_ids && f.cve_ids.length > 0 && (
            <div>
              <div className="eyebrow" style={{ marginBottom: 6 }}>CVE identifiers</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {f.cve_ids.map((cve) => <CveChip key={cve} cve={cve} />)}
              </div>
            </div>
          )}

          {/* Remediation */}
          {f.remediation && (
            <div>
              <div className="eyebrow" style={{ marginBottom: 6 }}>Remediation</div>
              <p style={{ margin: 0, fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.65,
                padding: "10px 14px", borderRadius: 8,
                background: "color-mix(in srgb, var(--nominal-color) 6%, var(--bg-surface))",
                borderLeft: "2px solid var(--nominal-color)" }}>
                {f.remediation}
              </p>
            </div>
          )}

          {!f.description && !f.remediation && !f.cve_ids?.length && (
            <p style={{ margin: 0, fontSize: 13, color: "var(--text-muted)" }}>
              No additional detail recorded for this finding.
            </p>
          )}
        </div>
      </td>
    </tr>
  );
}

export default function PortalFindings() {
  const q = useQuery({ queryKey: ["portal", "findings"], queryFn: () => portalApi<PortalFinding[]>("/findings") });
  const eng = usePortalEngagement();

  const [sortKey, setSortKey] = useState<SortKey>("severity");
  const [sortDir, setSortDir] = useState<SortDir>("asc");
  const [active, setActive] = useState<Set<string>>(new Set());
  const [selected, setSelected] = useState<string | null>(null);

  const all = q.data ?? [];
  const visible = all
    .filter((f) => active.size === 0 || active.has(f.severity))
    .sort((a, b) => {
      let c = 0;
      if (sortKey === "severity") c = (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9);
      else if (sortKey === "cvss") c = (a.cvss_score ?? -1) - (b.cvss_score ?? -1);
      else if (sortKey === "risk") c = (a.risk_score ?? -1) - (b.risk_score ?? -1);
      else if (sortKey === "first_seen") {
        c = (a.first_seen ? Date.parse(a.first_seen) : 0)
          - (b.first_seen ? Date.parse(b.first_seen) : 0);
      }
      else c = (a.status ?? "").localeCompare(b.status ?? "");
      return sortDir === "asc" ? c : -c;
    });

  function toggleSort(k: SortKey) {
    if (sortKey === k) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else { setSortKey(k); setSortDir(k === "severity" ? "asc" : "desc"); }
  }
  function toggleSev(s: string) {
    setActive((prev) => { const n = new Set(prev); if (n.has(s)) n.delete(s); else n.add(s); return n; });
  }
  function toggleRow(id: string) {
    setSelected((prev) => prev === id ? null : id);
  }

  return (
    <PortalShell
      title="Findings"
      subtitle={eng.data?.name ?? "Vulnerabilities in your engagement"}
      statusItems={all.length > 0 ? [{
        label: "TOTAL",
        value: String(all.length),
        color: "var(--text-secondary)",
      }, {
        label: "OPEN",
        value: String(all.filter((f) => f.status === "open" || f.status === "confirmed").length),
        color: all.some((f) => (f.severity === "critical" || f.severity === "high") && f.status === "open")
          ? "var(--sev-high-color)" : "var(--accent)",
      }] : undefined}
    >
      <DataState
        loading={q.isLoading}
        error={q.error}
        isEmpty={all.length === 0}
        onRetry={() => q.refetch()}
        onLogin={() => { window.location.href = "/portal/login"; }}
        skeleton={<div className="panel" style={{ padding: 16 }}><SkeletonRows rows={6} /></div>}
        empty={<div className="panel"><EmptyState icon={Bug} title="No findings yet"
          hint="Findings from your engagement will appear here after a scan." /></div>}
      >
        <div className="panel">
          {/* Severity filter chips */}
          <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 6,
            padding: "10px 16px", borderBottom: "var(--hairline) solid var(--border-subtle)" }}>
            <span className="eyebrow" style={{ marginRight: 2 }}>Filter</span>
            {SEVS.map((sev) => {
              const on = active.has(sev);
              const count = all.filter((f) => f.severity === sev).length;
              return (
                <button key={sev} className="legend-chip" aria-pressed={on}
                  onClick={() => toggleSev(sev)}
                  style={{ "--sev-edge": SEVERITY_VAR[sev], textTransform: "capitalize",
                    opacity: count === 0 ? 0.45 : 1 } as React.CSSProperties}>
                  <span style={{ width: 8, height: 8, borderRadius: 2, background: SEVERITY_VAR[sev] }} />
                  {sev} <span className="num" style={{ color: "var(--text-muted)" }}>{count}</span>
                </button>
              );
            })}
            {active.size > 0 && (
              <button onClick={() => setActive(new Set())} className="focusable"
                style={{ marginLeft: "auto", background: "none", border: "none", cursor: "pointer",
                  fontSize: 11, color: "var(--accent)", padding: "4px 6px", borderRadius: 6 }}>
                Clear
              </button>
            )}
          </div>

          {selected && (
            <div style={{ padding: "6px 16px 0", fontSize: 11, color: "var(--text-muted)" }}>
              Click a row to expand details · Click again to collapse
            </div>
          )}

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", minWidth: 620, fontSize: 13, borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "var(--bg-surface)" }}>
                  <SortHead k="severity" label="Severity" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
                  <th className="eyebrow" style={{ textAlign: "left", padding: "10px 16px" }}>Finding</th>
                  <SortHead k="cvss" label="CVSS" align="right" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
                  <SortHead k="risk" label="Risk" align="right" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
                  <SortHead k="status" label="Status" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
                  <SortHead k="first_seen" label="First seen" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
                </tr>
              </thead>
              <tbody>
                {visible.length === 0 ? (
                  <tr>
                    <td colSpan={6} style={{ padding: "32px 16px", textAlign: "center",
                      color: "var(--text-muted)", fontSize: 13 }}>
                      No findings match this filter.
                    </td>
                  </tr>
                ) : visible.map((f) => {
                  const isOpen = selected === f.id;
                  const sevColor = SEVERITY_VAR[f.severity] ?? SEVERITY_VAR.info;
                  return (
                    <>
                      <tr
                        key={f.id}
                        onClick={() => toggleRow(f.id)}
                        className="console-row"
                        aria-expanded={isOpen}
                        style={{
                          verticalAlign: "top",
                          cursor: "pointer",
                          background: isOpen
                            ? `color-mix(in srgb, ${sevColor} 5%, var(--bg-surface))`
                            : undefined,
                          borderLeft: isOpen ? `2px solid ${sevColor}` : "2px solid transparent",
                        }}
                      >
                        <td style={{ padding: "12px 16px" }}>
                          <span className="chip" style={{ ...severityChip(f.severity), textTransform: "capitalize" }}>
                            {f.severity}
                          </span>
                        </td>
                        <td style={{ padding: "12px 16px" }}>
                          <div style={{ fontWeight: 500, color: "var(--text-primary)" }}>{f.title}</div>
                          {f.cve_ids && f.cve_ids.length > 0 && (
                            <div style={{ marginTop: 2, fontSize: 11, color: "var(--accent)",
                              fontFamily: "var(--font-mono)" }}>
                              {f.cve_ids.slice(0, 2).join(", ")}
                              {f.cve_ids.length > 2 ? ` +${f.cve_ids.length - 2} more` : ""}
                            </div>
                          )}
                        </td>
                        <td className="num" style={{ padding: "12px 16px", textAlign: "right", color: "var(--text-secondary)" }}>
                          {f.cvss_score ?? "—"}
                        </td>
                        <td className="num" style={{ padding: "12px 16px", textAlign: "right", color: "var(--text-secondary)" }}>
                          {f.risk_score ?? "—"}
                        </td>
                        <td style={{ padding: "12px 16px", color: "var(--text-muted)", textTransform: "capitalize" }}>
                          {f.status}
                        </td>
                        <td style={{ padding: "12px 16px", color: "var(--text-secondary)", whiteSpace: "nowrap" }}>
                          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8 }}>
                            <Timestamp value={f.first_seen} relative block />
                            {isOpen
                              ? <ChevronUp size={13} style={{ color: "var(--text-faint)", flexShrink: 0 }} />
                              : <ChevronDown size={13} style={{ color: "var(--text-faint)", flexShrink: 0 }} />}
                          </div>
                        </td>
                      </tr>
                      {isOpen && <FindingDetail key={`${f.id}-detail`} f={f} />}
                    </>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </DataState>
    </PortalShell>
  );
}
