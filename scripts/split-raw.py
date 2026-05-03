#!/usr/bin/env python3
"""Split raw captures out of an agentlens session.json into per-request files.

Usage:
    scripts/split-raw.py <session.json>

Writes <session-dir>/NNN.request.json, NNN.response.json, NNN.sse.json
alongside the session file.

Temporary helper while the upstream agentlens "raw" export format ships.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(args: list[str]) -> int:
    if len(args) != 2:
        print("usage: split-raw.py <session.json>", file=sys.stderr)
        return 1

    src = Path(args[1])
    data = json.loads(src.read_text())
    raw = data.get("raw_captures") or []
    if not raw:
        print("no raw_captures in session.json", file=sys.stderr)
        return 1

    out_dir = src.parent

    for idx, cap in enumerate(raw, start=1):
        prefix = f"{idx:03d}"

        request_doc = {
            "index": idx,
            "request_id": cap.get("id"),
            "session_id": cap.get("session_id"),
            "timestamp": cap.get("timestamp"),
            "provider": cap.get("provider"),
            "method": cap.get("request_method"),
            "url": cap.get("request_url"),
            "headers": cap.get("request_headers", {}),
            "body": cap.get("request_body"),
        }
        (out_dir / f"{prefix}.request.json").write_text(
            json.dumps(request_doc, indent=2, default=str)
        )

        response_doc = {
            "index": idx,
            "request_id": cap.get("id"),
            "status": cap.get("response_status"),
            "headers": cap.get("response_headers", {}),
            "is_streaming": cap.get("is_streaming"),
            "body": cap.get("response_body"),
        }
        (out_dir / f"{prefix}.response.json").write_text(
            json.dumps(response_doc, indent=2, default=str)
        )

        sse = cap.get("sse_events") or []
        if sse:
            (out_dir / f"{prefix}.sse.json").write_text(
                json.dumps(sse, indent=2, default=str)
            )

    print(f"wrote {len(raw)} request(s) to {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
