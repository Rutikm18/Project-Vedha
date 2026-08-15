"use client";

import { useQuery } from "@tanstack/react-query";
import { Loader2, Bug } from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { portalApi, severityChip, type PortalFinding } from "../../../lib/portal-client";

const SEV_ORDER: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

export default function PortalFindings() {
  const q = useQuery({ queryKey: ["portal", "findings"], queryFn: () => portalApi<PortalFinding[]>("/findings") });

  const findings = [...(q.data ?? [])].sort(
    (a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9),
  );

  return (
    <PortalShell title="Findings" subtitle="Vulnerabilities in your engagement">
      {q.isLoading ? (
        <div style={{ display: "flex", alignItems: "center", gap: 8, color: "var(--text-muted)" }}>
          <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} /> Loading findings…
        </div>
      ) : q.isError ? (
        <div className="panel" style={{ padding: 16, color: "var(--sev-critical-color)" }}>
          {(q.error as Error).message}
        </div>
      ) : findings.length === 0 ? (
        <div className="panel" style={{ padding: 48, display: "flex", flexDirection: "column",
          alignItems: "center", textAlign: "center" }}>
          <Bug style={{ width: 32, height: 32, color: "var(--text-faint)" }} />
          <p style={{ marginTop: 12, fontSize: 13, fontWeight: 500, color: "var(--text-secondary)" }}>
            No findings yet
          </p>
          <p style={{ fontSize: 13, color: "var(--text-muted)" }}>
            Findings from your engagement will appear here after a scan.
          </p>
        </div>
      ) : (
        <div className="panel">
          <table style={{ width: "100%", fontSize: 13, borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "var(--bg-surface)" }}>
                {["Severity", "Finding", "CVSS", "Risk", "Status"].map((h) => (
                  <th key={h} className="eyebrow" style={{ textAlign: "left", padding: "10px 16px" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {findings.map((f) => (
                <tr key={f.id} className="console-row" style={{ verticalAlign: "top" }}>
                  <td style={{ padding: "12px 16px" }}>
                    <span className="chip" style={{ ...severityChip(f.severity), textTransform: "capitalize" }}>
                      {f.severity}
                    </span>
                  </td>
                  <td style={{ padding: "12px 16px" }}>
                    <div style={{ fontWeight: 500, color: "var(--text-primary)" }}>{f.title}</div>
                    {f.cve_ids && f.cve_ids.length > 0 && (
                      <div style={{ marginTop: 2, fontSize: 11, color: "var(--text-faint)" }}>
                        {f.cve_ids.join(", ")}
                      </div>
                    )}
                    {f.remediation && (
                      <div style={{ marginTop: 4, fontSize: 11, color: "var(--text-muted)" }}>
                        <span style={{ fontWeight: 600 }}>Fix:</span> {f.remediation}
                      </div>
                    )}
                  </td>
                  <td className="num" style={{ padding: "12px 16px", color: "var(--text-secondary)" }}>{f.cvss_score ?? "—"}</td>
                  <td className="num" style={{ padding: "12px 16px", color: "var(--text-secondary)" }}>{f.risk_score ?? "—"}</td>
                  <td style={{ padding: "12px 16px", color: "var(--text-muted)", textTransform: "capitalize" }}>{f.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </PortalShell>
  );
}
