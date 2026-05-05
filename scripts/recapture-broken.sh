#!/usr/bin/env bash
# Re-run capture-version.sh + extract + summarize for every version whose
# version-root tools.json is empty (3 bytes "[]\n"). Used after fixing
# the run-scenario.sh retry logic to recapture 2.0.46–2.0.76 which fail
# with "Execution error" on a non-trivial fraction of attempts.
#
#   scripts/recapture-broken.sh            # all empty versions
#   scripts/recapture-broken.sh 2.0.46 …   # explicit list

set -uo pipefail

REPO_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${REPO_DIR}/versions/.recapture-logs"
mkdir -p "$LOG_DIR"

if [[ $# -gt 0 ]]; then
    VERSIONS=("$@")
else
    VERSIONS=()
    for v in $(cd "$REPO_DIR" && ls versions/ | sort); do
        sz=$(stat -f%z "$REPO_DIR/versions/$v/tools.json" 2>/dev/null || echo 0)
        if [[ "$sz" -le 5 ]]; then
            VERSIONS+=("${v#*_}")
        fi
    done
fi

echo "Recapture queue (${#VERSIONS[@]}): ${VERSIONS[*]}" >&2

OK=()
FAIL=()
for ver in "${VERSIONS[@]}"; do
    log="$LOG_DIR/$ver.log"
    echo "=== $ver ===" | tee -a "$log"
    started=$(date +%s)

    {
        CAPTURE_TIMEOUT_SECS=120 SCENARIO_RETRY_LIMIT=10 \
            "$REPO_DIR/scripts/capture-version.sh" "$ver" 2>&1
    } >>"$log" 2>&1
    rc=$?

    # Always try to extract whatever was captured.
    for sd in "$REPO_DIR"/versions/*_"$ver"/scenarios/*/; do
        [[ -d "$sd/raw" ]] || continue
        python3 "$REPO_DIR/scripts/extract.py" "$sd" >>"$log" 2>&1 || true
    done
    python3 "$REPO_DIR/scripts/summarize-version.py" "$ver" >>"$log" 2>&1 || true

    sz=$(stat -f%z "$REPO_DIR/versions/"*"_${ver}/tools.json" 2>/dev/null | head -1)
    elapsed=$(( $(date +%s) - started ))
    if [[ "${sz:-0}" -gt 5 ]]; then
        OK+=("$ver")
        echo "[${elapsed}s] $ver OK (tools.json=$sz B)"
    else
        FAIL+=("$ver")
        echo "[${elapsed}s] $ver FAIL (tools.json=${sz:-0} B)"
    fi
done

echo
echo "=== recapture summary ==="
echo "ok:   ${#OK[@]}  ${OK[*]:-}"
echo "fail: ${#FAIL[@]} ${FAIL[*]:-}"
[[ ${#FAIL[@]} -eq 0 ]]
