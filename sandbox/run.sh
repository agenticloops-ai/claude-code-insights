#!/usr/bin/env bash
# Run a single Claude Code scenario inside the sandbox container.
#
#   sandbox/run.sh <claude-version> [-o <results-dir>] [-s <session-name>] \
#                  [--mode <agent|local>] \
#                  [-e KEY=VAL ...] -- <claude-args...>
#
# Examples:
#   # bare scenario — only the default fixture MCP server (1 demo tool)
#   sandbox/run.sh 2.1.126 -- -p "hi"
#
#   # scenario that adds its own MCP server on top of the default fixture
#   sandbox/run.sh 2.1.126 -- -p "list tools"   # fixture MCP is always loaded
#
# Auth: uses the named docker volume "cch-auth" (populated once via login.sh).
# Override with CCH_AUTH_VOLUME=<name> to use a different volume.
#
# Timeout: set CAPTURE_TIMEOUT_SECS=<n> to kill the container after n seconds.
# Default is no timeout. Exit code 124 signals a timeout.
#
# MCP: the sandbox MCP fixture (sandbox/fixtures/mcp-default.json — server
# "fixture", 3 tools) is registered by entrypoint.sh merging it into
# ~/.claude.json on container start. Claude reads it natively; no --mcp-config
# flag, no /tmp bind-mount. There is no per-scenario MCP override.
# claude.ai account-level connectors don't reach the sandbox because the
# auth volume only contains OAuth credentials, not the connector cache.
#
# Skills: sandbox/fixtures/skills/ is always bind-mounted readonly to
# ~/.claude/skills/ inside the container so every scenario sees the same
# fixture skill set.

set -euo pipefail

