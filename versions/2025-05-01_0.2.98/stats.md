# claude-code 0.2.98 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 5 | 14 | 0 | 0 | 0 | 0 | 13274 | 0 | 0 | 0 | 1.1s |
| `04-agent-task` | 5 | 14 | 0 | 0 | 0 | 0 | 13274 | 0 | 0 | 0 | 1.0s |
| `05-with-mcp` | 5 | 14 | 0 | 0 | 0 | 0 | 13274 | 0 | 0 | 0 | 0.9s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-3-7-sonnet-20250219`
