"use client";
import React, { useEffect, useState } from "react";
import { Cpu, ChevronDown } from "lucide-react";

export type ModelSelection = { provider: string; model: string };

interface ProviderStatus {
  id: string;
  label: string;
  configured: boolean;
  privacy: "local" | "cloud";
  default_model: string;
  models: string[];
  reason?: string | null;
}
interface AiStatus {
  provider: string;
  model: string;
  providers: ProviderStatus[];
}

const STORAGE_KEY = "vedha.ai.model";

function readStored(): ModelSelection | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<ModelSelection>;
    if (parsed?.provider && parsed?.model) return { provider: parsed.provider, model: parsed.model };
  } catch { /* ignore malformed */ }
  return null;
}

export function ModelSwitcher({
  value,
  onChange,
}: {
  value: ModelSelection | null;
  onChange: (v: ModelSelection) => void;
}) {
  const [status, setStatus] = useState<AiStatus | null>(null);

  useEffect(() => {
    let active = true;
    fetch("/api/ai/status", { credentials: "same-origin" })
      .then((r) => (r.ok ? r.json() : null))
      .then((data: AiStatus | null) => {
        if (!active || !data?.providers) return;
        setStatus(data);
        // Restore a still-valid stored choice, else fall back to the server default.
        const stored = readStored();
        const configured = data.providers.filter((p) => p.configured);
        const valid = stored && configured.some((p) => p.id === stored.provider);
        if (valid && stored) onChange(stored);
        else onChange({ provider: data.provider, model: data.model });
      })
      .catch(() => { /* status endpoint down — drawer still works on server default */ });
    return () => { active = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleChange = (raw: string) => {
    const [provider, ...rest] = raw.split("::");
    const model = rest.join("::");
    const next = { provider, model };
    onChange(next);
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); } catch { /* private mode */ }
  };

  if (!status) return null;

  const current = value ? `${value.provider}::${value.model}` : `${status.provider}::${status.model}`;

  return (
    <label className="model-switcher" title="AI model — falls back to a free model when the paid provider is out of credit">
      <Cpu size={12} aria-hidden />
      <div className="model-switcher-select">
        <select
          aria-label="Select AI model"
          value={current}
          onChange={(e) => handleChange(e.target.value)}
        >
          {status.providers.map((p) => (
            <optgroup
              key={p.id}
              label={p.configured ? p.label : `${p.label} · ${p.reason ?? "not configured"}`}
            >
              {(p.models.length ? p.models : [p.default_model]).map((m) => (
                <option key={`${p.id}::${m}`} value={`${p.id}::${m}`} disabled={!p.configured}>
                  {m}{p.privacy === "local" ? " · local" : ""}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
        <ChevronDown size={12} aria-hidden />
      </div>
    </label>
  );
}
