"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import { ArrowDown, ArrowUpRight, Check, Database, Globe2, Search, ShieldAlert, Target } from "lucide-react";
import type { FindingAssessment } from "../../lib/attack-assessments";

const GROUPS = [
  ["entry_context", "service_reachable_from_declared_entry"],
  ["finding_asset_binding", "finding_service_binding", "observed_service_instance", "source_evidence_budget", "reviewed_rule_applicability"],
  ["unauthenticated_datastore_data_read_supported", "observation_validity"],
];

export function FindingChainExplorer({ finding, engagementId, stacked = false, compact = false }: { finding: FindingAssessment; engagementId: string; stacked?: boolean; compact?: boolean }) {
  const [step, setStep] = useState(1);
  const [conditionKey, setConditionKey] = useState<string | null>(null);
  const inspectorRef = useRef<HTMLElement>(null);
  const canvasRef = useRef<HTMLDivElement>(null);
  const gatesRef = useRef<HTMLElement>(null);
  const condition = finding.prerequisites.find((p) => p.key === conditionKey);
  const conditions = finding.prerequisites.filter((p) => GROUPS[step].includes(p.key));
  const titles = ["Entry context", "Enabling finding", "Potential consequence"];
  const findingUrl = `/findings?engagement=${encodeURIComponent(engagementId)}&finding=${encodeURIComponent(finding.finding_id)}`;
  const missing = finding.prerequisites.filter((p) => p.state === "missing");
  const showStep = (index: number) => { setStep(index); setConditionKey(null); };
  const revealInspector = () => {
    if (compact ? (inspectorRef.current?.closest(".environment-finding-workbench")?.clientWidth ?? 0)<1080 : stacked || window.matchMedia("(max-width: 1150px)").matches) inspectorRef.current?.scrollIntoView({ block: "start", behavior: "instant" });
  };

  const candidateCanvas = <div className="chain-canvas" ref={canvasRef} aria-label="Candidate chain; required evidence is missing">
        <ol className="chain-steps" aria-label="Candidate chain steps">
          {titles.map((title, index) => {
            const Icon = index === 0 ? Globe2 : index === 1 ? Database : Target;
            return <li key={title}>
              {index > 0 && <div className="chain-connector"><ArrowDown size={18} aria-hidden="true" /><span>{index === 1 ? "Reachability not established" : "Access not established"}</span></div>}
              <button type="button" className="chain-node" data-kind={index === 1 ? "finding" : "context"} aria-pressed={step === index && !condition} aria-label={`Inspect ${title}`} onClick={() => { showStep(index); revealInspector(); }} onKeyDown={(event) => {
                const next = ["ArrowDown", "ArrowRight"].includes(event.key) ? (index + 1) % 3 : ["ArrowUp", "ArrowLeft"].includes(event.key) ? (index + 2) % 3 : event.key === "Home" ? 0 : event.key === "End" ? 2 : -1;
                if (next < 0) return;
                event.preventDefault(); showStep(next);
                event.currentTarget.closest("ol")?.querySelectorAll<HTMLButtonElement>(".chain-node")[next]?.focus();
              }}>
                <span className="chain-node-icon"><Icon size={20} aria-hidden="true" /></span>
                <span className="chain-node-copy"><span className="chain-node-role">{title}</span><strong>{index === 0 ? "Where would access begin?" : index === 1 ? finding.asset_label : finding.rule_applicability === "candidate" ? "Application data read" : "Outcome not evaluated"}</strong><span>{index === 0 ? "Entry location and permissions needed" : index === 1 ? finding.service_endpoint ?? "Identify the affected service" : "Consequence remains unconfirmed"}</span></span>
                {index === 1 && <span className="chain-severity" data-severity={finding.severity}>{finding.severity}</span>}
              </button>
              {index === 1 && <Link className="chain-finding-link" href={findingUrl}><ShieldAlert size={15} aria-hidden="true" /><span>{finding.title}</span><ArrowUpRight size={14} aria-hidden="true" /></Link>}
            </li>;
          })}
        </ol>
        <p className="chain-verdict">{finding.goal_state === "not_evaluated" ? "Not evaluated: no reviewed rule has been mapped." : "Incomplete: required evidence is missing."} No supported transition is established.</p>
      </div>;

  return <article className="finding-investigation" data-compact={compact} id="attack-assessment-proof" aria-label="Selected finding assessment">
    <div className="chain-main">
      <header className="chain-title"><div><h3>{finding.title}</h3><p>{finding.asset_label}{finding.service_endpoint ? ` · ${finding.service_endpoint}` : " · Service endpoint not recorded"}</p></div><span className="chain-status"><Search size={14} aria-hidden="true" />{finding.rule_applicability === "unmapped" ? "Rule not mapped" : "Evidence needed"}</span></header>
      {compact&&<div className="chain-review-action"><h4>Next action</h4><p>{finding.next_action}</p><span>{missing.length} required {missing.length===1?"condition needs":"conditions need"} evidence</span></div>}
      {!compact&&candidateCanvas}
      <section className="chain-gates" ref={gatesRef} aria-label="All required conditions">
        <header><h4>All required conditions</h4><span>{missing.length} {missing.length === 1 ? "gap" : "gaps"}</span></header>
        <p>Each condition must be established before this candidate can support a consequence.</p>
        <div className="chain-gate-list">{finding.prerequisites.map((p) => <button type="button" key={p.key} aria-pressed={conditionKey === p.key} onClick={() => { setConditionKey(p.key); revealInspector(); }} data-state={p.state}>
          {p.state === "supported" ? <Check size={14} aria-hidden="true" /> : <Search size={14} aria-hidden="true" />}<span>{p.label}</span><span className="chain-gate-state">{p.state === "supported" ? "Binding recorded" : "Evidence missing"}</span>
        </button>)}</div>
      </section>
      {compact&&<details className="chain-candidate-details"><summary>View the candidate chain</summary>{candidateCanvas}</details>}
    </div>
    <aside className="chain-inspector" ref={inspectorRef} aria-label="Evidence inspector">
      <header><Search size={16} aria-hidden="true" /><h4>Evidence inspector</h4></header>
      <button type="button" className="chain-back" onClick={() => { const target=compact?gatesRef.current:canvasRef.current;target?.scrollIntoView({ block: "start", behavior: "instant" });target?.querySelector<HTMLButtonElement>("button")?.focus({ preventScroll: true }); }}>{compact?"Back to required evidence":"Back to candidate chain"}</button>
      {compact&&<Link href={findingUrl} className="assessment-link">Open finding and source evidence <ArrowUpRight size={14} aria-hidden="true"/></Link>}
      <div aria-live="polite" className="chain-inspector-selection">
        <h5>{condition?.label ?? titles[step]}</h5>
        {condition ? <><span className="chain-inspector-state">{condition.state === "supported" ? "Binding recorded · access not established" : "Evidence missing"}</span><p>{condition.detail}</p></> : <>
          <p>{step === 0 ? "Record the starting location, actor and authentication state. Exposure labels alone do not establish access." : step === 1 ? "This finding is the candidate enabling weakness. Inspect its bindings and original evidence before treating it as a supported step." : finding.goal}</p>
          <ul className="chain-inspector-conditions">{conditions.map((p) => <li key={p.key}><strong>{p.label}</strong><span>{p.state === "supported" ? "Binding recorded" : "Evidence missing"}</span><p>{p.detail}</p></li>)}</ul>
        </>}
      </div>
      {!compact&&<Link href={findingUrl} className="assessment-link">Open finding and source evidence <ArrowUpRight size={14} aria-hidden="true" /></Link>}
      <details className="chain-reference"><summary>Finding and rule reference</summary><code>{finding.finding_id}</code><p>Rule: {finding.rule_version ?? "Experimental binding contract"}</p><p>Finding lifecycle: {finding.lifecycle}. A lifecycle edit alone does not verify a fix.</p></details>
      <section className="chain-next"><h4>Next action</h4><p>{condition?.state === "missing" ? condition.detail : finding.next_action}</p><dl><dt>Owner</dt><dd>{finding.owner_ref || "Not assigned"}</dd><dt>Verification</dt><dd>{finding.verification_required}</dd></dl></section>
    </aside>
  </article>;
}
