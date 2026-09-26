"use client";

import { Suspense } from "react";
import { RemediationWorkspace } from "../../../components/remediation/RemediationWorkspace";

export default function PortalRemediationPage() {
  return <Suspense fallback={null}><RemediationWorkspace surface="portal" /></Suspense>;
}
