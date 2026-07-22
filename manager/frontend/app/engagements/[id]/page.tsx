"use client";

import React, { useState, useRef } from "react";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import { use } from "react";
import Link from "next/link";
import {
  ArrowLeft, RefreshCw, AlertTriangle, Upload, Loader2,
  Network, Shield, Eye, FileText, BarChart2, Users, Pencil, X, Check,
} from "lucide-react";
import { PageShell } from "../../../components/PageShell";
import { fetchJson, isUnauthorized, getStoredToken } from "../../../lib/fetcher";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";
import { useToast } from "../../../hooks/useToast";

type TabKey = "overview" | "findings" | "assets" | "attack-paths" | "detection" | "reports";

interface Engagement {
  id: string; name: string; client: string; status: string;
  startDate: string; endDate: string; scopeCidrs: string[];
  excludedCidrs: string[]; assessor: string; assetCount: number;
  findingCount: number;
  findingsBySeverity: { CRITICAL: number; HIGH: number; MEDIUM: number; LOW: number };
  progress: number; description?: string; tags: string[];
}

function sevColor(s: string) {
  if (s === "CRITICAL") return "#FF1744";
  if (s === "HIGH")     return "#FF6D00";
  if (s === "MEDIUM")   return "#FFD600";
  return "#00E676";
}

function statusColor(s: string) {
  if (s === "ACTIVE")    return "#00E676";
  if (s === "PLANNING")  return "#FFD600";
  if (s === "COMPLETED") return "#00D4FF";
  if (s === "PAUSED")    return "#FF6D00";
  return "#64748B";
}

/* ─── Skeleton ─── */
function CardSkeleton() {
  return (
    <div style={{ background: "var(--adv-panel)", border: "1px solid var(--adv-border)", borderRadius: 6, padding: 16 }}>
      <div className="shimmer" style={{ width: 80, height: 10, borderRadius: 3, marginBottom: 10 }} />
      <div className="shimmer" style={{ width: 120, height: 28, borderRadius: 3 }} />
    </div>
  );
}

/* ─── Overview tab ─── */
function OverviewTab({ eng, activity }: { eng: Engagement; activity: { id: string; timestamp: string; actor: string; action: string; detail: string }[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {/* Metric cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
        {[
          { label: "FINDINGS", value: eng.findingCount,  color: eng.findingCount > 0 ? "#FF1744" : "var(--adv-accent)" },
          { label: "ASSETS",   value: eng.assetCount,    color: "var(--adv-accent)" },
          { label: "PROGRESS", value: `${eng.progress}%`,color: eng.progress === 100 ? "#00E676" : "var(--adv-accent)" },
          { label: "DAYS LEFT",value: Math.max(0, Math.ceil((new Date(eng.endDate).getTime() - Date.now()) / 86400000)), color: "#FFD600" },
        ].map((m) => (
          <div key={m.label} style={{ background: "var(--adv-panel)", border: "1px solid var(--adv-border)", borderRadius: 6, padding: "14px 16px" }}>
            <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "var(--adv-text-muted)", marginBottom: 6 }}>{m.label}</div>
            <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 26, fontWeight: 700, color: m.color }}>{m.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        {/* Engagement info */}
        <div style={{ background: "var(--adv-bg)", border: "1px solid var(--adv-border)", borderRadius: 6, overflow: "hidden" }}>
          <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--adv-border)", fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "var(--adv-text)" }}>
            ENGAGEMENT DETAILS
          </div>
          <div style={{ padding: 14 }}>
            {[
              { label: "Client",    value: eng.client },
              { label: "Assessor",  value: eng.assessor },
              { label: "Status",    value: eng.status },
              { label: "Start",     value: eng.startDate },
              { label: "End",       value: eng.endDate },
              { label: "Scope",     value: eng.scopeCidrs.join(", ") || "—" },
              { label: "Excluded",  value: eng.excludedCidrs.join(", ") || "—" },
              { label: "Tags",      value: eng.tags?.length ? eng.tags.join(", ") : "—" },
              { label: "Description", value: eng.description || "—" },
            ].map((r) => (
              <div key={r.label} style={{ display: "flex", padding: "6px 0", borderBottom: "1px solid var(--adv-border)" }}>
                <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "var(--adv-text-muted)", width: 80, flexShrink: 0 }}>{r.label}</span>
                <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, color: "var(--adv-text)" }}>{r.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Activity feed */}
        <div style={{ background: "var(--adv-bg)", border: "1px solid var(--adv-border)", borderRadius: 6, overflow: "hidden" }}>
          <div style={{ padding: "10px 14px", borderBottom: "1px solid var(--adv-border)", fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "var(--adv-text)" }}>
            ACTIVITY FEED
          </div>
          <div style={{ overflowY: "auto", maxHeight: 280 }}>
            {activity.length === 0 ? (
              <div style={{ padding: "40px 0", textAlign: "center", fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: "var(--adv-text-muted)" }}>No activity yet</div>
            ) : activity.map((a) => (
              <div key={a.id} style={{ padding: "10px 14px", borderBottom: "1px solid var(--adv-border)", display: "flex", gap: 10 }}>
                <div style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--adv-accent)", marginTop: 5, flexShrink: 0 }} />
                <div>
                  <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "var(--adv-accent)", marginBottom: 2 }}>{a.action}</div>
                  <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "var(--adv-text)" }}>{a.detail}</div>
                  <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "var(--adv-text-muted)", marginTop: 2 }}>
                    {a.actor} · {new Date(a.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Findings severity breakdown */}
      <div style={{ background: "var(--adv-bg)", border: "1px solid var(--adv-border)", borderRadius: 6, padding: "14px 16px" }}>
        <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, color: "var(--adv-text)", marginBottom: 12 }}>FINDINGS BY SEVERITY</div>
        <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
          {(["CRITICAL","HIGH","MEDIUM","LOW"] as const).map((s) => (
            <div key={s} style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ width: 10, height: 10, borderRadius: 2, background: sevColor(s) }} />
              <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 20, fontWeight: 700, color: sevColor(s) }}>{eng.findingsBySeverity[s]}</span>
              <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 9, color: "var(--adv-text-muted)" }}>{s}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ─── Placeholder tab ─── */
