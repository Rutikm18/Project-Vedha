"use client";
import React from "react";
import {
  AlertTriangle, Building2, CheckCircle2, ExternalLink, Gauge,
  ShieldCheck, Wrench,
} from "lucide-react";
import type { FactCardVM } from "../../lib/assistant";
import { SEV_COLOR } from "../../lib/severity";

function Pip({ label, on, color }: { label: string; on: boolean; color: string }) {
  if (!on) return null;
  return <span className="badge" style={{ color, background: `${color}15`, border: `1px solid ${color}30` }}>{label}</span>;
}

export function FactCard({ vm, compact = false }: { vm: FactCardVM; compact?: boolean }) {
  const sev = (SEV_COLOR as Record<string, string>)[vm.severity] ?? "var(--text-muted)";
  return (
    <article className="assistant-brief" data-source={vm.source} data-compact={compact}>
      <header>
        <div>
          <span className="assistant-brief-kicker">{vm.sourceLabel}</span>
          <h3>{vm.cveIds.length ? vm.cveIds.join(" · ") : vm.title}</h3>
          {vm.cveIds.length > 0 && vm.title !== vm.cveIds[0] && <p>{vm.title}</p>}
        </div>
        <div className="assistant-brief-badges">
          <span className="badge" style={{ color: sev, background: `${sev}15`, border: `1px solid ${sev}30` }}>{vm.severity}</span>
          <Pip label="CISA KEV" on={vm.kev} color="var(--sev-critical-color)" />
          <Pip label="EXPLOIT VALIDATED" on={vm.exploited} color="var(--sev-critical-color)" />
        </div>
      </header>

      <div className="assistant-brief-scope" data-grounded={vm.source === "finding"}>
        {vm.source === "finding" ? <ShieldCheck size={14} /> : <AlertTriangle size={14} />}
        <span>{vm.evidenceStatus}</span>
      </div>

      <div className="assistant-brief-section">
        <span><ShieldCheck size={15} /></span>
        <div><h4>What is the vulnerability?</h4><p>{vm.whatItIs}</p></div>
      </div>
      <div className="assistant-brief-section">
        <span><Building2 size={15} /></span>
        <div>
          <h4>How could it impact the organization?</h4>
          <p>{vm.whyItMatters}</p>
          <small>{vm.affectedAssets.length ? `Recorded assets: ${vm.affectedAssets.join(", ")}` : "Affected organizational assets: not validated"}</small>
        </div>
      </div>
      <div className="assistant-brief-section">
        <span><Gauge size={15} /></span>
        <div>
          <h4>Severity and score</h4>
          <div className="assistant-score-grid">
            <span><small>Severity</small><strong style={{ color: sev }}>{vm.severity}</strong></span>
            <span><small>CVSS</small><strong>{vm.cvss}</strong></span>
            {vm.source === "finding" && <span><small>Vedha risk</small><strong>{vm.risk}/1000</strong></span>}
            {vm.source === "finding" && <span><small>EPSS</small><strong>{vm.epssPct}%</strong></span>}
          </div>
        </div>
      </div>
      <div className="assistant-brief-section">
        <span><Wrench size={15} /></span>
        <div>
          <h4>Remediation plan</h4>
          {vm.remediationSteps.length ? (
            <ol>{vm.remediationSteps.map((step) => <li key={step}>{step}</li>)}</ol>
          ) : <p>{vm.whatToDo}</p>}
        </div>
      </div>

      <footer>
        <div><CheckCircle2 size={13} /><span>Status: {vm.status.replaceAll("_", " ")}</span></div>
        {vm.references.slice(0, compact ? 1 : 4).map((reference) => (
          <a href={reference.url} target="_blank" rel="noreferrer" key={reference.url}>
            {reference.label}<ExternalLink size={11} />
          </a>
        ))}
      </footer>
    </article>
  );
}
