#!/usr/bin/env bash
# Container entrypoint.
#
# Two modes, selected by $CAPTURE_MODE:
#   capture (default) - boot agentlens, set HTTP_PROXY, exec the agent
#   login             - skip agentlens, exec the agent directly so you can
#                       complete OAuth (sandbox/login.sh sets this)
set -euo pipefail

MODE="${CAPTURE_MODE:-capture}"

if [[ "$MODE" == "login" || "$MODE" == "local" ]]; then
    # No agentlens — used for `claude login` and for "local" scenarios that
    # capture deterministic stdout (--help, --version, mcp subcommands, etc.).
    exec "$@"
fi

# Wipe transient state from the auth volume so no scenario can leak data into
# the next one. Auth credentials and the mitmproxy CA are intentionally kept;
# everything else claude-code or agentlens may have written is removed.
# Set CAPTURE_KEEP_STATE=1 to skip (useful when debugging a specific scenario).
if [[ "${CAPTURE_KEEP_STATE:-0}" != "1" ]]; then
    rm -rf \
        "$HOME/.claude/projects" \
        "$HOME/.claude/sessions" \
        "$HOME/.claude/plans" \
        "$HOME/.claude/todos" \
        "$HOME/.claude/cache" \
        "$HOME/.claude/session-env" \
        "$HOME/.claude/backups" \
        "$HOME/.claude/shell-snapshots" \
        "$HOME/.claude/debug" \
        "$HOME/.claude/plugins" \
        "$HOME/.claude/mcp-needs-auth-cache.json" \
        "$HOME/.agentlens" \
        "$HOME/.cache/claude-cli-nodejs" \
        2>/dev/null || true
fi

OUTPUT_DIR="${CAPTURE_OUTPUT_DIR:-/results}"
SESSION_NAME="${CAPTURE_SESSION_NAME:-capture}"
PROXY_PORT="${AGENTLENS_PROXY_PORT:-8080}"
WEB_PORT="${AGENTLENS_WEB_PORT:-8081}"

mkdir -p "$OUTPUT_DIR"

agentlens wait \
    --output "$OUTPUT_DIR" \
    --session-name "$SESSION_NAME" \
    --proxy-port "$PROXY_PORT" \
    --web-port "$WEB_PORT" \
    --no-web \
    --no-open \
    >"$OUTPUT_DIR/agentlens.log" 2>&1 &
AGENTLENS_PID=$!

# Wait for proxy port.
for _ in $(seq 1 60); do
    if (echo > "/dev/tcp/127.0.0.1/${PROXY_PORT}") 2>/dev/null; then
        break
    fi
    if ! kill -0 "$AGENTLENS_PID" 2>/dev/null; then
        echo "ERROR: agentlens exited before proxy was ready" >&2
        cat "$OUTPUT_DIR/agentlens.log" >&2 || true
        exit 1
    fi
    sleep 0.5
done

# Wait for the mitmproxy CA cert to be generated (first run only).
CA_CERT="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
for _ in $(seq 1 60); do
    [[ -f "$CA_CERT" ]] && break
    sleep 0.5
done
if [[ ! -f "$CA_CERT" ]]; then
    echo "ERROR: mitmproxy CA cert never appeared at $CA_CERT" >&2
    exit 1
fi

export HTTP_PROXY="http://127.0.0.1:${PROXY_PORT}"
export HTTPS_PROXY="$HTTP_PROXY"
export ALL_PROXY="$HTTP_PROXY"
export NO_PROXY="localhost,127.0.0.1"
export NODE_EXTRA_CA_CERTS="$CA_CERT"
export SSL_CERT_FILE="$CA_CERT"

cleanup() {
    if kill -0 "$AGENTLENS_PID" 2>/dev/null; then
        kill -INT "$AGENTLENS_PID" 2>/dev/null || true
        wait "$AGENTLENS_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

"$@"
