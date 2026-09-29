"use client";

import React from "react";
import { PageShell } from "../PageShell";
import { PlanStrip } from "./PlanStrip";

/**
 * Customer pages intentionally use the canonical product shell. This wrapper
 * supplies only the authentication/navigation surface and the customer's plan
 * strip; all visual structure, typography, spacing, responsiveness, and
 * controls come from PageShell.
 */
export function PortalShell(
  props: Omit<React.ComponentProps<typeof PageShell>, "surface">,
) {
  const { children, ...rest } = props;
  return (
    <PageShell {...rest} surface="portal">
      <PlanStrip />
      {children}
    </PageShell>
  );
}
