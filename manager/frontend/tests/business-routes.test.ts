import assert from "node:assert/strict";
import test from "node:test";
import fixture from "../lib/demo-business-routes.json";
import { analyse, compare, previewFix, validEdges, type BusinessScan } from "../lib/business-routes";
import { routeLayout } from "../lib/business-route-layout";

// JSON is an isolated, labelled developer fixture, never the actual API source.
const [first,second]=fixture.scans as BusinessScan[];
test("made-up fixture has eight routes, three critical systems and one confirmed route",()=>{
  assert.equal(first.nodes.length,12);assert.equal(first.edges.length,15);
  const result=analyse(first,{showTheoretical:true});
  assert.equal(result.totalPaths,8);assert.equal(result.confirmedPaths,1);
  assert.deepEqual([...result.reachableCrowns].sort(),["backups","business","customer"]);
  assert.equal(result.edgeIds.size,15);assert.equal(result.truncated,false);
  const after=analyse(second,{showTheoretical:true});
  assert.equal(after.totalPaths,6);assert.equal(after.confirmedPaths,0);
  assert.deepEqual([...after.reachableCrowns].sort(),["backups","business"]);
});
test("previewing the only confirmed customer route breaks it without changing scan data",()=>{
  const baseline=JSON.stringify(first);
  const before=analyse(first,{showTheoretical:false});assert.equal(before.confirmedPaths,1);
  const preview=previewFix(first,"f3");const after=analyse(preview,{showTheoretical:false});
  assert.equal(after.confirmedPaths,0);assert.equal(after.reachableCrowns.has("customer"),false);
  assert.equal(JSON.stringify(first),baseline);
  assert.equal(analyse(previewFix(preview,"f3",false),{showTheoretical:false}).confirmedPaths,1);
  // Possible alternative access remains when the broader filter is on.
  assert.equal(analyse(preview,{showTheoretical:true}).reachableCrowns.has("customer"),true);
});
test("possible-route toggle filters the computation, cycles terminate, duplicates do not inflate counts",()=>{
  assert.equal(analyse(first,{showTheoretical:false}).totalPaths,1);
  const cyclic={...first,edges:[...first.edges,{id:"cycle",from:"jump",to:"vpn",findingId:"f2",status:"confirmed" as const},{...first.edges[0],id:"duplicate"}]};
  assert.equal(analyse(cyclic,{showTheoretical:true}).totalPaths,8);
  assert.equal(analyse(cyclic,{showTheoretical:true}).edgeIds.has("cycle"),false);
  assert.equal(validEdges(cyclic).edges.length,16);
});
test("budgets report incomplete counts while reachability remains correct",()=>{
  const result=analyse(first,{showTheoretical:true,maxPaths:1,maxWork:20});
  assert.equal(result.truncated,true);assert.equal(result.totalPaths,1);
  assert.equal(result.reachableCrowns.size,3);assert.equal(result.confirmedPaths,1);
  assert.throws(()=>analyse(first,{showTheoretical:true,maxPaths:0}));
  assert.throws(()=>validEdges({...first,edges:[...first.edges,{...first.edges[0],to:"mail"}]}),/Conflicting/);
  assert.equal(analyse({...first,edges:[]},{showTheoretical:true}).totalPaths,0);
});
test("comparison credits explicit fixed state and never turns a missing finding into a fix",()=>{
  assert.deepEqual(compare(first,second).fixed.sort(),["f3","f4"]);assert.deepEqual(compare(first,second).new,["f16"]);
  const missing={...first,findings:{...first.findings}};delete missing.findings.f3;
  assert.deepEqual(compare(first,missing).fixed,[]);assert.deepEqual(compare(first,missing).missing,["f3"]);
  assert.throws(()=>compare(first,{...second,engagementIds:["foreign"]}),/same scope/);
});
test("layout stays in four semantic columns and handles a 300-system/600-connection topology",()=>{
  const positions=routeLayout(first);assert.equal(positions.get("internet")?.x,0);assert.ok(positions.get("customer")!.x>positions.get("database")!.x);
  const scan:BusinessScan={id:"load",takenAt:first.takenAt,grade:null,nodes:Array.from({length:300},(_,i)=>({id:String(i),label:String(i),type:i===0?"entry":i===299?"crown":"asset",column:i===0?0:i===299?3:2})),edges:[],findings:{f:{id:"f",title:"Load test",severity:"low",plainReason:"Test",fixSteps:[],fixed:false}}};
  scan.edges=Array.from({length:600},(_,i)=>({id:String(i),from:String(i%298),to:String((i%298)+1+(i>=298?1:0)),findingId:"f",status:"theoretical"}));
  const started=performance.now();assert.equal(routeLayout(scan).size,300);const laidOut=performance.now()-started;
  const analysis=analyse(scan,{showTheoretical:true,maxPaths:20,maxWork:5000});assert.equal(analysis.reachableCrowns.has("299"),true);
  console.log(`300/600 route layout: ${Math.round(laidOut)}ms; bounded enumeration reports truncated=${analysis.truncated}`);
});

