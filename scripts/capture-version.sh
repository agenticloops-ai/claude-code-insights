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
IMAGE="cch:${VERSION}"

SCENARIOS=()
if [[ $# -eq 0 ]]; then
    while IFS= read -r line; do
        SCENARIOS+=("$line")
    done < <(cd "$REPO_DIR/scenarios" && ls -d */ 2>/dev/null | sed 's:/$::' | grep -v '^README' | sort)
else
    SCENARIOS=("$@")
fi

# Always rebuild from a clean slate so changes to entrypoint.sh / Dockerfile /
# fixtures land in the image. Docker layer cache keeps the slow `npm install`
# step warm, so a rebuild after pure entrypoint edits takes ~1s.
echo ">>> removing any existing $IMAGE so it rebuilds from current sources"
docker ps -aq --filter "ancestor=$IMAGE" | xargs -r docker rm -f >/dev/null 2>&1 || true
docker image rm -f "$IMAGE" >/dev/null 2>&1 || true

# Drop the image (and any leftover stopped containers from this version) once
# capture is done. Layer cache on the host stays, so the next run is still fast.
cleanup() {
    docker ps -aq --filter "ancestor=$IMAGE" | xargs -r docker rm -f >/dev/null 2>&1 || true
    docker image rm -f "$IMAGE" >/dev/null 2>&1 || true
}
trap cleanup EXIT

PASS=()
FAIL=()
SKIP=()
START=$(date +%s)

for scen in "${SCENARIOS[@]}"; do
    set +e
    "${REPO_DIR}/scripts/run-scenario.sh" "$VERSION" "$scen"
    rc=$?
    set -e
    case $rc in
        0)   PASS+=("$scen") ;;
        125) SKIP+=("$scen") ;;
        *)   FAIL+=("$scen") ;;
    esac
done

END=$(date +%s)
echo
echo "=== capture summary: claude-code-${VERSION} ==="
echo "duration: $((END - START))s"
echo "passed:   ${#PASS[@]}  (${PASS[*]:-})"
echo "skipped:  ${#SKIP[@]}  (${SKIP[*]:-})"
echo "failed:   ${#FAIL[@]}  (${FAIL[*]:-})"

[[ ${#FAIL[@]} -eq 0 ]]
