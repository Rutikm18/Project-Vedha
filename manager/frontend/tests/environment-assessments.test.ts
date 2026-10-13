import assert from "node:assert/strict";
import test from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { GET, POST } from "../app/api/attack-paths/environment-assessments/[[...path]]/route";
import { EnvironmentSystemChart } from "../components/attack-paths/EnvironmentSystemChart";
import type { EnvironmentResult } from "../lib/environment-assessments";

const id="11111111-1111-4111-8111-111111111111";

test("environment BFF rejects anonymous, traversal and unsupported write routes",async()=>{
  assert.equal((await GET(new Request("http://test/env"),{params:Promise.resolve({path:[]})})).status,401);
  const req=new Request("http://test/env",{headers:{authorization:"Bearer synthetic-test-token"}});
  assert.equal((await GET(req,{params:Promise.resolve({path:["..","engagements"]})})).status,404);
  assert.equal((await POST(new Request("http://test/env",{method:"POST",headers:{authorization:"Bearer synthetic-test-token"}}),{params:Promise.resolve({path:[id]})})).status,405);
});

test("selected engagement body and idempotency header reach the real API; denial stays denial",async()=>{
  const original=globalThis.fetch;
  let call: {url:string;body:unknown;key:string|null}|undefined;
  globalThis.fetch=async(input,init)=>{call={url:String(input),body:JSON.parse(String(init?.body)),key:new Headers(init?.headers).get("idempotency-key")};return Response.json({detail:"not authorized"},{status:403});};
  try {
    const response=await POST(new Request("http://test/env?tenant_id=foreign",{method:"POST",headers:{authorization:"Bearer synthetic-test-token","Content-Type":"application/json","Idempotency-Key":id},body:JSON.stringify({engagement_ids:[id]})}),{params:Promise.resolve({path:[]})});
    assert.equal(response.status,403);
    assert.equal(response.headers.get("cache-control"),"no-store");
    assert.deepEqual(call?.body,{engagement_ids:[id]});
    assert.equal(call?.key,id);
    assert.ok(!call?.url.includes("tenant_id"));
  }finally{globalThis.fetch=original;}
});

test("same system labels in two assessments remain separate recorded associations",()=>{
  const item={finding_id:"f1",title:"Example vulnerability <script>",severity:"high",lifecycle:"open",asset_label:"10.0.0.5",asset_id:"a1",service_endpoint:"tcp:6379",goal:"Assess read",goal_state:"indeterminate" as const,rule_applicability:"candidate" as const,supported_proofs:0,prerequisites:[],next_action:"Check evidence",owner_ref:null,verification_required:"Fresh evidence",engagement_id:"e1",engagement_name:"Assessment A"};
  const result:EnvironmentResult={snapshot:{id,status:"completed",engagement_ids:["e1","e2"],effective_as_of:"2026-10-13T00:00:00Z",failure_code:null,requires_reassessment:false},items:[item,{...item,finding_id:"f2",asset_id:null,engagement_id:"e2",engagement_name:"Assessment B"}],total:2,total_findings:2,page:1,page_size:20,compute:"complete_for_readiness",coverage:"partial",sources:[],systems:[],engine:{supported_proofs:[],realization:"not_observed_chain"},bridge_state:"not_normalized",missing_relationships:[]};
  const out=renderToStaticMarkup(createElement(EnvironmentSystemChart,{result,selectedId:"f1",onSelect:()=>{}}));
  assert.match(out,/Assessment A/);assert.match(out,/Assessment B/);
  assert.match(out,/Recorded associations/);
  assert.match(out,/No supported cross-assessment bridge/);
  assert.match(out,/Asset binding needed/);
  assert.ok(!out.includes("<script>"));
  const dismissed=renderToStaticMarkup(createElement(EnvironmentSystemChart,{result:{...result,items:[{...item,lifecycle:"fp"}]},selectedId:null,onSelect:()=>{}}));
  assert.match(dismissed,/Dismissed finding/);
  assert.match(dismissed,/Recorded associations/);
});

test("saved selection reads forward only supported query fields; malformed writes are rejected",async()=>{
  const original=globalThis.fetch;
  let called="";
  globalThis.fetch=async(input)=>{called=String(input);return Response.json({latest_request:null,last_completed:null});};
  try {
    const response=await GET(new Request(`http://test/env?engagement_ids=${id}&tenant_id=foreign`,{headers:{authorization:"Bearer synthetic-test-token"}}),{params:Promise.resolve({path:[]})});
    assert.equal(response.status,200);
    assert.ok(called.includes(`engagement_ids=${id}`));
    assert.ok(!called.includes("tenant_id"));
    const malformed=await POST(new Request("http://test/env",{method:"POST",headers:{authorization:"Bearer synthetic-test-token"},body:"{"}),{params:Promise.resolve({path:[]})});
    assert.equal(malformed.status,400);
  }finally{globalThis.fetch=original;}
});
