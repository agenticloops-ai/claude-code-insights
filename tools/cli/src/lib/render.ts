// Terminal renderers for VersionDiff. Stays pure (no IO) so the same
// shapes can render in the web app via a HTML version of these helpers.
import c from "ansi-colors";
import type { VersionDiff } from "./diff.js";

export function renderMetricsTable(d: VersionDiff): string {
  const rows = d.metrics.map((m) => [m.metric, String(m.from), String(m.to), m.delta ?? ""]);
  const head = ["metric", d.from.version, d.to.version, "Δ"];
  return tableMd([head, ...rows]);
}

export function renderToolsSection(d: VersionDiff): string {
  const lines: string[] = [];
  const t = d.tools;
  if (t.added.length) lines.push(c.green("added:    ") + t.added.join(", "));
  if (t.removed.length) lines.push(c.red("removed:  ") + t.removed.join(", "));
  if (t.movedToDeferred.length) lines.push(c.yellow("→deferred: ") + t.movedToDeferred.join(", "));
  if (t.movedToAdvertised.length) lines.push(c.yellow("→advertd:  ") + t.movedToAdvertised.join(", "));
  if (t.newDeferred.length) lines.push(c.green("new defrd:") + t.newDeferred.join(", "));
  if (t.removedDeferred.length) lines.push(c.red("rem defrd:") + t.removedDeferred.join(", "));
  if (t.modified.length) {
    lines.push(c.cyan("modified:"));
    for (const m of t.modified) {
      const flags = [m.descriptionChanged && "desc", m.schemaChanged && "schema"].filter(Boolean).join(", ");
      lines.push(`  - ${m.name} (${flags})`);
    }
  }
  return lines.join("\n");
}

export function renderSkillsSection(d: VersionDiff): string {
  const lines: string[] = [];
  if (d.skills.added.length) {
    lines.push(c.green("added skills:"));
    for (const s of d.skills.added) lines.push(`  + ${s.name} — ${s.description.slice(0, 80)}`);
  }
  if (d.skills.removed.length) {
    lines.push(c.red("removed skills:"));
    for (const s of d.skills.removed) lines.push(`  - ${s.name}`);
  }
  if (d.skills.descriptionChanged.length) {
    lines.push(c.yellow("description changed:"));
    for (const s of d.skills.descriptionChanged) lines.push(`  ~ ${s.name}`);
  }
  return lines.join("\n");
}

export function renderUnifiedDiff(diff: string): string {
  return diff
    .split("\n")
    .map((line) => {
      if (line.startsWith("+++") || line.startsWith("---")) return c.bold(line);
      if (line.startsWith("@@")) return c.cyan(line);
      if (line.startsWith("+")) return c.green(line);
      if (line.startsWith("-")) return c.red(line);
      return line;
    })
    .join("\n");
}

function tableMd(rows: string[][]): string {
  const widths = rows[0].map((_, col) => Math.max(...rows.map((r) => (r[col] ?? "").length)));
  const fmt = (r: string[]) => r.map((c, i) => c.padEnd(widths[i])).join("  ");
  return [fmt(rows[0]), widths.map((w) => "-".repeat(w)).join("  "), ...rows.slice(1).map(fmt)].join("\n");
}
