"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import {
  Plus, Briefcase, ChevronRight, X, Check,
  RefreshCw, AlertTriangle,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useToast } from "../../hooks/useToast";
import { fetchJson, errorMessage } from "../../lib/fetcher";

/* ─── Types ─── */
type EngagementStatus = "PLANNING" | "ACTIVE" | "PAUSED" | "COMPLETED" | "ARCHIVED";

interface Engagement {
  id: string; name: string; client: string; status: EngagementStatus;
  startDate: string; endDate: string; scopeCidrs: string[];
  assessor: string; assetCount: number; findingCount: number;
  findingsBySeverity: { CRITICAL: number; HIGH: number; MEDIUM: number; LOW: number };
  progress: number; tags: string[];
}

interface EngagementsResponse {
  engagements: Engagement[];
  stats?: { totalFindings: number; activeEngagements: number; totalAssets: number };
  activity?: unknown[];
  timeline?: unknown[];
}

/* ─── Multi-step form state ─── */
interface FormState {
  name: string; client: string; description: string;
  startDate: string; endDate: string; assessor: string; tags: string;
  scopeCidrs: string; excludedCidrs: string;
  credType: "ssh" | "winrm" | "domain" | "api"; credLabel: string; credUser: string;
  credVaultRef: string;
}

const EMPTY_FORM: FormState = {
  name: "", client: "", description: "",
  startDate: "", endDate: "", assessor: "analyst@vedha.io", tags: "",
  scopeCidrs: "", excludedCidrs: "",
  credType: "domain", credLabel: "", credUser: "", credVaultRef: "",
};

const splitEntries = (value: string) =>
  value.split(/[\s,]+/).map((entry) => entry.trim()).filter(Boolean);

const hasValidDateRange = (startDate: string, endDate: string) =>
  Boolean(startDate && endDate && endDate >= startDate);

/* ─── Helpers ─── */
function statusColor(s: EngagementStatus) {
  if (s === "ACTIVE")    return "var(--accent)";
  if (s === "PLANNING")  return "var(--sev-low-color)";
  if (s === "PAUSED")    return "var(--sev-medium-color)";
  if (s === "COMPLETED") return "var(--nominal-color)";
  return "var(--text-muted)";
}

function sevColor(s: string) {
  if (s === "CRITICAL") return "var(--sev-critical-color)";
  if (s === "HIGH")     return "var(--sev-high-color)";
  if (s === "MEDIUM")   return "var(--sev-medium-color)";
  return "var(--sev-low-color)";
}

/* ─── Skeleton ─── */
function RowSkeleton() {
  return (
    <tr>
      {[200, 100, 80, 80, 120, 80].map((w, i) => (
        <td key={i} style={{ padding: "12px 14px" }}>
          <div className="shimmer" style={{ width: w, height: 14, borderRadius: 4 }} />
        </td>
      ))}
    </tr>
  );
}

/* ─── Step labels ─── */
const STEPS = ["Name & Dates", "Scope CIDRs", "Credentials", "Review"];

