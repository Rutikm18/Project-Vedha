/** Pure bounded route analysis. A modelled connection is never a confirmed test. */
export type RouteStatus = "confirmed" | "theoretical";
export interface BusinessNode {
  id: string; label: string; type: "entry" | "asset" | "crown";
  column?: 0 | 1 | 2 | 3; entry?: boolean;
  assetId?: string; engagementId?: string; engagementName?: string;
}
export interface BusinessEdge {
  id: string; from: string; to: string; findingId: string; status: RouteStatus;
  basis?: string; sourcePathId?: string; stale?: boolean;
}
export interface BusinessFinding {
  id: string; title: string; severity: "critical" | "high" | "medium" | "low" | "info";
  plainReason: string; fixSteps: string[]; fixed: boolean;
  findingId?: string; engagementId?: string; assetId?: string; lifecycle?: string; findingConfirmed?: boolean;
  verificationState?: string | null; observedAt?: string | null; resolutionRunId?: string | null;
}

export function withdrawnFinding(finding: BusinessFinding): boolean {
  return finding.lifecycle === "fp" || finding.verificationState === "contradicted";
}
export interface BusinessScan {
  id: string; takenAt: string; grade: string | null;
  nodes: BusinessNode[]; edges: BusinessEdge[]; findings: Record<string, BusinessFinding>;
  source?: "stored_models" | "demo"; coverage?: string; version?: string;
  engagementIds?: string[]; truncated?: boolean; omittedConnections?: number; capturedModels?: number;
}
export interface BusinessPath { id: string; nodes: string[]; edges: string[]; confirmed: boolean; }
export interface RouteAnalysis {
  paths: BusinessPath[]; totalPaths: number; confirmedPaths: number;
  reachableCrowns: Set<string>; edgeIds: Set<string>; findingIds: Set<string>;
  truncated: boolean; confirmedTruncated: boolean; omittedEdges: number;
}

export function validEdges(scan: BusinessScan): { edges: BusinessEdge[]; omitted: number } {
  if (scan.nodes.length > 300 || scan.edges.length > 600) throw new Error("Route view exceeds 300 systems or 600 connections.");
  const nodes = new Set(scan.nodes.map(n => n.id));
  const nodeMap = new Map(scan.nodes.map(n => [n.id,n]));
  if (nodes.size !== scan.nodes.length) throw new Error("Duplicate system identity in route data.");
  const ids = new Map<string, string>(), unique = new Map<string, BusinessEdge>();
  let omitted = 0;
  for (const e of scan.edges) {
    const identity = JSON.stringify([e.from, e.to, e.findingId]);
    if (ids.has(e.id) && ids.get(e.id) !== identity) throw new Error("Conflicting connection identity in route data.");
    ids.set(e.id, identity);
    const finding=scan.findings[e.findingId], from=nodeMap.get(e.from), to=nodeMap.get(e.to);
    if (!from || !to || !finding || finding.id!==e.findingId || withdrawnFinding(finding) || !["confirmed", "theoretical"].includes(e.status)) { omitted++; continue; }
    // Stored-model payloads cannot authorize foreign bindings or promote proof.
    if (scan.source==="stored_models" && (!finding.findingId || !finding.engagementId || !finding.assetId || !from.assetId || !to.assetId ||
      from.engagementId!==finding.engagementId || to.engagementId!==finding.engagementId || to.assetId!==finding.assetId ||
      e.findingId!==`${finding.engagementId}:${finding.findingId}` || from.id!==`${from.engagementId}:${from.assetId}` || to.id!==`${to.engagementId}:${to.assetId}`)) { omitted++; continue; }
    const candidate=scan.source==="stored_models"?{...e,status:"theoretical" as const}:e;
    const existing = unique.get(identity);
    if (!existing) unique.set(identity,candidate);
    else unique.set(identity,{...existing,status:existing.status==="theoretical"||candidate.status==="theoretical"?"theoretical":"confirmed",stale:!!existing.stale||!!candidate.stale});
  }
  return { edges: [...unique.values()].sort((a,b) => a.id.localeCompare(b.id)), omitted };
}

