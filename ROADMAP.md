# ProseKernel Roadmap

ProseKernel is an open-source writing operating system for AI agents.

It helps agents retrieve strong writing examples, extract reusable craft patterns, build writing briefs, draft with structure, detect generic AI slop, rewrite with specificity and proof, and learn reusable lessons over time.

Short positioning: **Taste infrastructure for AI writing agents.**

ProseKernel is not a generic AI writing app, prompt library, personal writing system, private taste vault, web UI product, or only an anti-slop linter. The core product is a public, open-source, agent-friendly CLI and knowledge layer.

## Current status

Completed:

- Phase 1 — Foundation and initial corpus.
- Phase 2 — Taxonomy expansion and deterministic retrieval demo.
- Phase 3 — Seed expanded categories.
- Phase 3.5 — Public release readiness metadata/docs.
- Phase 4 — Corpus depth expansion: 100 annotated examples across 12 populated categories, with eight priority categories at 10-example taste depth.
- Phase 5 — Initial strict pattern layer: 12 `PATTERN_*.md` families, example `pattern_ids`, and retrieval/demo output that cites pattern IDs.
- Phase 6A — Provider-agnostic dry-run brief mode: `prosekernel brief` builds an agent-ready writing packet without model/API calls.
- Phase 6B — Explicit provider write mode: adapter interface, `prosekernel write --provider ... --model ...`, safe missing-credential errors, and provider/model trace reports.
- Phase 7A — Deeper basic evals: six-dimension scorecard implementation, weak/strong fixtures, `scorecard` CLI, `eval` CLI, and write-demo score improvement reports.
- Phase 8 — Offline semantic/hybrid retrieval: optional `--mode semantic|hybrid`, score explanations, cached concept expansion, and no new runtime dependencies.
- Phase 9 — Agent workflow integration: repo-local `SKILL.md`, prompt contracts, and command-grounded workflow docs for Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents.
- Phase 10 — Productized CLI/usability: `critique`, `rewrite`, productized Markdown reports, standalone rewrite outputs, exit-code docs, and friendlier aliases (`examples`, `demo`, `score`).
- Phase 11 — Public-safe learning loop: `learn` metadata-only learning notes, `validate-learning`, source-text exclusion checks, and rights/approval gates for promotion.
- Phase 12 — Endgame: Writing Operating System. Human-review/import bridge plus the full agent loop from task understanding to brief, critique, rewrite, explanation, and safe learning.

Current corpus: 100 annotated examples across 12 populated categories.
Current pattern layer: 12 strict pattern families.
Current eval layer: 6 benchmark tasks plus 12 weak/strong fixture drafts.
Current adapter layer: dry-run `brief` mode plus explicit provider-backed `write` mode. No default paid provider is selected; writes require explicit `--provider` and `--model`.
Current retrieval layer: default lexical/category scoring plus optional offline semantic and hybrid scoring.
Current release-hardening layer: root resolution, CI, validation hardening, old-brand scan, install docs, and v1 smoke-loop tests are complete.
Current editorial architecture layer: `prosekernel shape` diagnoses AI-looking document structure with deterministic rules, situated structure archetypes, shape scorecards, Markdown reports, and rewrite instructions.

## Phase 1 — Foundation and initial corpus

Status: implemented.

Established the repo structure, public positioning, first annotated writing examples, doctrine, anti-slop rules, tests, and CLI foundation.

## Phase 2 — Taxonomy expansion and deterministic retrieval demo

Status: implemented.

Added task classification, deterministic retrieval, and the first retrieval → craft moves → draft scaffold → lint/rewrite demo loop.

## Phase 3 — Seed expanded categories

Status: implemented.

Expanded the corpus beyond the initial writing modes and added more category scaffolding for public usefulness.

## Phase 3.5 — Public release readiness metadata/docs

Status: implemented.

Added public metadata, contributor docs, roadmap, quality bar, source policy, pattern schema, and release-readiness documentation.

## Phase 4 — Corpus depth

Status: implemented.

Goal: expand from representation to taste.

Implemented:

- 100 annotated examples across 12 populated categories.
- Eight priority categories at 10-example taste depth.
- Rights-safe metadata, source URLs, and original craft analysis.

Principle:

> One example gives a direction. Three to five examples create a pattern. Ten examples create taste.

## Phase 5 — Pattern extraction layer

Status: implemented.

Goal: turn examples into reusable intelligence.

Patterns are not summaries. They are agent-executable writing moves.

Implemented:

- 12 strict pattern files in `patterns/`.
- Pattern IDs linked from examples.
- Retrieval and demo output that cites pattern IDs.
- Validation of known pattern IDs.

Each pattern follows `docs/pattern-schema.md`:

- pattern ID
- use when
- reader situation
- structure
- why it works
- examples
- anti-patterns
- agent instruction

## Phase 6 — LLM-backed drafting adapter

Status: implemented.

