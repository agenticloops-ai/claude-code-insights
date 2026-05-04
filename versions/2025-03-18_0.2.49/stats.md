# claude-code 0.2.49 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 1 | 11 | 0 | 0 | 0 | 0 | 10827 | 0 | 0 | 0 | 0.3s |
| `04-agent-task` | 1 | 11 | 0 | 0 | 0 | 0 | 10827 | 0 | 0 | 0 | 0.2s |
| `05-with-mcp` | 1 | 11 | 0 | 0 | 0 | 0 | 10827 | 0 | 0 | 0 | 0.3s |

## Models seen across scenarios

- `claude-3-7-sonnet-20250219`
