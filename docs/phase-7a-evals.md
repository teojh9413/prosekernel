# ProseKernel Phase 7A Evals

Phase 7A exists before the LLM adapter so ProseKernel can prove improvement instead of merely generating fluent text.

## What gets measured

The deterministic scorecard in `src/prosekernel/evals.py` maps a draft to the same six human-readable dimensions in `evals/writing-scorecard.md`:

- Specificity
- Proof
- Structure
- Reader fit
- Memorability
- Non-genericness

It also reports automatic metrics:

- word count
- sentence count
- paragraph count
- proof marker count
- abstract noun count
- slop phrase count
- long sentence count

## Fixture suite

The regression suite lives under `evals/fixtures/`:

- `weak/*.md` — plausible but generic drafts that should score below 75.
- `strong/*.md` — concrete, reader-shaped drafts that should score 75 or higher.

Current coverage mirrors the benchmark task set:

- launch email
- generic social rewrite
- incident apology
- nontechnical explanation
- strategic memo
- onboarding empty state

Run:

```bash
prosekernel eval
```

Expected result:

```text
Passed: 12/12
```

## Score one draft

```bash
prosekernel scorecard draft.md --task "write a launch email for ProseKernel" --output /tmp/prosekernel-scorecard.md
```

The command exits non-zero when the draft needs revision, so agents can use it as a quality gate.

## Demo report integration

`prosekernel write-demo` now includes:

- initial lint score
- final lint score
- initial scorecard total
- final scorecard total
- scorecard delta
- per-dimension movement

This makes the demo useful as an improvement report, not just a generated draft.
