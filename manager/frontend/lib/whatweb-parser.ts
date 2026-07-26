export interface WhatWebResult {
  target: string;
  plugins: Record<string, unknown>;
}

export interface WhatWebParseResult {
  results: WhatWebResult[];
  invalidEntries: number;
}

/** Parse the JSON array emitted by WhatWeb's supported `--log-json=-` mode. */
export function parseWhatWebOutput(raw: string): WhatWebParseResult {
  if (!raw.trim()) {
    throw new Error("WhatWeb produced empty JSON output.");
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    throw new Error(`WhatWeb produced malformed JSON: ${String(err)}`);
  }

  if (!Array.isArray(parsed)) {
    throw new Error("WhatWeb JSON output must be an array.");
  }

  const results: WhatWebResult[] = [];
  let invalidEntries = 0;
  for (const entry of parsed) {
    if (
      !entry
      || typeof entry !== "object"
      || typeof (entry as { target?: unknown }).target !== "string"
      || !(entry as { target: string }).target
      || !(entry as { plugins?: unknown }).plugins
      || typeof (entry as { plugins: unknown }).plugins !== "object"
      || Array.isArray((entry as { plugins: unknown }).plugins)
    ) {
      invalidEntries += 1;
      continue;
    }
    results.push(entry as WhatWebResult);
  }

  return { results, invalidEntries };
}