Goal: make ProseKernel draft, not just brief, while staying provider-agnostic.

Phase 6A implemented:

- `prosekernel brief` dry-run command.
- Provider-neutral writing brief object and Markdown renderer.
- Strict pattern instructions pulled from `patterns/PATTERN_*.md`.
- Quality gate instructions for lint + scorecard.
- `docs/phase-6-brief-mode.md`.

Phase 6B implemented:

- Explicit provider adapter protocol in `src/prosekernel/providers.py`.
- Initial OpenAI, OpenRouter, and Anthropic HTTP adapters using stdlib HTTP calls.
- `prosekernel write --provider ... --model ...`.
- No-default-provider refusal path to prevent accidental paid calls.
- Missing-credential errors that name the exact env var and confirm no API call was made.
- Write reports with provider/model trace, retrieved examples, pattern IDs, draft, lint, scorecard, and quality gate.
- `docs/phase-6b-provider-write.md`.

## Phase 7A — Basic eval tasks and scorecards

Status: implemented.

Implemented:

- `evals/writing-scorecard.md` for the human-readable rubric.
- `evals/tasks/*.md` for benchmark task prompts.
- `evals/fixtures/weak/*.md` and `evals/fixtures/strong/*.md` for regression fixtures.
- `src/prosekernel/evals.py` for deterministic scorecard scoring.
- `prosekernel scorecard draft.md --task "..."` for draft scoring.
- `prosekernel eval` for weak/strong fixture regression tests.
- `write-demo` reports that include scorecard improvement by dimension.

Eval dimensions:

- specificity
- proof
- structure
- reader fit
- memorability
- non-genericness

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

ProseKernel is agent-ready for Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents.

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

See `docs/phase-11-public-safe-learning-loop.md`.

## Phase 12 — Endgame: Writing Operating System

Status: implemented.

At Phase 12, ProseKernel becomes a complete writing operating system for AI agents.

It can:

1. Understand the writing job.
2. Identify the reader, format, and intent.
3. Retrieve relevant examples.
4. Retrieve relevant patterns.
5. Build a writing brief.
6. Draft in the correct structure.
7. Detect generic AI slop.
8. Rewrite with specificity, proof, rhythm, and taste.
9. Explain why the piece works.
10. Learn reusable lessons from the result through explicit public-safe review.

Phase 12 also adds the final bridge between learning and corpus curation:

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

### v1 Definition of Done

ProseKernel v1 is complete when a user can install it, run it on a serious writing task, receive a structured brief / critique / rewrite report, and understand why the output is better than a generic LLM draft.

Concretely, a user can:

1. Install the package.
2. Run it on a serious writing task.
3. Generate a writing brief.
4. Generate or evaluate a draft.
5. Receive a structured critique.
6. Receive a rewrite.
7. See the examples and patterns used.
8. Understand why the output improved.
9. Run validation and tests successfully.

v1 does not require:

- web UI
- MCP server
- editor plugin
- local model support
- hundreds of examples
- automatic library growth
- fully automated corpus growth
- complex benchmark suite

See `docs/v1-definition-of-done.md`.

## Stop Building Rule

Do not expand the roadmap just because more features are possible.

ProseKernel should be considered v1-complete when it can reliably help an agent produce a better writing brief, critique, and rewrite than a generic LLM workflow.

After that, new work must fit into one of the Post-v1 Tracks and should improve stability, distribution, evaluation, or clearly demonstrated user value.

## Post-v1 Tracks

After Phase 12, ProseKernel is considered v1-complete.

Further work is organized into tracks, not numbered phases. These tracks are for hardening, distribution, and optional expansion.

Recommended practical priority:

1. Track H — Editorial Architecture — Implemented first because the immediate user pain was AI-looking document structure
2. Track A — Structured Outputs / Agent API — Planned
3. Track B — CI, Release, and Package Hardening — Mostly implemented / release hardening in progress
4. Track C — Public Distribution — In progress
5. Track D — Evaluation Maturity — Later
6. Track E — Library and Pattern Scale — Later
7. Track F — Provider and Local Model Support — Optional
8. Track G — Product Surfaces — Experimental

Do not jump immediately into web UI, MCP server, editor plugins, local models, huge benchmark systems, automatic corpus growth, or a 200+ example corpus. The project should become stable and shippable before becoming bigger.

### Track A — Structured Outputs / Agent API

Status: Planned

Goal: make ProseKernel easy for agents and automation tools to consume.

Planned work:

- JSON output for `brief`
- JSON output for `critique`
- JSON output for `rewrite`
- JSON output for `learn`
- JSON output for `eval`
- Stable schemas for machine-readable reports
- Better report objects for Codex, Claude Code, Cursor, OpenCode, Hermes, and future agent workflows

Future structured output mode should support commands like:

```bash
prosekernel brief "Write a launch email for an AI writing tool" --json
prosekernel critique draft.md --json
prosekernel rewrite draft.md --json
prosekernel learn final.md --json
```

