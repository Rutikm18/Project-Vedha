"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Loader2, FileText, Download } from "lucide-react";
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

  if (q.isLoading) return <div className="flex items-center gap-2 text-slate-500"><Loader2 className="h-4 w-4 animate-spin" /> Loading reports…</div>;
  if (q.isError) return <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">{(q.error as Error).message}</div>;

  const reports = q.data ?? [];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-900">Reports</h1>

      {reports.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-white py-16 text-center">
          <FileText className="h-8 w-8 text-slate-300" />
          <p className="mt-3 text-sm font-medium text-slate-700">No reports available</p>
          <p className="text-sm text-slate-400">Approved reports for your engagement will appear here.</p>
        </div>
      ) : (
        <div className="divide-y divide-slate-100 overflow-hidden rounded-lg border border-slate-200 bg-white">
          {reports.map((r) => (
            <div key={r.id} className="flex items-center justify-between px-4 py-3">
              <div className="flex items-center gap-3">
                <FileText className="h-5 w-5 text-indigo-500" />
                <div>
                  <div className="text-sm font-medium capitalize text-slate-900">{r.output_type.replace(/_/g, " ")}</div>
                  <div className="text-xs text-slate-400">{new Date(r.generated_at).toLocaleString()} · {r.model}</div>
                </div>
              </div>
              <button
                onClick={() => view(r.id)}
                disabled={loadingId === r.id}
                className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-60"
              >
                {loadingId === r.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4" />}
                View
              </button>
            </div>
          ))}
        </div>
      )}

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={() => setOpen(null)}>
          <div className="flex max-h-[80vh] w-full max-w-3xl flex-col rounded-lg bg-white shadow-xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
              <div className="text-sm font-semibold capitalize text-slate-900">{open.output_type.replace(/_/g, " ")}</div>
              <button onClick={() => setOpen(null)} className="text-slate-400 hover:text-slate-600">✕</button>
            </div>
            <pre className="overflow-auto whitespace-pre-wrap px-4 py-4 text-sm text-slate-700">{open.content}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
