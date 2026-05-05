#!/usr/bin/env bash
# Run a single scenario against a pinned claude-code version.
#
#   scripts/run-scenario.sh <claude-version> <scenario-name>
#
# Reads scenarios/<scenario-name>/{prompt.txt,meta.json} and forwards the
# right flags to sandbox/run.sh. Output layout:
#   versions/<version>/scenarios/<scenario-name>/raw/   <- agentlens captures
#   versions/<version>/scenarios/<scenario-name>/       <- extracted artifacts
# Local-mode scenarios produce just output.txt + exit-code.txt at the root.

set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "usage: $0 <claude-version> <scenario-name>" >&2
    exit 1
fi

VERSION="$1"
SCENARIO="$2"

REPO_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SCEN_DIR="${REPO_DIR}/scenarios/${SCENARIO}"

if [[ ! -d "$SCEN_DIR" ]]; then
    echo "ERROR: scenario not found: $SCEN_DIR" >&2
    exit 1
fi

META="${SCEN_DIR}/meta.json"
PROMPT_FILE="${SCEN_DIR}/prompt.txt"
[[ -f "$META" ]] || { echo "ERROR: missing $META" >&2; exit 1; }
[[ -f "$PROMPT_FILE" ]] || { echo "ERROR: missing $PROMPT_FILE" >&2; exit 1; }

# Print fields from meta.json on separate lines, then read them sequentially.
# Avoids `mapfile` which is bash 4+ (macOS ships 3.2).
META_TMP="$(mktemp)"
trap 'rm -f "$META_TMP"' EXIT

python3 - "$META" >"$META_TMP" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
print(m.get("mode") or "agent")
# claude_args separated by US (0x1f)
print("\x1f".join(m.get("claude_args") or []))
print(m.get("min_version") or "")
# env as KEY=VALUE per line
for k, v in (m.get("env") or {}).items():
    print(f"E={k}={v}")
PY

MODE="agent"
CLAUDE_ARGS_RAW=""
MIN_VERSION=""
ENV_LINES=()

LINE_NUM=0
while IFS= read -r line; do
    LINE_NUM=$((LINE_NUM + 1))
    case $LINE_NUM in
        1) MODE="$line" ;;
        2) CLAUDE_ARGS_RAW="$line" ;;
        3) MIN_VERSION="$line" ;;
        *) [[ "$line" == E=* ]] && ENV_LINES+=("${line#E=}") ;;
    esac
done <"$META_TMP"

# Skip the scenario if its min_version is above the target. Exit code 125
# signals "skipped" to capture-version.sh / batch-capture.py — distinct from
# 124 (timeout) and 0/other (run/fail).
if [[ -n "$MIN_VERSION" ]]; then
    SKIP_REASON="$(python3 - "$VERSION" "$MIN_VERSION" <<'PY'
import sys
def parts(v): return tuple(int(x) for x in v.split(".") if x.isdigit())
have, need = parts(sys.argv[1]), parts(sys.argv[2])
if have < need:
    print(f"target {sys.argv[1]} below scenario floor {sys.argv[2]}")
PY
)"
    if [[ -n "$SKIP_REASON" ]]; then
        echo "=== ${SCENARIO} @ claude-code-${VERSION} [SKIPPED] === ${SKIP_REASON}"
        exit 125
    fi
fi

# Split CLAUDE_ARGS_RAW on US (0x1f).
CLAUDE_ARGS=()
if [[ -n "$CLAUDE_ARGS_RAW" ]]; then
    OLD_IFS="$IFS"
    IFS=$'\x1f'
    for a in $CLAUDE_ARGS_RAW; do CLAUDE_ARGS+=("$a"); done
    IFS="$OLD_IFS"
fi

PROMPT="$(cat "$PROMPT_FILE")"

EXTRA_FLAGS=(--mode "$MODE")

for env_kv in ${ENV_LINES[@]+"${ENV_LINES[@]}"}; do
    EXTRA_FLAGS+=(-e "$env_kv")
done

# Folder layout: versions/<release-date>_<version>/scenarios/<scen>/
# so a plain `ls` sorts chronologically. The npm version itself stays
# unchanged for the docker build / npm install.
DIRNAME="$(python3 "${REPO_DIR}/scripts/_paths.py" dir_for "$VERSION")"
SCEN_OUT_DIR="${REPO_DIR}/versions/${DIRNAME}/scenarios/${SCENARIO}"
mkdir -p "$SCEN_OUT_DIR"

