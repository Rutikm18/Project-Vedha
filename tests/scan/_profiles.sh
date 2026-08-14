#!/usr/bin/env bash
# _profiles.sh — intensity profiles for the per-scanner test harness.
#
# Five nmap-style timing templates, mapped onto the probe's three real knobs:
#   --rate         max operations per second
#   --concurrency  max concurrent in-flight operations
#   --timeout      per-operation timeout (seconds)
#
# Usage (after sourcing):
#   resolve_profile T3   # -> sets PROFILE_RATE / PROFILE_CONC / PROFILE_TIMEOUT / PROFILE_LABEL
#
# macOS ships bash 3.2 (no associative arrays), so this uses a case statement.

# Every level, in order — used by the "all" sweep.
ALL_PROFILES="T1 T2 T3 T4 T5"

resolve_profile() {
    case "$1" in
        T1|t1) PROFILE_RATE=5    ; PROFILE_CONC=5   ; PROFILE_TIMEOUT=8 ; PROFILE_LABEL="T1 paranoid"   ;;
        T2|t2) PROFILE_RATE=25   ; PROFILE_CONC=20  ; PROFILE_TIMEOUT=5 ; PROFILE_LABEL="T2 sneaky"     ;;
        T3|t3) PROFILE_RATE=200  ; PROFILE_CONC=100 ; PROFILE_TIMEOUT=3 ; PROFILE_LABEL="T3 normal"     ;;
        T4|t4) PROFILE_RATE=800  ; PROFILE_CONC=300 ; PROFILE_TIMEOUT=2 ; PROFILE_LABEL="T4 aggressive" ;;
        T5|t5) PROFILE_RATE=2000 ; PROFILE_CONC=800 ; PROFILE_TIMEOUT=1 ; PROFILE_LABEL="T5 insane"     ;;
        *) echo "unknown intensity '$1' (use T1..T5, or 'all')" >&2; return 1 ;;
    esac
    return 0
}
