"use client";

import { useState } from "react";
import { ChevronDown, Layers, RefreshCw, Search } from "lucide-react";
import type { EnvironmentOptions } from "../../lib/environment-assessments";

export function EnvironmentScopeSelector({options,selected,pending,loading,onChange,onAnalyze}:{
  options:EnvironmentOptions;selected:string[];pending:boolean;loading:boolean;
  onChange:(ids:string[])=>void;onAnalyze:()=>void;
}) {
  const [expanded,setExpanded]=useState(false);
  const [search,setSearch]=useState("");
  const names=options.items.filter(item=>selected.includes(item.id)).map(item=>item.name);
  const shown=options.items.filter(item=>item.name.toLocaleLowerCase().includes(search.trim().toLocaleLowerCase()));
  return <section className="environment-scope" aria-label="Assessment scope">
    <div className="environment-scope-bar">
      <div className="environment-scope-identity"><span>Assessment scope</span><button type="button" className="btn btn-secondary" aria-expanded={expanded} aria-controls="environment-scope-editor" onClick={()=>setExpanded(!expanded)}><Layers size={15} aria-hidden="true"/>{selected.length?`${selected.length} selected`:"Choose assessments"}<ChevronDown size={14} aria-hidden="true"/></button><span className="environment-scope-names" title={names.join("; ")}>{names[0]}{names.length>1?` + ${names.length-1} more`:""}</span></div>
      <button type="button" className="btn btn-primary" disabled={pending||loading||!selected.length||!options.can_compute} onClick={()=>{onAnalyze();setExpanded(false);}}><RefreshCw size={15} aria-hidden="true"/>{pending?"Analyzing selection…":"Analyze selection"}</button>
    </div>
    {!options.items.length&&<p className="environment-scope-permission">No authorized assessments are enabled for this pilot.</p>}
    {!options.can_compute&&<p className="environment-scope-permission">Your role can review captured results. Creating a new analysis is unavailable.</p>}
    <div id="environment-scope-editor" className="environment-scope-editor" hidden={!expanded}>
      <div className="environment-scope-editor-heading"><label><Search size={15} aria-hidden="true"/><span className="sr-only">Search assessments</span><input type="search" placeholder="Search assessments" value={search} disabled={pending} onChange={e=>setSearch(e.target.value)}/></label><span>{selected.length} of 20 selected</span></div>
      <fieldset disabled={pending}><legend className="sr-only">Engagement selection</legend>{shown.map(item=><label key={item.id}><input type="checkbox" checked={selected.includes(item.id)} disabled={!selected.includes(item.id)&&selected.length>=20} onChange={e=>onChange(e.target.checked?[...selected,item.id]:selected.filter(id=>id!==item.id))}/><span>{item.name}</span></label>)}</fieldset>
      {!shown.length&&<p>{options.items.length?"No assessments match your search. Your selection is unchanged.":"No authorized engagements are enabled for this pilot."}</p>}
      {options.truncated&&<p>Showing the first 200 enabled assessments.</p>}
      <p>Choose one or several assessments. Findings retain their original system and engagement; selection does not establish a shared network.</p>
    </div>
  </section>;
}
