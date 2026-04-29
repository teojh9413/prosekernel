# Contributing to ProseKernel

ProseKernel is an open-source taste engine for AI writing agents. Contributions should make agents better at studying strong writing, transferring structure, and avoiding generic AI slop.

## What belongs here

A contribution belongs if it teaches a reusable writing move.

Good additions usually improve one of these layers:

- rights-safe annotated examples
- reusable craft patterns
- anti-slop lint rules
- writing briefs, critique prompts, or rewrite prompts
- evaluation tasks and scorecards
- retrieval quality
- documentation that helps agents use the system

## Example acceptance rules

Every example must include:

- source URL
- author/company
- rights classification
- category and format
- at least two tags
- quality score
- when to use it
- why it is good
- craft moves
- structure map
- excerpt or summary
- reusable pattern
- imitation prompt
- anti-patterns to avoid

Reject examples that are merely popular, clever, or famous if they do not teach a transferable move.

## Rights policy for examples

ProseKernel teaches structure and craft. It does not need to store full copyrighted works.

Allowed:

- public-domain works
- open-license works
- short excerpts with commentary when legally appropriate
- metadata + original analysis
- user-provided examples with permission

Default for modern copyrighted writing:

- use `metadata-only`
- link to the source
- summarize in your own words
- write original analysis
- do not copy the full text

Never add:

- full paid newsletters
- full copyrighted articles or books
- paywalled material copied into the repo
- private communications without explicit permission
- scraped examples with unclear provenance

## Quality bar

A ProseKernel example should teach at least one of:

- a sharper opening
- a proof structure
- a reader-awareness move
- a useful narrative or argument sequence
- a specificity move
- a rhythm/cadence move
- a compression move
- a trust-repair move
- a product/service clarity move
- an anti-pattern worth avoiding

## Pattern IDs

When extracting patterns, use stable IDs:

- `PATTERN_HOOK_001`
- `PATTERN_PROOF_001`
- `PATTERN_EMAIL_001`
- `PATTERN_CRISIS_001`
- `PATTERN_UX_001`
- `PATTERN_STRATEGY_001`
- `PATTERN_BRAND_001`
- `PATTERN_EXPLAIN_001`
- `PATTERN_SPEECH_001`
- `PATTERN_REPORTAGE_001`
- `PATTERN_INTERNAL_001`
- `PATTERN_PERSUASION_001`

Patterns should follow the schema in `docs/pattern-schema.md`.

## Verification

Before opening a pull request, run:

```bash
python3 -m pytest -q
PYTHONPATH=src python3 -m prosekernel.cli validate-library
```
