/**
 * Portal segment layout — a passthrough. Each portal page renders the canonical
 * <PageShell> through <PortalShell>, so manager and customer
 * surfaces share one renderer while retaining surface-specific navigation and
 * authentication. The login screen renders standalone.
 */
export default function PortalLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