if [[ $# -lt 1 || "${1:-}" == "--help" ]]; then
    cat >&2 <<'EOF'
usage: run.sh <claude-version> [-o <results-dir>] [-s <session-name>]
              [--mode agent|local]
              [-e KEY=VAL ...] -- <claude-args...>

env:
  CCH_AUTH_VOLUME      Docker volume name for auth state (default: cch-auth)
  CAPTURE_TIMEOUT_SECS Kill container after this many seconds (default: none)
  AGENTLENS_VERSION    optional pin for agentlens-proxy (build-time only)

If the auth volume is empty, run sandbox/login.sh <version> first.
EOF
    exit 1
fi

CLAUDE_VERSION="$1"; shift

SANDBOX_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SANDBOX_DIR")"

RESULTS_DIR=""
SESSION_NAME="capture"
MODE="agent"   # "agent" = capture via agentlens; "local" = no proxy, just stdout
EXTRA_ENV_ARGS=()

# Auth volume — override with CCH_AUTH_VOLUME env for alternative volumes.
AUTH_VOLUME="${CCH_AUTH_VOLUME:-cch-auth}"

# Per-container timeout (seconds). 0 = no timeout.
TIMEOUT_SECS="${CAPTURE_TIMEOUT_SECS:-0}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o) RESULTS_DIR="$2"; shift 2 ;;
        -s) SESSION_NAME="$2"; shift 2 ;;
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

docker volume inspect "$AUTH_VOLUME" >/dev/null 2>&1 || docker volume create "$AUTH_VOLUME" >/dev/null
if ! docker run --rm --mount "type=volume,src=${AUTH_VOLUME},dst=/h" alpine:3 \
        sh -c 'test -e /h/.claude.json -o -d /h/.claude' >/dev/null 2>&1; then
    echo "WARN: ${AUTH_VOLUME} volume looks empty — run sandbox/login.sh ${CLAUDE_VERSION} first" >&2
fi

# Bind-mount the fixture-mcp.py script and the source-of-truth MCP config.
# entrypoint.sh reads /opt/fixtures/mcp-default.json and patches ~/.claude.json
# on every container start so claude picks up the servers natively.
MCP_MOUNT_ARGS=(
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/mcp,dst=/opt/fixtures/mcp,readonly"
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/mcp-default.json,dst=/opt/fixtures/mcp-default.json,readonly"
)

# Default fixture skill always mounted so the baseline shows skill discovery.
SKILL_MOUNT_ARGS=(
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/skills,dst=/home/runner/.claude/skills,readonly"
)

echo ">>> running $IMAGE [$MODE] (results -> $RESULTS_DIR)" >&2

# ---------------------------------------------------------------------------
# Helper: run docker with optional timeout.
# If TIMEOUT_SECS > 0, starts detached and polls; kills on deadline; exits 124.
# If TIMEOUT_SECS == 0, exec's interactively (original behaviour).
# ---------------------------------------------------------------------------
_docker_run() {
    if [[ "${TIMEOUT_SECS}" -gt 0 ]]; then
        # Remove --rm from args: detached containers must be cleaned up manually
        # so we can read their exit code (and stream their logs) before they
        # disappear.
        local filtered=()
        for a in "$@"; do [[ "$a" == "--rm" ]] || filtered+=("$a"); done

        local cid
        cid=$(docker run -d "${filtered[@]}")
        # Stream container stdout/stderr to host stdout/stderr in real time
        # so callers (e.g. local-mode capture, which redirects host stdout to
        # output.txt) get the same byte stream as the foreground path.
        docker logs -f "$cid" &
        local logs_pid=$!

        local deadline=$(( $(date +%s) + TIMEOUT_SECS ))
        while true; do
            local st
            st=$(docker inspect --format '{{.State.Status}}' "$cid" 2>/dev/null || echo "gone")
            if [[ "$st" != "running" && "$st" != "created" ]]; then
                wait "$logs_pid" 2>/dev/null || true
                local rc
                rc=$(docker inspect --format '{{.State.ExitCode}}' "$cid" 2>/dev/null || echo 1)
                docker rm -f "$cid" >/dev/null 2>&1 || true
                return "$rc"
            fi
            if (( $(date +%s) >= deadline )); then
                # Use docker stop (SIGTERM + grace) so entrypoint.sh's EXIT
                # trap fires — agentlens needs SIGINT to flush its session
                # export and our flatten step needs to run. SIGKILL bypasses
                # both. 15s grace is enough for agentlens to write its JSON.
                echo ">>> TIMEOUT (${TIMEOUT_SECS}s) — stopping $cid (15s grace for agentlens flush)" >&2
                docker stop -t 15 "$cid" >/dev/null 2>&1 || true
                wait "$logs_pid" 2>/dev/null || true
                docker rm -f "$cid" >/dev/null 2>&1 || true
                return 124
            fi
            sleep 2
        done
    else
        exec docker run -i "$@"
    fi
}

if [[ "$MODE" == "local" ]]; then
    # No agentlens, no /results mount — caller captures stdout directly.
    _docker_run --rm \
        --hostname sandbox \
        --mount "type=volume,src=${AUTH_VOLUME},dst=/home/runner" \
        --mount "type=bind,src=${SANDBOX_DIR}/fixtures/home/.claude/settings.json,dst=/home/runner/.claude/settings.json,readonly" \
        --mount "type=bind,src=${SANDBOX_DIR}/fixtures/workdir,dst=/work,readonly" \
        ${MCP_MOUNT_ARGS[@]+"${MCP_MOUNT_ARGS[@]}"} \
        ${SKILL_MOUNT_ARGS[@]+"${SKILL_MOUNT_ARGS[@]}"} \
        ${EXTRA_ENV_ARGS[@]+"${EXTRA_ENV_ARGS[@]}"} \
        -e "CAPTURE_MODE=local" \
        "$IMAGE" \
        claude "$@"
    exit $?
fi

# Agent mode: full agentlens capture.
_docker_run --rm \
    --hostname sandbox \
    --mount "type=volume,src=${AUTH_VOLUME},dst=/home/runner" \
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/home/.claude/settings.json,dst=/home/runner/.claude/settings.json,readonly" \
    --mount "type=bind,src=${SANDBOX_DIR}/fixtures/workdir,dst=/work,readonly" \
    --mount "type=bind,src=${RESULTS_DIR},dst=/results" \
    ${MCP_MOUNT_ARGS[@]+"${MCP_MOUNT_ARGS[@]}"} \
    ${SKILL_MOUNT_ARGS[@]+"${SKILL_MOUNT_ARGS[@]}"} \
    ${EXTRA_ENV_ARGS[@]+"${EXTRA_ENV_ARGS[@]}"} \
    -e "CAPTURE_OUTPUT_DIR=/results" \
    -e "CAPTURE_SESSION_NAME=${SESSION_NAME}" \
    "$IMAGE" \
    claude "$@"
