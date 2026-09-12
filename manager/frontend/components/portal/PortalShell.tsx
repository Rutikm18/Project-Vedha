"use client";

import React from "react";
import { PageShell } from "../PageShell";

/**
 * Customer pages intentionally use the canonical product shell. This wrapper
 * supplies only the authentication/navigation surface; all visual structure,
 * typography, spacing, responsiveness, and controls come from PageShell.
 */
export function PortalShell(
  props: Omit<React.ComponentProps<typeof PageShell>, "surface">,
) {
  return <PageShell {...props} surface="portal" />;
}
