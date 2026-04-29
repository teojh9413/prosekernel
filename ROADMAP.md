# ProseKernel Roadmap

ProseKernel is an open-source taste engine for AI writing agents.

It helps agents retrieve strong writing examples, extract reusable craft patterns, draft with structure, and detect generic AI slop before publishing.

## Current status

Completed:

- Phase 1 — Foundation and initial corpus.
- Phase 2 — Taxonomy expansion and deterministic retrieval demo.
- Phase 3 — Seed expanded categories.
- Phase 3.5 — Public release readiness metadata/docs.
- Phase 4 — Corpus depth expansion: 100 annotated examples across 12 populated categories, with eight priority categories at 10-example taste depth.
- Phase 5 — Initial strict pattern layer: 12 `PATTERN_*.md` families, example `pattern_ids`, and retrieval/demo output that cites pattern IDs.
- Phase 7A — Deeper basic evals: six-dimension scorecard implementation, weak/strong fixtures, `scorecard` CLI, `eval` CLI, and write-demo score improvement reports.
- Phase 6A — Provider-agnostic dry-run brief mode: `prosekernel brief` builds an agent-ready writing packet without model/API calls.
- Phase 6B — Explicit provider write mode: adapter interface, `prosekernel write --provider ... --model ...`, safe missing-credential errors, and provider/model trace reports.
- Phase 8 — Offline semantic/hybrid retrieval: optional `--mode semantic|hybrid`, score explanations, cached concept expansion, and no new runtime dependencies.
- Phase 9 — Agent workflow integration: repo-local `SKILL.md`, prompt contracts, and command-grounded workflow docs for Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents.
- Phase 10 — Productized CLI/usability: `critique`, `rewrite`, productized Markdown reports, standalone rewrite outputs, exit-code docs, and friendlier aliases (`examples`, `demo`, `score`).
- Phase 11 — Public-safe learning loop: `learn` metadata-only learning notes, `validate-learning`, source-text exclusion checks, and rights/approval gates for promotion.
- Phase 12 — Human-review/import bridge: `propose-example` and `propose-pattern` generate review-required proposals from approved safe-rights learning notes without automatic import.

Current corpus: 100 annotated examples across 12 populated categories.
Current pattern layer: 12 strict pattern families.
Current eval layer: 6 benchmark tasks plus 12 weak/strong fixture drafts.
Current adapter layer: dry-run `brief` mode plus explicit provider-backed `write` mode. No default paid provider is selected; writes require explicit `--provider` and `--model`.
Current retrieval layer: default lexical/category scoring plus optional offline semantic and hybrid scoring.

## Phase 4 — Corpus depth

Goal: expand from representation to taste.

Target:

- 80-100 annotated examples next.
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
- `src/prosekernel/evals.py` for deterministic scorecard scoring.
- `prosekernel scorecard draft.md --task "..."` for draft scoring.
- `prosekernel eval` for weak/strong fixture regression tests.
- `write-demo` reports include scorecard improvement by dimension.

## Phase 6 — LLM-backed drafting adapter

Goal: make ProseKernel draft, not just brief.

Keep it provider-agnostic:

- OpenAI
- Anthropic
- OpenRouter
- local model later
- dry-run mode with generated brief only

Commands:

```bash
prosekernel brief "write a launch email for an AI writing library"
prosekernel write "write a launch email for an AI writing library"
```

Phase 6A deliverables now implemented:

- `prosekernel brief` dry-run command.
- provider-neutral `WritingBrief` object and markdown renderer.
- strict pattern agent instructions pulled from `patterns/PATTERN_*.md`.
- quality gate instructions for lint + scorecard.
- `docs/phase-6-brief-mode.md`.

Phase 6B deliverables now implemented:

- explicit provider adapter protocol in `src/prosekernel/providers.py`.
- initial OpenAI, OpenRouter, and Anthropic HTTP adapters using stdlib HTTP calls.
- `prosekernel write --provider ... --model ...`.
- no-default-provider refusal path to prevent accidental paid calls.
- missing credential errors that name the exact env var and confirm no API call was made.
- write reports with provider/model trace, retrieved examples, pattern IDs, draft, lint, scorecard, and quality gate.
- `docs/phase-6b-provider-write.md`.

Remaining later work:

- optional local model provider.
- optional LLM critique/rewrite loop after the first draft.
- richer provider configuration once real users exercise write mode.

Flow:

```text
task → retrieve examples/patterns → build brief → LLM drafts → lint critiques → LLM rewrites → report
```

## Phase 8 — Semantic / hybrid retrieval

Status: implemented.

ProseKernel keeps lexical/category scoring as the default and adds explicit opt-in modes:

