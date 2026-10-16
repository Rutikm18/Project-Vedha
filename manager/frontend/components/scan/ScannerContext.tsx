"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { Activity, CheckCircle2, ChevronRight, Clock, Layers, Radar, Target } from "lucide-react";

export function ScannerFrame({ active, children }: { active: boolean; children: ReactNode }) {
  return <div className="scanner-frame" data-active={active}>
    {children}
    {['tl', 'tr', 'bl', 'br'].map(corner => <span key={corner} className={`scanner-corner scanner-corner-${corner}`} aria-hidden="true" />)}
  </div>;
}

export function ScannerFleetStrip({ probes, loading, href }: {
  probes: Array<{ id: string; name: string; online: boolean; current_job_id: string | null; capabilities: string[]; location: string | null }>;
  loading: boolean; href: string;
}) {
  const online = probes.filter(probe => probe.online);
  const scanning = online.filter(probe => probe.current_job_id).length;
  return <section className="scanner-fleet" aria-label="vedha-agent fleet">
    <div className="scanner-fleet-summary">
      <span className="scanner-fleet-title"><i data-online={online.length > 0} aria-hidden="true" />vedha-agent Fleet</span>
      {loading ? <span>Loading…</span> : !probes.length ? <span>No vedha-agents registered — deploy one to begin</span> :
        <dl><div data-state="online"><dt>Online</dt><dd>{online.length}</dd></div><div><dt>Idle</dt><dd>{online.length - scanning}</dd></div><div data-state="scanning"><dt>Scanning</dt><dd>{scanning}</dd></div></dl>}
      <Link href={href}>View fleet <ChevronRight size={13} aria-hidden="true" /></Link>
    </div>
    {!loading && probes.length > 0 && <ul className="scanner-fleet-probes" aria-label="Agent availability">
      {probes.map(probe => {
        const state = !probe.online ? 'offline' : probe.current_job_id ? 'scanning' : 'online';
        return <li key={probe.id} data-state={state} title={[probe.location, probe.capabilities.length ? `Capabilities: ${probe.capabilities.join(', ')}` : null].filter(Boolean).join(' · ')}>
          <i aria-hidden="true" /><span className="scanner-agent-name">{probe.name}</span><span className="scanner-agent-status">{state}</span>
          <span className="scanner-agent-capabilities" aria-label={`${probe.capabilities.length} capabilities`}><Layers size={11} aria-hidden="true" />{probe.capabilities.length}</span>
        </li>;
      })}
    </ul>}
  </section>;
}

const stages = ['Discovery', 'Port map', 'Assessment', 'Exposure', 'Inventory', 'Detection'];

export function NetworkVaHero({ workflow, selected, loading, disabled, onConfigure, campaignHref }: {
  workflow?: { display_name: string; description: string; profile: string; expected_runtime_hint: string };
  selected: boolean; loading: boolean; disabled?: boolean; onConfigure: () => void; campaignHref: string;
}) {
  return <ScannerFrame active={selected && !!workflow && !loading}>
    <section className="scanner-network-va" data-selected={selected && !!workflow && !loading} aria-labelledby="scanner-network-va-title">
      <span className="scanner-workflow-glow" aria-hidden="true" />
      <header><span className="scanner-workflow-icon"><Radar size={26} aria-hidden="true" /></span>
        <div><div className="scanner-workflow-meta"><span>Flagship campaign</span>{workflow && <small>{workflow.profile.toUpperCase()}</small>}</div>
          <h2 id="scanner-network-va-title">{workflow?.display_name ?? 'Network Vulnerability Assessment'}</h2>
          <p>{workflow?.description ?? 'The Network Vulnerability Assessment workflow is unavailable.'}</p></div>
      </header>
      <ol className="scanner-workflow-stages" aria-label="Campaign stages, in order">
        {stages.map((stage, index) => <li key={stage}>{index > 0 && <ChevronRight size={12} aria-hidden="true" />}<span>{stage}</span></li>)}
      </ol>
      <div className="scanner-workflow-actions">
        {loading ? <span>Loading workflow…</span> : !workflow ? <span>Workflow unavailable</span>
          : selected ? <span className="scanner-workflow-selected"><CheckCircle2 size={15} aria-hidden="true" />Selected campaign</span>
          : <button type="button" className="btn btn-primary" disabled={disabled} onClick={onConfigure}><Target size={15} aria-hidden="true" />Configure campaign</button>}
        <Link href={campaignHref}><Activity size={14} aria-hidden="true" />View live campaigns</Link>
        {!loading && workflow?.expected_runtime_hint && <span className="scanner-workflow-runtime"><Clock size={12} aria-hidden="true" />{workflow.expected_runtime_hint}</span>}
      </div>
    </section>
  </ScannerFrame>;
}