echo "=== ${SCENARIO} @ claude-code-${VERSION} [${MODE}] ==="

if [[ "$MODE" == "local" ]]; then
    # Stdout-capture scenarios. `local` runs `claude <args>` (e.g. --help) —
    # no API call, no agentlens.
    OUT_FILE="${SCEN_OUT_DIR}/output.txt"
    EXIT_FILE="${SCEN_OUT_DIR}/exit-code.txt"
    set +e
    # Capture only stdout — stderr (sandbox diagnostics, any claude warnings)
    # stays on the host terminal so output.txt is the pristine CLI output.
    "${REPO_DIR}/sandbox/run.sh" \
        "$VERSION" \
        -o "$SCEN_OUT_DIR" \
        -s "$SCENARIO" \
        ${EXTRA_FLAGS[@]+"${EXTRA_FLAGS[@]}"} \
        -- ${CLAUDE_ARGS[@]+"${CLAUDE_ARGS[@]}"} \
        > "$OUT_FILE"
    rc=$?
    set -e
    echo "$rc" >"$EXIT_FILE"
    echo "wrote $OUT_FILE (exit $rc, $(wc -c <"$OUT_FILE" | tr -d ' ') bytes)"
    exit "$rc"
fi

# Every capture run replaces the prior contents of raw/. Extracted artifacts
# at the scenario root are overwritten by extract.py downstream.
RAW_DIR="${SCEN_OUT_DIR}/raw"
rm -rf "$RAW_DIR"
mkdir -p "$RAW_DIR"

"${REPO_DIR}/sandbox/run.sh" \
    "$VERSION" \
    -o "$RAW_DIR" \
    -s "$SCENARIO" \
    ${EXTRA_FLAGS[@]+"${EXTRA_FLAGS[@]}"} \
    -- ${CLAUDE_ARGS[@]+"${CLAUDE_ARGS[@]}"} "$PROMPT"

# If the API returned a model-not-found 404 (retired model) and the version
# supports --model (0.2.98+), retry with an explicit fallback model.
_raw_has_model_404() {
    python3 - "$RAW_DIR" <<'PY'
import json, sys
from pathlib import Path
for f in Path(sys.argv[1]).glob("*.response.json"):
    try:
        d = json.loads(f.read_text())
        body = d.get("body", "")
        if d.get("status") == 404 and isinstance(body, str) and "not_found_error" in body:
            print("yes"); sys.exit(0)
    except Exception:
        pass
PY
}
_version_gte() {
    python3 - "$VERSION" "$1" <<'PY'
import sys
def v(s): return tuple(int(x) for x in s.split(".") if x.isdigit())
sys.exit(0 if v(sys.argv[1]) >= v(sys.argv[2]) else 1)
PY
}
if [[ "$(_raw_has_model_404)" == "yes" ]] && _version_gte "1.0.0"; then
    echo "[retry] model 404 — retrying with --model claude-sonnet-4-5"
    rm -rf "$RAW_DIR"
    mkdir -p "$RAW_DIR"
    "${REPO_DIR}/sandbox/run.sh" \
        "$VERSION" \
        -o "$RAW_DIR" \
        -s "$SCENARIO" \
        ${EXTRA_FLAGS[@]+"${EXTRA_FLAGS[@]}"} \
        -- ${CLAUDE_ARGS[@]+"${CLAUDE_ARGS[@]}"} --model claude-sonnet-4-5 "$PROMPT"
fi

# Defensive flatten — entrypoint.sh already lifts files out of agentlens'
# timestamped subdir before the container exits, so this should be a no-op.
# Kept here for older container images / orphans from interrupted prior runs.
shopt -s nullglob
for ts in "$RAW_DIR"/*/; do
    case "$(basename "$ts")" in
        raw) continue ;;
    esac
    if [[ -d "${ts}raw" ]]; then
        mv "${ts}raw"/* "$RAW_DIR/" 2>/dev/null || true
        rmdir "${ts}raw" 2>/dev/null || true
    fi
    mv "${ts}"* "$RAW_DIR/" 2>/dev/null || true
    rmdir "${ts%/}" 2>/dev/null || true
done
shopt -u nullglob

# Strip claude.ai-account connectors and email PII from the raw bytes.
# entrypoint.sh empties the local cache, but Claude Code re-fetches the
# account profile + connector list from the API on every session and the
# deferred-tools list in the first user message echoes them back. The
# scrubber removes those substrings without touching anything else.
python3 "${REPO_DIR}/scripts/scrub-leaks.py" "$RAW_DIR" >/dev/null
