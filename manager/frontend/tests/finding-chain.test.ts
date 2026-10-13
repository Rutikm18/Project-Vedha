import assert from "node:assert/strict";
import test from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { FindingChainExplorer } from "../components/attack-paths/FindingChainExplorer";
import { PathDetailPanel } from "../app/engagements/[id]/attack-paths/Panels";
import type { FindingAssessment } from "../lib/attack-assessments";

const candidate: FindingAssessment = {
  finding_id: "finding-1", title: "Datastore exposure <script>", severity: "high", lifecycle: "accepted",
  asset_label: "service.example", service_endpoint: "tcp:6379", goal: "Assess data read",
  goal_state: "indeterminate", rule_applicability: "candidate", supported_proofs: 0,
  prerequisites: [{key:"finding_asset_binding",label:"Bound asset",state:"supported",detail:"Recorded binding"}, {key:"observed_service_instance",label:"Instance identity",state:"missing",detail:"Instance not recorded"}],
  next_action:"Review missing evidence", owner_ref:null, verification_required:"Recollect comparable evidence",
};

test("candidate chain never promotes recorded bindings into supported access", () => {
  const out = renderToStaticMarkup(createElement(FindingChainExplorer, {finding:candidate,engagementId:"eng-1"}));
  assert.match(out, /Candidate chain; required evidence is missing/);
  assert.match(out, /Access not established/);
  assert.match(out, /No supported transition is established/);
  assert.match(out, /Binding recorded/);
  assert.match(out, /Evidence missing/);
  assert.match(out, /All required conditions/);
  assert.match(out, /Not assigned/);
  assert.match(out, /finding=finding-1/);
  assert.ok(!out.includes("<script>"), "untrusted finding titles remain escaped");
});

test("unmapped finding never invents a data-read consequence", () => {
  const out = renderToStaticMarkup(createElement(FindingChainExplorer, {finding:{...candidate,rule_applicability:"unmapped",goal_state:"not_evaluated",goal:"Rule applicability not established"},engagementId:"eng-1"}));
  assert.match(out, /Outcome not evaluated/);
  assert.doesNotMatch(out, /Application data read/);
});

test("compact investigation leads with required evidence and keeps the speculative chain secondary",()=>{
  const out=renderToStaticMarkup(createElement(FindingChainExplorer,{finding:candidate,engagementId:"eng-1",compact:true}));
  assert.ok(out.indexOf("Review missing evidence")<out.indexOf("All required conditions"));
  assert.ok(out.indexOf("All required conditions")<out.indexOf("View the candidate chain"));
  assert.match(out,/Open finding and source evidence/);
  assert.match(out,/No supported transition is established/);
  assert.match(out,/Finding lifecycle: accepted/);
});

test("legacy chain links the actual enabling finding while preserving model limitations", () => {
  const out = renderToStaticMarkup(createElement(PathDetailPanel, {engagementId:"eng-1",detail:{id:"route-1", risk_score: 10, freshness:"fresh",node_count:2,nodes:["entry","target"],chokepoints:[],hops:[{from:"entry",to:"target",technique:"SAME_SUBNET",weight:1,exploited:true,cvss:9.8,via:[],basis:"assumed",likelihood:0.9,stale:false,explanation:"Modeled transition",finding:{id:"finding-1",title:"Actual enabling finding",severity:"high",lifecycle:"open",cve_ids:[],record_updated_at:"2026-10-13T00:00:00Z",metadata_basis:"current_scoped_finding_not_snapshot_proof"}}]}}));
  assert.match(out, /Actual enabling finding/);
  assert.match(out, /finding=finding-1/);
  assert.match(out, /Current finding metadata/);
  assert.doesNotMatch(out, /Likelihood 90%/);
});
