"use client";

import { DashboardWorkspace } from "../../components/dashboard/DashboardWorkspace";
import { usePortalEngagement } from "../../lib/portal-client";

export default function PortalDashboardPage() {
  const engagement = usePortalEngagement();
  return (
    <DashboardWorkspace
      surface="portal"
      scopeLabel={engagement.data?.name}
    />
  );
}
