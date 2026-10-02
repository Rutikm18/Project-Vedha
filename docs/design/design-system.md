# Vedha Design System

**Version:** 10.0 "SIGNAL"  
**Source files:** `manager/frontend/app/globals.css`, `manager/frontend/styles/console-tokens.css`

**Philosophy:** Quiet operational surfaces with colour reserved for meaning. Light mode default; dark mode preserves the same semantic roles.

---

## Typography

| Role | CSS Variable | Font Stack |
|---|---|---|
| Display / headings | `--font-display` | `-apple-system, BlinkMacSystemFont, "Segoe UI Variable Display", "Segoe UI", sans-serif` |
| Body / UI | `--font-body` / `--font-ui` | `-apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI", sans-serif` |
| Code / data / evidence | `--font-mono` | `ui-monospace, "SFMono-Regular", "Cascadia Code", "Roboto Mono", Consolas, monospace` |

No external webfonts — relies entirely on system UI (SF Pro on Mac, Segoe UI on Windows). This keeps load times fast and renders natively on every platform.

### Type Scale

| Token | Size | Usage |
|---|---|---|
| `--fs-display-xl` | `clamp(38px, 7vw, 52px)` | Ledger headline only |
| `--fs-display-l` | `clamp(30px, 5vw, 38px)` | Posture grade only |
| `--fs-display-m` | `26px` | Metric readouts |
| `--fs-display-s` | `24px` | SLA state counts |
| `--fs-body` | `13px` | Default body text |
| `--fs-body-s` | `12px` | Dense body, floor size |
| `--fs-label` | `11px` | Eyebrows, table headers (uppercase) |

---

## Colours — Light Mode (default)

### Backgrounds

| Role | Token | Hex |
|---|---|---|
| Page canvas | `--bg-root` / `--bg-app` | `#F3F6FA` |
| Panel / card surface | `--bg-panel` / `--bg-card` | `#FFFFFF` |
| Inset surface | `--bg-surface` | `#F8FAFC` |
| Hover state | `--bg-hover` | `#EDF2F7` |
| Active state | `--bg-active` | `#E2EAF3` |
| Elevated surface | `--bg-elevated` | `#E8EEF5` |
| Sidebar | `--bg-sidebar` | `#FFFFFF` |

### Borders

| Role | Token | Hex |
|---|---|---|
| Subtle (default hairline) | `--border-subtle` | `#DCE3EC` |
| Default | `--border-default` | `#C5D0DE` |
| Strong (emphasis) | `--border-strong` | `#8EA0B5` |
| Accent tint | `--border-accent` | `rgba(29, 78, 216, 0.24)` |

### Text

| Role | Token | Hex |
|---|---|---|
| Primary | `--text-primary` | `#0F172A` |
| Secondary | `--text-secondary` | `#475569` |
| Muted | `--text-muted` | `#607086` |
| Faint | `--text-faint` | `#64748B` |

### Accent — Product / Action Blue

| Role | Token | Value |
|---|---|---|
| Default | `--accent` | `#1D4ED8` |
| Hover | `--accent-hover` | `#2563EB` |
| Dim | `--accent-dim` | `#1E40AF` |
| Ghost (background tint) | `--accent-ghost` | `rgba(29, 78, 216, 0.08)` |
| Glow | `--accent-glow` | `rgba(29, 78, 216, 0.15)` |
| Pulse | `--accent-pulse` | `rgba(29, 78, 216, 0.28)` |
| On-accent text | `--accent-contrast` | `#FFFFFF` |

### Severity Colours

| Severity | Color token | Hex | Background token | Hex |
|---|---|---|---|---|
| Critical | `--sev-critical-color` | `#B91C1C` | `--sev-critical-bg` | `rgba(220, 38, 38, 0.06)` |
| High | `--sev-high-color` | `#C2410C` | `--sev-high-bg` | `rgba(234, 88, 12, 0.06)` |
| Medium | `--sev-medium-color` | `#A16207` | `--sev-medium-bg` | `rgba(202, 138, 4, 0.06)` |
| Low | `--sev-low-color` | `#78716C` | `--sev-low-bg` | `transparent` |
| Info | `--sev-info-color` | `#64748B` | `--sev-info-bg` | `rgba(100, 116, 139, 0.06)` |

### Special Purpose Colours

| Role | Token | Hex | Rule |
|---|---|---|---|
| Healthy / remediated / verified | `--nominal-color` | `#0F766E` (teal) | Reserved for resolved state only — never decorative |
| AI / machine actions | `--machine-color` | `#7C3AED` (purple) | Only for AI-generated content indicators |

---

## Colours — Dark Mode

Activated via `[data-theme="dark"]` on `:root`. All semantic roles remain identical; only the hex values shift.

