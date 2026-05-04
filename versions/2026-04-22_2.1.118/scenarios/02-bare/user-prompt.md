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
TaskOutput
TaskStop
TodoWrite
WebFetch
WebSearch
mcp__claude_ai_Canva__cancel-editing-transaction
mcp__claude_ai_Canva__comment-on-design
mcp__claude_ai_Canva__commit-editing-transaction
mcp__claude_ai_Canva__create-design-from-candidate
mcp__claude_ai_Canva__create-folder
mcp__claude_ai_Canva__export-design
mcp__claude_ai_Canva__generate-design
mcp__claude_ai_Canva__generate-design-structured
mcp__claude_ai_Canva__get-assets
mcp__claude_ai_Canva__get-design
mcp__claude_ai_Canva__get-design-content
mcp__claude_ai_Canva__get-design-pages
mcp__claude_ai_Canva__get-design-thumbnail
mcp__claude_ai_Canva__get-export-formats
mcp__claude_ai_Canva__get-presenter-notes
mcp__claude_ai_Canva__help
mcp__claude_ai_Canva__import-design-from-url
mcp__claude_ai_Canva__list-brand-kits
mcp__claude_ai_Canva__list-comments
mcp__claude_ai_Canva__list-folder-items
mcp__claude_ai_Canva__list-replies
mcp__claude_ai_Canva__merge-designs
mcp__claude_ai_Canva__move-item-to-folder
mcp__claude_ai_Canva__perform-editing-operations
mcp__claude_ai_Canva__reply-to-comment
mcp__claude_ai_Canva__request-outline-review
mcp__claude_ai_Canva__resize-design
mcp__claude_ai_Canva__resolve-shortlink
mcp__claude_ai_Canva__search-designs
mcp__claude_ai_Canva__search-folders
mcp__claude_ai_Canva__start-editing-transaction
mcp__claude_ai_Canva__upload-asset-from-url
mcp__claude_ai_Excalidraw__create_view
mcp__claude_ai_Excalidraw__export_to_excalidraw
mcp__claude_ai_Excalidraw__read_checkpoint
mcp__claude_ai_Excalidraw__read_me
mcp__claude_ai_Excalidraw__save_checkpoint
mcp__claude_ai_Figma__add_code_connect_map
mcp__claude_ai_Figma__create_design_system_rules
mcp__claude_ai_Figma__create_new_file
mcp__claude_ai_Figma__generate_diagram
mcp__claude_ai_Figma__get_code_connect_map
mcp__claude_ai_Figma__get_code_connect_suggestions
mcp__claude_ai_Figma__get_context_for_code_connect
mcp__claude_ai_Figma__get_design_context
mcp__claude_ai_Figma__get_figjam
mcp__claude_ai_Figma__get_libraries
mcp__claude_ai_Figma__get_metadata
mcp__claude_ai_Figma__get_screenshot
mcp__claude_ai_Figma__get_variable_defs
mcp__claude_ai_Figma__search_design_system
mcp__claude_ai_Figma__send_code_connect_mappings
mcp__claude_ai_Figma__upload_assets
mcp__claude_ai_Figma__use_figma
mcp__claude_ai_Figma__whoami
mcp__claude_ai_Gmail__create_draft
mcp__claude_ai_Gmail__create_label
mcp__claude_ai_Gmail__get_thread
mcp__claude_ai_Gmail__label_message
mcp__claude_ai_Gmail__label_thread
mcp__claude_ai_Gmail__list_drafts
mcp__claude_ai_Gmail__list_labels
mcp__claude_ai_Gmail__search_threads
mcp__claude_ai_Gmail__unlabel_message
mcp__claude_ai_Gmail__unlabel_thread
mcp__claude_ai_Google_Calendar__create_event
mcp__claude_ai_Google_Calendar__delete_event
mcp__claude_ai_Google_Calendar__get_event
mcp__claude_ai_Google_Calendar__list_calendars
mcp__claude_ai_Google_Calendar__list_events
mcp__claude_ai_Google_Calendar__respond_to_event
mcp__claude_ai_Google_Calendar__suggest_time
mcp__claude_ai_Google_Calendar__update_event
mcp__claude_ai_Google_Drive__copy_file
mcp__claude_ai_Google_Drive__create_file
mcp__claude_ai_Google_Drive__download_file_content
mcp__claude_ai_Google_Drive__get_file_metadata
mcp__claude_ai_Google_Drive__get_file_permissions
mcp__claude_ai_Google_Drive__list_recent_files
mcp__claude_ai_Google_Drive__read_file_content
mcp__claude_ai_Google_Drive__search_files
mcp__claude_ai_Miro__authenticate
mcp__claude_ai_Miro__complete_authentication
mcp__claude_ai_tldraw___exec_callback
mcp__claude_ai_tldraw___get_canvas_state
mcp__claude_ai_tldraw__exec
mcp__claude_ai_tldraw__read_checkpoint
mcp__claude_ai_tldraw__save_checkpoint
mcp__claude_ai_tldraw__search
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
- schedule: Create, update, list, or run scheduled remote agents (routines) on a cron schedule or once at a specific time. - When the user wants to schedule a recurring remote agent, set up automated tasks, create a cron job for Claude Code, or manage their scheduled agents/routines. Also use when the user wants a one-time scheduled run ("run this once at 3pm", "remind me to check X tomorrow").
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
# userEmail
The user's email address is <USER_EMAIL>.
# currentDate
Today's date is 2026-05-04.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
