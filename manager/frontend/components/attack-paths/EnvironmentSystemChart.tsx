import { Search, Server } from "lucide-react";
import type { EnvironmentFinding, EnvironmentResult } from "../../lib/environment-assessments";

const lifecycleLabels:Record<string,string>={open:"Open finding",confirmed:"Confirmed finding",accepted:"Risk accepted",remediated:"Remediation reported",fp:"Dismissed finding"};

/** A finding queue retains recorded system bindings; these rows are not attack edges. */
export function EnvironmentSystemChart({result,selectedId,onSelect}:{result:EnvironmentResult;selectedId:string|null;onSelect:(item:EnvironmentFinding)=>void}) {
  return <section className="environment-chart" aria-label="Systems and findings in the selected assessments">
    <header><h2>Captured findings</h2><span>{result.items.length} on this page</span></header>
    <p>Select a finding to review its system, required evidence and next action.</p>
    <div className="environment-finding-list">{result.items.slice(0,20).map(item=><button type="button" className="environment-finding-row" key={`${item.engagement_id}:${item.finding_id}`} aria-pressed={selectedId===item.finding_id} data-severity={item.severity.toLowerCase()} onClick={()=>onSelect(item)}>
      <span className="environment-finding-title"><strong>{item.title}</strong><span className="environment-finding-severity" data-severity={item.severity.toLowerCase()}>{item.severity}</span></span>
      <span className="environment-finding-system"><Server size={14} aria-hidden="true"/><span>{item.asset_label}{item.service_endpoint?` · ${item.service_endpoint}`:" · Service endpoint not recorded"}</span></span>
      <span className="environment-finding-assessment">{item.engagement_name}</span>
      <span className="environment-finding-state">{lifecycleLabels[item.lifecycle]??"Status not recorded"}{!item.asset_id?" · Asset binding needed":""}</span>
    </button>)}</div>
    <details className="environment-association-note"><summary>Recorded associations</summary><p>Each finding stays attached to its recorded system. System bindings do not establish a connection between systems.</p>
      {result.snapshot.engagement_ids.length>1&&<div className="environment-bridge-gap"><Search size={15} aria-hidden="true"/><div><strong>No supported cross-assessment bridge is available</strong><p>Shared IP addresses, hostnames or vulnerabilities do not prove the same system or a movement path. Directed reachability, service identity and access-transfer evidence are required.</p></div></div>}
    </details>
  </section>;
}
