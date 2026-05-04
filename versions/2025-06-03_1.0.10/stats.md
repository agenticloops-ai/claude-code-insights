# claude-code 1.0.10 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 12 | 2.4s |
| `04-agent-task` | 9 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 20 | 4965 | 84.9s |
| `05-with-mcp` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 75 | 4.9s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
