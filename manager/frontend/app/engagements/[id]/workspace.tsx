"use client";

import React, { use, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Activity, AlertTriangle, ArrowLeft, CalendarDays, Check, ChevronLeft, ChevronRight,
  CircleDot, Clock3, FileText, Loader2, Network, Pencil, Play, RefreshCw, Target,
  Route, Shield, Tags, Upload, UserRound, Users, X,
} from "lucide-react";
import { PageShell } from "../../../components/PageShell";
import { PortalShell } from "../../../components/portal/PortalShell";
import { DataState, EmptyState, SkeletonRows } from "../../../components/states/DataState";
import { AttackAssessmentsPanel } from "../../../components/attack-paths/AttackAssessmentsPanel";
import { isUnauthorized } from "../../../lib/fetcher";
import { useToast } from "../../../hooks/useToast";
import { EngagementStatusControl, STATUS_COLOR } from "../../../components/EngagementStatusControl";
import {
  createEngagementWorkspaceApi,
  type EngagementWorkspaceSurface,
} from "../../../lib/engagement-workspace-api";
import { AssetTagList, ManualTagEditor, TagFilterBar } from "../../../components/intel/AssetTags";
import { RegulatoryProfilePanel } from "../../../components/intel/RegulatoryProfilePanel";
import { filterAssetsByTags, fragileReasons, tagCounts, type TagsDoc } from "../../../lib/intel";

type TabKey = "overview" | "findings" | "assets" | "activity" | "attack-assessments";
type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

interface Engagement {
  id: string;
  name: string;
  client: string;
  status: string;
  startDate: string;
  endDate: string;
  scopeCidrs: string[];
  excludedCidrs: string[];
  assessor: string;
  assetCount: number;
  findingCount: number;
  findingsBySeverity: Record<Severity, number>;
  progress: number;
  description?: string;
  tags: string[];
}

interface ActivityItem {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  detail: string;
}

interface AssetRow {
  id: string;
  ip_address: string | null;
  hostname: string | null;
  os: string | null;
  asset_type: string;
  criticality: string;
  tags?: TagsDoc | null;
  services: Array<{
    port: number;
    protocol: string;
    service: string | null;
    product: string | null;
    version: string | null;
  }>;
}

interface FindingRow {
  id: string;
  title: string;
  severity: Severity | "INFO";
  affectedHost: string;
  status: string;
  riskScore: number;
}
interface FindingPage {
  items: FindingRow[];
  total: number;
  page: number;
  pageSize: number;
  pages: number;
}

const SEVERITY_COLOR: Record<Severity, string> = {
  CRITICAL: "var(--sev-critical-color)",
  HIGH: "var(--sev-high-color)",
  MEDIUM: "var(--sev-medium-color)",
  LOW: "var(--sev-low-color)",
};

function displayDate(value: string) {
  if (!value) return "Not set";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString(undefined, {
    day: "2-digit", month: "short", year: "numeric",
  });
}

