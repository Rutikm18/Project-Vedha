"use client";

import Link from "next/link";
import { Activity, ArrowRight, CheckCircle2, Radar } from "lucide-react";

export function ScannerFleetStrip({ probes, loading, href }: {
  probes: Array<{ id: string; name: string; online: boolean; current_job_id: string | null }>;
  loading: boolean; href: string;
}) {
  const online = probes.filter(probe => probe.online);
  const scanning = online.filter(probe => probe.current_job_id).length;
  return <section className="scanner-fleet" aria-label="vedha-agent fleet">
    <span className="scanner-fleet-title"><Activity size={15} aria-hidden="true" /> vedha-agent fleet</span>
    {loading ? <span>Checking agents…</span> : !probes.length ? <span>No agents registered. Connect a vedha-agent to begin.</span> : <>
      <dl><div><dt>Online</dt><dd>{online.length}</dd></div><div><dt>Idle</dt><dd>{online.length - scanning}</dd></div><div><dt>Scanning</dt><dd>{scanning}</dd></div></dl>
      <span className="scanner-fleet-names">{online.slice(0, 2).map(probe => <span key={probe.id}><i aria-hidden="true" />{probe.name}</span>)}</span>
    </>}
    <Link href={href}>View fleet <ArrowRight size={13} aria-hidden="true" /></Link>
  </section>;
}

const stages = ["Discovery", "Port map", "Assessment", "Exposure", "Inventory", "Detection"];

/** The existing Network VA entry, kept separate from live job progress. */
export function NetworkVaHero({ selected, available, loading, disabled, onConfigure, campaignHref }: {
  selected: boolean; available: boolean; loading: boolean; disabled?: boolean; onConfigure: () => void; campaignHref: string;
}) {
  return <section className="scanner-network-va" aria-labelledby="scanner-network-va-title">
    <header><span className="scanner-workflow-icon"><Radar size={23} aria-hidden="true" /></span>
      <div><h2 id="scanner-network-va-title">Network Vulnerability Assessment</h2>
        <p>Discover assets, assess exposed services, and prioritize findings in one workflow.</p></div>
      <Link href={campaignHref}>View live campaigns <ArrowRight size={13} aria-hidden="true" /></Link>
    </header>
    <div className="scanner-workflow-footer"><ol aria-label="Network VA workflow stages">
      {stages.map(stage => <li key={stage}>{stage}</li>)}
    </ol>
      {loading ? <span>Loading workflow…</span> : !available ? <span>Workflow unavailable</span>
        : selected ? <span className="scanner-workflow-selected"><CheckCircle2 size={14} aria-hidden="true" /> Selected workflow</span>
        : <button type="button" className="scanner-text-action" disabled={disabled} onClick={onConfigure}>Use network assessment</button>}
    </div>
  </section>;
}