function LinkedTab({ label, href, icon: Icon }: { label: string; href: string; icon: React.ComponentType<{ size: number; color: string }> }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "80px 0", gap: 14 }}>
      <Icon size={40} color="var(--adv-border)" />
      <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: "var(--adv-text-muted)" }}>{label.toUpperCase()}</div>
      <Link href={href}
        style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "var(--adv-accent)", textDecoration: "none", border: "1px solid rgba(37,99,235,0.3)", borderRadius: 4, padding: "6px 16px" }}>
        OPEN {label.toUpperCase()} →
      </Link>
    </div>
  );
}

/* ─── Attack Surface (real data: probe-discovered hosts + services) ─── */
interface AssetRow {
  id: string; ip_address: string | null; hostname: string | null; os: string | null;
  asset_type: string; criticality: string;
  services: { port: number; protocol: string; service: string | null; product: string | null; version: string | null }[];
}

function AssetsTab({ engagementId }: { engagementId: string }) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["assets", engagementId],
    queryFn: () => fetchJson<AssetRow[]>(`/api/engagements/${engagementId}/assets`),
    refetchInterval: 20_000,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const assets = data ?? [];
  const mono = "'JetBrains Mono', monospace";
  return (
    <DataState
      loading={isLoading}
      error={error}
      isEmpty={assets.length === 0}
      onRetry={() => refetch()}
      skeleton={<SkeletonRows rows={4} height={64} />}
      empty={
        <EmptyState
          icon={Shield}
          title="No hosts discovered yet"
          hint="Run a host/service discovery scan on this operation — discovered hosts and their open services appear here."
        />
      }
    >
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <div style={{ fontFamily: mono, fontSize: 10, color: "var(--adv-text-muted)", marginBottom: 2 }}>
          {assets.length} host{assets.length === 1 ? "" : "s"} · {assets.reduce((n, a) => n + a.services.length, 0)} services
        </div>
        {assets.map((a) => (
          <div key={a.id} style={{ background: "var(--adv-panel)", border: "1px solid var(--adv-border)", borderRadius: 8, padding: "12px 14px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: a.services.length ? 8 : 0 }}>
              <Network size={14} color="var(--adv-accent)" />
              <span style={{ fontFamily: mono, fontSize: 13, fontWeight: 600, color: "var(--adv-text)" }}>{a.ip_address}</span>
              {a.hostname && <span style={{ fontFamily: mono, fontSize: 11, color: "var(--adv-text-muted)" }}>{a.hostname}</span>}
              {a.os && <span style={{ fontFamily: mono, fontSize: 10, color: "var(--adv-text-muted)", marginLeft: "auto" }}>{a.os}</span>}
              <span style={{ fontFamily: mono, fontSize: 10, color: "var(--adv-text-muted)", marginLeft: a.os ? 8 : "auto" }}>{a.services.length} svc</span>
            </div>
            {a.services.length > 0 && (
              <div style={{ display: "grid", gap: 3 }}>
                {a.services.map((s, i) => (
                  <div key={i} style={{ display: "flex", gap: 12, fontFamily: mono, fontSize: 11 }}>
                    <span style={{ color: "var(--adv-accent)", minWidth: 72 }}>{s.port}/{s.protocol}</span>
                    <span style={{ color: "var(--adv-text)", minWidth: 90 }}>{s.service || "—"}</span>
                    <span style={{ color: "var(--adv-text-muted)" }}>{[s.product, s.version].filter(Boolean).join(" ")}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </DataState>
  );
}

/* ─── Import scan file (probe .json bundle / .jsonl) → detection + graph ─── */
function ImportScanButton({ engagementId }: { engagementId: string }) {
  const fileRef = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const toast = useToast();
  const qc = useQueryClient();

  async function onPick(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    e.target.value = ""; // allow re-selecting the same file later
    if (!file) return;
    setBusy(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      // Multipart upload — can't use fetchJson (it forces application/json and
      // would break the boundary), so attach the Bearer token by hand. Without it
      // the withBackend route 401s and the import silently fails.
      const token = getStoredToken();
      const res = await fetch(`/api/engagements/${engagementId}/import-facts`, {
        method: "POST",
        body: fd,
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.error || data?.detail || `Import failed (${res.status}).`);
      toast.success(
        `Imported ${data.fact_count} facts`,
        `${data.assets_promoted ?? 0} assets · detection running — findings & graph update shortly.`,
      );
      // Detection runs in the background; refresh the views that reflect it.
      qc.invalidateQueries({ queryKey: ["assets", engagementId] });
      qc.invalidateQueries({ queryKey: ["engagement", engagementId] });
    } catch (err) {
      toast.error("Import failed", err instanceof Error ? err.message : "Unknown error");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <input
        ref={fileRef}
        type="file"
        accept=".json,.jsonl,application/json"
        onChange={onPick}
        style={{ display: "none" }}
      />
      <button
        className="btn-secondary"
        disabled={busy}
        onClick={() => fileRef.current?.click()}
        title="Import a probe scan file (.json bundle or .jsonl) → detection + attack graph"
      >
        {busy ? <Loader2 size={13} className="animate-spin" /> : <Upload size={13} />}
        {busy ? "Importing…" : "Import scan"}
      </button>
    </>
  );
}

/* ─── Edit Engagement modal — makes every field editable (PATCH via BFF) ─── */
const EDIT_STATUSES = ["PLANNING", "ACTIVE", "PAUSED", "COMPLETED"] as const;

function EditEngagementModal({ eng, id, onClose }: { eng: Engagement; id: string; onClose: () => void }) {
  const qc = useQueryClient();
  const toast = useToast();
  const dash = (v?: string) => (!v || v === "—" ? "" : v);
  const [f, setF] = useState({
    name: eng.name ?? "",
    client: dash(eng.client),
    assessor: dash(eng.assessor),
    description: eng.description ?? "",
    status: eng.status ?? "PLANNING",
    startDate: (eng.startDate ?? "").slice(0, 10),
    endDate: (eng.endDate ?? "").slice(0, 10),
    scopeCidrs: (eng.scopeCidrs ?? []).join(", "),
    excludedCidrs: (eng.excludedCidrs ?? []).join(", "),
    tags: (eng.tags ?? []).join(", "),
  });
  const patch = (p: Partial<typeof f>) => setF((o) => ({ ...o, ...p }));

  const save = useMutation({
    // fetchJson injects the Authorization header (raw fetch would 401 at the BFF).
    mutationFn: () => fetchJson(`/api/engagements/${id}`, {
      method: "PUT",
      body: JSON.stringify(f),
    }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["engagement", id] });
      qc.invalidateQueries({ queryKey: ["engagements"] });
      toast.success("Saved", "Engagement updated.");
      onClose();
    },
    onError: (e) => toast.error("Update failed", e instanceof Error ? e.message : "Could not save."),
  });

  const mono = "'JetBrains Mono', monospace";
  const input: React.CSSProperties = {
    width: "100%", boxSizing: "border-box", background: "var(--adv-bg)",
    border: "1px solid var(--adv-border)", borderRadius: 5, padding: "8px 10px",
    color: "var(--adv-text)", fontFamily: mono, fontSize: 12, outline: "none",
  };
  const label: React.CSSProperties = { fontFamily: mono, fontSize: 9, color: "var(--adv-text-muted)", marginBottom: 5, display: "block" };
  const canSave = f.name.trim().length > 0 && f.scopeCidrs.split(/[\n,]/).some((s) => s.trim());

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", zIndex: 100, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div className="animate-scale-in" style={{ background: "var(--adv-panel)", border: "1px solid var(--adv-border)", borderRadius: 10, width: 540, maxHeight: "90vh", overflow: "hidden", display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "16px 20px", borderBottom: "1px solid var(--adv-border)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <span style={{ fontFamily: mono, fontSize: 13, color: "var(--adv-text)", letterSpacing: 1 }}>EDIT ENGAGEMENT</span>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--adv-text-muted)" }}><X size={16} /></button>
        </div>

        <div style={{ padding: "18px 22px", overflowY: "auto", display: "flex", flexDirection: "column", gap: 12 }}>
          <div><label style={label}>ENGAGEMENT NAME *</label>
            <input value={f.name} onChange={(e) => patch({ name: e.target.value })} style={input} /></div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div><label style={label}>CLIENT</label><input value={f.client} onChange={(e) => patch({ client: e.target.value })} style={input} /></div>
            <div><label style={label}>ASSESSOR</label><input value={f.assessor} onChange={(e) => patch({ assessor: e.target.value })} style={input} /></div>
          </div>
          <div><label style={label}>DESCRIPTION</label>
            <textarea value={f.description} onChange={(e) => patch({ description: e.target.value })} rows={2} style={{ ...input, resize: "vertical", lineHeight: 1.5 }} /></div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
            <div><label style={label}>STATUS</label>
              <select value={f.status} onChange={(e) => patch({ status: e.target.value })} style={{ ...input, cursor: "pointer" }}>
                {EDIT_STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
              </select></div>
            <div><label style={label}>START</label><input type="date" value={f.startDate} onChange={(e) => patch({ startDate: e.target.value })} style={input} /></div>
            <div><label style={label}>END</label><input type="date" value={f.endDate} onChange={(e) => patch({ endDate: e.target.value })} style={input} /></div>
          </div>
          <div><label style={label}>SCOPE CIDRs * (comma-separated)</label>
            <textarea value={f.scopeCidrs} onChange={(e) => patch({ scopeCidrs: e.target.value })} rows={2} style={{ ...input, resize: "vertical", lineHeight: 1.5 }} /></div>
          <div><label style={label}>EXCLUDED IPs / CIDRs</label>
            <textarea value={f.excludedCidrs} onChange={(e) => patch({ excludedCidrs: e.target.value })} rows={2} style={{ ...input, resize: "vertical", lineHeight: 1.5 }} /></div>
          <div><label style={label}>TAGS (comma-separated)</label>
            <input value={f.tags} onChange={(e) => patch({ tags: e.target.value })} placeholder="external, web, pci" style={input} /></div>
        </div>

        <div style={{ padding: "14px 20px", borderTop: "1px solid var(--adv-border)", display: "flex", justifyContent: "flex-end", gap: 8 }}>
          <button onClick={onClose} style={{ fontFamily: mono, fontSize: 10, color: "var(--adv-text-muted)", background: "none", border: "1px solid var(--adv-border)", borderRadius: 4, padding: "6px 16px", cursor: "pointer" }}>CANCEL</button>
          <button onClick={() => save.mutate()} disabled={!canSave || save.isPending}
            style={{ display: "flex", alignItems: "center", gap: 6, fontFamily: mono, fontSize: 10, color: canSave ? "#00E676" : "#64748B", background: canSave ? "rgba(0,230,118,0.08)" : "transparent", border: `1px solid ${canSave ? "rgba(0,230,118,0.3)" : "var(--adv-border)"}`, borderRadius: 4, padding: "6px 20px", cursor: canSave ? "pointer" : "not-allowed" }}>
            {save.isPending ? <RefreshCw size={11} style={{ animation: "spin 1s linear infinite" }} /> : <Check size={11} />} SAVE CHANGES
          </button>
        </div>
      </div>
    </div>
  );
}

/* ─── Main Page ─── */
export default function EngagementDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [activeTab, setActiveTab] = useState<TabKey>("overview");
  const [showEdit, setShowEdit] = useState(false);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["engagement", id],
    // fetchJson injects the Bearer token; a raw fetch 401s against the
    // withBackend route and the detail page renders empty.
    queryFn: () => fetchJson<any>(`/api/engagements/${id}`),
  });

  const eng: Engagement | null = data?.engagement ?? null;
  const activity = data?.activity ?? [];

  const tabs: { key: TabKey; label: string; icon: React.ComponentType<{ size: number; color: string }> }[] = [
    { key: "overview",      label: "Overview",      icon: BarChart2 },
    { key: "findings",      label: "Findings",      icon: AlertTriangle },
    { key: "assets",        label: "Assets",        icon: Users },
    { key: "attack-paths",  label: "Attack Paths",  icon: Network },
    { key: "detection",     label: "Detection",     icon: Eye },
    { key: "reports",       label: "Reports",       icon: FileText },
  ];

  return (
    <PageShell
      title={isLoading ? "LOADING…" : eng?.name ?? "ENGAGEMENT"}
      subtitle={eng ? `${eng.client} · ${eng.assessor}` : ""}
      headerActions={
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {eng && (
            <button className="btn-secondary" onClick={() => setShowEdit(true)} title="Edit engagement fields">
              <Pencil size={13} /> Edit
            </button>
          )}
          <ImportScanButton engagementId={id} />
        </div>
      }
      statusItems={eng ? [
        { label: "STATUS",   value: eng.status,           color: statusColor(eng.status) },
        { label: "FINDINGS", value: String(eng.findingCount), color: eng.findingCount > 0 ? "#FF1744" : "var(--adv-text-muted)" },
        { label: "ASSETS",   value: String(eng.assetCount),  color: "var(--adv-accent)" },
      ] : []}
    >
      {/* Back + tabs */}
      <div style={{ display: "flex", alignItems: "center", gap: 0, borderBottom: "1px solid var(--adv-border)", marginBottom: 0, flexShrink: 0 }}>
        <Link href="/engagements" style={{ display: "flex", alignItems: "center", gap: 5, padding: "8px 14px", fontFamily: "'JetBrains Mono', monospace", fontSize: 10, color: "var(--adv-text-muted)", textDecoration: "none", borderRight: "1px solid var(--adv-border)" }}>
          <ArrowLeft size={11} /> BACK
        </Link>
        {tabs.map(({ key, label, icon: Icon }) => (
          <button key={key} onClick={() => setActiveTab(key)}
            style={{
              padding: "8px 14px", border: "none", background: "none", cursor: "pointer",
              borderBottom: `2px solid ${activeTab === key ? "var(--adv-accent)" : "transparent"}`,
              display: "flex", alignItems: "center", gap: 5, marginBottom: -1,
              fontFamily: "'JetBrains Mono', monospace", fontSize: 10,
              color: activeTab === key ? "var(--adv-accent)" : "var(--adv-text-muted)",
              whiteSpace: "nowrap",
            }}>
            <Icon size={11} color={activeTab === key ? "var(--adv-accent)" : "var(--adv-text-muted)"} />
            {label.toUpperCase()}
          </button>
        ))}
      </div>

      <div style={{ flex: 1, overflowY: "auto", paddingTop: 14 }}>
        {isLoading && (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
            {[1,2,3,4].map((i) => <CardSkeleton key={i} />)}
          </div>
        )}

        {isError && (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "80px 0", gap: 10 }}>
            <AlertTriangle size={36} color="#FF1744" />
            <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: "#FF1744" }}>Failed to load engagement</span>
            <Link href="/engagements" style={{ color: "var(--adv-accent)", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>← Back to list</Link>
          </div>
        )}

        {!isLoading && !isError && eng && (
          <>
            {activeTab === "overview"     && <OverviewTab eng={eng} activity={activity} />}
            {activeTab === "findings"     && <LinkedTab label="Findings"     href="/findings"      icon={AlertTriangle} />}
            {activeTab === "assets"       && <AssetsTab engagementId={id} />}
            {activeTab === "attack-paths" && <LinkedTab label="Attack Paths" href="/attack-graph"  icon={Network} />}
            {activeTab === "detection"    && <LinkedTab label="Detection"    href="/detection"     icon={Eye} />}
            {activeTab === "reports"      && <LinkedTab label="Reports"      href="/reports"       icon={FileText} />}
          </>
        )}
      </div>

      {showEdit && eng && (
        <EditEngagementModal eng={eng} id={id} onClose={() => setShowEdit(false)} />
      )}
    </PageShell>
  );
}
