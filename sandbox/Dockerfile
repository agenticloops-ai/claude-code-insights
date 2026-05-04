# Reproducible sandbox for capturing Claude Code CLI behavior across releases.
#
# Build with a pinned Claude Code version:
#   docker build --build-arg CLAUDE_VERSION=2.1.5 -t cch:2.1.5 sandbox/
#
# Both Claude Code and AgentLens (the MITM proxy that records the traffic) live
# *inside* the image so the only host dependency is Docker itself. The image
# contains no MCP servers, no skills, and no user config — those are mounted
# in at run time from sandbox/fixtures/. OAuth credentials live in a named
# Docker volume and are populated once via sandbox/login.sh.

FROM node:20-bookworm-slim

ARG CLAUDE_VERSION
ARG AGENTLENS_VERSION=0.1.12
ENV CLAUDE_VERSION=${CLAUDE_VERSION}
ENV AGENTLENS_VERSION=${AGENTLENS_VERSION}

# Pin locale, timezone, and hostname so the system prompt's environment block
# is byte-identical across runs on different machines.
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TZ=UTC \
    DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        tini \
        tzdata \
        git \
        python3 \
        python3-pip \
        python3-venv \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && rm -rf /var/lib/apt/lists/*

RUN if [ -z "$CLAUDE_VERSION" ]; then \
        echo "ERROR: --build-arg CLAUDE_VERSION=<version> is required" >&2; exit 1; \
    fi \
    && npm install -g --no-fund --no-audit \
        "@anthropic-ai/claude-code@${CLAUDE_VERSION}"

# AgentLens lives in its own venv to keep system Python clean.
RUN python3 -m venv /opt/agentlens \
    && /opt/agentlens/bin/pip install --upgrade pip \
    && if [ -n "$AGENTLENS_VERSION" ]; then \
           /opt/agentlens/bin/pip install "agentlens-proxy==${AGENTLENS_VERSION}"; \
       else \
           /opt/agentlens/bin/pip install "agentlens-proxy"; \
       fi \
    && ln -s /opt/agentlens/bin/agentlens /usr/local/bin/agentlens

# Deterministic non-root user. node:20-bookworm-slim already ships a `node`
# user at uid/gid 1000; rename it to `runner` and move its home so paths are
# stable across base-image refreshes.
RUN groupmod -n runner node \
    && usermod -l runner -d /home/runner -m -s /bin/bash node \
    && mkdir -p /home/runner /work /results \
    && chown -R runner:runner /home/runner /work /results

# Make the global npm prefix writable to runner. Older claude versions (0.2.x)
# show an interactive "Enable automatic updates?" Ink prompt the first time
# they run with a read-only npm prefix; without a TTY it crashes the agent
# with "Raw mode is not supported on the current process.stdin". The prompt's
# own recommended fix is `chown -R $USER /usr/local && chmod -R u+w /usr/local`,
# so we apply exactly that scope at build time.
RUN chown -R runner:runner /usr/local && chmod -R u+w /usr/local

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER runner
WORKDIR /work

# AgentLens will generate the mitmproxy CA into the (volume-backed) home dir
# at first run; entrypoint waits for it and sets NODE_EXTRA_CA_CERTS.

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]
CMD ["claude", "--version"]
