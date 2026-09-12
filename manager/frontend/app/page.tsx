import React from "react";
import { DashboardWorkspace } from "../components/dashboard/DashboardWorkspace";
import { OperatorConsoleProvider } from "../lib/console-source";

export default function Dashboard() {
  return (
    <OperatorConsoleProvider>
      <DashboardWorkspace />
    </OperatorConsoleProvider>
  );
}
