#!/usr/bin/env bash
# Run a single Claude Code scenario inside the sandbox container.
#
#   sandbox/run.sh <claude-version> [-o <results-dir>] [-s <session-name>] \
#                  [--mcp <path-to-.mcp.json>] [--mode <agent|local>] \
#                  [-e KEY=VAL ...] -- <claude-args...>
#
# Examples:
#   # bare scenario — only the default fixture MCP server (1 demo tool)
#   sandbox/run.sh 2.1.126 -- -p "hi"
#
#   # scenario that adds its own MCP server on top of the default fixture
#   sandbox/run.sh 2.1.126 --mcp scenarios/03-with-mcp-3tools/mcp.json -- -p "list tools"
#
# Auth: uses the named docker volume "cch-auth" (populated once via login.sh).
#
# MCP isolation: --strict-mcp-config keeps account-level claude.ai connectors
# (Canva, Figma, Gmail, etc.) out. We always merge sandbox/fixtures/mcp-default.json
# (the demo server) with the scenario's --mcp file (if any) into a SINGLE
# config we pass to claude — claude-code's `--mcp-config <configs...>` is
# variadic and uses last-wins replacement, so passing the flag twice would
# silently drop the default. The merged file is bind-mounted at
# /tmp/mcp-merged.json inside the container.
#
# Skills: sandbox/fixtures/skills/ is always bind-mounted readonly to
# ~/.claude/skills/ inside the container so every scenario sees the same
# fixture skill set.

set -euo pipefail

if [[ $# -lt 1 || "${1:-}" == "--help" ]]; then
    cat >&2 <<'EOF'
usage: run.sh <claude-version> [-o <results-dir>] [-s <session-name>]
              [--mcp <path-to-.mcp.json>] [--mode agent|local]
              [-e KEY=VAL ...] -- <claude-args...>

env:
  AGENTLENS_VERSION  optional pin for agentlens-proxy (build-time only)

If the cch-auth volume is empty, run sandbox/login.sh <version> first.
EOF
    exit 1
fi

CLAUDE_VERSION="$1"; shift

SANDBOX_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SANDBOX_DIR")"

RESULTS_DIR=""
SESSION_NAME="capture"
MCP_CONFIG=""
MODE="agent"   # "agent" = capture via agentlens; "local" = no proxy, just stdout
EXTRA_ENV_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o) RESULTS_DIR="$2"; shift 2 ;;
        -s) SESSION_NAME="$2"; shift 2 ;;
        --mcp) MCP_CONFIG="$2"; shift 2 ;;
        --mode) MODE="$2"; shift 2 ;;
        -e) EXTRA_ENV_ARGS+=(-e "$2"); shift 2 ;;
        --) shift; break ;;
        *) echo "unknown arg: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$RESULTS_DIR" ]]; then
    RESULTS_DIR="${REPO_DIR}/results/${CLAUDE_VERSION}/${SESSION_NAME}"
fi
mkdir -p "$RESULTS_DIR"
RESULTS_DIR="$(cd "$RESULTS_DIR" && pwd)"

IMAGE="cch:${CLAUDE_VERSION}"
"$SANDBOX_DIR/build.sh" "$CLAUDE_VERSION"

docker volume inspect cch-auth >/dev/null 2>&1 || docker volume create cch-auth >/dev/null
if ! docker run --rm --mount "type=volume,src=cch-auth,dst=/h" alpine:3 \
        sh -c 'test -e /h/.claude.json -o -d /h/.claude' >/dev/null 2>&1; then
    echo "WARN: cch-auth volume looks empty — run sandbox/login.sh ${CLAUDE_VERSION} first" >&2
fi

# MCP isolation: --strict-mcp-config keeps account-level claude.ai connectors
# out. We always include the default fixture ("demo", 1 tool) so the baseline
# shows how MCP gets registered. Scenarios may add more via --mcp. Because
# claude-code's `--mcp-config <configs...>` is variadic and uses last-wins
# replacement, we merge default + scenario into a single JSON file rather than
# passing the flag twice.
MERGED_MCP_HOST="$(mktemp -t cch-mcp-merged.XXXXXX.json)"
trap 'rm -f "$MERGED_MCP_HOST"' EXIT

