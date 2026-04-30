# ProseKernel

Taste infrastructure for AI writing agents.

ProseKernel is an open-source writing operating system for AI agents.

It helps agents retrieve strong writing examples, extract reusable craft patterns, build writing briefs, draft with structure, detect generic AI slop, rewrite with specificity and proof, and learn reusable lessons over time.

The system has four layers:

1. **Library** — annotated examples of excellent writing across formats.
2. **Patterns** — reusable craft moves extracted from the examples.
3. **Doctrine** — rules for clear, specific, persuasive, human writing.
4. **Evals** — anti-slop checks that catch fake significance, generic claims, weak proof, and AI cadence.

ProseKernel preserves source metadata, summarizes what matters, extracts craft concepts, connects related ideas, and turns writing knowledge into reusable operating rules for agents.

## Why this exists

Most AI writing is not bad because it is grammatically wrong. It is bad because it is:

- generic
- over-smoothed
- overconfident without proof
- inflated with fake importance
- formatted like an answer instead of written like a human
- full of phrases no serious writer would choose

ProseKernel is designed to make future agents pause, study, retrieve relevant examples, and write with taste.

## How agents should use this repo

Before writing anything important:

1. Read `docs/doctrine.md`.
2. Open `LIBRARY.md` and find 3-5 relevant examples.
3. Read the example annotations, not just the excerpts.
4. Extract structure and craft moves. Do **not** copy phrases.
5. Draft.
6. Run the anti-slop checklist in `docs/anti-slop.md`.
7. Score the draft with `evals/writing-scorecard.md`.

## Current status

Phase 12 is the official v1 endgame: ProseKernel now covers the full writing operating-system loop for agents — task understanding, retrieval, patterns, briefs, critique, rewrite, explanation, public-safe learning, and a human-review/import bridge. Later work is organized as Post-v1 Tracks, not new numbered phases.

Phase 12 human-review/import bridge is implemented: approved, safe-rights learning notes can generate review-required example and pattern proposals with `propose-example` and `propose-pattern`; nothing is imported automatically into `library/` or `patterns/`.

Phase 11 public-safe learning loop is implemented: `learn` creates metadata-only learning notes from drafts without storing source prose, `validate-learning` checks the learning directory, and promotion requests are blocked unless rights and explicit approval are safe.

Phase 10 productized CLI/usability is implemented: `critique` and `rewrite` produce deterministic Markdown reports for existing drafts, `rewrite --rewrite-output` can also save the rewritten draft as a standalone file, and shorter aliases (`examples`, `demo`, `score`) preserve existing command contracts while making common flows easier to run.

Phase 9 agent workflow integration is implemented: repo-local `SKILL.md`, reusable prompt contracts, and command-grounded agent docs package the workflow for Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents.

Phase 8 retrieval is implemented: `search-examples`, `brief`, `write`, and `write-demo` default to the existing deterministic lexical/category scorer, and can opt into `--mode semantic` or `--mode hybrid`. Hybrid retrieval remains offline and dependency-free, using curated concept aliases, category concepts, simple stemming, and cached semantic token expansion. `search-examples --explain` prints lexical/semantic/hybrid score components.

Seed corpus includes examples/resources across:

- viral/social writing
- persuasive copywriting
- strategic/intelligent writing
- essay/literary craft
- technical/explanatory writing
- brand/positioning writing

Seed examples now exist for email/newsletters, speeches/oratory, journalism/reportage, UX/product microcopy, crisis communications, and internal ops docs.

This is intentionally high-signal. Quality beats volume.

Corpus depth rule: one example gives a direction; three to five examples create a pattern; ten examples create taste.

## Quick CLI

The repo also includes CLI tools for common AI-slop markers, deterministic/hybrid retrieval, critique/rewrite reports, drafting demos, and Phase 7A scorecards/evals:

