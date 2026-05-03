#!/usr/bin/env bash
# Capture + extract + summarize + release-notes + (consecutive-pair) diff for
# the curated "first and last of every major" set. Sequential because the
# cch-auth Docker volume is exclusive.
set -uo pipefail

REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$REPO/.tools/run-batch.log"
: >"$LOG"

VERSIONS=(0.2.126 1.0.0 1.0.128 2.0.0 2.1.126)

dir_for() { python3 "$REPO/scripts/_paths.py" dir_for "$1"; }

log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

for V in "${VERSIONS[@]}"; do
    D="$(dir_for "$V")"
    log "=== capturing $V (-> versions/$D/) ==="
    "$REPO/scripts/capture-version.sh" "$V" >>"$LOG" 2>&1
    log "capture exit: $?"

    log "extracting $V"
    for d in "$REPO/versions/$D/scenarios"/*/; do
        [[ -d "$d" ]] || continue
        python3 "$REPO/scripts/extract.py" "$d" >>"$LOG" 2>&1 || log "extract FAILED: $(basename "${d%/}")"
    done

    log "summarizing $V"
    python3 "$REPO/scripts/summarize-version.py" "$V" >>"$LOG" 2>&1 || log "summarize FAILED: $V"

    log "release-notes $V"
    python3 "$REPO/scripts/fetch-release-notes.py" "$V" >>"$LOG" 2>&1 || log "release-notes FAILED: $V"
done

log "=== diffing consecutive pairs ==="
PREV=""
for V in "${VERSIONS[@]}"; do
    if [[ -n "$PREV" ]]; then
        log "diff $PREV -> $V"
        python3 "$REPO/scripts/diff-versions.py" "$PREV" "$V" >>"$LOG" 2>&1 || log "diff FAILED: $PREV -> $V"
    fi
    PREV="$V"
done

log "=== batch complete ==="
