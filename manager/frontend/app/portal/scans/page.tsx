"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Loader2, Radar, CheckCircle2, AlertTriangle, X, Plus } from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { portalApi, type PortalScan, type PortalEngagement } from "../../../lib/portal-client";

// All active scan types the customer may request (an operator approves each one).
const SCAN_TYPES: Array<{ value: string; label: string }> = [
  { value: "discovery", label: "Discovery (host/service map)" },
  { value: "vuln_scan", label: "Vulnerability scan" },
  { value: "exploit", label: "Exploit validation" },
  { value: "ad_enum", label: "Active Directory enumeration" },
  { value: "lateral", label: "Lateral movement" },
  { value: "cloud_scan", label: "Cloud scan" },
  { value: "detection", label: "Detection validation" },
];

// UI intensity → wire intensity (probe scan-hardness knob).
const INTENSITIES: Array<{ value: string; label: string; hint: string }> = [
  { value: "light", label: "Light", hint: "top ports · gentle timing" },
  { value: "standard", label: "Normal", hint: "balanced (default)" },
  { value: "deep", label: "Thorough", hint: "full ports · aggressive" },
];

const STATUS_VAR: Record<string, string> = {
  pending: "var(--sev-medium-color)",
  approved: "var(--sev-info-color)",
  rejected: "var(--sev-critical-color)",
  running: "var(--accent)",
  completed: "var(--nominal-color)",
  failed: "var(--sev-critical-color)",
};

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

