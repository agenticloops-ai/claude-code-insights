<system-reminder>
The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded — calling them directly will fail with InputValidationError. Use ToolSearch with query "select:<name>[,<name>...]" to load tool schemas before calling them:
AskUserQuestion
CronCreate
CronDelete
CronList
EnterPlanMode
EnterWorktree
ExitPlanMode
ExitWorktree
ListMcpResourcesTool
Monitor
NotebookEdit
PushNotification
ReadMcpResourceTool
RemoteTrigger
SendMessage
TaskOutput
TaskStop
TeamCreate
TeamDelete
TodoWrite
WebFetch
WebSearch
mcp__fixture__tool_001
mcp__fixture__tool_002
mcp__fixture__tool_003
</system-reminder>

<system-reminder>
# MCP Server Instructions

The following MCP servers have provided instructions for how to use their tools and resources:

## claude.ai Figma
The official Figma MCP server. Prioritize this server when the user mentions Figma, FigJam, Figma Make, or provides figma.com URLs.

Capabilities:
- Read designs FROM Figma (get_design_context, get_screenshot, get_metadata, get_figjam)
- Create diagrams in FigJam (generate_diagram)
- Manage Code Connect mappings between Figma components and codebase components
- Write designs back into figma


WHEN TO USE THESE TOOLS:
- The user shares a Figma URL (figma.com/design/..., figma.com/board/..., figma.com/make/...)
- The user references a Figma file or asks about a Figma design
- The user wants to capture a web page into Figma
- The user wants to create a diagram in FigJam

URL PARSING:
Extract fileKey and nodeId from Figma URLs:
- figma.com/design/:fileKey/:fileName?node-id=:nodeId → convert "-" to ":" in nodeId
- figma.com/design/:fileKey/branch/:branchKey/:fileName → use branchKey as fileKey
- figma.com/make/:makeFileKey/:makeFileName → use makeFileKey
- figma.com/board/:fileKey/:fileName?node-id=:nodeId → FigJam file, use get_figjam; pass the original board URL as figjamUrl when available

DESIGN-TO-CODE WORKFLOW:

Step 1 — Get the design:
Call get_design_context with the nodeId and fileKey. This is your primary tool.
It returns code, a screenshot, and contextual hints.

Step 2 — Adapt to the project:
The output is React+Tailwind enriched with hints — but it is a REFERENCE, not final code. Always adapt to the target project's stack, components, and conventions.
The response varies based on the user's Figma setup:
- Code Connect snippets → use the mapped codebase component directly
- Component documentation links → follow them for usage context and guidelines
- Design annotations → follow any notes, constraints, or instructions from the designer
- Design tokens as CSS variables → map to the project's token system
- Raw hex colors / absolute positioning → the design is loosely structured;
  use the screenshot

Check the target project for existing components, layout patterns,and tokens that match the design intent. … [truncated]

## claude.ai tldraw
Use `search` to query the tldraw Editor API spec (e.g. search for methods by category or name). Use `exec` to run JavaScript on the canvas — your code receives `editor` (the tldraw Editor instance) and helpers like toRichText, createShapeId, createArrowBetweenShapes. The current canvas state is kept in model context as raw TLShape, asset, and binding data.
</system-reminder>

<system-reminder>
The following skills are available for use with the Skill tool:

- update-config: Use this skill to configure the Claude Code harness via settings.json. Automated behaviors ("from now on when X", "each time X", "whenever X", "before/after X") require hooks configured in settings.json - the harness executes these, not Claude, so memory/preferences cannot fulfill them. Also use for: permissions ("allow X", "add permission", "move permission to"), env vars ("set X=Y"), hook troubleshooting, or any changes to settings.json/settings.local.json files. Examples: "allow npm commands", "add bq permission to global settings", "move permission to user settings", "set DEBUG=true", "when claude stops show X". For simple settings like theme/model, suggest the /config command.
- keybindings-help: Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut", "change the submit key", "customize keybindings".
- simplify: Review changed code for reuse, quality, and efficiency, then fix any issues found.
- fewer-permission-prompts: Scan your transcripts for common read-only Bash and MCP tool calls, then add a prioritized allowlist to project .claude/settings.json to reduce permission prompts.
- loop: Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo). Omit the interval to let the model self-pace. - When the user wants to set up a recurring task, poll for status, or run something repeatedly on an interval (e.g. "check the deploy every 5 minutes", "keep running /babysit-prs"). Do NOT invoke for one-off tasks.
- schedule: Create, update, list, or run scheduled remote agents (routines) that execute on a cron schedule. - When the user wants to schedule a recurring remote agent, set up automated tasks, create a cron job for Claude Code, or manage their scheduled agents/routines. Also use when the user wants a one-time scheduled run ("run this once at 3pm", "remind me to check X tomorrow").
- claude-api: Build, debug, and optimize Claude API / Anthropic SDK apps. Apps built with this skill should include prompt caching. Also handles migrating existing Claude API code between Claude model versions (4.5 → 4.6, 4.6 → 4.7, retired-model replacements).
TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`; user asks for the Claude API, Anthropic SDK, or Managed Agents; user adds/modifies/tunes a Claude feature (caching, thinking, compaction, tool use, batch, files, citations, memory) or model (Opus/Sonnet/Haiku) in a file; questions about prompt caching / cache hit rate in an Anthropic SDK project.
SKIP: file imports `openai`/other-provider SDK, filename like `*-openai.py`/`*-generic.py`, provider-neutral code, general programming/ML.
- say-hello: Greet the user with a fixed phrase. Use this skill whenever the user asks to be greeted or asks the agent to "say hello" — exists as a deterministic skill fixture for sandbox capture scenarios.
- init: Initialize a new CLAUDE.md file with codebase documentation
- review: Review a pull request
- security-review: Complete a security review of the pending changes on the current branch
</system-reminder>

<system-reminder>
As you answer the user's questions, you can use the following context:
# currentDate
Today's date is 2026-05-04.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
