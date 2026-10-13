import assert from "node:assert/strict";
import test from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { BusinessRoutePanel } from "../components/attack-paths/BusinessRoutePanel";
import fixture from "../lib/demo-business-routes.json";
import type { BusinessScan } from "../lib/business-routes";

const [first,second]=fixture.scans as BusinessScan[];
test("demo panel labels its origin and offers preview rather than changing real findings",()=>{
  const html=renderToStaticMarkup(createElement(BusinessRoutePanel,{current:second,previous:first}));
  assert.match(html,/Made-up demonstration/);assert.match(html,/Preview this fix/);
  assert.match(html,/View as list/);assert.match(html,/What changed between these/);
  assert.ok(!html.includes("Mark as fixed and rescan"));assert.ok(!html.includes("100% secure"));
});
test("actual empty graph cannot substitute demo assets, a grade or confirmed connections",()=>{
  const actual:BusinessScan={id:"actual",takenAt:first.takenAt,grade:null,source:"stored_models",nodes:[],edges:[],findings:{},coverage:"partial"};
  const html=renderToStaticMarkup(createElement(BusinessRoutePanel,{current:actual}));
  assert.match(html,/Not available/);assert.match(html,/No routes shown/);
  assert.ok(!html.includes("VPN gateway"));assert.ok(!html.includes("Made-up demonstration"));
});
test("finding copy remains escaped and an unavailable remediation is stated plainly",()=>{
  const scan:BusinessScan={...first,findings:Object.fromEntries(Object.entries(first.findings).map(([id,f])=>[id,{...f,title:"<script>unsafe</script>",fixSteps:[]}]))};
  const html=renderToStaticMarkup(createElement(BusinessRoutePanel,{current:scan}));
  assert.ok(!html.includes("<script>unsafe</script>"));assert.match(html,/No fix instructions were captured/);
});

test("actual finding provenance is visible while a confirmed finding remains only a possible connection",()=>{
  const actual:BusinessScan={id:"capture",source:"stored_models",takenAt:first.takenAt,grade:null,nodes:[
    {id:"a:entry",assetId:"entry",engagementId:"a",label:"Assessed entry",type:"entry"},
    {id:"a:target",assetId:"target",engagementId:"a",label:"Critical system",type:"crown"}],
    edges:[{id:"hop",from:"a:entry",to:"a:target",findingId:"a:f",status:"confirmed"}],
    findings:{"a:f":{...first.findings.f3,id:"a:f",findingId:"f",engagementId:"a",assetId:"target",verificationState:"confirmed",findingConfirmed:true,observedAt:"2026-10-01T12:00:00Z",lifecycle:"remediated",fixed:false}}};
  const html=renderToStaticMarkup(createElement(BusinessRoutePanel,{current:actual}));
  assert.match(html,/Based on recorded findings/);assert.match(html,/Finding verdict: confirmed/);
  assert.match(html,/Last observed/);assert.match(html,/completed scan confirmation/);
  assert.match(html,/Theoretical \(possible\)/);assert.match(html,/Open finding and record remediation/);
  assert.ok(!html.includes('data-certainty="confirmed"'));
  const stale=renderToStaticMarkup(createElement(BusinessRoutePanel,{current:{...actual,edges:actual.edges.map(e=>({...e,stale:true}))}}));
  assert.match(stale,/Older connection/);assert.match(stale,/excluded from route counts/);
});
