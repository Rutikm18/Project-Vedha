"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Shield, LayoutDashboard, Bug, FileText, Radar, LogOut } from "lucide-react";

const NAV = [
  { href: "/portal", label: "Overview", icon: LayoutDashboard },
  { href: "/portal/findings", label: "Findings", icon: Bug },
  { href: "/portal/reports", label: "Reports", icon: FileText },
  { href: "/portal/scans", label: "Scans", icon: Radar },
];

export default function PortalLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  // The login screen has no shell (customers never see operator chrome anyway).
  if (pathname === "/portal/login") return <>{children}</>;

  async function logout() {
    await fetch("/api/portal/logout", { method: "POST" });
    router.push("/portal/login");
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2 font-semibold">
            <Shield className="h-5 w-5 text-indigo-600" />
            <span>Vedha</span>
            <span className="text-slate-400">Customer Portal</span>
          </div>
          <nav className="flex items-center gap-1">
            {NAV.map((n) => {
              const Icon = n.icon;
              const active = pathname === n.href;
              return (
                <Link
                  key={n.href}
                  href={n.href}
                  className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                    active
                      ? "bg-indigo-50 text-indigo-700"
                      : "text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {n.label}
                </Link>
              );
            })}
            <button
              onClick={logout}
              className="ml-2 flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm text-slate-500 hover:bg-slate-100"
            >
              <LogOut className="h-4 w-4" />
              Sign out
            </button>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6">{children}</main>
    </div>
  );
}
