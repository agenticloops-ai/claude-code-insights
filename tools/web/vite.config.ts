import { defineConfig } from "vite";
import preact from "@preact/preset-vite";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";

// The web app needs to read the captured artifacts from versions/. We
// expose them via a tiny dev-server middleware that mirrors the on-disk
// layout under /api/*. For production build (`npm run build`), the same
// data is dumped to public/data/ so the bundle is fully static.
const REPO_DIR = resolve(__dirname, "..", "..");
const VERSIONS_DIR = join(REPO_DIR, "versions");

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
    .sort((a, b) => a.dirName.localeCompare(b.dirName));
}

export default defineConfig({
  plugins: [
    preact(),
    {
      name: "cci-versions-api",
      configureServer(server) {
        // GET /api/versions                     → version index
        // GET /api/v/<dirName>                  → single-version bundle
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
            res.end(
              JSON.stringify({
                dirName,
                manifest: readJsonOr(join(dir, "manifest.json"), null),
                tools: readJsonOr(join(dir, "tools.json"), []),
                deferredTools: readJsonOr(join(dir, "deferred-tools.json"), []),
                skills: readJsonOr(join(dir, "skills.json"), []),
                systemPrompt: readTextOr(join(dir, "system-prompt.md")),
                userPrompt: readTextOr(join(dir, "user-prompt.md")),
                releaseNotes: readTextOr(join(dir, "release-notes.md")),
              }),
            );
            return;
          }
          next();
        });
      },
    },
  ],
});
