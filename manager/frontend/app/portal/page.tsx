"use client";

import React from "react";
import { DashboardWorkspace } from "../../components/dashboard/DashboardWorkspace";
import { PortalConsoleProvider } from "../../lib/console-source";
import { usePortalEngagement } from "../../lib/portal-client";

export default function PortalOverview() {
  const engagement = usePortalEngagement();
  return (
    <PortalConsoleProvider scopeLabel={engagement.data?.name ?? "Your engagement"}>
      <DashboardWorkspace />
    </PortalConsoleProvider>
  );
}