function enumerate(scan: BusinessScan, edges: BusinessEdge[], maxPaths: number, maxWork: number) {
  const crowns = new Set(scan.nodes.filter(n => n.type === "crown").map(n => n.id));
  const adjacency = new Map<string, BusinessEdge[]>();
  for (const e of edges) adjacency.set(e.from, [...(adjacency.get(e.from) ?? []), e]);
  const paths: BusinessPath[] = [];
  let work = 0, truncated = false;
  const stack = scan.nodes.filter(n => n.type === "entry" || n.entry).reverse().map(n => ({nodes:[n.id], edges:[] as string[], confirmed:true}));
  while (stack.length) {
    if (++work > maxWork) { truncated = true; break; }
    const path = stack.pop()!;
    const here = path.nodes[path.nodes.length-1];
    // A zero-hop entry/crown is an exposure annotation, not a confirmed route.
    if (crowns.has(here) && path.edges.length) {
      if (paths.length >= maxPaths) { truncated = true; break; }
      paths.push({...path, id:path.edges.join("|")});
      if (paths.length >= maxPaths && stack.length) { truncated = true; break; }
      // A critical asset can itself lead to another critical asset.
    }
    for (const e of [...(adjacency.get(here) ?? [])].reverse()) {
      if (!path.nodes.includes(e.to)) stack.push({nodes:[...path.nodes,e.to],edges:[...path.edges,e.id],confirmed:path.confirmed && e.status === "confirmed"});
    }
  }
  // Reachability does not depend on how much path enumeration could finish.
  const reachable = new Set<string>();
  // Per-entry traversal requires a non-zero simple route, including for entry/crowns.
  // Bounded by 300 entries × (300 systems + 600 connections), independent of enumeration.
  for (const start of scan.nodes.filter(n => n.type === "entry" || n.entry)) {
    const reached=new Set([start.id]),queue=[start.id];
    for (let i=0;i<queue.length;i++) for (const e of adjacency.get(queue[i]) ?? []) if (!reached.has(e.to)) {
      reached.add(e.to);queue.push(e.to);if(crowns.has(e.to))reachable.add(e.to);
    }
  }
  return {paths,truncated,reachable};
}

export function analyse(scan: BusinessScan, options: {showTheoretical:boolean;maxPaths?:number;maxWork?:number}): RouteAnalysis {
  const maxPaths=options.maxPaths ?? 2000, maxWork=options.maxWork ?? 100000;
  if (!Number.isInteger(maxPaths) || maxPaths<1 || maxPaths>2000 || !Number.isInteger(maxWork) || maxWork<1 || maxWork>100000) throw new Error("Invalid route computation budget.");
  const normalized=validEdges(scan);
  const active=normalized.edges.filter(e=>!e.stale && !scan.findings[e.findingId].fixed && (options.showTheoretical || e.status==="confirmed"));
  const all=enumerate(scan,active,maxPaths,maxWork);
  const confirmed=options.showTheoretical ? enumerate(scan,active.filter(e=>e.status==="confirmed"),maxPaths,maxWork) : all;
  // Use the enumerated simple-path union: cycle-only detours must never be shown as route edges.
  const edgeIds=new Set(all.paths.flatMap(p=>p.edges));
  return {paths:all.paths,totalPaths:all.paths.length,confirmedPaths:confirmed.paths.length,reachableCrowns:all.reachable,
    edgeIds,findingIds:new Set(active.filter(e=>edgeIds.has(e.id)).map(e=>e.findingId)),
    truncated:all.truncated,confirmedTruncated:confirmed.truncated,omittedEdges:normalized.omitted};
}

export function previewFix(scan: BusinessScan, findingId: string, fixed=true): BusinessScan {
  if (!scan.findings[findingId]) throw new Error("Finding is not in this snapshot.");
  return {...scan,findings:{...scan.findings,[findingId]:{...scan.findings[findingId],fixed}}};
}

export function compare(first: BusinessScan, second: BusinessScan) {
  if ([...(first.engagementIds??[])].sort().join() !== [...(second.engagementIds??[])].sort().join() || first.version!==second.version) throw new Error("Compare snapshots of the same scope and route model.");
  const fixed=Object.keys(second.findings).filter(id=>second.findings[id].fixed && !withdrawnFinding(second.findings[id]) && !first.findings[id]?.fixed && !!first.findings[id]);
  const added=Object.keys(second.findings).filter(id=>!first.findings[id]&&!withdrawnFinding(second.findings[id]));
  const stillOpen=Object.keys(second.findings).filter(id=>!!first.findings[id] && !second.findings[id].fixed && !withdrawnFinding(second.findings[id]) && second.findings[id].lifecycle!=="remediated");
  const awaitingConfirmation=Object.keys(second.findings).filter(id=>second.findings[id].lifecycle==="remediated"&&!second.findings[id].fixed&&!withdrawnFinding(second.findings[id]));
  const dismissed=Object.keys(second.findings).filter(id=>withdrawnFinding(second.findings[id]));
  const missing=Object.keys(first.findings).filter(id=>!second.findings[id]);
  return {fixed,new:added,stillOpen,awaitingConfirmation,dismissed,missing};
}
