"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Loader2, Radar, CheckCircle2, AlertTriangle, X, Plus,
  ChevronDown, Clock, XCircle,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { portalApi, type PortalScan, type PortalEngagement, type PortalUseCase } from "../../../lib/portal-client";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";

// Scan use-cases are fetched from the operator capability catalog (GET
// /portal/use-cases) so the portal only ever offers what the probe can run.

// UI intensity → wire intensity (probe scan-hardness knob).
const INTENSITIES: Array<{ value: string; label: string; hint: string }> = [
  { value: "light", label: "Light", hint: "top ports · gentle timing" },
  { value: "standard", label: "Normal", hint: "balanced (default)" },
  { value: "deep", label: "Thorough", hint: "full ports · aggressive" },
];

// Light client-side sanity check (backend is authoritative for scope). Accepts an
// IPv4/IPv6 address, a CIDR, or an a-b range.
function looksLikeTarget(v: string): boolean {
  const s = v.trim();
  if (!s) return false;
  const ipv4 = /^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$/;
  const range = /^(\d{1,3}\.){3}\d{1,3}\s*-\s*(\d{1,3}\.){3}\d{1,3}$/;
  const ipv6 = /^[0-9a-fA-F:]+(\/\d{1,3})?$/;
  return ipv4.test(s) || range.test(s) || (s.includes(":") && ipv6.test(s));
}

// ── Customer-facing job status model ────────────────────────────────────────
const PHASES = ["Requested", "Approved", "Running", "Complete"] as const;

interface JobMeta {
  label: string;
  color: string;
  explain: string;
  phaseIdx: number;               // index into PHASES for the ticker
  active: boolean;                // still in flight → show under "Active" + poll
  terminal: "ok" | "bad" | null;  // completed / failed|rejected / in-progress
}

function jobMeta(status: string, kind: string): JobMeta {
  switch (status) {
    case "pending":
      return kind === "request"
        ? { label: "Pending review", color: "var(--sev-medium-color)", phaseIdx: 0, active: true, terminal: null,
            explain: "Waiting for your security team to review and approve this request." }
        : { label: "Queued", color: "var(--sev-info-color)", phaseIdx: 1, active: true, terminal: null,
            explain: "Approved and queued — it will start on the next available window." };
    case "approved":
      return { label: "Approved", color: "var(--sev-info-color)", phaseIdx: 1, active: true, terminal: null,
        explain: "Approved by your security team and queued to run." };
    case "running":
      return { label: "Running", color: "var(--accent)", phaseIdx: 2, active: true, terminal: null,
        explain: "The scan is running now. This view refreshes automatically." };
    case "completed":
      return { label: "Completed", color: "var(--nominal-color)", phaseIdx: 3, active: false, terminal: "ok",
        explain: "The scan finished. Any new findings appear in Findings and Reports." };
    case "failed":
      return { label: "Failed", color: "var(--sev-critical-color)", phaseIdx: -1, active: false, terminal: "bad",
        explain: "The scan didn't finish. Your security team has been notified." };
    case "rejected":
      return { label: "Not approved", color: "var(--sev-critical-color)", phaseIdx: -1, active: false, terminal: "bad",
        explain: "Your security team did not approve this request." };
    default:
      return { label: status, color: "var(--text-muted)", phaseIdx: 0, active: false, terminal: null, explain: "" };
  }
}

function relTime(iso: string | null): string {
  if (!iso) return "—";
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return "—";
  const s = Math.floor((Date.now() - t) / 1000);
  if (s < 60) return "just now";
  const m = Math.floor(s / 60); if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60); if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24); if (d < 30) return `${d}d ago`;
  return new Date(iso).toLocaleDateString();
}

const prettyType = (s: string) => s.replace(/_/g, " ");

function StatusIcon({ status, color }: { status: string; color: string }) {
  const st = { width: 15, height: 15, color } as React.CSSProperties;
  if (status === "running") return <Loader2 className="animate-spin" style={st} />;
  if (status === "completed") return <CheckCircle2 style={st} />;
  if (status === "failed" || status === "rejected") return <XCircle style={st} />;
  return <Clock style={st} />;
}

