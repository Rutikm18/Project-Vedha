"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Loader2, Radar, AlertTriangle, ServerCog, CheckCircle2 } from "lucide-react";
import {
  portalApi,
  GRADE_STYLE,
  type PortalEngagement,
  type PortalPosture,
} from "../../lib/portal-client";

function Metric({ label, value, hint }: { label: string; value: React.ReactNode; hint?: string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</div>
      <div className="mt-1 text-2xl font-semibold text-slate-900">{value}</div>
      {hint && <div className="mt-0.5 text-xs text-slate-400">{hint}</div>}
    </div>
  );
}

export default function PortalOverview() {
  const qc = useQueryClient();
  const eng = useQuery({ queryKey: ["portal", "engagement"], queryFn: () => portalApi<PortalEngagement>("/engagement") });
  const posture = useQuery({ queryKey: ["portal", "posture"], queryFn: () => portalApi<PortalPosture>("/posture") });
  const [msg, setMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);

  const requestScan = useMutation({
    mutationFn: () => portalApi("/scan-requests", { method: "POST", body: { scan_type: "vuln_scan" } }),
    onSuccess: () => {
      setMsg({ type: "ok", text: "Scan requested — your security team will review and run it." });
      qc.invalidateQueries({ queryKey: ["portal", "scans"] });
    },
    onError: (e: Error) => setMsg({ type: "err", text: e.message }),
  });

  if (eng.isLoading || posture.isLoading) {
    return <div className="flex items-center gap-2 text-slate-500"><Loader2 className="h-4 w-4 animate-spin" /> Loading your engagement…</div>;
  }
  if (eng.isError) {
    return <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700">{(eng.error as Error).message}</div>;
  }

  const e = eng.data!;
  const p = posture.data;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">{e.name}</h1>
          <div className="mt-1 flex items-center gap-2 text-sm text-slate-500">
            <span className="rounded-full bg-slate-100 px-2 py-0.5 capitalize">{e.status}</span>
            <span>{e.scope_cidr_count} scope range{e.scope_cidr_count === 1 ? "" : "s"}</span>
            <span className="inline-flex items-center gap-1">
              <ServerCog className="h-3.5 w-3.5" />
              {e.has_assigned_agent ? "Probe assigned" : "No probe assigned yet"}
            </span>
          </div>
        </div>
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

      {p ? (
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">Security posture</h2>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <Metric label="Posture grade" value={<span className={GRADE_STYLE[p.grade] ?? ""}>{p.grade}</span>} hint={`score ${p.posture_score}/100`} />
            <Metric label="Risk index" value={p.risk_index} hint="0 = low, 100 = high" />
            <Metric label="Exploitable" value={p.exploitable_score} hint="weighted exposure" />
            <Metric label="Open findings" value={p.open_findings} />
          </div>
        </section>
      ) : (
        <div className="rounded-md bg-slate-50 px-4 py-3 text-sm text-slate-500">Posture will appear once your first scan completes.</div>
      )}
    </div>
  );
}
