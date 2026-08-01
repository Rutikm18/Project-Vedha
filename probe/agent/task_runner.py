"""
task_runner.py — orchestrates the full lifecycle of a single scan job.

Given a job dict from the manager (pushed via WebSocket or polled via HTTP),
the runner:
  1. Resolves the use_case_id → scan_type + profile
  2. Fetches engagement scope (belt-and-suspenders validation)
  3. Validates targets against scope + exclusions
  4. Executes the scan (via engine.run_scan)
  5. Submits the result (via transport or result_spool with retry)

All I/O dependencies are injected so the runner is fully testable with mocks.
"""
from __future__ import annotations

import ipaddress
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from agent.use_cases import resolve as resolve_use_case

LOG = logging.getLogger("task_runner")


@dataclass
class JobResult:
    """Structured result from running one scan job."""
    success: bool
    job_id: str
    engagement_id: str
    scan_type: str
    profile: str
    result: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    use_case_id: str | None = None


class TaskRunner:
    """Orchestrates one scan job's lifecycle.

    The runner holds injected dependencies so it can be instantiated once
    and reused across many jobs without leaking state.
    """

    def __init__(
        self,
        http_get: Callable[[str], dict[str, Any] | None],
        submit_result: Callable[[str, dict[str, Any]], bool],
        *,
        spool_submit: Callable[[str, dict[str, Any], Callable], bool] | None = None,
        run_scan_fn: Callable[..., dict[str, Any]] | None = None,
        identity_sk: bytes | None = None,
        local_allowed_networks: list[str] | None = None,
    ):
        """Args:
            http_get:       Callback for authenticated GET (from Transport).
            submit_result:  Callable(job_id, payload) -> bool for direct upload.
            spool_submit:   Optional Callable(job_id, payload, upload_fn) -> bool
                            that saves locally first and retries. When None, falls
                            back to calling submit_result directly.
            run_scan_fn:    The scan function to call. Defaults to engine.run_scan
                            when not provided (production use).
            identity_sk:    X25519 private key bytes for scope decryption (Phase 4).
                            When None, encrypted scope is silently skipped.
            local_allowed_networks: Probe-local IP/CIDR ceiling. ``None`` keeps
                            standalone/library compatibility; an explicit empty
                            list is fail-closed and refuses all network jobs.
        """
        self._http_get = http_get
        self._submit_result = submit_result
        self._spool_submit = spool_submit
        self._run_scan = run_scan_fn
        self._identity_sk = identity_sk
        self._local_allowed_networks = (
            None
            if local_allowed_networks is None
            else list(local_allowed_networks)
        )
        if self._run_scan is None:
            from agent.engine import run_scan
            self._run_scan = run_scan

    # ── Main entry point ─────────────────────────────────────────────────────

    def run_job(self, job: dict[str, Any], agent_id: str) -> JobResult:
        """Execute a complete scan job lifecycle.

        Args:
            job: Job dict from the manager (job_id, engagement_id, job_type, params,
                 and optionally encrypted_scope).
            agent_id: The probe's own agent ID (for the submit URL).

        Returns:
            A JobResult describing the outcome.
        """
        if not isinstance(job, dict):
            error = "job payload must be an object"
            return JobResult(
                success=False,
                job_id="?",
                engagement_id="",
                scan_type="unknown",
                profile="it",
                error=error,
            )

        job_id = job.get("job_id", "?")
        engagement_id = job.get("engagement_id", "")
        raw_params = job.get("params") or {}
        if not isinstance(raw_params, dict):
            error = "job params must be an object"
            self._submit_or_spool(job_id, {
                "success": False,
                "result": {},
                "error": error,
            })
            return JobResult(
                success=False,
                job_id=job_id,
                engagement_id=engagement_id,
                scan_type="unknown",
                profile="it",
                error=error,
            )
        params = dict(raw_params)
        use_case_id = params.get("use_case_id") or job.get("use_case_id")
        job_type = job.get("job_type", "discovery")

        # ── Phase 4: Decrypt encrypted scope (if present) ──────────────────
        # The manager encrypts the engagement scope to this probe's X25519
        # public key. Decrypt it here BEFORE any validation or scanning.
        decrypted_scope = None
        encrypted_scope_b64 = job.get("encrypted_scope") or params.get("encrypted_scope")
        if encrypted_scope_b64 and self._identity_sk:
            try:
                from agent.scope_crypt import decrypt_scope_b64
                scope_json = decrypt_scope_b64(encrypted_scope_b64, self._identity_sk)
                decrypted_scope = json.loads(scope_json)
                if not isinstance(decrypted_scope, dict):
                    raise ValueError("decrypted scope must be an object")
                LOG.info("scope.decrypted job=%s eng=%s cidrs=%d",
                         job_id,
                         decrypted_scope.get("engagement_id", ""),
                         len(decrypted_scope.get("scope_cidrs", [])))
                # Merge decrypted scope into params so validation uses it
                if decrypted_scope.get("scope_cidrs"):
                    params["scope_cidrs"] = decrypted_scope["scope_cidrs"]
                if decrypted_scope.get("excluded_cidrs"):
                    existing = params.get("excluded_cidrs") or []
                    if isinstance(existing, str):
                        existing = [existing]
                    deduped = list(dict.fromkeys([*existing, *decrypted_scope["excluded_cidrs"]]))
                    params["excluded_cidrs"] = deduped
            except Exception as exc:
                LOG.warning("scope.decrypt_failed job=%s error=%s", job_id, exc)
                # Don't fail the job — fall back to unencrypted scope in params
                # and HTTP scope fetch validation (belt-and-suspenders)

        # ── Step 1: Resolve use-case → scan_type + profile ──────────────────
        try:
            scan_type, profile = resolve_use_case(use_case_id, job_type, params)
        except ValueError as exc:
            LOG.error("Job %s rejected: %s", job_id, exc)
            self._submit_or_spool(job_id, {
                "success": False, "result": {}, "error": str(exc),
            })
            return JobResult(
                success=False, job_id=job_id, engagement_id=engagement_id,
                scan_type="unknown", profile="it", error=str(exc),
                use_case_id=use_case_id,
            )

        # ── Step 2: Extract targets ──────────────────────────────────────────
        if "targets" in params:
            targets_raw = params["targets"]
        elif "target" in params:
            targets_raw = params["target"]
        else:
            targets_raw = params.get("scope_cidrs") or []
        if isinstance(targets_raw, str):
            targets_raw = [targets_raw]
        if (
            not isinstance(targets_raw, (list, tuple))
            or any(not isinstance(target, str) for target in targets_raw)
        ):
            error = "targets must be a string or list of strings"
            LOG.error("Job %s: %s", job_id, error)
            self._submit_or_spool(job_id, {
                "success": False, "result": {}, "error": error,
            })
            return JobResult(
                success=False, job_id=job_id, engagement_id=engagement_id,
                scan_type=scan_type, profile=profile, error=error,
                use_case_id=use_case_id,
            )
        targets_raw = [target.strip() for target in targets_raw if target.strip()]

        if not targets_raw:
            error = "No targets or scope_cidrs provided in job params"
            LOG.error("Job %s: %s", job_id, error)
            self._submit_or_spool(job_id, {
                "success": False, "result": {}, "error": error,
            })
            return JobResult(
                success=False, job_id=job_id, engagement_id=engagement_id,
                scan_type=scan_type, profile=profile, error=error,
                use_case_id=use_case_id,
            )
        params["targets"] = targets_raw

        # ── Step 3: Re-validate scope (defense in depth) ────────────────────
        from agent.scope_validator import (
            fetch_engagement_scope,
            validate_targets_in_scope,
            targets_in_excludes,
            merge_exclusions,
        )

        engagement_scope = None
        engagement_excludes: list[str] = []
        if engagement_id:
            engagement_scope, engagement_excludes = fetch_engagement_scope(
                engagement_id, self._http_get,
            )

        # `_excluded_cidrs` is the manager-carried authoritative fallback used
        # when refreshing /scope fails. Preserve it alongside operator-supplied
        # per-job exclusions.
        manager_excludes = params.get("_excluded_cidrs") or []
        if isinstance(manager_excludes, str):
            manager_excludes = [manager_excludes]
        job_excludes = params.get("excluded_cidrs") or []
        if isinstance(job_excludes, str):
            job_excludes = [job_excludes]
        all_excludes = merge_exclusions(
            engagement_excludes,
            [*manager_excludes, *job_excludes],
        )
        params.pop("_excluded_cidrs", None)
        params["excluded_cidrs"] = all_excludes

        embedded_scope = params.get("scope_cidrs") or []
        if isinstance(embedded_scope, str):
            embedded_scope = [embedded_scope]
        effective_scope = engagement_scope or embedded_scope

        if engagement_id and not effective_scope:
            error = (
                "No authoritative scope available for manager-issued job; "
                "refusing to scan target-only payload"
            )
            LOG.error("Job %s: %s", job_id, error)
            self._submit_or_spool(job_id, {
                "success": False, "result": {},
                "error": error,
            })
            return JobResult(
                success=False, job_id=job_id, engagement_id=engagement_id,
                scan_type=scan_type, profile=profile, error=error,
                use_case_id=use_case_id,
            )

        # Validate targets against authoritative scope, falling back to the
        # manager-embedded scope when the /scope fetch is unavailable.
        if effective_scope and targets_raw:
            allowed, rejected = validate_targets_in_scope(targets_raw, effective_scope)
            if rejected:
                LOG.info("scope guard: %d target(s) outside scope — skipped: %s",
                         len(rejected), rejected[:5])
            if not allowed:
                error = f"All targets outside engagement scope {effective_scope}"
                LOG.error("Job %s: %s", job_id, error)
                self._submit_or_spool(job_id, {
                    "success": False, "result": {},
                    "error": error,
                })
                return JobResult(
                    success=False, job_id=job_id, engagement_id=engagement_id,
                    scan_type=scan_type, profile=profile, error=error,
                    use_case_id=use_case_id,
                )
            params["targets"] = allowed

        # The engagement is the operator authorization boundary; the local
        # ceiling is the appliance owner's deployment boundary. Both must allow
        # every requested target. An explicit empty ceiling intentionally
        # denies execution instead of treating an omitted config as unlimited.
        if self._local_allowed_networks is not None:
            locally_allowed, locally_rejected = validate_targets_in_scope(
                params.get("targets") or [],
                self._local_allowed_networks,
            )
            if locally_rejected:
                LOG.warning(
                    "local scope ceiling rejected %d target(s): %s",
                    len(locally_rejected),
                    locally_rejected[:5],
                )
            if not locally_allowed:
                error = (
                    "All targets outside the probe's local network ceiling; "
                    "set PROBE_NETWORK_SEGMENTS to authorized reachable CIDRs"
                )
                LOG.error("Job %s: %s", job_id, error)
                self._submit_or_spool(job_id, {
                    "success": False, "result": {}, "error": error,
                })
                return JobResult(
                    success=False, job_id=job_id, engagement_id=engagement_id,
                    scan_type=scan_type, profile=profile, error=error,
                    use_case_id=use_case_id,
                )
            params["targets"] = locally_allowed

        # Drop excluded targets
        if all_excludes and params.get("targets"):
            kept, dropped = targets_in_excludes(params["targets"], all_excludes)
            if dropped:
                LOG.info("exclusion guard: %d target(s) in excluded range — skipped: %s",
                         len(dropped), dropped[:5])
            if not kept:
                error = f"All targets fall inside excluded ranges {all_excludes}"
                LOG.error("Job %s: %s", job_id, error)
                self._submit_or_spool(job_id, {
                    "success": False, "result": {},
                    "error": error,
                })
                return JobResult(
                    success=False, job_id=job_id, engagement_id=engagement_id,
                    scan_type=scan_type, profile=profile, error=error,
                    use_case_id=use_case_id,
                )
            params["targets"] = kept

        # ── Step 4: Log the resolved task ───────────────────────────────────
        uc_label = f"use-case={use_case_id}" if use_case_id else f"scan_type={scan_type}"
        LOG.info("▶ Executing %s", uc_label)
        LOG.info("    profile        : %s", profile)
        LOG.info("    targets        : %s", params.get("targets") or "?")
        if all_excludes:
            LOG.info("    excluded       : %s", all_excludes)

        # ── Step 5: Execute the scan ────────────────────────────────────────
        params["profile"] = profile
        try:
            result = self._run_scan(
                scan_type, params,
                use_case_id=use_case_id,
                engagement_uuid=engagement_id,
                validated_scope=effective_scope or None,
                validated_excludes=all_excludes,
                local_allowed_scope=self._local_allowed_networks,
            )
            if not isinstance(result, dict):
                raise TypeError("scan engine returned a non-object result")
        except Exception as exc:
            error = f"scan engine failed: {type(exc).__name__}: {exc}"
            LOG.exception("Job %s: %s", job_id, error)
            result = {
                "result_schema_version": "1.1",
                "ok": False,
                "outcome": "failed",
                "error_code": "scan_engine_exception",
                "error": error,
                "errors": [error],
                "facts": [],
                "run_stats": {},
            }

        # ── Step 6: Submit result ───────────────────────────────────────────
        stats = result.get("run_stats") or {}
        LOG.info("done — %d hosts, %d open ports",
                 stats.get("host_count", 0),
                 stats.get("open_ports", 0))

        success = bool(result.get("ok"))
        payload = {
            "success": success,
            "result": result,
            "error": result.get("error"),
        }
        self._submit_or_spool(job_id, payload)

        return JobResult(
            success=success,
            job_id=job_id,
            engagement_id=engagement_id,
            scan_type=scan_type,
            profile=profile,
            result=result,
            error=result.get("error"),
            use_case_id=use_case_id,
        )

    def _submit_or_spool(self, job_id: str, payload: dict[str, Any]) -> None:
        """Submit the result, with spool-and-retry if available."""
        if self._spool_submit:
            self._spool_submit(job_id, payload, self._submit_result)
        else:
            self._submit_result(job_id, payload)
