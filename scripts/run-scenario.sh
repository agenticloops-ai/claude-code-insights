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

# MCP isolation strategy:
#
# - 0.2.93+ supports `--mcp-config <file>` so the agent reads ONLY the
#   fixture map and ignores anything in ~/.claude.json's mcpServers.
# - 1.0.44+ supports `--strict-mcp-config` which also blocks claude.ai
#   account connectors and any other config source from leaking in.
#
# When the version is below the floor we fall back to entrypoint.sh
# merging the fixture into ~/.claude.json (see FALLBACK_MCP_MERGE=1
# below). Local-mode scenarios (--help) don't need MCP at all.
SUPPORTS_MCP_CONFIG="$(python3 - "$VERSION" "0.2.93" <<'PY'
import sys
def v(s): return tuple(int(x) for x in s.split(".") if x.isdigit())
print("yes" if v(sys.argv[1]) >= v(sys.argv[2]) else "no")
PY
)"
SUPPORTS_STRICT_MCP_CONFIG="$(python3 - "$VERSION" "1.0.44" <<'PY'
import sys
def v(s): return tuple(int(x) for x in s.split(".") if x.isdigit())
print("yes" if v(sys.argv[1]) >= v(sys.argv[2]) else "no")
PY
)"

CLAUDE_MCP_FLAGS=()
if [[ "$MODE" == "agent" ]]; then
    if [[ "$SUPPORTS_MCP_CONFIG" == "yes" ]]; then
        CLAUDE_MCP_FLAGS+=("--mcp-config" "/opt/fixtures/mcp-default.json")
    fi
    if [[ "$SUPPORTS_STRICT_MCP_CONFIG" == "yes" ]]; then
        CLAUDE_MCP_FLAGS+=("--strict-mcp-config")
    fi
    if [[ "$SUPPORTS_MCP_CONFIG" != "yes" ]]; then
        # No --mcp-config support; fall back to merging fixture into
        # ~/.claude.json via entrypoint.sh.
        EXTRA_FLAGS+=(-e "FALLBACK_MCP_MERGE=1")
    fi
fi

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

_run_capture() {
    local extra_model_flag=("$@")
    "${REPO_DIR}/sandbox/run.sh" \
        "$VERSION" \
        -o "$RAW_DIR" \
        -s "$SCENARIO" \
        ${EXTRA_FLAGS[@]+"${EXTRA_FLAGS[@]}"} \
        -- ${CLAUDE_ARGS[@]+"${CLAUDE_ARGS[@]}"} \
        ${CLAUDE_MCP_FLAGS[@]+"${CLAUDE_MCP_FLAGS[@]}"} \
        ${extra_model_flag[@]+"${extra_model_flag[@]}"} \
        "$PROMPT"
}

# Detect a degenerate capture (no /v1/messages with tools, or all
# requests <2). 2.0.46–2.0.76 are flaky: claude exits with "Execution
# error" on a non-trivial fraction of runs even outside the proxy. We
# retry up to N times; first successful run wins.
_capture_looks_complete() {
    python3 - "$RAW_DIR" <<'PY'
import json, sys
from pathlib import Path
raw = Path(sys.argv[1])
# Find the agentlens session export (<scenario>.json).
session_files = list(raw.glob("*.json"))
session = None
for f in session_files:
    if f.name.endswith(".request.json") or f.name.endswith(".response.json"):
        continue
    try:
        d = json.loads(f.read_text())
    except Exception:
        continue
    if isinstance(d, dict) and "requests" in d and "raw_captures" in d:
        session = d
        break

if not session:
    print("no")
    sys.exit(0)

requests = session.get("requests") or []
# We want at least one request that carries the agent's system prompt /
# tools — the haiku-quota probe (max_tokens=1, no tools, no system) does
# not count. Look for any request with non-empty `tools` OR a non-empty
# `system_prompt`.
for r in requests:
    sp = r.get("system_prompt") or ""
    tools = r.get("tools") or []
    if tools or (isinstance(sp, str) and len(sp) > 100):
        print("yes")
        sys.exit(0)
    if isinstance(sp, list) and any(isinstance(s, dict) and len(s.get("text") or "") > 100 for s in sp):
        print("yes")
        sys.exit(0)

print("no")
PY
}

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

# First attempt.
_run_capture

# Retry with --model fallback on retired-model 404.
if [[ "$(_raw_has_model_404)" == "yes" ]] && _version_gte "1.0.0"; then
    echo "[retry] model 404 — retrying with --model claude-sonnet-4-5"
    rm -rf "$RAW_DIR"
    mkdir -p "$RAW_DIR"
    _run_capture --model claude-sonnet-4-5
fi

# Flaky-version retry: up to 8 extra attempts when the capture is
# incomplete (claude printed "Execution error" before the main session
# call landed). Only kicks in when the first attempt produced no
# tool-bearing request. claude-code 2.0.46 through 2.0.76 fail on a
# non-trivial fraction of runs even outside the proxy — observed success
# rate ~25%, so 8 retries gets to ~90% confidence. Each extra attempt is
# ~30s when the docker image is already cached.
RETRY_LIMIT="${SCENARIO_RETRY_LIMIT:-8}"
if [[ "$(_capture_looks_complete)" != "yes" ]]; then
    for attempt in $(seq 1 "$RETRY_LIMIT"); do
        echo "[retry] capture looks incomplete (no tool-bearing request) — retry $attempt/$RETRY_LIMIT"
        rm -rf "$RAW_DIR"
        mkdir -p "$RAW_DIR"
        _run_capture
        if [[ "$(_capture_looks_complete)" == "yes" ]]; then
            echo "[retry] success on attempt $attempt"
            break
        fi
    done
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
