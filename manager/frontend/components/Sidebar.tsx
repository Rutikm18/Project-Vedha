"use client";

import React, { useState, useCallback, useRef, useSyncExternalStore } from "react";
import Link from "next/link";
import { useModalFocus } from "../hooks/useModalFocus";
import { usePathname } from "next/navigation";
import {
  Shield, Brain, AlertTriangle, FileText,
  Terminal, Briefcase, Settings, RadioTower, Users, X, Radar, Wrench,
} from "lucide-react";
import { VedhaMark } from "./brand/VedhaMark";

// Resolved at build time from the repo-root VERSION file (see next.config.mjs).
const APP_VERSION = process.env.NEXT_PUBLIC_APP_VERSION ?? "dev";

interface NavItem {
  icon: React.ComponentType<{ size?: number; color?: string }>;
  label: string;
  href: string;
  badge?: string;
}

const NAV_SECTIONS: { label: string; items: NavItem[] }[] = [
  {
    label: "OPERATIONS",
    items: [
      { icon: Shield,      label: "Dashboard",    href: "/"            },
      { icon: Briefcase,   label: "Engagements",  href: "/engagements" },
      { icon: Terminal,    label: "Scanner",      href: "/scan"        },
      { icon: Radar,       label: "VA Campaigns", href: "/campaign"    },
      { icon: RadioTower,  label: "Fleet",        href: "/fleet"       },
    ],
  },
  {
    label: "ANALYSIS",
    items: [
      { icon: Brain,         label: "AI Brain",   href: "/aibrain"  },
      { icon: AlertTriangle, label: "Findings",   href: "/findings" },
      { icon: Wrench,        label: "Remediation", href: "/remediation" },
    ],
  },
  {
    label: "MANAGEMENT",
    items: [
      { icon: Users,       label: "Customers",    href: "/customers" },
      { icon: FileText,    label: "Reports",      href: "/reports", badge: "BETA" },
      { icon: Settings,    label: "Settings",     href: "/settings" },
    ],
  },
];

const PORTAL_NAV_SECTIONS: { label: string; items: NavItem[] }[] = [
  {
    label: "OPERATIONS",
    items: [
      { icon: Shield,     label: "Dashboard",    href: "/portal" },
      { icon: Briefcase,  label: "Engagement",   href: "/portal/scope" },
      { icon: Terminal,   label: "Scanner",      href: "/portal/scans" },
      { icon: Radar,      label: "VA Campaigns", href: "/portal/campaign" },
      { icon: RadioTower, label: "Fleet",        href: "/portal/fleet" },
    ],
  },
  {
    label: "ANALYSIS",
    items: [
      { icon: Brain,         label: "AI Brain", href: "/portal/assistant" },
      { icon: AlertTriangle, label: "Findings", href: "/portal/findings" },
      { icon: Wrench,        label: "Remediation", href: "/portal/remediation" },
    ],
  },
  {
    label: "MANAGEMENT",
    items: [
      { icon: FileText, label: "Reports",  href: "/portal/reports", badge: "BETA" },
      { icon: Settings, label: "Settings", href: "/portal/settings" },
    ],
  },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  surface?: "manager" | "portal";
}

function subscribeToMobile(onChange: () => void) {
  const media = window.matchMedia("(max-width: 767px)");
  media.addEventListener("change", onChange);
  return () => media.removeEventListener("change", onChange);
}