MCP_HOST_PATH=""
if [[ -n "$MCP_CONFIG" ]]; then
    MCP_HOST_PATH="$(cd "$(dirname "$MCP_CONFIG")" && pwd)/$(basename "$MCP_CONFIG")"
    if [[ ! -f "$MCP_HOST_PATH" ]]; then
        echo "ERROR: --mcp file not found: $MCP_HOST_PATH" >&2
        exit 1
    fi
fi

python3 - "$SANDBOX_DIR/fixtures/mcp-default.json" "$MCP_HOST_PATH" "$MERGED_MCP_HOST" <<'PY'
import json, sys
base_path, extra_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
base = json.load(open(base_path))
base.setdefault("mcpServers", {})
if extra_path:
    extra = json.load(open(extra_path))
    base["mcpServers"].update(extra.get("mcpServers", {}))
json.dump(base, open(out_path, "w"), indent=2)
PY

MCP_MOUNT_ARGS=(
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/mcp,dst=/opt/fixtures/mcp,readonly"
    --mount "type=bind,src=${MERGED_MCP_HOST},dst=/tmp/mcp-merged.json,readonly"
)

# Probe the image's `claude --help` to see which MCP flags it supports. Older
# claude versions (0.2.x, early 1.0.x) lack --strict-mcp-config and only accept
# a single --mcp-config <file>. Pass only what's available so older binaries
# don't error with "unknown option".
HELP_TEXT="$(docker run --rm --entrypoint claude "$IMAGE" --help 2>&1 || true)"
MCP_FLAGS=()
if grep -q -- "--strict-mcp-config" <<<"$HELP_TEXT"; then
    MCP_FLAGS+=("--strict-mcp-config")
fi
if grep -q -- "--mcp-config" <<<"$HELP_TEXT"; then
    MCP_FLAGS+=("--mcp-config" "/tmp/mcp-merged.json")
fi

# Default fixture skill always mounted so the baseline shows skill discovery.
SKILL_MOUNT_ARGS=(
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/skills,dst=/home/runner/.claude/skills,readonly"
)

echo ">>> running $IMAGE [$MODE] (results -> $RESULTS_DIR)" >&2

if [[ "$MODE" == "local" ]]; then
    # No agentlens, no /results mount — caller captures stdout directly.
    exec docker run --rm -i \
        --hostname sandbox \
        --mount "type=volume,src=cch-auth,dst=/home/runner" \
        --mount "type=bind,src=${SANDBOX_DIR}/fixtures/home/.claude/settings.json,dst=/home/runner/.claude/settings.json,readonly" \
        --mount "type=bind,src=${SANDBOX_DIR}/fixtures/workdir,dst=/work,readonly" \
        ${MCP_MOUNT_ARGS[@]+"${MCP_MOUNT_ARGS[@]}"} \
        ${SKILL_MOUNT_ARGS[@]+"${SKILL_MOUNT_ARGS[@]}"} \
        ${EXTRA_ENV_ARGS[@]+"${EXTRA_ENV_ARGS[@]}"} \
        -e "CAPTURE_MODE=local" \
        "$IMAGE" \
        claude "$@"
fi

exec docker run --rm -i \
    --hostname sandbox \
    --mount "type=volume,src=cch-auth,dst=/home/runner" \
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/home/.claude/settings.json,dst=/home/runner/.claude/settings.json,readonly" \
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/workdir,dst=/work,readonly" \
    --mount "type=bind,src=${RESULTS_DIR},dst=/results" \
    ${MCP_MOUNT_ARGS[@]+"${MCP_MOUNT_ARGS[@]}"} \
    ${SKILL_MOUNT_ARGS[@]+"${SKILL_MOUNT_ARGS[@]}"} \
    ${EXTRA_ENV_ARGS[@]+"${EXTRA_ENV_ARGS[@]}"} \
    -e "CAPTURE_OUTPUT_DIR=/results" \
    -e "CAPTURE_SESSION_NAME=${SESSION_NAME}" \
    "$IMAGE" \
    claude "${MCP_FLAGS[@]}" "$@"
