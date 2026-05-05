// Reads the on-disk shape produced by scripts/extract.py and
// scripts/summarize-version.py.
//
// Layout (per version dir under versions/<release-date>_<version>/):
//   manifest.json         aggregate counts
//   system-prompt.md      baseline scenario's system prompt
//   user-prompt.md        baseline first user message reminders
//   tools.json            built-in tools (sorted, normalized)
//   deferred-tools.json   names hidden behind ToolSearch
//   skills.json           [{name, description}]
//   release-notes.md      upstream CHANGELOG entry
//   diff-from-<v>.md      markdown diff vs the previous captured version
//
// We keep this layer dumb: file IO + path resolution. Anything fancier
// (semver compare, diff rendering) lives in callers.
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Shape of manifest.json as written by scripts/summarize-version.py.
//
// `baseline` is a stripped-down summary of the baseline scenario's
// stats; the per-scenario `scenarios.<name>` blocks are the full
// stats.json files keyed by scenario.
export interface Manifest {
  version: string;
  dir_name: string;
  baseline_scenario: string;
  scenarios: Record<string, ScenarioStats | LocalScenarioStats>;
  baseline?: BaselineSummary;
}

export interface BaselineSummary {
  models?: string[];
  tool_count?: number;
  deferred_tool_count?: number;
  mcp_tool_count_advertised?: number;
  mcp_tool_count_deferred?: number;
  system_prompt_chars?: number;
  reminder_count?: number;
  skill_count?: number;
  user_prompt_chars?: number;
}

export interface LocalScenarioStats {
  mode: "local";
  output_chars?: number;
  output_lines?: number;
  exit_code?: number;
}

export interface ScenarioStats {
  mode?: "agent";
  version: string;
  scenario: string;
  request_count: number;
  models?: string[];
  tool_count_first_request?: number;
  deferred_tool_count?: number;
  mcp_tool_count_advertised?: number;
  mcp_tool_count_deferred?: number;
  system_prompt_chars?: number;
  user_prompt_chars?: number;
  skill_count?: number;
  reminder_count?: number;
  tokens?: { input: number; output: number; cache_read: number; cache_creation: number; total: number };
  duration_ms_total?: number;
  captured_at?: string;
}

export function isAgentScenario(s: ScenarioStats | LocalScenarioStats): s is ScenarioStats {
  return s.mode !== "local" && "request_count" in s;
}

export interface ToolSchema {
  name: string;
  description?: string;
  input_schema?: unknown;
}

export interface Skill {
  name: string;
  description: string;
}

export interface VersionRecord {
  /** semver string, e.g. "2.1.128" */
  version: string;
  /** ISO date prefix, e.g. "2026-04-30" */
  date: string;
  /** Folder name on disk, "<date>_<version>" */
  dirName: string;
  /** Absolute path to versions/<dirName> */
  dir: string;
  /** True if manifest.json is present (i.e. capture succeeded) */
  captured: boolean;
}

export function repoRoot(): string {
  // tools/cli/src/lib -> tools/cli/src -> tools/cli -> tools -> repo
  const here = fileURLToPath(new URL(".", import.meta.url));
  return resolve(here, "..", "..", "..", "..");
}

export function versionsDir(): string {
  return join(repoRoot(), "versions");
}

export function listVersions(): VersionRecord[] {
  const root = versionsDir();
  if (!existsSync(root)) return [];
  return readdirSync(root)
    .filter((n) => /^\d{4}-\d{2}-\d{2}_/.test(n))
    .map((dirName) => {
      const [date, ...rest] = dirName.split("_");
      const version = rest.join("_");
      const dir = join(root, dirName);
      const captured = existsSync(join(dir, "manifest.json"));
      return { version, date, dirName, dir, captured };
    })
    .sort((a, b) => a.dirName.localeCompare(b.dirName));
}

/** Resolve a user-provided argument (semver or dirName) to a version record. */
export function resolveVersion(arg: string): VersionRecord | undefined {
  const all = listVersions();
  return (
    all.find((v) => v.dirName === arg) ||
    all.find((v) => v.version === arg) ||
    all.find((v) => v.dirName.endsWith("_" + arg))
  );
}

export function readManifest(rec: VersionRecord): Manifest | null {
  const f = join(rec.dir, "manifest.json");
  if (!existsSync(f)) return null;
  return JSON.parse(readFileSync(f, "utf8")) as Manifest;
}

export function readJson<T>(rec: VersionRecord, name: string): T | null {
  const f = join(rec.dir, name);
  if (!existsSync(f)) return null;
  try {
    return JSON.parse(readFileSync(f, "utf8")) as T;
  } catch {
    return null;
  }
}

export function readText(rec: VersionRecord, name: string): string {
  const f = join(rec.dir, name);
  if (!existsSync(f)) return "";
  return readFileSync(f, "utf8");
}

export function readTools(rec: VersionRecord): ToolSchema[] {
  return readJson<ToolSchema[]>(rec, "tools.json") ?? [];
}

export function readDeferredTools(rec: VersionRecord): string[] {
  return readJson<string[]>(rec, "deferred-tools.json") ?? [];
}

export function readSkills(rec: VersionRecord): Skill[] {
  return readJson<Skill[]>(rec, "skills.json") ?? [];
}

export function diffFilePath(from: VersionRecord, to: VersionRecord): string {
  return join(to.dir, `diff-from-${from.dirName}.md`);
}

export function hasDiff(from: VersionRecord, to: VersionRecord): boolean {
  const p = diffFilePath(from, to);
  return existsSync(p) && statSync(p).size > 0;
}
