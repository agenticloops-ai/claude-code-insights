// Shapes the dev-server middleware (vite.config.ts) hands over the wire.
// Mirrors the disk layout produced by scripts/extract.py and
// scripts/summarize-version.py.

export interface VersionRow {
  dirName: string;
  date: string;
  version: string;
  captured: boolean;
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

export interface Manifest {
  version: string;
  dir_name: string;
  baseline_scenario: string;
  baseline?: BaselineSummary;
  scenarios?: Record<string, unknown>;
}

export interface VersionBundle {
  dirName: string;
  manifest: Manifest | null;
  tools: ToolSchema[];
  deferredTools: string[];
  skills: Skill[];
  systemPrompt: string;
  userPrompt: string;
  releaseNotes: string;
}
