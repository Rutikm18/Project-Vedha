"use client";

import { EngagementWorkspace } from "../../engagements/[id]/page";
import { PortalShell } from "../../../components/portal/PortalShell";
import { SkeletonRows } from "../../../components/states/DataState";
import { usePortalEngagement } from "../../../lib/portal-client";

/** The customer route renders the exact manager engagement workspace. */
export default function PortalEngagementWorkspacePage() {
  const engagement = usePortalEngagement();

  if (!engagement.data) {
    return (
      <PortalShell title="Engagement" subtitle="Loading your assigned engagement…">
        <SkeletonRows rows={5} height={76} />
      </PortalShell>
    );
  }

  return <EngagementWorkspace id={engagement.data.id} surface="portal" />;
}