### Backgrounds

| Role | Token | Hex |
|---|---|---|
| Page canvas | `--bg-root` | `#0F1117` |
| App shell | `--bg-app` | `#111318` |
| Panel | `--bg-panel` | `#161820` |
| Surface | `--bg-surface` | `#1C1F28` |
| Hover | `--bg-hover` | `#232632` |
| Card | `--bg-card` | `#181B24` |

### Text

| Role | Token | Hex |
|---|---|---|
| Primary | `--text-primary` | `#F1F5F9` |
| Secondary | `--text-secondary` | `#94A3B8` |
| Muted | `--text-muted` | `#7D8CA1` |

### Accent

| Role | Token | Hex |
|---|---|---|
| Default | `--accent` | `#60A5FA` |
| Hover | `--accent-hover` | `#93C5FD` |

### Severity (Dark)

| Severity | Color | Hex |
|---|---|---|
| Critical | `--sev-critical-color` | `#F87171` |
| High | `--sev-high-color` | `#FB923C` |
| Medium | `--sev-medium-color` | `#FBBF24` |
| Low | `--sev-low-color` | `#A8A29E` |
| Info | `--sev-info-color` | `#94A3B8` |
| Nominal | `--nominal-color` | `#5EEAD4` |
| AI / machine | `--machine-color` | `#A78BFA` |

---

## Chart / Data Visualisation Series

Used in recharts and SVG charts. Switch automatically with the theme.

| Series | Light | Dark |
|---|---|---|
| 1 (primary) | `#1D4ED8` | `#60A5FA` |
| 2 | `#0F766E` | `#5EEAD4` |
| 3 | `#7C3AED` | `#A78BFA` |
| 4 | `#0E7490` | `#22D3EE` |
| 5 (neutral) | `#64748B` | `#94A3B8` |

---

## Spacing Scale

4px base grid. Use tokens — avoid magic numbers.

| Token | Value |
|---|---|
| `--space-1` | `4px` |
| `--space-2` | `8px` |
| `--space-3` | `12px` |
| `--space-4` | `16px` |
| `--space-5` | `20px` |
| `--space-6` | `24px` |
| `--space-7` | `32px` |
| `--space-8` | `40px` |

---

## Border Radius

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | `6px` | Inputs, badges, chips |
| `--radius-md` | `8px` | Cards, panels |
| `--radius-lg` | `8px` | Larger cards |
| `--radius-xl` | `10px` | Modals, elevated panels |
| `--r-pill` | `999px` | Pills, tags |

---

## Motion

Apple HIG-inspired easing. All animation is gated by `prefers-reduced-motion`.

| Token | Value | Usage |
|---|---|---|
| `--ease-spring` | `cubic-bezier(0.16, 1, 0.3, 1)` | Interactive lift, scale |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrances |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Theme transitions |
| `--dur-micro` | `100ms` | Immediate feedback |
| `--dur-fast` | `180ms` | Hover states |
| `--dur-base` | `240ms` | Most transitions |
| `--dur-slow` | `350ms` | Larger panel reveals |
| `--dur-theme` | `300ms` | Light ↔ dark crossfade |

---

## Colour Semantic Rules

These rules are enforced across the entire codebase. Follow them on any new UI:

| Colour | Reserved for | Never use for |
|---|---|---|
| **Blue** (`--accent`) | Interactive elements, focus rings, active states, links | Decoration, backgrounds, non-actionable elements |
| **Teal** (`--nominal-color`) | Healthy / verified / remediated state indicators | Any other purpose — it means "safe" |
| **Red** (`--sev-critical-color`) | Critical severity findings only | Error states unrelated to security severity |
| **Orange** (`--sev-high-color`) | High severity findings only | Warnings, non-security alerts |
| **Amber** (`--sev-medium-color`) | Medium severity findings only | General caution states |
| **Purple** (`--machine-color`) | AI-generated content, machine-authored actions | Brand colour, decoration |
| **Green** | Not used as a brand colour | Never use green outside of `--nominal-color` |

---

## Website / Marketing Usage

When building the Vedha marketing site or any external-facing page, follow these adaptations of the same token system:

- **Background:** Use `#060B14` (deep indigo-black) as the hero ground — darker than the app's `--bg-root` to convey authority
- **Accent:** Same `#1D4ED8` / `#3B7BFF` family — keep brand consistency
- **Headline typography:** Same `-apple-system` stack, `font-weight: 800`, `letter-spacing: -0.04em`
- **Severity colours:** Use the same critical/high/medium/low palette in any finding previews or marketing callouts
- **Compliance chips:** Use `--bg-surface` equivalent with `--border-subtle` borders — same muted treatment as the app

Reference: `docs/design/brand-competitive-analysis.md` for competitive positioning context.