/* ─── Main Page ─── */
export default function EngagementsPage() {
  const { success, error: toastError } = useToast();
  const qc = useQueryClient();

  // fetchJson injects the stored Bearer token and THROWS on non-2xx. The BFF
  // (withBackend) authenticates via the Authorization header, not the cookie —
  // a raw fetch() sends only the cookie, so every call 401'd silently: the list
  // came back empty and creates looked successful ("Created" toast) while
  // nothing persisted. Throwing on error also makes isError / onError real.
  const { data, isLoading, isError, refetch, isFetching } = useQuery<EngagementsResponse>({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<EngagementsResponse>("/api/engagements"),
  });

  const createMutation = useMutation({
    mutationFn: (body: Record<string, unknown>) =>
      fetchJson<{ engagement: Engagement }>("/api/engagements", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["engagements"] });
      success("Created", "Engagement created successfully.");
      setShowModal(false);
      setStep(0);
      setForm(EMPTY_FORM);
    },
    onError: (err) => toastError("Error", errorMessage(err)),
  });

  const [showModal, setShowModal] = useState(false);
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<FormState>(EMPTY_FORM);

  const engagements: Engagement[] = data?.engagements ?? [];

  function patchForm(patch: Partial<FormState>) {
    setForm((p) => ({ ...p, ...patch }));
  }

  function canProceed() {
    if (step === 0) {
      return Boolean(form.name.trim() && form.client.trim() && hasValidDateRange(form.startDate, form.endDate));
    }
    if (step === 1) return splitEntries(form.scopeCidrs).length > 0;
    if (step === 2) {
      const credentialStarted = Boolean(form.credLabel.trim() || form.credUser.trim() || form.credVaultRef.trim());
      return !credentialStarted || Boolean(form.credLabel.trim() && form.credVaultRef.trim());
    }
    return true;
  }

  function submit() {
    createMutation.mutate({
      name: form.name.trim(),
      client: form.client.trim(),
      description: form.description.trim(),
      startDate: form.startDate,
      endDate: form.endDate,
      assessor: form.assessor.trim(),
      tags: form.tags.split(",").map((s) => s.trim()).filter(Boolean),
      scopeCidrs: splitEntries(form.scopeCidrs),
      excludedCidrs: splitEntries(form.excludedCidrs),
      credentials: form.credLabel.trim()
        ? [{
            type: form.credType,
            label: form.credLabel.trim(),
            username: form.credUser.trim() || undefined,
            vaultRef: form.credVaultRef.trim(),
          }]
        : [],
    });
  }

  const inputStyle: React.CSSProperties = {
    width: "100%", boxSizing: "border-box",
    background: "var(--adv-bg)", border: "1px solid var(--adv-border)",
    borderRadius: 5, padding: "8px 10px", color: "var(--adv-text)",
    fontFamily: "var(--font-body)", fontSize: 13, outline: "none",
  };

  const labelStyle: React.CSSProperties = {
    fontFamily: "var(--font-body)", fontSize: 11, fontWeight: 600,
    color: "var(--adv-text-muted)", marginBottom: 6, display: "block",
  };

  return (
    <PageShell
      title="Engagements"
      subtitle="Scope, track, and report on client assessments"
      statusItems={[
        { label: "ACTIVE",    value: String(engagements.filter((e) => e.status === "ACTIVE").length),    color: "var(--accent)" },
        { label: "PLANNING",  value: String(engagements.filter((e) => e.status === "PLANNING").length),  color: "var(--sev-low-color)" },
        { label: "COMPLETED", value: String(engagements.filter((e) => e.status === "COMPLETED").length), color: "var(--nominal-color)" },
      ]}
    >
      {/* Toolbar */}
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 14 }}>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}
          style={{ display: "flex", alignItems: "center", gap: 7 }}>
          <Plus size={14} /> New engagement
        </button>
      </div>

      {/* Table */}
      <div style={{ background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 12, overflowX: "auto", boxShadow: "var(--shadow-sm)" }}>
        <table style={{ width: "100%", minWidth: 980, borderCollapse: "collapse" }}>
          <thead>
            <tr>
              {["Engagement", "Client", "Status", "Scope", "Findings", "Assets", "Progress", "Dates", ""].map((h) => (
                <th key={h} style={{ padding: "11px 14px", textAlign: "left", fontFamily: "var(--font-body)", fontSize: 11, fontWeight: 600, color: "var(--text-muted)", background: "var(--bg-surface)", borderBottom: "1px solid var(--border-subtle)", whiteSpace: "nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {isLoading && [1, 2, 3].map((i) => <RowSkeleton key={i} />)}
            {isError && (
              <tr>
                <td colSpan={9} style={{ padding: "40px 0", textAlign: "center" }}>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
                    <AlertTriangle size={28} color="var(--sev-critical-color)" />
                    <span style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--sev-critical-color)" }}>Failed to load engagements</span>
                    <button onClick={() => refetch()} disabled={isFetching}
                      style={{ display: "flex", alignItems: "center", gap: 6, fontFamily: "var(--font-body)", fontSize: 12, color: "var(--accent)", background: "none", border: "1px solid var(--border-accent)", borderRadius: 6, padding: "6px 14px", cursor: isFetching ? "not-allowed" : "pointer" }}>
                      <RefreshCw size={11} style={isFetching ? { animation: "spin 1s linear infinite" } : undefined} /> Retry
                    </button>
                  </div>
                </td>
              </tr>
            )}
            {!isLoading && !isError && engagements.length === 0 && (
              <tr>
                <td colSpan={9} style={{ padding: "60px 0", textAlign: "center" }}>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
                    <Briefcase size={36} color="var(--adv-border)" />
                    <span style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-muted)" }}>No engagements yet</span>
                    <button onClick={() => setShowModal(true)} style={{ fontFamily: "var(--font-body)", fontSize: 12, color: "var(--accent)", background: "none", border: "1px solid var(--border-accent)", borderRadius: 6, padding: "6px 14px", cursor: "pointer" }}>
                      Create first engagement
                    </button>
                  </div>
                </td>
              </tr>
            )}
            {engagements.map((eng) => (
              <tr key={eng.id} className="card-hover" style={{ borderBottom: "1px solid var(--adv-border)" }}>
                <td style={{ padding: "12px 14px" }}>
                  <div style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-primary)", fontWeight: 600 }}>{eng.name}</div>
                  <div style={{ fontFamily: "var(--font-body)", fontSize: 10, color: "var(--text-muted)", marginTop: 4 }}>
                    {eng.tags.map((t) => (
                      <span key={t} style={{ marginRight: 4, background: "var(--accent-ghost)", borderRadius: 5, padding: "2px 5px", color: "var(--accent)" }}>{t}</span>
                    ))}
                  </div>
                </td>
                <td style={{ padding: "12px 14px", fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-secondary)" }}>{eng.client}</td>
                <td style={{ padding: "12px 14px" }}>
                  <span style={{ fontFamily: "var(--font-body)", fontSize: 10, fontWeight: 650, color: statusColor(eng.status), background: `color-mix(in srgb, ${statusColor(eng.status)} 10%, transparent)`, border: `1px solid color-mix(in srgb, ${statusColor(eng.status)} 28%, transparent)`, borderRadius: 6, padding: "3px 7px" }}>{eng.status}</span>
                </td>
                <td style={{ padding: "12px 14px", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-secondary)" }}>{eng.scopeCidrs.length} CIDR{eng.scopeCidrs.length !== 1 ? "s" : ""}</td>
                <td style={{ padding: "12px 14px" }}>
                  <div style={{ display: "flex", gap: 5 }}>
                    {(["CRITICAL","HIGH","MEDIUM","LOW"] as const).map((s) => (eng.findingsBySeverity?.[s] ?? 0) > 0 ? (
                      <span title={`${s.toLowerCase()} findings`} key={s} style={{ fontFamily: "var(--font-mono)", fontSize: 10, fontWeight: 650, color: sevColor(s), background: `color-mix(in srgb, ${sevColor(s)} 9%, transparent)`, borderRadius: 5, padding: "2px 5px" }}>{s.slice(0, 1)} {eng.findingsBySeverity[s]}</span>
                    ) : null)}
                    {eng.findingCount === 0 && <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-muted)" }}>—</span>}
                  </div>
                </td>
                <td style={{ padding: "12px 14px", fontFamily: "var(--font-mono)", fontSize: 13, fontWeight: 650, color: "var(--text-primary)" }}>{eng.assetCount}</td>
                <td style={{ padding: "12px 14px", minWidth: 100 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                    <div style={{ flex: 1, height: 5, background: "var(--adv-panel)", borderRadius: 3, overflow: "hidden" }}>
                      <div style={{ height: "100%", width: `${eng.progress}%`, background: eng.progress === 100 ? "var(--nominal-color)" : "var(--accent)", borderRadius: 3, transition: "width 0.4s ease" }} />
                    </div>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-muted)", flexShrink: 0 }}>{eng.progress}%</span>
                  </div>
                </td>
                <td style={{ padding: "12px 14px", fontFamily: "var(--font-body)", fontSize: 11, color: "var(--text-muted)", whiteSpace: "nowrap" }}>
                  {eng.startDate} → {eng.endDate}
                </td>
                <td style={{ padding: "12px 14px" }}>
                  <Link href={`/engagements/${eng.id}`}
                    style={{ display: "flex", alignItems: "center", gap: 4, fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 600, color: "var(--accent)", textDecoration: "none" }}>
                    Open <ChevronRight size={12} />
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ── Multi-step Create Modal ── */}
      {showModal && (
        <div role="presentation" style={{ position: "fixed", inset: 0, background: "var(--modal-backdrop)", zIndex: 100, display: "flex", alignItems: "center", justifyContent: "center", padding: 12 }}>
          <div role="dialog" aria-modal="true" aria-labelledby="new-engagement-title" className="animate-scale-in" style={{ background: "var(--adv-panel)", border: "1px solid var(--adv-border)", borderRadius: 10, width: 520, maxWidth: "calc(100vw - 24px)", maxHeight: "90vh", overflow: "hidden", display: "flex", flexDirection: "column" }}>
            {/* Modal header */}
            <div style={{ padding: "16px 20px", borderBottom: "1px solid var(--adv-border)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span id="new-engagement-title" style={{ fontFamily: "var(--font-body)", fontSize: 15, fontWeight: 650, color: "var(--text-primary)" }}>New engagement</span>
              <button aria-label="Close new engagement dialog" onClick={() => { setShowModal(false); setStep(0); setForm(EMPTY_FORM); }}
                style={{ background: "none", border: "none", cursor: "pointer", color: "var(--adv-text-muted)" }}>
                <X size={16} />
              </button>
            </div>

            {/* Step indicators */}
            <div style={{ padding: "12px 20px", borderBottom: "1px solid var(--adv-border)", display: "flex", gap: 0 }}>
              {STEPS.map((s, i) => (
                <div key={s} style={{ display: "flex", alignItems: "center" }}>
                  <div style={{
                    width: 22, height: 22, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center",
                    background: i < step ? "var(--accent)" : i === step ? "var(--accent-ghost)" : "var(--bg-surface)",
                    border: `1.5px solid ${i <= step ? "var(--adv-accent)" : "var(--adv-border)"}`,
                    fontFamily: "var(--font-mono)", fontSize: 9,
                    color: i <= step ? (i < step ? "#fff" : "var(--adv-accent)") : "var(--adv-text-muted)",
                  }}>
                    {i < step ? <Check size={11} /> : i + 1}
                  </div>
                  <span style={{ fontFamily: "var(--font-body)", fontSize: 11, color: i === step ? "var(--text-primary)" : "var(--text-muted)", marginLeft: 6, marginRight: i < STEPS.length - 1 ? 12 : 0 }}>{s}</span>
                  {i < STEPS.length - 1 && <div style={{ width: 24, height: 1, background: "var(--adv-border)", marginRight: 8 }} />}
                </div>
              ))}
            </div>

            {/* Step content */}
            <div style={{ padding: "20px 24px", flex: 1, overflowY: "auto" }}>
              {step === 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                  {[
                    { label: "ENGAGEMENT NAME *", key: "name" as const, placeholder: "ACME Corp — Q2 VAPT" },
                    { label: "CLIENT NAME *",     key: "client" as const, placeholder: "ACME Corporation" },
                    { label: "DESCRIPTION",       key: "description" as const, placeholder: "Scope and objectives…" },
                    { label: "ASSESSOR",          key: "assessor" as const, placeholder: "analyst@vedha.io" },
                    { label: "TAGS (comma-separated)", key: "tags" as const, placeholder: "external, web, pci" },
                  ].map(({ label, key, placeholder }) => (
                    <div key={key}>
                      <label htmlFor={`eng-create-${key}`} style={labelStyle}>{label}</label>
                      <input id={`eng-create-${key}`} value={form[key]} onChange={(e) => patchForm({ [key]: e.target.value })}
                        placeholder={placeholder} style={inputStyle} />
                    </div>
                  ))}
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                    <div>
                      <label htmlFor="eng-create-start" style={labelStyle}>START DATE *</label>
                      <input id="eng-create-start" type="date" value={form.startDate} onChange={(e) => patchForm({ startDate: e.target.value })} style={inputStyle} />
                    </div>
                    <div>
                      <label htmlFor="eng-create-end" style={labelStyle}>END DATE *</label>
                      <input id="eng-create-end" type="date" min={form.startDate || undefined} value={form.endDate} onChange={(e) => patchForm({ endDate: e.target.value })} style={inputStyle} />
                    </div>
                  </div>
                  {form.startDate && form.endDate && !hasValidDateRange(form.startDate, form.endDate) && (
                    <div role="alert" style={{ fontSize: 11, color: "var(--sev-high-color)" }}>
                      End date must be on or after the start date.
                    </div>
                  )}
                </div>
              )}

              {step === 1 && (
                <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                  <div>
                    <label htmlFor="eng-create-scope" style={labelStyle}>SCOPE IPs / CIDRs * (comma or one per line)</label>
                    <textarea id="eng-create-scope" value={form.scopeCidrs} onChange={(e) => patchForm({ scopeCidrs: e.target.value })}
                      placeholder={"10.0.0.0/8\n192.168.1.0/24"} rows={3}
                      style={{ ...inputStyle, resize: "vertical", lineHeight: 1.5 }} />
                    <div style={{ fontFamily: "var(--font-body)", fontSize: 11, color: "var(--text-muted)", marginTop: 4 }}>
                      {splitEntries(form.scopeCidrs).length} entr{splitEntries(form.scopeCidrs).length === 1 ? "y" : "ies"}
                    </div>
                  </div>
                  <div>
                    <label htmlFor="eng-create-excluded" style={labelStyle}>EXCLUDED IPs / CIDRs (comma or one per line)</label>
                    <textarea id="eng-create-excluded" value={form.excludedCidrs} onChange={(e) => patchForm({ excludedCidrs: e.target.value })}
                      placeholder="10.0.0.1, 192.168.1.1" rows={2}
                      style={{ ...inputStyle, resize: "vertical", lineHeight: 1.5 }} />
                  </div>
                  <div style={{ background: "var(--sev-medium-bg)", border: "1px solid color-mix(in srgb, var(--sev-medium-color) 24%, transparent)", borderRadius: 7, padding: "10px 12px", fontFamily: "var(--font-body)", fontSize: 12, color: "var(--text-secondary)" }}>
                    Scope is enforced server-side by the exploit engine. Out-of-scope targets are blocked automatically.
                  </div>
                </div>
              )}

              {step === 2 && (
                <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                  <div style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-secondary)" }}>
                    Optional: attach an existing secret from your approved vault. Vedha stores only the reference, never the secret value.
                  </div>
                  <div>
                    <div style={labelStyle}>CREDENTIAL TYPE</div>
                    <div role="group" aria-label="Credential type" style={{ display: "flex", gap: 6 }}>
                      {(["domain", "ssh", "winrm", "api"] as const).map((t) => (
                        <button key={t} aria-pressed={form.credType === t} onClick={() => patchForm({ credType: t })}
                          style={{ fontFamily: "var(--font-body)", fontSize: 11, padding: "6px 12px", borderRadius: 6, cursor: "pointer",
                            border: `1px solid ${form.credType === t ? "var(--adv-accent)" : "var(--adv-border)"}`,
                            background: form.credType === t ? "var(--accent-ghost)" : "transparent",
                            color: form.credType === t ? "var(--adv-accent)" : "var(--adv-text-muted)" }}>
                          {t.toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label htmlFor="eng-create-cred-label" style={labelStyle}>LABEL</label>
                    <input id="eng-create-cred-label" value={form.credLabel} onChange={(e) => patchForm({ credLabel: e.target.value })}
                      placeholder="e.g. corp.local standard user" style={inputStyle} />
                  </div>
                  <div>
                    <label htmlFor="eng-create-cred-user" style={labelStyle}>USERNAME</label>
                    <input id="eng-create-cred-user" value={form.credUser} onChange={(e) => patchForm({ credUser: e.target.value })}
                      placeholder="e.g. pentest@corp.local" style={inputStyle} />
                  </div>
                  <div>
                    <label htmlFor="eng-create-vault-ref" style={labelStyle}>VAULT REFERENCE *</label>
                    <input id="eng-create-vault-ref" value={form.credVaultRef} onChange={(e) => patchForm({ credVaultRef: e.target.value })}
                      placeholder="e.g. vedha/engagements/acme-q2/domain-user" style={inputStyle} />
                  </div>
                  <div style={{ background: "var(--accent-ghost)", border: "1px solid var(--border-accent)", borderRadius: 7, padding: "9px 12px", fontFamily: "var(--font-body)", fontSize: 11, color: "var(--text-muted)" }}>
                    Create the secret in Vault first. This form does not create, verify, or copy secret material.
                  </div>
                  {!canProceed() && (
                    <div role="alert" style={{ fontSize: 11, color: "var(--sev-high-color)" }}>
                      A credential label and vault reference are both required when attaching credentials.
                    </div>
                  )}
                </div>
              )}

              {step === 3 && (
                <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                  <div style={{ fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 650, color: "var(--text-secondary)", marginBottom: 6 }}>Review before creating</div>
                  {[
                    { label: "NAME",       value: form.name },
                    { label: "CLIENT",     value: form.client },
                    { label: "DATES",      value: `${form.startDate} → ${form.endDate}` },
                    { label: "ASSESSOR",   value: form.assessor },
                    { label: "TAGS",       value: form.tags || "—" },
                    { label: "SCOPE",      value: `${splitEntries(form.scopeCidrs).length} target(s): ${splitEntries(form.scopeCidrs).join(", ")}` },
                    { label: "EXCLUDED",   value: form.excludedCidrs || "—" },
                    { label: "CREDENTIAL", value: form.credLabel ? `${form.credLabel} → ${form.credVaultRef}` : "None added" },
                  ].map(({ label, value }) => (
                    <div key={label} style={{ display: "flex", padding: "6px 0", borderBottom: "1px solid var(--adv-border)" }}>
                      <span style={{ fontFamily: "var(--font-body)", fontSize: 11, color: "var(--text-muted)", width: 110, flexShrink: 0 }}>{label}</span>
                      <span style={{ fontFamily: "var(--font-body)", fontSize: 13, color: "var(--text-primary)" }}>{value}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            <div style={{ padding: "14px 20px", borderTop: "1px solid var(--adv-border)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <button disabled={step === 0} onClick={() => setStep((p) => p - 1)}
                style={{ fontFamily: "var(--font-body)", fontSize: 12, color: "var(--text-muted)", background: "none", border: "1px solid var(--border-default)", borderRadius: 7, padding: "7px 16px", cursor: step === 0 ? "not-allowed" : "pointer" }}>
                BACK
              </button>
              {step < STEPS.length - 1 ? (
                <button onClick={() => setStep((p) => p + 1)} disabled={!canProceed()}
                  style={{ fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 600, color: canProceed() ? "var(--accent)" : "var(--text-muted)", background: canProceed() ? "var(--accent-ghost)" : "transparent", border: `1px solid ${canProceed() ? "var(--border-accent)" : "var(--border-default)"}`, borderRadius: 7, padding: "7px 20px", cursor: canProceed() ? "pointer" : "not-allowed" }}>
                  NEXT
                </button>
              ) : (
                <button onClick={submit} disabled={createMutation.isPending}
                  style={{ display: "flex", alignItems: "center", gap: 6, fontFamily: "var(--font-body)", fontSize: 12, fontWeight: 600, color: "var(--nominal-color)", background: "var(--nominal-bg)", border: "1px solid color-mix(in srgb, var(--nominal-color) 28%, transparent)", borderRadius: 7, padding: "7px 20px", cursor: "pointer" }}>
                  {createMutation.isPending ? <RefreshCw size={11} style={{ animation: "spin 1s linear infinite" }} /> : <Check size={11} />}
                  CREATE ENGAGEMENT
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </PageShell>
  );
}
