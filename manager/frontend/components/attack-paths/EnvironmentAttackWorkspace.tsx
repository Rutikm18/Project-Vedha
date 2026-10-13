"use client";

import { useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ChevronLeft, ChevronRight, GitBranch, Layers, RefreshCw } from "lucide-react";
import { assessmentRequest } from "../../lib/attack-assessments";
import { environmentBase, type EnvironmentHistory, type EnvironmentOptions, type EnvironmentResult, type EnvironmentSnapshot } from "../../lib/environment-assessments";
import { ApiError } from "../../lib/fetcher";
import { newId } from "../../lib/uuid";
import { PageShell } from "../PageShell";
import { EmptyState, ErrorState, SkeletonRows, Unauthorized } from "../states/DataState";
import { FindingChainExplorer } from "./FindingChainExplorer";
import { EnvironmentSystemChart } from "./EnvironmentSystemChart";
import { BusinessRoutePanel } from "./BusinessRoutePanel";
import "./attack-assessments.css";
import "@xyflow/react/dist/style.css";
import "./business-routes.css";

export function EnvironmentAttackWorkspace() {
  const [selection, setSelection] = useState<string[] | null>(null);
  const [requestId, setRequestId] = useState<string|null>(null);
  const [previous, setPrevious] = useState<EnvironmentResult|null>(null);
  const [page, setPage] = useState(1);
  const [findingId, setFindingId] = useState<string|null>(null);
  const options = useQuery({queryKey:["environment-assessment-options"],queryFn:()=>assessmentRequest<EnvironmentOptions>(`${environmentBase}/options`),gcTime:0,staleTime:0,retry:false,refetchInterval:15000});
  const selected = selection ?? options.data?.items.slice(0,2).map(i=>i.id) ?? [];
  const scopeKey = [...selected].sort().join(",");
  const history = useQuery({queryKey:["environment-history",scopeKey],queryFn:()=>assessmentRequest<EnvironmentHistory>(`${environmentBase}?engagement_ids=${encodeURIComponent(scopeKey)}`),enabled:selected.length>0 && !options.error,gcTime:0,retry:false,refetchInterval:15000});
  const activeRequestId = requestId ?? history.data?.latest_request?.id;
  const resultQuery = useQuery({queryKey:["environment-assessment",activeRequestId,page],queryFn:()=>assessmentRequest<EnvironmentResult>(`${environmentBase}/${activeRequestId}?page=${page}&page_size=20`),enabled:!!activeRequestId && !options.error && !history.error,gcTime:0,retry:false,refetchInterval:q=>["queued","running"].includes(q.state.data?.snapshot.status ?? "")?2000:15000});
  const completedId = history.data?.last_completed?.id;
  const completedQuery = useQuery({queryKey:["environment-assessment",completedId,page],queryFn:()=>assessmentRequest<EnvironmentResult>(`${environmentBase}/${completedId}?page=${page}&page_size=20`),enabled:!!completedId && completedId!==activeRequestId && !options.error && !history.error,gcTime:0,retry:false,refetchInterval:15000});
  const result = resultQuery.data?.snapshot.status === "completed" ? resultQuery.data : completedQuery.data ?? previous;
  const baselineId=[...(result?.snapshot.engagement_ids??[])].sort().join(",")===scopeKey?history.data?.completed_history?.find(row=>row.id!==result?.snapshot.id&&!row.requires_reassessment)?.id:undefined;
  const baselineQuery=useQuery({queryKey:["environment-route-baseline",baselineId],queryFn:()=>assessmentRequest<EnvironmentResult>(`${environmentBase}/${baselineId}?page_size=1`),enabled:!!result?.route_graph&&!!baselineId&&!options.error&&!history.error,gcTime:0,retry:false,refetchInterval:15000});
  const compute = useMutation({mutationFn:(ids:string[])=>assessmentRequest<EnvironmentSnapshot>(environmentBase,{method:"POST",headers:{"Content-Type":"application/json","Idempotency-Key":newId()},body:JSON.stringify({engagement_ids:ids})}),onSuccess:row=>{setPrevious(result ?? null);setRequestId(row.id);setPage(1);setFindingId(null);void history.refetch();}});
  const error=options.error ?? history.error ?? resultQuery.error ?? completedQuery.error ?? baselineQuery.error;
  const denied=error instanceof ApiError && [401,403,404].includes(error.status);
  const loadingSaved=(selected.length>0 && history.isPending) || (!!activeRequestId && resultQuery.isPending) || (!!completedId && completedId!==activeRequestId && completedQuery.isPending);
  const pending=compute.isPending || ["queued","running"].includes(resultQuery.data?.snapshot.status ?? "");
  const active=result?.items.find(i=>i.finding_id===findingId) ?? result?.items[0];
  const scopeChanged=!!result && [...selected].sort().join()!==[...result.snapshot.engagement_ids].sort().join();
  const changePage=(next:number)=>{setPrevious(result ?? null);setPage(next);setFindingId(null);};
  return <PageShell title="Attack paths" subtitle="Investigate findings across selected assessments" hideRefresh>
    <nav className="attack-path-modes" aria-label="Attack-path scope"><Link href="/attack-paths" aria-current="page"><GitBranch size={15} aria-hidden="true" />Environment chains</Link><Link href="/attack-paths?mode=overview"><Layers size={15} aria-hidden="true" />Engagement overview</Link></nav>
    {denied ? error.status===401 ? <Unauthorized/> : <EmptyState title="Environment analysis is not available" hint="Your workspace or role is not enabled for this pilot."/> : error ? <ErrorState title="Could not load environment analysis" detail={error.message} onRetry={()=>{void options.refetch();void history.refetch();void resultQuery.refetch();void completedQuery.refetch();}}/> : options.isPending ? <SkeletonRows rows={4} height={60}/> : <div className="environment-workspace">
      <aside className="environment-selector" aria-label="Select engagements"><h2>Select assessments</h2><p>Choose up to 20 engagements to review their findings together.</p>
        <fieldset disabled={pending}><legend className="sr-only">Engagement selection</legend>{options.data?.items.map(item=><label key={item.id}><input type="checkbox" checked={selected.includes(item.id)} disabled={!selected.includes(item.id)&&selected.length>=20} onChange={e=>setSelection(e.target.checked?[...selected,item.id]:selected.filter(id=>id!==item.id))}/><span>{item.name}</span></label>)}</fieldset>
        {!options.data?.items.length && <p>No authorized engagements are enabled for this pilot.</p>}
        {options.data?.truncated && <p>Showing the first 200 enabled engagements.</p>}
        <button type="button" className="btn btn-primary" disabled={pending||loadingSaved||selected.length===0||!options.data?.can_compute} onClick={()=>compute.mutate(selected)}><RefreshCw size={15} aria-hidden="true" />{pending?"Analyzing selection…":"Analyze selection"}</button><span className="environment-selection-count">{selected.length} selected</span>
        <details><summary>How assessments are combined</summary><p>Findings retain their original engagement and system identity. Selecting assessments does not establish common customer ownership, connectivity or an attack.</p></details>
      </aside>
      <div className="environment-results">
        <header className="assessment-heading"><div><h2>Your environment view</h2><p>Review the selected systems and the findings behind their possible connections.</p></div><Link href="/attack-paths/demo">View made-up example</Link></header>
        {compute.error && <p role="alert" className="assessment-notice">{compute.error.message}</p>}
        {pending && <p role="status" className="assessment-notice">Capturing a coherent selection and evaluating its evidence. {result?"The previous completed result remains below.":"Results will appear when computation finishes."}</p>}
        {resultQuery.data?.snapshot.status==="failed" && <p role="alert" className="assessment-notice">The latest analysis failed. {result?"The previous completed result is retained.":"Retry the selection."}</p>}
        {scopeChanged && <p role="status" className="assessment-notice">Selection changed. The result below belongs to the previous analyzed selection; analyze again to update it.</p>}
        {!result && loadingSaved ? <SkeletonRows rows={3} height={64}/> : !result ? <EmptyState title="Build your environment view" hint="Select engagements and analyze them. Recorded vulnerabilities will appear beside their systems; missing relationships remain visible."/> : <>
          {result.snapshot.requires_reassessment && <p role="status" className="assessment-notice">The analysis model has changed. Analyze this selection again to use the current model.</p>}
          <div className="assessment-context"><span>{result.snapshot.engagement_ids.length} engagements analyzed</span><span>{result.total} of {result.total_findings} findings included</span><span>Evidence coverage: incomplete</span><span>Snapshot: {new Date(result.snapshot.effective_as_of).toLocaleString()}</span></div>
          <p className="assessment-qualification">{result.compute==="truncated"?"Only part of the selected records could be included. ":""}Findings show where weaknesses were recorded. Cross-system attack paths remain unconfirmed until their connection evidence is available.</p>
          {result.route_graph&&<BusinessRoutePanel current={result.route_graph} previous={baselineQuery.data?.route_graph}/>}
          {result.items.length ? <><EnvironmentSystemChart result={result} selectedId={active?.finding_id ?? null} onSelect={item=>{setFindingId(item.finding_id);document.getElementById("environment-selected-chain")?.scrollIntoView({block:"start",behavior:"instant"});}}/>
            <nav className="assessment-pagination" aria-label="Environment finding pages"><button type="button" className="btn btn-secondary" aria-label="Previous environment finding page" disabled={pending||loadingSaved||page===1} onClick={()=>changePage(page-1)}><ChevronLeft size={16}/></button><span>Page {result.page} of {Math.max(1,Math.ceil(result.total/20))}</span><button type="button" className="btn btn-secondary" aria-label="Next environment finding page" disabled={pending||loadingSaved||page*20>=result.total} onClick={()=>changePage(page+1)}><ChevronRight size={16}/></button></nav>
            {active && <section id="environment-selected-chain" className="environment-selected-chain"><header><h3>Selected finding chain</h3><span>{active.engagement_name}</span><Link href={`/engagements/${encodeURIComponent(active.engagement_id)}/attack-paths?finding=${encodeURIComponent(active.finding_id)}`}>Open source assessment</Link></header><FindingChainExplorer key={`${result.snapshot.id}:${active.finding_id}`} finding={active} engagementId={active.engagement_id} stacked/></section>}</> : <EmptyState title="No findings were captured" hint="This result does not establish that the selected environment is safe."/>}
        </>}
      </div>
    </div>}
  </PageShell>;
}
