# `tools/` — CLI and web UI

Two thin TypeScript apps that read the artifacts under `versions/` (produced by
the Python pipeline in `scripts/`) and surface them for ad-hoc browsing /
comparison.

## CLI — `tools/cli/`

```bash
cd tools/cli
npm install
npm run build
./dist/index.js help

# list captured versions
./dist/index.js versions

# print metrics for one version
./dist/index.js show 2.1.128

# compare two versions (semver or dated dirname)
./dist/index.js diff 2.0.45 2.1.128
./dist/index.js diff 2.0.45 2.1.128 --json
./dist/index.js diff 2.0.45 2.1.128 --json --write /tmp/diff.json

# interactive picker (requires a TTY)
./dist/index.js diff
```

The CLI reuses pure-JS diffing (`tools/cli/src/lib/diff.ts`) so the same
result shape is produced on the terminal and in the web UI.

## Web — `tools/web/`

Vite + Preact dev server that exposes the on-disk `versions/` layout via a
small `/api/*` middleware (see `vite.config.ts`) and renders a side-by-side
diff explorer.

```bash
cd tools/web
npm install
npm run dev          # http://localhost:5173

# or, from the CLI:
../cli/dist/index.js serve --port 5173
```

UI: pick two versions in the sidebar (A=from, B=to), the main pane shows
metrics, tool/skill diffs, and unified system/user-prompt diffs.

## Why TypeScript and not Python?

The Python scripts (`scripts/extract.py`, `scripts/diff-versions.py`,
`scripts/summarize-version.py`) own the **capture pipeline**: parsing
agentlens session JSON, scrubbing, and writing the canonical artifacts. The
TypeScript layer here is intentionally **read-only** — it consumes those
artifacts. Sharing the diff logic between CLI and browser is the main reason
to be in JS land for this layer; we keep the heavy ETL in Python where it
already works.
