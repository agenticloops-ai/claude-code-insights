import { defineConfig } from "vite";
import preact from "@preact/preset-vite";
import { readdirSync, readFileSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

// The web app needs to read the captured artifacts from versions/. In dev,
// we expose them via a tiny middleware under /api/*. For production
// (`npm run build` → GitHub Pages) the same data is emitted as static JSON
// under dist/data/ via the cci-data-emit plugin below.
const REPO_DIR = resolve(__dirname, "..", "..");
const VERSIONS_DIR = join(REPO_DIR, "versions");

// When deploying to https://<owner>.github.io/claude-code-insights/, all
// asset paths need the repo prefix. Use BASE env var to override (e.g. for
// a custom domain set BASE=/ in the workflow).
const PROD_BASE = process.env.BASE ?? "/claude-code-insights/";

function readJsonOr<T>(p: string, fallback: T): T {
  if (!existsSync(p)) return fallback;
  try {
    return JSON.parse(readFileSync(p, "utf8")) as T;
  } catch {
    return fallback;
  }
}
function readTextOr(p: string, fallback = ""): string {
  return existsSync(p) ? readFileSync(p, "utf8") : fallback;
}

function listVersions() {
  return readdirSync(VERSIONS_DIR)
    .filter((n) => /^\d{4}-\d{2}-\d{2}_/.test(n))
    .map((dirName) => {
      const dir = join(VERSIONS_DIR, dirName);
      const [date, ...rest] = dirName.split("_");
      const captured = existsSync(join(dir, "manifest.json"));
      return { dirName, date, version: rest.join("_"), captured };
    })
    .sort((a, b) => b.dirName.localeCompare(a.dirName));
}

function readBundle(dirName: string) {
  const dir = join(VERSIONS_DIR, dirName);
  return {
    dirName,
    manifest: readJsonOr(join(dir, "manifest.json"), null),
    tools: readJsonOr(join(dir, "tools.json"), []),
    deferredTools: readJsonOr(join(dir, "deferred-tools.json"), []),
    skills: readJsonOr(join(dir, "skills.json"), []),
    systemPrompt: readTextOr(join(dir, "system-prompt.md")),
    userPrompt: readTextOr(join(dir, "user-prompt.md")),
    releaseNotes: readTextOr(join(dir, "release-notes.md")),
  };
}

export default defineConfig(({ command }) => ({
  base: command === "build" ? PROD_BASE : "/",
  plugins: [
    preact(),
    {
      name: "cci-versions-api",
      apply: "serve",
      configureServer(server) {
        // GET /api/versions            → version index
        // GET /api/v/<dirName>         → single-version bundle
        server.middlewares.use("/api", (req, res, next) => {
          const url = req.url ?? "/";
          res.setHeader("content-type", "application/json");
          if (url === "/versions" || url === "/versions/") {
            res.end(JSON.stringify(listVersions()));
            return;
          }
          const m = url.match(/^\/v\/([^/?#]+)/);
          if (m) {
            const dirName = decodeURIComponent(m[1]);
            const dir = join(VERSIONS_DIR, dirName);
            if (!existsSync(dir)) {
              res.statusCode = 404;
              res.end(JSON.stringify({ error: "not found" }));
              return;
            }
            res.end(JSON.stringify(readBundle(dirName)));
            return;
          }
          next();
        });
      },
    },
    {
      // Mirrors the /api/* middleware as static JSON in dist/data/ so the
      // production bundle works on Pages without a server.
      name: "cci-data-emit",
      apply: "build",
      closeBundle() {
        const outDir = resolve(__dirname, "dist");
        const dataDir = join(outDir, "data");
        const vDir = join(dataDir, "v");
        mkdirSync(vDir, { recursive: true });

        const versions = listVersions();
        writeFileSync(join(dataDir, "versions.json"), JSON.stringify(versions));

        let captured = 0;
        for (const v of versions) {
          if (!v.captured) continue;
          writeFileSync(
            join(vDir, `${v.dirName}.json`),
            JSON.stringify(readBundle(v.dirName)),
          );
          captured++;
        }
        // eslint-disable-next-line no-console
        console.log(`[cci-data-emit] wrote versions.json + ${captured} bundles → ${dataDir}`);
      },
    },
  ],
}));
