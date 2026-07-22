"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";
import {
  Play, Shield, Globe, Database, Server, Wifi,
  Activity, Eye, RefreshCw, ChevronDown,
  CheckCircle2, Clock, XCircle, Loader,
  Cpu, Network, RotateCcw, Target, Layers,
  Lock, KeyRound, Timer, ShieldAlert, Crosshair, Send, Radar,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useToast } from "../../hooks/useToast";

/* ══════════════════════════════════════════════════════
   TYPES
══════════════════════════════════════════════════════ */

interface UseCase {
  use_case_id: string;
  display_name: string;
  description: string;
  scan_type: string;
  profile: "it" | "iot" | "ot";
  expected_runtime_hint: string;
}

interface Probe {
  id: string;
  name: string;
  location: string | null;
  status: string;
  capabilities: string[];
  network_segments: string[];
  last_heartbeat: string | null;
  current_job_id: string | null;
  online: boolean;
}

interface Engagement {
  id: string;
  name: string;
  status: string;
  scopeCidrs?: string[];
  excludedCidrs?: string[];
}

interface JobStatus {
  job_id: string;
  engagement_id: string;
  status: "pending" | "running" | "completed" | "failed";
  created_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  agent_id: string | null;
  agent_name: string | null;
  use_case_id: string | null;
  result: Record<string, unknown> | null;
}

/* ══════════════════════════════════════════════════════
   METADATA
══════════════════════════════════════════════════════ */

const UC_META: Record<string, { cat: string; icon: React.ReactNode; risk: "passive" | "low" | "medium" | "high" }> = {
  uc_discovery_only:       { cat: "Discovery",   icon: <Network size={17} />,   risk: "low"     },
  uc_iot_device_survey:    { cat: "Discovery",   icon: <Wifi size={17} />,      risk: "low"     },
  uc_full_assessment:      { cat: "Assessment",  icon: <Shield size={17} />,    risk: "high"    },
  uc_rescan_delta:         { cat: "Assessment",  icon: <RefreshCw size={17} />, risk: "high"    },
  uc_external_web_triage:  { cat: "Targeted",    icon: <Globe size={17} />,     risk: "medium"  },
  uc_web_app_triage:       { cat: "Targeted",    icon: <Globe size={17} />,     risk: "medium"  },
  uc_db_exposure:          { cat: "Targeted",    icon: <Database size={17} />,  risk: "medium"  },
  uc_windows_estate:       { cat: "Targeted",    icon: <Server size={17} />,    risk: "medium"  },
  uc_udp_service_exposure: { cat: "Targeted",    icon: <Activity size={17} />,  risk: "medium"  },
  uc_ot_passive:           { cat: "Specialized", icon: <Eye size={17} />,       risk: "passive" },
  uc_ai_endpoint_sweep:    { cat: "Specialized", icon: <Cpu size={17} />,       risk: "medium"  },
};

const RISK: Record<string, { color: string; label: string }> = {
  passive: { color: "#6ee7b7",                label: "Passive"  },
  low:     { color: "var(--sev-low-color)",    label: "Low noise" },
  medium:  { color: "var(--sev-medium-color)", label: "Moderate" },
  high:    { color: "var(--sev-high-color)",   label: "Active"   },
};

const PROFILE_BADGE: Record<string, { label: string; color: string }> = {
  it:  { label: "IT",  color: "var(--accent)" },
  iot: { label: "IoT", color: "#f59e0b"       },
  ot:  { label: "OT",  color: "#10b981"       },
};

const CATS = ["All", "Discovery", "Assessment", "Targeted", "Specialized"] as const;
type Cat = typeof CATS[number];

/* Scan-intensity presets — the one offensive-security knob operators reason about
   (nmap-style timing). The BFF resolves each to a rate/concurrency/timeout tuple. */
type Intensity = "stealth" | "normal" | "aggressive";
const INTENSITY: { id: Intensity; label: string; pps: string; why: string; color: string; angle: number; sweep: string }[] = [
  { id: "stealth",    label: "Stealth",    pps: "50 pps",  color: "#6ee7b7",             angle: -60, sweep: "6.2s",
    why: "Low and slow. Minimizes IDS/IPS triggers and link load — for monitored, production, or fragile segments." },
  { id: "normal",     label: "Normal",     pps: "200 pps", color: "var(--accent)",        angle: 0,   sweep: "3.4s",
    why: "Balanced default. Right for most internal engagements with no special constraints." },
  { id: "aggressive", label: "Aggressive", pps: "600 pps", color: "var(--sev-high-color)", angle: 60,  sweep: "1.3s",
    why: "Fast and loud. Large scopes under time pressure — expect alerts and noticeable traffic." },
];

/* ══════════════════════════════════════════════════════
   AUTH HELPER
══════════════════════════════════════════════════════ */

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("vedha_token") || sessionStorage.getItem("vedha_token");
}

async function apiFetch<T>(path: string, opts?: RequestInit): Promise<T> {
  const token = getToken();
  const res = await fetch(path, {
    ...opts,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(opts?.headers ?? {}),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText })) as { error?: string };
    throw new Error(err.error ?? res.statusText);
  }
  return res.json() as Promise<T>;
}

/* ══════════════════════════════════════════════════════
   SMALL PRIMITIVES
══════════════════════════════════════════════════════ */

const SectionLabel = ({ children, num }: { children: React.ReactNode; num?: string }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
    {num && (
      <span style={{ fontSize: 9.5, fontWeight: 700, fontFamily: "var(--font-mono)", color: "var(--accent)", background: "var(--accent-ghost)", border: "0.5px solid var(--border-accent)", borderRadius: 5, padding: "2px 6px", letterSpacing: 0.5 }}>
        {num}
      </span>
    )}
    <span style={{ fontSize: 10.5, fontWeight: 700, color: "var(--text-faint)", letterSpacing: 1.4, textTransform: "uppercase" }}>{children}</span>
  </div>
);

const FieldLabel = ({ icon, children, hint }: { icon?: React.ReactNode; children: React.ReactNode; hint?: string }) => (
  <label style={{ fontSize: 10.5, fontWeight: 600, color: "var(--text-secondary)", display: "flex", alignItems: "center", gap: 6, marginBottom: 7, letterSpacing: 0.5, textTransform: "uppercase" }}>
    {icon}{children}
    {hint && <span style={{ fontWeight: 400, color: "var(--text-faint)", textTransform: "none", letterSpacing: 0, fontSize: 10 }}>{hint}</span>}
  </label>
);

/** HUD corner-bracket frame — the page's recurring "locked on" motif.
    Wraps any element; brackets fade in when `active` flips true. */
