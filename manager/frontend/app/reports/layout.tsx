import type { ReactNode } from "react";

// Route-scoped report styling. Imported here (a nested layout) so it always
// lands AFTER the root layout's globals.css in the cascade — which is what the
// module's print overrides rely on.
import "../../styles/report-finding.css";

export const metadata = {
  title: "Report · Vedha",
  description: "Professional VAPT deliverable — grounded in verified scanner evidence.",
};

export default function ReportsLayout({ children }: { children: ReactNode }) {
  return children;
}
