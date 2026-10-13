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