```bash
python -m pip install -e .
prosekernel lint examples/ai-slop-sample.md
prosekernel search-examples "write a launch email for ProseKernel"
prosekernel examples "write a launch email for ProseKernel"
prosekernel search-examples "write a security incident update for customers" --mode hybrid --explain
prosekernel brief "write a launch email for ProseKernel" --output /tmp/prosekernel-brief.md
prosekernel critique draft.md --task "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-critique.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-rewrite.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --output /tmp/prosekernel-rewrite-report.md --rewrite-output /tmp/prosekernel-rewritten.md
prosekernel learn draft.md --task "write a launch email for ProseKernel" --source-title "Launch draft" --source-author "User" --source-url "https://example.com/launch-draft" --rights user-provided --category email-newsletters --tags "launch, email" --promote --approved --output /tmp/prosekernel-lesson.md
prosekernel validate-learning
prosekernel propose-example /tmp/prosekernel-lesson.md --root /root/prosekernel --output /tmp/prosekernel-example-proposal.md
prosekernel propose-pattern /tmp/prosekernel-lesson.md --root /root/prosekernel --pattern-id PATTERN_EMAIL_999 --output /tmp/prosekernel-pattern-proposal.md
prosekernel write "write a launch email for ProseKernel" --provider openai --model gpt-4o-mini --output /tmp/prosekernel-write.md
prosekernel write-demo "write a launch email for ProseKernel" --output /tmp/prosekernel-demo.md
prosekernel demo "write a launch email for ProseKernel" --output /tmp/prosekernel-demo.md
prosekernel scorecard draft.md --task "write a launch email for ProseKernel" --output /tmp/prosekernel-scorecard.md
prosekernel score draft.md --task "write a launch email for ProseKernel"
prosekernel eval
```

Root-aware commands resolve the ProseKernel repo/data root in this order: explicit `--root`, `PROSEKERNEL_ROOT`, then an upward search from the current directory for `pyproject.toml`, `library/`, `patterns/`, and `src/prosekernel`. If installed usage cannot find those assets, ProseKernel fails with a clear setup message instead of returning empty retrieval results.

## Core standard

Good ProseKernel writing must be:

- **clear** — the reader understands the point fast
- **specific** — claims have names, numbers, examples, or scenes
- **alive** — it sounds like a person with judgment wrote it
- **persuasive** — structure fits reader awareness and desired action
- **honest** — no fake certainty, fake citations, or inflated importance


## Public source policy

ProseKernel teaches structure, taste, and craft. It is not a copyrighted text mirror.

For modern copyrighted writing, default to:

- source metadata
- source URL
- rights classification
- short excerpt only when legally appropriate
- original craft analysis
- reusable pattern
- imitation prompt

See `docs/legal-source-policy.md`, `docs/source-ingestion.md`, and `CONTRIBUTING.md`.

## Roadmap

See `ROADMAP.md` and `docs/v1-definition-of-done.md`. The official numbered roadmap ends at Phase 12: public readiness → corpus depth → patterns → basic evals → LLM adapter → hybrid retrieval → agent workflow → productized CLI → public-safe learning loop → human-review/import bridge → v1 Writing OS endgame. Later work belongs in Post-v1 Tracks for structured outputs, CI/release hardening, public distribution, evaluation maturity, library/pattern scale, provider support, and optional product surfaces.

## Source ingestion

Use `docs/source-ingestion.md` and `prosekernel new-example` to add new examples safely and consistently. Run `prosekernel validate-library` before committing.

## Retrieval + writing demo

Use `docs/retrieval-writing-demo.md` for the current workflow: task → category recommendation → example retrieval → craft move extraction → draft scaffold → anti-slop lint → scorecard → rewrite/report. Use `docs/phase-12-human-review-import-bridge.md` for generating review-required example/pattern proposals from approved learning notes. Use `docs/phase-11-public-safe-learning-loop.md` for metadata-only learning notes and safe promotion gates. Use `docs/phase-10-productized-cli.md` for deterministic critique/rewrite reports, standalone rewrite outputs, exit-code semantics, and short CLI aliases. Use `docs/phase-8-hybrid-retrieval.md` for optional offline semantic/hybrid retrieval modes. Use `docs/phase-9-agent-workflow.md` and `docs/agent-workflow.md` for the full agent loop: classify → retrieve → patterns → brief → draft → lint/score → revise → explain. Use `docs/phase-7a-evals.md` for the fixture suite and scorecard CLI. Use `docs/phase-6-brief-mode.md` for the provider-agnostic dry-run brief mode and `docs/phase-6b-provider-write.md` for explicit provider write mode.
