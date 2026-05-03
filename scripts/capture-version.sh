#!/usr/bin/env bash
# Run every scenario against a pinned claude-code version.
#
#   scripts/capture-version.sh <claude-version> [scenario-name...]
#
# Without scenario names, runs the full suite in scenarios/. With names,
# runs just those. Continues on failure; prints a summary at the end.

set -uo pipefail

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <claude-version> [scenario...]" >&2
    exit 1
fi

VERSION="$1"; shift
REPO_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

SCENARIOS=()
if [[ $# -eq 0 ]]; then
    while IFS= read -r line; do
        SCENARIOS+=("$line")
    done < <(cd "$REPO_DIR/scenarios" && ls -d */ 2>/dev/null | sed 's:/$::' | grep -v '^README' | sort)
else
    SCENARIOS=("$@")
fi

PASS=()
FAIL=()
START=$(date +%s)

for scen in "${SCENARIOS[@]}"; do
    if "${REPO_DIR}/scripts/run-scenario.sh" "$VERSION" "$scen"; then
        PASS+=("$scen")
    else
        FAIL+=("$scen")
    fi
done

END=$(date +%s)
echo
echo "=== capture summary: claude-code-${VERSION} ==="
echo "duration: $((END - START))s"
echo "passed:   ${#PASS[@]}  (${PASS[*]:-})"
echo "failed:   ${#FAIL[@]}  (${FAIL[*]:-})"

[[ ${#FAIL[@]} -eq 0 ]]
