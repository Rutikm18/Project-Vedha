"use client";

import React, { useState, useCallback } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Shield, Brain, AlertTriangle, FileText,
  Terminal, Briefcase, Settings, X,
} from "lucide-react";

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
    ],
  },
  {
    label: "ANALYSIS",
    items: [
      { icon: Brain,         label: "AI Brain",   href: "/aibrain"  },
      { icon: AlertTriangle, label: "Findings",   href: "/findings" },
    ],
  },
  {
    label: "MANAGEMENT",
    items: [
      { icon: FileText,    label: "Reports",      href: "/reports", badge: "BETA" },
      { icon: Settings,    label: "Settings",     href: "/settings" },
    ],
  },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();
  const [hoveredHref, setHoveredHref] = useState<string | null>(null);

  const handleHover = useCallback((href: string | null) => {
    setHoveredHref(href);
  }, []);

  return (
    <aside
      className={[
        "fixed md:static z-50",
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
        height: "100vh",
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
            <Shield size={15} color="var(--accent)" strokeWidth={2} />
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
                background: "var(--accent)",
                display: "inline-block",
                animation: "pulse 2s ease-in-out infinite",
              }} />
              <span style={{
                fontSize: 9,
                color: "var(--text-muted)",
                fontWeight: 500,
                letterSpacing: 0.3,
              }}>
                v1.0 Enterprise
              </span>
            </div>
          </div>
        </div>

        {/* Close button — mobile only */}
        <button
          className="md:hidden"
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
      <nav style={{ paddingTop: 10, flex: 1 }}>
        {NAV_SECTIONS.map((section, si) => (
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
              const isActive  = pathname === item.href;
              const isHovered = hoveredHref === item.href;

              return (
                <Link
                  key={item.label}
                  href={item.href}
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
                    borderLeft: isActive ? "2px solid var(--accent)" : "2px solid transparent",
                    transition: "background 0.12s ease, border-color 0.12s ease, transform 0.12s var(--ease-spring), padding-left 0.12s ease",
                    transform: isHovered && !isActive ? "translateX(3px)" : "translateX(0)",
                  }}
                  onMouseEnter={() => handleHover(item.href)}
                  onMouseLeave={() => handleHover(null)}
                >
                  <div style={{
                    transition: "transform 0.15s var(--ease-spring)",
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
        <div style={{ display: "flex", alignItems: "center", gap: 7, marginBottom: 3 }}>
          <div className="status-dot" style={{ width: 8, height: 8 }}>
            <span className="status-dot-ring" style={{ background: "var(--accent-pulse)" }} />
            <span className="status-dot-core" style={{ background: "var(--accent)", width: 6, height: 6 }} />
          </div>
          <span style={{
            fontSize: 11,
            fontWeight: 600,
            color: "var(--accent)",
          }}>
            System Nominal
          </span>
        </div>
        <div style={{
          fontFamily: "var(--font-mono)",
          fontSize: 9,
          color: "var(--text-muted)",
          paddingLeft: 15,
        }}>
          VEDHA v1.0.0 · Enterprise
        </div>
      </div>
    </aside>
  );
}
