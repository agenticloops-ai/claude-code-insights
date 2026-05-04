# claude-code 1.0.0 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 2 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 2 | 19 | 2.2s |
| `04-agent-task` | 8 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 20 | 5793 | 96.5s |
| `05-with-mcp` | 2 | 15 | 0 | 0 | 0 | 0 | 12993 | 1 | 2 | 29 | 2.7s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
