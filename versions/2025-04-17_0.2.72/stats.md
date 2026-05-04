# claude-code 0.2.72 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 2 | 12 | 0 | 0 | 0 | 0 | 10370 | 0 | 0 | 0 | 0.4s |
| `04-agent-task` | 2 | 12 | 0 | 0 | 0 | 0 | 10370 | 0 | 0 | 0 | 0.5s |
| `05-with-mcp` | 2 | 12 | 0 | 0 | 0 | 0 | 10370 | 0 | 0 | 0 | 0.4s |

## Models seen across scenarios

- `claude-3-7-sonnet-20250219`
