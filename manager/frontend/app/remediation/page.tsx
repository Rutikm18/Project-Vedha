"use client";

import { Suspense } from "react";
import { RemediationWorkspace } from "../../components/remediation/RemediationWorkspace";

export default function RemediationPage() {
  // useSearchParams (engagement/fix deep links) needs a Suspense boundary.
  return <Suspense fallback={null}><RemediationWorkspace surface="manager" /></Suspense>;
}
