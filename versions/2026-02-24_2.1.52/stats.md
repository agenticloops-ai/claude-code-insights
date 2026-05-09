# claude-code 2.1.52 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 1 | 21 | 0 | 0 | 0 | 2 | 14755 | 2 | 3 | 12 | 1.6s |
| `03-with-mcp` | 1 | 21 | 0 | 0 | 0 | 2 | 14755 | 2 | 3 | 82 | 3.0s |
| `04-with-skill` | 2 | 21 | 0 | 0 | 0 | 2 | 14755 | 2 | 5 | 97 | 9.8s |

## Models seen across scenarios

- `claude-opus-4-6`
