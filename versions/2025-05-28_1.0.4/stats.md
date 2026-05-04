# claude-code 1.0.4 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 13128 | 1 | 2 | 16 | 1.8s |
| `04-agent-task` | 9 | 15 | 0 | 0 | 0 | 0 | 13128 | 1 | 20 | 4315 | 77.0s |
| `05-with-mcp` | 2 | 15 | 0 | 0 | 0 | 0 | 13128 | 1 | 2 | 29 | 5.6s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