export function Sidebar({ open, onClose, surface = "manager" }: SidebarProps) {
  const sidebarRef = useRef<HTMLElement>(null);
  const mobile = useSyncExternalStore(subscribeToMobile, () => window.matchMedia("(max-width: 767px)").matches, () => false);
  useModalFocus(sidebarRef, mobile && open, onClose, '[aria-controls="operator-navigation"]');
  const pathname = usePathname();
  const [hoveredHref, setHoveredHref] = useState<string | null>(null);
  const sections = surface === "portal" ? PORTAL_NAV_SECTIONS : NAV_SECTIONS;

  const handleHover = useCallback((href: string | null) => {
    setHoveredHref(href);
  }, []);


  return (
    <aside
      ref={sidebarRef}
      data-open={open}
      id="operator-navigation"
      tabIndex={-1}
      role={mobile && open ? "dialog" : undefined}
      aria-modal={mobile && open ? true : undefined}
      aria-label={mobile && open ? "Navigation" : undefined}
      inert={mobile && !open}
      className={[
        "vedha-sidebar fixed md:static z-50",
        "transition-transform duration-200 ease-in-out",
        open ? "translate-x-0" : "-translate-x-full md:translate-x-0",
      ].join(" ")}
      style={{
        width: 216,
        background: "var(--bg-panel)",
        borderRight: "0.5px solid var(--border-default)",
        boxShadow: "1px 0 0 rgba(15, 23, 42, 0.02)",
        display: "flex",
        flexDirection: "column",
        height: "100dvh",
        flexShrink: 0,
        overflowY: "auto",
      }}
    >
      {/* ── Logo ─── */}
      <div style={{
        padding: "20px 16px 14px",
        borderBottom: "0.5px solid var(--border-subtle)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexShrink: 0,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: "var(--accent-ghost)",
            border: "0.5px solid var(--border-accent)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            position: "relative",
            transition: "box-shadow 0.2s ease, transform 0.15s ease",
          }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = "0 0 12px var(--accent-glow)";
              e.currentTarget.style.transform = "scale(1.05)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = "none";
              e.currentTarget.style.transform = "scale(1)";
            }}
          >
            <span style={{ color: "var(--accent)", display: "flex" }}><VedhaMark size={18} title="Vedha" /></span>
          </div>
          <div>
            <div style={{
              fontFamily: "var(--font-display)",
              fontSize: 13,
              fontWeight: 700,
              color: "var(--text-primary)",
              letterSpacing: 2,
              lineHeight: 1,
            }}>
              VEDHA
            </div>
            <div style={{
              display: "flex",
              alignItems: "center",
              gap: 4,
              marginTop: 3,
            }}>
              <span style={{
                width: 4,
                height: 4,
                borderRadius: "50%",
                background: "var(--nominal-color)",
                display: "inline-block",
                animation: "pulse 2s ease-in-out infinite",
              }} />
              <span style={{
                fontSize: 9,
                color: "var(--text-muted)",
                fontWeight: 500,
                letterSpacing: 0.3,
              }}>
                v{APP_VERSION} Enterprise
              </span>
            </div>
          </div>
        </div>

        {/* Close button — mobile only */}
        <button
          className="vedha-sidebar-close md:hidden"
          onClick={onClose}
          aria-label="Close sidebar"
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            padding: 4,
            borderRadius: 6,
            color: "var(--text-muted)",
            transition: "color 0.15s, background 0.15s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "var(--bg-surface)";
            e.currentTarget.style.color = "var(--text-primary)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "none";
            e.currentTarget.style.color = "var(--text-muted)";
          }}
        >
          <X size={14} />
        </button>
      </div>

      {/* ── Navigation ─── */}
      <nav aria-label="Operator navigation" style={{ paddingTop: 10, flex: 1 }}>
        {sections.map((section, si) => (
          <div key={section.label} style={{ marginBottom: 6 }}>
            {/* Section label */}
            <div style={{
              padding: "5px 16px 4px",
              fontSize: 9,
              fontWeight: 700,
              color: "var(--text-faint)",
              letterSpacing: 1.4,
              textTransform: "uppercase" as const,
            }}>
              {section.label}
            </div>

            {section.items.map((item, ii) => {
              const Icon = item.icon;
              const isActive  = pathname === item.href || (item.href !== "/" && item.href !== "/portal" && pathname.startsWith(`${item.href}/`));
              const isHovered = hoveredHref === item.href;

              return (
                <Link
                  key={item.label}
                  href={item.href}
                  aria-current={isActive ? "page" : undefined}
                  onClick={onClose}
                  className="stagger-item"
                  style={{
                    animationDelay: `${(si * 4 + ii) * 25}ms`,
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    padding: "7px 10px 7px 14px",
                    margin: "1px 8px",
                    borderRadius: 7,
                    textDecoration: "none",
                    background: isActive
                      ? "var(--accent-ghost)"
                      : isHovered ? "var(--bg-surface)" : "transparent",
                    border: isActive ? "1px solid var(--border-accent)" : "1px solid transparent",
                    transition: "background 0.12s ease, border-color 0.12s ease, transform 0.12s var(--ease-out)",
                    transform: isHovered && !isActive ? "translateX(3px)" : "translateX(0)",
                  }}
                  onMouseEnter={() => handleHover(item.href)}
                  onMouseLeave={() => handleHover(null)}
                >
                  <div style={{
                    transition: "transform 0.15s var(--ease-out)",
                    transform: isHovered ? "scale(1.15)" : "scale(1)",
                    flexShrink: 0,
                    display: "flex",
                  }}>
                    <Icon
                      size={14}
                      color={isActive ? "var(--accent)" : isHovered ? "var(--text-primary)" : "var(--text-secondary)"}
                    />
                  </div>

                  <span style={{
                    fontSize: 13,
                    fontWeight: isActive ? 600 : 450,
                    color: isActive ? "var(--text-primary)" : isHovered ? "var(--text-primary)" : "var(--text-secondary)",
                    transition: "color 0.12s ease",
                    flex: 1,
                    letterSpacing: isActive ? "0.01em" : "0em",
                  }}>
                    {item.label}
                  </span>

                  {item.badge && (
                    <span style={{
                      padding: "2px 5px",
                      borderRadius: 4,
                      color: "var(--accent)",
                      background: "var(--accent-ghost)",
                      border: "0.5px solid var(--border-accent)",
                      fontSize: 7,
                      fontWeight: 800,
                      letterSpacing: 0.5,
                    }}>
                      {item.badge}
                    </span>
                  )}

                  {/* Active dot */}
                  {isActive && (
                    <span style={{
                      width: 4,
                      height: 4,
                      borderRadius: "50%",
                      background: "var(--accent)",
                      flexShrink: 0,
                      boxShadow: "0 0 5px var(--accent-glow)",
                    }} />
                  )}
                </Link>
              );
            })}
          </div>
        ))}
      </nav>

      {/* ── Footer ─── */}
      <div style={{
        padding: "12px 16px",
        borderTop: "0.5px solid var(--border-subtle)",
        flexShrink: 0,
      }}>
        <div style={{
          display: "flex",
          alignItems: "baseline",
          gap: 6,
          paddingLeft: 15,
          marginTop: 2,
        }}>
          <span style={{
            fontFamily: "var(--font-mono)",
            fontSize: 12,
            fontWeight: 700,
            color: "var(--text-secondary)",
            letterSpacing: 0.2,
          }}>
            v{APP_VERSION}
          </span>
          <span style={{
            fontSize: 9,
            fontWeight: 600,
            color: "var(--text-faint)",
            letterSpacing: 0.5,
            textTransform: "uppercase" as const,
          }}>
            Enterprise
          </span>
        </div>
      </div>
    </aside>
  );
}
