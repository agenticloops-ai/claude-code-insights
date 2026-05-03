#!/usr/bin/env python3
"""Minimal stdio MCP server for sandbox scenarios.

Speaks just enough JSON-RPC over stdin/stdout to advertise N synthetic tools
to claude-code, where N is set by FIXTURE_TOOL_COUNT (default 3). This lets
us track:

- how MCP tools land in the system prompt / tools array
- the threshold at which claude-code switches to deferred ToolSearch
- per-tool naming/schema conventions (e.g. mcp__<server>__<tool>)

Tool calls return a deterministic placeholder so we can also probe how
results are surfaced if a scenario actually invokes one.
"""
from __future__ import annotations

import json
import os
import sys

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = os.environ.get("FIXTURE_SERVER_NAME", "fixture")
SERVER_VERSION = "1.0.0"


def _tools(count: int) -> list[dict]:
    tools = []
    for i in range(1, count + 1):
        name = f"tool_{i:03d}"
        tools.append(
            {
                "name": name,
                "description": (
                    f"Synthetic fixture tool #{i}. Echoes the supplied 'text' "
                    "argument in its response. Exists only so claude-code "
                    "registers a deterministic, version-comparable MCP tool."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to echo back.",
                        }
                    },
                    "required": ["text"],
                    "additionalProperties": False,
                },
            }
        )
    return tools


def _send(message: dict) -> None:
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def _result(req_id, result) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def _error(req_id, code: int, message: str) -> None:
    _send(
        {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }
    )


def main() -> int:
    tool_count = int(os.environ.get("FIXTURE_TOOL_COUNT", "3"))
    tools = _tools(tool_count)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method")
        req_id = msg.get("id")

        # Notifications have no id and expect no response.
        if method == "notifications/initialized":
            continue
        if method == "notifications/cancelled":
            continue

        if method == "initialize":
            _result(
                req_id,
                {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {
                        "name": SERVER_NAME,
                        "version": SERVER_VERSION,
                    },
                },
            )
        elif method == "tools/list":
            _result(req_id, {"tools": tools})
        elif method == "tools/call":
            params = msg.get("params") or {}
            tname = params.get("name", "")
            args = params.get("arguments") or {}
            text = args.get("text", "")
            _result(
                req_id,
                {
                    "content": [
                        {"type": "text", "text": f"{tname} echo: {text}"}
                    ],
                    "isError": False,
                },
            )
        elif method == "ping":
            _result(req_id, {})
        elif method == "shutdown":
            _result(req_id, {})
            return 0
        elif req_id is not None:
            _error(req_id, -32601, f"Method not found: {method}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
