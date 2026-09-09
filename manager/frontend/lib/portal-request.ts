const REPLAY_SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);

/**
 * A request may be repeated after token rotation only when it is intrinsically
 * safe or the caller supplied an idempotency key for backend deduplication.
 */
export function canReplayPortalRequest(method: string, idempotencyKey?: string): boolean {
  return REPLAY_SAFE_METHODS.has(method.toUpperCase()) || Boolean(idempotencyKey?.trim());
}
