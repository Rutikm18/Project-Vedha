"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Settings2, Building2, Palette, SlidersHorizontal, Bell, CheckCircle2,
  Server, LockKeyhole, Sun, Moon, User, LogOut,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { useTheme } from "../../../components/ThemeProvider";
import { portalApi, usePortalEngagement, type PortalEngagement } from "../../../lib/portal-client";

const SLA_POLICY = [
  { severity: "Critical", window: "24 hours", escalation: "12 hours remaining", color: "var(--sev-critical-color)", intent: "Immediate owner assignment and executive visibility" },
  { severity: "High", window: "72 hours", escalation: "24 hours remaining", color: "var(--sev-high-color)", intent: "Prioritised remediation in the active cycle" },
  { severity: "Medium", window: "7 days", escalation: "48 hours remaining", color: "var(--sev-medium-color)", intent: "Planned remediation with risk acceptance if deferred" },
  { severity: "Low", window: "30 days", escalation: "7 days remaining", color: "var(--sev-low-color)", intent: "Routine hardening and hygiene backlog" },
];

function SectionTitle({ icon: Icon, title, detail, badge }: {
  icon: React.ElementType; title: string; detail: string; badge?: string;
}) {
  return (
    <header className="settings-content-heading">
      <span><Icon size={18} /></span>
      <div><h2>{title}</h2><p>{detail}</p></div>
      {badge && <span className="badge badge-info">{badge}</span>}
    </header>
  );
}

function EngagementSection({ eng }: { eng?: PortalEngagement }) {
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Building2} title="Engagement & scope"
        detail="Your active engagement and the network scope your security team authorised." />
      <div className="settings-security-notice">
        <LockKeyhole size={15} />
        <div><strong>Read-only</strong><span>Scope and engagement settings are managed by your security team. Contact them to change authorised targets.</span></div>
      </div>
      <div className="settings-workspace-card">
        <span><Building2 size={20} /></span>
        <div><strong>{eng?.name ?? "Loading…"}</strong><p>{eng ? `${eng.scope_cidr_count} authorised range${eng.scope_cidr_count === 1 ? "" : "s"}` : "…"}</p></div>
        <span className={`badge ${eng?.has_assigned_agent ? "badge-success" : "badge-high"}`}>{eng?.has_assigned_agent ? "vedha-agent assigned" : "No vedha-agent"}</span>
      </div>
      <div className="settings-readiness-grid">
        <article data-ready={Boolean(eng)}><Building2 size={16} /><div><small>Engagement</small><strong>{eng?.name ?? "…"}</strong></div></article>
        <article data-ready={eng?.status === "active"}><CheckCircle2 size={16} /><div><small>Status</small><strong style={{ textTransform: "capitalize" }}>{eng?.status ?? "…"}</strong></div></article>
        <article data-ready={eng?.has_assigned_agent ?? false}><Server size={16} /><div><small>vedha-agent</small><strong>{eng?.has_assigned_agent ? "Assigned" : "Pending"}</strong></div></article>
      </div>
      {eng && eng.scope_cidrs.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <div className="settings-field-label">Authorised scope</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {eng.scope_cidrs.map((c) => (
              <span key={c} className="chip num-mono" style={{ color: "var(--text-secondary)", border: "var(--hairline) solid var(--border-default)" }}>{c}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function AppearanceSection() {
  const { theme, toggleTheme } = useTheme();
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Palette} title="Appearance" detail="Choose how the portal looks. Saved on this device." />
      <div className="settings-workspace-card">
        <span>{theme === "dark" ? <Moon size={20} /> : <Sun size={20} />}</span>
        <div><strong>Theme</strong><p>Currently {theme === "dark" ? "dark" : "light"} mode.</p></div>
        <button onClick={toggleTheme} className="btn btn-secondary">
          {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
          Switch to {theme === "dark" ? "light" : "dark"}
        </button>
      </div>
    </div>
  );
}

function SlaSection() {
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={SlidersHorizontal} title="SLA policy" detail="Remediation windows your findings are measured against." badge="Reference" />
      <div className="settings-sla-list">
        {SLA_POLICY.map((row) => (
          <article key={row.severity} style={{ "--severity": row.color } as React.CSSProperties}>
            <span /><div><strong>{row.severity}</strong><p>{row.intent}</p></div>
            <dl><div><dt>Remediation window</dt><dd>{row.window}</dd></div><div><dt>Escalate at</dt><dd>{row.escalation}</dd></div></dl>
          </article>
        ))}
      </div>
      <div className="settings-decision-note"><SlidersHorizontal size={16} /><div><strong>Set by policy</strong><p>These windows are defined by your security team&apos;s remediation policy and drive the SLA status shown on your dashboard.</p></div></div>
    </div>
  );
}

function AccountSection() {
  const rules = [
    ["Critical finding opened", "Immediate", true],
    ["High finding opened", "Near real-time", true],
    ["Scan request approved", "Immediate", true],
    ["Report published", "Immediate", true],
    ["Weekly summary", "Digest", false],
  ] as const;
  const logout = async () => {
    await fetch("/api/portal/logout", { method: "POST" }).catch(() => {});
    window.location.href = "/portal/login";
  };
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Bell} title="Notifications & account" detail="When your team notifies you, and your portal session." badge="Read only" />
      <div className="settings-notification-list">
        {rules.map(([event, cadence, enabled]) => (
          <article key={event}>
            <span className="settings-rule-icon" data-enabled={enabled}>{enabled ? <CheckCircle2 size={15} /> : <Bell size={15} />}</span>
            <div><strong>{event}</strong><small>{cadence}</small></div>
            <span className={`badge ${enabled ? "badge-success" : "badge-info"}`}>{enabled ? "On" : "Off"}</span>
          </article>
        ))}
      </div>
      <div className="settings-decision-note">
        <Bell size={16} />
        <div><strong>Managed by your security team</strong><p>Notification routing is configured by your security team. Contact them to change what you receive.</p></div>
      </div>
      <div className="settings-workspace-card" style={{ marginTop: 14 }}>
        <span><User size={20} /></span>
        <div><strong>Portal session</strong><p>You are signed in to the customer portal.</p></div>
        <button onClick={logout} className="btn btn-danger"><LogOut size={14} /> Sign out</button>
      </div>
    </div>
  );
}

export default function PortalSettings() {
  const [section, setSection] = useState("engagement");
  const eng = usePortalEngagement();

  const sections = [
    { key: "engagement", label: "Engagement & scope", icon: Building2 },
    { key: "appearance", label: "Appearance", icon: Palette },
    { key: "sla", label: "SLA policy", icon: SlidersHorizontal },
    { key: "account", label: "Notifications & account", icon: Bell },
  ];

  return (
    <PortalShell title="Settings" subtitle="Preferences & engagement reference">
      <div className="settings-layout">
        <aside className="settings-nav">
          <div className="settings-nav-heading"><Settings2 size={14} /> Preferences</div>
          {sections.map(({ key, label, icon: Icon }) => (
            <button key={key} className="settings-nav-button" data-active={section === key} onClick={() => setSection(key)}>
              <Icon size={14} /><span>{label}</span>
            </button>
          ))}
        </aside>

        <div>
          {section === "engagement" && <EngagementSection eng={eng.data} />}
          {section === "appearance" && <AppearanceSection />}
          {section === "sla" && <SlaSection />}
          {section === "account" && <AccountSection />}
        </div>
      </div>
    </PortalShell>
  );
}
