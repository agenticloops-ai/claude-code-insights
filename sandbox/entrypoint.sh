#!/usr/bin/env bash
# Container entrypoint.
#
# Two modes, selected by $CAPTURE_MODE:
#   capture (default) - boot agentlens, set HTTP_PROXY, exec the agent
#   login             - skip agentlens, exec the agent directly so you can
#                       complete OAuth (sandbox/login.sh sets this)
set -euo pipefail

MODE="${CAPTURE_MODE:-capture}"

# Disable interactive prompts. Older claude versions (0.2.x) try to show an
# Ink-based "Enable automatic updates?" picker the first time they run with a
# writable npm prefix; without a TTY this crashes with "Raw mode is not
# supported on the current process.stdin". Newer versions honor CI=1 too.
export DISABLE_AUTOUPDATER=1
export CI=1

# Sandbox MCP fixture + leak prevention.
#
# 1. Force mcpServers to be EXACTLY the fixture map (replace, not merge) so
#    no account-installed server can survive into the next capture.
# 2. Empty claudeAiMcpEverConnected — when this list is non-empty, Claude
#    Code asks the API for the user's account-attached claude.ai connectors
#    (Gmail, Canva, Figma, …) and exposes them as deferred mcp__claude_ai_*
#    tools, polluting cross-version diffs.
# 3. Strip identifying fields from oauthAccount (emailAddress, displayName,
#    organizationName) so the harness "userEmail" reminder and any echoed
#    account profile don't leak the real owner's PII into captures. Routing
#    fields (accountUuid, organizationUuid) are kept so the API client keeps
#    working.
# Idempotent — safe to run on every container start.
FIXTURE_MCP="/opt/fixtures/mcp-default.json"
if [[ -d "$HOME" && -f "$FIXTURE_MCP" ]]; then
    FIXTURE_MCP="$FIXTURE_MCP" python3 - <<'PY'
import json, os, pathlib
home = pathlib.Path(os.environ["HOME"])
cfg_path = home / ".claude.json"
fixture = json.loads(pathlib.Path(os.environ["FIXTURE_MCP"]).read_text())
cfg = {}
if cfg_path.exists():
    try:
        cfg = json.loads(cfg_path.read_text() or "{}")
    except Exception:
        cfg = {}

cfg["mcpServers"] = dict(fixture.get("mcpServers", {}))
cfg["claudeAiMcpEverConnected"] = []

acc = cfg.get("oauthAccount") or {}
if acc:
    pii_keys = {"emailAddress", "displayName", "organizationName"}
    cfg["oauthAccount"] = {k: v for k, v in acc.items() if k not in pii_keys}

cfg_path.write_text(json.dumps(cfg, indent=2))

# .claude.json.backup mirrors the live file and is recreated by Claude on
# next write, but it can carry stale PII forward; remove it.
backup = home / ".claude.json.backup"
if backup.exists():
    backup.unlink()
PY
fi

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
        "$HOME/.claude/__store.db" \
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

flatten_output() {
    # agentlens writes session files into $OUTPUT_DIR/<timestamp>/ (and a
    # nested raw/ for per-request files). Lift everything up one level so
    # consumers find <scenario>.json + per-request *.json directly under
    # $OUTPUT_DIR. Idempotent; safe to call multiple times.
    shopt -s nullglob
    for ts in "$OUTPUT_DIR"/*/; do
        # Skip a non-timestamp subdir (e.g. raw/ that we already lifted).
        case "$(basename "$ts")" in
            raw) continue ;;
        esac
        if [[ -d "${ts}raw" ]]; then
            mv "${ts}raw"/* "$OUTPUT_DIR/" 2>/dev/null || true
            rmdir "${ts}raw" 2>/dev/null || true
        fi
        mv "${ts}"* "$OUTPUT_DIR/" 2>/dev/null || true
        rmdir "${ts%/}" 2>/dev/null || true
    done
    shopt -u nullglob
}

cleanup() {
    if kill -0 "$AGENTLENS_PID" 2>/dev/null; then
        kill -INT "$AGENTLENS_PID" 2>/dev/null || true
        # Bound the wait — agentlens normally flushes in <2s. If it hangs
        # (proxy mid-stream), give it 12s then SIGTERM, then move on.
        for _ in $(seq 1 24); do
            kill -0 "$AGENTLENS_PID" 2>/dev/null || break
            sleep 0.5
        done
        kill -TERM "$AGENTLENS_PID" 2>/dev/null || true
        wait "$AGENTLENS_PID" 2>/dev/null || true
    fi
    flatten_output
}
trap cleanup EXIT
# docker stop sends SIGTERM to PID 1; without an explicit handler bash exits
# without running the EXIT trap. Forward TERM to the agent (so it can shut
# down cleanly) then let cleanup() flush agentlens on the way out.
trap 'kill -TERM "$AGENT_PID" 2>/dev/null || true' TERM INT

"$@" &
AGENT_PID=$!
wait "$AGENT_PID" 2>/dev/null
AGENT_RC=$?
exit "$AGENT_RC"
