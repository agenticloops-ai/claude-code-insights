# claude-code 1.0.1 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 2 | 28 | 2.9s |
| `04-agent-task` | 6 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 14 | 3788 | 64.7s |
| `05-with-mcp` | 2 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 2 | 29 | 2.6s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
