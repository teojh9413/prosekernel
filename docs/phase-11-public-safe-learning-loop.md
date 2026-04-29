# Phase 11 — Public-safe Learning Loop

Status: implemented.

Phase 11 lets ProseKernel learn from drafts and source materials without becoming a private-writing dump or a copyrighted-text mirror.

The rule is simple:

> Store metadata, hashes, metrics, and original lessons. Do not store source prose.

## New commands

```bash
prosekernel learn draft.md \
  --task "rewrite help center copy for delayed refunds" \
  --source-title "Refund workflow draft" \
  --source-author "Support Team" \
  --source-url "https://example.com/refund-workflow" \
  --rights metadata-only \
  --category ux-product-microcopy \
  --tags "refunds, support" \
  --output learning/lessons/refund-workflow-draft.md

prosekernel validate-learning
```

`learn` reads the source draft, runs deterministic lint/scorecard analysis, and writes a learning note. The generated note includes:

- source title, author, URL, rights, category, tags, and pattern IDs
- `source_text_stored: false`
- SHA-256 hash of the source text for auditability
- source word count, lint score, and scorecard total
- original reusable lessons based on the quality findings
- a promotion gate that prevents silent example/pattern promotion

It does **not** store the source text.

## Default output

If `--output` is omitted, notes are written to:

```text
learning/lessons/<source-title>.md
```

## Rights and promotion checks

Learning notes are lesson-only by default.

Promotion is refused unless both are true:

1. `--approved` is supplied.
2. Rights are one of:
   - `public-domain`
   - `open-license`
   - `user-provided`

These commands fail safely:

```bash
# Refused: promotion requested without human approval
prosekernel learn draft.md ... --rights user-provided --promote

# Refused: metadata-only source cannot be promoted even with approval
prosekernel learn draft.md ... --rights metadata-only --promote --approved
```

For `metadata-only` and `short-excerpt` sources, the output remains a safe learning note and cannot be marked as promotion-ready by the CLI.

## Validation

Run:

```bash
prosekernel validate-learning
```

Validation fails if a learning note:

- omits required source metadata
- omits `source_text_stored: false`
- says `source_text_stored: true`
- includes source-text sections such as `## Source text`, `### Original draft`, or `## Full source`
- marks `promotion_status: "ready-for-human-review"` without safe rights and `approved: true`
- lacks a reusable lesson or promotion gate

`learn` refuses to overwrite an existing note unless `--force` is supplied. This protects audit history when two sources share a title.

## Intended loop

```text
draft/source → critique metrics → metadata-only lesson → validation → human review → optional safe promotion
```

## Safety posture

- No hidden model calls.
- No auto-saving private writing.
- No copied source prose in learning notes.
- No automatic pattern/example promotion.
- Structure transfer only: preserve the lesson, not the wording.
