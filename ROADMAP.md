# Humanprint Roadmap

Humanprint is an open-source writing taste layer for AI agents.

It helps agents retrieve strong writing examples, extract reusable craft patterns, draft with structure, and detect generic AI slop before publishing.

## Current status

Completed:

- Phase 1 — Foundation and initial corpus.
- Phase 2 — Taxonomy expansion and deterministic retrieval demo.
- Phase 3 — Seed expanded categories.
- Phase 3.5 — Public release readiness metadata/docs.
- Phase 4 — Corpus depth lower bound: 60 annotated examples across 12 populated categories.
- Phase 5 — Initial strict pattern layer: 12 `PATTERN_*.md` families, example `pattern_ids`, and retrieval/demo output that cites pattern IDs.
- Phase 7A — Deeper basic evals: six-dimension scorecard implementation, weak/strong fixtures, `scorecard` CLI, `eval` CLI, and write-demo score improvement reports.
- Phase 6A — Provider-agnostic dry-run brief mode: `humanprint brief` builds an agent-ready writing packet without model/API calls.

Current corpus: 60 annotated examples across 12 populated categories.
Current pattern layer: 12 strict pattern families.
Current eval layer: 6 benchmark tasks plus 12 weak/strong fixture drafts.
Current adapter layer: dry-run `brief` mode, no credentials required.

## Phase 4 — Corpus depth

Goal: expand from representation to taste.

Target:

- 60-80 annotated examples.
- Prioritize public usefulness instead of even expansion.

Priority order:

1. Persuasive / Copywriting
2. Technical / Explanatory
3. Viral / Social
4. Brand / Positioning
5. Email / Newsletters
6. Strategic / Intelligent
7. UX / Product Microcopy
8. Crisis Communications
9. Speeches / Oratory
10. Journalism / Reportage
11. Internal Ops Docs
12. Essays / Literary Craft

Principle:

> One example gives a direction. Three to five examples create a pattern. Ten examples create taste.

## Phase 5 — Pattern extraction layer

Goal: turn examples into reusable intelligence.

Patterns are not summaries. They are agent-executable writing moves.

Each pattern follows `docs/pattern-schema.md`:

- pattern ID
- use when
- reader situation
- structure
- why it works
- examples
- anti-patterns
- agent instruction

Deliverables:

- `patterns/*.md`
- examples link to patterns
- retrieval output includes pattern IDs

## Phase 7A — Basic eval tasks and scorecards

Start evals before the LLM adapter.

Create benchmark tasks for:

- launch email
- generic social post rewrite
- incident apology
- technical explanation for non-technical users
- strategic memo
- onboarding empty state

Eval types:

1. Automated checks:
   - slop phrase count
   - proof markers
   - weak opener detection
   - abstract noun density
   - long sentence count
2. Human-readable scorecard:
   - specificity
   - proof
   - structure
   - reader fit
   - memorability
   - non-genericness

Deliverables now implemented:

- `evals/writing-scorecard.md` for the human-readable rubric.
- `evals/tasks/*.md` for benchmark task prompts.
- `evals/fixtures/weak/*.md` and `evals/fixtures/strong/*.md` for regression fixtures.
- `src/humanprint/evals.py` for deterministic scorecard scoring.
- `humanprint scorecard draft.md --task "..."` for draft scoring.
- `humanprint eval` for weak/strong fixture regression tests.
- `write-demo` reports include scorecard improvement by dimension.

## Phase 6 — LLM-backed drafting adapter

Goal: make Humanprint draft, not just brief.

Keep it provider-agnostic:

- OpenAI
- Anthropic
- OpenRouter
- local model later
- dry-run mode with generated brief only

Commands:

```bash
humanprint brief "write a launch email for an AI writing library"
humanprint write "write a launch email for an AI writing library"
```

Phase 6A deliverables now implemented:

- `humanprint brief` dry-run command.
- provider-neutral `WritingBrief` object and markdown renderer.
- strict pattern agent instructions pulled from `patterns/PATTERN_*.md`.
- quality gate instructions for lint + scorecard.
- `docs/phase-6-brief-mode.md`.

Remaining Phase 6B work:

- explicit provider adapter interface.
- `humanprint write --provider ... --model ...`.
- clear missing-credential errors; no default paid provider.
- preserve `brief` as the no-credential dry run.

Flow:

```text
task → retrieve examples/patterns → build brief → LLM drafts → lint critiques → LLM rewrites → report
```

## Phase 8 — Semantic / hybrid retrieval

Delay until the corpus is larger, around 80-150 examples.

Use hybrid retrieval, not pure vector search:

- category match
- keyword match
- tag match
- pattern match
- semantic similarity
- quality score

## Phase 9 — Agent workflow integration

Make Humanprint agent-ready for Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents.

Add/strengthen:

- `SKILL.md`
- `prompts/agent-workflow.md`
- `prompts/writing-brief.md`
- `prompts/critique.md`
- `prompts/rewrite.md`

Generic agent workflow:

1. Classify the task.
2. Retrieve examples.
3. Retrieve patterns.
4. Build a brief.
5. Draft.
6. Lint.
7. Rewrite.
8. Explain what changed.

## Phase 10 — Productization / usability

Keep the first product surface as CLI + Markdown reports.

Commands:

- `humanprint search`
- `humanprint brief`
- `humanprint lint`
- `humanprint critique`
- `humanprint rewrite`
- `humanprint write`
- `humanprint new-example`
- `humanprint validate-library`
- `humanprint index`

Do not rush into a web UI.

## Phase 11 — Public-safe learning loop

Public use must not auto-save private user writing.

Learning command should be explicit:

```bash
humanprint learn --from output.md --review
```

Flow:

1. User writes.
2. Humanprint critiques.
3. User manually approves saving a lesson.
4. System creates candidate pattern/example.
5. Maintainer reviews before merge.

## Phase 12 — Writing OS endgame

Humanprint is a writing operating system for agents: retrieve taste, apply structure, detect slop, improve drafts, and preserve reusable lessons.

Definition of done:

- Handles most serious writing formats.
- Produces better first drafts than generic AI.
- Maintains a rights-safe corpus and pattern library.
- Has evals that prove improvement.
- Offers agent-ready CLI and Markdown outputs.
- Learns only with explicit public-safe review.
