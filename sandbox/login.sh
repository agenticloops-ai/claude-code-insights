#!/usr/bin/env bash
# One-time interactive login: starts the sandbox image with the cch-auth
# volume mounted and runs `claude` so you can complete the OAuth flow.
# Credentials persist in the volume and are reused by every subsequent run.sh
# invocation, regardless of which Claude Code version it pins.
#
#   sandbox/login.sh <claude-version>
#
# When the OAuth handshake finishes, exit claude (Ctrl+C or /exit) — the
# volume now holds your subscription credentials.

set -euo pipefail

if [[ $# -lt 1 || "${1:-}" == "--help" ]]; then
    echo "usage: $0 <claude-version>" >&2
    exit 1
fi

CLAUDE_VERSION="$1"
SANDBOX_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

IMAGE="cch:${CLAUDE_VERSION}"
"$SANDBOX_DIR/build.sh" "$CLAUDE_VERSION"

docker volume inspect cch-auth >/dev/null 2>&1 || docker volume create cch-auth >/dev/null

echo ">>> launching $IMAGE for OAuth login"
echo ">>> when prompted, open the URL on your host browser, paste the code back, then exit claude"

exec docker run --rm -it \
    --hostname sandbox \
    --mount "type=volume,src=cch-auth,dst=/home/runner" \
    -e "CAPTURE_MODE=login" \
    "$IMAGE" \
    claude
