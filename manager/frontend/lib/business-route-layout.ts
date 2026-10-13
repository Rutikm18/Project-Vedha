import { graphlib, layout } from "@dagrejs/dagre";
import type { BusinessScan } from "./business-routes";

/** Dagre orders each semantic lane; fixed columns keep the business story stable. */
export function routeLayout(scan: Pick<BusinessScan, "nodes" | "edges">) {
  const crowns=new Set(scan.nodes.filter(n=>n.type==="crown").map(n=>n.id));
  const primary=(confirmedOnly:boolean)=>{
    const paths=scan.nodes.filter(n=>n.type==="entry"||n.entry).map(n=>[n.id]),visited=new Set(paths.map(p=>p[0]));
    for(let i=0;i<paths.length;i++){
      const path=paths[i],here=path[path.length-1];
      if(path.length>1&&crowns.has(here))return path;
      for(const edge of scan.edges)if(edge.from===here&&(!confirmedOnly||edge.status==="confirmed")&&!visited.has(edge.to)){visited.add(edge.to);paths.push([...path,edge.to]);}
    }
    return [];
  };
  // A topology-only primary route stays aligned, even while its fix is previewed.
  const preferred=new Set(primary(true).length?primary(true):primary(false));
  const graph = new graphlib.Graph({multigraph:true}).setGraph({rankdir:"LR",nodesep:32,ranksep:48}).setDefaultEdgeLabel(()=>({}));
  for (const node of scan.nodes) graph.setNode(node.id,{width:132,height:134});
  for (const edge of scan.edges) if(graph.hasNode(edge.from) && graph.hasNode(edge.to)) graph.setEdge(edge.from,edge.to,{},edge.id);
  layout(graph);
  const lanes=new Map<number,typeof scan.nodes>();
  for(const node of scan.nodes){const lane=node.column ?? (node.type==="entry"?0:node.type==="crown"?3:2);lanes.set(lane,[...(lanes.get(lane)??[]),node]);}
  const positions=new Map<string,{x:number;y:number}>();
  for(const [lane,nodes] of lanes){nodes.sort((a,b)=>Number(preferred.has(b.id))-Number(preferred.has(a.id))||(graph.node(a.id)?.y??0)-(graph.node(b.id)?.y??0)||a.id.localeCompare(b.id));nodes.forEach((node,i)=>positions.set(node.id,{x:lane*160,y:64+i*166}));}
  return positions;
}
