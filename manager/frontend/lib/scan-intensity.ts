/* Display data for the scan-intensity dial. The probe owns the real envelope
   (probe/workflow/intensity.py) and the launcher sends only the name, so
   `rate` must equal the preset's rate — a test enforces it. The dial measures
   HARDNESS, not speed: the widest sweep probes the most gently. */
export type Intensity = "stealth" | "normal" | "aggressive";

export interface IntensityOption {
  id: Intensity;
  label: string;
  rate: number;
  why: string;
  color: string;
  angle: number;
  sweep: string;
}

export const INTENSITY: IntensityOption[] = [
  { id: "stealth",    label: "Stealth",    rate: 50,  color: "#6ee7b7",             angle: -60, sweep: "6.2s",
    why: "Low and slow over a small high-signal port set. Minimizes IDS/IPS triggers and link load — for monitored, production, or fragile segments." },
  { id: "normal",     label: "Normal",     rate: 200, color: "var(--accent)",        angle: 0,   sweep: "3.4s",
    why: "Balanced default. Right for most internal engagements with no special constraints." },
  { id: "aggressive", label: "Aggressive", rate: 150, color: "var(--sev-high-color)", angle: 60,  sweep: "4.2s",
    why: "Exhaustive, not fast: all 65,535 ports, probed patiently so silence means a firewall rather than a rushed probe. Each host runs on a time budget; a large estate takes hours." },
];
