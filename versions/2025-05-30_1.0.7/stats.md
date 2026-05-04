# claude-code 1.0.7 — capture summary

Baseline scenario: `03-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `03-bare` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 12 | 2.5s |
| `04-agent-task` | 7 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 14 | 3627 | 63.4s |
| `05-with-mcp` | 3 | 15 | 0 | 0 | 0 | 0 | 13228 | 1 | 2 | 29 | 2.8s |

## Models seen across scenarios

- `claude-3-5-haiku-20241022`
- `claude-opus-4-20250514`
