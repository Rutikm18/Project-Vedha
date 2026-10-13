"use client";

import Link from "next/link";
import { PageShell } from "../../../components/PageShell";
import { BusinessRoutePanel } from "../../../components/attack-paths/BusinessRoutePanel";
import fixture from "../../../lib/demo-business-routes.json";
import type { BusinessScan } from "../../../lib/business-routes";
import "@xyflow/react/dist/style.css";
import "../../../components/attack-paths/business-routes.css";

const scans=fixture.scans as BusinessScan[];
export default function RouteDemonstration(){
  return <PageShell title="Route-map example" subtitle="Made-up data for explaining the interface" hideRefresh>
    <div style={{padding:"var(--space-5)",maxWidth:1600,margin:"0 auto",width:"100%"}}>
      <Link href="/attack-paths" className="assessment-link">Return to actual environment</Link>
      <BusinessRoutePanel current={scans[1]} previous={scans[0]}/>
    </div>
  </PageShell>;
}
