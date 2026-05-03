#!/usr/bin/env bash
# Build cch:<version> if it doesn't already exist.
#   sandbox/build.sh <claude-version>
set -euo pipefail

CLAUDE_VERSION="${1:?usage: build.sh <claude-version>}"
SANDBOX_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="cch:${CLAUDE_VERSION}"

if docker image inspect "$IMAGE" >/dev/null 2>&1; then
    exit 0
fi

echo ">>> building $IMAGE"
BUILD_ARGS=(--build-arg "CLAUDE_VERSION=${CLAUDE_VERSION}")
if [[ -n "${AGENTLENS_VERSION:-}" ]]; then
    BUILD_ARGS+=(--build-arg "AGENTLENS_VERSION=${AGENTLENS_VERSION}")
fi

docker build "${BUILD_ARGS[@]}" -t "$IMAGE" "$SANDBOX_DIR"
