"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowLeft, ChevronLeft, ChevronRight, GitBranch, Layers } from "lucide-react";
import { assessmentRequest } from "../../lib/attack-assessments";
import { environmentBase, type EnvironmentHistory, type EnvironmentOptions, type EnvironmentResult, type EnvironmentSnapshot } from "../../lib/environment-assessments";
import { ApiError } from "../../lib/fetcher";
import { newId } from "../../lib/uuid";
import { PageShell } from "../PageShell";
import { EmptyState, ErrorState, SkeletonRows, Unauthorized } from "../states/DataState";
import { FindingChainExplorer } from "./FindingChainExplorer";
import { EnvironmentSystemChart } from "./EnvironmentSystemChart";
import { BusinessRoutePanel } from "./BusinessRoutePanel";
import { EnvironmentScopeSelector } from "./EnvironmentScopeSelector";
import "./attack-assessments.css";
import "@xyflow/react/dist/style.css";
import "./business-routes.css";

export function EnvironmentAttackWorkspace() {
  const [selection, setSelection] = useState<string[] | null>(null);
  const [requestId, setRequestId] = useState<string|null>(null);
  const [previous, setPrevious] = useState<EnvironmentResult|null>(null);
  const [page, setPage] = useState(1);
  const [findingId, setFindingId] = useState<string|null>(null);
  const [viewChoice,setView]=useState<"paths"|"findings"|null>(null);
  const tabsRef=useRef<HTMLDivElement>(null);
  const findingQueueRef=useRef<HTMLDivElement>(null);
  const reviewFindings=()=>{setView("findings");tabsRef.current?.querySelector<HTMLButtonElement>("#environment-findings-tab")?.focus();};
  const options = useQuery({queryKey:["environment-assessment-options"],queryFn:()=>assessmentRequest<EnvironmentOptions>(`${environmentBase}/options`),gcTime:0,staleTime:0,retry:false,refetchInterval:15000});
  const selected = selection ?? options.data?.items.slice(0,2).map(i=>i.id) ?? [];
  const scopeKey = [...selected].sort().join(",");
  const history = useQuery({queryKey:["environment-history",scopeKey],queryFn:()=>assessmentRequest<EnvironmentHistory>(`${environmentBase}?engagement_ids=${encodeURIComponent(scopeKey)}`),enabled:selected.length>0 && !options.error,gcTime:0,retry:false,refetchInterval:15000});
  const activeRequestId = requestId ?? history.data?.latest_request?.id;
  const resultQuery = useQuery({queryKey:["environment-assessment",activeRequestId,page],queryFn:()=>assessmentRequest<EnvironmentResult>(`${environmentBase}/${activeRequestId}?page=${page}&page_size=20`),enabled:!!activeRequestId && !options.error && !history.error,gcTime:0,retry:false,refetchInterval:q=>["queued","running"].includes(q.state.data?.snapshot.status ?? "")?2000:15000});
  const completedId = history.data?.last_completed?.id;
  const completedQuery = useQuery({queryKey:["environment-assessment",completedId,page],queryFn:()=>assessmentRequest<EnvironmentResult>(`${environmentBase}/${completedId}?page=${page}&page_size=20`),enabled:!!completedId && completedId!==activeRequestId && !options.error && !history.error,gcTime:0,retry:false,refetchInterval:15000});
  const result = resultQuery.data?.snapshot.status === "completed" ? resultQuery.data : completedQuery.data ?? previous;
  const view=viewChoice??(result?.route_graph?.edges.length&&!result.snapshot.requires_reassessment?"paths":"findings");
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
      {options.data&&<EnvironmentScopeSelector options={options.data} selected={selected} pending={pending} loading={loadingSaved} onChange={setSelection} onAnalyze={()=>compute.mutate(selected)}/>}
      <div className="environment-results">
        {compute.error && <p role="alert" className="assessment-notice">{compute.error.message}</p>}
        {pending && <p role="status" className="assessment-notice">Capturing a coherent selection and evaluating its evidence. {result?"The previous completed result remains below.":"Results will appear when computation finishes."}</p>}
        {resultQuery.data?.snapshot.status==="failed" && <p role="alert" className="assessment-notice">The latest analysis failed. {result?"The previous completed result is retained.":"Retry the selection."}</p>}
        {scopeChanged && <p role="status" className="assessment-notice">Selection changed. The result below belongs to the previous analyzed selection; analyze again to update it.</p>}
        {!result && loadingSaved ? <SkeletonRows rows={3} height={64}/> : !result ? <EmptyState title="Build your environment view" hint="Select engagements and analyze them. Recorded vulnerabilities will appear beside their systems; missing relationships remain visible."/> : <>
          {result.snapshot.requires_reassessment && <p role="status" className="assessment-notice">The accuracy checks have changed. Analyze this selection again to refresh it. Route counts are withheld until the captured view passes the current checks.</p>}
          <div className="environment-capture-context"><span>{result.snapshot.engagement_ids.length} assessments in this capture</span><span>{result.total} of {result.total_findings} findings included</span><span className="environment-coverage-state">Connection evidence incomplete</span></div>
          {result.compute==="truncated"&&<p className="assessment-notice" role="status">Only part of the selected records could be captured. Counts are incomplete.</p>}
          <div className="environment-view-tabs" role="tablist" aria-label="Environment investigation views" ref={tabsRef} onKeyDown={event=>{
            const next=event.key==="Home"?"paths":event.key==="End"?"findings":["ArrowLeft","ArrowRight"].includes(event.key)?view==="paths"?"findings":"paths":null;
            if(next){event.preventDefault();setView(next);event.currentTarget.querySelector<HTMLButtonElement>(`#environment-${next}-tab`)?.focus();}
          }}><button type="button" role="tab" id="environment-paths-tab" aria-controls="environment-paths-panel" aria-selected={view==="paths"} tabIndex={view==="paths"?0:-1} onClick={()=>setView("paths")}><GitBranch size={15} aria-hidden="true"/>Paths</button><button type="button" role="tab" id="environment-findings-tab" aria-controls="environment-findings-panel" aria-selected={view==="findings"} tabIndex={view==="findings"?0:-1} onClick={()=>setView("findings")}><Layers size={15} aria-hidden="true"/>Findings &amp; evidence <span>{result.total}</span></button></div>
          <div role="tabpanel" id="environment-paths-panel" aria-labelledby="environment-paths-tab" tabIndex={0} hidden={view!=="paths"}>
            {result.route_graph&&!result.snapshot.requires_reassessment?<BusinessRoutePanel current={result.route_graph} previous={baselineQuery.data?.route_graph} onReviewFindings={reviewFindings}/>:<EmptyState title="Refresh the path view" hint="Analyze this selection to capture connections under the current accuracy checks."/>}
          </div>
          <div role="tabpanel" id="environment-findings-panel" aria-labelledby="environment-findings-tab" tabIndex={0} hidden={view!=="findings"}>
            <div className="environment-evidence-context"><time dateTime={result.snapshot.effective_as_of}>Captured {new Date(result.snapshot.effective_as_of).toLocaleString()}</time><span>Analyze again after findings change. This view does not test live connectivity.</span></div>
            {result.items.length?<div className="environment-finding-workbench">
              <div className="environment-finding-queue" ref={findingQueueRef}><EnvironmentSystemChart result={result} selectedId={active?.finding_id??null} onSelect={item=>{setFindingId(item.finding_id);if((findingQueueRef.current?.closest(".environment-finding-workbench")?.clientWidth??0)<=600)document.getElementById("environment-selected-chain")?.scrollIntoView({block:"start",behavior:"instant"});}}/>
                <nav className="assessment-pagination" aria-label="Environment finding pages"><button type="button" className="btn btn-secondary" aria-label="Previous environment finding page" disabled={pending||loadingSaved||page===1} onClick={()=>changePage(page-1)}><ChevronLeft size={16}/></button><span>Page {result.page} of {Math.max(1,Math.ceil(result.total/20))}</span><button type="button" className="btn btn-secondary" aria-label="Next environment finding page" disabled={pending||loadingSaved||page*20>=result.total} onClick={()=>changePage(page+1)}><ChevronRight size={16}/></button></nav>
              </div>
              {active&&<section id="environment-selected-chain" className="environment-selected-chain"><header><button type="button" className="environment-back-to-findings" onClick={()=>{findingQueueRef.current?.scrollIntoView({block:"start",behavior:"instant"});findingQueueRef.current?.querySelector<HTMLButtonElement>('[aria-pressed="true"]')?.focus({preventScroll:true});}}><ArrowLeft size={14} aria-hidden="true"/>Back to findings</button><span>{active.engagement_name}</span><Link href={`/engagements/${encodeURIComponent(active.engagement_id)}/attack-paths?finding=${encodeURIComponent(active.finding_id)}`}>Open source assessment</Link></header><FindingChainExplorer key={`${result.snapshot.id}:${active.finding_id}`} finding={active} engagementId={active.engagement_id} compact/></section>}
            </div>:<EmptyState title="No findings were captured" hint="This result does not establish that the selected environment is safe."/>}
          </div>
          <details className="environment-view-help"><summary>About this captured view</summary><p>Findings retain their original engagement and system. Selecting assessments does not establish common ownership, connectivity or an attack. Source gaps stay visible; a finding verdict alone cannot confirm a connection.</p><Link href="/attack-paths/demo">View made-up example</Link></details>
        </>}
      </div>
    </div>}
  </PageShell>;
}
