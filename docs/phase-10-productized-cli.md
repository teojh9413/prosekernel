# Phase 10 — Productized CLI / Usability

Status: implemented.

Phase 10 keeps ProseKernel's first product surface as a CLI plus Markdown reports. It does not add a web app and does not make default paid model calls.

## Added commands

```bash
prosekernel critique draft.md --task "write a launch email for ProseKernel" --mode hybrid --output critique.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --mode hybrid --output rewrite.md
```

Both commands are deterministic.

- `critique` reads an existing draft, runs lint + scorecard, retrieves relevant examples/patterns, and emits a revision plan.
- `rewrite` reads an existing draft, runs the critique path, produces a deterministic working rewrite, and reports score/lint deltas.

## Friendlier aliases

Existing command names remain stable. Phase 10 adds shorter aliases:

```bash
prosekernel examples "write a launch email for ProseKernel"
prosekernel demo "write a launch email for ProseKernel"
prosekernel score draft.md --task "write a launch email for ProseKernel"
```

Aliases preserve the same output contracts as:

- `search-examples`
- `write-demo`
- `scorecard`

## Productized report contracts

### Critique report

The critique report includes:

- verdict
- scorecard
- lint findings
- revision plan
- retrieved examples
- patterns to apply
- next command

It explicitly states that no model call was made.

### Rewrite report

The rewrite report includes:

- quality delta
- revision plan used
- rewritten draft
- retrieved examples
- patterns applied
- quality gate

It explicitly states that no model call was made and that the rewrite is a source-safe working draft, not final copy.

## Intended loop

```text
brief → draft → critique → rewrite → score/lint → human edit
```

Use `write` only when an explicit provider/model call is desired:

```bash
prosekernel write "<task>" --provider openai --model gpt-4o-mini
```

## Safety posture

- No hidden provider selection.
- No default paid model calls.
- Structure transfer only; do not copy source phrases.
- Deterministic rewrite is a starting point for editing, not a claim of final quality.