function HudFrame({ active, radius = 14, children, style }: { active: boolean; radius?: number; children: React.ReactNode; style?: React.CSSProperties }) {
  return (
    <div style={{ position: "relative", borderRadius: radius, ...style }}>
      {children}
      {(["tl", "tr", "bl", "br"] as const).map((pos) => (
        <span key={pos} className={`scn-hud scn-hud-${pos}`} data-active={active} />
      ))}
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   FLEET STRIP (probe health)
══════════════════════════════════════════════════════ */

function FleetStrip({ probes, loading }: { probes: Probe[]; loading: boolean }) {
  const online = probes.filter((p) => p.online).length;
  const busy   = probes.filter((p) => p.current_job_id).length;
  const idle   = online - busy;

  return (
    <div className="scn-fleet" style={{ display: "flex", alignItems: "center", gap: 14, padding: "12px 18px", borderRadius: 13, background: "var(--bg-panel)", border: "0.5px solid var(--border-subtle)", flexWrap: "wrap", position: "relative", overflow: "hidden" }}>
      {/* live heartbeat trace */}
      <div style={{ position: "absolute", left: 0, top: 0, width: 220, height: 28, opacity: 0.45, pointerEvents: "none" }}>
        <svg viewBox="0 0 220 28" preserveAspectRatio="none" style={{ width: "100%", height: "100%" }}>
          <path d="M0,14 L55,14 L63,4 L71,24 L79,14 L220,14" fill="none" stroke="var(--nominal-color)" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 8, position: "relative" }}>
        <span style={{ position: "relative", display: "inline-flex", width: 8, height: 8 }}>
          <span className="scn-ping" style={{ position: "absolute", inset: 0, borderRadius: "50%", background: online ? "var(--nominal-color)" : "var(--text-faint)" }} />
          <span style={{ position: "relative", width: 8, height: 8, borderRadius: "50%", background: online ? "var(--nominal-color)" : "var(--text-faint)" }} />
        </span>
        <span style={{ fontSize: 13, fontWeight: 700, color: "var(--text-primary)", fontFamily: "var(--font-display)", letterSpacing: 0.3, textTransform: "uppercase" }}>Probe Fleet</span>
      </div>

      <div style={{ width: 1, height: 18, background: "var(--border-subtle)" }} />

      {loading ? (
        <span style={{ fontSize: 12, color: "var(--text-muted)" }}>Loading…</span>
      ) : !probes.length ? (
        <span style={{ fontSize: 12, color: "var(--text-muted)" }}>No probes registered — deploy an agent to begin</span>
      ) : (
        <>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            {([["online", online, "var(--nominal-color)"], ["idle", idle, "var(--sev-low-color)"], ["scanning", busy, "var(--sev-medium-color)"]] as [string, number, string][]).map(([k, v, c]) => (
              <span key={k} style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
                <span style={{ fontSize: 15, fontWeight: 700, fontFamily: "var(--font-mono)", color: v > 0 ? c : "var(--text-faint)", lineHeight: 1 }}>{v}</span>
                <span style={{ fontSize: 10.5, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: 0.6 }}>{k}</span>
              </span>
            ))}
          </div>

          <div style={{ display: "flex", gap: 6, marginLeft: "auto", flexWrap: "wrap" }}>
            {probes.map((p) => {
              const dot = !p.online ? "var(--text-faint)" : p.current_job_id ? "var(--sev-medium-color)" : "var(--nominal-color)";
              return (
                <span key={p.id} title={p.location ?? undefined} style={{ display: "flex", alignItems: "center", gap: 6, padding: "4px 9px", borderRadius: 7, background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)", fontSize: 11 }}>
                  <span style={{ width: 6, height: 6, borderRadius: "50%", background: dot }} />
                  <span style={{ color: "var(--text-secondary)", fontWeight: 500 }}>{p.name}</span>
                </span>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   USE-CASE CARD
══════════════════════════════════════════════════════ */

function UseCaseCard({ uc, selected, index, onClick }: { uc: UseCase; selected: boolean; index: number; onClick: () => void }) {
  const meta = UC_META[uc.use_case_id] ?? { cat: "Other", icon: <Target size={17} />, risk: "medium" as const };
  const risk = RISK[meta.risk];
  const prof = PROFILE_BADGE[uc.profile];
  return (
    <button className="scn-card" data-sel={selected} onClick={onClick} style={{ animationDelay: `${index * 45}ms` }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 9 }}>
        <span className="scn-card-icon" data-sel={selected}>{meta.icon}</span>
        <span style={{ fontWeight: 650, fontSize: 13, color: "var(--text-primary)", lineHeight: 1.25, flex: 1 }}>{uc.display_name}</span>
        {selected && <CheckCircle2 size={16} color="var(--accent)" style={{ flexShrink: 0 }} />}
      </div>
      <p style={{ margin: "0 0 11px", fontSize: 11.5, color: "var(--text-muted)", lineHeight: 1.5, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden", minHeight: 34 }}>
        {uc.description}
      </p>
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={{ fontSize: 9.5, fontWeight: 700, color: prof.color, background: `color-mix(in srgb, ${prof.color} 12%, transparent)`, border: `0.5px solid color-mix(in srgb, ${prof.color} 35%, transparent)`, borderRadius: 5, padding: "2px 6px", letterSpacing: 0.3 }}>{prof.label}</span>
        <span style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 10, color: risk.color }}>
          <span style={{ width: 5, height: 5, borderRadius: "50%", background: risk.color }} />{risk.label}
        </span>
        <span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>{uc.expected_runtime_hint}</span>
      </div>
    </button>
  );
}

/* ══════════════════════════════════════════════════════
   INTENSITY DIAL — radar-style gauge that doubles as the rate
   selector. Color and sweep speed both encode aggression.
══════════════════════════════════════════════════════ */

function IntensityDial({ value, onChange }: { value: Intensity; onChange: (v: Intensity) => void }) {
  const active = INTENSITY.find((i) => i.id === value)!;

  // semicircle gauge, three 60° zones, radius 78, center (100,96)
  const arcs = [
    { d: "M22,96 A78,78 0 0 1 61,29.4",   color: "#6ee7b7" },
    { d: "M61,29.4 A78,78 0 0 1 139,29.4", color: "var(--accent)" },
    { d: "M139,29.4 A78,78 0 0 1 178,96",  color: "var(--sev-high-color)" },
  ];

  return (
    <div>
      <div className="scn-dial-wrap">
        <div className="scn-dial-sweep" style={{ animationDuration: active.sweep, background: `conic-gradient(from 180deg at 50% 100%, transparent 0deg, color-mix(in srgb, ${active.color} 33%, transparent) 18deg, transparent 40deg)` }} />
        <svg viewBox="0 0 200 110" className="scn-dial-svg">
          {arcs.map((a, i) => (
            <path key={i} d={a.d} fill="none" stroke={a.color} strokeWidth="9" strokeLinecap="round" opacity={0.32} />
          ))}
          <g style={{ transform: `rotate(${active.angle}deg)`, transformOrigin: "100px 96px", transition: "transform 480ms var(--ease-out)" }}>
            <line x1="100" y1="96" x2="100" y2="26" stroke={active.color} strokeWidth="2.5" strokeLinecap="round" style={{ filter: `drop-shadow(0 0 5px ${active.color})` }} />
          </g>
          <circle cx="100" cy="96" r="5.5" fill="var(--bg-panel)" stroke={active.color} strokeWidth="2" />
        </svg>
        <div className="scn-dial-readout">
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 21, fontWeight: 700, color: active.color, lineHeight: 1 }}>{active.pps}</span>
          <span style={{ fontSize: 9.5, color: "var(--text-faint)", letterSpacing: 1.2, textTransform: "uppercase", marginTop: 3 }}>{active.label}</span>
        </div>
      </div>

      <div className="scn-dial-seg">
        {INTENSITY.map((opt) => (
          <button key={opt.id} data-on={value === opt.id} onClick={() => onChange(opt.id)} style={{ ["--seg-c" as string]: opt.color }}>
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: opt.color, flexShrink: 0 }} />
            {opt.label}
          </button>
        ))}
      </div>
      <p style={{ margin: "9px 0 0", fontSize: 10.5, color: "var(--text-muted)", lineHeight: 1.55 }}>{active.why}</p>
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   JOB PANEL
══════════════════════════════════════════════════════ */

const PHASES = ["Queued", "Dispatched", "Scanning", "Aggregating", "Complete"];

function JobPanel({ job, ucName }: { job: JobStatus; ucName?: string }) {
  const r = job.result ?? {};
  const elapsed = job.started_at && job.completed_at
    ? Math.round((new Date(job.completed_at).getTime() - new Date(job.started_at).getTime()) / 1000)
    : null;

  const ST: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
    pending:   { icon: <Clock size={13} />, color: "var(--text-muted)",        label: "Queued"    },
    running:   { icon: <Loader size={13} className="scn-spin" />, color: "var(--accent)", label: "Running" },
    completed: { icon: <CheckCircle2 size={13} />, color: "var(--nominal-color)", label: "Completed" },
    failed:    { icon: <XCircle size={13} />, color: "var(--sev-critical-color)", label: "Failed"    },
  };
  const s = ST[job.status] ?? ST.pending;
  const active = job.status === "pending" || job.status === "running";

  // Map the real coarse status onto the five-step ticker.
  const phaseIdx = job.status === "failed" ? -1
    : job.status === "completed" ? 4
    : job.status === "running" ? (job.started_at ? 2 : 1)
    : 0;

  return (
    <HudFrame active radius={12}>
    <div style={{ borderRadius: 12, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", overflow: "hidden", boxShadow: "var(--shadow-md)" }}>
      <div style={{ padding: "13px 16px", display: "flex", alignItems: "center", gap: 11, background: `color-mix(in srgb, ${s.color} 7%, transparent)`, borderBottom: "0.5px solid var(--border-subtle)" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 7, color: s.color, fontWeight: 700, fontSize: 12.5 }}>
          {s.icon} {s.label}
        </span>
        {ucName && <span style={{ fontSize: 12.5, color: "var(--text-secondary)", fontWeight: 500 }}>{ucName}</span>}
        {active && <span style={{ fontSize: 10.5, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>· polling 4s</span>}
        {elapsed !== null && <span style={{ marginLeft: "auto", fontSize: 11.5, color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>{elapsed}s</span>}
      </div>

      {/* phase ticker — replaces the flat indeterminate bar */}
      {job.status !== "failed" && (
        <div className="scn-ticker">
          {PHASES.map((p, i) => (
            <React.Fragment key={p}>
              <div className="scn-phase" data-state={i < phaseIdx ? "done" : i === phaseIdx ? "active" : "pending"}>
                <span className="scn-phase-dot" />
                <span className="scn-phase-label">{p}</span>
              </div>
              {i < PHASES.length - 1 && <span className="scn-phase-link" data-on={i < phaseIdx} />}
            </React.Fragment>
          ))}
        </div>
      )}

      {job.status === "completed" && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)" }}>
          {([
            ["Hosts",      (r.host_count    ?? (r.run_stats as Record<string, unknown>)?.host_count    ?? "—")],
            ["Open Ports", (r.open_ports    ?? (r.run_stats as Record<string, unknown>)?.open_ports    ?? "—")],
            ["Facts",      (r.fact_count    ?? (r.run_stats as Record<string, unknown>)?.fact_count    ?? "—")],
            ["Findings",   (r.finding_count ?? "0")],
          ] as [string, unknown][]).map(([label, val], i) => (
            <div key={label} style={{ padding: "16px 12px", textAlign: "center", borderRight: i < 3 ? "0.5px solid var(--border-subtle)" : "none" }}>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 24, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1 }}>{String(val)}</div>
              <div style={{ fontSize: 9.5, color: "var(--text-muted)", marginTop: 5, textTransform: "uppercase", letterSpacing: 0.8 }}>{label}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ padding: "10px 16px", display: "flex", flexWrap: "wrap", gap: 14, borderTop: "0.5px solid var(--border-subtle)" }}>
        {job.agent_name && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Probe <strong style={{ color: "var(--text-secondary)", fontWeight: 600 }}>{job.agent_name}</strong></span>}
        {job.created_at && <span style={{ fontSize: 11, color: "var(--text-muted)" }}>Queued <strong style={{ color: "var(--text-secondary)", fontWeight: 600 }}>{new Date(job.created_at).toLocaleTimeString()}</strong></span>}
        <span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-faint)", fontFamily: "var(--font-mono)" }}>{job.job_id.slice(0, 8)}</span>
      </div>

      {job.status === "failed" && r.error && (
        <div style={{ padding: "11px 16px", background: "var(--sev-critical-bg)", borderTop: "0.5px solid var(--border-subtle)", fontSize: 11.5, color: "var(--sev-critical-color)", fontFamily: "var(--font-mono)" }}>
          {String(r.error)}
        </div>
      )}
    </div>
    </HudFrame>
  );
}

/* ══════════════════════════════════════════════════════
   DISPATCH RECEIPT — prints the exact request sent to the probe
══════════════════════════════════════════════════════ */

function DispatchReceipt({ payload }: { payload: Record<string, unknown> }) {
  const [open, setOpen] = useState(true);
  const params = (payload.params ?? {}) as Record<string, unknown>;
  const line = (k: string, v: unknown) => (v === undefined || v === null || v === "" ? null : (
    <div key={k} style={{ display: "flex", gap: 10, padding: "4px 0", fontSize: 11.5, borderBottom: "0.5px solid var(--border-subtle)" }}>
      <span style={{ color: "var(--text-faint)", fontFamily: "var(--font-mono)", width: 132, flexShrink: 0, fontSize: 10.5 }}>{k}</span>
      <span style={{ color: "var(--text-secondary)", fontFamily: "var(--font-mono)", wordBreak: "break-word", flex: 1 }}>
        {Array.isArray(v) ? v.join("  ·  ") : typeof v === "object" ? JSON.stringify(v) : String(v)}
      </span>
    </div>
  ));
  return (
    <div style={{ borderRadius: 12, border: "0.5px solid var(--border-accent)", background: "var(--bg-panel)", overflow: "hidden", boxShadow: "var(--shadow-md)" }}>
      <button onClick={() => setOpen((v) => !v)} style={{ width: "100%", display: "flex", alignItems: "center", gap: 9, padding: "12px 16px", cursor: "pointer", background: "var(--accent-ghost)", border: "none", borderBottom: open ? "0.5px solid var(--border-subtle)" : "none" }}>
        <Send size={13} color="var(--accent)" />
        <span style={{ fontSize: 12.5, fontWeight: 700, color: "var(--text-primary)", fontFamily: "var(--font-display)" }}>Dispatched to Probe</span>
        <span style={{ fontSize: 10, color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>POST /agents/jobs</span>
        <ChevronDown size={14} color="var(--text-muted)" style={{ marginLeft: "auto", transform: open ? "rotate(180deg)" : "none", transition: "transform var(--dur-fast)" }} />
      </button>
      {open && (
        <div style={{ padding: "6px 16px 14px" }}>
          {line("use_case_id", payload.use_case_id)}
          {line("job_type", payload.job_type)}
          {line("engagement_id", payload.engagement_id)}
          {line("scope (targets)", params.targets ?? "→ engagement scope")}
          {line("excluded_cidrs", params.excluded_cidrs)}
          {line("intensity", params.intensity)}
          {line("rate / conc / timeout", params.rate !== undefined ? `${params.rate} pps · ${params.concurrency} · ${params.timeout}s` : undefined)}
          {line("passive_listen_seconds", params.passive_listen_seconds)}
          {line("recheck_hours", params.recheck_hours)}
          {line("ssh_creds", params.ssh_creds)}
          {line("win_creds", params.win_creds)}
          <div style={{ marginTop: 11, display: "flex", gap: 7, alignItems: "flex-start" }}>
            <ShieldAlert size={13} color="var(--accent)" style={{ flexShrink: 0, marginTop: 1 }} />
            <span style={{ fontSize: 10, color: "var(--text-muted)", lineHeight: 1.5 }}>
              The probe re-validates this against the engagement&apos;s authoritative scope and exclusions before sending a single packet. Credential values are masked here and redacted from any status echoed back.
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════
   PAGE
══════════════════════════════════════════════════════ */

export default function ScanPage() {
  const { success: toastOk, error: toastErr } = useToast();

  const [useCases,    setUseCases]    = useState<UseCase[]>([]);
  const [probes,      setProbes]      = useState<Probe[]>([]);
  const [engagements, setEngagements] = useState<Engagement[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  const [selectedUc,  setSelectedUc]  = useState("");
  const [selectedEng, setSelectedEng] = useState("");
  const [targets,     setTargets]     = useState("");
  const [excluded,    setExcluded]    = useState("");
  // The engagement's own defined scope/exclusions, joined for the textareas. We
  // pre-fill from these so the operator never re-types what the engagement already
  // declares; if they leave it untouched we send empty targets and let the backend
  // apply the engagement's authoritative scope.
  const [inheritedScope,    setInheritedScope]    = useState("");
  const [inheritedExcluded, setInheritedExcluded] = useState("");
  const [catFilter,   setCatFilter]   = useState<Cat>("All");
  const [dispatched,  setDispatched]  = useState<Record<string, unknown> | null>(null);

  // ── Scan tuning ──
  const [intensity,    setIntensity]    = useState<Intensity>("normal");
  const [passiveSecs,  setPassiveSecs]  = useState(60);
  const [recheckHours, setRecheckHours] = useState(24);
  const [showCreds,    setShowCreds]    = useState(false);
  const [sshUser, setSshUser] = useState(""); const [sshPass, setSshPass] = useState("");
  const [winUser, setWinUser] = useState(""); const [winPass, setWinPass] = useState("");
  const [winDomain, setWinDomain] = useState("");

  const [launching, setLaunching] = useState(false);
  const [job,       setJob]       = useState<JobStatus | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoadingData(true);
      try {
        const [uc, pr, engRaw] = await Promise.all([
          apiFetch<UseCase[]>("/api/scan/use-cases"),
          apiFetch<Probe[]>("/api/scan/probes"),
          apiFetch<{ engagements?: Engagement[] } | Engagement[]>("/api/engagements"),
        ]);
        if (!alive) return;
        setUseCases(uc);
        setProbes(pr);
        const engs = Array.isArray(engRaw) ? engRaw : (engRaw as { engagements?: Engagement[] }).engagements ?? [];
        setEngagements(engs);
        if (engs.length === 1) setSelectedEng(engs[0].id);
      } catch (e) {
        toastErr("Load failed", (e as Error).message);
      } finally {
        if (alive) setLoadingData(false);
      }
    })();
    return () => { alive = false; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const startPolling = useCallback((jobId: string) => {
    if (pollRef.current) clearInterval(pollRef.current);
    pollRef.current = setInterval(async () => {
      try {
        const j = await apiFetch<JobStatus>(`/api/scan/jobs/${jobId}`);
        setJob(j);
        if (j.status === "completed" || j.status === "failed") {
          clearInterval(pollRef.current!); pollRef.current = null;
          if (j.status === "completed") toastOk("Scan complete"); else toastErr("Scan failed");
        }
      } catch { /* network blip */ }
    }, 4000);
  }, [toastOk, toastErr]);

  useEffect(() => () => { if (pollRef.current) clearInterval(pollRef.current); }, []);

  // Resolve an engagement's declared scope + exclusions into textarea strings.
  const engScope = useCallback((engId: string) => {
    const eng = engagements.find((e) => e.id === engId);
    return {
      scope:    (eng?.scopeCidrs ?? []).join("\n"),
      excluded: (eng?.excludedCidrs ?? []).join("\n"),
    };
  }, [engagements]);

  // When the selected engagement changes, inherit its scope/exclusions into the
  // fields (only re-runs on engagement change, so manual edits are preserved).
  useEffect(() => {
    const { scope, excluded } = engScope(selectedEng);
    setInheritedScope(scope);
    setInheritedExcluded(excluded);
    if (selectedEng) { setTargets(scope); setExcluded(excluded); }
  }, [selectedEng, engScope]);

  const ucObj      = useCases.find((u) => u.use_case_id === selectedUc);
  const idleProbes = probes.filter((p) => p.online && !p.current_job_id);

  const isOt         = ucObj?.profile === "ot";
  const isRescan     = selectedUc === "uc_rescan_delta";
  const isAssessment = ucObj?.scan_type === "assessment";
  const credsActive  = showCreds && (sshUser.trim() !== "" || winUser.trim() !== "");
  const parseList    = (s: string) => s.split(/[\s,\n]+/).map((t) => t.trim()).filter(Boolean);
  const targetCount  = parseList(targets).length;
  const excludeCount = parseList(excluded).length;
  // True when the field still matches what the engagement declared (i.e. the
  // operator hasn't overridden it) — drives the "inherited" UI + launch payload.
  const scopeIsInherited   = inheritedScope.trim()    !== "" && targets.trim()  === inheritedScope.trim();
  const excludeIsInherited = inheritedExcluded.trim() !== "" && excluded.trim() === inheritedExcluded.trim();

  function buildLaunchBody() {
    const targetList  = parseList(targets);
    const excludeList = parseList(excluded);
    const b: Record<string, unknown> = {
      engagement_id: selectedEng, use_case_id: selectedUc,
      // Only send an explicit list when the operator narrowed it beyond what the
      // engagement declares; otherwise send nothing and let the backend apply the
      // engagement's authoritative scope/exclusions (no duplication).
      targets: (targetList.length && !scopeIsInherited) ? targetList : undefined,
      excluded_cidrs: (excludeList.length && !excludeIsInherited) ? excludeList : undefined,
    };
    if (isOt) b.passive_listen_seconds = passiveSecs; else b.intensity = intensity;
    if (isRescan) b.recheck_hours = recheckHours;
    if (isAssessment && showCreds) {
      if (sshUser.trim()) b.ssh_creds = { user: sshUser.trim(), password: sshPass || undefined };
      if (winUser.trim()) b.win_creds = { user: winUser.trim(), password: winPass || undefined, domain: winDomain.trim() || undefined };
    }
    return b;
  }

  async function launch() {
    if (!selectedUc)  { toastErr("Select a scan"); return; }
    if (!selectedEng) { toastErr("Select an engagement"); return; }
    setLaunching(true); setJob(null); setDispatched(null);
    try {
      const res = await apiFetch<{ job_id: string; status: string; dispatched?: Record<string, unknown> }>("/api/scan/launch", {
        method: "POST", body: JSON.stringify(buildLaunchBody()),
      });
      if (res.dispatched) setDispatched(res.dispatched);
      setJob({
        job_id: res.job_id, engagement_id: selectedEng, status: "pending",
        created_at: new Date().toISOString(), started_at: null, completed_at: null,
        agent_id: null, agent_name: null, use_case_id: selectedUc, result: null,
      });
      startPolling(res.job_id);
      toastOk("Job queued", "Probe picks up on next poll (~10s)");
    } catch (e) {
      toastErr("Launch failed", (e as Error).message);
    } finally {
      setLaunching(false);
    }
  }

  function reset() {
    setSelectedUc("");
    const nextEng = engagements.length === 1 ? engagements[0].id : "";
    setSelectedEng(nextEng);
    // Re-inherit the engagement's scope rather than blanking it (the effect won't
    // refire when nextEng equals the current selection, e.g. the single-engagement case).
    const { scope, excluded: excl } = nextEng ? engScope(nextEng) : { scope: "", excluded: "" };
    setTargets(scope); setExcluded(excl);
    setJob(null); setDispatched(null);
    setIntensity("normal"); setPassiveSecs(60); setRecheckHours(24);
    setShowCreds(false); setSshUser(""); setSshPass(""); setWinUser(""); setWinPass(""); setWinDomain("");
  }

  // category counts + filtered list
  const counts: Record<string, number> = { All: useCases.length };
  for (const uc of useCases) { const c = UC_META[uc.use_case_id]?.cat ?? "Other"; counts[c] = (counts[c] ?? 0) + 1; }
  const filtered = catFilter === "All" ? useCases : useCases.filter((u) => (UC_META[u.use_case_id]?.cat ?? "Other") === catFilter);

  const canLaunch = !!selectedUc && !!selectedEng && !launching;
  const intensityObj = INTENSITY.find((i) => i.id === intensity)!;

  return (
    <PageShell title="Scanner" subtitle="Compose and dispatch a scan to a field-deployed probe">
      <style>{STYLES}</style>

      <div style={{ display: "flex", flexDirection: "column", gap: 20, maxWidth: 1140 }}>

        <FleetStrip probes={probes} loading={loadingData} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 340px", gap: 20, alignItems: "start" }}>

          {/* ── STEP 1 · Choose a scan ── */}
          <section>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12, flexWrap: "wrap", gap: 8 }}>
              <SectionLabel num="01">Choose a scan</SectionLabel>
              {/* category filter pills */}
              <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
                {CATS.map((c) => {
                  const on = catFilter === c;
                  if (c !== "All" && !counts[c]) return null;
                  return (
                    <button key={c} className="scn-pill" data-on={on} onClick={() => setCatFilter(c)}>
                      {c === "All" && <Layers size={11} style={{ marginRight: 4 }} />}
                      {c}
                      <span style={{ marginLeft: 5, opacity: 0.6, fontFamily: "var(--font-mono)", fontSize: 10 }}>{counts[c] ?? 0}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {loadingData ? (
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {[0, 1, 2, 3].map((i) => <div key={i} className="scn-skeleton" style={{ height: 122 }} />)}
              </div>
            ) : (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(228px, 1fr))", gap: 10 }}>
                {filtered.map((uc, i) => (
                  <UseCaseCard key={uc.use_case_id} uc={uc} index={i} selected={selectedUc === uc.use_case_id} onClick={() => setSelectedUc(uc.use_case_id)} />
                ))}
              </div>
            )}
          </section>

          {/* ── STEP 2 · Configure & launch ── */}
          <div style={{ position: "sticky", top: 16 }}>
            <SectionLabel num="02">Configure &amp; launch</SectionLabel>

            <HudFrame active={!!ucObj} radius={14}>
            <div style={{ borderRadius: 14, border: "0.5px solid var(--border-subtle)", background: "var(--bg-panel)", boxShadow: "var(--shadow-md)", overflow: "hidden" }}>

              {/* Panel hero: selected scan */}
              {ucObj ? (
                <div style={{ padding: "15px 16px", borderBottom: "0.5px solid var(--border-subtle)", background: "linear-gradient(180deg, var(--accent-ghost), transparent)" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
                    <span className="scn-card-icon" data-sel="true" style={{ width: 36, height: 36 }}>{UC_META[ucObj.use_case_id]?.icon}</span>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: 700, fontSize: 14, color: "var(--text-primary)", fontFamily: "var(--font-display)" }}>{ucObj.display_name}</div>
                      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10.5, color: "var(--text-muted)", marginTop: 3 }}>
                        {ucObj.scan_type} · {ucObj.profile.toUpperCase()} · {ucObj.expected_runtime_hint}
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{ padding: "32px 20px", textAlign: "center" }}>
                  <Crosshair size={22} color="var(--text-faint)" style={{ marginBottom: 8 }} />
                  <div style={{ fontSize: 12.5, color: "var(--text-muted)", lineHeight: 1.5 }}>Pick a scan on the left<br />to configure the launch.</div>
                </div>
              )}

              {ucObj && (
                <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 16 }}>

                  {/* Engagement */}
                  <div>
                    <FieldLabel>Engagement</FieldLabel>
                    <div style={{ position: "relative" }}>
                      <select className="scn-input scn-select" value={selectedEng} onChange={(e) => setSelectedEng(e.target.value)}>
                        <option value="">— select engagement —</option>
                        {engagements.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
                      </select>
                      <ChevronDown size={13} color="var(--text-muted)" style={{ position: "absolute", right: 11, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }} />
                    </div>
                  </div>

                  {/* Scope / Targets — pre-filled from the selected engagement */}
                  <div>
                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8 }}>
                      <FieldLabel icon={<Crosshair size={11} />} hint={targetCount ? `${targetCount} target${targetCount > 1 ? "s" : ""}` : "engagement scope"}>Scope</FieldLabel>
                      {scopeIsInherited
                        ? <span title="Auto-filled from the engagement's defined scope" style={{ display: "inline-flex", alignItems: "center", gap: 4, fontSize: 8.5, fontWeight: 700, color: "var(--accent)", background: "var(--accent-ghost)", border: "0.5px solid var(--border-accent)", borderRadius: 4, padding: "2px 6px", letterSpacing: 0.4, marginBottom: 7 }}><Layers size={9} /> FROM ENGAGEMENT</span>
                        : (inheritedScope && (
                            <button type="button" onClick={() => setTargets(inheritedScope)} style={{ fontSize: 9.5, color: "var(--text-muted)", background: "none", border: "none", cursor: "pointer", marginBottom: 7, display: "inline-flex", alignItems: "center", gap: 4 }} title="Reset to the engagement's scope"><RotateCcw size={9} /> reset scope</button>
                          ))}
                    </div>
                    <textarea
                      className="scn-input"
                      value={targets} onChange={(e) => setTargets(e.target.value)}
                      placeholder={selectedEng ? "This engagement declares no scope — add targets\n10.0.0.0/24   ·   172.16.0.5" : "Select an engagement to inherit its scope"}
                      rows={2}
                      style={{ fontFamily: "var(--font-mono)", fontSize: 11.5, resize: "vertical", lineHeight: 1.5 }}
                    />
                    <p style={{ margin: "6px 0 0", fontSize: 10, color: "var(--text-faint)", lineHeight: 1.5 }}>
                      {scopeIsInherited
                        ? "Inherited from the engagement — edit to narrow this run to a subset."
                        : inheritedScope
                          ? "Overriding the engagement scope for this run only."
                          : "No scope defined on the engagement — targets entered here are used as-is."}
                    </p>
                  </div>

                  {/* Excluded scope */}
                  <div>
                    <FieldLabel icon={<ShieldAlert size={11} />} hint={excludeCount ? `${excludeCount} carve-out${excludeCount > 1 ? "s" : ""}` : "optional"}>Excluded Scope</FieldLabel>
                    <textarea
                      className="scn-input"
                      value={excluded} onChange={(e) => setExcluded(e.target.value)}
                      placeholder={"Carve out hosts to never touch\n10.0.0.5   ·   10.0.0.240/28"}
                      rows={2}
                      style={{ fontFamily: "var(--font-mono)", fontSize: 11.5, resize: "vertical", lineHeight: 1.5 }}
                    />
                    {excludeCount > 0 && (
                      <p style={{ margin: "6px 0 0", fontSize: 10, color: "var(--text-faint)", lineHeight: 1.5 }}>
                        Subtracted from scope — the probe never sends a packet to these, even if inside the allowed range.
                      </p>
                    )}
                  </div>

                  {/* Intensity (non-OT) */}
                  {!isOt && (
                    <div>
                      <FieldLabel icon={<Radar size={11} />}>Scan Intensity</FieldLabel>
                      <IntensityDial value={intensity} onChange={setIntensity} />
                    </div>
                  )}

                  {/* OT passive window */}
                  {isOt && (
                    <div>
                      <FieldLabel icon={<Timer size={11} />}>Passive Listen Window</FieldLabel>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <input type="number" min={5} max={3600} value={passiveSecs} className="scn-input"
                          onChange={(e) => setPassiveSecs(Math.max(5, Math.min(3600, Number(e.target.value) || 0)))}
                          style={{ width: 84, fontFamily: "var(--font-mono)", fontSize: 12 }} />
                        <span style={{ fontSize: 11, color: "var(--text-muted)" }}>sec</span>
                        <div style={{ display: "flex", gap: 5, marginLeft: "auto" }}>
                          {[30, 60, 300].map((s) => (
                            <button key={s} className="scn-chip" data-on={passiveSecs === s} onClick={() => setPassiveSecs(s)}>{s}s</button>
                          ))}
                        </div>
                      </div>
                      <div style={{ display: "flex", gap: 7, marginTop: 9, padding: "8px 10px", borderRadius: 8, background: "rgba(16,185,129,0.07)", border: "0.5px solid rgba(16,185,129,0.25)" }}>
                        <ShieldAlert size={15} color="#10b981" style={{ flexShrink: 0, marginTop: 1 }} />
                        <span style={{ fontSize: 10.5, color: "#34d399", lineHeight: 1.5 }}><strong>OT Safe Mode</strong> — zero active packets. The probe only listens. Safe for SCADA / ICS / PLC.</span>
                      </div>
                    </div>
                  )}

                  {/* Rescan delta */}
                  {isRescan && (
                    <div>
                      <FieldLabel icon={<RefreshCw size={11} />}>Re-scan Delta Window</FieldLabel>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <input type="number" min={0} max={8760} value={recheckHours} className="scn-input"
                          onChange={(e) => setRecheckHours(Math.max(0, Math.min(8760, Number(e.target.value) || 0)))}
                          style={{ width: 84, fontFamily: "var(--font-mono)", fontSize: 12 }} />
                        <span style={{ fontSize: 11, color: "var(--text-muted)" }}>hrs</span>
                        <div style={{ display: "flex", gap: 5, marginLeft: "auto" }}>
                          {[[1, "1h"], [24, "1d"], [168, "1w"]].map(([h, lbl]) => (
                            <button key={String(h)} className="scn-chip" data-on={recheckHours === h} onClick={() => setRecheckHours(h as number)}>{lbl}</button>
                          ))}
                        </div>
                      </div>
                      <p style={{ margin: "8px 0 0", fontSize: 10.5, color: "var(--text-muted)", lineHeight: 1.5 }}>Facts older than this are re-probed; fresher facts are reused. Lower = more thorough.</p>
                    </div>
                  )}

                  {/* Credentialed scan */}
                  {isAssessment && (
                    <div style={{ borderRadius: 10, border: `0.5px solid ${credsActive ? "var(--border-accent)" : "var(--border-subtle)"}`, overflow: "hidden", background: "var(--bg-card)" }}>
                      <button onClick={() => setShowCreds((v) => !v)} style={{ width: "100%", display: "flex", alignItems: "center", gap: 8, padding: "10px 12px", cursor: "pointer", background: credsActive ? "var(--accent-ghost)" : "transparent", border: "none" }}>
                        <Lock size={13} color={credsActive ? "var(--accent)" : "var(--text-muted)"} />
                        <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-primary)" }}>Authenticated scan</span>
                        {credsActive
                          ? <span style={{ fontSize: 8.5, fontWeight: 700, color: "var(--accent)", background: "var(--accent-ghost)", border: "0.5px solid var(--border-accent)", borderRadius: 4, padding: "2px 5px", letterSpacing: 0.5 }}>ACTIVE</span>
                          : <span style={{ fontSize: 10, color: "var(--text-faint)" }}>optional</span>}
                        <ChevronDown size={14} color="var(--text-muted)" style={{ marginLeft: "auto", transform: showCreds ? "rotate(180deg)" : "none", transition: "transform var(--dur-fast)" }} />
                      </button>
                      {showCreds && (
                        <div style={{ padding: "0 12px 12px", display: "flex", flexDirection: "column", gap: 11 }}>
                          <div style={{ display: "flex", gap: 7, fontSize: 10, color: "var(--text-muted)", lineHeight: 1.5, padding: "8px 10px", borderRadius: 8, background: "var(--sev-medium-bg)", border: "0.5px solid color-mix(in srgb, var(--sev-medium-color) 25%, transparent)" }}>
                            <ShieldAlert size={16} color="var(--sev-medium-color)" style={{ flexShrink: 0, marginTop: 1 }} />
                            <span>Unlocks Gate-6 collection for deeper facts. Credentials travel with the job and are redacted from any status echoed back. Use engagement-scoped accounts only.</span>
                          </div>
                          <div>
                            <div className="scn-cred-h"><KeyRound size={11} /> SSH · Linux/Unix</div>
                            <div style={{ display: "flex", gap: 6 }}>
                              <input className="scn-input scn-mono" value={sshUser} onChange={(e) => setSshUser(e.target.value)} placeholder="username" autoComplete="off" />
                              <input className="scn-input scn-mono" value={sshPass} onChange={(e) => setSshPass(e.target.value)} placeholder="password" type="password" autoComplete="new-password" />
                            </div>
                          </div>
                          <div>
                            <div className="scn-cred-h"><Server size={11} /> Windows · WinRM/SMB</div>
                            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                              <div style={{ display: "flex", gap: 6 }}>
                                <input className="scn-input scn-mono" value={winUser} onChange={(e) => setWinUser(e.target.value)} placeholder="username" autoComplete="off" />
                                <input className="scn-input scn-mono" value={winPass} onChange={(e) => setWinPass(e.target.value)} placeholder="password" type="password" autoComplete="new-password" />
                              </div>
                              <input className="scn-input scn-mono" value={winDomain} onChange={(e) => setWinDomain(e.target.value)} placeholder="domain (optional)" autoComplete="off" />
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Pre-flight summary */}
                  <div style={{ borderRadius: 10, background: "var(--bg-card)", border: "0.5px solid var(--border-subtle)", padding: "11px 13px", display: "flex", flexDirection: "column", gap: 7 }}>
                    {([
                      ["Mode", isOt ? `Passive · ${passiveSecs}s` : `${intensityObj.label} · ${intensityObj.pps}`],
                      ["Scope", scopeIsInherited ? `Engagement scope · ${targetCount}` : targetCount ? `${targetCount} explicit target${targetCount > 1 ? "s" : ""}` : "Full engagement scope"],
                      ...(excludeCount ? [["Exclude", `${excludeCount} carve-out${excludeCount > 1 ? "s" : ""}`]] as [string, string][] : []),
                      ...(isRescan ? [["Delta", `re-probe > ${recheckHours}h old`]] as [string, string][] : []),
                      ["Auth", credsActive ? [sshUser.trim() && "SSH", winUser.trim() && "Windows"].filter(Boolean).join(" + ") : "Unauthenticated"],
                    ] as [string, string][]).map(([k, v]) => (
                      <div key={k} style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 11 }}>
                        <span style={{ color: "var(--text-faint)", textTransform: "uppercase", letterSpacing: 0.6, fontSize: 9.5, fontWeight: 600, width: 48, flexShrink: 0 }}>{k}</span>
                        <span style={{ color: "var(--text-secondary)", fontWeight: 500 }}>{v}</span>
                      </div>
                    ))}
                  </div>

                  {/* Probe readiness */}
                  {probes.length > 0 && (
                    <div style={{ display: "flex", alignItems: "center", gap: 7, fontSize: 11, color: "var(--text-muted)" }}>
                      <span style={{ width: 6, height: 6, borderRadius: "50%", background: idleProbes.length ? "var(--nominal-color)" : "var(--sev-medium-color)" }} />
                      {idleProbes.length ? `${idleProbes.length} idle probe${idleProbes.length > 1 ? "s" : ""} ready` : "All probes busy — job will queue"}
                    </div>
                  )}

                  {/* Launch + reset */}
                  <div style={{ display: "flex", flexDirection: "column", gap: 9 }}>
                    <button className="scn-launch" onClick={launch} disabled={!canLaunch}>
                      {launching ? <><Loader size={15} className="scn-spin" /> Dispatching…</> : <><Play size={15} fill="currentColor" /> Launch Scan</>}
                    </button>
                    <button onClick={reset} className="scn-reset"><RotateCcw size={11} /> Reset</button>
                  </div>
                </div>
              )}
            </div>
            </HudFrame>
          </div>
        </div>

        {/* ── Active job + dispatch receipt ── */}
        {job && (
          <section>
            <SectionLabel>Active Job</SectionLabel>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {dispatched && <DispatchReceipt payload={dispatched} />}
              <JobPanel job={job} ucName={ucObj?.display_name} />
            </div>
          </section>
        )}
      </div>
    </PageShell>
  );
}

/* ══════════════════════════════════════════════════════
   STYLES
══════════════════════════════════════════════════════ */

const STYLES = `
@keyframes scn-spin { to { transform: rotate(360deg); } }
.scn-spin { animation: scn-spin 1s linear infinite; }

@keyframes scn-ping { 75%, 100% { transform: scale(2.2); opacity: 0; } }
.scn-ping { animation: scn-ping 1.8s cubic-bezier(0,0,0.2,1) infinite; }

@keyframes scn-shimmer { 100% { transform: translateX(100%); } }
.scn-skeleton { border-radius: 12px; background: var(--bg-card); border: 0.5px solid var(--border-subtle); position: relative; overflow: hidden; }
.scn-skeleton::after { content:""; position:absolute; inset:0; transform: translateX(-100%); background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent); animation: scn-shimmer 1.4s infinite; }

/* Use-case card */
@keyframes scn-card-in { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
.scn-card { text-align:left; cursor:pointer; padding:14px; border-radius:12px; background:var(--bg-card); border:0.5px solid var(--border-subtle); width:100%; display:flex; flex-direction:column; animation: scn-card-in 420ms var(--ease-out) both; transition: transform var(--dur-fast) var(--ease-out), border-color var(--dur-fast), background var(--dur-fast), box-shadow var(--dur-fast); }
.scn-card:hover { transform: translateY(-2px); border-color: var(--border-strong); background: var(--bg-surface); box-shadow: var(--shadow-md); }
.scn-card[data-sel="true"] { border-color: var(--accent); background: var(--accent-ghost); box-shadow: 0 0 0 1px var(--accent), 0 0 28px var(--accent-glow); }
.scn-card-icon { width:32px; height:32px; border-radius:9px; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:var(--bg-surface); border:0.5px solid var(--border-subtle); color:var(--text-secondary); transition: all var(--dur-fast); }
.scn-card-icon[data-sel="true"] { background:var(--accent-ghost); border-color:var(--border-accent); color:var(--accent); }
.scn-card:hover .scn-card-icon { color: var(--text-primary); }

/* Category pills */
.scn-pill { display:inline-flex; align-items:center; padding:5px 11px; border-radius:8px; font-size:11.5px; font-weight:600; cursor:pointer; background:var(--bg-surface); border:0.5px solid var(--border-subtle); color:var(--text-muted); transition: all var(--dur-fast); }
.scn-pill:hover { color:var(--text-secondary); border-color:var(--border-strong); }
.scn-pill[data-on="true"] { background:var(--accent-ghost); border-color:var(--accent); color:var(--accent); }

/* Inputs */
.scn-input { width:100%; padding:9px 11px; border-radius:9px; background:var(--bg-surface); border:0.5px solid var(--border-subtle); color:var(--text-primary); font-size:12.5px; font-family:var(--font-body); outline:none; box-sizing:border-box; transition: border-color var(--dur-fast), box-shadow var(--dur-fast), background var(--dur-fast); }
.scn-input::placeholder { color:var(--text-faint); }
.scn-input:focus { border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-ghost); background:var(--bg-card); }
.scn-mono { font-family:var(--font-mono); font-size:11.5px; }
.scn-select { appearance:none; -webkit-appearance:none; cursor:pointer; padding-right:30px; }

/* Intensity radar dial */
.scn-dial-wrap { position:relative; width:100%; max-width:220px; margin:0 auto; height:118px; }
.scn-dial-svg { width:100%; height:100%; overflow:visible; }
.scn-dial-sweep { position:absolute; inset:0; border-radius:50% 50% 0 0 / 100% 100% 0 0; animation: scn-dial-spin linear infinite; transform-origin:50% 100%; pointer-events:none; }
@keyframes scn-dial-spin { to { transform: rotate(360deg); } }
.scn-dial-readout { position:absolute; left:50%; bottom:6px; transform:translateX(-50%); display:flex; flex-direction:column; align-items:center; }
.scn-dial-seg { display:flex; gap:6px; margin-top:10px; }
.scn-dial-seg button { flex:1; display:flex; align-items:center; justify-content:center; gap:6px; padding:8px 4px; border-radius:9px; cursor:pointer; background:var(--bg-card); border:0.5px solid var(--border-subtle); color:var(--text-muted); font-size:11px; font-weight:600; transition: all var(--dur-fast); }
.scn-dial-seg button:hover { color:var(--text-secondary); }
.scn-dial-seg button[data-on="true"] { color:var(--seg-c); background:color-mix(in srgb, var(--seg-c) 14%, transparent); border-color:color-mix(in srgb, var(--seg-c) 45%, transparent); }

/* Chips */
.scn-chip { padding:4px 9px; border-radius:6px; font-size:10px; font-weight:600; cursor:pointer; background:var(--bg-surface); border:0.5px solid var(--border-subtle); color:var(--text-muted); transition: all var(--dur-fast); }
.scn-chip:hover { color:var(--text-secondary); }
.scn-chip[data-on="true"] { background:var(--accent-ghost); border-color:var(--accent); color:var(--accent); }

/* Cred section header */
.scn-cred-h { font-size:9.5px; font-weight:700; color:var(--text-faint); text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px; display:flex; align-items:center; gap:5px; }

/* Launch button */
.scn-launch { width:100%; padding:13px 0; border-radius:11px; border:none; font-weight:700; font-size:14px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; color:#fff; background:linear-gradient(180deg, var(--accent-hover), var(--accent)); box-shadow:0 4px 20px var(--accent-glow), inset 0 1px 0 rgba(255,255,255,0.15); transition: transform var(--dur-fast), box-shadow var(--dur-fast), filter var(--dur-fast); }
.scn-launch:hover:not(:disabled) { transform:translateY(-1px); box-shadow:0 6px 28px var(--accent-glow), inset 0 1px 0 rgba(255,255,255,0.2); filter:brightness(1.05); }
.scn-launch:active:not(:disabled) { transform:translateY(0); }
.scn-launch:disabled { background:var(--bg-surface); color:var(--text-faint); box-shadow:none; cursor:not-allowed; }

.scn-reset { background:none; border:none; cursor:pointer; font-size:11px; color:var(--text-faint); display:flex; align-items:center; justify-content:center; gap:5px; padding:2px; transition:color var(--dur-fast); }
.scn-reset:hover { color:var(--text-secondary); }

/* HUD corner brackets — the page's recurring "locked on" signature */
.scn-hud { position:absolute; width:16px; height:16px; pointer-events:none; opacity:0; transition: opacity 320ms var(--ease-out); z-index:2; }
.scn-hud[data-active="true"] { opacity:1; }
.scn-hud-tl { top:-1px; left:-1px; border-top:2px solid var(--accent); border-left:2px solid var(--accent); border-top-left-radius:6px; }
.scn-hud-tr { top:-1px; right:-1px; border-top:2px solid var(--accent); border-right:2px solid var(--accent); border-top-right-radius:6px; }
.scn-hud-bl { bottom:-1px; left:-1px; border-bottom:2px solid var(--accent); border-left:2px solid var(--accent); border-bottom-left-radius:6px; }
.scn-hud-br { bottom:-1px; right:-1px; border-bottom:2px solid var(--accent); border-right:2px solid var(--accent); border-bottom-right-radius:6px; }

/* Job phase ticker */
.scn-ticker { display:flex; align-items:center; padding:16px; overflow-x:auto; }
.scn-phase { display:flex; flex-direction:column; align-items:center; gap:6px; flex-shrink:0; width:84px; }
.scn-phase-dot { width:9px; height:9px; border-radius:50%; background:var(--bg-surface); border:2px solid var(--border-strong); transition: all var(--dur-fast); }
.scn-phase[data-state="active"] .scn-phase-dot { background:var(--accent); border-color:var(--accent); box-shadow:0 0 8px var(--accent-glow); animation:scn-pulse-dot 1.4s ease-in-out infinite; }
.scn-phase[data-state="done"] .scn-phase-dot { background:var(--nominal-color); border-color:var(--nominal-color); }
@keyframes scn-pulse-dot { 50% { transform:scale(1.3); } }
.scn-phase-label { font-size:9.5px; color:var(--text-faint); text-transform:uppercase; letter-spacing:0.5px; text-align:center; }
.scn-phase[data-state="active"] .scn-phase-label { color:var(--accent); font-weight:600; }
.scn-phase[data-state="done"] .scn-phase-label { color:var(--text-muted); }
.scn-phase-link { flex:1; height:2px; background:var(--border-subtle); margin:0 -2px 18px; min-width:14px; transition: background 400ms var(--ease-out); }
.scn-phase-link[data-on="true"] { background:var(--nominal-color); }

@media (prefers-reduced-motion: reduce) {
  .scn-card, .scn-dial-sweep, .scn-ping, .scn-phase[data-state="active"] .scn-phase-dot { animation: none !important; }
}
`;
