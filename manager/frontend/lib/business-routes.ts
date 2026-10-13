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
  findingId?: string; engagementId?: string; lifecycle?: string; findingConfirmed?: boolean;
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
  if (nodes.size !== scan.nodes.length) throw new Error("Duplicate system identity in route data.");
  const ids = new Map<string, string>(), unique = new Map<string, BusinessEdge>();
  let omitted = 0;
  for (const e of scan.edges) {
    const identity = JSON.stringify([e.from, e.to, e.findingId]);
    if (ids.has(e.id) && ids.get(e.id) !== identity) throw new Error("Conflicting connection identity in route data.");
    ids.set(e.id, identity);
    if (!nodes.has(e.from) || !nodes.has(e.to) || !scan.findings[e.findingId] || !["confirmed", "theoretical"].includes(e.status)) { omitted++; continue; }
    const existing = unique.get(identity);
    if (!existing || (existing.status === "confirmed" && e.status === "theoretical")) unique.set(identity, e);
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
      paths.push({...path, id:path.edges.join("|")});
      if (paths.length >= maxPaths && stack.length) { truncated = true; break; }
      continue;
    }
    for (const e of [...(adjacency.get(here) ?? [])].reverse()) {
      if (!path.nodes.includes(e.to)) stack.push({nodes:[...path.nodes,e.to],edges:[...path.edges,e.id],confirmed:path.confirmed && e.status === "confirmed"});
    }
  }
  // Reachability does not depend on how much path enumeration could finish.
  const reached = new Set(scan.nodes.filter(n => n.type === "entry" || n.entry).map(n => n.id));
  const queue = [...reached];
  for (let i=0;i<queue.length;i++) for (const e of adjacency.get(queue[i]) ?? []) if (!reached.has(e.to)) { reached.add(e.to); queue.push(e.to); }
  return {paths,truncated,reachable:new Set([...crowns].filter(id=>reached.has(id)))};
}

export function analyse(scan: BusinessScan, options: {showTheoretical:boolean;maxPaths?:number;maxWork?:number}): RouteAnalysis {
  const maxPaths=options.maxPaths ?? 2000, maxWork=options.maxWork ?? 100000;
  if (!Number.isInteger(maxPaths) || maxPaths<1 || maxPaths>2000 || !Number.isInteger(maxWork) || maxWork<1 || maxWork>100000) throw new Error("Invalid route computation budget.");
  const normalized=validEdges(scan);
  const active=normalized.edges.filter(e=>!scan.findings[e.findingId].fixed && (options.showTheoretical || e.status==="confirmed"));
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
  const fixed=Object.keys(second.findings).filter(id=>second.findings[id].fixed && !first.findings[id]?.fixed && !!first.findings[id]);
  const added=Object.keys(second.findings).filter(id=>!first.findings[id]);
  const stillOpen=Object.keys(second.findings).filter(id=>!!first.findings[id] && !second.findings[id].fixed);
  const missing=Object.keys(first.findings).filter(id=>!second.findings[id]);
  return {fixed,new:added,stillOpen,missing};
}
