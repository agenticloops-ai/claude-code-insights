#!/usr/bin/env node
// Entrypoint for the `cci` CLI. Subcommands:
//   cci versions             — list all captured versions
//   cci show <ver>           — print the per-version metrics
//   cci diff <from> <to>     — print structured diff between any two versions
//   cci diff                 — interactive picker (requires a TTY)
//   cci serve [--port 5173]  — launch the web UI from tools/web (delegated)
import { search, select } from "@inquirer/prompts";
import c from "ansi-colors";
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { join } from "node:path";
import { listVersions, readManifest, repoRoot, resolveVersion, type VersionRecord } from "./lib/repo.js";
import { buildDiff } from "./lib/diff.js";
import { renderMetricsTable, renderSkillsSection, renderToolsSection, renderUnifiedDiff } from "./lib/render.js";

const argv = process.argv.slice(2);
const cmd = argv[0] ?? "help";

async function main() {
  switch (cmd) {
    case "versions":
      return cmdVersions();
    case "show":
      return cmdShow(argv[1]);
    case "diff":
      return cmdDiff(argv[1], argv[2], argv);
    case "serve":
      return cmdServe(argv);
    case "help":
    case "--help":
    case "-h":
      return printHelp();
    default:
      console.error(c.red(`unknown command: ${cmd}`));
      printHelp();
      process.exitCode = 1;
  }
}

function printHelp() {
  console.log(
    `cci — claude-code-insights CLI

Usage:
  cci versions                 list all captured versions
  cci show <version>           print metrics for one version
  cci diff <from> <to>         compare two versions (semver or dirName)
  cci diff                     interactive: pick two versions
  cci serve [--port 5173]      run the web UI (npm run dev under tools/web)

Args accept the npm version (e.g. 2.1.126) or the dated folder
(e.g. 2026-04-30_2.1.126).`,
  );
}

function cmdVersions() {
  const v = listVersions();
  for (const r of v) {
    const flag = r.captured ? c.green("●") : c.gray("○");
    console.log(`${flag} ${r.dirName.padEnd(26)} ${r.captured ? "" : c.dim("(no manifest)")}`);
  }
  console.log(c.dim(`\n${v.filter((x) => x.captured).length} captured / ${v.length} total`));
}

function cmdShow(arg?: string) {
  const rec = mustResolve(arg, "show");
  const m = readManifest(rec);
  if (!m) {
    console.error(c.red(`no manifest.json under ${rec.dir} — run /process-version ${rec.version}`));
    return;
  }
  console.log(c.bold(`${rec.version}`) + c.dim(`  (${rec.dirName})`));
  console.log(`  baseline:           ${m.baseline_scenario}`);
  const b = m.baseline ?? {};
  console.log(`  models:             ${(b.models ?? []).join(", ")}`);
  console.log(`  tools (advertised): ${b.tool_count ?? 0}`);
  console.log(`  tools (deferred):   ${b.deferred_tool_count ?? 0}`);
  console.log(`  mcp advertised:     ${b.mcp_tool_count_advertised ?? 0}`);
  console.log(`  mcp deferred:       ${b.mcp_tool_count_deferred ?? 0}`);
  console.log(`  skills:             ${b.skill_count ?? 0}`);
  console.log(`  system_prompt:      ${b.system_prompt_chars ?? 0} chars`);
  console.log(`  user_prompt:        ${b.user_prompt_chars ?? 0} chars`);
  console.log(`  reminders:          ${b.reminder_count ?? 0}`);
  const scens = Object.keys(m.scenarios ?? {}).sort();
  if (scens.length) console.log(`\n  scenarios:          ${scens.join(", ")}`);
  console.log(c.dim(`\nartifacts: ${rec.dir}`));
}

async function cmdDiff(fromArg: string | undefined, toArg: string | undefined, argv: string[]) {
  const captured = listVersions().filter((v) => v.captured);
  const from = fromArg ? mustResolve(fromArg, "diff <from>") : await pickVersion("from", captured);
  const to = toArg ? mustResolve(toArg, "diff <to>") : await pickVersion("to", captured, from);
  const json = argv.includes("--json");
  const writeFlag = argv.indexOf("--write");
  const writePath = writeFlag >= 0 ? argv[writeFlag + 1] : undefined;

  const d = buildDiff(from, to);

  if (json) {
    const out = JSON.stringify(d, null, 2);
    if (writePath) writeFileSync(writePath, out);
    else console.log(out);
    return;
  }

  console.log(c.bold(`# claude-code: ${from.version} → ${to.version}\n`));
  console.log(renderMetricsTable(d));
  console.log("");
  const tools = renderToolsSection(d);
  if (tools) console.log(c.bold("## tools\n") + tools + "\n");
  const skills = renderSkillsSection(d);
  if (skills) console.log(c.bold("## skills\n") + skills + "\n");
  if (d.systemPromptDiff.split("\n").length > 4) {
    console.log(c.bold("## system prompt"));
    console.log(renderUnifiedDiff(d.systemPromptDiff));
  }
  if (d.userPromptDiff.split("\n").length > 4) {
    console.log(c.bold("## user prompt"));
    console.log(renderUnifiedDiff(d.userPromptDiff));
  }
}

function cmdServe(argv: string[]) {
  const portIdx = argv.indexOf("--port");
  const port = portIdx >= 0 ? argv[portIdx + 1] : "5173";
  const cwd = join(repoRoot(), "tools", "web");
  console.log(c.dim(`launching tools/web on port ${port}…`));
  const child = spawn("npm", ["run", "dev", "--", "--port", port], { cwd, stdio: "inherit" });
  child.on("exit", (code) => process.exit(code ?? 0));
}

async function pickVersion(label: string, options: VersionRecord[], exclude?: VersionRecord): Promise<VersionRecord> {
  const filtered = options.filter((o) => !exclude || o.dirName !== exclude.dirName);
  const stdoutTty = process.stdout.isTTY;
  const stdinTty = process.stdin.isTTY;
  if (!stdoutTty || !stdinTty) {
    console.error(c.red("non-TTY environment — pass <from> and <to> as arguments"));
    process.exit(1);
  }
  // search() supports as-you-type filtering against a long list.
  const choice = await search<string>({
    message: `pick ${label} version`,
    source: async (term) => {
      const t = (term ?? "").toLowerCase();
      return filtered
        .filter((v) => !t || v.version.includes(t) || v.date.includes(t))
        .map((v) => ({ name: `${v.version}  ${c.dim(v.date)}`, value: v.dirName }));
    },
  });
  return options.find((v) => v.dirName === choice)!;
}

function mustResolve(arg: string | undefined, where: string): VersionRecord {
  if (!arg) {
    console.error(c.red(`${where}: missing argument`));
    process.exit(1);
  }
  const r = resolveVersion(arg);
  if (!r) {
    console.error(c.red(`unknown version: ${arg}`));
    process.exit(1);
  }
  return r;
}

main().catch((e) => {
  console.error(c.red(String(e)));
  process.exit(1);
});