```bash
prosekernel search-examples "write a security incident update for customers" --mode hybrid --explain
prosekernel brief "write a customer trust update after a compromised credential scare" --mode hybrid
prosekernel write-demo "write an outage apology" --mode hybrid
```

Implemented signals:

- category match
- keyword match
- tag match
- pattern match
- offline semantic concept aliases
- category concepts
- quality score
- cached semantic token expansion

See `docs/phase-8-hybrid-retrieval.md`.

## Phase 9 — Agent workflow integration

Status: implemented.

ProseKernel is now agent-ready for Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents.

Implemented assets:

- `SKILL.md`
- `prompts/agent-workflow.md`
- `prompts/writing-brief.md`
- `prompts/critique.md`
- `prompts/rewrite.md`
- `docs/agent-workflow.md`
- `docs/phase-9-agent-workflow.md`

Generic agent workflow:

1. Classify the task.
2. Retrieve examples.
3. Retrieve patterns.
4. Build a brief.
5. Draft.
6. Lint/score.
7. Revise.
8. Explain what changed.

Short form: classify → retrieve → patterns → brief → draft → lint/score → revise → explain

## Phase 10 — Productization / usability

Status: implemented.

The first product surface remains CLI + Markdown reports.

Implemented commands:

- `prosekernel critique draft.md --task "..." --output critique.md`
- `prosekernel rewrite draft.md --task "..." --output rewrite.md`
- `prosekernel rewrite draft.md --task "..." --output rewrite-report.md --rewrite-output rewritten.md`
- `prosekernel examples "..."` as a shorter alias for `search-examples`
- `prosekernel demo "..."` as a shorter alias for `write-demo`
- `prosekernel score draft.md` as a shorter alias for `scorecard`

Implemented behavior:

- Critique reports combine deterministic lint, scorecard, retrieved examples, pattern IDs, and a revision plan.
- Rewrite reports produce a deterministic working rewrite plus score/lint deltas and quality gates.
- `--rewrite-output` writes the rewritten draft as a standalone file for downstream editing.
- Exit-code semantics are documented for product use and shell automation.
- Existing command contracts remain stable.
- No default provider/model is selected; no hidden paid model calls are made.

See `docs/phase-10-productized-cli.md`.

## Phase 11 — Public-safe learning loop

Status: implemented.

Public use must not auto-save private user writing or mirror copyrighted text. Learning is explicit, metadata-first, and validation-backed.

Implemented commands:

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

Implemented behavior:

1. User or maintainer explicitly invokes `learn`.
2. ProseKernel reads the source draft for local metrics only.
3. The generated learning note stores metadata, source hash, word count, lint score, scorecard total, pattern IDs, and original reusable lessons.
4. The generated note sets `source_text_stored: false` and omits source prose.
5. `validate-learning` rejects notes that claim source text is stored or include a `## Source text` section.
6. Promotion is refused unless `--approved` is supplied and rights are `public-domain`, `open-license`, or `user-provided`.
7. Approved safe-rights notes can generate review-required proposals with `propose-example` and `propose-pattern`; import still requires human review.

See `docs/phase-11-public-safe-learning-loop.md`.

## Phase 12 — Human-review / import bridge

Status: implemented.

Phase 12 creates a controlled bridge from learning notes into curation work.

Implemented commands:

```bash
prosekernel propose-example learning/lessons/refund-workflow-draft.md \
  --root /root/prosekernel

prosekernel propose-pattern learning/lessons/refund-workflow-draft.md \
  --root /root/prosekernel \
  --pattern-id PATTERN_UX_002
```

Implemented behavior:

1. Loads and validates an existing learning note.
2. Refuses notes that are not `promotion_status: "ready-for-human-review"`.
3. Refuses notes without `approved: true`.
4. Refuses unsafe rights (`metadata-only` and `short-excerpt`).
5. Writes proposals under `proposals/examples/` or `proposals/patterns/` by default.
6. Preserves source provenance, source hash, and learning-note path.
7. Marks proposals `proposal_status: review-required` and `source_text_stored: false`.
8. Does not move anything into `library/` or `patterns/` automatically.

See `docs/phase-12-human-review-import-bridge.md`.

## Phase 13 — Writing OS endgame

ProseKernel is a writing operating system for agents: retrieve taste, apply structure, detect slop, improve drafts, and preserve reusable lessons.

Definition of done:

- Handles most serious writing formats.
- Produces better first drafts than generic AI.
- Maintains a rights-safe corpus and pattern library.
- Has evals that prove improvement.
- Offers agent-ready CLI and Markdown outputs.
- Learns only with explicit public-safe review.
