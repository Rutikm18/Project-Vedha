import type { ReactNode } from "react";

// The portal renders the same ReportsWorkspace as /reports, but route-scoped
// CSS only loads for the route that imports it. Without this, a customer who
// opens /portal/reports directly gets an unstyled findings register — and an
// export without the module's print rules.
import "../../../styles/report-finding.css";
import "../../../styles/report-document.css";
import "../../../styles/report-finding-elevated.css";

export const metadata = {
  title: "Report · Vedha",
  description: "Your VAPT deliverable — grounded in verified scanner evidence.",
};

export default function PortalReportsLayout({ children }: { children: ReactNode }) {
  return children;
}
