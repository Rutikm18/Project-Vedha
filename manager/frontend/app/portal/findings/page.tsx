"use client";

import { FindingsWorkspace } from "../../findings/page";

/** Customer route adapter: the manager-owned workspace supplies all UI/UX. */
export default function PortalFindingsPage() {
  return <FindingsWorkspace surface="portal" />;
}
