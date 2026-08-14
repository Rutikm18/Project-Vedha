"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, UserPlus, KeyRound, ServerCog, Loader2, Check, X } from "lucide-react";

async function ca<T>(id: string, path: string, opts: { method?: string; body?: unknown } = {}): Promise<T> {
  const res = await fetch(`/api/engagements/${id}/customer-access${path}`, {
    method: opts.method ?? "GET",
    headers: { "Content-Type": "application/json" },
    body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
  });
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error((data && (data.error || data.detail)) || res.statusText);
  return data as T;
}

interface ScanReq {
  id: string; scan_type: string; status: string; note: string | null;
  requested_at: string; reviewed_by: string | null;
}
interface ClientUser { id: string; email: string; is_active: boolean; temp_password?: string | null }

export default function CustomerAccessPage() {
  const { id } = useParams<{ id: string }>();
  const qc = useQueryClient();
  const [email, setEmail] = useState("");
  const [agentId, setAgentId] = useState("");
  const [tempPw, setTempPw] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);

  const clientUser = useQuery({
    queryKey: ["ca", id, "client-user"],
    queryFn: () => ca<ClientUser | null>(id, "/client-user").catch(() => null),
  });
  const requests = useQuery({
    queryKey: ["ca", id, "scan-requests"],
    queryFn: () => ca<ScanReq[]>(id, "/scan-requests"),
  });

  const provision = useMutation({
    mutationFn: () => ca<ClientUser>(id, "/client-user", { method: "POST", body: { email } }),
    onSuccess: (u) => { setTempPw(u.temp_password ?? null); setNote("Customer login created."); qc.invalidateQueries({ queryKey: ["ca", id, "client-user"] }); },
    onError: (e: Error) => setNote(e.message),
  });
  const resetPw = useMutation({
    mutationFn: () => ca<ClientUser>(id, "/client-user", { method: "PATCH", body: { reset_password: true } }),
    onSuccess: (u) => { setTempPw(u.temp_password ?? null); setNote("Password reset."); },
    onError: (e: Error) => setNote(e.message),
  });
  const assign = useMutation({
    mutationFn: () => ca(id, "/assign-agent", { method: "PATCH", body: { agent_id: agentId } }),
    onSuccess: () => setNote("Agent assigned."),
    onError: (e: Error) => setNote(e.message),
  });
  const review = useMutation({
    mutationFn: (v: { rid: string; action: "approve" | "reject" }) =>
      ca(id, `/scan-requests/${v.rid}/${v.action}`, { method: "POST", body: v.action === "reject" ? { reason: "declined" } : {} }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ca", id, "scan-requests"] }),
    onError: (e: Error) => setNote(e.message),
  });

  const u = clientUser.data;

  return (
    <div className="mx-auto max-w-4xl px-4 py-6">
      <Link href={`/engagements/${id}`} className="mb-4 inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-800">
        <ArrowLeft className="h-4 w-4" /> Back to engagement
      </Link>
      <h1 className="text-xl font-semibold text-slate-900">Customer Access</h1>
      <p className="mb-6 text-sm text-slate-500">Provision the customer portal login, assign the probe, and review scan requests.</p>

      {note && <div className="mb-4 rounded-md bg-slate-100 px-4 py-2 text-sm text-slate-700">{note}</div>}
      {tempPw && (
        <div className="mb-4 rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-800">
          One-time password (share securely, shown once): <code className="font-mono font-semibold">{tempPw}</code>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {/* Client login */}
        <section className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-800"><UserPlus className="h-4 w-4" /> Customer login</h2>
          {u ? (
            <div className="space-y-2 text-sm">
              <div>Email: <span className="font-medium">{u.email}</span></div>
              <div>Status: {u.is_active ? "active" : "disabled"}</div>
              <button onClick={() => resetPw.mutate()} disabled={resetPw.isPending}
                className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50">
                {resetPw.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <KeyRound className="h-4 w-4" />} Reset password
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="customer@company.com"
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" />
              <button onClick={() => provision.mutate()} disabled={provision.isPending || !email}
                className="inline-flex items-center gap-1.5 rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60">
                {provision.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <UserPlus className="h-4 w-4" />} Provision login
              </button>
            </div>
          )}
        </section>

        {/* Assign agent */}
        <section className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-800"><ServerCog className="h-4 w-4" /> Assigned probe</h2>
          <input value={agentId} onChange={(e) => setAgentId(e.target.value)} placeholder="agent UUID"
            className="mb-2 w-full rounded-md border border-slate-300 px-3 py-2 text-sm" />
          <button onClick={() => assign.mutate()} disabled={assign.isPending || !agentId}
            className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-60">
            {assign.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <ServerCog className="h-4 w-4" />} Assign
          </button>
        </section>
      </div>

      {/* Scan-request inbox */}
      <section className="mt-6 rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-sm font-semibold text-slate-800">Scan requests</h2>
        {requests.isLoading ? (
          <div className="flex items-center gap-2 text-sm text-slate-500"><Loader2 className="h-4 w-4 animate-spin" /> Loading…</div>
        ) : (requests.data ?? []).length === 0 ? (
          <p className="text-sm text-slate-400">No scan requests.</p>
        ) : (
          <div className="divide-y divide-slate-100">
            {(requests.data ?? []).map((r) => (
              <div key={r.id} className="flex items-center justify-between py-2 text-sm">
                <div>
                  <span className="font-medium capitalize">{r.scan_type.replace(/_/g, " ")}</span>
                  <span className="ml-2 capitalize text-slate-500">{r.status}</span>
                  <span className="ml-2 text-xs text-slate-400">{new Date(r.requested_at).toLocaleString()}</span>
                </div>
                {r.status === "pending" && (
                  <div className="flex gap-2">
                    <button onClick={() => review.mutate({ rid: r.id, action: "approve" })}
                      className="inline-flex items-center gap-1 rounded-md bg-emerald-600 px-2.5 py-1 text-xs font-semibold text-white hover:bg-emerald-700">
                      <Check className="h-3.5 w-3.5" /> Approve
                    </button>
                    <button onClick={() => review.mutate({ rid: r.id, action: "reject" })}
                      className="inline-flex items-center gap-1 rounded-md border border-slate-300 px-2.5 py-1 text-xs hover:bg-slate-50">
                      <X className="h-3.5 w-3.5" /> Reject
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