export default function PortalScans() {
  const qc = useQueryClient();
  const eng = useQuery({ queryKey: ["portal", "engagement"], queryFn: () => portalApi<PortalEngagement>("/engagement") });
  const scans = useQuery({ queryKey: ["portal", "scans"], queryFn: () => portalApi<PortalScan[]>("/scans") });

  const [scanType, setScanType] = useState("vuln_scan");
  const [intensity, setIntensity] = useState("standard");
  const [note, setNote] = useState("");
  const [targets, setTargets] = useState<string[]>([]);
  const [targetInput, setTargetInput] = useState("");
  const [msg, setMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);

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
      body: { scan_type: scanType, intensity, targets, note: note || null },
    }),
    onSuccess: () => {
      setMsg({ type: "ok", text: "Scan requested — pending review by your security team." });
      setTargets([]); setNote("");
      qc.invalidateQueries({ queryKey: ["portal", "scans"] });
      qc.invalidateQueries({ queryKey: ["portal", "summary"] });
    },
    onError: (e: Error) => setMsg({ type: "err", text: e.message }),
  });

  const canSubmit = targets.length > 0 && invalidTargets.length === 0 && !request.isPending;

  const selectStyle: React.CSSProperties = {
    width: "100%", borderRadius: 8, padding: "8px 10px", fontSize: 13,
    background: "var(--bg-app)", color: "var(--text-primary)",
    border: "0.5px solid var(--border-default)", outline: "none",
  };

  return (
    <PortalShell title="Scans" subtitle="Request a scan and track the queue">
      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "minmax(0, 1fr)" }}>
        {/* ── New request ── */}
        <div className="panel">
          <div className="panel-head"><h2 className="panel-title">Request a scan</h2></div>
          <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 14 }}>
            {msg && (
              <div style={{ display: "flex", alignItems: "center", gap: 8, borderRadius: 8,
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
                <label className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Scan type</label>
                <select value={scanType} onChange={(e) => setScanType(e.target.value)} style={selectStyle}>
                  {SCAN_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
              </div>
              <div>
                <label className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Intensity</label>
                <select value={intensity} onChange={(e) => setIntensity(e.target.value)} style={selectStyle}>
                  {INTENSITIES.map((t) => <option key={t.value} value={t.value}>{t.label} — {t.hint}</option>)}
                </select>
              </div>
            </div>

            {/* Targets */}
            <div>
              <label className="eyebrow" style={{ display: "block", marginBottom: 6 }}>
                Targets (must be within your allowed scope)
              </label>
              {eng.data && eng.data.scope_cidrs.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 8 }}>
                  <span style={{ fontSize: 11, color: "var(--text-faint)" }}>Allowed:</span>
                  {eng.data.scope_cidrs.map((c) => (
                    <button key={c} type="button" onClick={() => {
                      if (!targets.includes(c)) setTargets([...targets, c]);
                    }}
                      className="chip num-mono" style={{ cursor: "pointer",
                        color: "var(--text-secondary)", border: "0.5px solid var(--border-default)" }}>
                      {c}
                    </button>
                  ))}
                </div>
              )}
              <div style={{ display: "flex", gap: 8 }}>
                <input value={targetInput} onChange={(e) => setTargetInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTarget(); } }}
                  placeholder="10.0.1.5 · 10.0.1.0/28 · 10.0.1.10-10.0.1.20"
                  style={{ ...selectStyle, flex: 1, fontFamily: "var(--font-mono)" }} />
                <button type="button" onClick={addTarget}
                  style={{ display: "inline-flex", alignItems: "center", gap: 5, borderRadius: 8,
                    padding: "0 12px", fontSize: 13, border: "0.5px solid var(--border-default)",
                    background: "var(--bg-surface)", color: "var(--text-secondary)", cursor: "pointer" }}>
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
                        border: `0.5px solid ${bad ? "var(--sev-critical-color)" : "var(--border-default)"}`,
                        background: "var(--bg-surface)" }}>
                        {t}
                        <button type="button" onClick={() => setTargets(targets.filter((x) => x !== t))}
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
                <div style={{ marginTop: 6, fontSize: 11, color: "var(--sev-critical-color)" }}>
                  Not a valid IP / CIDR / range: {invalidTargets.join(", ")}
                </div>
              )}
            </div>

            <div>
              <label className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Note (optional)</label>
              <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={2}
                placeholder="Anything your security team should know…"
                style={{ ...selectStyle, resize: "vertical" }} />
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <button onClick={() => request.mutate()} disabled={!canSubmit}
                style={{ display: "inline-flex", alignItems: "center", gap: 8, borderRadius: 8,
                  padding: "9px 16px", fontSize: 13, fontWeight: 600, color: "#fff",
                  background: "var(--accent)", border: "none",
                  cursor: canSubmit ? "pointer" : "default", opacity: canSubmit ? 1 : 0.55 }}>
                {request.isPending ? <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} />
                  : <Radar style={{ width: 16, height: 16 }} />}
                Request scan
              </button>
              <span style={{ fontSize: 11, color: "var(--text-faint)" }}>
                Add at least one in-scope target. Your security team approves before it runs.
              </span>
            </div>
          </div>
        </div>

        {/* ── Queue / history ── */}
        <div className="panel">
          <div className="panel-head"><h2 className="panel-title">Queue &amp; history</h2></div>
          {scans.isLoading ? (
            <div style={{ padding: 16, display: "flex", alignItems: "center", gap: 8, color: "var(--text-muted)" }}>
              <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} /> Loading scans…
            </div>
          ) : (scans.data ?? []).length === 0 ? (
            <div style={{ padding: 48, display: "flex", flexDirection: "column", alignItems: "center",
              textAlign: "center" }}>
              <Radar style={{ width: 32, height: 32, color: "var(--text-faint)" }} />
              <p style={{ marginTop: 12, fontSize: 13, fontWeight: 500, color: "var(--text-secondary)" }}>No scans yet</p>
              <p style={{ fontSize: 13, color: "var(--text-muted)" }}>Request a scan and it will show here once your team approves it.</p>
            </div>
          ) : (
            <table style={{ width: "100%", fontSize: 13, borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "var(--bg-surface)" }}>
                  {["Type", "Kind", "Status", "When"].map((h) => (
                    <th key={h} className="eyebrow" style={{ textAlign: "left", padding: "10px 16px" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(scans.data ?? []).map((s) => (
                  <tr key={`${s.kind}-${s.id}`} className="console-row">
                    <td style={{ padding: "12px 16px", textTransform: "capitalize", color: "var(--text-primary)" }}>
                      {s.scan_type.replace(/_/g, " ")}
                    </td>
                    <td style={{ padding: "12px 16px", color: "var(--text-muted)" }}>
                      {s.kind === "request" ? "Request" : "Scan job"}
                    </td>
                    <td style={{ padding: "12px 16px" }}>
                      <span className="chip" style={{ textTransform: "capitalize",
                        color: STATUS_VAR[s.status] ?? "var(--text-muted)",
                        background: `color-mix(in srgb, ${STATUS_VAR[s.status] ?? "var(--text-muted)"} 12%, transparent)`,
                        border: `0.5px solid color-mix(in srgb, ${STATUS_VAR[s.status] ?? "var(--text-muted)"} 30%, transparent)` }}>
                        {s.status}
                      </span>
                    </td>
                    <td style={{ padding: "12px 16px", color: "var(--text-muted)" }}>
                      {s.at ? new Date(s.at).toLocaleString() : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </PortalShell>
  );
}
