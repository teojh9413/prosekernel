# Phase 10 — Productized CLI / Usability

Status: implemented.

Phase 10 keeps ProseKernel's first product surface as a CLI plus Markdown reports. It does not add a web app and does not make default paid model calls.

## Added commands

```bash
prosekernel critique draft.md --task "write a launch email for ProseKernel" --mode hybrid --output critique.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --mode hybrid --output rewrite.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --output rewrite-report.md --rewrite-output rewritten.md
```

Both commands are deterministic.

- `critique` reads an existing draft, runs lint + scorecard, retrieves relevant examples/patterns, and emits a revision plan.
- `rewrite` reads an existing draft, runs the critique path, produces a deterministic working rewrite, and reports score/lint deltas. Use `--rewrite-output rewritten.md` when you want the rewritten draft as a standalone file instead of extracting it from the report.

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

## Exit-code semantics

- `0`: command completed successfully for its contract.
- `1`: command ran but found a quality/validation problem, a draft still needs revision, an overwrite was refused, fixture evals failed, or an explicit provider call failed.
- `2`: usage/configuration/safety refusal, such as missing explicit provider/model, invalid learning metadata, unsafe promotion request, or conflicting output paths.

Command-specific notes:

- `critique`: exits `1` when the draft needs revision.
- `rewrite`: exits `0` when the deterministic rewrite does not lower the scorecard total; this is not a guarantee that the draft is publish-ready.
- `lint` / `scorecard`: exit `1` when the draft fails the automated threshold.
- `write`: exits `0` after a successful explicit provider call even if the generated draft still needs editing; exits `1` for provider call failures and `2` for missing provider/model/config.
- `learn`: exits `0` when a safe metadata-only learning note is created, `1` for overwrite refusal, and `2` for invalid metadata or unsafe promotion requests.
- `validate-learning` / `validate-library` / `eval`: exit `1` when validation or fixture checks fail.

Use `write` only when an explicit provider/model call is desired:

```bash
prosekernel write "<task>" --provider openai --model gpt-4o-mini
```

## Safety posture

- No hidden provider selection.
- No default paid model calls.
- Structure transfer only; do not copy source phrases.
- Deterministic rewrite is a starting point for editing, not a claim of final quality.