JSON outputs should include stable fields such as:

- task
- inferred writing type
- audience
- examples used
- patterns used
- critique
- scores
- rewrite
- rationale
- warnings
- next actions

Why this matters:

- Agents need structured outputs, not only Markdown.
- JSON outputs make ProseKernel easier to use in automated workflows.
- This should be the first post-v1 hardening track.

### Track B — CI, Release, and Package Hardening

Status: Mostly implemented / release hardening in progress

Goal: make the repo stable, testable, and ready for public release.

Planned / completed work:

Completed:

- GitHub Actions
- Run tests on pull requests
- Validate library files
- Validate learning notes
- Run old-brand scan
- Clean install docs
- Public-release checklist
- v1 smoke-loop tests
- Validation hardening for learning notes and proposal generation
- Root resolution for installed and repo-local CLI usage

Remaining or later:

- Validate pattern files
- Run schema checks
- Add versioning
- Prepare release artifacts
- Prepare PyPI publishing

Why this matters:

- This is not feature bloat.
- This makes the repo credible and safe for public use.
- This should happen before major public distribution.

### Track C — Public Distribution

Status: In progress

Goal: make ProseKernel easy for other people to install, understand, and try.

Planned work:

- PyPI package
- Clean install docs
- Demo repo or examples folder
- Example reports
- Quickstart guide
- “Use ProseKernel with Claude Code” guide
- “Use ProseKernel with Codex” guide
- “Use ProseKernel with Cursor” guide
- “Use ProseKernel with OpenCode” guide
- “Use ProseKernel with Hermes” guide
- Launch README improvements
- 3 strong public demos

Public launch should happen after:

1. v1 definition of done is satisfied.
2. Structured outputs are planned or partially implemented.
3. CI checks pass.
4. Install docs are clear.
5. At least 3 strong demos exist.
6. Old-brand references are cleaned up or documented.

Why this matters:

- Distribution matters more than adding more features too early.
- The project should become shippable before expanding into more surfaces.

### Track D — Evaluation Maturity

Status: Later

Goal: prove that ProseKernel-guided writing is better than generic LLM writing.

Planned work:

- Larger benchmark task set
- Strong / weak fixture pairs
- Regression scoring by writing category
- Generic LLM draft vs ProseKernel-guided draft comparison
- Human-readable scorecards
- Category-specific evals

Why this matters:

- Without evals, quality claims are vibes.
- With evals, ProseKernel becomes an improving system.

### Track E — Library and Pattern Scale

Status: Later

Goal: grow the corpus and pattern system carefully without reducing quality.

Planned work:

- Grow beyond 100 examples only when quality can be maintained
- Add more pattern families
- Add stronger category-specific taste depth
- Improve source provenance
- Add duplicate detection
- Keep rights checks fail-closed
- Improve category indexes

Why this matters:

- Better examples create better retrieval.
- But low-quality scale will weaken the project.
- 80 excellent examples are better than 300 loose examples.

### Track F — Provider and Local Model Support

Status: Optional

Goal: support deeper model workflows without making the project dependent on one provider.

Planned work:

- Optional local model provider
- Provider config profiles
- Multi-pass critique / rewrite loops
- Model-specific adapter settings
- OpenAI / Anthropic / OpenRouter / local model support where appropriate

Why this matters:

- Provider flexibility is useful.
- But it is not required for v1.
- Most users first need to see that ProseKernel improves writing quality.

### Track G — Product Surfaces

Status: Experimental

Goal: explore additional interfaces only after the CLI and agent workflow prove useful.

Possible surfaces:

- CLI-only pro tool
- MCP server
- web UI
- editor plugin
- agent skill pack
- Obsidian integration
- local dashboard

Why this matters:

- These surfaces may become useful later.
- They should not distract from making the core CLI and agent workflow excellent.

### Track H — Editorial Architecture

Status: implemented.

Goal: detect and repair AI-looking document structure, not just weak sentences.

Track H was prioritized before Track A because the immediate user pain was AI-looking document structure: drafts that had polished sentences but inherited the default article or proposal skeleton.

Implemented:

1. `prosekernel shape` diagnostic command.
2. Deterministic structure lint for generic article/proposal ladders.
3. Situated structure archetypes selected from task, reader, intent, and channel.
4. One-sentence paragraph overuse detection.
5. Em dash and repeated contrast formula detection.
6. Generic signposting, weak ending, fake completeness, and topic-container heading detection.
7. Shape scorecards with reader fit, intent fit, structure originality, judgment, rhythm, heading quality, ending strength, and reversed AI template risk.
8. Markdown shape reports with rewrite instructions for agents.

Non-goals:

- No new numbered phase.
- No web UI.
- No MCP server.
- No editor plugin.
- No local model support.
- No full JSON output in the first version.
- No framing as making AI writing undetectable.
