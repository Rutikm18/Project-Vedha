"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Loader2, Radar, CheckCircle2, AlertTriangle } from "lucide-react";
import { portalApi, type PortalScan } from "../../../lib/portal-client";

const STATUS_STYLE: Record<string, string> = {
  pending: "bg-amber-100 text-amber-700",
  approved: "bg-sky-100 text-sky-700",
  rejected: "bg-red-100 text-red-700",
  running: "bg-indigo-100 text-indigo-700",
  completed: "bg-emerald-100 text-emerald-700",
  failed: "bg-red-100 text-red-700",
};

export default function PortalScans() {
  const qc = useQueryClient();
  const q = useQuery({ queryKey: ["portal", "scans"], queryFn: () => portalApi<PortalScan[]>("/scans") });
  const [msg, setMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);

  const requestScan = useMutation({
    mutationFn: () => portalApi("/scan-requests", { method: "POST", body: { scan_type: "vuln_scan" } }),
    onSuccess: () => {
      setMsg({ type: "ok", text: "Scan requested — pending review by your security team." });
      qc.invalidateQueries({ queryKey: ["portal", "scans"] });
    },
    onError: (e: Error) => setMsg({ type: "err", text: e.message }),
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-900">Scans</h1>
        <button
          onClick={() => requestScan.mutate()}
          disabled={requestScan.isPending}
          className="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60"
        >
          {requestScan.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Radar className="h-4 w-4" />}
          Request scan
        </button>
      </div>

      {msg && (
        <div className={`flex items-center gap-2 rounded-md px-4 py-3 text-sm ${msg.type === "ok" ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-800"}`}>
          {msg.type === "ok" ? <CheckCircle2 className="h-4 w-4" /> : <AlertTriangle className="h-4 w-4" />}
          {msg.text}
        </div>
      )}

      {q.isLoading ? (
        <div className="flex items-center gap-2 text-slate-500"><Loader2 className="h-4 w-4 animate-spin" /> Loading scans…</div>
      ) : q.isError ? (
        <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">{(q.error as Error).message}</div>
      ) : (q.data ?? []).length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-white py-16 text-center">
          <Radar className="h-8 w-8 text-slate-300" />
          <p className="mt-3 text-sm font-medium text-slate-700">No scans yet</p>
          <p className="text-sm text-slate-400">Request a scan and it will show here once your team approves it.</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2.5">Type</th>
                <th className="px-4 py-2.5">Kind</th>
                <th className="px-4 py-2.5">Status</th>
                <th className="px-4 py-2.5">When</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(q.data ?? []).map((s) => (
                <tr key={`${s.kind}-${s.id}`} className="hover:bg-slate-50">
                  <td className="px-4 py-3 capitalize text-slate-900">{s.scan_type.replace(/_/g, " ")}</td>
                  <td className="px-4 py-3 capitalize text-slate-500">{s.kind === "request" ? "Request" : "Scan job"}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium capitalize ${STATUS_STYLE[s.status] ?? "bg-slate-100 text-slate-600"}`}>
                      {s.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-500">{s.at ? new Date(s.at).toLocaleString() : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
