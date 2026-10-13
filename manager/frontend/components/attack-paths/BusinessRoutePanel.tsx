"use client";

import { memo, useCallback, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { Controls, Handle, MarkerType, Position, ReactFlow, type Edge, type EdgeChange, type Node, type NodeChange, type NodeProps, type ReactFlowInstance } from "@xyflow/react";
import { ArrowRight, CheckCircle2, Crown, Globe, List, RotateCcw, Search, Server, Undo2 } from "lucide-react";
import { analyse, compare, previewFix, validEdges, type BusinessNode, type BusinessScan } from "../../lib/business-routes";
import { routeLayout } from "../../lib/business-route-layout";

type FlowNode = Node<{ model: BusinessNode; reachable: boolean; confirmed: boolean }, "business">;
type Selection = {kind:"node"|"edge";id:string}|null;
const LANES = ["Entry point", "Exposed assets", "Inside the network", "Critical assets"];
const RouteNode = memo(function RouteNode({data}:NodeProps<FlowNode>){
  const {model,reachable,confirmed}=data;
  const Icon=model.type==="crown"?Crown:model.type==="entry"?Globe:Server;
  return <div className="business-route-node" data-kind={model.type} data-reachable={reachable} data-certainty={confirmed?"confirmed":reachable?"possible":"unknown"}>
    <Handle type="target" position={Position.Left} isConnectable={false}/>
    <Icon size={18} aria-hidden="true"/><strong>{model.label}</strong>
    <span>{model.type==="crown"?(confirmed?"Confirmed route":reachable?"Possible route":"No route shown"):model.type==="entry"?"Entry location":model.engagementName??"Assessed system"}</span>
    <Handle type="source" position={Position.Right} isConnectable={false}/>
  </div>;
});
const LaneNode = memo(function LaneNode({data}:{data:{label:string}}){return <div className="business-route-lane">{data.label}</div>;});
const nodeTypes={business:RouteNode,lane:LaneNode};

export function BusinessRoutePanel({current,previous}:{current:BusinessScan;previous?:BusinessScan}) {
  return <RoutePanel key={`${current.id}:${previous?.id??"none"}`} current={current} previous={previous}/>;
}

function RoutePanel({current,previous}:{current:BusinessScan;previous?:BusinessScan}) {
  const [capture,setCapture]=useState<"current"|"previous">("current");
  const [showTheoretical,setShowTheoretical]=useState(true);
  const [viewAsList,setViewAsList]=useState(false);
  const [page,setPage]=useState(0);
  const [selection,setSelection]=useState<Selection>(null);
  const [previews,setPreviews]=useState<Set<string>>(new Set());
  const inspectorRef=useRef<HTMLElement>(null);
  const flowRef=useRef<ReactFlowInstance>(null);
  const base=capture==="previous"&&previous?previous:current;
  const laneLabels=base.source==="demo"?LANES:["Modelled entry", "Exposed assets", "Assessed systems", "Critical assets"];
  const scan=useMemo(()=>{
    let next=base;
    for(const id of Object.keys(base.findings)) if(previews.has(`${base.id}:${id}`)) next=previewFix(next,id);
    return next;
  },[base,previews]);
  const analysis=useMemo(()=>analyse(scan,{showTheoretical}),[scan,showTheoretical]);
  const confirmedAnalysis=useMemo(()=>showTheoretical?analyse(scan,{showTheoretical:false}):analysis,[scan,showTheoretical,analysis]);
  const positions=useMemo(()=>routeLayout({nodes:base.nodes,edges:base.edges}),[base.nodes,base.edges]); // preview fixes never move the map
  const normalized=useMemo(()=>validEdges(base).edges,[base]);
  const nodeMap=useMemo(()=>new Map(base.nodes.map(n=>[n.id,n])),[base.nodes]);
  const delta=useMemo(()=>previous?compare(previous,current):null,[previous,current]);
  const defaultEdge=normalized.find(e=>analysis.edgeIds.has(e.id)&&scan.findings[e.findingId].severity==="critical")??normalized[0];
  const selected=selection??(defaultEdge?{kind:"edge",id:defaultEdge.id} as const:null);
  const selectedEdge=selected?.kind==="edge"?normalized.find(e=>e.id===selected.id):null;
  const selectedNode=selected?.kind==="node"?nodeMap.get(selected.id):null;
  const finding=selectedEdge?scan.findings[selectedEdge.findingId]:null;
  const openDetails=useCallback((next:Selection)=>{
    setSelection(old=>old?.id===next?.id&&old?.kind===next?.kind?old:next);
    if(window.matchMedia("(max-width: 1299px)").matches) inspectorRef.current?.scrollIntoView({block:"nearest",behavior:"instant"});
  },[]);
  const initialIds=analysis.paths[0]?.nodes??base.nodes.slice(0,12).map(n=>n.id);
  const flowNodes:Node[]=base.nodes.map(model=>({id:model.id,type:"business",position:positions.get(model.id)!,width:132,height:134,
    data:{model,reachable:analysis.reachableCrowns.has(model.id),confirmed:confirmedAnalysis.reachableCrowns.has(model.id)},selected:selection?.kind==="node"&&selection.id===model.id,
    ariaLabel:`${model.label}, ${model.type==="crown"?"critical asset":model.type==="entry"?"entry location":"system"}${model.type==="crown"?analysis.reachableCrowns.has(model.id)?", reachable in this view":", no route shown":""}`,
    sourcePosition:Position.Right,targetPosition:Position.Left}));
  for(let lane=0;lane<4;lane++) flowNodes.push({id:`route-lane-${lane}`,type:"lane",position:{x:lane*160,y:12},width:132,height:40,data:{label:laneLabels[lane]},selectable:false,focusable:false});
  const flowEdges:Edge[]=normalized.filter(e=>showTheoretical||e.status==="confirmed").map(e=>{
    const fixed=scan.findings[e.findingId].fixed, onRoute=analysis.edgeIds.has(e.id);
    const status=e.status==="confirmed"?"Confirmed":"Theoretical";
    const inactiveLabel=base.findings[e.findingId].fixed?"Fixed by scan":"Fix preview";
    const colour=fixed?"var(--route-inactive)":e.status==="confirmed"?"var(--route-confirmed)":"var(--route-possible)";
    return {id:e.id,source:e.from,target:e.to,type:"smoothstep",label:selection?.id===e.id?(fixed?inactiveLabel:status):undefined,
      selected:selection?.kind==="edge"&&selection.id===e.id,className:`business-route-edge ${fixed?"is-fixed":e.status} ${onRoute?"on-route":""}`,
      markerEnd:{type:MarkerType.ArrowClosed,width:16,height:16,color:colour},
      style:{stroke:colour,strokeWidth:selection?.id===e.id?3.5:onRoute?2.5:1.4,strokeDasharray:e.status==="theoretical"?"6 5":undefined,opacity:fixed?.55:1},
      labelStyle:{fill:"var(--text-primary)",fontSize:11},labelBgStyle:{fill:"var(--bg-panel)"},labelBgPadding:[5,4],interactionWidth:28,
      ariaLabel:`Route from ${nodeMap.get(e.from)?.label} to ${nodeMap.get(e.to)?.label}, ${status.toLowerCase()}, ${scan.findings[e.findingId].severity}${fixed?", removed from this view":""}`};
  });
  const confirmedLabel=analysis.confirmedTruncated?`${analysis.confirmedPaths}+`:String(analysis.confirmedPaths);
  const fixedCount=Object.values(scan.findings).filter(f=>f.fixed).length;
  const previewCount=Object.keys(base.findings).filter(id=>previews.has(`${base.id}:${id}`)).length;
  const countLabel=analysis.truncated?`At least ${analysis.totalPaths}`:String(analysis.totalPaths);
  const reset=()=>{setPreviews(new Set());setShowTheoretical(true);setSelection(null);setPage(0);void flowRef.current?.fitView({nodes:initialIds.map(id=>({id})),padding:.18,maxZoom:1});};
  const sourceLink=finding?.findingId&&finding.engagementId?`/findings?engagement=${encodeURIComponent(finding.engagementId)}&finding=${encodeURIComponent(finding.findingId)}`:null;
  const selectedInMap=useCallback(({nodes,edges}:{nodes:Node[];edges:Edge[]})=>{
    const node=nodes.find(n=>n.type==="business"),edge=edges[0];
    if(node) openDetails({kind:"node",id:node.id});else if(edge) openDetails({kind:"edge",id:edge.id});
  },[openDetails]);
  const nodeChanges=useCallback((changes:NodeChange[])=>{for(const change of changes) if(change.type==="select"&&change.selected&&!change.id.startsWith("route-lane-"))openDetails({kind:"node",id:change.id});},[openDetails]);
  const edgeChanges=useCallback((changes:EdgeChange[])=>{for(const change of changes) if(change.type==="select"&&change.selected)openDetails({kind:"edge",id:change.id});},[openDetails]);

  return <section className="business-routes" aria-labelledby="business-routes-title">
    <header className="business-routes-heading"><div><h2 id="business-routes-title">Routes to your critical assets</h2><p>See what could connect, why it matters, and which fix would break a route.</p></div><span>{base.source==="demo"?"Made-up example":"Captured environment"}</span></header>
    {base.source==="demo"?<p className="business-route-notice" role="status">Made-up demonstration. These systems, findings and scans are not customer evidence.</p>:<p className="business-route-notice">Connections come from your stored route models. They remain possible until the full connection is confirmed. Entry locations are modelled; selecting engagements does not establish a shared network.</p>}
    <dl className="business-route-metrics">
      <div><dt>Environment grade</dt><dd data-unavailable={!base.grade}>{base.grade??"Not available"}</dd></div>
      <div><dt>Confirmed routes</dt><dd data-tone={analysis.confirmedPaths>0?"risk":"neutral"}>{confirmedLabel}</dd></div>
      <div><dt>Critical assets reachable</dt><dd data-tone={confirmedAnalysis.reachableCrowns.size>0?"risk":analysis.reachableCrowns.size>0?"possible":"neutral"}>{analysis.reachableCrowns.size}<small>in this view</small></dd></div>
      <div><dt>Open findings on a route</dt><dd data-tone={analysis.findingIds.size>0?"possible":"neutral"}>{analysis.findingIds.size}{analysis.truncated&&<small>partial count</small>}</dd></div>
      <div><dt>{previewCount?"Fixed in this preview":base.source==="demo"?"Findings fixed":"Findings fixed by scan"}</dt><dd data-tone={previewCount?"preview":fixedCount>0?"confirmed":"neutral"}>{fixedCount}</dd></div>
    </dl>
    <div className="business-route-toolbar">
      <div className="business-route-captures" aria-label="Captured view"><button type="button" aria-pressed={capture==="current"} onClick={()=>{setCapture("current");setSelection(null);setPage(0);}}>{base.source==="demo"?"Scan two":"Latest view"}</button><button type="button" disabled={!previous} aria-pressed={capture==="previous"} onClick={()=>{setCapture("previous");setSelection(null);setPage(0);}}>{base.source==="demo"?"Scan one":"Previous view"}</button></div>
      <label><input type="checkbox" checked={showTheoretical} onChange={e=>{setShowTheoretical(e.target.checked);setSelection(null);setPage(0);}}/>Show possible routes</label>
      <button type="button" className="btn btn-secondary" aria-pressed={viewAsList} onClick={()=>setViewAsList(!viewAsList)}><List size={15} aria-hidden="true"/>{viewAsList?"View as map":"View as list"}</button>
      <button type="button" className="btn btn-secondary" onClick={reset}><RotateCcw size={14} aria-hidden="true"/>Reset preview</button>
    </div>
    <div className="business-route-meta"><span>{base.nodes.length} systems · {normalized.length} recorded connections · {countLabel} routes</span><time dateTime={base.takenAt}>Captured {new Date(base.takenAt).toLocaleString()}</time></div>
    {(base.truncated||analysis.truncated||analysis.omittedEdges||(base.omittedConnections??0)>0)&&<p role="status" className="business-route-notice">This view is incomplete. {(base.omittedConnections??0)+analysis.omittedEdges} connections could not be included. {analysis.truncated?"The route computation limit was reached; counts are lower bounds.":"Some source records are unavailable or exceeded the view limit."}</p>}
    {previewCount>0&&<p className="business-route-preview" role="status">What-if preview: {previewCount} {previewCount===1?"fix":"fixes"} applied in this view. Your findings and scans have not changed. Undo a fix or reset to return to the captured result.</p>}
    <div className="business-route-workspace">
      <div className="business-route-main">
        {!analysis.totalPaths&&<div className="business-route-empty"><Search size={18} aria-hidden="true"/><div><strong>No routes shown to your critical assets</strong><p>{base.nodes.some(n=>n.type==="crown")?"The selected connections do not establish a route. Missing evidence or hidden possible routes can explain this result.":"No assessed system in this view is marked critical. Mark the business systems that matter before interpreting route counts."}</p></div></div>}
        {viewAsList?<div className="business-route-list"><table><caption>Routes in this view; select a connection to read its finding</caption><thead><tr><th>Route</th><th>Systems and enabling findings</th><th>Status</th></tr></thead><tbody>{analysis.paths.slice(page*20,page*20+20).map((path,index)=><tr key={path.id}><th scope="row">{page*20+index+1}</th><td><ol>{path.edges.map(id=>{const e=normalized.find(e=>e.id===id)!;return <li key={id}><button type="button" onClick={()=>openDetails({kind:"edge",id})}>{nodeMap.get(e.from)?.label}<ArrowRight size={12} aria-hidden="true"/>{nodeMap.get(e.to)?.label}<span>{scan.findings[e.findingId].title}</span></button></li>;})}</ol></td><td><span className="business-route-status" data-status={path.confirmed?"confirmed":"theoretical"}>{path.confirmed?"Confirmed":"Possible"}</span></td></tr>)}</tbody></table>{analysis.paths.length>20&&<nav aria-label="Route list pages"><button className="btn btn-secondary" disabled={page===0} onClick={()=>setPage(page-1)}>Previous 20</button><span>{Math.max(0,analysis.paths.length-(page+1)*20)} more{analysis.truncated?" or more":""}</span><button className="btn btn-secondary" disabled={(page+1)*20>=analysis.paths.length} onClick={()=>setPage(page+1)}>Next 20</button></nav>}</div>:<div className="business-route-canvas" aria-label="Route map. Use Tab to focus systems and connections; Enter to select. Drag the background to pan.">
          <ReactFlow nodes={flowNodes} edges={flowEdges} nodeTypes={nodeTypes} fitView fitViewOptions={{nodes:[...initialIds.map(id=>({id})),...LANES.map((_,i)=>({id:`route-lane-${i}`}))],padding:.12,minZoom:.45,maxZoom:1}}
            onInit={instance=>{flowRef.current=instance;}} onNodeClick={(_,node)=>{if(node.type==="business")openDetails({kind:"node",id:node.id});}} onEdgeClick={(_,edge)=>openDetails({kind:"edge",id:edge.id})}
            onNodesChange={nodeChanges} onEdgesChange={edgeChanges}
            onSelectionChange={selectedInMap}
            nodesDraggable={false} nodesConnectable={false} edgesReconnectable={false} deleteKeyCode={null} minZoom={.15} maxZoom={1.8} onlyRenderVisibleElements>
            <Controls showInteractive={false}/>
          </ReactFlow>
        </div>}
        <div className="business-route-legend" aria-label="Connection legend"><span><i data-state="confirmed"/>Confirmed</span><span><i data-state="theoretical"/>Theoretical (possible)</span><span><i data-state="fixed"/>Removed in preview / fixed</span></div>
        <p className="business-route-caption">A route is confirmed only when every connection on it is confirmed. No route shown does not establish that the environment is safe.</p>
      </div>
      <aside ref={inspectorRef} className="business-route-inspector" aria-label="Connection details">
        <header><h3>{selectedNode?"How this system is reached":"Finding behind this connection"}</h3></header>
        {finding&&selectedEdge?<>
          <div className="business-route-status-row"><span className="business-route-status" data-status={previews.has(`${base.id}:${finding.id}`)?"preview":base.findings[finding.id].fixed?"fixed":selectedEdge.status}><span>{previews.has(`${base.id}:${finding.id}`)?<Undo2 size={14}/>:base.findings[finding.id].fixed||selectedEdge.status==="confirmed"?<CheckCircle2 size={14}/>:<Search size={14}/>}</span>{previews.has(`${base.id}:${finding.id}`)?"Fix preview":base.findings[finding.id].fixed?"Fixed by scan":selectedEdge.status==="confirmed"?"Confirmed":"Theoretical (possible)"}</span><span className="business-route-severity" data-severity={finding.severity}>{finding.severity}</span></div>
          <h4>{finding.title}</h4><p className="business-route-direction">{nodeMap.get(selectedEdge.from)?.label}<ArrowRight size={14} aria-hidden="true"/>{nodeMap.get(selectedEdge.to)?.label}</p><p>{finding.plainReason}</p>
          {finding.findingConfirmed&&selectedEdge.status!=="confirmed"&&<p>The finding itself is confirmed. That does not confirm the full connection.</p>}
          {selectedEdge.stale&&<p>This stored connection includes an older observation. Check it again before relying on it.</p>}
          {finding.lifecycle==="remediated"&&!base.findings[finding.id].fixed&&<p>Remediation was reported manually; scan confirmation is still missing.</p>}
          <h5>How to fix it</h5>{finding.fixSteps.length?<ol>{finding.fixSteps.map((step,i)=><li key={i}>{step}</li>)}</ol>:<p>No fix instructions were captured. Open the finding to review its remediation.</p>}
          {base.findings[finding.id].fixed?<p className="business-route-fixed">This capture records a scan-confirmed fix.</p>:<button type="button" className="btn btn-primary" onClick={()=>{setSelection({kind:"edge",id:selectedEdge.id});setPreviews(old=>{const next=new Set(old),key=`${base.id}:${finding.id}`;if(next.has(key))next.delete(key);else next.add(key);return next;});}}>{previews.has(`${base.id}:${finding.id}`)?<Undo2 size={15}/>:<Search size={15}/>} {previews.has(`${base.id}:${finding.id}`)?"Undo fix preview":"Preview this fix"}</button>}
          <p className="business-route-action-note">Preview only. Record the work in the finding, then use a fresh approved scan to confirm it.</p>{sourceLink&&<Link href={sourceLink}>Open finding and record remediation <ArrowRight size={12} aria-hidden="true"/></Link>}
        </>:selectedNode?<><h4>{selectedNode.label}</h4><p>{selectedNode.engagementName??"System in this captured view"}</p><p>{analysis.paths.filter(p=>p.nodes.includes(selectedNode.id)).length} displayed routes include this system.</p><ul>{normalized.filter(e=>e.to===selectedNode.id).map(e=><li key={e.id}><button type="button" onClick={()=>openDetails({kind:"edge",id:e.id})}>{nodeMap.get(e.from)?.label} → {scan.findings[e.findingId].title}</button></li>)}</ul>{!normalized.some(e=>e.to===selectedNode.id)&&<p>No incoming connection is recorded here. An entry location starts a modelled route; it is not an invented Internet hop.</p>}</>:<p>Select a connection or a system to inspect it. No connection data has been captured for this view yet.</p>}
      </aside>
    </div>
    {delta&&<details className="business-route-comparison"><summary>What changed between these {base.source==="demo"?"scans":"captured views"}?</summary><p>{delta.fixed.length} findings fixed · {delta.new.length} new · {delta.stillOpen.length} still open · {delta.missing.length} no longer included</p><p>Comparison uses captured records, excluding fix previews. Missing records do not count as confirmed fixes.</p><ul>{delta.fixed.map(id=><li key={id}>Fixed: {current.findings[id].title}</li>)}{delta.new.map(id=><li key={id}>New: {current.findings[id].title}</li>)}{delta.missing.map(id=><li key={id}>No longer included: {previous!.findings[id].title}</li>)}</ul></details>}
  </section>;
}
