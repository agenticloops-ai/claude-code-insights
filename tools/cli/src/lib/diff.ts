// Pure-JS diffing of the version artifacts: tools, skills, and the
// system/user prompts. Mirrors what scripts/diff-versions.py emits but
// returns structured data so the CLI and the web app can render it
// however they like (terminal table, HTML cards, JSON to a downstream
// pipeline). Anything that needs to be byte-identical with the
// committed diff-from-*.md files should keep using the Python; this is
// for ad-hoc compare-any-two flows.
import { createTwoFilesPatch, structuredPatch } from "diff";
import {
  readDeferredTools,
  readSkills,
  readText,
  readTools,
  type Skill,
  type ToolSchema,
  type VersionRecord,
} from "./repo.js";

export interface MetricRow {
  metric: string;
  from: string | number;
  to: string | number;
  delta?: string;
}

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

export interface VersionDiff {
  from: VersionRecord;
  to: VersionRecord;
  metrics: MetricRow[];
  tools: ToolsDiff;
  skills: SkillsDiff;
  systemPromptDiff: string;
  userPromptDiff: string;
}

function namesOf<T extends { name: string }>(arr: T[]): Set<string> {
  return new Set(arr.map((x) => x.name));
}

function diffTools(
  fromAdvertised: ToolSchema[],
  toAdvertised: ToolSchema[],
  fromDeferred: string[],
  toDeferred: string[],
): ToolsDiff {
  const fromAdv = namesOf(fromAdvertised);
  const toAdv = namesOf(toAdvertised);
  const fromDef = new Set(fromDeferred);
  const toDef = new Set(toDeferred);

  const added: string[] = [];
  const removed: string[] = [];
  const movedToDeferred: string[] = [];
  const movedToAdvertised: string[] = [];

  for (const n of toAdv) if (!fromAdv.has(n) && !fromDef.has(n)) added.push(n);
  for (const n of fromAdv) {
    if (!toAdv.has(n) && !toDef.has(n)) removed.push(n);
    else if (!toAdv.has(n) && toDef.has(n)) movedToDeferred.push(n);
  }
  for (const n of fromDef) if (!toDef.has(n) && toAdv.has(n)) movedToAdvertised.push(n);

  const newDeferred: string[] = [];
  for (const n of toDef) if (!fromDef.has(n) && !fromAdv.has(n)) newDeferred.push(n);
  const removedDeferred: string[] = [];
  for (const n of fromDef) if (!toDef.has(n) && !toAdv.has(n) && !removed.includes(n)) removedDeferred.push(n);

  // Modified: same name in both advertised lists but changed shape.
  const fromAdvMap = new Map(fromAdvertised.map((t) => [t.name, t]));
  const modified: ToolsDiff["modified"] = [];
  for (const t of toAdvertised) {
    const prev = fromAdvMap.get(t.name);
    if (!prev) continue;
    const descriptionChanged = (prev.description ?? "") !== (t.description ?? "");
    const schemaChanged = JSON.stringify(prev.input_schema ?? null) !== JSON.stringify(t.input_schema ?? null);
    if (descriptionChanged || schemaChanged) modified.push({ name: t.name, descriptionChanged, schemaChanged });
  }

  added.sort();
  removed.sort();
  movedToDeferred.sort();
  movedToAdvertised.sort();
  newDeferred.sort();
  removedDeferred.sort();
  modified.sort((a, b) => a.name.localeCompare(b.name));
  return { added, removed, movedToDeferred, movedToAdvertised, newDeferred, removedDeferred, modified };
}

function diffSkills(from: Skill[], to: Skill[]): SkillsDiff {
  const fromMap = new Map(from.map((s) => [s.name, s]));
  const toMap = new Map(to.map((s) => [s.name, s]));
  const added = to.filter((s) => !fromMap.has(s.name)).sort((a, b) => a.name.localeCompare(b.name));
  const removed = from.filter((s) => !toMap.has(s.name)).sort((a, b) => a.name.localeCompare(b.name));
  const descriptionChanged = to
    .filter((s) => fromMap.get(s.name) && fromMap.get(s.name)!.description !== s.description)
    .map((s) => ({ name: s.name, from: fromMap.get(s.name)!.description, to: s.description }))
    .sort((a, b) => a.name.localeCompare(b.name));
  return { added, removed, descriptionChanged };
}

export function unifiedTextDiff(fromName: string, toName: string, fromText: string, toText: string): string {
  return createTwoFilesPatch(fromName, toName, fromText, toText, "", "", { context: 3 });
}

export function structuredTextDiff(fromName: string, toName: string, fromText: string, toText: string) {
  return structuredPatch(fromName, toName, fromText, toText, "", "", { context: 3 });
}

export function buildDiff(from: VersionRecord, to: VersionRecord): VersionDiff {
  const fromTools = readTools(from);
  const toTools = readTools(to);
  const fromDef = readDeferredTools(from);
  const toDef = readDeferredTools(to);
  const fromSkills = readSkills(from);
  const toSkills = readSkills(to);
  const fromSys = readText(from, "system-prompt.md");
  const toSys = readText(to, "system-prompt.md");
  const fromUsr = readText(from, "user-prompt.md");
  const toUsr = readText(to, "user-prompt.md");

  const tools = diffTools(fromTools, toTools, fromDef, toDef);
  const skills = diffSkills(fromSkills, toSkills);

  const metrics: MetricRow[] = [
    { metric: "tools (advertised)", from: fromTools.length, to: toTools.length, delta: deltaStr(toTools.length - fromTools.length) },
    { metric: "tools (deferred)", from: fromDef.length, to: toDef.length, delta: deltaStr(toDef.length - fromDef.length) },
    { metric: "skills", from: fromSkills.length, to: toSkills.length, delta: deltaStr(toSkills.length - fromSkills.length) },
    { metric: "system_prompt chars", from: fromSys.length, to: toSys.length, delta: deltaStr(toSys.length - fromSys.length) },
    { metric: "user_prompt chars", from: fromUsr.length, to: toUsr.length, delta: deltaStr(toUsr.length - fromUsr.length) },
  ];

  return {
    from,
    to,
    metrics,
    tools,
    skills,
    systemPromptDiff: unifiedTextDiff(`${from.version}/system-prompt.md`, `${to.version}/system-prompt.md`, fromSys, toSys),
    userPromptDiff: unifiedTextDiff(`${from.version}/user-prompt.md`, `${to.version}/user-prompt.md`, fromUsr, toUsr),
  };
}

function deltaStr(n: number): string {
  if (n === 0) return "";
  return n > 0 ? `+${n}` : `${n}`;
}