test("critical entries require a non-zero simple route and critical assets may lead to other critical assets",()=>{
  const scan:BusinessScan={...first,nodes:[{id:"a",label:"A",type:"crown",entry:true},{id:"b",label:"B",type:"crown"},{id:"c",label:"C",type:"crown"}],
    edges:[{id:"ab",from:"a",to:"b",findingId:"f1",status:"confirmed"},{id:"bc",from:"b",to:"c",findingId:"f2",status:"confirmed"},{id:"ba",from:"b",to:"a",findingId:"f3",status:"confirmed"}]};
  const result=analyse(scan,{showTheoretical:false});
  assert.equal(result.totalPaths,2);assert.equal(result.confirmedPaths,2);
  assert.deepEqual([...result.reachableCrowns].sort(),["b","c"]);
  assert.equal(analyse({...scan,edges:[]},{showTheoretical:false}).reachableCrowns.size,0);
  const limited=analyse(scan,{showTheoretical:false,maxPaths:1});
  assert.equal(limited.totalPaths,1);assert.equal(limited.truncated,true);
  assert.deepEqual([...limited.reachableCrowns].sort(),["b","c"]);
  const secondEntry={...scan,nodes:scan.nodes.map(n=>n.id==="b"?{...n,entry:true}:n)};
  assert.equal(analyse(secondEntry,{showTheoretical:false}).reachableCrowns.has("a"),true);
});

test("withdrawn findings and stale duplicate connections cannot contribute to counted routes",()=>{
  for (const withdrawn of [{lifecycle:"fp"},{verificationState:"contradicted"}]) {
    const scan={...first,findings:{...first.findings,f3:{...first.findings.f3,...withdrawn}}};
    assert.equal(analyse(scan,{showTheoretical:false}).confirmedPaths,0);
    assert.equal(analyse(scan,{showTheoretical:false}).reachableCrowns.size,0);
    assert.equal(validEdges(scan).omitted,1);
  }
  const fresh=first.edges.find(e=>e.findingId==="f3")!;
  for(const duplicates of [[{...fresh,id:"old",stale:true},fresh],[fresh,{...fresh,id:"old",stale:true}]]) {
    const scan={...first,edges:[...first.edges.filter(e=>e.findingId!=="f3"),...duplicates]};
    assert.equal(analyse(scan,{showTheoretical:false}).confirmedPaths,0);
    assert.equal(validEdges(scan).edges.find(e=>e.findingId==="f3")?.stale,true);
  }
});

test("actual stored-model bindings are checked and cannot promote a finding verdict into a confirmed route",()=>{
  const scan:BusinessScan={id:"actual",source:"stored_models",takenAt:first.takenAt,grade:null,nodes:[
    {id:"a:source",assetId:"source",engagementId:"a",label:"Source",type:"entry"},
    {id:"a:target",assetId:"target",engagementId:"a",label:"Target",type:"crown"}],
    findings:{"a:f":{...first.findings.f1,id:"a:f",findingId:"f",engagementId:"a",assetId:"target",findingConfirmed:true}},
    edges:[{id:"edge",from:"a:source",to:"a:target",findingId:"a:f",status:"confirmed"}]};
  const result=analyse(scan,{showTheoretical:true});
  assert.equal(result.totalPaths,1);assert.equal(result.confirmedPaths,0);
  assert.equal(analyse(scan,{showTheoretical:false}).totalPaths,0);
  for(const patch of [{assetId:"source"},{engagementId:"b"},{findingId:"foreign"}]) {
    assert.equal(analyse({...scan,findings:{"a:f":{...scan.findings["a:f"],...patch}}},{showTheoretical:true}).totalPaths,0);
  }
});

test("comparison distinguishes dismissals and unverified closure from unresolved findings and scan fixes",()=>{
  const scan={...first,findings:{...first.findings,f1:{...first.findings.f1,lifecycle:"fp"},f2:{...first.findings.f2,lifecycle:"remediated",fixed:false},f3:{...first.findings.f3,verificationState:"contradicted"},f4:{...first.findings.f4,lifecycle:"accepted"}}};
  const delta=compare(first,scan);
  assert.deepEqual(delta.dismissed.sort(),["f1","f3"]);
  assert.deepEqual(delta.awaitingConfirmation,["f2"]);
  assert.ok(!delta.stillOpen.includes("f1")&&!delta.stillOpen.includes("f2")&&!delta.stillOpen.includes("f3"));
  assert.ok(delta.stillOpen.includes("f4"));assert.deepEqual(delta.fixed,[]);
});
