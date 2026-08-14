"use client";

import { useQuery } from "@tanstack/react-query";
import { Loader2, Bug } from "lucide-react";
import { portalApi, SEVERITY_STYLE, type PortalFinding } from "../../../lib/portal-client";

const SEV_ORDER: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

export default function PortalFindings() {
  const q = useQuery({ queryKey: ["portal", "findings"], queryFn: () => portalApi<PortalFinding[]>("/findings") });

  if (q.isLoading) return <div className="flex items-center gap-2 text-slate-500"><Loader2 className="h-4 w-4 animate-spin" /> Loading findings…</div>;
  if (q.isError) return <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">{(q.error as Error).message}</div>;

  const findings = [...(q.data ?? [])].sort(
    (a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9),
  );

  if (findings.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-white py-16 text-center">
        <Bug className="h-8 w-8 text-slate-300" />
        <p className="mt-3 text-sm font-medium text-slate-700">No findings yet</p>
        <p className="text-sm text-slate-400">Findings from your engagement will appear here after a scan.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h1 className="text-xl font-semibold text-slate-900">Findings</h1>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2.5">Severity</th>
              <th className="px-4 py-2.5">Finding</th>
              <th className="px-4 py-2.5">CVSS</th>
              <th className="px-4 py-2.5">Risk</th>
              <th className="px-4 py-2.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {findings.map((f) => (
              <tr key={f.id} className="align-top hover:bg-slate-50">
                <td className="px-4 py-3">
                  <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium capitalize ring-1 ring-inset ${SEVERITY_STYLE[f.severity] ?? SEVERITY_STYLE.info}`}>
                    {f.severity}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="font-medium text-slate-900">{f.title}</div>
                  {f.cve_ids && f.cve_ids.length > 0 && (
                    <div className="mt-0.5 text-xs text-slate-400">{f.cve_ids.join(", ")}</div>
                  )}
                  {f.remediation && (
                    <div className="mt-1 text-xs text-slate-500"><span className="font-medium">Fix:</span> {f.remediation}</div>
                  )}
                </td>
                <td className="px-4 py-3 text-slate-700">{f.cvss_score ?? "—"}</td>
                <td className="px-4 py-3 text-slate-700">{f.risk_score ?? "—"}</td>
                <td className="px-4 py-3 capitalize text-slate-600">{f.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
