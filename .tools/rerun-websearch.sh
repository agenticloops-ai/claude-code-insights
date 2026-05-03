#!/usr/bin/env bash
# Re-capture only 08-websearch for the already-captured versions, then
# refresh extracts, per-version summaries, and consecutive-pair diffs.
set -uo pipefail

REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$REPO/.tools/rerun-websearch.log"
: >"$LOG"

VERSIONS=(0.2.126 1.0.0 1.0.128 2.0.0 2.1.126)
SCEN=08-websearch

log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

for V in "${VERSIONS[@]}"; do
    D="$(python3 "$REPO/scripts/_paths.py" dir_for "$V")"
    log "=== $SCEN @ $V (-> versions/$D/) ==="
    rm -rf "$REPO/versions/$D/scenarios/$SCEN/raw" \
           "$REPO/versions/$D/scenarios/$SCEN/extracted"
    "$REPO/scripts/run-scenario.sh" "$V" "$SCEN" >>"$LOG" 2>&1
    log "  capture exit: $?"
    python3 "$REPO/scripts/extract.py" "$REPO/versions/$D/scenarios/$SCEN" >>"$LOG" 2>&1 \
        || log "  extract FAILED"
    log "summarizing $V"
    python3 "$REPO/scripts/summarize-version.py" "$V" >>"$LOG" 2>&1 || log "  summarize FAILED"
done

log "=== diffing consecutive pairs ==="
PREV=""
for V in "${VERSIONS[@]}"; do
    if [[ -n "$PREV" ]]; then
        log "diff $PREV -> $V"
        python3 "$REPO/scripts/diff-versions.py" "$PREV" "$V" >>"$LOG" 2>&1 || log "  diff FAILED"
    fi
    PREV="$V"
done

log "=== rerun complete ==="
