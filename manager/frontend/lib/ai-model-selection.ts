export const AI_PROVIDERS = ["ollama", "openrouter", "anthropic", "openai"] as const;

export type AiProvider = (typeof AI_PROVIDERS)[number];

export type AiModelSelection = {
  provider?: AiProvider;
  model?: string;
};

const MODEL_ID = /^[A-Za-z0-9][A-Za-z0-9._:/-]{0,159}$/;

/** Keep the browser-to-Manager provider seam as strict as Manager's schema.
 * `null` means the caller supplied a value that Manager must never receive. */
export function parseAiModelSelection(
  provider: unknown,
  model: unknown,
): AiModelSelection | null {
  if (provider !== undefined && !AI_PROVIDERS.includes(provider as AiProvider)) return null;
  if (model !== undefined && (typeof model !== "string" || !MODEL_ID.test(model))) return null;
  const selectedProvider = provider as AiProvider | undefined;
  const selectedModel = model as string | undefined;
  return {
    ...(selectedProvider !== undefined ? { provider: selectedProvider } : {}),
    ...(selectedModel !== undefined ? { model: selectedModel } : {}),
  };
}