function OverviewTab({ engagement, surface }: { engagement: Engagement; surface: EngagementWorkspaceSurface }) {
  const [renderedAt] = useState(() => Date.now());
  // No (or an unparseable) end date is "—", not NaN.
  const endMs = engagement.endDate ? new Date(engagement.endDate).getTime() : Number.NaN;
  const daysLeft = Number.isNaN(endMs) ? null : Math.max(0, Math.ceil((endMs - renderedAt) / 86_400_000));
  const progress = Math.max(0, Math.min(100, engagement.progress));
  const severityTotal = (Object.keys(SEVERITY_COLOR) as Severity[]).reduce(
    (total, severity) => total + (engagement.findingsBySeverity[severity] ?? 0),
    0,
  );
  const metrics = [
    { label: "Findings", value: engagement.findingCount, detail: "recorded issues", color: "var(--sev-critical-color)", icon: AlertTriangle },
    { label: "Assets", value: engagement.assetCount, detail: "in attack surface", color: "var(--accent)", icon: Network },
    { label: "Progress", value: `${progress}%`, detail: "assessment complete", color: "var(--nominal-color)", icon: CircleDot, progress },
    { label: "Time remaining", value: daysLeft == null ? "—" : `${daysLeft}d`,
      detail: daysLeft == null ? "no end date set" : `ends ${displayDate(engagement.endDate)}`, color: "var(--sev-medium-color)", icon: Clock3 },
  ];

  const details = [
    { label: "Client", value: engagement.client || "Not assigned", icon: Users },
    { label: "Lead assessor", value: engagement.assessor || "Not assigned", icon: UserRound },
    { label: "Start date", value: displayDate(engagement.startDate), icon: CalendarDays },
    { label: "End date", value: displayDate(engagement.endDate), icon: CalendarDays },
  ];

  return (
    <div className="engagement-stack">
      <section className="engagement-metric-grid" aria-label="Engagement summary">
        {metrics.map(({ label, value, detail, color, icon: Icon, progress: metricProgress }) => (
          <article className="engagement-metric-card" key={label} style={{ "--metric-color": color } as React.CSSProperties}>
            <div className="engagement-metric-label"><span><Icon size={16} /></span>{label}</div>
            <strong>{value}</strong>
            <span className="engagement-metric-detail">{detail}</span>
            {typeof metricProgress === "number" && (
              <div
                className="engagement-metric-progress"
                role="progressbar"
                aria-label="Assessment completion"
                aria-valuemin={0}
                aria-valuemax={100}
                aria-valuenow={metricProgress}
              >
                <span style={{ width: `${metricProgress}%` }} />
              </div>
            )}
          </article>
        ))}
      </section>

      <section className="engagement-overview-grid">
        <article className="engagement-panel">
          <header><div><Shield size={16} /><span>Engagement brief</span></div><span className="badge badge-info">Authorized scope</span></header>
          <div className="engagement-panel-body">
            <p className="engagement-description">
              {engagement.description || "No assessment brief has been added yet. Add context so operators and client reviewers share the same objective."}
            </p>
            <div className="engagement-detail-grid">
              {details.map(({ label, value, icon: Icon }) => (
                <div className="engagement-detail" key={label}>
                  <Icon size={14} />
                  <div><span>{label}</span><strong>{value}</strong></div>
                </div>
              ))}
            </div>
            {engagement.tags?.length > 0 && (
              <div className="engagement-tags"><Tags size={13} />{engagement.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
            )}
          </div>
        </article>

        <article className="engagement-panel">
          <header><div><Target size={16} /><span>Scope boundaries</span></div><span>{engagement.scopeCidrs.length} {engagement.scopeCidrs.length === 1 ? "target" : "targets"}</span></header>
          <div className="engagement-panel-body engagement-scope">
            <div>
              <span className="engagement-field-label">Included networks and hosts</span>
              <div className="engagement-chip-list">
                {engagement.scopeCidrs.length
                  ? engagement.scopeCidrs.map((cidr) => <code className="engagement-chip included" key={cidr}>{cidr}</code>)
                  : <span className="engagement-empty-inline">No scope recorded</span>}
              </div>
            </div>
            <div>
              <span className="engagement-field-label">Explicit exclusions</span>
              <div className="engagement-chip-list">
                {engagement.excludedCidrs.length
                  ? engagement.excludedCidrs.map((cidr) => <code className="engagement-chip excluded" key={cidr}>{cidr}</code>)
                  : <span className="engagement-empty-inline">No exclusions recorded</span>}
              </div>
            </div>
            <div className="engagement-scope-note">
              <Shield size={14} />
              Scans must remain inside included scope and must never target an excluded address.
            </div>
          </div>
        </article>
      </section>

      <RegulatoryProfilePanel engagementId={engagement.id} surface={surface} />

      <article className="engagement-panel engagement-severity-panel">
        <header>
          <div><AlertTriangle size={16} /><span>Finding distribution</span></div>
          <Link href={`${surface === "portal" ? "/portal/findings" : "/findings"}?engagement=${engagement.id}`}>Open findings <ChevronRight size={14} /></Link>
        </header>
        <div className="engagement-severity-body">
          <div className="engagement-severity-summary">
            <div
              className="engagement-severity-bar"
              role="img"
              aria-label={`${severityTotal} scored findings grouped by severity`}
              data-empty={severityTotal === 0}
            >
              {(Object.keys(SEVERITY_COLOR) as Severity[]).map((severity) => {
                const count = engagement.findingsBySeverity[severity] ?? 0;
                if (!count || !severityTotal) return null;
                return <span key={severity} style={{ width: `${(count / severityTotal) * 100}%`, background: SEVERITY_COLOR[severity] }} />;
              })}
            </div>
            <span>{severityTotal} scored {severityTotal === 1 ? "finding" : "findings"}</span>
          </div>
          <div className="engagement-severity-grid">
            {(Object.keys(SEVERITY_COLOR) as Severity[]).map((severity) => (
              <div key={severity} style={{ "--severity-color": SEVERITY_COLOR[severity] } as React.CSSProperties}>
                <span className="engagement-severity-dot" />
                <div>
                  <strong>{engagement.findingsBySeverity[severity] ?? 0}</strong>
                  <small>{severity.toLowerCase()}</small>
                </div>
              </div>
            ))}
          </div>
        </div>
      </article>
    </div>
  );
}

function FindingsTab({ engagementId, surface }: { engagementId: string; surface: EngagementWorkspaceSurface }) {
  const [page, setPage] = useState(1);
  const api = useMemo(() => createEngagementWorkspaceApi(surface), [surface]);
  const query = useQuery({
    queryKey: ["engagement-findings", surface, engagementId, page],
    queryFn: () => api.findings<FindingPage>(engagementId, page),
  });
  const rows = query.data?.items ?? [];
  const total = query.data?.total ?? 0;
  const pages = query.data?.pages ?? 1;
  const currentPage = query.data?.page ?? page;

  return (
    <DataState
      loading={query.isLoading}
      error={query.error}
      isEmpty={rows.length === 0}
      onRetry={() => query.refetch()}
      skeleton={<SkeletonRows rows={5} height={58} />}
      empty={<EmptyState icon={AlertTriangle} title="No findings in this engagement" hint="Import evidence or run an authorized scan to populate findings." />}
    >
      <div className="engagement-list-panel">
        <div className="engagement-list-heading"><span>Highest risk first</span><span>{total} findings · 20 per page</span></div>
        {rows.map((finding) => (
          <Link href={`${surface === "portal" ? "/portal/findings" : "/findings"}?engagement=${engagementId}&finding=${finding.id}`} className="engagement-finding-row" key={finding.id}>
            <span className={`badge badge-${finding.severity.toLowerCase()}`}>{finding.severity}</span>
            <div><strong>{finding.title}</strong><small>{finding.affectedHost} · {finding.status.replaceAll("_", " ")}</small></div>
            <span className="engagement-risk-score"><small>Risk</small><strong>{finding.riskScore}</strong></span>
            <ChevronRight size={14} />
          </Link>
        ))}
        {total > 0 && (
          <nav className="findings-pagination" aria-label="Engagement findings pagination">
            <div>
              Showing <strong>{(currentPage - 1) * 20 + 1}</strong>–
              <strong>{Math.min(currentPage * 20, total)}</strong> of <strong>{total}</strong>
            </div>
            <span>20 per page</span>
            <div className="findings-pagination-controls">
              <button type="button" onClick={() => setPage((value) => Math.max(1, value - 1))} disabled={currentPage === 1} aria-label="Previous findings page"><ChevronLeft size={14} /></button>
              <span>Page {currentPage} of {pages}</span>
              <button type="button" onClick={() => setPage((value) => Math.min(pages, value + 1))} disabled={currentPage === pages} aria-label="Next findings page"><ChevronRight size={14} /></button>
            </div>
          </nav>
        )}
      </div>
    </DataState>
  );
}

function AssetsTab({ engagementId, surface }: { engagementId: string; surface: EngagementWorkspaceSurface }) {
  const api = useMemo(() => createEngagementWorkspaceApi(surface), [surface]);
  const queryClient = useQueryClient();
  const toast = useToast();
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const query = useQuery({
    queryKey: ["assets", surface, engagementId],
    queryFn: () => api.assets<AssetRow[]>(engagementId),
    refetchInterval: 20_000,
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const assets = useMemo(() => query.data ?? [], [query.data]);
  const counts = useMemo(() => tagCounts(assets), [assets]);
  const visible = useMemo(() => filterAssetsByTags(assets, selectedTags), [assets, selectedTags]);
  const toggle = (tag: string) => setSelectedTags((current) =>
    current.includes(tag) ? current.filter((item) => item !== tag) : [...current, tag]);
  const refresh = () => queryClient.invalidateQueries({ queryKey: ["assets", surface, engagementId] });

  const retag = useMutation({
    mutationFn: () => api.retag<{ retagged: number }>(engagementId),
    onSuccess: (data) => {
      void refresh();
      void queryClient.invalidateQueries({ queryKey: ["compliance", surface, engagementId] });
      toast.success("Tags recomputed", `${data.retagged} hosts re-evaluated from recorded evidence.`);
    },
    onError: (error) => toast.error("Re-tag failed", error instanceof Error ? error.message : "Unknown error"),
  });

  return (
    <DataState
      loading={query.isLoading}
      error={query.error}
      isEmpty={assets.length === 0}
      onRetry={() => query.refetch()}
      skeleton={<SkeletonRows rows={5} height={72} />}
      empty={<EmptyState icon={Network} title="No hosts discovered yet" hint="Run discovery from this engagement to build the attack surface." />}
    >
      <div className="intel-assets-toolbar">
        <TagFilterBar
          counts={counts}
          selected={selectedTags}
          onToggle={toggle}
          onClear={() => setSelectedTags([])}
          total={assets.length}
          shown={visible.length}
        />
        {api.canEditIntel && (
          <button type="button" className="btn btn-secondary" disabled={retag.isPending} onClick={() => retag.mutate()}
            title="Re-derive tags for every host from the evidence already recorded">
            {retag.isPending ? <Loader2 size={13} className="animate-spin" /> : <RefreshCw size={13} />} Re-tag hosts
          </button>
        )}
      </div>
      {visible.length === 0 && (
        <EmptyState icon={Tags} title="No host carries every selected tag" hint="Remove a tag from the filter to widen the view." />
      )}
      <div className="engagement-asset-grid">
        {visible.map((asset) => (
          <article className="engagement-asset-card" key={asset.id}>
            <header>
              <span><Network size={15} /> <code>{asset.ip_address || "Address unavailable"}</code></span>
              <span className="badge badge-info">{asset.criticality}</span>
            </header>
            <div className="engagement-asset-meta">{asset.hostname || "Unknown host"} · {asset.os || "OS not identified"}</div>
            {fragileReasons(asset).length > 0 && (
              <div className="intel-fragile" title={`Fragile: ${fragileReasons(asset).join(", ")}. Intrusive scans skip this host unless an admin/manager overrides with a reason.`}>
                <Shield size={12} /> Fragile · gentle scans only
              </div>
            )}
            <AssetTagList asset={asset} selected={selectedTags} onToggle={toggle} />
            {api.canEditIntel && (
              <ManualTagEditor
                asset={asset}
                onSave={async (tags) => {
                  await api.setAssetTags(engagementId, asset.id, tags);
                  toast.success("Tags saved", asset.ip_address ?? asset.hostname ?? "Host updated");
                  await refresh();
                }}
              />
            )}
            <div className="engagement-service-list">
              {asset.services.length ? asset.services.map((service, index) => (
                <div key={`${service.port}-${index}`}>
                  <code>{service.port}/{service.protocol}</code>
                  <span>{service.service || "unknown service"}</span>
                  <small>{[service.product, service.version].filter(Boolean).join(" ") || "No banner"}</small>
                </div>
              )) : <span className="engagement-empty-inline">No open services recorded</span>}
            </div>
          </article>
        ))}
      </div>
    </DataState>
  );
}

function ActivityTab({ activity }: { activity: ActivityItem[] }) {
  if (!activity.length) return <EmptyState icon={Activity} title="No engagement activity yet" hint="Scan, import, and review events will appear here." />;
  return (
    <div className="engagement-timeline">
      {activity.map((item) => (
        <div key={item.id}>
          <span className="engagement-timeline-dot" />
          <article>
            <header><strong>{item.action}</strong><time>{new Date(item.timestamp).toLocaleString()}</time></header>
            <p>{item.detail}</p><small>Actor: {item.actor}</small>
          </article>
        </div>
      ))}
    </div>
  );
}

function ImportScanButton({ engagementId, surface }: { engagementId: string; surface: EngagementWorkspaceSurface }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const toast = useToast();
  const queryClient = useQueryClient();
  const api = useMemo(() => createEngagementWorkspaceApi(surface), [surface]);

  async function pickFile(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    setBusy(true);
    try {
      const form = new FormData();
      form.append("file", file);
      const data = await api.importFacts<{ fact_count?: number }>(engagementId, form);
      toast.success("Evidence imported", `${data.fact_count ?? 0} facts accepted; detection processing has started.`);
      void queryClient.invalidateQueries({ queryKey: ["engagement", surface, engagementId] });
      void queryClient.invalidateQueries({ queryKey: ["assets", surface, engagementId] });
      void queryClient.invalidateQueries({ queryKey: ["engagement-findings", surface, engagementId] });
    } catch (error) {
      toast.error("Import failed", error instanceof Error ? error.message : "Unknown error");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <input ref={inputRef} type="file" accept=".json,.jsonl,application/json" onChange={pickFile} hidden />
      <button type="button" className="btn btn-secondary engagement-action" disabled={busy} onClick={() => inputRef.current?.click()}>
        {busy ? <Loader2 size={14} className="animate-spin" /> : <Upload size={14} />}
        {busy ? "Importing…" : "Import evidence"}
      </button>
    </>
  );
}

const EDIT_STATUSES = ["PLANNING", "ACTIVE", "PAUSED", "COMPLETED"] as const;

function EditEngagementModal({ engagement, surface, onClose }: { engagement: Engagement; surface: EngagementWorkspaceSurface; onClose: () => void }) {
  const queryClient = useQueryClient();
  const toast = useToast();
  const api = useMemo(() => createEngagementWorkspaceApi(surface), [surface]);
  const [form, setForm] = useState({
    name: engagement.name || "",
    client: engagement.client === "—" ? "" : engagement.client || "",
    assessor: engagement.assessor === "—" ? "" : engagement.assessor || "",
    description: engagement.description || "",
    status: engagement.status || "PLANNING",
    startDate: (engagement.startDate || "").slice(0, 10),
    endDate: (engagement.endDate || "").slice(0, 10),
    scopeCidrs: engagement.scopeCidrs.join(", "),
    excludedCidrs: engagement.excludedCidrs.join(", "),
    tags: engagement.tags.join(", "),
  });
  const update = (change: Partial<typeof form>) => setForm((current) => ({ ...current, ...change }));
  const scope = form.scopeCidrs.split(/[\s,]+/).filter(Boolean);
  const datesValid = !form.startDate || !form.endDate || form.endDate >= form.startDate;
  const valid = Boolean(form.name.trim() && scope.length && datesValid);

  const mutation = useMutation({
    mutationFn: () => api.update(engagement.id, form),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["engagement", surface, engagement.id] });
      void queryClient.invalidateQueries({ queryKey: ["engagements"] });
      toast.success("Engagement updated", "Scope and assessment details were saved.");
      onClose();
    },
    onError: (error) => toast.error("Update failed", error instanceof Error ? error.message : "Could not save changes."),
  });

  return (
    <div className="engagement-modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <div className="engagement-modal" role="dialog" aria-modal="true" aria-labelledby="edit-engagement-title">
        <header>
          <div><span className="engagement-modal-icon"><Pencil size={16} /></span><div><h2 id="edit-engagement-title">Edit engagement</h2><p>Keep client context and scope boundaries accurate.</p></div></div>
          <button type="button" aria-label="Close edit dialog" onClick={onClose}><X size={18} /></button>
        </header>
        <div className="engagement-form">
          <label className="engagement-form-wide"><span>Engagement name *</span><input value={form.name} onChange={(event) => update({ name: event.target.value })} /></label>
          <label><span>Client</span><input value={form.client} onChange={(event) => update({ client: event.target.value })} placeholder="Organization name" /></label>
          <label><span>Lead assessor</span><input value={form.assessor} onChange={(event) => update({ assessor: event.target.value })} placeholder="Assessment owner" /></label>
          <label><span>Status</span><select value={form.status} onChange={(event) => update({ status: event.target.value })}>{EDIT_STATUSES.map((status) => <option key={status}>{status}</option>)}</select></label>
          <label><span>Tags</span><input value={form.tags} onChange={(event) => update({ tags: event.target.value })} placeholder="external, web, pci" /></label>
          <label><span>Start date</span><input type="date" value={form.startDate} onChange={(event) => update({ startDate: event.target.value })} /></label>
          <label><span>End date</span><input type="date" min={form.startDate || undefined} value={form.endDate} onChange={(event) => update({ endDate: event.target.value })} /></label>
          <label className="engagement-form-wide"><span>Assessment brief</span><textarea rows={3} value={form.description} onChange={(event) => update({ description: event.target.value })} placeholder="Objective, constraints, and expected outcome" /></label>
          <label className="engagement-form-wide"><span>Included IPs / CIDRs *</span><textarea rows={3} value={form.scopeCidrs} onChange={(event) => update({ scopeCidrs: event.target.value })} /><small>Comma, space, or newline separated. At least one valid scope entry is required.</small></label>
          <label className="engagement-form-wide"><span>Excluded IPs / CIDRs</span><textarea rows={2} value={form.excludedCidrs} onChange={(event) => update({ excludedCidrs: event.target.value })} /><small>Explicit exclusions always take precedence over included networks.</small></label>
          {!datesValid && <div className="engagement-form-error">End date must be on or after the start date.</div>}
        </div>
        <footer>
          <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button type="button" className="btn btn-primary" disabled={!valid || mutation.isPending} onClick={() => mutation.mutate()}>
            {mutation.isPending ? <Loader2 size={14} className="animate-spin" /> : <Check size={14} />} Save changes
          </button>
        </footer>
      </div>
    </div>
  );
}

export function EngagementWorkspace({
  engagementId,
  surface = "manager",
  initialSection = "overview",
  initialFindingId,
}: {
  engagementId?: string;
  surface?: EngagementWorkspaceSurface;
  initialSection?: TabKey;
  initialFindingId?: string;
}) {
  const id = engagementId ?? "current";
  const [activeTab, setActiveTab] = useState<TabKey>(initialSection);
  const [editing, setEditing] = useState(false);
  const api = useMemo(() => createEngagementWorkspaceApi(surface), [surface]);
  const query = useQuery({
    queryKey: ["engagement", surface, id],
    queryFn: () => api.detail<{ engagement: Engagement; activity?: ActivityItem[] }>(id),
  });
  const engagement = query.data?.engagement;
  const activity = query.data?.activity ?? [];

  // Live scan state, shown BESIDE the status control rather than inside it: the
  // stored status is the operator's intent, this is an observed fact.
  const progress = useQuery({
    queryKey: ["engagement-progress", surface, id],
    queryFn: () => api.progress<{ job_stats?: { running?: number } }>(id),
    refetchInterval: 20_000,
  });
  const runningJobs = progress.data?.job_stats?.running ?? 0;
  const tabs = useMemo(() => [
    { key: "overview" as const, label: "Overview", icon: Shield },
    { key: "findings" as const, label: "Findings", icon: AlertTriangle, count: engagement?.findingCount },
    { key: "assets" as const, label: "Attack surface", icon: Network, count: engagement?.assetCount },
    ...(surface === "manager" && process.env.NEXT_PUBLIC_ATTACK_ASSESSMENTS_ENABLED === "true"
      ? [{ key: "attack-assessments" as const, label: "Attack paths", icon: Target, count: undefined }]
      : []),
    { key: "activity" as const, label: "Activity", icon: Activity, count: activity.length },
  ], [activity.length, engagement?.assetCount, engagement?.findingCount, surface]);

  const Shell = surface === "portal" ? PortalShell : PageShell;

  return (
    <Shell
      title={query.isLoading ? "Loading engagement…" : engagement?.name || "Engagement"}
      subtitle={engagement ? `${engagement.client || "Unassigned client"} · ${engagement.assessor || "No assessor"}` : undefined}
      headerActions={
        <div className="engagement-actions">
          {engagement && (
            <EngagementStatusControl
              engagementId={id}
              status={engagement.status}
              queryScope={surface}
              updateStatus={(next) => api.update(id, { status: next })}
              liveHint={runningJobs > 0
                ? `${runningJobs} scan${runningJobs === 1 ? "" : "s"} running`
                : null}
            />
          )}
          {engagement && <button type="button" className="btn btn-secondary engagement-action" onClick={() => setEditing(true)}><Pencil size={14} /> Edit details</button>}
          <ImportScanButton engagementId={id} surface={surface} />
          <Link className="btn btn-primary engagement-action" href={`${surface === "portal" ? "/portal/scans" : "/scan"}?engagementId=${encodeURIComponent(id)}`}><Play size={14} /> Start scan</Link>
        </div>
      }
      statusItems={engagement ? [
        { label: "STATUS", value: engagement.status, color: STATUS_COLOR[engagement.status] || "var(--text-secondary)" },
      ] : []}
    >
      <div className="engagement-workspace">
        {/* On a phone the header has no room for three buttons, and the one that matters
            (Start scan) scrolled out of sight. The same actions sit here instead, full width. */}
        {engagement && (
          <div className="engagement-mobile-actions" role="group" aria-label="Engagement actions">
            <Link className="btn btn-primary engagement-action" href={`${surface === "portal" ? "/portal/scans" : "/scan"}?engagementId=${encodeURIComponent(id)}`}><Play size={14} aria-hidden /> Start scan</Link>
            <ImportScanButton engagementId={id} surface={surface} />
            <button type="button" className="btn btn-secondary engagement-action" onClick={() => setEditing(true)}><Pencil size={14} aria-hidden /> Edit details</button>
          </div>
        )}
        <div className="engagement-toolbar">
          <Link href={surface === "portal" ? "/portal" : "/engagements"} className="engagement-back"><ArrowLeft size={15} /> {surface === "portal" ? "Dashboard" : "All engagements"}</Link>
          <nav aria-label="Engagement sections" role="tablist">
            {tabs.map(({ key, label, icon: Icon, count }) => (
              <button
                type="button"
                key={key}
                id={`engagement-tab-${key}`}
                role="tab"
                aria-selected={activeTab === key}
                tabIndex={activeTab === key ? 0 : -1}
                aria-controls="engagement-tabpanel"
                data-active={activeTab === key}
                onClick={() => setActiveTab(key)}
                onKeyDown={(event) => {
                  const index = tabs.findIndex((tab) => tab.key === key);
                  const next = event.key === "ArrowRight" ? (index + 1) % tabs.length
                    : event.key === "ArrowLeft" ? (index + tabs.length - 1) % tabs.length
                    : event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : -1;
                  if (next < 0) return;
                  event.preventDefault();
                  setActiveTab(tabs[next].key);
                  document.getElementById(`engagement-tab-${tabs[next].key}`)?.focus();
                }}
              >
                <Icon size={15} /> {label}{typeof count === "number" && <span>{count}</span>}
              </button>
            ))}
          </nav>
          <div className="engagement-toolbar-links">
            {surface === "manager" && (
              <Link href={`/engagements/${encodeURIComponent(id)}/attack-paths`} className="engagement-attack-link"><Route size={15} /> {process.env.NEXT_PUBLIC_ATTACK_ASSESSMENTS_ENABLED === "true" ? "Expand chain workspace" : "Attack paths"} <span className="badge badge-info">Beta</span></Link>
            )}
            <Link href={surface === "portal" ? "/portal/reports" : "/reports"} className="engagement-report-link"><FileText size={15} /> Reports <span className="badge badge-info">Beta</span></Link>
          </div>
        </div>

        <div
          className="engagement-content"
          id="engagement-tabpanel"
          role="tabpanel"
          aria-labelledby={`engagement-tab-${activeTab}`}
        >
          {query.isLoading && <SkeletonRows rows={5} height={76} />}
          {query.error && <EmptyState icon={AlertTriangle} title="Could not load this engagement" hint="Check the Manager API connection and your access, then retry." />}
          {engagement && activeTab === "overview" && <OverviewTab engagement={engagement} surface={surface} />}
          {engagement && activeTab === "findings" && <FindingsTab engagementId={id} surface={surface} />}
          {engagement && activeTab === "assets" && <AssetsTab engagementId={id} surface={surface} />}
          {engagement && surface === "manager" && activeTab === "attack-assessments" && <AttackAssessmentsPanel engagementId={id} initialFindingId={initialFindingId} />}
          {engagement && activeTab === "activity" && <ActivityTab activity={activity} />}
        </div>
      </div>

      {editing && engagement && <EditEngagementModal engagement={engagement} surface={surface} onClose={() => setEditing(false)} />}
    </Shell>
  );
}

export default function EngagementDetailPage({ params, searchParams }: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ section?: string | string[]; finding?: string | string[] }>;
}) {
  const { id } = use(params);
  const query = use(searchParams);
  const section = query.section === "attack-assessments" && process.env.NEXT_PUBLIC_ATTACK_ASSESSMENTS_ENABLED === "true" ? "attack-assessments" : "overview";
  const finding = typeof query.finding === "string" ? query.finding : undefined;
  return <EngagementWorkspace key={`${id}:${section}:${finding ?? ""}`} engagementId={id} initialSection={section} initialFindingId={finding} />;
}
