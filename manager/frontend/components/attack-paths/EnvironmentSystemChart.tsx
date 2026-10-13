import { Building2, Search, Server, ShieldAlert } from "lucide-react";
import type { EnvironmentFinding, EnvironmentResult } from "../../lib/environment-assessments";

const lifecycleLabels:Record<string,string>={open:"Open finding",confirmed:"Confirmed finding",accepted:"Risk accepted",remediated:"Remediation reported",fp:"Dismissed finding"};

/** Recorded system→finding associations, never network/attack edges. */
export function EnvironmentSystemChart({ result, selectedId, onSelect }: {result:EnvironmentResult;selectedId:string|null;onSelect:(item:EnvironmentFinding)=>void}) {
  return <section className="environment-chart" aria-label="Systems and findings in the selected assessments">
    <header><h3>How the findings relate to your systems</h3><span>Recorded associations</span></header>
    <p>Each line binds a finding to its recorded system. Cross-system attack connections need additional evidence.</p>
    <div className="environment-chart-lanes">{result.items.slice(0,20).map(item => <button type="button" className="environment-system-lane" key={`${item.engagement_id}:${item.finding_id}`} aria-pressed={selectedId === item.finding_id} onClick={()=>onSelect(item)}>
      <span className="environment-system-source"><Building2 size={16} aria-hidden="true" /><span>{item.engagement_name}</span></span>
      <span className="environment-system-asset"><Server size={17} aria-hidden="true" /><strong>{item.asset_label}</strong><small>{item.service_endpoint ?? "Service endpoint not recorded"}</small></span>
      <span className="environment-association" data-missing={!item.asset_id} aria-hidden="true" />
      <span className="environment-system-finding" data-severity={item.severity.toLowerCase()}><ShieldAlert size={16} aria-hidden="true" /><strong>{item.title}</strong><small><span className="environment-finding-severity" data-severity={item.severity.toLowerCase()}>{item.severity}</span><span>{lifecycleLabels[item.lifecycle]??"Status not recorded"} · {!item.asset_id ? "Asset binding needed · " : ""}{item.rule_applicability === "unmapped" ? "Rule not mapped" : "Connection evidence needed"}</span></small></span>
    </button>)}</div>
    {result.snapshot.engagement_ids.length > 1 && <div className="environment-bridge-gap"><Search size={17} aria-hidden="true" /><div><strong>No supported cross-assessment bridge is available</strong><p>Shared IP addresses, hostnames or vulnerabilities do not prove the same system or a movement path. Record directed reachability, service identity and the required access transfer to connect these chains.</p></div></div>}
  </section>;
}
