<system-reminder>
The following skills are available for use with the Skill tool:

- keybindings-help: Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut", "change the submit key", "customize keybindings".
- claude-developer-platform: Use this skill when the user wants to build a program that calls the Claude API or Anthropic SDK, OR when they need an AI/LLM and haven't chosen a platform yet. Trigger if the request:
- Mentions Claude, Opus, Sonnet, Haiku, or the Anthropic SDK / Agent SDK / API
- References Anthropic-specific features (Batches API, Files API, prompt caching, extended thinking, etc.)
- Involves building a chatbot, AI agent, or LLM-powered app and the existing code already uses Claude/Anthropic, or no AI SDK has been chosen yet
- Describes a program whose core logic requires calling an AI model and no non-Claude SDK is already in use
Do NOT trigger if the user is already working with a non-Claude AI platform. Check for these signals BEFORE reading this skill's docs:
- Filenames in the prompt referencing another provider (e.g. "openai", "gpt", "gemini" in the filename)
- The prompt explicitly mentions using OpenAI, GPT, Gemini, or another non-Claude provider
- Existing project files import a non-Claude AI SDK (e.g. openai, google.generativeai, or another provider)
This skill only contains Claude/Anthropic documentation and cannot help with other providers.
Do NOT trigger for purely conventional programming with no AI — calculators, timers, unit converters, file utilities, todo apps, password generators, URL shorteners, format converters, or similar deterministic-logic tasks.
Do NOT trigger for traditional ML/data science tasks that don't call an LLM API — scikit-learn pipelines, PyTorch model training, pandas/numpy data processing, etc.
- say-hello: Greet the user with a fixed phrase. Use this skill whenever the user asks to be greeted or asks the agent to "say hello" — exists as a deterministic skill fixture for sandbox capture scenarios.
</system-reminder>

<system-reminder>
As you answer the user's questions, you can use the following context:
# currentDate
Today's date is 2026-05-04.

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