function PhaseTicker({ phaseIdx }: { phaseIdx: number }) {
  return (
    <div style={{ marginTop: 8 }}>
      <div style={{ display: "flex", alignItems: "center" }}>
        {PHASES.map((p, i) => {
          const done = i < phaseIdx, active = i === phaseIdx;
          const color = done ? "var(--nominal-color)" : active ? "var(--accent)" : "var(--border-strong)";
          return (
            <React.Fragment key={p}>
              <span style={{ width: 10, height: 10, borderRadius: "50%", flexShrink: 0, background: color,
                boxShadow: active ? "0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent)" : "none" }} />
              {i < PHASES.length - 1 && (
                <span style={{ flex: 1, height: 2, background: done ? "var(--nominal-color)" : "var(--border-subtle)" }} />
              )}
            </React.Fragment>
          );
        })}
      </div>
      <div style={{ display: "flex", marginTop: 5 }}>
        {PHASES.map((p, i) => (
          <span key={p} style={{ flex: i < PHASES.length - 1 ? 1 : "0 0 auto",
            fontSize: 9.5, color: i <= phaseIdx ? "var(--text-secondary)" : "var(--text-faint)",
            textAlign: i === PHASES.length - 1 ? "right" : "left", whiteSpace: "nowrap" }}>{p}</span>
        ))}
      </div>
    </div>
  );
}

function Field({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div>
      <dt className="eyebrow" style={{ marginBottom: 3 }}>{label}</dt>
      <dd style={{ margin: 0, fontSize: 12.5, color: "var(--text-primary)",
        fontFamily: mono ? "var(--font-mono)" : "inherit" }}>{value}</dd>
    </div>
  );
}

