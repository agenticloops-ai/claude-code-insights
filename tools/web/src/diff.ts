// Browser-side diff. Mirrors tools/cli/src/lib/diff.ts so the same
// shapes power both terminal and web rendering.
import { createTwoFilesPatch, type ParsedDiff, structuredPatch } from "diff";
import type { Skill, ToolSchema, VersionBundle } from "./types.ts";

export interface ToolsDiff {
  added: string[];
  removed: string[];
  movedToDeferred: string[];
  movedToAdvertised: string[];
  newDeferred: string[];
  removedDeferred: string[];
  modified: { name: string; descriptionChanged: boolean; schemaChanged: boolean }[];
}

export interface SkillsDiff {
  added: Skill[];
  removed: Skill[];
  descriptionChanged: { name: string; from: string; to: string }[];
}

export interface MetricRow {
  metric: string;
  from: number;
  to: number;
  delta: number;
}

export interface VersionDiff {
  metrics: MetricRow[];
  tools: ToolsDiff;
  skills: SkillsDiff;
  systemPromptDiff: ParsedDiff;
  userPromptDiff: ParsedDiff;
  systemPromptUnified: string;
  userPromptUnified: string;
}

export function diffBundles(from: VersionBundle, to: VersionBundle): VersionDiff {
  const tools = diffTools(from.tools, to.tools, from.deferredTools, to.deferredTools);
  const skills = diffSkills(from.skills, to.skills);
  const metrics: MetricRow[] = [
    row("tools (advertised)", from.tools.length, to.tools.length),
    row("tools (deferred)", from.deferredTools.length, to.deferredTools.length),
    row("skills", from.skills.length, to.skills.length),
    row("system_prompt chars", from.systemPrompt.length, to.systemPrompt.length),
    row("user_prompt chars", from.userPrompt.length, to.userPrompt.length),
  ];
  const sysSpFrom = `${from.dirName}/system-prompt.md`;
  const sysSpTo = `${to.dirName}/system-prompt.md`;
  const usrSpFrom = `${from.dirName}/user-prompt.md`;
  const usrSpTo = `${to.dirName}/user-prompt.md`;
  return {
    metrics,
    tools,
    skills,
    systemPromptDiff: structuredPatch(sysSpFrom, sysSpTo, from.systemPrompt, to.systemPrompt, "", "", { context: 3 }),
    userPromptDiff: structuredPatch(usrSpFrom, usrSpTo, from.userPrompt, to.userPrompt, "", "", { context: 3 }),
    systemPromptUnified: createTwoFilesPatch(sysSpFrom, sysSpTo, from.systemPrompt, to.systemPrompt, "", "", { context: 3 }),
    userPromptUnified: createTwoFilesPatch(usrSpFrom, usrSpTo, from.userPrompt, to.userPrompt, "", "", { context: 3 }),
  };
}

function row(metric: string, from: number, to: number): MetricRow {
  return { metric, from, to, delta: to - from };
}

function diffTools(
  fromAdv: ToolSchema[],
  toAdv: ToolSchema[],
  fromDef: string[],
  toDef: string[],
): ToolsDiff {
  const fromAdvSet = new Set(fromAdv.map((t) => t.name));
  const toAdvSet = new Set(toAdv.map((t) => t.name));
  const fromDefSet = new Set(fromDef);
  const toDefSet = new Set(toDef);

  const added: string[] = [];
  const removed: string[] = [];
  const movedToDeferred: string[] = [];
  const movedToAdvertised: string[] = [];
  const newDeferred: string[] = [];
  const removedDeferred: string[] = [];

  for (const n of toAdvSet) if (!fromAdvSet.has(n) && !fromDefSet.has(n)) added.push(n);
  for (const n of fromAdvSet) {
    if (!toAdvSet.has(n) && !toDefSet.has(n)) removed.push(n);
    else if (!toAdvSet.has(n) && toDefSet.has(n)) movedToDeferred.push(n);
  }
  for (const n of fromDefSet) if (!toDefSet.has(n) && toAdvSet.has(n)) movedToAdvertised.push(n);
  for (const n of toDefSet) if (!fromDefSet.has(n) && !fromAdvSet.has(n)) newDeferred.push(n);
  for (const n of fromDefSet) if (!toDefSet.has(n) && !toAdvSet.has(n) && !removed.includes(n)) removedDeferred.push(n);

  const fromAdvMap = new Map(fromAdv.map((t) => [t.name, t]));
  const modified: ToolsDiff["modified"] = [];
  for (const t of toAdv) {
    const prev = fromAdvMap.get(t.name);
    if (!prev) continue;
    const descriptionChanged = (prev.description ?? "") !== (t.description ?? "");
    const schemaChanged = JSON.stringify(prev.input_schema ?? null) !== JSON.stringify(t.input_schema ?? null);
    if (descriptionChanged || schemaChanged) modified.push({ name: t.name, descriptionChanged, schemaChanged });
  }
  for (const arr of [added, removed, movedToDeferred, movedToAdvertised, newDeferred, removedDeferred]) arr.sort();
  modified.sort((a, b) => a.name.localeCompare(b.name));
  return { added, removed, movedToDeferred, movedToAdvertised, newDeferred, removedDeferred, modified };
}

function diffSkills(from: Skill[], to: Skill[]): SkillsDiff {
  const fromMap = new Map(from.map((s) => [s.name, s]));
  const toMap = new Map(to.map((s) => [s.name, s]));
  return {
    added: to.filter((s) => !fromMap.has(s.name)).sort((a, b) => a.name.localeCompare(b.name)),
    removed: from.filter((s) => !toMap.has(s.name)).sort((a, b) => a.name.localeCompare(b.name)),
    descriptionChanged: to
      .filter((s) => fromMap.get(s.name) && fromMap.get(s.name)!.description !== s.description)
      .map((s) => ({ name: s.name, from: fromMap.get(s.name)!.description, to: s.description }))
      .sort((a, b) => a.name.localeCompare(b.name)),
  };
}
