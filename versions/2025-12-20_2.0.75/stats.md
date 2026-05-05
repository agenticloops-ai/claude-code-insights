# claude-code 2.0.75 — capture summary

Baseline scenario: `02-bare` (its system-prompt / tools are mirrored at the version root).

| scenario | requests | tools | deferred | mcp adv | mcp def | skills | sys-prompt | reminders | input | output | duration |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `02-bare` | 4 | 18 | 0 | 0 | 0 | 0 | 13204 | 0 | 1594 | 271 | 16.6s |
| `03-with-mcp` | 0 | None | 0 | 0 | 0 | 0 | None | None | None | None | — |
| `04-with-skill` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 1 | 0.8s |

## Models seen across scenarios

- `claude-haiku-4-5-20251001`
- `claude-opus-4-5-20251101`
