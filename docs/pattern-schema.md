# Pattern Schema

Patterns are reusable writing moves extracted from examples. They are the intelligence layer between raw examples and agent drafting.

Each pattern file should use this structure:

```markdown
# PATTERN_CATEGORY_001 — Pattern name

## Use when
The writing situation where this pattern helps.

## Reader situation
What the reader knows, feels, wants, doubts, or needs at this moment.

## Structure
1. First move.
2. Second move.
3. Third move.

## Why it works
The psychological, rhetorical, or usability reason the pattern works.

## Examples
- `library/category/examples/example.md` — how it uses the pattern.

## Anti-patterns
- What weak writers or generic AI outputs do instead.

## Agent instruction
A direct instruction an AI agent can follow when drafting or revising.
```

## ID conventions

Use stable IDs so retrieval, evals, and reports can cite patterns precisely.

Suggested prefixes:

- `PATTERN_HOOK_` — openings, hooks, first lines
- `PATTERN_PROOF_` — evidence, specificity, credibility
- `PATTERN_EMAIL_` — newsletters and lifecycle email
- `PATTERN_CRISIS_` — incident, apology, trust repair
- `PATTERN_UX_` — microcopy, onboarding, error recovery
- `PATTERN_STRATEGY_` — memos, theses, executive reasoning
- `PATTERN_BRAND_` — positioning and category design
- `PATTERN_EXPLAIN_` — docs, tutorials, explanation
- `PATTERN_SPEECH_` — public address and oratory
- `PATTERN_REPORTAGE_` — journalism and reported narrative
- `PATTERN_INTERNAL_` — ownership, process, internal operating docs
- `PATTERN_PERSUASION_` — reader awareness, objection handling, conversion logic

## Rule

A pattern is not a summary. It must be executable by an agent.
