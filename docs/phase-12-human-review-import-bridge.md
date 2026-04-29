# Phase 12 — Human-review / Import Bridge

Status: implemented.

Phase 12 closes the loop between public-safe learning notes and curated ProseKernel library assets without making promotion automatic.

The rule is:

> Approved learning notes can generate review-required proposals. Humans still decide what enters `library/` or `patterns/`.

## New commands

```bash
prosekernel propose-example learning/lessons/refund-workflow-draft.md \
  --root /root/prosekernel

prosekernel propose-pattern learning/lessons/refund-workflow-draft.md \
  --root /root/prosekernel \
  --pattern-id PATTERN_UX_002
```

Default outputs:

```text
proposals/examples/<category>/<source-title>.md
proposals/patterns/<pattern-id>-<source-title>.md
```

Use `--output` to choose a different proposal path. Existing proposal files are not overwritten unless `--force` is supplied.

## Proposal gates

`propose-example` and `propose-pattern` are fail-closed. They refuse to run unless the learning note has all of the following:

1. `promotion_status: "ready-for-human-review"`
2. `approved: true`
3. Rights are one of:
   - `public-domain`
   - `open-license`
   - `user-provided`
4. At least one valid `pattern_id`.
5. A known ProseKernel category.

Unsafe notes remain useful as metadata-only lessons, but they cannot generate import proposals.

## What proposals contain

Generated proposals preserve provenance and review requirements:

- source title, author, URL, rights, and source hash
- pointer back to the learning note
- `proposal_status: review-required`
- `source_text_stored: false`
- proposed library/pattern destination
- reusable lessons abstracted from the note
- explicit warnings not to copy source prose or bypass rights review

The proposal templates intentionally include review-required placeholders. A maintainer must replace those placeholders with original analysis before moving content into `library/` or `patterns/`.

## Intended loop

```text
source/draft
  → prosekernel learn
  → metadata-only learning note
  → prosekernel validate-learning
  → human approval + safe rights
  → prosekernel propose-example / propose-pattern
  → human edit/review
  → library or pattern import
  → validate-library + tests
```

## Safety posture

- No source prose is copied into proposals.
- No automatic import into `library/` or `patterns/`.
- No hidden model/API calls.
- Promotion requires explicit approval plus safe rights.
- Proposal files are staged under `proposals/` until a human reviews them.

## Verification

Run:

```bash
prosekernel validate-learning --root /root/prosekernel
prosekernel validate-library --root /root/prosekernel
python3 -m pytest -q
```

For a smoke test, create a temporary approved user-provided learning note, run both proposal commands with `--output /tmp/...`, and confirm the generated files contain `proposal_status: review-required` and `source_text_stored: false` but do not contain source prose.