/* One scan — collapsed by default, expands into status ticker + detail. */
function JobCard({ scan }: { scan: PortalScan }) {
  const [open, setOpen] = useState(false);
  const m = jobMeta(scan.status, scan.kind);
  return (
    <div style={{ border: "var(--hairline) solid var(--border-subtle)", borderRadius: "var(--radius-md)",
      background: "var(--bg-panel)", overflow: "hidden",
      borderLeft: `2px solid ${m.active ? m.color : "transparent"}` }}>
      <button onClick={() => setOpen((v) => !v)} aria-expanded={open} className="focusable"
        style={{ width: "100%", display: "flex", alignItems: "center", gap: 11, padding: "11px 14px",
          background: "none", border: "none", cursor: "pointer", textAlign: "left" }}>
        <StatusIcon status={scan.status} color={m.color} />
        <span style={{ fontSize: 13, fontWeight: 550, color: "var(--text-primary)", textTransform: "capitalize" }}>
          {prettyType(scan.scan_type)}
        </span>
        <span className="chip" style={{ textTransform: "capitalize", color: m.color,
          background: `color-mix(in srgb, ${m.color} 12%, transparent)`,
          border: `var(--hairline) solid color-mix(in srgb, ${m.color} 30%, transparent)` }}>{m.label}</span>
        <span style={{ marginLeft: "auto", fontSize: 11, color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
          {relTime(scan.at)}
        </span>
        <ChevronDown size={15} color="var(--text-muted)"
          style={{ transition: "transform var(--dur-fast) var(--ease-out)",
            transform: open ? "rotate(180deg)" : "rotate(0deg)" }} />
      </button>
      {open && (
        <div className="animate-fade-in" style={{ padding: "8px 16px 16px", borderTop: "var(--hairline) solid var(--border-subtle)" }}>
          {m.terminal === null ? (
            <PhaseTicker phaseIdx={m.phaseIdx} />
          ) : (
            <div style={{ marginTop: 10, display: "inline-flex", alignItems: "center", gap: 7,
              fontSize: 12, fontWeight: 600, color: m.color }}>
              {m.terminal === "ok" ? <CheckCircle2 size={14} /> : <XCircle size={14} />} {m.label}
            </div>
          )}
          <p style={{ marginTop: 12, fontSize: 12.5, color: "var(--text-secondary)", lineHeight: 1.5 }}>{m.explain}</p>
          <dl style={{ margin: "12px 0 0", display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: 10 }}>
            <Field label="Kind" value={scan.kind === "request" ? "Scan request" : "Scan job"} />
            <Field label={scan.kind === "request" ? "Requested" : "Created"}
              value={scan.at ? new Date(scan.at).toLocaleString() : "—"} mono />
          </dl>
        </div>
      )}
    </div>
  );
}

function Group({ label, count, children }: { label: string; count: number; children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span className="eyebrow">{label}</span>
        <span className="num" style={{ fontSize: 11, color: "var(--text-faint)" }}>{count}</span>
      </div>
      {children}
    </div>
  );
}

export default function PortalScans() {
  const qc = useQueryClient();
  const eng = useQuery({ queryKey: ["portal", "engagement"], queryFn: () => portalApi<PortalEngagement>("/engagement") });
  const scans = useQuery({
    queryKey: ["portal", "scans"],
    queryFn: () => portalApi<PortalScan[]>("/scans"),
    // Poll only while something is in flight, so the running/queued state stays live.
    refetchInterval: (q) => {
      const d = q.state.data as PortalScan[] | undefined;
      return d && d.some((s) => jobMeta(s.status, s.kind).active) ? 8000 : false;
    },
  });
  const useCases = useQuery({
    queryKey: ["portal", "use-cases"],
    queryFn: () => portalApi<PortalUseCase[]>("/use-cases"),
    staleTime: 5 * 60_000,
  });

  const [useCaseId, setUseCaseId] = useState("");
  const [intensity, setIntensity] = useState("standard");
  const [note, setNote] = useState("");
  const [targets, setTargets] = useState<string[]>([]);
  const [targetInput, setTargetInput] = useState("");
  const [msg, setMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  // Default to the first *available* catalog use-case until the customer picks one
  // (never auto-select a coming-soon entry, which the <select> disables anyway).
  const ucId = useCaseId
    || useCases.data?.find((u) => u.status !== "coming_soon")?.use_case_id
    || "";
  const selectedUc = useCases.data?.find((u) => u.use_case_id === ucId);

  function addTarget() {
    const raw = targetInput.trim();
    if (!raw) return;
    // Support pasting several comma/space/newline-separated targets at once.
    const parts = raw.split(/[\s,]+/).filter(Boolean);
    const next = [...targets];
    for (const p of parts) if (!next.includes(p)) next.push(p);
    setTargets(next);
    setTargetInput("");
  }

  const invalidTargets = targets.filter((t) => !looksLikeTarget(t));

  const request = useMutation({
    mutationFn: () => portalApi("/scan-requests", {
      method: "POST",
      body: { use_case_id: ucId, intensity, targets, note: note || null },
    }),
    onSuccess: () => {
      setMsg({ type: "ok", text: "Scan requested — pending review by your security team." });
      setTargets([]); setNote("");
      qc.invalidateQueries({ queryKey: ["portal", "scans"] });
      qc.invalidateQueries({ queryKey: ["portal", "summary"] });
    },
    onError: (e: Error) => setMsg({ type: "err", text: e.message }),
  });

  const canSubmit = !!ucId && targets.length > 0 && invalidTargets.length === 0 && !request.isPending;

  const all = scans.data ?? [];
  const active = all.filter((s) => jobMeta(s.status, s.kind).active);
  const history = all.filter((s) => !jobMeta(s.status, s.kind).active);

  return (
    <PortalShell title="Scans" subtitle="Request a scan and track activity" live={active.length > 0}>
      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "minmax(0, 1fr)" }}>
        {/* ── New request ── */}
        <div className="panel">
          <div className="panel-head"><h2 className="panel-title">Request a scan</h2></div>
          <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 14 }}>
            {msg && (
              <div role={msg.type === "ok" ? "status" : "alert"} aria-live="polite"
                style={{ display: "flex", alignItems: "center", gap: 8, borderRadius: 8,
                padding: "9px 11px", fontSize: 13,
                color: msg.type === "ok" ? "var(--nominal-color)" : "var(--sev-high-color)",
                background: `color-mix(in srgb, ${msg.type === "ok" ? "var(--nominal-color)" : "var(--sev-high-color)"} 10%, transparent)` }}>
                {msg.type === "ok" ? <CheckCircle2 style={{ width: 16, height: 16 }} />
                  : <AlertTriangle style={{ width: 16, height: 16 }} />}
                {msg.text}
              </div>
            )}

            <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))" }}>
              <div>
                <label htmlFor="scan-type" className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Use case</label>
                <select id="scan-type" value={ucId} onChange={(e) => setUseCaseId(e.target.value)}
                  className="input-base" disabled={useCases.isLoading || !useCases.data?.length}>
                  {useCases.isLoading && <option value="">Loading…</option>}
                  {(() => {
                    const avail = useCases.data?.filter((u) => u.status !== "coming_soon") ?? [];
                    const soon = useCases.data?.filter((u) => u.status === "coming_soon") ?? [];
                    return (
                      <>
                        {/* Active capabilities first, then a disabled "Coming soon" group. */}
                        {avail.map((u) => (
                          <option key={u.use_case_id} value={u.use_case_id}>{u.display_name}</option>
                        ))}
                        {soon.length > 0 && (
                          <optgroup label="⏳ Coming soon">
                            {soon.map((u) => (
                              <option key={u.use_case_id} value={u.use_case_id} disabled>{u.display_name}</option>
                            ))}
                          </optgroup>
                        )}
                      </>
                    );
                  })()}
                </select>
              </div>
              <div>
                <label htmlFor="scan-intensity" className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Intensity</label>
                <select id="scan-intensity" value={intensity} onChange={(e) => setIntensity(e.target.value)} className="input-base">
                  {INTENSITIES.map((t) => <option key={t.value} value={t.value}>{t.label} — {t.hint}</option>)}
                </select>
              </div>
            </div>

            {selectedUc?.description && (
              <div style={{ marginTop: -4, fontSize: 11, color: "var(--text-muted)", lineHeight: 1.5 }}>
                {selectedUc.description}
                {selectedUc.expected_runtime_hint && (
                  <span style={{ color: "var(--text-faint)" }}> · ~{selectedUc.expected_runtime_hint}</span>
                )}
              </div>
            )}

            {/* Targets */}
            <div>
              <label htmlFor="scan-targets" className="eyebrow" style={{ display: "block", marginBottom: 6 }}>
                Targets (must be within your allowed scope)
              </label>
              {eng.data && eng.data.scope_cidrs.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 8 }}>
                  <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Allowed:</span>
                  {eng.data.scope_cidrs.map((c) => (
                    <button key={c} type="button" onClick={() => {
                      if (!targets.includes(c)) setTargets([...targets, c]);
                    }}
                      className="chip num-mono" style={{ cursor: "pointer",
                        color: "var(--text-secondary)", border: "var(--hairline) solid var(--border-default)" }}>
                      {c}
                    </button>
                  ))}
                </div>
              )}
              <div style={{ display: "flex", gap: 8 }}>
                <input id="scan-targets" value={targetInput} onChange={(e) => setTargetInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTarget(); } }}
                  placeholder="10.0.1.5 · 10.0.1.0/28 · 10.0.1.10-10.0.1.20"
                  className="input-base num-mono" style={{ flex: 1 }} />
                <button type="button" onClick={addTarget} className="btn btn-secondary">
                  <Plus style={{ width: 14, height: 14 }} /> Add
                </button>
              </div>
              {targets.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
                  {targets.map((t) => {
                    const bad = !looksLikeTarget(t);
                    return (
                      <span key={t} className="chip num-mono" style={{
                        color: bad ? "var(--sev-critical-color)" : "var(--text-primary)",
                        border: `var(--hairline) solid ${bad ? "var(--sev-critical-color)" : "var(--border-default)"}`,
                        background: "var(--bg-surface)" }}>
                        {t}
                        <button type="button" aria-label={`Remove ${t}`}
                          onClick={() => setTargets(targets.filter((x) => x !== t))}
                          style={{ background: "none", border: "none", cursor: "pointer",
                            color: "inherit", display: "flex", padding: 0 }}>
                          <X style={{ width: 12, height: 12 }} />
                        </button>
                      </span>
                    );
                  })}
                </div>
              )}
              {invalidTargets.length > 0 && (
                <div role="alert" style={{ marginTop: 6, fontSize: 11, color: "var(--sev-critical-color)" }}>
                  Not a valid IP / CIDR / range: {invalidTargets.join(", ")}
                </div>
              )}
            </div>

            <div>
              <label htmlFor="scan-note" className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Note (optional)</label>
              <textarea id="scan-note" value={note} onChange={(e) => setNote(e.target.value)} rows={2}
                placeholder="Anything your security team should know…"
                className="textarea-base" />
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <button onClick={() => request.mutate()} disabled={!canSubmit} className="btn btn-primary">
                {request.isPending ? <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} />
                  : <Radar style={{ width: 16, height: 16 }} />}
                Request scan
              </button>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                Add at least one in-scope target. Your security team approves before it runs.
              </span>
            </div>
          </div>
        </div>

        {/* ── Activity: all jobs, collapsed by default, expand any one ── */}
        <div className="panel">
          <div className="panel-head" style={{ justifyContent: "space-between" }}>
            <h2 className="panel-title">Activity</h2>
            {active.length > 0 && (
              <span className="chip" style={{ display: "inline-flex", alignItems: "center", gap: 6,
                color: "var(--accent)", background: "var(--accent-ghost)", border: "var(--hairline) solid var(--border-accent)" }}>
                <span className="animate-pulse-dot" style={{ width: 6, height: 6, borderRadius: "50%",
                  background: "var(--accent)" }} />
                {active.length} active
              </span>
            )}
          </div>
          <div style={{ padding: 16 }}>
            <DataState
              loading={scans.isLoading}
              error={scans.error}
              isEmpty={all.length === 0}
              onRetry={() => scans.refetch()}
              onLogin={() => { window.location.href = "/portal/login"; }}
              skeleton={<SkeletonRows rows={4} />}
              empty={<EmptyState icon={Radar} title="No scans yet"
                hint="Request a scan above and it will show here once your team approves it." />}
            >
              <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
                {active.length > 0 && (
                  <Group label="Active" count={active.length}>
                    {active.map((s) => <JobCard key={`${s.kind}-${s.id}`} scan={s} />)}
                  </Group>
                )}
                {history.length > 0 && (
                  <Group label="History" count={history.length}>
                    {history.map((s) => <JobCard key={`${s.kind}-${s.id}`} scan={s} />)}
                  </Group>
                )}
              </div>
            </DataState>
          </div>
        </div>
      </div>
    </PortalShell>
  );
}
