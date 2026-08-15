"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Loader2, FileText, Download } from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { portalApi, type PortalReport } from "../../../lib/portal-client";

interface ReportContent extends PortalReport {
  content: string;
}

export default function PortalReports() {
  const q = useQuery({ queryKey: ["portal", "reports"], queryFn: () => portalApi<PortalReport[]>("/reports") });
  const [open, setOpen] = useState<ReportContent | null>(null);
  const [loadingId, setLoadingId] = useState<string | null>(null);

  async function view(id: string) {
    setLoadingId(id);
    try {
      setOpen(await portalApi<ReportContent>(`/reports/${id}`));
    } finally {
      setLoadingId(null);
    }
  }

  const reports = q.data ?? [];

  return (
    <PortalShell title="Reports" subtitle="Approved assessment reports">
      {q.isLoading ? (
        <div style={{ display: "flex", alignItems: "center", gap: 8, color: "var(--text-muted)" }}>
          <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} /> Loading reports…
        </div>
      ) : q.isError ? (
        <div className="panel" style={{ padding: 16, color: "var(--sev-critical-color)" }}>
          {(q.error as Error).message}
        </div>
      ) : reports.length === 0 ? (
        <div className="panel" style={{ padding: 48, display: "flex", flexDirection: "column",
          alignItems: "center", textAlign: "center" }}>
          <FileText style={{ width: 32, height: 32, color: "var(--text-faint)" }} />
          <p style={{ marginTop: 12, fontSize: 13, fontWeight: 500, color: "var(--text-secondary)" }}>
            No reports available
          </p>
          <p style={{ fontSize: 13, color: "var(--text-muted)" }}>
            Approved reports for your engagement will appear here.
          </p>
        </div>
      ) : (
        <div className="panel">
          {reports.map((r) => (
            <div key={r.id} className="console-row" style={{ display: "flex",
              alignItems: "center", justifyContent: "space-between", padding: "12px 16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <FileText style={{ width: 20, height: 20, color: "var(--accent)" }} />
                <div>
                  <div style={{ fontSize: 13, fontWeight: 500, textTransform: "capitalize",
                    color: "var(--text-primary)" }}>
                    {r.output_type.replace(/_/g, " ")}
                  </div>
                  <div style={{ fontSize: 11, color: "var(--text-faint)" }}>
                    {new Date(r.generated_at).toLocaleString()} · {r.model}
                  </div>
                </div>
              </div>
              <button onClick={() => view(r.id)} disabled={loadingId === r.id}
                style={{ display: "inline-flex", alignItems: "center", gap: 6, borderRadius: 7,
                  border: "0.5px solid var(--border-default)", padding: "6px 12px", fontSize: 13,
                  color: "var(--text-secondary)", background: "transparent", cursor: "pointer" }}>
                {loadingId === r.id ? <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} />
                  : <Download style={{ width: 16, height: 16 }} />}
                View
              </button>
            </div>
          ))}
        </div>
      )}

      {open && (
        <div onClick={() => setOpen(null)} style={{ position: "fixed", inset: 0, zIndex: 50,
          display: "flex", alignItems: "center", justifyContent: "center",
          background: "var(--modal-backdrop)", padding: 16 }}>
          <div onClick={(e) => e.stopPropagation()} className="panel"
            style={{ display: "flex", maxHeight: "80vh", width: "100%", maxWidth: 768,
              flexDirection: "column" }}>
            <div className="panel-head" style={{ justifyContent: "space-between" }}>
              <div className="panel-title" style={{ textTransform: "capitalize" }}>
                {open.output_type.replace(/_/g, " ")}
              </div>
              <button onClick={() => setOpen(null)}
                style={{ color: "var(--text-muted)", background: "none", border: "none",
                  cursor: "pointer", fontSize: 14 }}>✕</button>
            </div>
            <pre style={{ overflow: "auto", whiteSpace: "pre-wrap", padding: "16px 18px",
              fontSize: 13, color: "var(--text-secondary)", fontFamily: "var(--font-mono)" }}>
              {open.content}
            </pre>
          </div>
        </div>
      )}
    </PortalShell>
  );
}
