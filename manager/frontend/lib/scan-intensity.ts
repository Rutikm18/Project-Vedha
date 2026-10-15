/** Mode descriptions follow probe/workflow/intensity.py; requests send only the preset name.
 * Rates describe configured envelopes, not observed throughput or completion time. */
export type Intensity = "stealth" | "normal" | "aggressive";
export interface IntensityOption { id: Intensity; label: string; rate: number; why: string }
export const INTENSITY: IntensityOption[] = [
  { id: "stealth", label: "Stealth", rate: 50,
    why: "Lower traffic with a focused port set. This remains an active assessment." },
  { id: "normal", label: "Normal", rate: 200,
    why: "Balanced coverage for routine engagement assessments." },
  { id: "aggressive", label: "Aggressive", rate: 150,
    why: "Broader enterprise coverage and additional retries. Choose Deep scan for all TCP ports on one IP." },
];
