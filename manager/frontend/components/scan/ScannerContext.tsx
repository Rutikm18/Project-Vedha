"use client";

import Link from "next/link";
import { useEffect, useRef } from "react";
import { Activity, ArrowRight, CheckCircle2, ChevronRight, Fingerprint, Layers, Network, Radar, ShieldCheck, Workflow } from "lucide-react";

export function ScannerFleetStrip({ probes, loading, href }: {
  probes: Array<{ id: string; name: string; online: boolean; current_job_id: string | null }>;
  loading: boolean; href: string;
}) {
  const online = probes.filter(probe => probe.online);
  const scanning = online.filter(probe => probe.current_job_id).length;
  return <section className="scanner-fleet" aria-label="vedha-agent fleet">
    <span className="scanner-fleet-title"><Activity size={15} aria-hidden="true" /> vedha-agent fleet</span>
    {loading ? <span>Checking agents…</span> : !probes.length ? <span>No agents registered. Connect a vedha-agent to begin.</span> : <>
      <dl><div data-state={online.length ? "online" : undefined}><dt>Online</dt><dd>{online.length}</dd></div><div><dt>Idle</dt><dd>{online.length - scanning}</dd></div><div data-state={scanning ? "scanning" : undefined}><dt>Scanning</dt><dd>{scanning}</dd></div></dl>
      <span className="scanner-fleet-names">{online.slice(0, 2).map(probe => <span key={probe.id}><i aria-hidden="true" />{probe.name}</span>)}</span>
    </>}
    <Link href={href}>View fleet <ArrowRight size={13} aria-hidden="true" /></Link>
  </section>;
}

const stages = [
  { label: "Discovery", Icon: Radar }, { label: "Port map", Icon: Network },
  { label: "Assessment", Icon: ShieldCheck }, { label: "Exposure", Icon: Workflow },
  { label: "Inventory", Icon: Layers }, { label: "Detection", Icon: Fingerprint },
];

/** The existing Network VA entry, kept separate from live job progress. */
export function NetworkVaHero({ selected, available, loading, disabled, onConfigure, campaignHref }: {
  selected: boolean; available: boolean; loading: boolean; disabled?: boolean; onConfigure: () => void; campaignHref: string;
}) {
  const intro = useRef<HTMLElement>(null);
  useEffect(() => {
    const element = intro.current;
    if (!element || window.matchMedia("(prefers-reduced-motion: reduce)").matches || !element.animate) return;
    // Inspired by React Bits Animated Content; implemented with native WAAPI and Vedha tokens.
    // Content stays visible before hydration, and the reveal never delays interaction.
    const tokens = getComputedStyle(element);
    const animation = element.animate([{ opacity: 0.85 }, { opacity: 1 }], {
      duration: parseFloat(tokens.getPropertyValue("--dur-fast")) || 180,
      easing: tokens.getPropertyValue("--ease-out").trim(),
    });
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const stop = () => { if (reduceMotion.matches) animation.cancel(); };
    reduceMotion.addEventListener("change", stop);
    return () => { animation.cancel(); reduceMotion.removeEventListener("change", stop); };
  }, []);
  return <section ref={intro} className="scanner-network-va" aria-labelledby="scanner-network-va-title">
    <header><span className="scanner-workflow-icon"><Radar size={23} aria-hidden="true" /></span>
      <div><h2 id="scanner-network-va-title">Network Vulnerability Assessment</h2>
        <p>Discover assets, assess exposed services, and prioritize findings in one workflow.</p></div>
      <Link href={campaignHref}>View live campaigns <ArrowRight size={13} aria-hidden="true" /></Link>
    </header>
    <div className="scanner-workflow-footer"><ol aria-label="Network VA workflow stages">
      {stages.map(({ label, Icon }) => <li key={label}><Icon size={14} aria-hidden="true" /><span>{label}</span><ChevronRight className="scanner-stage-connector" size={12} aria-hidden="true" /></li>)}
    </ol>
      {loading ? <span>Loading workflow…</span> : !available ? <span>Workflow unavailable</span>
        : selected ? <span className="scanner-workflow-selected"><CheckCircle2 size={14} aria-hidden="true" /> Selected workflow</span>
        : <button type="button" className="scanner-text-action" disabled={disabled} onClick={onConfigure}>Use network assessment</button>}
    </div>
  </section>;
}
