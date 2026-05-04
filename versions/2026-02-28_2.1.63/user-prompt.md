<system-reminder>
The following skills are available for use with the Skill tool:

- keybindings-help: Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut", "change the submit key", "customize keybindings".
- simplify: Review changed code for reuse, quality, and efficiency, then fix any issues found.
- claude-developer-platform: Build apps with the Claude API or Anthropic SDK.
TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`, or user asks to use Claude API, Anthropic SDKs, or Agent SDK.
DO NOT TRIGGER when: code imports `openai`/other AI SDK, general programming, or ML/data-science tasks.
- say-hello: Greet the user with a fixed phrase. Use this skill whenever the user asks to be greeted or asks the agent to "say hello" — exists as a deterministic skill fixture for sandbox capture scenarios.
</system-reminder>

<system-reminder>
As you answer the user's questions, you can use the following context:
# currentDate
Today's date is 2026-05-04.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
