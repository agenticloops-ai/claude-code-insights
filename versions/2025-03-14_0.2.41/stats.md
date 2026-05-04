# claude-code 0.2.41 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 1 | 10 | 0 | 0 | 0 | 0 | 10316 | 0 | 0 | 0 | 0.2s |
| `04-agent-task` | 1 | 10 | 0 | 0 | 0 | 0 | 10316 | 0 | 0 | 0 | 0.2s |
| `05-with-mcp` | 1 | 10 | 0 | 0 | 0 | 0 | 10316 | 0 | 0 | 0 | 0.2s |

## Models seen across scenarios

- `claude-3-7-sonnet-20250219`
